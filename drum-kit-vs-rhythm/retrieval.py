import csv
from pathlib import Path


def read_similarities():
    with Path(__file__).with_name("loop-similarities.csv").open(newline="") as file:
        reader = csv.reader(file)
        ids = next(reader)[1:]
        rows = list(reader)
    if [row[0] for row in rows] != ids or any(len(row) != len(ids) + 1 for row in rows):
        raise ValueError("Expected a square similarity matrix with matching clip IDs.")
    return ids, [[float(value) for value in row[1:]] for row in rows]


def retrieval_summary(ids, scores):
    clips = [clip.rsplit("_", 1) for clip in ids]
    same_kit = exact_cross_kit = 0
    for i, (performance, kit) in enumerate(clips):
        ranked = sorted((j for j in range(len(ids)) if j != i),
                        key=scores[i].__getitem__, reverse=True)
        same_kit += clips[ranked[0]][1] == kit
        closest_other = next(j for j in ranked if clips[j][1] != kit)
        exact_cross_kit += clips[closest_other][0] == performance

    n = len(ids)
    return (f"The closest loop used the same kit for {same_kit} of {n} references. "
            f"When we excluded that kit, the exact kick, snare and hi-hat pattern ranked "
            f"first for {exact_cross_kit} of {n} references ({exact_cross_kit / n:.1%}).")
