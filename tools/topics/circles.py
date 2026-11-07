"""Circles: tangent and chord theorems. Quiz tier — new topic, filed from Rakesh Yadav Ch17 (Geometry)."""
from topics._ch17ci_ry import PYQS_RY as PYQS_C17CI

TOPIC = "circles"
PREFIX = "ci"
TIER = "quiz"

NODES = {
    "c-ci-tangent": {"short": "Tangents", "label": "Tangent-length and tangent-chord facts", "kind": "concept", "parent": TOPIC, "order": 1,
                     "summary": "A radius is perpendicular to the tangent at the point of contact. The tangent-chord angle equals the inscribed angle in the alternate segment.", "links": []},
    "q-ci-tangent-len": {"short": "Tangent length", "label": "Length of a tangent segment via a right angle at the centre", "kind": "qtype", "parent": "c-ci-tangent", "order": 1,
                         "summary": "Two external points and the centre form a right triangle (when the angle at the centre is given as 90°) — Pythagoras gives the distance between them.", "links": []},
    "q-ci-tangent-chord": {"short": "Tangent-chord angle", "label": "Angle between a tangent and a chord", "kind": "qtype", "parent": "c-ci-tangent", "order": 2,
                           "summary": "The angle between a tangent and a chord drawn from the point of contact equals the inscribed angle subtended by that chord in the alternate segment.", "links": []},
    "c-ci-chord": {"short": "Chords", "label": "Chord-chord angles and chords of concentric circles", "kind": "concept", "parent": TOPIC, "order": 2,
                   "summary": "Two chords crossing inside a circle make an angle equal to half the sum of the two arcs they cut off. A chord of a bigger circle tangent to a smaller, concentric circle is split in half by the point of tangency.", "links": []},
    "q-ci-chord-angle": {"short": "Angle between two chords", "label": "Angle where two chords intersect inside a circle", "kind": "qtype", "parent": "c-ci-chord", "order": 1,
                         "summary": "Given the two central angles for the arcs the chords cut off, find the angle between the chords.", "links": []},
    "q-ci-semicircle": {"short": "Right angle → diameter", "label": "A 90° inscribed angle marks a diameter", "kind": "qtype", "parent": "c-ci-chord", "order": 2,
                        "summary": "If a chord subtends 90° at a point on the circle, that chord is a diameter — converse of the angle-in-a-semicircle theorem.", "links": []},
    "q-ci-concentric-chord": {"short": "Chord tangent to inner circle", "label": "Chord of the outer circle tangent to the inner, concentric circle", "kind": "qtype", "parent": "c-ci-chord", "order": 3,
                              "summary": "Half the chord, the inner radius and the outer radius form a right triangle — the chord is 2√(R² − r²).", "links": []},
    "q-ci-parallel-chord": {"short": "Distance between parallel chords", "label": "Gap between two parallel chords", "kind": "qtype", "parent": "c-ci-chord", "order": 4,
                            "summary": "Each chord's distance from the centre is √(r² − (half-chord)²); add or subtract these depending on whether the chords are on opposite or the same side.", "links": []},
}
FORMULAS = [
    {"id": "ci-f1", "node": "c-ci-tangent", "text": "The radius to a point of tangency is perpendicular to the tangent there", "note": "This right angle is what turns a tangent-length question into a plain Pythagoras problem."},
    {"id": "ci-f2", "node": "c-ci-tangent", "text": "Tangent-chord angle = inscribed angle in the alternate segment", "note": "The chord is the one drawn FROM the point of tangency; 'alternate segment' means the arc on the far side of that chord from the tangent angle."},
    {"id": "ci-f3", "node": "c-ci-chord", "text": "Angle between two chords meeting inside a circle = ½ (sum of the two arcs cut off), equivalently ½ (sum of the two central angles for those arcs)", "note": "The two arcs are the ones between the chords' endpoints on each side of the intersection — not the whole circle."},
    {"id": "ci-f4", "node": "c-ci-chord", "text": "An inscribed angle of 90° always subtends a diameter (converse of the angle-in-a-semicircle theorem)", "note": "So if ∠BAC = 90° with A on the circle, BC must be a diameter — radius = BC/2."},
    {"id": "ci-f5", "node": "c-ci-chord", "text": "A chord of a circle of radius R, tangent to a concentric circle of radius r, has length 2√(R² − r²)", "note": "The point of tangency bisects the chord, and the inner radius there is perpendicular to it."},
    {"id": "ci-f6", "node": "c-ci-chord", "text": "A chord of length L in a circle of radius r sits at distance √(r² − (L/2)²) from the centre", "note": "Two parallel chords: add the two distances if they're on opposite sides of the centre, subtract if on the same side."},
]
METHODS = {
    "q-ci-tangent-len": {
        "cue": "A tangent line touches the circle at one point while two OTHER points (often where the tangent meets other lines) have their distances from the centre given, along with the angle between those two distances AT the centre.",
        "formulas": ["ci-f1"], "tech": ["identity"],
        "standard": "If the angle at the centre between the two given distances is 90°, the triangle formed by the centre and the two points is right-angled there — apply Pythagoras directly for the segment joining them.",
        "fast": "Don't be distracted by the radius if the centre-angle is already 90° — the two given distances ARE the legs of the right triangle you need.",
        "eliminate": "The answer must be bigger than either given distance alone (it's a hypotenuse) — rule out anything smaller.",
        "traps": ["Trying to use the radius in the main computation when the 90°-at-the-centre shortcut doesn't need it.", "Adding the two distances instead of combining them via Pythagoras.", "Subtracting instead of using the Pythagorean sum."]},
    "q-ci-tangent-chord": {
        "cue": "'PAT is the tangent at A' (or similar) together with a chord from A and another angle inside the triangle formed with a third point on the circle.",
        "formulas": ["ci-f2"], "tech": ["identity"],
        "standard": "Identify the tangent-chord angle, set it equal to the inscribed angle in the alternate segment, then finish with the ordinary triangle angle sum.",
        "fast": "The tangent-chord equality hands you one triangle angle immediately — the rest is just 180° minus the two known angles.",
        "eliminate": "The three triangle angles found this way must add to exactly 180° — a quick check catches a misapplied tangent-chord step.",
        "traps": ["Applying the tangent-chord angle to the wrong chord (there are two chords from the point of tangency in some figures).", "Confusing the alternate segment with the same-side segment.", "Forgetting that the final step is still an ordinary triangle angle sum."]},
    "q-ci-chord-angle": {
        "cue": "Two chords (or lines through the circle) cross inside the circle, and TWO central angles are given (∠AOC, ∠BOD style), asking for the angle at the crossing point.",
        "formulas": ["ci-f3"], "tech": ["identity"],
        "standard": "Add the two given central angles and halve the result.",
        "fast": "It's literally (angle 1 + angle 2)/2 — no triangle construction needed.",
        "eliminate": "The answer must be less than either central angle's sum and typically less than 90° in these problems — a much bigger number signals a setup error.",
        "traps": ["Halving only one of the two given angles.", "Using the difference of the two angles instead of their sum (that's the formula for chords meeting OUTSIDE the circle, a different case).", "Adding an unrelated extra term."]},
    "q-ci-semicircle": {
        "cue": "Two chords from the same point are given, with the angle between them stated as 90°, asking for the circle's radius.",
        "formulas": ["ci-f4"], "tech": ["standard-values"],
        "standard": "Recognise that the chord opposite the 90° angle must be a diameter; find its length by Pythagoras from the two given chords, then halve for the radius.",
        "fast": "Spot a Pythagorean triple among the two given chords (6-8-10, 3-4-5, …) — the diameter is the triple's third number.",
        "eliminate": "The radius must be less than either given chord's length — an option bigger than both given chords is wrong.",
        "traps": ["Reporting the diameter instead of the radius (forgetting to halve).", "Reporting the square of the diameter instead of the diameter itself.", "Halving the wrong chord instead of the computed diameter BC."]},
    "q-ci-concentric-chord": {
        "cue": "'Concentric circles' with two different radii, and a chord of the BIGGER one that is tangent to the SMALLER one.",
        "formulas": ["ci-f5"], "tech": ["standard-values"],
        "standard": "Compute √(R² − r²) for the half-chord using the right triangle formed by the two radii and the half-chord, then double it.",
        "fast": "Spot the Pythagorean triple in R and r directly (9-12-15 is a scaled 3-4-5, etc.) — the half-chord drops out immediately.",
        "eliminate": "The chord must be less than 2R (the full diameter of the outer circle) — an option at or above that is wrong.",
        "traps": ["Reporting the half-chord instead of doubling it for the full chord.", "Swapping R and r inside the square root.", "Adding R and r instead of using √(R²−r²)."]},
    "q-ci-parallel-chord": {
        "cue": "Two parallel chords are given (same length or different lengths) together with either the gap between them (find the radius) or the radius (find the gap), and whether they're on the same or opposite sides of the centre.",
        "formulas": ["ci-f6"], "tech": ["standard-values", "identity"],
        "standard": "Find each chord's distance from the centre with √(r² − (half-chord)²), then combine: ADD the two distances if the chords are on opposite sides of the centre, SUBTRACT if they're on the same side.",
        "fast": "Equal-length chords on opposite sides are symmetric — just double the one distance you need.",
        "eliminate": "A 'same side' gap must be smaller than either chord's own distance from the centre; an 'opposite sides' gap must be bigger than either one alone.",
        "traps": ["Adding when the chords are on the same side (should subtract) or vice versa.", "Forgetting to halve the chord length before using it in √(r² − (L/2)²).", "Mixing up which of two different-length chords is closer to the centre (the longer chord is always closer)."]},
}
PYQS = PYQS_C17CI


def practice_items():
    return []
