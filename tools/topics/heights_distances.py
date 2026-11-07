"""Heights and distances: elevation/depression word problems built on one right triangle, or on two
triangles sharing a side. Quiz tier — new topic, filed from Rakesh Yadav Ch22 (Height and Distance)."""
from topics._ch22hd_ry import PYQS_RY as PYQS_C22HD

TOPIC = "heights-distances"
PREFIX = "hd"
TIER = "quiz"

NODES = {
    "c-hd-basics": {"short": "One triangle", "label": "A single right triangle from one angle and one side", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "The oldest move in the chapter: one angle of elevation or depression and one known side give every other side by a plain trig ratio.", "links": []},
    "q-hd-single-triangle": {"short": "Single right triangle", "label": "Find the missing side of one right triangle", "kind": "qtype", "parent": "c-hd-basics", "order": 1,
                             "summary": "Given one angle and one side (opposite, adjacent, or the hypotenuse — a thread, a ladder, a line of sight), find any other side.", "links": []},

    "c-hd-shadow-ratio": {"short": "Shadow ratio", "label": "Height-to-shadow ratio at one instant", "kind": "concept", "parent": TOPIC, "order": 2,
                          "summary": "At the same moment the sun's angle is the same everywhere, so height:shadow is one fixed ratio across every object — and that ratio IS tan(elevation).", "links": []},
    "q-hd-shadow-ratio": {"short": "Shadow ratio", "label": "Shadow-length-to-height relationships", "kind": "qtype", "parent": "c-hd-shadow-ratio", "order": 1,
                          "summary": "Use one object's height:shadow ratio to find another's height, or read the sun's angle straight off a given ratio.", "links": []},

    "c-hd-two-angle-walk": {"short": "Walking toward/away", "label": "Elevation changes as the observer moves", "kind": "concept", "parent": TOPIC, "order": 3,
                            "summary": "The same fixed height is seen at two different angles from two points on the ground, a known distance apart on the same side of the foot.", "links": []},
    "q-hd-two-angle-walk": {"short": "Two-angle walk", "label": "Height or distance from a change in elevation while walking", "kind": "qtype", "parent": "c-hd-two-angle-walk", "order": 1,
                            "summary": "h(cotθ₁ − cotθ₂) equals the distance walked — solve for whichever of height or distance is missing.", "links": []},

    "c-hd-fixed-height-shift": {"short": "Fixed height, shifting shadow", "label": "A fixed height, the ground point shifts as the angle changes", "kind": "concept", "parent": TOPIC, "order": 4,
                                "summary": "The vertical height never changes; only the angle (sun's elevation, or a ladder's angle) does, so the horizontal distance shifts — find the height, or the amount of shift.", "links": []},
    "q-hd-fixed-height-shift": {"short": "Shadow / foot shift", "label": "Height from a shadow-length change, or the reverse", "kind": "qtype", "parent": "c-hd-fixed-height-shift", "order": 1,
                               "summary": "Exactly the same relation as the two-angle-walk type, read the other way: the SHIFT is given (or asked for) instead of the observer's own walk.", "links": []},

    "c-hd-complementary": {"short": "Complementary angles", "label": "Two points, complementary elevation angles", "kind": "concept", "parent": TOPIC, "order": 5,
                           "summary": "Two points on the line through a tower's foot see the top at angles that add to 90° — multiplying their two tangent expressions always collapses to height² = (distance 1)×(distance 2).", "links": []},
    "q-hd-complementary-geomean": {"short": "Geometric mean", "label": "Height as the geometric mean of two distances", "kind": "qtype", "parent": "c-hd-complementary", "order": 1,
                                  "summary": "height = √(a×b) the moment you see 'complementary' together with two given distances (or two other heights playing that role) on the same line as the tower.", "links": []},

    "c-hd-vertical-pair": {"short": "Stacked objects", "label": "Two objects on the same vertical line", "kind": "concept", "parent": TOPIC, "order": 6,
                           "summary": "One object sits directly above another (two aeroplanes on the same vertical), so both share the same horizontal distance from the ground observer.", "links": []},
    "q-hd-vertical-pair": {"short": "Shared base, two heights", "label": "Vertical gap between two stacked objects", "kind": "qtype", "parent": "c-hd-vertical-pair", "order": 1,
                           "summary": "One object's height is given; use its own angle to find the shared horizontal distance, then the other object's angle to get its height, and subtract.", "links": []},

    "c-hd-two-objects-between": {"short": "Point between two objects", "label": "An observer standing between two objects", "kind": "concept", "parent": TOPIC, "order": 7,
                                 "summary": "A single ground point between two vertical objects sees each at a different angle — the two objects may be equal in height, or in a stated ratio.", "links": []},
    "q-hd-equal-objects-between": {"short": "Equal objects, point between", "label": "Two equal-height objects, elevation from a point between them", "kind": "qtype", "parent": "c-hd-two-objects-between", "order": 1,
                                   "summary": "Split the known total distance into two parts so that both objects give the same height — one linear equation in the split point.", "links": []},
    "q-hd-midpoint-ratio": {"short": "Midpoint, height ratio", "label": "Unequal posts, complementary angles from the midpoint", "kind": "qtype", "parent": "c-hd-two-objects-between", "order": 2,
                            "summary": "One post is a stated multiple of the other's height; from the midpoint their elevations are complementary — multiply the two tangent expressions as usual.", "links": []},

    "c-hd-angle-doubling": {"short": "Angle doubles", "label": "Moving closer doubles the subtended angle", "kind": "concept", "parent": TOPIC, "order": 8,
                            "summary": "An exterior-angle argument (exterior angle = sum of the two remote interior angles) makes the triangle between the top and the two ground points isosceles, handing you a known side for free.", "links": []},
    "q-hd-angle-doubling": {"short": "Isosceles from doubling", "label": "Height when a nearer point sees exactly double the angle", "kind": "qtype", "parent": "c-hd-angle-doubling", "order": 1,
                            "summary": "Spot that the near point's angle is exactly twice the far point's — the segment from the top to the near point then equals the gap between the two points.", "links": []},

    "c-hd-combo-structures": {"short": "Two-stage structures", "label": "A building with something on top, seen from one point", "kind": "concept", "parent": TOPIC, "order": 9,
                              "summary": "A tree-and-building, chimney-and-roof, or building-and-flagstaff pair, with two different elevation angles taken from the same ground point to the two different heights.", "links": []},
    "q-hd-combo-algebraic": {"short": "Symbolic formula", "label": "Height of the upper structure, as a formula in the two angles", "kind": "qtype", "parent": "c-hd-combo-structures", "order": 1,
                            "summary": "Write the shared horizontal distance two different ways (one from each angle) and equate — the options are themselves cot/tan formulas, not numbers.", "links": []},
    "q-hd-combo-numeric": {"short": "Numeric two-stage", "label": "Length of the add-on structure, with real numbers", "kind": "qtype", "parent": "c-hd-combo-structures", "order": 2,
                          "summary": "Same shared-distance idea as the symbolic version, but every angle and length is a number — find the extra piece's own length, not the total.", "links": []},

    "c-hd-tower-sees-tower": {"short": "Viewer atop a structure", "label": "Viewer at the top of one structure, looking at another", "kind": "concept", "parent": TOPIC, "order": 10,
                              "summary": "From the known structure's top, the depression to the other structure's foot gives the shared horizontal gap; the depression to its top then gives the height difference.", "links": []},
    "q-hd-tower-sees-tower": {"short": "Depression to top & foot", "label": "Height of the unknown structure from two depression angles", "kind": "qtype", "parent": "c-hd-tower-sees-tower", "order": 1,
                             "summary": "The steeper depression angle always points at the object's foot (the nearer-in-height target) — use it first to pin down the shared horizontal distance.", "links": []},

    "c-hd-wire": {"short": "Connecting wire", "label": "A wire or rope strung between two different heights", "kind": "concept", "parent": TOPIC, "order": 11,
                 "summary": "Only the height DIFFERENCE between the two ends matters — that gap is the side opposite the wire's angle with the horizontal.", "links": []},
    "q-hd-connecting-wire": {"short": "Wire length", "label": "Length of a wire joining two unequal poles", "kind": "qtype", "parent": "c-hd-wire", "order": 1,
                            "summary": "wire = (height difference) / sin(angle with horizontal) — neither pole's own height is needed separately.", "links": []},

    "c-hd-broken-pole": {"short": "Broken pole", "label": "A pole snaps and its top touches the ground", "kind": "concept", "parent": TOPIC, "order": 12,
                        "summary": "The broken part keeps its own length but tilts; its vertical rise back up to the break point equals the break height itself.", "links": []},
    "q-hd-broken-pole": {"short": "Break height", "label": "Height at which a pole breaks, given the ground angle", "kind": "qtype", "parent": "c-hd-broken-pole", "order": 1,
                        "summary": "sin(angle) = (break height)/(remaining rigid length) — one linear equation in the break height.", "links": []},

    "c-hd-hill-two-objects": {"short": "Hill or cliff, two objects", "label": "Depression from a height to two ground objects", "kind": "concept", "parent": TOPIC, "order": 13,
                              "summary": "Two objects seen from the same high point: ADD their two cot-distances if they're on either side of the foot, SUBTRACT if they're on the same side.", "links": []},
    "q-hd-hill-two-objects": {"short": "Either-side / same-side", "label": "Distance between two objects seen from a cliff-top", "kind": "qtype", "parent": "c-hd-hill-two-objects", "order": 1,
                             "summary": "Read the wording carefully: 'either side' sums the two cot-distances, 'same side' (both ends of one bridge, say) subtracts them.", "links": []},

    "c-hd-hill-pillar": {"short": "Hill and a nearby pillar", "label": "A hill (or building) and a separate shorter pillar", "kind": "concept", "parent": TOPIC, "order": 14,
                         "summary": "The same depression-to-top-and-bottom method as a viewer atop a tower, just with a hill standing in for the known structure.", "links": []},
    "q-hd-hill-pillar-pair": {"short": "Hill-pillar pair", "label": "Height of a pillar (or hill) from a depression/elevation pair", "kind": "qtype", "parent": "c-hd-hill-pillar", "order": 1,
                             "summary": "One of the two heights is given directly; the steeper angle gives the shared horizontal distance, the shallower one gives the height difference.", "links": []},

    "c-hd-parallel-poles": {"short": "Known separation", "label": "Two poles with the horizontal distance already given", "kind": "concept", "parent": TOPIC, "order": 15,
                            "summary": "Unlike most pair-of-structures problems, the horizontal gap is handed to you directly — no need to derive it from an angle first.", "links": []},
    "q-hd-parallel-poles": {"short": "Depression between tops", "label": "Height of the second pole from the depression to its top", "kind": "qtype", "parent": "c-hd-parallel-poles", "order": 1,
                           "summary": "height₂ = height₁ − (given distance)×tan(depression angle) — one step once the distance is already known.", "links": []},

    "c-hd-circumcentre": {"short": "Equal angle, every corner", "label": "A fact about equal elevation from every vertex", "kind": "concept", "parent": TOPIC, "order": 16,
                         "summary": "Equal elevation angle from every corner of a triangle, to a single point above it, forces equal horizontal distance to every corner too.", "links": []},
    "q-hd-circumcentre-fact": {"short": "Circumcentre", "label": "Where the foot of the pole must stand", "kind": "qtype", "parent": "c-hd-circumcentre", "order": 1,
                              "summary": "Equal distance from all three vertices is exactly the definition of the circumcentre — a conceptual question, no computation.", "links": []},
}

