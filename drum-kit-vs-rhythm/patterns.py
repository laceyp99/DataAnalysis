"""Beat positions used to render and display the drum loops."""

# One-indexed beats within each bar. Each tuple is (kick positions, hat positions).
PATTERNS = {
    "p1": ((1, 3), (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5)),
    "p2": ((1, 2.5, 3.75), (1.5, 2.5, 3.5, 4.5)),
    "p3": ((1, 1.75, 3, 4.5), (1, 2, 2.5, 3, 4, 4.5)),
    "p4": ((1, 2, 3, 4), (1.5, 1.75, 2.5, 3.5, 3.75, 4.5, 4.75)),
}
SNARE_PARTS = {"3": (3,), "24": (2, 4), "13": (1, 3)}
