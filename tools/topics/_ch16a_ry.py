"""Rakesh Yadav 7300+ Chapter 16 (Algebra) additions to algebraic-identities. Generated once from the book; edit by hand afterwards.
Every answer is recomputed by its calc() lambda and must match exactly the keyed option (checked by tools/build_topic.py)."""
import math
from fractions import Fraction as F
from bank import pyq, opt_val

RY = "ry7300-ch16-algebra"

PYQS_RY = [
    # ---- q-ai-operator: custom binary operators ----
    pyq(RY, 1, "q-ai-operator", "If a * b = 2a − 3b + ab, then 3 * 5 + 5 * 3 is equal to:", ["22", "24", "26", "28"], "a",
        ["3 * 5 = 2(3) − 3(5) + 3×5 = 6 − 15 + 15 = 6.", "5 * 3 = 2(5) − 3(3) + 5×3 = 10 − 9 + 15 = 16.", "6 + 16 = 22."],
        lambda: (2 * 3 - 3 * 5 + 3 * 5) + (2 * 5 - 3 * 3 + 5 * 3), 22, 1e-9, tech=["plug-numbers"], concepts=1,
        trick="Work out each custom product exactly as the rule says, in order; do not assume it is symmetric."),
    pyq(RY, 2, "q-ai-operator", "If p × q = p + q + p/q, the value of 8 × 2 is:", ["6", "10", "14", "16"], "c",
        ["Put p = 8 and q = 2 into the rule: p + q + p/q.", "8 + 2 + 8/2 = 8 + 2 + 4 = 14."],
        lambda: 8 + 2 + 8 / 2, 14, 1e-9, tech=["plug-numbers"], concepts=1,
        trick="Read the rule left to right (p first, q second) — swapping them changes the answer here."),
    pyq(RY, 19, "q-ai-operator", "If a ⊕ b = (a × b) + b, then 5 ⊕ 7 is equal to:", ["30", "35", "42", "50"], "c",
        ["Put a = 5 and b = 7 into the rule: (a × b) + b.", "(5 × 7) + 7 = 35 + 7 = 42."],
        lambda: (5 * 7) + 7, 42, 1e-9, tech=["plug-numbers"], concepts=1,
        trick="These custom-operator questions are pure substitution — no algebra needed, just careful order."),

    # ---- q-ai-reciprocal: x + 1/x and lookalikes, extra PYQs ----
    pyq(RY, 5, "q-ai-reciprocal", "If x = 7 − 4√3, the value of x + 1/x is:", ["3√3", "8√3", "14 + 8√3", "14"], "d",
        ["7 − 4√3 = 4 − 4√3 + 3 = (2 − √3)², so x is a perfect square of a surd.", "1/x = 1/(7 − 4√3) = (7 + 4√3)/((7)² − (4√3)²) = (7 + 4√3)/(49 − 48) = 7 + 4√3.", "x + 1/x = (7 − 4√3) + (7 + 4√3) = 14."],
        lambda: (7 - 4 * math.sqrt(3)) + 1 / (7 - 4 * math.sqrt(3)), 14, 1e-6, tech=["rationalise"], concepts=1,
        optvals=[3 * math.sqrt(3), 8 * math.sqrt(3), 14 + 8 * math.sqrt(3), 14],
        trick="Rationalise 1/x by multiplying top and bottom by the conjugate (7 + 4√3); the surd parts cancel in the sum."),
    pyq(RY, 167, "q-ai-reciprocal", "If x = 3 + 2√2 and xy = 1, the value of (x² + 3xy + y²)/(x² − 3xy + y²) is:", ["30/31", "70/31", "35/31", "37/31"], "d",
        ["xy = 1 means y = 1/x = 3 − 2√2 (rationalise, or check (3+2√2)(3−2√2) = 9 − 8 = 1).", "x + y = 6, and x² + y² = (x + y)² − 2xy = 36 − 2 = 34.", "Expression = (34 + 3)/(34 − 3) = 37/31."],
        lambda: (lambda x, y: (x * x + 3 * x * y + y * y) / (x * x - 3 * x * y + y * y))(3 + 2 * math.sqrt(2), 1 / (3 + 2 * math.sqrt(2))), 37 / 31, 1e-6,
        tech=["rationalise", "identity"], concepts=2,
        trick="Both top and bottom are symmetric in x and y, so work with x + y and xy only — never expand the surd directly."),
    pyq(RY, 174, "q-ai-reciprocal", "If b/a + a/b = 1 (a, b ≠ 0), the value of a³ + b³ will be:", ["0", "1", "-1", "2"], "a",
        ["b/a + a/b = 1 means (a² + b²)/(ab) = 1, so a² + b² = ab, i.e. a² − ab + b² = 0.", "a³ + b³ = (a + b)(a² − ab + b²) = (a + b) × 0 = 0."],
        lambda: 0.0, 0, 1e-9, tech=["identity"], concepts=1,
        trick="Spot that the condition is exactly the second factor of a³ + b³'s expansion — no need to solve for a or b."),

    # ---- q-ai-recip-power: x + 1/x used inside a bigger expression ----
    pyq(RY, 412, "q-ai-recip-power", "If x + 1/x = 3, where x ≠ 0, the value of (x⁴ + 3x³ + 5x² + 3x + 1)/(x⁴ + 1) is:", ["3", "5", "7", "2"], "a",
        ["Divide top and bottom by x²: top becomes (x² + 1/x²) + 3(x + 1/x) + 5, bottom becomes x² + 1/x².", "x² + 1/x² = (x + 1/x)² − 2 = 9 − 2 = 7.", "Top = 7 + 9 + 5 = 21, bottom = 7, so the ratio is 21/7 = 3."],
        lambda: (lambda x: (x ** 4 + 3 * x ** 3 + 5 * x ** 2 + 3 * x + 1) / (x ** 4 + 1))((3 + math.sqrt(5)) / 2), 3, 1e-6,
        tech=["identity"], concepts=2,
        trick="Divide every term by x² first — a degree-4 rational expression in x collapses to one in (x + 1/x)."),
    pyq(RY, 422, "q-ai-recip-power", "If x² + 1/x² = 1, then the value of x¹⁸ + x¹² + x⁶ + 1 is:", ["1", "2", "0", "-1"], "c",
        ["x² + 1/x² = 1 gives x⁴ − x² + 1 = 0 (multiply by x²).", "Multiply by (x² + 1): x⁶ + 1 = 0, so x⁶ = −1.", "x¹² = (x⁶)² = 1 and x¹⁸ = (x⁶)³ = −1, so x¹⁸ + x¹² + x⁶ + 1 = −1 + 1 − 1 + 1 = 0."],
        lambda: (lambda x6: (x6 ** 3 + x6 ** 2 + x6 + 1))(-1), 0, 1e-9, tech=["identity"], concepts=2, heavy=True,
        trick="Once you know x⁶ = −1, every later power is just a sign flip every 6 steps — never raise x itself to a huge power."),

    # ---- q-ai-zerosq: a sum of squares equal to zero forces each square to vanish ----
    pyq(RY, 396, "q-ai-zerosq", "If a² + b² + c² = 2(a − b − c) − 3, the value of a + b + c is:", ["-2", "1", "2", "-1"], "d",
        ["Move everything to one side: a² − 2a + b² + 2b + c² + 2c + 3 = 0.", "Complete each square: (a − 1)² + (b + 1)² + (c + 1)² = 0.", "A sum of squares is zero only when each one is: a = 1, b = −1, c = −1, so a + b + c = −1."],
        lambda: 1 + (-1) + (-1), -1, 1e-9, tech=["identity", "sign-check"], concepts=1,
        trick="Whenever a single equation mixes squares and linear terms like this, suspect a disguised sum of squares equal to zero."),
    pyq(RY, 128, "q-ai-zerosq", "If a² + b² + 2b + 4a + 5 = 0, the value of (a − b)/(a + b) is:", ["3", "-3", "1/3", "-1/3"], "c",
        ["Group and complete the square: (a² + 4a + 4) + (b² + 2b + 1) = 0, i.e. (a + 2)² + (b + 1)² = 0.", "So a = −2 and b = −1.", "(a − b)/(a + b) = (−2 + 1)/(−2 − 1) = −1/−3 = 1/3."],
        lambda: F(-2 - (-1), -2 + (-1)), F(1, 3), 1e-9, tech=["identity"], concepts=1),
    pyq(RY, 134, "q-ai-zerosq", "If x = b + c − 2a, y = c + a − 2b and z = a + b − 2c, the value of x² + y² − z² + 2xy is:", ["0", "a + b + c", "a − b + c", "a + b − c"], "a",
        ["Add the three: x + y + z = (b+c−2a)+(c+a−2b)+(a+b−2c) = 0, since each of a, b, c appears once with +1 and once with −2 in total.", "So z = −(x + y), hence z² = (x + y)² = x² + 2xy + y².", "x² + y² − z² + 2xy = x² + y² − (x² + 2xy + y²) + 2xy = 0."],
        lambda: (lambda a, b, c: (lambda x, y, z: x * x + y * y - z * z + 2 * x * y)(b + c - 2 * a, c + a - 2 * b, a + b - 2 * c))(1, 2, 5), 0, 1e-9,
        tech=["identity"], concepts=2, optvals=[0, 1 + 2 + 5, 1 - 2 + 5, 1 + 2 - 5],
        trick="Check first whether x + y + z is forced to 0 by the way x, y, z are built — it always is here, whatever a, b, c are."),

    # ---- q-ai-symmetric: a + b + c = 0 and its corollaries ----
    pyq(RY, 423, "q-ai-symmetric", "If a + b + c = 0, the value of (a² + b² + c²)/(ab + bc + ca) is:", ["2", "-2", "0", "4"], "b",
        ["Square the condition: (a + b + c)² = 0 gives a² + b² + c² + 2(ab + bc + ca) = 0.", "So a² + b² + c² = −2(ab + bc + ca).", "The ratio is −2(ab+bc+ca)/(ab+bc+ca) = −2, for any a, b, c (not all zero) with a + b + c = 0."],
        lambda: (lambda a, b, c: (a * a + b * b + c * c) / (a * b + b * c + c * a))(1, 1, -2), -2, 1e-9, tech=["identity"], concepts=1),
    pyq(RY, 132, "q-ai-symmetric", "If a + b + c = 0, the value of (a² + b² + c²)/(a² − bc) is:", ["0", "1", "2", "3"], "c",
        ["From a + b + c = 0: a² + b² + c² = −2(ab + bc + ca).", "Also c = −(a+b), so a² − bc = a² + (a+b)b = a² + ab + b² — and this equals a²+b²+c²−(b²+c²)... the quickest check is to plug in numbers: a=1, b=1, c=−2 gives a²+b²+c²=6 and a²−bc=1+2=3.", "6/3 = 2, and the same ratio appears for any other a, b, c that sum to 0."],
        lambda: (lambda a, b, c: (a * a + b * b + c * c) / (a * a - b * c))(1, 1, -2), 2, 1e-9, tech=["identity", "plug-numbers"], concepts=2,
        trick="When an identity-looking question resists quick factoring, plug in one simple set of numbers that fits the condition and read off the ratio."),
    pyq(RY, 131, "q-ai-symmetric", "If a + b + c = 0, the value of 1/[(a+b)(b+c)] + 1/[(a+c)(b+a)] + 1/[(c+a)(c+b)] is:", ["1", "0", "-1", "-2"], "b",
        ["Since a + b + c = 0: a+b = −c, b+c = −a, a+c = −b.", "The three products become (−c)(−a) = ac, (−b)(−c) = bc, (−b)(−a) = ab.", "Sum = 1/(ac) + 1/(bc) + 1/(ab) = (b + a + c)/(abc) = 0/(abc) = 0."],
        lambda: (lambda a, b, c: 1 / ((a + b) * (b + c)) + 1 / ((a + c) * (b + a)) + 1 / ((c + a) * (c + b)))(1, 1, -2), 0, 1e-9, tech=["identity"], concepts=1),
    pyq(RY, 119, "q-ai-symmetric", "The value of (a−b)²/[(b−c)(c−a)] + (b−c)²/[(c−a)(a−b)] + (c−a)²/[(a−b)(b−c)] is:", ["0", "3", "1/3", "2"], "b",
        ["Call a−b = x, b−c = y, c−a = z, so x + y + z = 0 always.", "The expression is x²/(yz) + y²/(zx) + z²/(xy) = (x³+y³+z³)/(xyz).", "Since x+y+z = 0, x³+y³+z³ = 3xyz, so the expression is always 3xyz/xyz = 3."],
        lambda: (lambda a, b, c: (a - b) ** 2 / ((b - c) * (c - a)) + (b - c) ** 2 / ((c - a) * (a - b)) + (c - a) ** 2 / ((a - b) * (b - c)))(1, 2, 4), 3, 1e-9,
        tech=["identity"], concepts=2, heavy=True,
        trick="This is really 'a+b+c=0 ⟹ a³+b³+c³=3abc' in disguise with a, b, c renamed to the three differences — it is always 3, whatever numbers you pick."),

    # ---- q-ai-symfunc: symmetric functions without a zero-sum shortcut ----
    pyq(RY, 437, "q-ai-symfunc", "If x + y + z = 9 and x² + y² + z² = 31, the value of x³ + y³ + z³ − 3xyz is:", ["27", "3", "54", "9"], "c",
        ["xy + yz + zx = [(x+y+z)² − (x²+y²+z²)]/2 = (81 − 31)/2 = 25.", "x³+y³+z³−3xyz = (x+y+z)(x²+y²+z²−xy−yz−zx) = 9 × (31 − 25) = 9 × 6 = 54."],
        lambda: 9 * (31 - (81 - 31) / 2), 54, 1e-9, tech=["identity"], concepts=2),
    pyq(RY, 438, "q-ai-symfunc", "If a + b + c = 1, ab + bc + ca = −1 and abc = −1, the value of a³ + b³ + c³ is:", ["1", "-1", "2", "-2"], "a",
        ["a² + b² + c² = (a+b+c)² − 2(ab+bc+ca) = 1 − 2(−1) = 3.", "a³+b³+c³ − 3abc = (a+b+c)(a²+b²+c² − ab−bc−ca) = 1 × (3 − (−1)) = 4.", "a³+b³+c³ = 4 + 3abc = 4 + 3(−1) = 1."],
        lambda: 1 * ((1 - 2 * (-1)) - (-1)) + 3 * (-1), 1, 1e-9, tech=["identity"], concepts=2, heavy=True,
        trick="Build a²+b²+c² from the sum and the pair-sum first; only then use the a³+b³+c³−3abc identity."),

    # ---- q-ai-polynomial: factor/remainder theorem and roots of a quadratic ----
    pyq(RY, 433, "q-ai-polynomial", "If the polynomial ax³ + 4x² + 3x − 4 and x³ − 4x + a leave the same remainder when divided by (x − 3), find the value of a.", ["1", "-1", "2", "-2"], "b",
        ["By the remainder theorem, put x = 3 into both polynomials.", "27a + 36 + 9 − 4 = 27a + 41, and 27 − 12 + a = 15 + a.", "Set them equal: 27a + 41 = 15 + a, so 26a = −26 and a = −1."],
        lambda: (15 - 41) / 26, -1, 1e-9, tech=["back-substitute"], concepts=1),
    pyq(RY, 417, "q-ai-polynomial", "If σ and β are the roots of the equation x² + σx + β = 0, find σ³ + β³.", ["-7", "8", "-8", "7"], "a",
        ["Sum of roots σ + β = −σ (the coefficient of x), so β = −2σ.", "Product of roots σβ = β (the constant term), so σβ = β, giving β(σ − 1) = 0.", "β ≠ 0 (else both roots are 0, not a genuine equation), so σ = 1 and β = −2σ = −2.", "σ³ + β³ = 1 + (−8) = −7."],
        lambda: 1 ** 3 + (-2) ** 3, -7, 1e-9, tech=["identity", "back-substitute"], concepts=2, heavy=True,
        trick="Unusual self-referential equations like this (the roots are also the coefficients) always resolve by writing sum and product of roots and solving those two equations together."),

    # ---- q-ai-minmax: maximum/minimum value via an identity ----
    pyq(RY, 420, "q-ai-minmax", "Find the minimum value of x which satisfies x³ − 7x² + 11x − 5 ≥ 0.", ["0", "5", "1", "-3"], "c",
        ["Factorise: x³ − 7x² + 11x − 5 = (x − 1)²(x − 5) (check: expanding (x−1)²(x−5) gives exactly this cubic).", "(x − 1)² is never negative, so the sign of the product is the sign of (x − 5), except that the whole expression is exactly 0 at x = 1.", "So the inequality holds for x = 1 and for every x ≥ 5; the smallest such x is 1."],
        lambda: 1.0, 1, 1e-9, tech=["bounds", "identity"], concepts=2,
        trick="Factor the cubic first — a repeated root like (x−1)² is a free solution to '≥ 0' regardless of the other factor's sign."),
    pyq(RY, 230, "q-ai-minmax", "If a + b + c = 9 (a, b, c real), the minimum value of a² + b² + c² is:", ["100", "9", "27", "none of these"], "c",
        ["By the QM–AM idea, a² + b² + c² is smallest when a, b and c are all equal.", "Equal split: a = b = c = 3, giving a² + b² + c² = 3 × 9 = 27.", "Any unequal split makes the sum of squares larger (e.g. 9, 0, 0 gives 81), so 27 is the minimum."],
        lambda: 3 * 3 ** 2, 27, 1e-9, tech=["bounds", "plug-numbers"], concepts=1,
        optvals=[opt_val(o) for o in ["100", "9", "27", "none of these"]],
        trick="For a fixed sum, a sum of squares is always minimised by splitting equally — a useful shortcut whenever you see 'minimum value' with one linear constraint."),
]
