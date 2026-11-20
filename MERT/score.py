"""Extract MERT frame vectors and score all four reference roles in each trial set."""

import csv
import hashlib
import io
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from tempfile import NamedTemporaryFile
import wave

import numpy as np
import torch
from transformers import AutoModel, Wav2Vec2FeatureExtractor


ROOT = Path(__file__).resolve().parent
MODEL = "m-a-p/MERT-v1-95M"
REVISION = "12af15fef9d0ac838c3f475bfbbf26d2060dd4f5"
SAMPLE_RATE = 24_000
SAMPLES_PER_CLIP = 96_000
FRAME_SHAPE = (299, 768)
PATTERNS = ("p1", "p2", "p3", "p4")
SNARE_PAIRS = (("3", "24"), ("13", "24"))
KIT_NAMES = ("virtuosity", "black-pearl", "red-zeppelin", "phazite")
TRIAL_COLUMNS = (
    "pattern", "snare", "kit", "other_snare", "other_kit", "group",
    "rhythm_score", "kit_score", "margin", "outcome", "aligned_margin", "aligned_outcome",
)


def read_samples(wav_bytes, clip_id):
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
        layout = (
            wav_file.getnchannels(), wav_file.getsampwidth(),
            wav_file.getframerate(), wav_file.getnframes(),
        )
        if layout != (1, 2, SAMPLE_RATE, SAMPLES_PER_CLIP):
            raise ValueError(f"{clip_id} must be four seconds of mono 24 kHz 16-bit PCM.")
        return np.frombuffer(wav_file.readframes(SAMPLES_PER_CLIP), dtype="<i2").astype(np.float32) / 32768


def check_frames(frames, clip_id):
    if frames.shape != FRAME_SHAPE or not np.isfinite(frames).all():
        raise ValueError(f"{clip_id} did not yield finite frame vectors of shape {FRAME_SHAPE}.")


def save_frames(path, frames):
    with NamedTemporaryFile(dir=path.parent, suffix=".npy", delete=False) as temporary:
        np.save(temporary, frames, allow_pickle=False)
    Path(temporary.name).replace(path)


def extract_frames():
    cache = ROOT / ".cache" / "mert-frames" / REVISION / "final"
    cache.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = model = None
    features = {}
    for clip in product(PATTERNS, ("3", "24", "13"), KIT_NAMES):
        clip_id = "_".join(clip)
        wav_bytes = (ROOT / "audio" / f"{clip_id}.wav").read_bytes()
        digest = hashlib.sha256(wav_bytes).hexdigest()
        cached_file = cache / f"{clip_id}-{digest}.npy"
        if cached_file.exists():
            frames = np.load(cached_file, allow_pickle=False)
            check_frames(frames, clip_id)
        else:
            samples = read_samples(wav_bytes, clip_id)
            if model is None:
                processor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL, revision=REVISION)
                model = AutoModel.from_pretrained(MODEL, revision=REVISION, trust_remote_code=True)
                model.eval().to(device)
            inputs = processor(samples, sampling_rate=SAMPLE_RATE, return_tensors="pt").to(device)
            with torch.inference_mode():
                frames = model(**inputs).last_hidden_state[0].cpu().numpy()
            check_frames(frames, clip_id)
            save_frames(cached_file, frames)
            print(f"{clip_id}: {frames.shape} on {device}", flush=True)
        features[clip] = frames.astype(np.float64)
    return features


def unit_vectors(vectors):
    length = np.linalg.norm(vectors, axis=-1, keepdims=True)
    if np.any(length == 0):
        raise ValueError("Cosine similarity requires nonzero vectors.")
    return vectors / length


def outcome(margin):
    if margin > 0:
        return "rhythm"
    if margin < 0:
        return "kit"
    return "tie"


def score_trials(features):
    pooled = {clip: unit_vectors(frames.mean(axis=0)) for clip, frames in features.items()}
    aligned = {clip: unit_vectors(frames) for clip, frames in features.items()}
    for pattern, snares, kits in product(PATTERNS, SNARE_PAIRS, combinations(KIT_NAMES, 2)):
        group = "electronic" if "phazite" in kits else "acoustic"
        for snare_index, kit_index in product(range(2), repeat=2):
            snare, other_snare = snares[snare_index], snares[1 - snare_index]
            kit, other_kit = kits[kit_index], kits[1 - kit_index]
            reference = (pattern, snare, kit)
            same_rhythm = (pattern, snare, other_kit)
            same_kit = (pattern, other_snare, kit)
            rhythm_score = float(pooled[reference] @ pooled[same_rhythm])
            kit_score = float(pooled[reference] @ pooled[same_kit])
            margin = rhythm_score - kit_score
            aligned_rhythm = np.einsum("ij,ij->i", aligned[reference], aligned[same_rhythm]).mean()
            aligned_kit = np.einsum("ij,ij->i", aligned[reference], aligned[same_kit]).mean()
            aligned_margin = float(aligned_rhythm - aligned_kit)
            yield (
                pattern, snare, kit, other_snare, other_kit, group,
                rhythm_score, kit_score, margin, outcome(margin), aligned_margin, outcome(aligned_margin),
            )


def main():
    features = extract_frames()
    rows = list(score_trials(features))
    groups = Counter(row[5] for row in rows)
    if groups != {"acoustic": 96, "electronic": 96} or len({row[:5] for row in rows}) != 192:
        raise ValueError(f"Expected 192 distinct trials, split 96 per group. Found {groups}.")

    with NamedTemporaryFile(mode="w", dir=ROOT, encoding="utf-8", newline="", delete=False) as temporary:
        writer = csv.writer(temporary, lineterminator="\n")
        writer.writerow(TRIAL_COLUMNS)
        writer.writerows(rows)
    Path(temporary.name).replace(ROOT / "trials.csv")
    print(f"Scored {len(rows)} trials across {len(features)} clips.")


if __name__ == "__main__":
    main()