FORMULAS = [
    {"id": "hd-f1", "node": "c-hd-basics", "text": "opposite = adjacent × tanθ; opposite = hypotenuse × sinθ; adjacent = hypotenuse × cosθ", "note": "Pick whichever one connects the given side to the wanted side."},
    {"id": "hd-f2", "node": "c-hd-shadow-ratio", "text": "height / shadow = tan(elevation), the same ratio for every object at one instant", "note": "Scale one object's ratio up or down to another's shadow length, or read the angle straight off the ratio."},
    {"id": "hd-f3", "node": "c-hd-two-angle-walk", "text": "distance moved = h(cotθ₁ − cotθ₂), for θ₂ > θ₁ seen after moving closer", "note": "Solve for h if the distance is given, or for the distance if h is given — same one equation either way."},
    {"id": "hd-f4", "node": "c-hd-fixed-height-shift", "text": "shift in the ground point = h(cotθ₁ − cotθ₂), height h unchanged between the two angles", "note": "Identical algebra to hd-f3; only the physical story (shadow, ladder) differs."},
    {"id": "hd-f5", "node": "c-hd-complementary", "text": "If the elevations from two points at distances a and b (same line as the foot) are complementary, height = √(ab)", "note": "Comes from tanθ·tan(90°−θ) = 1 = h²/(ab)."},
    {"id": "hd-f6", "node": "c-hd-vertical-pair", "text": "Two objects sharing a horizontal distance d: height = d·tan(its own elevation angle)", "note": "Find d from whichever object's height is already known, then apply it to the other's angle."},
    {"id": "hd-f7", "node": "c-hd-two-objects-between", "text": "Equal heights, point between: x·tanθ₁ = (total−x)·tanθ₂ for the split point x", "note": "For an m:1 height ratio instead of equal heights, the same idea gives (mh)/(x) and h/(total−x) equal to the respective tangents."},
    {"id": "hd-f8", "node": "c-hd-angle-doubling", "text": "If a nearer point's subtended angle is exactly double a farther point's, the segment from the top to the near point equals the gap between the two points", "note": "Exterior-angle theorem: the doubled angle splits into two equal parts, one of which is the far point's own angle, making the triangle isosceles."},
    {"id": "hd-f9", "node": "c-hd-combo-structures", "text": "Shared horizontal distance d, written from each of the two angles on the same vertical structure, equated", "note": "d = (lower height)·cot(its angle) = (height difference)·cot(the other angle), or similar, depending on which heights are known."},
    {"id": "hd-f10", "node": "c-hd-tower-sees-tower", "text": "From a known height H: d = H·cot(depression to the far foot); unknown height = H − d·tan(depression to the far top)", "note": "The steeper angle (bigger value) always goes with the foot, since the foot is 'more below' the viewer than the top."},
    {"id": "hd-f11", "node": "c-hd-wire", "text": "wire length = (height difference) / sin(angle with horizontal)", "note": "The two poles' own heights don't matter individually, only their difference."},
    {"id": "hd-f12", "node": "c-hd-broken-pole", "text": "sin(angle with ground) = (break height) / (remaining rigid length = original − break height)", "note": "One linear equation in the break height once this is set up."},
    {"id": "hd-f13", "node": "c-hd-hill-two-objects", "text": "Either side of the foot: distance = h·cotθ₁ + h·cotθ₂. Same side: distance = h·cotθ₁ − h·cotθ₂ (farther minus nearer)", "note": "The wording 'either side' vs 'same side' is the only signal for which formula applies."},
    {"id": "hd-f14", "node": "c-hd-circumcentre", "text": "Equal elevation angle from every vertex of a triangle to one point above it ⇒ equal horizontal distance from every vertex ⇒ that foot is the circumcentre", "note": "tan(angle) = height/distance, with the same angle and the same height for all three corners, forces the same distance too."},
]

