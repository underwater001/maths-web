"""Trigonometric ratios: quiz tier."""
import math
from bank import bound, mistake, pyq
from topics._ch21tr_ry import PYQS_RY as PYQS_C21TR

TOPIC = "trig-ratios"
PREFIX = "tr"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
r5, r3 = math.sqrt(5), math.sqrt(3)

NODES = {
    "c-tr-angles": {"short": "Radians", "label": "Radians and degrees", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "π radians = 180°. Convert by replacing π with 180.", "links": ["mensuration-2d"]},
    "c-tr-ratios": {"short": "Ratios", "label": "Ratios of an acute angle", "kind": "concept", "parent": TOPIC, "order": 2,
                    "summary": "From one ratio get the other five with a right triangle; complementary angles swap sin and cos.", "links": []},
    "q-tr-convert": {"short": "Radians → degrees", "label": "Convert radians to degrees", "kind": "qtype", "parent": "c-tr-angles", "order": 1,
                     "summary": "An angle like 3π/2 radians in degrees.", "links": []},
    "q-tr-complement": {"short": "Complementary angles", "label": "sin(90° − B) = cos B", "kind": "qtype", "parent": "c-tr-ratios", "order": 1,
                        "summary": "A ratio of (90° − B) is given; find the cofunction of B.", "links": []},
    "q-tr-triangle": {"short": "Find another ratio", "label": "Another ratio from one ratio", "kind": "qtype", "parent": "c-tr-ratios", "order": 2,
                      "summary": "cos A = 5/13 (A acute); find tan A.", "links": []},

    "c-tr-maxmin": {"short": "Max/min and bounds", "label": "Maximum, minimum, and bound tricks", "kind": "concept", "parent": TOPIC, "order": 3,
                    "summary": "sin, cos and their squares are trapped in [-1, 1] / [0, 1]; a·sinθ+b·cosθ is trapped in [-√(a²+b²), √(a²+b²)]; and a positive term plus its own reciprocal is at least 2 (AM-GM). Many 'find the value' questions are really asking you to spot one of these bounds.", "links": []},
    "q-tr-max-linear": {"short": "Max/min of a·sinθ+b·cosθ", "label": "Maximum or minimum of a linear or squared trig expression", "kind": "qtype", "parent": "c-tr-maxmin", "order": 1,
                        "summary": "Max of a·sinθ+b·cosθ is √(a²+b²) (min is its negative); a·sin²θ+b·cos²θ ranges between a and b.", "links": []},
    "q-tr-max-amgm": {"short": "AM-GM on a reciprocal pair", "label": "Minimum of a·x² + b/x² by AM-GM", "kind": "qtype", "parent": "c-tr-maxmin", "order": 2,
                      "summary": "a·tan²θ + b·cot²θ (or similar reciprocal pairs) has minimum 2√(ab), by AM-GM.", "links": []},
    "q-tr-bound-trick": {"short": "Equality forced by a bound", "label": "An equation only works because of a sin/cos bound", "kind": "qtype", "parent": "c-tr-maxmin", "order": 3,
                         "summary": "If the equation forces one side to be ≥ some value while sin or cos caps the other side at that same value, the only way out is exact equality (or, if the cap is never reached, no solution at all).", "links": []},

    "c-tr-chains": {"short": "Complementary chains", "label": "Products and sums over a run of complementary angles", "kind": "concept", "parent": TOPIC, "order": 4,
                    "summary": "tanθ·tan(90°−θ) = 1 and sin²θ+sin²(90°−θ) = 1; a long product or sum built from angles that pair up to 90° collapses almost entirely.", "links": []},
    "q-tr-complement-telescope": {"short": "Product collapses to 1", "label": "A product of several complementary-angle tangents/cotangents", "kind": "qtype", "parent": "c-tr-chains", "order": 1,
                                  "summary": "Pair every tan k° with tan(90°−k)°: each pair is 1, so the whole product is 1 (tan45°, if present, is already 1 on its own).", "links": []},
    "q-tr-complement-sumsq": {"short": "Sum of sin² collapses", "label": "A sum of sin² (or cos²) over a run of angles", "kind": "qtype", "parent": "c-tr-chains", "order": 2,
                              "summary": "Pair sin²k° with sin²(90°−k)°: each pair sums to 1; count the pairs, and watch for a lone 45° term (= 1/2) or an extra term stuck on the end.", "links": []},

    "c-tr-identities": {"short": "Identity simplification", "label": "Collapsing a big expression with sin²+cos²=1 and friends", "kind": "concept", "parent": TOPIC, "order": 5,
                        "summary": "Swap 1+cot²θ for cosec²θ, 1+tan²θ for sec²θ, and sin²θ+cos²θ for 1 as early as possible, before any other algebra.", "links": []},
    "q-tr-identity-simplify": {"short": "Numeric value of a big expression", "label": "A tangled expression that collapses to a plain number", "kind": "qtype", "parent": "c-tr-identities", "order": 1,
                               "summary": "Rewrite every 1+tan²θ / 1+cot²θ term as sec²θ / cosec²θ (or their reciprocals) immediately, then the sin²θ+cos²θ=1 terms cancel out cleanly.", "links": []},

    "c-tr-componendo": {"short": "secθ±tanθ are reciprocals", "label": "secθ+tanθ and secθ-tanθ multiply to 1", "kind": "concept", "parent": TOPIC, "order": 6,
                        "summary": "(secθ+tanθ)(secθ−tanθ) = sec²θ−tan²θ = 1 always, so knowing one of the pair (or their ratio) hands you the other directly, no angle-finding needed.", "links": []},
    "q-tr-componendo": {"short": "Given the ratio, find a ratio", "label": "Given (secθ+tanθ)/(secθ−tanθ), find sinθ or cosθ", "kind": "qtype", "parent": "c-tr-componendo", "order": 1,
                        "summary": "Cross-multiply the given ratio into a secθ = (number)·tanθ relation, then convert to sinθ/cosθ.", "links": []},
    "q-tr-power-sum-trap": {"short": "sinθ+cosecθ=2 forces sinθ=1", "label": "A sum like sinθ+cosecθ=2 fixes the angle entirely", "kind": "qtype", "parent": "c-tr-componendo", "order": 2,
                            "summary": "By AM-GM, sinθ+cosecθ ≥ 2 always, with equality only at sinθ=1 — so if the sum IS 2, any power sum sinⁿθ+cosecⁿθ is just 2, whatever n is.", "links": []},

    "c-tr-equations": {"short": "Solving for θ", "label": "Solving a trig equation for the angle", "kind": "concept", "parent": TOPIC, "order": 7,
                       "summary": "Rewrite everything in terms of one ratio (often via an identity like tan²θ=sec²θ−1), turn it into a standard equation, and solve for the acute angle(s).", "links": []},
    "q-tr-equation-solve": {"short": "Solve the equation for θ", "label": "Find the acute angle(s) satisfying a trig equation", "kind": "qtype", "parent": "c-tr-equations", "order": 1,
                            "summary": "Convert to a single ratio using an identity, solve the resulting equation (often a quadratic), and match standard angles to the resulting ratio value(s).", "links": []},
}
FORMULAS = [
    {"id": "tr-f1", "node": "c-tr-angles", "text": "π radians = 180°     1 radian ≈ 57.3°", "note": "3π/2 rad = 3 × 180° ÷ 2 = 270°."},
    {"id": "tr-f2", "node": "c-tr-ratios", "text": "sin(90° − θ) = cos θ     cos(90° − θ) = sin θ     tan(90° − θ) = cot θ", "note": "Complementary angles swap the pair."},
    {"id": "tr-f3", "node": "c-tr-ratios", "text": "sin²θ + cos²θ = 1;  with cos A = b/h, sin A = p/h and tan A = p/b where p² + b² = h²", "note": "5–12–13 and 3–4–5 triangles come up all the time."},
    {"id": "tr-f4", "node": "c-tr-maxmin", "text": "Max of a·sinθ+b·cosθ is √(a²+b²); min is −√(a²+b²). a·sin²θ+b·cos²θ ranges over [min(a,b), max(a,b)].", "note": "Both facts come from sin²θ+cos²θ=1 trapping sin, cos in [-1,1]."},
    {"id": "tr-f5", "node": "c-tr-maxmin", "text": "a·x² + b/x² ≥ 2√(ab) by AM-GM, for positive a, b and real x ≠ 0.", "note": "Equality holds when a·x² = b/x², which for trig x = tanθ always has a real solution."},
    {"id": "tr-f6", "node": "c-tr-chains", "text": "tan k°·tan(90°−k)° = 1; sin²k° + sin²(90°−k)° = 1.", "note": "Pair the angles from the ends inward; a leftover 45° term contributes 1 (product) or 1/2 (sum of squares)."},
    {"id": "tr-f7", "node": "c-tr-identities", "text": "1 + tan²θ = sec²θ; 1 + cot²θ = cosec²θ; sin²θ + cos²θ = 1.", "note": "Swap these in immediately, before trying any other algebra on a tangled expression."},
    {"id": "tr-f8", "node": "c-tr-componendo", "text": "(secθ+tanθ)(secθ−tanθ) = sec²θ−tan²θ = 1, so secθ−tanθ = 1/(secθ+tanθ).", "note": "Knowing secθ+tanθ (or its ratio to secθ−tanθ) hands you the other factor for free."},
    {"id": "tr-f9", "node": "c-tr-equations", "text": "tan²θ = sec²θ − 1 and cot²θ = cosec²θ − 1 turn a tan/cot equation into a sec/cosec one (often a quadratic).", "note": "Factor the quadratic in secθ (or cosecθ) and match each root to a standard angle."},
]
METHODS = {
    "q-tr-convert": {
        "cue": "'… radians in degrees' with a multiple of π.",
        "formulas": ["tr-f1"], "tech": ["standard-values", "cancel-first"],
        "standard": "Replace π by 180°: 3π/2 → 3 × 180° ÷ 2 = 270°.",
        "fast": "π/2 = 90°, so 3π/2 is three of those: 270°.",
        "eliminate": "The answer is a multiple of 90° for π/2 steps. 210° and 300° are not.",
        "traps": ["Using 360° for π.", "Reading 3π/2 as 3π ÷ 2 with the wrong π (π = 3.14 → 4.71°)."]},
    "q-tr-complement": {
        "cue": "sin(90° − B) = value; find cos B (or the reverse).",
        "formulas": ["tr-f2"], "tech": ["identity"],
        "standard": "sin(90° − B) = cos B, so cos B = 2/3.",
        "fast": "The answer is the same number: complementary angles swap sin and cos but keep the value.",
        "eliminate": "No calculation is needed; the option equal to the given value is the answer. The other options are different values.",
        "traps": ["Computing sin B (which is √5/3) instead of cos B.", "Taking 1 − 2/3 = 1/3."]},
    "q-tr-triangle": {
        "cue": "One ratio of an acute angle is a simple fraction; another ratio is asked.",
        "formulas": ["tr-f3"], "tech": ["standard-values", "plug-numbers"],
        "standard": "cos A = 5/13: base 5, hypotenuse 13, so the height is √(169 − 25) = 12. tan A = height ÷ base = 12/5.",
        "fast": "Recognise the 5–12–13 triangle. tan = opposite ÷ adjacent = 12/5.",
        "eliminate": "A is acute and cos A is smaller than sin A here (5/13 < 12/13), so A > 45° and tan A > 1. Options below 1 are out.",
        "traps": ["Giving cot A = 5/12 (adjacent ÷ opposite).", "Giving sec or cosec (13/12 is cosec A).", "Giving sin A = 12/13."]},
    "q-tr-max-linear": {
        "cue": "'Maximum/minimum value of a sinθ + b cosθ' or of 'a sin²θ + b cos²θ'.",
        "formulas": ["tr-f4"], "tech": ["standard-values", "bounds"],
        "standard": "For a·sinθ+b·cosθ: the max is √(a²+b²), the min is −√(a²+b²). For a·sin²θ+b·cos²θ: rewrite as the smaller coefficient plus (gap)×sin²θ or cos²θ, then use that the squared term ranges over [0,1].",
        "fast": "Spot which form it is and apply the matching formula directly — no calculus, no trial angles.",
        "eliminate": "For the squared form, the answer must lie between the two coefficients themselves; for the linear form, it must not exceed √(a²+b²).",
        "traps": ["Using a+b instead of √(a²+b²) for the linear form.", "Forgetting the squared form's range is bounded by the coefficients themselves, not by √(a²+b²)."]},
    "q-tr-max-amgm": {
        "cue": "'Minimum value of a·tan²θ + b·cot²θ' (or any positive term plus its own reciprocal-shaped partner).",
        "formulas": ["tr-f5"], "tech": ["bounds"],
        "standard": "Apply AM-GM: a·x² + b/x² ≥ 2√(ab), with equality when a·x² = b/x².",
        "fast": "Just multiply the two coefficients, take the square root, and double it — 2√(ab).",
        "eliminate": "The answer must be achievable, i.e. 2√(ab) exactly; a value below that is impossible, and one above it isn't the minimum.",
        "traps": ["Adding the coefficients instead of taking 2√(ab).", "Forgetting the 2 in front of the square root."]},
    "q-tr-bound-trick": {
        "cue": "An equation where one side is manifestly ≥ some number (often after completing the square) and the other side is a sin or cos (capped at 1).",
        "formulas": ["tr-f4"], "tech": ["bounds"],
        "standard": "Find the minimum of the 'always ≥' side (often by completing the square). If sin/cos can actually reach that minimum, that pins down the unknown exactly; if it can't, there's no solution at all.",
        "fast": "Complete the square first — the minimum and the value of the unknown that achieves it both fall out together.",
        "eliminate": "Test whether the proposed equality point actually makes the trig side equal 1 (or whatever the bound requires); if it doesn't, that option is impossible.",
        "traps": ["Assuming a solution must exist just because the algebra looks solvable.", "Finding the minimum of one side but forgetting to check whether the trig side can actually reach it."]},
    "q-tr-complement-telescope": {
        "cue": "A product of several tan/cot terms at angles that look like they pair up to 90° (e.g. tan1°·tan2°·…·tan89°).",
        "formulas": ["tr-f6"], "tech": ["identity"],
        "standard": "Pair tan k° with tan(90°−k)°: each such pair multiplies to 1. If tan45° appears alone, it's already 1.",
        "fast": "Count the pairs; if everything pairs up (or the leftover is exactly 45°), the whole product is 1 without computing a single tangent.",
        "eliminate": "An answer other than a clean power of a standard value (often just 1) is suspicious the moment every angle pairs to 90°.",
        "traps": ["Trying to compute individual tangent values instead of spotting the complementary pairing.", "Missing that one leftover angle doesn't pair (check it's exactly 45°, which is self-paired)."]},
    "q-tr-complement-sumsq": {
        "cue": "A sum of sin² (or cos²) across a run of angles that are symmetric around 45° (e.g. sin²5°+sin²6°+…+sin²85°).",
        "formulas": ["tr-f6"], "tech": ["identity"],
        "standard": "Pair sin²k° with sin²(90°−k)°: each pair sums to 1. Count the pairs; a lone middle term at 45° contributes 1/2, and watch for any extra term (like sin²90°=1) tacked on outside the run.",
        "fast": "Half the number of terms (rounding for an odd count) gives the pair total directly; just add any leftover terms.",
        "eliminate": "The answer must be close to half the term count — anything far from that is a sign the pairing was miscounted.",
        "traps": ["Forgetting the half-unit contribution from a lone 45° term.", "Missing an extra term stuck on the end of the range that isn't part of the complementary pairing."]},
    "q-tr-identity-simplify": {
        "cue": "A tangled expression mixing 1+tan²θ, 1+cot²θ, sin²θ, cos²θ that's asked to reduce to a plain number.",
        "formulas": ["tr-f7"], "tech": ["identity"],
        "standard": "Replace 1+tan²θ with sec²θ (so 1/(1+tan²θ) = cos²θ) and 1+cot²θ with cosec²θ (so 1/(1+cot²θ) = sin²θ) immediately, then combine the remaining sin²θ/cos²θ terms.",
        "fast": "Do the identity swap before any other simplification — the expression usually collapses to a small integer in one more line.",
        "eliminate": "Plug in a convenient angle (like 45°) and check which option matches — the expression is usually angle-independent.",
        "traps": ["Swapping 1/(1+tan²θ) for sin²θ instead of cos²θ (the pairing is crosswise).", "Leaving the expression partly in tan/cot instead of finishing the conversion to sin/cos."]},
    "q-tr-componendo": {
        "cue": "'(secθ+tanθ)/(secθ−tanθ) = …' or 'secθ+tanθ = …', asking for sinθ, cosθ, or another combination of tanθ.",
        "formulas": ["tr-f8"], "tech": ["identity"],
        "standard": "Use secθ−tanθ = 1/(secθ+tanθ) (from their product being 1) to get both quantities, or cross-multiply a given ratio directly into a secθ = (number)·tanθ relation.",
        "fast": "Never solve for θ itself — work entirely with secθ+tanθ and its reciprocal.",
        "eliminate": "Check that the recovered sinθ or cosθ is between 0 and 1 (θ is acute) — an option outside that range can't be right.",
        "traps": ["Trying to find θ numerically instead of using the reciprocal relationship directly.", "Mixing up which of secθ+tanθ, secθ−tanθ is the larger one."]},
    "q-tr-power-sum-trap": {
        "cue": "'sinθ + cosecθ = 2' (or a similar sum with another reciprocal pair) with a high power asked for, like sin¹⁰⁰θ + cosec¹⁰⁰θ.",
        "formulas": ["tr-f5"], "tech": ["bounds"],
        "standard": "By AM-GM, sinθ+cosecθ ≥ 2 always, with equality only at sinθ=1. So the given sum being exactly 2 forces sinθ=1 (and cosecθ=1), making any power sum equal to 2.",
        "fast": "Recognise the trap immediately: the huge exponent is irrelevant once sinθ is pinned to exactly 1.",
        "eliminate": "Any answer except 2 ignores that sinθ is forced to exactly 1 — there's no other value the equation can take.",
        "traps": ["Trying to actually compute a high power instead of spotting that sinθ is forced to be exactly 1.", "Assuming the exponent changes the answer when it never does for this setup."]},
    "q-tr-equation-solve": {
        "cue": "An equation in one trig ratio (plus a constant) that's asked to be solved for the acute angle θ, often over a stated range.",
        "formulas": ["tr-f9"], "tech": ["identity", "back-substitute"],
        "standard": "Convert every term to one ratio using an identity (e.g. tan²θ = sec²θ−1), turn it into a standard (often quadratic) equation, solve, then match each root to its standard angle.",
        "fast": "Factor the resulting quadratic rather than using the general formula — the roots are almost always 1 and a small integer.",
        "eliminate": "Plug each candidate angle back into the ORIGINAL equation (not the converted one) to confirm it actually satisfies it.",
        "traps": ["Converting to the wrong identity (e.g. using cosec²θ−1 where cot²θ was needed).", "Reporting only one root of the quadratic when the question allows two valid angles."]},
}


