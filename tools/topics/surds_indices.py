"""Surds and indices: quiz tier."""
import math, re
from bank import bound, mistake, pyq
from topics._ix_ry import PYQS_RY

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
    "c-ix-indices": {"short": "Indices", "label": "Laws of indices and equations in powers", "kind": "concept", "parent": TOPIC, "order": 3,
                     "summary": "Write every base as a prime power, then add, subtract or multiply the exponents. Equal bases mean equal exponents.", "links": ["simplification", "number-system"]},
    "c-ix-nested": {"short": "Nested roots", "label": "Nested roots and infinite roots", "kind": "concept", "parent": TOPIC, "order": 4,
                    "summary": "a + b ± 2√(ab) is a perfect square; an infinite root √(n + √(n + …)) is the positive root of x² = n + x.", "links": ["quadratic-equations"]},
    "c-ix-identity": {"short": "Identity sums", "label": "Decimal sums that collapse by an identity", "kind": "concept", "parent": TOPIC, "order": 5,
                      "summary": "Ugly decimals are a³ ± b³ over a² ∓ ab + b², or a perfect square. Spot the identity and the answer is a ± b.", "links": ["algebraic-identities", "simplification"]},
    "q-ix-power": {"short": "Evaluate powers", "label": "Evaluate an expression with fractional and negative powers", "kind": "qtype", "parent": "c-ix-indices", "order": 1,
                   "summary": "(64)^(−2/3), 16^0.16 × 2^0.36, (243)^0.13 × (243)^0.07: reduce to prime powers.", "links": []},
    "q-ix-eq": {"short": "Solve for the power", "label": "Find x (or n) from an equation in powers", "kind": "qtype", "parent": "c-ix-indices", "order": 2,
                "summary": "27^(2n − 1) = 243³, 3^(x + 8) = 27^(2x + 1): same base, equate the exponents.", "links": []},
    "q-ix-nested": {"short": "Nested / infinite roots", "label": "Simplify a nested or infinite root", "kind": "qtype", "parent": "c-ix-nested", "order": 1,
                    "summary": "√(11 + 2√30), √(12 + √(12 + …)), √(10 + √(25 + √(108 + …))), sums of surds with a root-scale.", "links": []},
    "q-ix-identity": {"short": "Decimal identity", "label": "Collapse a decimal expression with an identity", "kind": "qtype", "parent": "c-ix-identity", "order": 1,
                      "summary": "(0.06³ − 0.05³) ÷ (0.06² + 0.06 × 0.05 + 0.05²), (a + b + c) forms, 137 and 133 type numbers.", "links": []},
}
FORMULAS = [
    {"id": "sd-f1", "node": "c-sd-compare", "text": "(√a + √b)² = a + b + 2√(ab)", "note": "Squaring both sides makes the comparison one of 2√(ab) terms."},
    {"id": "sd-f2", "node": "c-sd-compare", "text": "For positive A, B: A < B ⇔ A² < B²", "note": "Never square if a side can be negative."},
    {"id": "sd-f3", "node": "c-sd-conjugate", "text": "1/(a + √b) = (a − √b)/(a² − b)", "note": "Multiply top and bottom by the conjugate."},
    {"id": "sd-f4", "node": "c-sd-conjugate", "text": "(a + √b)(a − √b) = a² − b     (5 + 2√6)(5 − 2√6) = 1", "note": "Why 5 + 2√6 and 5 − 2√6 are reciprocals."},
    {"id": "ix-f1", "node": "c-ix-indices", "text": "aᵐ × aⁿ = aᵐ⁺ⁿ;  (aᵐ)ⁿ = aᵐⁿ;  a⁻ⁿ = 1/aⁿ;  a^(1/n) = ⁿ√a", "note": "Always reduce to one prime base first."},
    {"id": "ix-f2", "node": "c-ix-indices", "text": "If aˣ = aʸ (a ≠ 0, ±1) then x = y", "note": "Make the bases equal, then equate the exponents."},
    {"id": "ix-f3", "node": "c-ix-nested", "text": "√(a + b ± 2√(ab)) = √a ± √b", "note": "Split the number into a sum with the right product: 11 + 2√30: 6 + 5 = 11, 6 × 5 = 30."},
    {"id": "ix-f4", "node": "c-ix-nested", "text": "√(n + √(n + √(n + …))) = x where x² = x + n", "note": "For n = 12, 30, 72: x = 4, 6, 9 (consecutive factors of n)."},
    {"id": "ix-f5", "node": "c-ix-identity", "text": "a³ ± b³ = (a ± b)(a² ∓ ab + b²);  a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)", "note": "The quotient collapses to a ± b, or to a + b + c."},
    {"id": "ix-f6", "node": "c-ix-identity", "text": "1/(√(n + 1) + √n) = √(n + 1) − √n", "note": "A chain of such terms telescopes to the end roots only."},
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
    "q-ix-power": {
        "cue": "Fractional, decimal or negative powers of numbers like 16, 64, 243, 256.",
        "formulas": ["ix-f1"], "tech": ["identity"],
        "standard": "Write each base as a prime power, add exponents of the same base: 243^0.16 × 243^0.04 = 243^0.2 = 3.",
        "fast": "Add decimal exponents of the same base at once: 0.16 + 0.04 = 0.2, and 0.2 is the 5th root.",
        "eliminate": "Check the sign and size: a negative exponent gives a number below 1 for a base above 1.",
        "traps": ["Multiplying the exponents when the bases are multiplied (they are added).", "Dropping the negative sign on a fractional power.", "Taking a^(2/3) as the square root of a cube-root."]},
    "q-ix-eq": {
        "cue": "'If 3^(x + 8) = 27^(2x + 1), find x', or 3^x − 3^(x − 1) = 486.",
        "formulas": ["ix-f1", "ix-f2"], "tech": ["identity", "back-substitute"],
        "standard": "Convert to the same base (27 = 3³), equate the exponents and solve the linear equation. For 3^x − 3^(x − 1): take out 3^(x − 1).",
        "fast": "Plug the options: for 3^(x − 1) = 243 only x = 6 works.",
        "eliminate": "Test the smallest option first: the powers grow quickly.",
        "traps": ["Forgetting to multiply the exponent when converting 27^(2x + 1) = 3^(3(2x + 1)).", "Writing 3^x − 3^(x − 1) = 3^1."]},
    "q-ix-nested": {
        "cue": "Root inside a root, an endless √(n + √(n + …)), or a sum of such roots.",
        "formulas": ["ix-f3", "ix-f4"], "tech": ["identity", "back-substitute"],
        "standard": "Rewrite each inner root as (√a ± √b)²; for the infinite form solve x² = x + n and keep the positive root.",
        "fast": "Infinite root: split n into consecutive factors, 30 = 6 × 5, the answer is the larger one, 6. Or test each option.",
        "eliminate": "An infinite root is always larger than √n: √12 = 3.46 < x < 12.",
        "traps": ["Taking the negative root of x² = x + n.", "Splitting 11 + 2√30 as 5 + 6 but forgetting the product check (30).", "Working from the outside of a nested root when the inside is a perfect square."]},
    "q-ix-identity": {
        "cue": "Cubes and squares of ugly decimals, or numbers like 137, 133, 18221.",
        "formulas": ["ix-f5"], "tech": ["identity", "cancel-first"],
        "standard": "Match the pattern: a³ − b³ over a² + ab + b² = a − b; a³ + b³ + c³ − 3abc over its partner = a + b + c. Read a and b from the numbers.",
        "fast": "Check if the odd-looking number is a product (137 × 133 = 18221, 0.0016 = 0.08 × 0.02): it is the ab term.",
        "eliminate": "The answer is a sum or difference of the numbers shown, so the magnitude fixes the option.",
        "traps": ["Computing the cubes by hand.", "Reading a² − ab + b² as a² + ab + b² and getting a + b instead of a − b.", "Missing the extra 3abc in the a + b + c identity."]},
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

PYQS = PYQS + PYQS_RY


def practice_items():
    return []
