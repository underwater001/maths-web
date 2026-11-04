"""Polygons and quadrilaterals: quiz tier."""
from bank import bound, mistake, pyq

TOPIC = "polygons"
PREFIX = "pg"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-pg-angles": {"short": "Angle sums", "label": "Angle sum of a polygon", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "The angles of a quadrilateral add to 360°. In a cyclic quadrilateral opposite angles add to 180°.", "links": ["lines-angles"]},
    "q-pg-ratio": {"short": "Angles in a ratio", "label": "Angles in a given ratio", "kind": "qtype", "parent": "c-pg-angles", "order": 1,
                   "summary": "Four angles in a ratio like 1 : 3 : 4 : 4; find the largest or smallest.", "links": []},
}
FORMULAS = [
    {"id": "pg-f1", "node": "c-pg-angles", "text": "Sum of the angles of an n-sided polygon = (n − 2) × 180°", "note": "Quadrilateral: 360°."},
    {"id": "pg-f2", "node": "c-pg-angles", "text": "Cyclic quadrilateral: opposite angles add to 180°", "note": "Use it as a check or as the main step when two angles are given."},
]
METHODS = {
    "q-pg-ratio": {
        "cue": "'The angles of a quadrilateral are in the ratio …'; find the biggest or smallest angle.",
        "formulas": ["pg-f1", "pg-f2"], "tech": ["ratio-parts", "cancel-first"],
        "standard": "Ratio parts add to 1 + 3 + 4 + 4 = 12. One part = 360° ÷ 12 = 30°. Largest = 4 × 30° = 120°.",
        "fast": "360 ÷ 12 = 30 is clean, so every angle is a multiple of 30°. Only the multiples of 30 can be an answer.",
        "eliminate": "The largest angle's share is 4/12 = 1/3 of 360° = 120°. Options that are not multiples of 30 (108°, 135°) are out; 90° is the 3-part angle.",
        "traps": ["Using 180° instead of 360° (opposite angles are 180° but the whole sum is 360°).", "Picking the 3-part angle (90°) as the largest.", "Pairing opposite angles and getting inconsistent ratios; the question is solved from the angle sum alone."]},
}
PYQS = [
    pyq(S2, 72, "q-pg-ratio", "The angles of a cyclic quadrilateral are in the ratio 1 : 3 : 4 : 4. What is the largest angle?", ["90°", "108°", "120°", "135°"], "c",
        ["The four angles add to 360°, and the ratio parts add to 1 + 3 + 4 + 4 = 12.", "One part = 360° ÷ 12 = 30°.", "The largest angle = 4 × 30° = 120°. (Strictly, no pairing of these angles gives opposite sums of 180°, so the question only works with the 360° sum.)"],
        lambda: 360 / 12 * 4, 120, 0, tech=["ratio-parts", "divisibility"], trick="360 ÷ 12 = 30, so every angle is a multiple of 30. Only 90° and 120° are, and 90° is the 3-part angle.",
        wrong={"a": mistake("90° is the angle with 3 parts, not the largest.", 90), "b": bound("Parts of 30° give multiples of 30°, and 108° is not one.", lambda v: v % 30 != 0), "d": bound("Parts of 30° give multiples of 30°, and 135° is not one.", lambda v: v % 30 != 0)}),
]


def practice_items():
    return []
