"""Simplification and BODMAS: quiz tier."""
import math
from fractions import Fraction as F
from bank import bound, mistake, pyq
from topics._sm_ry import PYQS_RY

TOPIC = "simplification"
PREFIX = "sm"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
K1 = "kiran-ch01-t01"
KH = sum(1 / j for j in range(1, 26))      # 1 + 1/2 + … + 1/25, for kiran Q41

NODES = {
    "c-sm-compare": {"short": "Compare fractions", "label": "Comparing and ordering fractions", "kind": "concept", "parent": TOPIC, "order": 1,
                     "summary": "Put fractions against a common yardstick (a decimal, or a benchmark like 0.6) instead of finding a common denominator.", "links": []},
    "c-sm-bodmas": {"short": "BODMAS", "label": "BODMAS with nested fractions", "kind": "concept", "parent": TOPIC, "order": 2,
                    "summary": "Work from the innermost bracket outwards, keep fractions exact, and estimate first so options can be struck.", "links": ["surds-indices"]},
    "q-sm-order": {"short": "Order fractions", "label": "Arrange fractions in order", "kind": "qtype", "parent": "c-sm-compare", "order": 1,
                   "summary": "Four fractions to put in ascending or descending order.", "links": []},
    "q-sm-bodmas": {"short": "Nested BODMAS", "label": "Evaluate nested brackets and mixed numbers", "kind": "qtype", "parent": "c-sm-bodmas", "order": 1,
                    "summary": "Brackets inside brackets, mixed numbers and a division; or a very plain sum with decimals.", "links": []},
    "q-sm-continued": {"short": "Continued fraction", "label": "Continued fraction", "kind": "qtype", "parent": "c-sm-bodmas", "order": 2,
                       "summary": "3 + 1/(2 + 1/(5 + 1/3)): start from the bottom.", "links": []},
    "q-sm-decimal": {"short": "Decimals", "label": "Decimal fractions: cancel before you multiply", "kind": "qtype", "parent": "c-sm-bodmas", "order": 3,
                     "summary": "Products and quotients of decimals, or a series of decimal fractions that all reduce to the same value.", "links": []},
    "q-sm-roots": {"short": "Roots of decimals", "label": "Square roots of decimal numbers", "kind": "qtype", "parent": "c-sm-bodmas", "order": 4,
                   "summary": "Sums of √0.49, √59.29 … and statements to be judged true or false.", "links": ["surds-indices"]},
    "q-sm-harmonic": {"short": "Fraction series", "label": "Series of fractions with a known partial sum", "kind": "qtype", "parent": "c-sm-bodmas", "order": 5,
                      "summary": "A series like 5/6 + 5/9 + 5/12 + … written in terms of 1 + 1/2 + 1/3 + … = k.", "links": []},
    "q-sm-root-trick": {"short": "Perfect-square trick", "label": "Expression under a root that is a perfect square", "kind": "qtype", "parent": "c-sm-bodmas", "order": 6,
                        "summary": "N = a² − a − (a − 1) and √N asked: rewrite as (a − 1)².", "links": ["algebraic-identities"]},
    "c-sy-squares": {"short": "Squares and cubes", "label": "Perfect squares and cubes by multiplying, dividing, adding or subtracting", "kind": "concept", "parent": TOPIC, "order": 3,
                     "summary": "Write the number in primes. A square needs every power even, a cube every power a multiple of 3. Add or subtract: bracket the number between two squares or cubes.", "links": ["number-system", "surds-indices"]},
    "c-sy-identity": {"short": "Identity sums", "label": "Decimal sums that collapse by an identity", "kind": "concept", "parent": TOPIC, "order": 4,
                      "summary": "a² − b², a³ ± b³, a + b + c = 0: spot the pattern and the answer is a ± b, a + b + c or 3abc.", "links": ["algebraic-identities"]},
    "c-sy-word": {"short": "Number puzzles", "label": "Short number puzzles on squares, sums and differences", "kind": "concept", "parent": TOPIC, "order": 5,
                  "summary": "Two numbers with a given sum, difference, product or sum of squares; counting squares in a range; digits in a root.", "links": ["algebraic-identities", "number-system"]},
    "q-sy-square": {"short": "Make a square / cube", "label": "Least number to make a perfect square or cube", "kind": "qtype", "parent": "c-sy-squares", "order": 1,
                    "summary": "Multiply, divide, add or subtract the smallest number so that 5808, 1323, 63522 … becomes a perfect square or cube.", "links": []},
    "q-sy-identity": {"short": "Identity decimals", "label": "Collapse a decimal expression with an identity", "kind": "qtype", "parent": "c-sy-identity", "order": 1,
                      "summary": "(2.644² − 2.356²) ÷ 0.288, (0.1³ + 0.2³ + 0.3³ − 3 × 0.1 × 0.2 × 0.3) ÷ …, 22³ + (−15)³ + (−7)³.", "links": []},
    "q-sy-word": {"short": "Number puzzles", "label": "Find the numbers from a sum, product or sum of squares", "kind": "qtype", "parent": "c-sy-word", "order": 1,
                  "summary": "Sum of squares 100, difference of squares 28; perfect squares between 50 and 1000; digits in √62478078.", "links": []},
    "q-sy-compare": {"short": "Compare roots", "label": "Which root expression is the greatest or the true statement", "kind": "qtype", "parent": "c-sm-compare", "order": 2,
                     "summary": "Pick the largest of √a − √b pairs, or decide √5 + √3 against √6 + √2.", "links": []},}
