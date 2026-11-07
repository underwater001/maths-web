"""Triangles: classification, medians/cevian theorems, and the incentre/circumcentre/orthocentre
family. Quiz tier — new topic, filed from Rakesh Yadav Ch17 (Geometry)."""
from topics._ch17tr_ry import PYQS_RY as PYQS_C17TR

TOPIC = "triangles"
PREFIX = "tr"
TIER = "quiz"

NODES = {
    "c-tr-classify": {"short": "Classify by sides", "label": "Acute, right or obtuse from the three sides", "kind": "concept", "parent": TOPIC, "order": 1,
                      "summary": "Compare the square of the longest side with the sum of the squares of the other two — that alone tells you the triangle's angle type.", "links": []},
    "q-tr-classify": {"short": "Classify a triangle", "label": "Decide acute / right / obtuse from three side lengths or a ratio", "kind": "qtype", "parent": "c-tr-classify", "order": 1,
                      "summary": "Given three sides (or a ratio of sides), say whether the triangle is acute-, right- or obtuse-angled.", "links": []},
    "c-tr-cevian": {"short": "Medians & cevians", "label": "Medians, bisectors and parallel-line segments", "kind": "concept", "parent": TOPIC, "order": 2,
                    "summary": "Special segments inside a triangle — medians (meeting at the centroid, split 2:1), the angle bisector (splits the opposite side in the ratio of the adjacent sides), and any line parallel to a side (cuts the other two sides in the same ratio).", "links": []},
    "q-tr-median-hyp": {"short": "Median to the hypotenuse", "label": "Median to the hypotenuse of a right triangle", "kind": "qtype", "parent": "c-tr-cevian", "order": 1,
                        "summary": "The median from the right angle to the hypotenuse is always half the hypotenuse.", "links": []},
    "q-tr-equilateral-seg": {"short": "Equilateral triangle segments", "label": "Inradius, circumradius and median of an equilateral triangle", "kind": "qtype", "parent": "c-tr-cevian", "order": 2,
                             "summary": "In an equilateral triangle these three special lengths are all fixed multiples of each other.", "links": []},
    "q-tr-median-perp": {"short": "Perpendicular medians", "label": "Two medians meeting at right angles", "kind": "qtype", "parent": "c-tr-cevian", "order": 3,
                         "summary": "Split each median 2 : 1 at the centroid, then use the right angle between them with Pythagoras.", "links": []},
    "q-tr-bisector": {"short": "Angle bisector theorem", "label": "Internal bisector splitting the opposite side", "kind": "qtype", "parent": "c-tr-cevian", "order": 4,
                      "summary": "An internal angle bisector splits the opposite side in the same ratio as the two adjacent sides.", "links": []},
    "q-tr-parallel": {"short": "Line parallel to a side", "label": "Basic proportionality (Thales) theorem", "kind": "qtype", "parent": "c-tr-cevian", "order": 5,
                      "summary": "A line parallel to one side of a triangle cuts the other two sides proportionally — use it to find a missing segment.", "links": []},
    "c-tr-centers": {"short": "Triangle centres", "label": "Incentre, circumcentre and orthocentre", "kind": "concept", "parent": TOPIC, "order": 3,
                     "summary": "The incentre gives a clean angle formula (∠BOC = 90° + A/2). Where the orthocentre or circumcentre sits (inside, on a vertex/side, or outside) tells you the triangle's type.", "links": []},
    "q-tr-incentre": {"short": "Incentre angle", "label": "∠BOC = 90° + A/2 at the incentre", "kind": "qtype", "parent": "c-tr-centers", "order": 1,
                      "summary": "Given two angles (or the vertex angle A directly), find the angle the incentre makes with the other two vertices, or run the formula backwards.", "links": []},
    "q-tr-center-facts": {"short": "Centre-position facts", "label": "What a centre's special position tells you", "kind": "qtype", "parent": "c-tr-centers", "order": 2,
                          "summary": "Orthocentre = centroid ⟺ equilateral. Orthocentre on a vertex ⟺ right-angled there. Circumcentre outside ⟺ obtuse.", "links": []},
}
FORMULAS = [
    {"id": "tr-f1", "node": "c-tr-classify", "text": "For sides a ≤ b ≤ c: c² < a² + b² acute, c² = a² + b² right-angled, c² > a² + b² obtuse", "note": "Only the longest side's square needs comparing — the common factor in a ratio like 3:4:6 cancels out."},
    {"id": "tr-f2", "node": "c-tr-cevian", "text": "In a right triangle, the median from the right-angle vertex to the hypotenuse = half the hypotenuse", "note": "Equivalent to: the right-angle vertex lies on the circle with the hypotenuse as diameter, and the median is a radius."},
    {"id": "tr-f3", "node": "c-tr-cevian", "text": "Equilateral triangle: circumradius R = 2 × inradius r; and r = (median)/3 (the centroid splits each median 2 : 1)", "note": "So a median = 3r = 1.5R — any one of the three (side, R, r, median) gives the other three."},
    {"id": "tr-f4", "node": "c-tr-cevian", "text": "The centroid splits every median 2 : 1 from the vertex", "note": "Needed whenever a question gives a whole median's length but the working needs the centroid's two pieces separately (e.g. two perpendicular medians)."},
    {"id": "tr-f5", "node": "c-tr-cevian", "text": "Angle bisector theorem: if AD bisects ∠A meeting BC at D, then BD : DC = AB : AC", "note": "Works in either direction — from the side ratio to BD/DC, or from BD/DC to the side ratio."},
    {"id": "tr-f6", "node": "c-tr-cevian", "text": "Basic proportionality (Thales) theorem: if PQ ∥ BC with P on AB and Q on AC, then AP/PB = AQ/QC, and also AP/AB = AQ/AC = PQ/BC", "note": "Pick whichever of the two ratio forms matches what the question gives — part:part, or part:whole."},
    {"id": "tr-f7", "node": "c-tr-centers", "text": "Incentre O of △ABC: ∠BOC = 90° + ∠A/2 (and cyclically ∠AOC = 90° + ∠B/2, ∠AOB = 90° + ∠C/2)", "note": "Works forwards (given angles, find the incentre angle) or backwards (given the incentre angle, find a vertex angle)."},
    {"id": "tr-f8", "node": "c-tr-centers", "text": "Orthocentre = centroid ⟺ the triangle is equilateral. Orthocentre lies on a vertex ⟺ the triangle is right-angled there. Circumcentre lies outside the triangle ⟺ the triangle is obtuse-angled", "note": "All four classical centres (centroid, incentre, circumcentre, orthocentre) coincide only in the equilateral case."},
]
METHODS = {
    "q-tr-classify": {
        "cue": "'The sides of a triangle are … (or are in the ratio …). The triangle is:' with acute/right/obtuse as options.",
        "formulas": ["tr-f1"], "tech": ["identity"],
        "standard": "Square the largest side and compare it with the sum of the squares of the other two.",
        "fast": "With a ratio, just compare the squares of the ratio numbers directly — the scale factor cancels.",
        "eliminate": "If the comparison is close to equal, check for a Pythagorean triple (3-4-5, 6-8-10, 5-12-13, …) first.",
        "traps": ["Comparing the wrong side as 'largest'.", "Mixing up the inequality direction (bigger sum-of-squares means acute, not obtuse).", "Forgetting a ratio's common factor cancels, so the raw ratio numbers can be compared directly."]},
    "q-tr-median-hyp": {
        "cue": "Three side lengths are given (often a Pythagorean triple) and the question asks for the median to the largest/greatest side.",
        "formulas": ["tr-f1", "tr-f2"], "tech": ["standard-values"],
        "standard": "Confirm the triangle is right-angled (largest² = sum of other two squares), then the median to the hypotenuse is simply half of it.",
        "fast": "Recognise the triple (6-8-10, 3-4-5, 5-12-13, …) on sight — the median is then just half the largest number.",
        "eliminate": "The answer must be exactly half the given largest side; rule out anything that isn't.",
        "traps": ["Giving a leg's length instead of half the hypotenuse.", "Computing the altitude to the hypotenuse (leg₁×leg₂/hypotenuse) instead of the median.", "Not checking first that the triangle actually is right-angled."]},
    "q-tr-equilateral-seg": {
        "cue": "'Circumradius of an equilateral triangle is …, find the inradius' or '…inradius is …, find the median' (or side).",
        "formulas": ["tr-f3"], "tech": ["standard-values"],
        "standard": "Use R = 2r and r = median/3 to convert directly between whichever two of {R, r, median, side} the question involves.",
        "fast": "Memorise the chain: median = 3r = 1.5R — one multiplication or division solves it.",
        "eliminate": "r must be smaller than R (specifically R = 2r exactly) and smaller than the median (r = median/3) — options that break this ratio are wrong.",
        "traps": ["Mixing up which of R and r is bigger (R is always twice r, never the other way round).", "Using the general-triangle inradius formula (Area/semi-perimeter) when the direct equilateral-triangle ratio is much faster.", "Confusing the median with the full height split 1:1 instead of 2:1."]},
    "q-tr-median-perp": {
        "cue": "Two medians are given to intersect 'at right angles' (or 'perpendicularly') at the centroid, and a segment like BD (half a side) is asked for.",
        "formulas": ["tr-f4"], "tech": ["standard-values", "identity"],
        "standard": "Split each median 2 : 1 at the centroid to get the two legs of a right triangle at G, then apply Pythagoras for the needed side.",
        "fast": "Once the two centroid-pieces come out as a recognisable triple (like 3-4-5), the hypotenuse is immediate.",
        "eliminate": "Using the full medians as the right-triangle legs (instead of their 2:1 pieces) gives a much bigger, wrong number — a good sign the split was skipped.",
        "traps": ["Using the whole median lengths as the legs instead of splitting 2:1 at the centroid.", "Mixing up which piece (2/3 or 1/3) belongs to which vertex.", "Forgetting BD is HALF of BC, not the full side, if BC itself were asked for instead."]},
    "q-tr-bisector": {
        "cue": "'AD is the internal bisector of ∠A, meeting BC at D' with two of BD, DC, BC given, asking for AB : AC (or vice versa).",
        "formulas": ["tr-f5"], "tech": ["identity"],
        "standard": "Find the missing piece of BC if needed (BC − given piece), then AB : AC = BD : DC directly.",
        "fast": "If BD and BC are given, DC = BC − BD falls out in one subtraction before applying the theorem.",
        "eliminate": "The ratio must simplify the same way BD : DC does — options that don't reduce to that exact ratio are wrong.",
        "traps": ["Inverting the ratio (DC : BD instead of BD : DC, or vice versa, depending which side the question asks first).", "Using BD : BC or DC : BC instead of BD : DC.", "Forgetting to subtract from BC to get the missing piece before forming the ratio."]},
    "q-tr-parallel": {
        "cue": "'A line parallel to BC intersects AB and AC at P and Q' with a mix of segment lengths given, one of which may be unknown and shared with another via a condition like AP = QC.",
        "formulas": ["tr-f6"], "tech": ["identity"],
        "standard": "Write the proportion AP/PB = AQ/QC (or the part:whole form AP/AB = AQ/AC = PQ/BC, whichever matches what's given) and solve for the unknown.",
        "fast": "When the unknown appears on both sides of the proportion (like AP = QC), it often collapses to a mean-proportional square root.",
        "eliminate": "A ratio answer (like 'AC = 3×AQ') should be checked by confirming AP:AB equals the same ratio as AQ:AC — if not, the wrong pair of segments was used.",
        "traps": ["Mixing up the part:part form (AP/PB) with the part:whole form (AP/AB).", "Using the wrong vertex's segments (B's instead of C's, or vice versa).", "Not spotting a mean-proportional setup when the same unknown appears in two places."]},
    "q-tr-incentre": {
        "cue": "'I (or O) is the incentre of △ABC' with either two base angles given (find ∠BIC) or the vertex angle A given (find ∠BOC), or the reverse (∠BOC given, find ∠A).",
        "formulas": ["tr-f7"], "tech": ["identity"],
        "standard": "Find ∠A (from 180° minus the other two, if not given directly), then apply ∠BOC = 90° + ∠A/2 — or solve this same equation for ∠A if ∠BOC is what's given.",
        "fast": "If ∠A is given directly, skip the triangle-angle-sum step entirely and halve it straight into the formula.",
        "eliminate": "∠BOC must always be between 90° and 180° (since 0° < A < 180°) — an option outside that range is wrong immediately.",
        "traps": ["Using ∠A alone, or ∠A/2 alone, instead of 90° + ∠A/2.", "Forgetting to subtract from 180° to get ∠A when only the other two angles are given.", "When running the formula backwards, forgetting to double (∠A/2 vs ∠A) after subtracting 90°."]},
    "q-tr-center-facts": {
        "cue": "A qualitative fact about where a named centre (orthocentre, circumcentre) sits — 'the orthocentre and centroid are the same', 'the orthocentre lies on a vertex', 'the circumcentre lies outside the triangle' — asking for the triangle's type.",
        "formulas": ["tr-f8"], "tech": ["identity"],
        "standard": "Match the stated position directly to the known fact: centres coincide ⟺ equilateral; orthocentre on a vertex ⟺ right-angled there; circumcentre outside ⟺ obtuse-angled.",
        "fast": "These are pure recall — no computation, just matching the position to the triangle type.",
        "eliminate": "A scalene or isosceles option (with nothing more specific stated) is never the match for any of these special positions.",
        "traps": ["Confusing the orthocentre's special positions with the circumcentre's (they are opposite in the obtuse case: orthocentre moves further outside, circumcentre also outside, but 'on a vertex' is specifically an orthocentre/right-angle fact).", "Thinking any isosceles triangle has coinciding centres — only equilateral does.", "Mixing up 'inside' (acute) and 'outside' (obtuse) for the circumcentre."]},
}
PYQS = PYQS_C17TR


def practice_items():
    return []
