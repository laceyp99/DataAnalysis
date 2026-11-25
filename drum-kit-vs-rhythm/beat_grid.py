"""One-bar rhythm diagrams for the two listening reports."""


from urllib.parse import quote

from patterns import PATTERNS, SNARE_PARTS


def _row(label, beats, instrument):
    groups = []
    for beat in range(1, 5):
        cells = []
        for step in range(4):
            active = beat + step / 4 in beats
            cells.append('<i class="hit"></i>' if active else '<i></i>')
        groups.append('<span class="beat">' + ''.join(cells) + '</span>')
    return f'<div class="step-row {instrument}"><span>{label}</span>{"".join(groups)}</div>'


def pattern_grid(pattern, snare):
    kicks, hats = PATTERNS[pattern]
    rows = (("Hi-hat", hats, "hat"), ("Snare", SNARE_PARTS[snare], "snare"),
            ("Kick", kicks, "kick"))
    description = "; ".join(f"{name}: {', '.join(map(str, beats))}" for name, beats, _ in rows)
    counts = '<div class="step-row counts"><span></span>' + ''.join(
        f'<span>{beat}</span>' for beat in range(1, 5)
    ) + '</div>'
    return (
        f'<figure class="steps score-grid" role="img" aria-label="Pattern {pattern[1:]}. {description}">'
        f'<figcaption>Pattern {pattern[1:]}</figcaption>'
        + ''.join(_row(*row) for row in rows) + counts + '</figure>'
    )


def header_grid():
    # Tile the margins with all four performances, one three-instrument band per pattern.
    marks = []
    for band, (kicks, hats) in enumerate(PATTERNS.values()):
        for row, (hits, color) in enumerate(((hats, "#81978b"), (SNARE_PARTS["24"], "#b46236"),
                                             (kicks, "#408579"))):
            for step in range(16):
                fill = color if 1 + step / 4 in hits else "#e1e4db"
                marks.append(f'<rect x="{step*12}" y="{band*42+row*12}" width="10" height="10" '
                             f'rx="2" fill="{fill}"/>')
    tile = '<svg xmlns="http://www.w3.org/2000/svg" width="192" height="168">' + ''.join(marks) + '</svg>'
    backdrop = f"<style>body{{--study-pattern:url('data:image/svg+xml,{quote(tile)}')}}</style>"
    return (backdrop + '<div class="pattern-atlas"><div class="atlas-title">Four backing patterns'
            ' <span>120 BPM &middot; snare on 2 and 4</span></div><div class="pattern-panels">'
            + ''.join(pattern_grid(pattern, "24") for pattern in PATTERNS) + '</div></div>')