FORMULAS = [
    {"id": "sm-f1", "node": "c-sm-compare", "text": "a/b < c/d  ⇔  a×d < c×b   (cross-multiply, b and d positive)", "note": "Or compare each fraction with a benchmark such as 1/2 or 0.6."},
    {"id": "sm-f2", "node": "c-sm-compare", "text": "Closer to 1 means a smaller gap: a/b = 1 − (b − a)/b", "note": "5/9 = 1 − 4/9 and 4/7 = 1 − 3/7: compare 4/9 and 3/7."},
    {"id": "sm-f3", "node": "c-sm-bodmas", "text": "Order: Brackets (innermost first), Of, Division, Multiplication, Addition, Subtraction", "note": "Mixed numbers: change 8⅓ to 25/3 before any division."},
    {"id": "sm-f4", "node": "c-sm-bodmas", "text": "a ÷ (b/c) = a × (c/b)", "note": "Dividing by a fraction is multiplying by its flip."},
    {"id": "sm-f5", "node": "c-sm-bodmas", "text": "Cancel before multiplying: (a × b) ÷ (c × d) → pair numerator and denominator factors that share a factor.", "note": "Decimals: shift the point the same number of places in numerator and denominator."},
    {"id": "sm-f6", "node": "c-sm-bodmas", "text": "√0.49 = 0.7, √0.0049 = 0.07, √59.29 = 7.7: the root has half as many decimal places.", "note": "Take the root of the digits, then place the point."},
    {"id": "sm-f7", "node": "c-sm-bodmas", "text": "c/(3 × 2) + c/(3 × 3) + … = (c/3)(1/2 + 1/3 + …)", "note": "Remove the common factor, then match the remaining series with the known one."},
    {"id": "sm-f8", "node": "c-sm-bodmas", "text": "a² − 2a + 1 = (a − 1)²", "note": "Express the small numbers through the big one (98764 = 98765 − 1)."},
    {"id": "sy-f1", "node": "c-sy-squares", "text": "Perfect square: every prime power even.  Perfect cube: every prime power a multiple of 3.", "note": "1323 = 3³ × 7²: multiply by 7 for a cube."},
    {"id": "sy-f2", "node": "c-sy-squares", "text": "Add or subtract: find the nearest square or cube above or below.", "note": "63522: 252² = 63504, so subtract 18."},
    {"id": "sy-f3", "node": "c-sy-identity", "text": "a² − b² = (a − b)(a + b);  a³ ± b³ = (a ± b)(a² ∓ ab + b²)", "note": "The quotient collapses to a ± b."},
    {"id": "sy-f4", "node": "c-sy-identity", "text": "If a + b + c = 0 then a³ + b³ + c³ = 3abc", "note": "22 − 15 − 7 = 0, so 22³ − 15³ − 7³ = 3 × 22 × (−15) × (−7) = 6930."},
    {"id": "sy-f5", "node": "c-sy-word", "text": "x² + y² = (x + y)² − 2xy = (x − y)² + 2xy;  x² − y² = (x + y)(x − y)", "note": "Sum 22 and sum of squares 404: xy = (484 − 404)/2 = 40."},
    {"id": "sy-f6", "node": "c-sy-word", "text": "Digits in the square root of an n-digit number: n/2 (n even) or (n + 1)/2 (n odd)", "note": "62478078 has 8 digits, so its root has 4."},
    {"id": "sy-f7", "node": "c-sm-compare", "text": "√a − √b = (a − b)/(√a + √b)", "note": "Equal gaps: the pair with the smaller numbers gives the larger difference."},
]

