"""Linear equations: quiz tier."""
import re
from bank import bound, mistake, pyq

TOPIC = "linear-equations"
PREFIX = "le"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-le-point": {"short": "Point on a line", "label": "A point lies on a line when it satisfies the equation", "kind": "concept", "parent": TOPIC, "order": 1,
                   "summary": "Put the point's x and y into the equation. If both sides agree, the point is on the line.", "links": []},
    "q-le-point": {"short": "Point on a line", "label": "Substitute a point into a line", "kind": "qtype", "parent": "c-le-point", "order": 1,
                   "summary": "Find an unknown in the equation, or pick the option point that lies on the line.", "links": []},
}
FORMULAS = [
    {"id": "le-f1", "node": "c-le-point", "text": "Point (p, q) is on ax + by = c  ⇔  a·p + b·q = c", "note": "For y = mx + c put y = q and x = p and solve for the unknown."},
]
METHODS = {
    "q-le-point": {
        "cue": "'The line … passes through (…)' with one unknown, or 'which point lies on the line?'",
        "formulas": ["le-f1"], "tech": ["back-substitute", "plug-numbers"],
        "standard": "Replace x and y by the point's coordinates and solve the one equation left.",
        "fast": "For options, test the point with the smallest numbers first. 3x + 2y = 12: (2, 3) gives 6 + 6 = 12 straight away.",
        "eliminate": "Check the parity or a unit digit: 3x + 2y = 12 is even and 2y is even, so 3x must be even, so x must be even. That removes (1, 6) and (1, 4) at once.",
        "traps": ["Swapping x and y.", "Subtracting 7 but forgetting to divide by x (13 − 7 = 6, not 3).", "Testing only one option and stopping before checking that the others fail."]},
}


def _pt(t):
    x, y = map(int, re.findall(r"\d+", t)); return x, y


PYQS = [
    pyq(S1, 74, "q-le-point", "The line y = mx + 7 passes through the point (2, 13). Find m.", ["2", "3", "6", "5"], "b",
        ["Put x = 2 and y = 13: 13 = 2m + 7.", "2m = 6, so m = 3."],
        lambda: (13 - 7) / 2, 3, 0, tech=["back-substitute"], trick="Try the options: 2 × 3 + 7 = 13 is the only one that works.",
        wrong={"a": mistake("Gave the x-coordinate (2) instead of solving.", 2), "c": mistake("Subtracted 7 but forgot to divide by x = 2: 13 − 7 = 6.", 6)}),
    pyq(S2, 75, "q-le-point", "The line 3x + 2y = 12 passes through which of the following points?", ["(2, 3)", "(4, 1)", "(1, 6)", "(1, 4)"], "a",
        ["(2, 3): 3×2 + 2×3 = 6 + 6 = 12. Yes.", "(4, 1): 12 + 2 = 14. (1, 6): 3 + 12 = 15. (1, 4): 3 + 8 = 11. None of these is 12."],
        lambda: 1, 1, 0, tech=["back-substitute", "divisibility"], optvals=[1 if 3 * _pt(t)[0] + 2 * _pt(t)[1] == 12 else 0 for t in ("(2, 3)", "(4, 1)", "(1, 6)", "(1, 4)")],
        trick="3x + 2y = 12 is even and 2y is even, so x must be even. Only (2, 3) and (4, 1) have an even x; (4, 1) gives 14.",
        wrong={"b": bound("3×4 + 2×1 = 14, not 12.", lambda v: v == 0), "c": bound("3×1 + 2×6 = 15, not 12.", lambda v: v == 0), "d": bound("3×1 + 2×4 = 11, not 12.", lambda v: v == 0)}),
]


def practice_items():
    return []
