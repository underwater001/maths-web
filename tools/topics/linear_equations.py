"""Linear equations: quiz tier."""
import re
from bank import bound, mistake, pyq
from topics._ch16l_ry import PYQS_RY as PYQS_C16L

TOPIC = "linear-equations"
PREFIX = "le"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-le-point": {"short": "Point on a line", "label": "A point lies on a line when it satisfies the equation", "kind": "concept", "parent": TOPIC, "order": 1,
                   "summary": "Put the point's x and y into the equation. If both sides agree, the point is on the line.", "links": []},
    "q-le-point": {"short": "Point on a line", "label": "Substitute a point into a line", "kind": "qtype", "parent": "c-le-point", "order": 1,
                   "summary": "Find an unknown in the equation, or pick the option point that lies on the line.", "links": []},
    "c-le-system": {"short": "Lines together", "label": "Two or three lines drawn together", "kind": "concept", "parent": TOPIC, "order": 2,
                    "summary": "Where two lines cross is the point satisfying both equations; three lines taken in pairs enclose a triangle whose area can be read from the crossing points.", "links": ["mensuration-2d"]},
    "q-le-system": {"short": "Intersection & enclosed area", "label": "Where lines meet, and the triangle they enclose", "kind": "qtype", "parent": "c-le-system", "order": 1,
                    "summary": "Solve a pair of equations for their crossing point, or find the area of the triangle three lines form.", "links": []},
}
FORMULAS = [
    {"id": "le-f1", "node": "c-le-point", "text": "Point (p, q) is on ax + by = c  ⇔  a·p + b·q = c", "note": "For y = mx + c put y = q and x = p and solve for the unknown."},
    {"id": "le-f2", "node": "c-le-system", "text": "Solve two linear equations by elimination or substitution to find their one crossing point. x = k and y = m are a vertical and a horizontal line, crossing at (k, m).", "note": "Lines like x = 4 and y = 3 are often two sides of a triangle already — their crossing point is a vertex and the two legs can be read straight off."},
]
METHODS = {
    "q-le-point": {
        "cue": "'The line … passes through (…)' with one unknown, or 'which point lies on the line?'",
        "formulas": ["le-f1"], "tech": ["back-substitute", "plug-numbers"],
        "standard": "Replace x and y by the point's coordinates and solve the one equation left.",
        "fast": "For options, test the point with the smallest numbers first. 3x + 2y = 12: (2, 3) gives 6 + 6 = 12 straight away.",
        "eliminate": "Check the parity or a unit digit: 3x + 2y = 12 is even and 2y is even, so 3x must be even, so x must be even. That removes (1, 6) and (1, 4) at once.",
        "traps": ["Swapping x and y.", "Subtracting 7 but forgetting to divide by x (13 − 7 = 6, not 3).", "Testing only one option and stopping before checking that the others fail."]},
    "q-le-system": {
        "cue": "'The lines … intersect at the point' or 'the area of the triangle formed by the graphs of …'.",
        "formulas": ["le-f2"], "tech": ["back-substitute", "identity"],
        "standard": "Solve any two of the equations simultaneously to get each crossing point, then use those points (or two of the lines as legs) to find the area.",
        "fast": "If two of the three lines are x = k and y = m, they are already a vertical and a horizontal leg of the triangle — the area is just half their lengths' product.",
        "eliminate": "Check a candidate crossing point in both original equations before using it further.",
        "traps": ["Solving the wrong pair of equations for a given vertex.", "Forgetting the ½ in the triangle-area formula.", "Mixing up which two lines give the two legs of a right triangle."]},
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

PYQS = PYQS + PYQS_C16L


def practice_items():
    return []
