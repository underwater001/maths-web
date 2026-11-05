"""Surds and indices: quiz tier."""
import math, re
from bank import bound, mistake, pyq

K1 = "kiran-ch01-t01"

TOPIC = "surds-indices"
PREFIX = "sd"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
r3, r5, r6, r7, r12 = (math.sqrt(x) for x in (3, 5, 6, 7, 12))

NODES = {
    "c-sd-compare": {"short": "Compare surds", "label": "Comparing surd expressions", "kind": "concept", "parent": TOPIC, "order": 1,
                     "summary": "Square both sides (both positive) so the roots shrink, or compare decimals.", "links": ["simplification"]},
    "c-sd-conjugate": {"short": "Conjugates", "label": "Conjugates and rationalising", "kind": "concept", "parent": TOPIC, "order": 2,
                       "summary": "(a + √b)(a − √b) = a² − b removes the root. Pairs of conjugates often cancel to a clean number.", "links": ["algebraic-identities"]},
    "q-sd-compare": {"short": "Compare surds", "label": "Which surd expression is greater?", "kind": "qtype", "parent": "c-sd-compare", "order": 1,
                     "summary": "Sums of square roots on each side; decide <, > or =.", "links": []},
    "q-sd-rationalise": {"short": "Rationalise", "label": "Rationalise and simplify", "kind": "qtype", "parent": "c-sd-conjugate", "order": 1,
                         "summary": "Fractions with surds in the denominator, then an expression in x.", "links": []},
}
FORMULAS = [
    {"id": "sd-f1", "node": "c-sd-compare", "text": "(√a + √b)² = a + b + 2√(ab)", "note": "Squaring both sides makes the comparison one of 2√(ab) terms."},
    {"id": "sd-f2", "node": "c-sd-compare", "text": "For positive A, B: A < B ⇔ A² < B²", "note": "Never square if a side can be negative."},
    {"id": "sd-f3", "node": "c-sd-conjugate", "text": "1/(a + √b) = (a − √b)/(a² − b)", "note": "Multiply top and bottom by the conjugate."},
    {"id": "sd-f4", "node": "c-sd-conjugate", "text": "(a + √b)(a − √b) = a² − b     (5 + 2√6)(5 − 2√6) = 1", "note": "Why 5 + 2√6 and 5 − 2√6 are reciprocals."},
]
METHODS = {
    "q-sd-compare": {
        "cue": "'Which is greater?' with two sums of square roots.",
        "formulas": ["sd-f1", "sd-f2"], "tech": ["estimate", "identity"],
        "standard": "Square both sides: (√5 + √7)² = 12 + 2√35 and (√12 + √3)² = 15 + 2√36 = 27. Compare 2√35 ≈ 11.83 with 12 (a² = 23.83 < 27).",
        "fast": "Use decimals: √5 + √7 ≈ 2.24 + 2.65 = 4.88; √12 + √3 ≈ 3.46 + 1.73 = 5.20.",
        "eliminate": "'Cannot be determined' is almost never right when the numbers are all known. If one decimal sum is clearly larger, equality is out too.",
        "traps": ["Assuming √a + √b = √(a + b).", "Comparing under the roots (5 + 7 against 12 + 3), which says equal.", "Choosing 'cannot be determined' because the roots look awkward."]},
    "q-sd-rationalise": {
        "cue": "A surd in a denominator, or x = (a + √b)/(a − √b) and a value of an expression in x.",
        "formulas": ["sd-f3", "sd-f4"], "tech": ["rationalise", "identity"],
        "standard": "Multiply by the conjugate. For x = √((5 + 2√6)/(5 − 2√6)): the fraction equals (5 + 2√6)², so x = 5 + 2√6. Then x² + 3x − 15 = 49 + 20√6 + 15 + 6√6 − 15 = 49 + 26√6.",
        "fast": "Spot conjugate pairs: 1/(5 + √3) + 1/(5 − √3) = 10/(25 − 3), so the whole expression is 10/22 − 10/22 = 0.",
        "eliminate": "Compare the rational and root parts separately in the options (a + b√6): the √6 coefficient is 20 + 6 = 26, which singles out one option.",
        "traps": ["Squaring (5 + 2√6) without the middle term: 25 + 24 instead of 49 + 20√6.", "Forgetting the conjugate changes the sign inside only.", "Adding fractions with different denominators without rationalising."]},
}


def _ab(t):
    m = re.fullmatch(r"(\d+) \+ (\d+)√6", t); return int(m[1]) + int(m[2]) * r6


def _plain(t):
    return {"√3": r3}.get(t) or float(t)