METHODS = {
    "q-sm-order": {
        "cue": "'Arrange the fractions … in ascending / descending order.'",
        "formulas": ["sm-f1", "sm-f2"], "tech": ["fraction-percent", "estimate"],
        "standard": "Convert each to a decimal (5/9 = 0.556, 4/7 = 0.571, 3/5 = 0.6, 7/11 = 0.636) and sort.",
        "fast": "Pick a benchmark like 3/5 = 0.6 and sort the others into 'below' and 'above' (cross-multiply once each).",
        "eliminate": "Look at the first and last item of each option. 3/5 is bigger than 5/9 and 4/7, so it cannot be first. That alone removes two options.",
        "traps": ["Comparing numerators or denominators alone.", "Reading ascending as descending."]},
    "q-sm-bodmas": {
        "cue": "A long expression with brackets inside brackets, mixed numbers and ÷, or a short one with decimals.",
        "formulas": ["sm-f3", "sm-f4"], "tech": ["estimate", "cancel-first"],
        "standard": "Innermost bracket first: 5/6 − 1/6 = 2/3; 1/3 × 2/3 = 2/9; 2/5 − 2/9 = 8/45; 7/9 ÷ 8/45 = 35/8; then 25/3 − 35/8 = 95/24.",
        "fast": "Estimate while you work: 8.33 − (0.78 ÷ 0.18) ≈ 8.33 − 4.4 ≈ 3.9. Only 95/24 ≈ 3.96 is near.",
        "eliminate": "Estimate the whole expression to one decimal; options with the wrong sign or size go at once (−41/15 is negative, 32/3 is above 10).",
        "traps": ["Doing the division before the bracket.", "Leaving 8⅓ as 8 + 1/3 inside the division.", "Adding instead of subtracting inside the middle bracket."]},
    "q-sm-continued": {
        "cue": "A fraction whose denominator contains another fraction, stacked.",
        "formulas": ["sm-f4"], "tech": ["cancel-first", "estimate"],
        "standard": "Start at the bottom: 5 + 1/3 = 16/3; 1/(16/3) = 3/16; 2 + 3/16 = 35/16; 1/(35/16) = 16/35; 3 + 16/35 = 121/35.",
        "fast": "Estimate: 5.33 → 0.19 → 2.19 → 0.457 → 3.457. Then 121/35 = 3.457 is the match.",
        "eliminate": "The value is a little above 3 (3 + a fraction less than 1/2). Options above 3.5 or below 3 are out.",
        "traps": ["Starting at the top.", "Flipping the wrong layer.", "Adding 1/3 to 5 and forgetting to flip before adding 2."]},
    "q-sm-decimal": {
        "cue": "Several decimals multiplied and divided, or a row of decimal fractions that look the same.",
        "formulas": ["sm-f5"], "tech": ["cancel-first"],
        "standard": "Remove the decimals (multiply top and bottom by the same power of 10) and cancel before you multiply.",
        "fast": "A row of fractions where numerator and denominator shrink together: every term has the same value; multiply by the count.",
        "eliminate": "Estimate each part to one significant figure; options far from that are out.",
        "traps": ["Misplacing the decimal point after multiplying.", "Adding the terms as if they differed."]},
    "q-sm-roots": {
        "cue": "A true/false statement with several square roots of decimals.",
        "formulas": ["sm-f6"], "tech": ["estimate"],
        "standard": "Take each root exactly (0.49 → 0.7, 0.0049 → 0.07, 59.29 → 7.7) and add; compare with the right side.",
        "fast": "Roots of decimals: halve the number of decimal places, then take the integer root.",
        "eliminate": "Check the last decimal place: the sum of the roots' last digits must match the claimed total.",
        "traps": ["√0.0049 = 0.07 not 0.7.", "Not testing both statements."]},
    "q-sm-harmonic": {
        "cue": "A series whose terms are a constant times 1/2, 1/3, 1/4 … and a known sum k.",
        "formulas": ["sm-f7"], "tech": ["identity"],
        "standard": "Factor out the constant; match the remaining series with the known one and remove any missing first term.",
        "fast": "The first term 1 of 1 + 1/2 + … is not in the new series, so subtract it: k − 1.",
        "eliminate": "Compare sizes: the new sum has no 1 and a 5/3 multiplier.",
        "traps": ["Forgetting to remove the first term 1.", "Using 5/6 as the first term of 5/3 × series: 5/6 is 5/3 × 1/2."]},
    "q-sm-root-trick": {
        "cue": "A big number squared minus consecutive numbers, with a square root asked.",
        "formulas": ["sm-f8"], "tech": ["identity"],
        "standard": "Let a be the big number and rewrite every other number in terms of a.",
        "fast": "a² − a − (a − 1) = a² − 2a + 1 = (a − 1)².",
        "eliminate": "√N must be just below the big number, so options near it are the only ones possible.",
        "traps": ["Computing 98765² directly.", "Taking √N = a instead of a − 1."]},
    "q-sy-square": {
        "cue": "'By which smallest number should … be multiplied (divided) to make a perfect square (cube)?' or 'least number to be added / subtracted'.",
        "formulas": ["sy-f1", "sy-f2"], "tech": ["divisibility", "bounds"],
        "standard": "Prime factorise: 5808 = 2⁴ × 3 × 11². The 3 is unpaired, so multiply by 3. For add/subtract, locate the nearest square: 252² = 63504, so subtract 18.",
        "fast": "Square: the last digit of the target and a quick range check: 250² = 62500, 260² = 67600, the root is 252.",
        "eliminate": "Multiplier must be a product of the unpaired primes: options with a factor not in the number can go.",
        "traps": ["Adding when the question says subtract.", "Multiplying by the whole repeated factor instead of the missing power.", "Using a perfect square for a cube question (cube needs powers of 3)."]},
    "q-sy-identity": {
        "cue": "Decimals with squares or cubes of two ugly numbers, a ± b hidden in the denominator.",
        "formulas": ["sy-f3", "sy-f4"], "tech": ["identity", "cancel-first"],
        "standard": "Name a and b, match the formula, then read off the answer: (2.644² − 2.356²) ÷ 0.288 = (a − b)(a + b)/(a − b) = a + b = 5.",
        "fast": "The bottom is usually (a − b) or a²... so the answer is the other factor, and the arithmetic is one addition.",
        "eliminate": "Estimate a ± b first; only one option has that size.",
        "traps": ["Expanding the cubes by hand.", "Using a + b when the formula gives a − b.", "Missing that one number is negative in a + b + c = 0."]},
    "q-sy-word": {
        "cue": "'The sum of two numbers is …, the sum of their squares …', or 'how many perfect squares between …'.",
        "formulas": ["sy-f5", "sy-f6"], "tech": ["identity", "bounds"],
        "standard": "Use (x + y)² = x² + y² + 2xy. Sum 22 and sum of squares 404: 2xy = 484 − 404 = 80, so xy = 40.",
        "fast": "Plug the options: the pair 5 and 8 has sum 13 and product 40.",
        "eliminate": "Use the last digit: a perfect square never ends in 2, 3, 7 or 8.",
        "traps": ["Taking (x + y)² as x² + y².", "Counting squares inclusively when the range is 'between'.", "Counting digits of the root as the digits of the number."]},
    "q-sy-compare": {
        "cue": "'Which is the greatest' with differences like √19 − √17, or two sums of roots to compare.",
        "formulas": ["sy-f7", "sy-f1"], "tech": ["identity", "estimate"],
        "standard": "√a − √b = (a − b)/(√a + √b): when the gaps are equal, the smallest numbers give the greatest value.",
        "fast": "Estimate each to two decimals and compare.",
        "eliminate": "Square both sides when both are positive: 8 + 2√15 against 8 + 2√12.",
        "traps": ["Assuming √a + √b = √(a + b).", "Squaring when a side is negative."]}
}
_ord = lambda t: sorted(map(F, t.split(", "))) == list(map(F, t.split(", ")))
OPT57 = ["3/5, 4/7, 5/9, 7/11", "5/9, 4/7, 3/5, 7/11", "3/5, 5/9, 4/7, 7/11", "4/7, 5/9, 7/11, 3/5"]
_inner = F(2, 5) - F(1, 3) * (F(5, 6) - F(1, 6))
PYQS = [
    pyq(S1, 57, "q-sm-order", "Arrange the fractions 7/11, 5/9, 4/7 and 3/5 in ascending order.", OPT57, "b",
        ["Decimals: 5/9 = 0.556, 4/7 = 0.571, 3/5 = 0.600, 7/11 = 0.636.", "Ascending: 5/9, 4/7, 3/5, 7/11."],
        lambda: 1, 1, 0, tech=["fraction-percent", "estimate"], optvals=[1 if _ord(t) else 0 for t in OPT57],
        trick="3/5 is 0.6: bigger than 5/9 and 4/7, smaller than 7/11. So 3/5 sits third, which only option (b) does.",
        wrong={"a": bound("3/5 = 0.6 is larger than 4/7 and 5/9, so it cannot come first.", lambda v: v == 0), "c": bound("3/5 = 0.6 is larger than 5/9 and 4/7, so it cannot come first.", lambda v: v == 0),
               "d": bound("5/9 = 0.556 is smaller than 4/7 = 0.571, so 4/7 cannot come first; and 3/5 = 0.6 is smaller than 7/11, so it cannot come last.", lambda v: v == 0)}),
    pyq(S1, 58, "q-sm-bodmas", "Evaluate: 8⅓ − [7/9 ÷ {2/5 − (1/3 × (5/6 − 1/6))}].", ["-41/15", "45/23", "95/24", "32/3"], "c",
        ["Innermost bracket: 5/6 − 1/6 = 2/3. Then 1/3 × 2/3 = 2/9.", "2/5 − 2/9 = (18 − 10)/45 = 8/45.", "7/9 ÷ 8/45 = 7/9 × 45/8 = 35/8.", "8⅓ = 25/3, so 25/3 − 35/8 = (200 − 105)/24 = 95/24."],
        lambda: float(F(25, 3) - F(7, 9) / _inner), 95 / 24, 1e-9, tech=["estimate", "cancel-first"], concepts=1, heavy=True,
        trick="Estimate: 8.33 − 0.78 ÷ 0.18 ≈ 8.33 − 4.4 ≈ 3.9. Only 95/24 (3.96) is close.",
        wrong={"a": bound("The result is about 3.96, positive. −41/15 is negative.", lambda v: v < 0), "b": bound("45/23 ≈ 1.96, but the expression is about 3.96.", lambda v: abs(v - 3.958) > 0.5),
               "d": bound("32/3 ≈ 10.7 is bigger than 8⅓, but the expression subtracts something from 8⅓.", lambda v: v > 8.34)}),
    pyq(S1, 75, "q-sm-bodmas", "Simplify: (3 + 2.8) − 1.5.", ["3.2", "4.3", "5.4", "6.2"], "b",
        ["Bracket first: 3 + 2.8 = 5.8.", "5.8 − 1.5 = 4.3."],
        lambda: (3 + 2.8) - 1.5, 4.3, 1e-9, tech=["estimate"], trick="About 6 − 1.5 = 4.5, so 4.3 is the only option near it."),
    pyq(S2, 56, "q-sm-continued", "Evaluate the continued fraction x = 3 + 1/(2 + 1/(5 + 1/3)).", ["121/35", "47/16", "61/20", "59/19"], "a",
        ["Bottom: 5 + 1/3 = 16/3, so 1/(16/3) = 3/16.", "2 + 3/16 = 35/16, so 1/(35/16) = 16/35.", "x = 3 + 16/35 = 121/35."],
        lambda: float(3 + 1 / (2 + 1 / (5 + F(1, 3)))), 121 / 35, 1e-9, tech=["estimate"], concepts=1,
        trick="x is a bit over 3 (3 + about 0.46). 121/35 = 3.457; 47/16 = 2.94 and 59/19 = 3.1 are far off."),
    pyq(K1, 21, "q-sm-root-trick", 'If N = (98765)^2 − 98765 − 98764, what is the value of √N?', ['98764', '98762', '98761', '98760'], "a",
        ['With a = 98765: N = a² − a − (a − 1) = a² − 2a + 1 = (a − 1)².', '√N = a − 1 = 98764.'],
        lambda: 98765 - 1, 98764, 0, tech=['identity'], trick='Rewrite 98764 as 98765 − 1: the expression is (98765 − 1)².'),
    pyq(K1, 22, "q-sm-decimal", 'Find the value of 0.05/0.8 + 0.005/0.08 + 0.0005/0.008 + 0.00005/0.0008 + 0.000005/0.00008.', ['0.1250', '0.1875', '0.25', '0.3125'], "d",
        ['Each fraction equals 0.05 ÷ 0.8 = 1/16 = 0.0625 (numerator and denominator shrink by ten each time).', 'Five equal terms: 5 × 0.0625 = 0.3125.'],
        lambda: 5 * 0.05 / 0.8, 0.3125, 1e-09, tech=['cancel-first'], trick='Every term is the same 0.05 ÷ 0.8 = 1/16; multiply by 5.'),
    pyq(K1, 29, "q-sm-decimal", 'What is the value of (0.72 × 4.2) ÷ (2.8 × 0.6) − (0.75 × 1.92) ÷ (1.2 × 1.5)?', ['1', '1.2', '1.4', '1.5'], "a",
        ['First part: 3.024 ÷ 1.68 = 1.8. Second part: 1.44 ÷ 1.8 = 0.8.', '1.8 − 0.8 = 1.'],
        lambda: 0.72 * 4.2 / (2.8 * 0.6) - 0.75 * 1.92 / (1.2 * 1.5), 1.0, 1e-09, tech=['cancel-first'], trick='Cancel before multiplying: 0.72 ÷ 0.6 = 1.2 and 4.2 ÷ 2.8 = 1.5 gives 1.8.'),
    pyq(K1, 40, "q-sm-roots", 'Which statement(s) is/are true?  I. √0.49 + √0.0049 + √0.0121 + √0.0036 = 0.84   II. √59.29 + √10.89 + √1.44 = 11.2', ['Only I', 'Only II', 'Both I and II', 'Neither I nor II'], "d",
        ['I: 0.7 + 0.07 + 0.11 + 0.06 = 0.94, not 0.84.', 'II: 7.7 + 3.3 + 1.2 = 12.2, not 11.2.', 'Both are false.'],
        lambda: int(abs(sum(math.sqrt(x) for x in (0.49, 0.0049, 0.0121, 0.0036)) - 0.84) > 1e-9 and abs(sum(math.sqrt(x) for x in (59.29, 10.89, 1.44)) - 11.2) > 1e-9), 1, 0, tech=['estimate'], optvals=[0, 0, 0, 1], trick='Take each root separately (0.7, 0.07, 0.11, 0.06; 7.7, 3.3, 1.2) and add.'),
    pyq(K1, 41, "q-sm-harmonic", 'If 1 + 1/2 + 1/3 + 1/4 + … + 1/25 = k, what is the value of 5/6 + 5/9 + 5/12 + … + 1/15?', ['(k − 1)/3', '5k/3', '5(k − 1)/3', '5(k − 1)'], "c",
        ['The terms are 5/(3 × 2), 5/(3 × 3), 5/(3 × 4), …, 5/(3 × 25) = 1/15.', 'Sum = (5/3) × (1/2 + 1/3 + … + 1/25) = (5/3)(k − 1).'],
        lambda: sum(5 / (3 * j) for j in range(2, 26)), 4.693263629589178, 1e-09, tech=['identity'], optvals=[(KH - 1) / 3, 5 * KH / 3, 5 * (KH - 1) / 3, 5 * (KH - 1)], trick='Pull out 5/3: what is left is the given sum without its first term 1.', concepts=2),
    pyq(K1, 48, "q-sm-continued", 'If 1 / (1 + 1 / (1 + 1 / (1 + 1 / (1 + 1/x)))) = 23/38, what is the value of x?', ['9', '7', '5', '2'], "b",
        ['Work from the outside in. 1/(1 + s) = 23/38 gives s = 38/23 − 1 = 15/23. Flip and subtract 1 each time: 23/15 − 1 = 8/15; 15/8 − 1 = 7/8; 8/7 − 1 = 1/7.', 'So 1/x = 1/7 and x = 7.'],
        lambda: (lambda s: 1 / [s := 1 / s - 1 for _ in range(3)][-1])(1 / F(23, 38) - 1), 7, 1e-09, tech=['cancel-first'], trick='Peel layers from the outside: flip, subtract 1, repeat; 1/x = 1/7.', concepts=2),
]

PYQS = PYQS + PYQS_RY


def practice_items():
    return []
