"""Polygons and quadrilaterals: quiz tier."""
from bank import bound, mistake, pyq
from topics._ch17pg_ry import PYQS_RY as PYQS_C17PG

TOPIC = "polygons"
PREFIX = "pg"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-pg-angles": {"short": "Angle sums", "label": "Angle sum of a polygon", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "The angles of a quadrilateral add to 360°. In a cyclic quadrilateral opposite angles add to 180°.", "links": ["lines-angles"]},
    "q-pg-ratio": {"short": "Angles in a ratio", "label": "Angles in a given ratio", "kind": "qtype", "parent": "c-pg-angles", "order": 1,
                   "summary": "Four angles in a ratio like 1 : 3 : 4 : 4; find the largest or smallest.", "links": []},
    "c-pg-regular": {"short": "Regular polygons", "label": "Interior/exterior angles of a regular polygon", "kind": "concept", "parent": TOPIC, "order": 2,
                      "summary": "Every exterior angle of a regular n-gon is 360°/n, and it pairs with its interior angle to 180°. The angle sum is (n−2)×180°.", "links": []},
    "q-pg-sides": {"short": "Sides from an angle fact", "label": "Find n from an angle condition", "kind": "qtype", "parent": "c-pg-regular", "order": 1,
                   "summary": "Given a ratio, a sum, or an interior-angle value for a regular polygon, find (or rule out) the number of sides.", "links": []},
    "c-pg-cyclic": {"short": "Cyclic quadrilaterals", "label": "Cyclic quadrilateral and trapezium facts", "kind": "concept", "parent": TOPIC, "order": 3,
                    "summary": "A cyclic trapezium is always an isosceles trapezium, so its base angles are equal. An exterior angle of any cyclic quadrilateral equals the interior angle at the opposite vertex.", "links": []},
    "q-pg-cyclic": {"short": "Trapezium & exterior angle", "label": "Cyclic trapezium base angles, or the exterior-angle rule", "kind": "qtype", "parent": "c-pg-cyclic", "order": 1,
                    "summary": "Find a base angle of a cyclic trapezium, or the interior opposite angle from a given exterior angle.", "links": []},
    "c-pg-rhombus": {"short": "Rhombus", "label": "Angles and diagonals of a rhombus", "kind": "concept", "parent": TOPIC, "order": 4,
                     "summary": "Opposite angles of a rhombus are equal and adjacent angles are supplementary. A diagonal splits it into two triangles with two equal sides (the rhombus's sides), solvable with the cosine rule.", "links": []},
    "q-pg-rhombus": {"short": "Angle or diagonal", "label": "Find a rhombus angle or diagonal", "kind": "qtype", "parent": "c-pg-rhombus", "order": 1,
                     "summary": "Given one angle (or a ratio of two angles), find another angle or a diagonal's length.", "links": []},
}
FORMULAS = [
    {"id": "pg-f1", "node": "c-pg-angles", "text": "Sum of the angles of an n-sided polygon = (n − 2) × 180°", "note": "Quadrilateral: 360°."},
    {"id": "pg-f2", "node": "c-pg-angles", "text": "Cyclic quadrilateral: opposite angles add to 180°", "note": "Use it as a check or as the main step when two angles are given."},
    {"id": "pg-f3", "node": "c-pg-regular", "text": "Exterior angle of a regular n-gon = 360°/n; interior + exterior = 180°; sum of interior angles = (n − 2) × 180°", "note": "Any one of these, plus whatever the question gives (a ratio, a sum, a single angle), pins down n — and n must come out a whole number ≥ 3."},
    {"id": "pg-f4", "node": "c-pg-cyclic", "text": "Cyclic trapezium (AD ∥ BC) is isosceles: the base angles at B and C are equal, so ∠BCD = ∠ABC directly", "note": "A trapezium that is also cyclic has no freedom left — it must be isosceles."},
    {"id": "pg-f5", "node": "c-pg-cyclic", "text": "Exterior angle of a cyclic quadrilateral = interior angle at the opposite vertex", "note": "Not the same-vertex interior angle (that one is merely supplementary to the exterior angle)."},
    {"id": "pg-f6", "node": "c-pg-rhombus", "text": "Rhombus: opposite angles equal, adjacent angles supplementary; a diagonal BD in triangle ABD (sides AB = AD) gives BD² = 2·AB²·(1 − cos∠A)", "note": "∠A here is the angle between the two sides meeting at the diagonal's own vertex, not the angle given at B or C — convert first with the supplementary-angles rule."},
]
METHODS = {
    "q-pg-ratio": {
        "cue": "'The angles of a quadrilateral are in the ratio …'; find the biggest or smallest angle.",
        "formulas": ["pg-f1", "pg-f2"], "tech": ["ratio-parts", "cancel-first"],
        "standard": "Ratio parts add to 1 + 3 + 4 + 4 = 12. One part = 360° ÷ 12 = 30°. Largest = 4 × 30° = 120°.",
        "fast": "360 ÷ 12 = 30 is clean, so every angle is a multiple of 30°. Only the multiples of 30 can be an answer.",
        "eliminate": "The largest angle's share is 4/12 = 1/3 of 360° = 120°. Options that are not multiples of 30 (108°, 135°) are out; 90° is the 3-part angle.",
        "traps": ["Using 180° instead of 360° (opposite angles are 180° but the whole sum is 360°).", "Picking the 3-part angle (90°) as the largest.", "Pairing opposite angles and getting inconsistent ratios; the question is solved from the angle sum alone."]},
    "q-pg-sides": {
        "cue": "'The exterior and interior angles are in the ratio …', 'the sum of the interior angles is …°', or 'which of these can never be an interior angle?'",
        "formulas": ["pg-f3"], "tech": ["ratio-parts", "back-substitute", "divisibility"],
        "standard": "Turn whatever is given into the exterior angle (or n − 2), then use n = 360°/exterior or n = sum/180° + 2.",
        "fast": "For a 'can never be' question, just check whether 180° − (the angle) divides 360° exactly — if not, that angle is impossible.",
        "eliminate": "n must be a whole number at least 3; throw out any angle or ratio that gives a fraction or a value under 3.",
        "traps": ["Mixing up the interior and exterior angle in the ratio.", "Forgetting the '+2' (or '−2') when going between the angle sum and n.", "For the impossible-angle question, checking only one option instead of all four."]},
    "q-pg-cyclic": {
        "cue": "'ABCD is a cyclic trapezium…' asking for the other base angle, or 'an exterior angle of a cyclic quadrilateral is …°, find the interior opposite angle'.",
        "formulas": ["pg-f4", "pg-f5"], "tech": ["symmetry", "identity"],
        "standard": "For the trapezium: recognise it must be isosceles, so the two base angles on the same parallel side are equal — no further computation. For the exterior-angle question: the interior opposite angle simply equals the given exterior angle.",
        "fast": "Both facts are direct equalities — there is nothing to compute once the rule is recalled.",
        "eliminate": "180° minus the given angle is the trap answer in both cases (confusing 'opposite' with 'same vertex', or the ordinary co-interior angle rule) — rule it out.",
        "traps": ["Treating the base angles as supplementary (180° − angle) instead of equal.", "Using the exterior angle = same-vertex interior angle's supplement instead of the opposite vertex's interior angle.", "Forgetting that only a trapezium that is ALSO cyclic is guaranteed isosceles."]},
    "q-pg-rhombus": {
        "cue": "'ABCD is a rhombus … ∠A : ∠B = …' or '… side AB = … cm and ∠ABC = …°, find diagonal BD/AC'.",
        "formulas": ["pg-f6"], "tech": ["ratio-parts", "identity", "standard-values"],
        "standard": "For an angle: split 180° by the given ratio, then use equal-opposite-angles. For a diagonal: find the angle at the diagonal's own vertex (180° minus the given adjacent angle), then apply the cosine rule with the two equal sides.",
        "fast": "If the angle at the diagonal's vertex works out to 60°, the triangle on that diagonal is equilateral — the diagonal equals the side, no cosine rule needed.",
        "eliminate": "The diagonal must be less than twice the side and (for angle < 180°) more than 0; options far outside that range are out.",
        "traps": ["Using the given angle directly in the cosine rule instead of its supplement at the diagonal's own vertex.", "Confusing ∠C (opposite, equal to ∠A) with ∠D (adjacent, supplementary to ∠A).", "For the diagonal, forgetting the cosine rule needs the INCLUDED angle between the two known sides."]},
}
PYQS = [
    pyq(S2, 72, "q-pg-ratio", "The angles of a cyclic quadrilateral are in the ratio 1 : 3 : 4 : 4. What is the largest angle?", ["90°", "108°", "120°", "135°"], "c",
        ["The four angles add to 360°, and the ratio parts add to 1 + 3 + 4 + 4 = 12.", "One part = 360° ÷ 12 = 30°.", "The largest angle = 4 × 30° = 120°. (Strictly, no pairing of these angles gives opposite sums of 180°, so the question only works with the 360° sum.)"],
        lambda: 360 / 12 * 4, 120, 0, tech=["ratio-parts", "divisibility"], trick="360 ÷ 12 = 30, so every angle is a multiple of 30. Only 90° and 120° are, and 90° is the 3-part angle.",
        wrong={"a": mistake("90° is the angle with 3 parts, not the largest.", 90), "b": bound("Parts of 30° give multiples of 30°, and 108° is not one.", lambda v: v % 30 != 0), "d": bound("Parts of 30° give multiples of 30°, and 135° is not one.", lambda v: v % 30 != 0)}),
]

PYQS = PYQS + PYQS_C17PG


def practice_items():
    return []
