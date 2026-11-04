"""Trigonometric ratios: quiz tier."""
import math
from bank import bound, mistake, pyq

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
}
FORMULAS = [
    {"id": "tr-f1", "node": "c-tr-angles", "text": "π radians = 180°     1 radian ≈ 57.3°", "note": "3π/2 rad = 3 × 180° ÷ 2 = 270°."},
    {"id": "tr-f2", "node": "c-tr-ratios", "text": "sin(90° − θ) = cos θ     cos(90° − θ) = sin θ     tan(90° − θ) = cot θ", "note": "Complementary angles swap the pair."},
    {"id": "tr-f3", "node": "c-tr-ratios", "text": "sin²θ + cos²θ = 1;  with cos A = b/h, sin A = p/h and tan A = p/b where p² + b² = h²", "note": "5–12–13 and 3–4–5 triangles come up all the time."},
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


def practice_items():
    return []