def _frac(t):
    return {"√5/3": r5 / 3, "√3/2": r3 / 2}.get(t) or (lambda a, b: a / b)(*map(int, t.split("/")))


PYQS = [
    pyq(S2, 55, "q-tr-convert", "What is 3π/2 radians in degrees?", ["180°", "210°", "270°", "300°"], "c",
        ["π radians = 180°.", "3π/2 radians = 3 × 180° ÷ 2 = 270°."], lambda: 3 * 180 / 2, 270, 0, tech=["standard-values"],
        trick="π/2 is 90°, so 3π/2 is 3 × 90° = 270°."),
    pyq(S2, 65, "q-tr-complement", "If sin(90° − B) = 2/3, what is cos B?", ["1/3", "2/3", "√5/3", "√3/2"], "b",
        ["sin(90° − B) = cos B.", "So cos B = 2/3."], lambda: 2 / 3, 2 / 3, 1e-9, tech=["identity"], optvals=[_frac(t) for t in ("1/3", "2/3", "√5/3", "√3/2")],
        trick="Same value: sin of the complement is cos. No working needed.",
        wrong={"a": mistake("Took 1 − 2/3 = 1/3.", 1 / 3, 1e-9), "c": mistake("This is sin B = √(1 − 4/9) = √5/3, not cos B.", r5 / 3, 1e-9),
               "d": bound("No step of the working gives √3/2; the answer is the given value itself.", lambda v: abs(v - 2 / 3) > 1e-6)}),
    pyq(S2, 74, "q-tr-triangle", "If cos A = 5/13 and A is acute, find tan A.", ["5/12", "12/5", "13/12", "12/13"], "b",
        ["Base 5, hypotenuse 13, so height = √(13² − 5²) = 12.", "tan A = height ÷ base = 12/5."], lambda: 12 / 5, 12 / 5, 1e-9, tech=["standard-values"],
        optvals=[_frac(t) for t in ("5/12", "12/5", "13/12", "12/13")],
        trick="5–12–13 triangle. tan is opposite over adjacent, so 12/5, and it must be above 1 because cos A < sin A.",
        wrong={"a": mistake("Adjacent ÷ opposite is cot A = 5/12, not tan A.", 5 / 12, 1e-9), "c": mistake("Hypotenuse ÷ opposite is cosec A = 13/12.", 13 / 12, 1e-9),
               "d": mistake("Opposite ÷ hypotenuse is sin A = 12/13.", 12 / 13, 1e-9)}),
]
PYQS = PYQS + PYQS_C21TR


def practice_items():
    return []