PYQS = [
    pyq(S2, 51, "q-sd-compare", "Let a = √5 + √7 and b = √12 + √3. Which is greater?", ["a = b", "a > b", "a < b", "Cannot be determined"], "c",
        ["Square both: a² = 12 + 2√35 ≈ 12 + 11.83 = 23.83.", "b² = 15 + 2√36 = 15 + 12 = 27.", "Both sides are positive and a² < b², so a < b (4.88 < 5.20)."],
        lambda: 1, 1, 0, tech=["estimate", "identity"], optvals=[1 if abs((r5 + r7) - (r12 + r3)) < 1e-12 else 0, 1 if (r5 + r7) > (r12 + r3) else 0, 1 if (r5 + r7) < (r12 + r3) else 0, 0],
        trick="Decimals do it: 2.24 + 2.65 = 4.89 against 3.46 + 1.73 = 5.19.",
        wrong={"a": bound("The two sums are 4.88 and 5.20, not equal.", lambda v: v == 0), "b": bound("a ≈ 4.88 is smaller than b ≈ 5.20.", lambda v: v == 0), "d": bound("Both numbers are known, so they can be compared.", lambda v: v == 0)}),
    pyq(S2, 73, "q-sd-rationalise", "If x = √((5 + 2√6)/(5 − 2√6)), find the value of x² + 3x − 15.", ["50 + 12√6", "40 + 23√6", "49 + 26√6", "35 + 15√6"], "c",
        ["(5 + 2√6)(5 − 2√6) = 25 − 24 = 1, so 1/(5 − 2√6) = 5 + 2√6.", "The fraction is (5 + 2√6)/(5 − 2√6) = (5 + 2√6)², so x = 5 + 2√6.", "x² = 49 + 20√6, 3x = 15 + 6√6.", "x² + 3x − 15 = 49 + 20√6 + 15 + 6√6 − 15 = 49 + 26√6."],
        lambda: (lambda x: x * x + 3 * x - 15)(math.sqrt((5 + 2 * r6) / (5 - 2 * r6))), 49 + 26 * r6, 1e-9, tech=["rationalise", "identity"], concepts=2, heavy=True,
        trick="The √6 part of the answer is 20 (from x²) + 6 (from 3x) = 26. Only option (c) has 26√6.",
        optvals=[_ab(t) for t in ("50 + 12√6", "40 + 23√6", "49 + 26√6", "35 + 15√6")],
        wrong={"a": bound("The √6 part must be 20 + 6 = 26, but this option has 12.", lambda v: abs(v - (49 + 26 * r6)) > 1e-6), "b": bound("The √6 part must be 26, but this option has 23.", lambda v: abs(v - (49 + 26 * r6)) > 1e-6),
               "d": bound("The √6 part must be 26, but this option has 15.", lambda v: abs(v - (49 + 26 * r6)) > 1e-6)}),
    pyq(S3, 67, "q-sd-rationalise", "Simplify: 1/(5 + √3) + 1/(5 − √3) − 10/(25 − 3).", ["0", "1", "2", "√3"], "a",
        ["1/(5 + √3) + 1/(5 − √3) = ((5 − √3) + (5 + √3)) / (25 − 3) = 10/22.", "10/22 − 10/22 = 0."],
        lambda: 1 / (5 + r3) + 1 / (5 - r3) - 10 / (25 - 3), 0, 1e-9, tech=["rationalise", "identity"], optvals=[_plain(t) for t in ("0", "1", "2", "√3")],
        trick="The first two fractions together already equal 10/22, which is exactly what is subtracted.",
        wrong={"b": bound("The sum of the two fractions is 10/22 and so is the subtracted term. They cancel to 0, not 1.", lambda v: v != 0),
               "c": bound("The expression cancels completely to 0.", lambda v: v != 0), "d": bound("No root is left once the conjugates are added.", lambda v: v != 0)}),
    pyq(K1, 33, "q-sd-compare", 'Which of the following is true?', ['24^(1/9) < 6^(1/6) < 2^(1/2)', '6^(1/6) < 2^(1/2) < 24^(1/9)', '2^(1/2) < 24^(1/9) < 6^(1/6)', '2^(1/2) < 6^(1/6) < 24^(1/9)'], "b",
        ['Bring to a common root index 18: 6^(1/6) = 216^(1/18), 2^(1/2) = 512^(1/18), 24^(1/9) = 576^(1/18).', '216 < 512 < 576, so 6^(1/6) < 2^(1/2) < 24^(1/9).'],
        lambda: int(6 ** (1 / 6) < 2 ** 0.5 < 24 ** (1 / 9)), 1, 0, tech=['bounds'], optvals=[int(24 ** (1 / 9) < 6 ** (1 / 6) < 2 ** 0.5), int(6 ** (1 / 6) < 2 ** 0.5 < 24 ** (1 / 9)), int(2 ** 0.5 < 24 ** (1 / 9) < 6 ** (1 / 6)), int(2 ** 0.5 < 6 ** (1 / 6) < 24 ** (1 / 9))], trick='Common index 18 (the LCM of 2, 6, 9): compare 216, 512 and 576.'),
    pyq(K1, 34, "q-sd-compare", 'Which of the following is true?', ['5^(1/2) < 9^(1/3) < 21^(1/4)', '1/21^(1/4) > 1/9^(1/3) > 1/5^(1/2)', '1/9^(1/3) > 1/21^(1/4) > 1/5^(1/2)', '1/9^(1/3) > 1/5^(1/2) > 1/21^(1/4)'], "c",
        ['Common index 12: 5^(1/2) = 15625^(1/12), 9^(1/3) = 6561^(1/12), 21^(1/4) = 9261^(1/12).', 'So 9^(1/3) < 21^(1/4) < 5^(1/2) (6561 < 9261 < 15625). Reciprocals reverse it: 1/9^(1/3) > 1/21^(1/4) > 1/5^(1/2).'],
        lambda: int(1 / 9 ** (1 / 3) > 1 / 21 ** 0.25 > 1 / 5 ** 0.5), 1, 0, tech=['bounds'], optvals=[int(5 ** 0.5 < 9 ** (1 / 3) < 21 ** 0.25), int(1 / 21 ** 0.25 > 1 / 9 ** (1 / 3) > 1 / 5 ** 0.5), int(1 / 9 ** (1 / 3) > 1 / 21 ** 0.25 > 1 / 5 ** 0.5), int(1 / 9 ** (1 / 3) > 1 / 5 ** 0.5 > 1 / 21 ** 0.25)], trick='Common index 12 (6561 < 9261 < 15625), then flip the order for reciprocals.'),
]


def practice_items():
    return []