METHODS = {
    "q-hd-single-triangle": {
        "cue": "One right triangle, one angle (elevation or depression) and exactly one known side — a thread, a ladder, a line of sight, or a shadow.",
        "formulas": ["hd-f1"], "tech": ["standard-values"],
        "standard": "Identify which side is given (opposite, adjacent, or hypotenuse) and which is wanted, then apply the one matching ratio.",
        "fast": "With a 30°/45°/60° angle, use the standard 1:1:√2 or 1:√3:2 side ratios directly instead of computing sin/cos/tan from scratch.",
        "eliminate": "The hypotenuse must be the largest side of the three — an option smaller than the given leg is automatically wrong.",
        "traps": ["Using sin where cos was needed (or the reverse) by misreading which side is 'opposite' the given angle.", "Treating the hypotenuse (thread, ladder) as if it were a leg.", "Forgetting to rationalise a 1/√3-type answer, leaving it in a form that doesn't match any option."]},
    "q-hd-shadow-ratio": {
        "cue": "Two shadows (or a shadow and a height) compared 'at the same time' or 'at the same instant', or a shadow given as a multiple of the height.",
        "formulas": ["hd-f2"], "tech": ["ratio-parts", "standard-values"],
        "standard": "Write height:shadow as one ratio from the object you know fully, then scale it to the other object's shadow — or read tanθ off a given ratio directly.",
        "fast": "Shadow = height means θ=45°; shadow = √3×height means θ=30°; shadow = height/√3 means θ=60° — recognise these on sight.",
        "eliminate": "A taller shadow at the same instant must belong to a taller object — ratios must stay internally consistent.",
        "traps": ["Inverting the ratio (using shadow/height where height/shadow was needed).", "Mixing up which object's shadow is given when two are mentioned.", "Reading a 1/√3 ratio as 30° instead of 60° (or the reverse)."]},
    "q-hd-two-angle-walk": {
        "cue": "An observer 'walks', 'moves', or 'travels' a stated distance toward (or away from) the foot of a tower, and the elevation angle changes between the two points.",
        "formulas": ["hd-f3"], "tech": ["standard-values", "rationalise"],
        "standard": "Write the two ground distances as h·cotθ₁ and h·cotθ₂; their difference is the distance walked — solve for whichever of h or the distance is missing.",
        "fast": "cot30°−cot60° = 2/√3 and cot45°−cot60° = 1−1/√3 are the two combinations that come up again and again — memorise their rationalised forms.",
        "eliminate": "The height must be positive and the walked distance must be smaller than the farther of the two ground distances.",
        "traps": ["Adding the two cot-distances instead of subtracting (that's the either-side/same-point type, a different family).", "Swapping which angle belongs to the nearer point.", "Leaving a surd denominator unrationalised, so the numeric answer doesn't match any option."]},
    "q-hd-fixed-height-shift": {
        "cue": "A shadow 'increases' or 'decreases' by a stated amount as the sun's angle changes, OR a ladder/pole of fixed length slips to a shallower angle.",
        "formulas": ["hd-f4"], "tech": ["standard-values", "rationalise"],
        "standard": "Same h(cotθ₁−cotθ₂) relation as the walking type — here the SHIFT is the given or wanted quantity instead of the observer's own distance.",
        "fast": "Decreasing shadow (angle increasing) always means cot(smaller angle) − cot(larger angle), kept positive — check the sign makes physical sense before finishing.",
        "eliminate": "A 'decrease' must come out positive and smaller than the original shadow length implied by the smaller angle.",
        "traps": ["Getting the sign backwards (computing an increase where a decrease was described, or vice versa).", "Rationalising with the wrong sign, e.g. (√3−1) instead of (√3+1) in the numerator.", "Reporting the new foot-distance itself instead of how much it moved."]},
    "q-hd-complementary-geomean": {
        "cue": "The word 'complementary' applied to two elevation angles from two points on the same line as the tower's foot.",
        "formulas": ["hd-f5"], "tech": ["identity"],
        "standard": "Multiply the two tangent expressions (they're reciprocals since the angles are complementary) to get height² = (distance 1)×(distance 2), then take the square root.",
        "fast": "If the product of the two distances is a perfect square, the height is a clean integer — check that first.",
        "eliminate": "The height must lie strictly between the two given distances when they're unequal (it's their geometric mean, always between the min and max).",
        "traps": ["Reporting the plain product ab instead of its square root.", "Reporting a ratio (a/b) instead of a product.", "Squaring instead of square-rooting (or the reverse)."]},
    "q-hd-vertical-pair": {
        "cue": "Two aeroplanes (or similar) are 'vertically above/below' each other, observed from the SAME ground point, with two different elevation angles.",
        "formulas": ["hd-f6"], "tech": ["standard-values"],
        "standard": "Use the object whose height is given, together with its own angle, to find the shared horizontal distance; then apply that distance to the other object's angle.",
        "fast": "Work out which angle belongs to which object by height first: the higher object always has the larger elevation angle (same shared distance).",
        "eliminate": "The gap must be smaller than the larger of the two heights and the two separately-computed heights must be consistent with 'one above the other'.",
        "traps": ["Assigning the larger angle to the lower object (angles and heights must rank the same way).", "Treating the given height as the shared horizontal distance instead of a vertical height.", "Reporting one plane's height instead of the gap between the two."]},
    "q-hd-equal-objects-between": {
        "cue": "Two equal-height poles/towers stand opposite each other across a road or gap of known total width, and a point BETWEEN them sees the two tops at different angles.",
        "formulas": ["hd-f7"], "tech": ["standard-values"],
        "standard": "Let the point be x from one foot and (total−x) from the other; set the two tan-expressions for the (equal) height equal and solve the resulting linear equation for x.",
        "fast": "A 30°/60° pair always splits the total distance in a 1:3 ratio (the tan60° side gets the smaller share) — a shortcut once you've derived it once.",
        "eliminate": "The computed height must be smaller than the total road width (a much larger number signals a setup error).",
        "traps": ["Assuming an even 50:50 split regardless of the two angles.", "Mixing up which share (x or total−x) goes with which angle.", "Finding x but forgetting to then compute the height itself."]},
    "q-hd-midpoint-ratio": {
        "cue": "Two posts of UNEQUAL, stated-ratio height (often 'one is double the other'), with the elevations from the MIDPOINT between their feet complementary.",
        "formulas": ["hd-f7"], "tech": ["identity"],
        "standard": "Write both tangent expressions using the ratio (h and mh) over the same half-distance, multiply them (complementary ⇒ product is 1), and solve for h.",
        "fast": "The algebra always reduces to h² = (half-distance)²/m — just substitute the stated ratio m and take the square root.",
        "eliminate": "The answer must be expressed as a fraction or surd multiple of the total distance x, matching the ratio given — a bare number without x is automatically wrong here.",
        "traps": ["Using the full distance x instead of the half-distance x/2 in the tangent expressions.", "Forgetting the height ratio (treating both posts as equal height).", "Reporting the taller post's height instead of the shorter one asked for."]},
    "q-hd-angle-doubling": {
        "cue": "A tower 'subtends an angle' at a far point, and at a nearer point (a stated distance closer) the angle is 'twice as before' or given as an exact double (e.g. 15° and 30°).",
        "formulas": ["hd-f8"], "tech": ["identity", "standard-values"],
        "standard": "Use the exterior-angle theorem to show the triangle between the top and the two ground points is isosceles, with the top-to-near-point segment equal to the gap between the two points; finish with that segment as a hypotenuse (standard ratio) or via Pythagoras with the near-point's own ground distance.",
        "fast": "Once the isosceles side is known, check whether the near-point's angle is a standard one (30°, 45°, 60°) for a direct ratio, or use Pythagoras when it isn't.",
        "eliminate": "The height must be smaller than the isosceles side (which is itself a hypotenuse or a side of the bigger triangle).",
        "traps": ["Reporting the isosceles side itself instead of continuing to the actual height.", "Using the original far distance instead of the near-point distance in the final right triangle.", "Misapplying the exterior-angle split when the angles given aren't exactly double."]},
    "q-hd-combo-algebraic": {
        "cue": "The answer options are themselves formulas in cot/tan of two named angles (not plain numbers) — a tree-and-building or similar two-height setup.",
        "formulas": ["hd-f9"], "tech": ["identity"],
        "standard": "Write the shared horizontal distance two different ways, one from each of the two given angles, and equate them to isolate the unknown height symbolically.",
        "fast": "Substitute convenient concrete numbers for the angles and the known height to check which option matches numerically — faster than re-deriving under exam pressure.",
        "eliminate": "The denominator must be a DIFFERENCE of cotangents (cot x − cot y), not a sum, whenever the two angles come from the SAME vertical structure at different heights.",
        "traps": ["Writing cot x + cot y in the denominator where a difference was needed (that pattern belongs to the either-side/same-point family instead).", "Swapping which angle's cotangent sits in the numerator.", "Forgetting that the known height h multiplies only one of the two cotangents, not the whole expression."]},
    "q-hd-combo-numeric": {
        "cue": "A building (or similar) of known height has something extra on top (a flagstaff, a chimney) and two different elevation angles are given from one ground point, with specific numbers throughout.",
        "formulas": ["hd-f9"], "tech": ["standard-values"],
        "standard": "Find the shared horizontal distance from the lower (known) structure's own angle, then use it with the upper angle to get the TOTAL height, and subtract the known part to get just the add-on's length.",
        "fast": "If the upper angle is 45°, the total height equals the shared horizontal distance exactly — one less computation.",
        "eliminate": "The add-on's length must be smaller than the total height and (usually) smaller than the known building height too, for a realistic flagstaff or chimney.",
        "traps": ["Reporting the TOTAL height (building + add-on) instead of just the add-on's own length.", "Using the add-on's angle with the building's own height instead of the shared horizontal distance.", "Forgetting the question's rounding instruction (e.g. 'take √3=1.732') and leaving a surd that doesn't match any option."]},
    "q-hd-tower-sees-tower": {
        "cue": "The observer stands at the TOP of one known-height structure (post, temple, a point above another observer) and reports the angle of depression to both the top and the foot of a second, unknown structure.",
        "formulas": ["hd-f10"], "tech": ["standard-values"],
        "standard": "Use the depression to the FOOT (always the steeper, larger angle) to find the shared horizontal distance; then the depression to the TOP (shallower) gives the height difference, which you subtract from the known height.",
        "fast": "Depression angles of 30° and 60° together usually mean the horizontal distance is a clean multiple of √3 — simplify that first before finishing.",
        "eliminate": "The unknown structure's height must be smaller than the known one whenever its depression-to-top angle is the shallower of the two (a bigger result signals a swapped-angle error).",
        "traps": ["Using the shallower angle to find the shared distance instead of the steeper one.", "Reporting the height DIFFERENCE as the final answer instead of subtracting it from the known height.", "Mixing up which depression angle (to the top or to the foot) is the steeper one."]},
    "q-hd-connecting-wire": {
        "cue": "A wire, rope, or ladder joins the TOPS of two poles or walls of different, stated heights, making a given angle with the horizontal.",
        "formulas": ["hd-f11"], "tech": ["standard-values"],
        "standard": "Subtract the two heights to get the wire's vertical rise, then divide by sin(the wire's angle with the horizontal) to get the wire's own length.",
        "fast": "Recognise a standard triple scaled by the height gap (e.g. a 12 m gap at 60° is a scaled 30-60-90 triangle) to skip the division.",
        "eliminate": "The wire must be longer than the plain height difference (it's a hypotenuse, the difference is only one leg).",
        "traps": ["Using sin where cos was needed (the wire's angle is with the HORIZONTAL, so the height gap is the opposite side).", "Using either pole's full height instead of just the difference.", "Reporting the horizontal projection of the wire instead of the wire's own length."]},
    "q-hd-broken-pole": {
        "cue": "A pole or post 'breaks' or 'snaps' at some height, and its top part — still attached, not fully separated — now touches the ground at a stated angle.",
        "formulas": ["hd-f12"], "tech": ["standard-values"],
        "standard": "Let the break height be h; the remaining original length minus h is the broken part's own (unchanged) length, which is the hypotenuse of the triangle it now forms with the ground.",
        "fast": "sin(angle) = h/(L−h) rearranges to h = L·sinθ/(1+sinθ) in one line — plug in directly rather than re-deriving each time.",
        "eliminate": "The break height must be less than half the original pole whenever the ground angle is under 30° (sinθ < 1/2 forces h < L−h).",
        "traps": ["Treating the FULL original length as the hypotenuse instead of just the broken (upper) part's length.", "Writing the equation with h and (L−h) swapped.", "Using cos instead of sin (the angle is with the ground, so the break height is the opposite, vertical side)."]},
    "q-hd-hill-two-objects": {
        "cue": "Depression angles from one high point to TWO separate ground objects (two ships, two ends of a bridge, two sides of something) — watch for 'either side' versus 'same side' in the wording.",
        "formulas": ["hd-f13"], "tech": ["standard-values"],
        "standard": "Compute each object's own distance from the foot as height×cot(its depression angle); ADD the two if the objects are on either side of the foot, SUBTRACT (farther minus nearer) if they're on the same side.",
        "fast": "cot30°+cot60° = 4/√3 and cot30°−cot45° = √3−1 are the two combinations that recur — recognise them on sight.",
        "eliminate": "An 'either side' distance must be bigger than either single cot-distance alone; a 'same side' distance must be smaller than the larger cot-distance alone.",
        "traps": ["Subtracting when the objects are on either side (should add) or adding when they're on the same side (should subtract) — the single most common slip in this type.", "Mixing up which angle's cot-distance is the larger one before subtracting.", "Forgetting to multiply by the given height before combining the two cot values."]},
    "q-hd-hill-pillar-pair": {
        "cue": "A hill or building of KNOWN height, with the depression (to the top) and a further depression or elevation (to the bottom) of a SEPARATE, unknown-height object given from the same viewpoint.",
        "formulas": ["hd-f10"], "tech": ["standard-values"],
        "standard": "Exactly the tower-sees-tower method: the steeper angle (to the object's bottom) gives the shared horizontal distance, the shallower one (to its top) gives the height difference.",
        "fast": "If both angles are standard (30°/60°), the horizontal distance and the height difference both come out as clean multiples of the known height — no decimal arithmetic needed.",
        "eliminate": "The unknown object's height is always smaller than the known hill's height in this family — an answer bigger than the given height is wrong.",
        "traps": ["Swapping which angle (depression-to-top vs depression-to-bottom) is the steeper one.", "Reporting the shared horizontal distance instead of the object's actual height.", "Forgetting to subtract the height difference from the known height at the final step."]},
    "q-hd-parallel-poles": {
        "cue": "The horizontal distance between the two poles is stated directly in the question (not something you must derive from an angle).",
        "formulas": ["hd-f10"], "tech": ["standard-values"],
        "standard": "Apply tan(depression angle) to the GIVEN distance directly to get the height drop, then subtract it from the known pole's height.",
        "fast": "No distance-finding step here — go straight to drop = distance × tan(angle); this type is one step shorter than the tower-sees-tower family.",
        "eliminate": "The second pole's height must be smaller than the first whenever the depression is downward, from the taller pole to the shorter one.",
        "traps": ["Re-deriving the horizontal distance from an angle when it was already given directly (wasted work, and an easy place to introduce an error).", "Adding the drop instead of subtracting it.", "Reporting the drop itself instead of the second pole's actual height."]},
    "q-hd-circumcentre-fact": {
        "cue": "A pole stands inside a triangle, and the elevation angle to its top is stated to be the SAME from every corner of the triangle.",
        "formulas": ["hd-f14"], "tech": ["identity"],
        "standard": "Factor the shared pole height out of 'same angle from every corner': tan(angle) = height/distance being equal for all three corners forces equal distance too — the circumcentre's definition.",
        "fast": "No computation at all — just recognise 'equal angle from every vertex' as the circumcentre's signature and pick it directly.",
        "eliminate": "Centroid, incentre and orthocentre are each equidistant from something else (medians' balance point, the sides, the altitudes' intersection) — none of them guarantees equal distance from the three VERTICES.",
        "traps": ["Confusing circumcentre (equidistant from vertices) with incentre (equidistant from sides).", "Picking centroid out of habit, since it's the most commonly cited triangle centre.", "Picking orthocentre, which has no general equidistance property at all."]},
}
REFS = [
    {"title": "NCERT Class 10 Maths, Chapter 9 — Some Applications of Trigonometry", "url": "https://ncert.nic.in/textbook.php", "note": "The standard elevation/depression setup (angle of elevation = angle of depression from the other end, by alternate angles) that every question in this topic builds on."},
]

PYQS = PYQS_C22HD


def practice_items():
    return []
