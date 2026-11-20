"""Render the fixed two-bar listening stimuli and write their manifest."""

import csv
from itertools import product
from math import gcd
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly
import soundfile as sf


ROOT = Path(__file__).resolve().parent
SAMPLE_RATE = 24_000
BPM = 120
SAMPLES_PER_BEAT = 60 * SAMPLE_RATE // BPM
BEATS_PER_BAR = 4
BAR_COUNT = 2
CLIP_FRAMES = BAR_COUNT * BEATS_PER_BAR * SAMPLES_PER_BEAT
TAIL_LIMIT = 18_000  # 750 ms
TAIL_FADE = 600  # 25 ms
END_FADE = 240  # 10 ms
PEAK_LIMIT = 0.85

# One-indexed beats within each bar. Each tuple is (kick positions, hat positions).
PATTERNS = {
    "p1": ((1, 3), (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5)),
    "p2": ((1, 2.5, 3.75), (1.5, 2.5, 3.5, 4.5)),
    "p3": ((1, 1.75, 3, 4.5), (1, 2, 2.5, 3, 4, 4.5)),
    "p4": ((1, 2, 3, 4), (1.5, 1.75, 2.5, 3.5, 3.75, 4.5, 4.75)),
}
SNARE_PARTS = {"3": (3,), "24": (2, 4), "13": (1, 3)}

# Linear kick, snare and closed-hat gains. Reused in every clip for each kit.
KIT_GAINS = {
    "virtuosity": (24.0, 3.0, 16.0),
    "black-pearl": (0.55, 0.50, 1.2),
    "red-zeppelin": (0.55, 0.73, 1.2),
    "phazite": (0.85, 0.90, 0.80),
}


def load_hit(kit, instrument, gain):
    source = ROOT / "samples" / kit / f"{instrument}.flac"
    channels, rate = sf.read(source, always_2d=True)
    divisor = gcd(rate, SAMPLE_RATE)
    mono = resample_poly(channels.mean(axis=1), SAMPLE_RATE // divisor, rate // divisor)
    magnitude = np.abs(mono)
    peak = magnitude.max()
    if not np.isfinite(peak) or peak == 0:
        raise ValueError(f"Invalid one-shot: {source}")

    attack = np.flatnonzero(magnitude >= 0.02 * peak)[0]
    hit = mono[attack:] * gain
    if len(hit) > TAIL_LIMIT:
        hit = hit[:TAIL_LIMIT]
        hit[-TAIL_FADE:] *= np.linspace(1, 0, TAIL_FADE)
    return hit


def mix_clip(hits, kick_beats, snare_beats, hat_beats):
    clip = np.zeros(CLIP_FRAMES)
    for hit, beats in zip(hits, (kick_beats, snare_beats, hat_beats), strict=True):
        for bar in range(BAR_COUNT):
            for beat in beats:
                start = round((bar * BEATS_PER_BAR + beat - 1) * SAMPLES_PER_BEAT)
                end = min(start + len(hit), CLIP_FRAMES)
                clip[start:end] += hit[: end - start]
    clip[-END_FADE:] *= np.linspace(1, 0, END_FADE)
    return clip


def main():
    kit_hits = {
        kit: tuple(
            load_hit(kit, instrument, gain)
            for instrument, gain in zip(("kick", "snare", "hat"), gains, strict=True)
        )
        for kit, gains in KIT_GAINS.items()
    }
    mixes = {}
    for pattern, snare, kit in product(PATTERNS, SNARE_PARTS, KIT_GAINS):
        kick_beats, hat_beats = PATTERNS[pattern]
        mixes[pattern, snare, kit] = mix_clip(
            kit_hits[kit], kick_beats, SNARE_PARTS[snare], hat_beats
        )

    gain = PEAK_LIMIT / max(np.abs(clip).max() for clip in mixes.values())
    audio = ROOT / "audio"
    audio.mkdir(exist_ok=True)
    fields = ("clip_id", "pattern", "snare", "kit", "path", "common_gain")
    with (ROOT / "manifest.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for (pattern, snare, kit), clip in mixes.items():
            clip_id = f"{pattern}_{snare}_{kit}"
            path = audio / f"{clip_id}.wav"
            sf.write(path, clip * gain, SAMPLE_RATE, subtype="PCM_16")
            writer.writerow({
                "clip_id": clip_id,
                "pattern": pattern,
                "snare": snare,
                "kit": kit,
                "path": path.relative_to(ROOT).as_posix(),
                "common_gain": f"{gain:.12g}",
            })
    print(f"Rendered {len(mixes)} clips, {CLIP_FRAMES} frames each at {SAMPLE_RATE} Hz.")


if __name__ == "__main__":
    main()
