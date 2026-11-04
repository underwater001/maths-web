"""Algebraic identities: quiz tier (past questions with checked answers, solutions and a short method per type)."""
import math, re
from bank import bound, mistake, pyq

TOPIC = "algebraic-identities"
PREFIX = "ai"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-ai-cubes": {"short": "Cubes", "label": "Cubes of big numbers", "kind": "concept", "parent": TOPIC, "order": 1,
                   "summary": "Add and subtract cubes of two-digit numbers without a calculator: last digit first, then a rough size.", "links": []},
    "c-ai-reciprocal": {"short": "x + 1/x", "label": "x + 1/x and its powers", "kind": "concept", "parent": TOPIC, "order": 2,
                        "summary": "One value of x + 1/x unlocks x² + 1/x² and x³ + 1/x³ through two small identities.", "links": ["surds-indices"]},
    "q-ai-cubes": {"short": "Big cubes", "label": "Sum and difference of big cubes", "kind": "qtype", "parent": "c-ai-cubes", "order": 1,
                   "summary": "Cubes of numbers like 32, 19 and 38 added, subtracted and adjusted.", "links": []},
    "q-ai-reciprocal": {"short": "x + 1/x", "label": "Value of x + 1/x", "kind": "qtype", "parent": "c-ai-reciprocal", "order": 1,
                        "summary": "x is given (often a surd); find x + 1/x or a power of it.", "links": []},
}
FORMULAS = [
    {"id": "ai-f1", "node": "c-ai-cubes", "text": "Last digit of a cube: digits 0 to 9 give 0, 1, 8, 7, 4, 5, 6, 3, 2, 9", "note": "Only 2↔8 and 3↔7 swap; the rest repeat. Use it to kill options in seconds."},
    {"id": "ai-f2", "node": "c-ai-cubes", "text": "a³ + b³ = (a + b)(a² − ab + b²)     a³ − b³ = (a − b)(a² + ab + b²)", "note": "Use when the numbers are related (a + b is round)."},
    {"id": "ai-f3", "node": "c-ai-cubes", "text": "If a + b + c = 0 then a³ + b³ + c³ = 3abc", "note": "Check this first: it turns three big cubes into one product."},
    {"id": "ai-f4", "node": "c-ai-reciprocal", "text": "x + 1/x = (x² + 1) ÷ x", "note": "When x² is a whole number (x = √11) the top is a whole number at once."},
    {"id": "ai-f5", "node": "c-ai-reciprocal", "text": "x² + 1/x² = (x + 1/x)² − 2     x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x)"},
]
METHODS = {
    "q-ai-cubes": {
        "cue": "Cubes of two-digit numbers joined by plus and minus, maybe with a small number added at the end.",
        "formulas": ["ai-f1", "ai-f2", "ai-f3"], "tech": ["unit-digit", "estimate", "identity"],
        "standard": "Cube each number (square it, then multiply), add and subtract in order, then add the small number.",
        "fast": "Find the last digit of the answer from the last digits of the cubes (2→8, 9→9, 8→2 here). Then rough-size each cube to settle the sign and the magnitude.",
        "eliminate": "Work out the last digit of the true answer and strike every option that ends differently. In the PYQ here three of the four options end in 0.",
        "traps": ["Squaring instead of cubing.", "A sign slip when subtracting the biggest cube: the answer is negative.", "Forgetting the small number at the end (+312)."],
        "variations": ["Three cubes with a + b + c = 0, so the sum is 3abc.", "(a³ + b³) ÷ (a² − ab + b²), which is just a + b."]},
    "q-ai-reciprocal": {
        "cue": "x is a surd or a simple number and the question asks for x + 1/x (or x² + 1/x²).",
        "formulas": ["ai-f4", "ai-f5"], "tech": ["identity", "estimate"],
        "standard": "Write 1/x, rationalise it, add to x. Or use (x² + 1) ÷ x.",
        "fast": "If x = √n then x² = n, so x + 1/x = (n + 1)/√n. Multiply top and bottom by √n to get (n + 1)√n / n.",
        "eliminate": "Estimate x + 1/x (3.32 + 0.30 ≈ 3.62 for x = √11) and test each option numerically.",
        "traps": ["Inverting the fraction: (n + 1)/√n becomes √n/(n + 1).", "Using x² + 2 instead of x² + 1 on top.", "Forgetting to rationalise and picking an option with a different form."]},
}


def _surd(t):
    m = re.fullmatch(r"(\d+)√(\d+)/(\d+)", t); return int(m[1]) * math.sqrt(int(m[2])) / int(m[3])


r11 = math.sqrt(11)

PYQS = [
    pyq(S1, 59, "q-ai-cubes", "Find the value of 32³ + 19³ − 38³ + 312.", ["-38520", "-26840", "-14933", "-52100"], "c",
        ["32³ = 32,768, 19³ = 6,859 and 38³ = 54,872.", "32,768 + 6,859 = 39,627, and 39,627 − 54,872 = −15,245.", "Add 312: −15,245 + 312 = −14,933."],
        lambda: 32 ** 3 + 19 ** 3 - 38 ** 3 + 312, -14933, 0, tech=["unit-digit", "estimate"], concepts=1, heavy=True,
        trick="Last digits: 2³ ends in 8, 9³ in 9, 8³ in 2, so the answer ends in 8 + 9 − 2 + 2 = 17 → 7. Only −14933 ends in 7 (−14933 = −14940 + 7); the other three all end in 0.",
        wrong={k: bound(f"The true value ends in 7 (last digits 8 + 9 − 2 + 2 = 17), but {o} ends in 0.", lambda v: v % 10 != 7) for k, o in (("a", "-38520"), ("b", "-26840"), ("d", "-52100"))}),
    pyq(S2, 66, "q-ai-reciprocal", "If x = √11, find the value of x + 1/x.", ["12√11/11", "11√11/12", "13√11/11", "14√11/11"], "a",
        ["x² = 11, so 1/x = 1/√11 = √11/11.", "x + 1/x = √11 + √11/11 = (11√11 + √11)/11 = 12√11/11."],
        lambda: r11 + 1 / r11, 12 * r11 / 11, 1e-9, tech=["identity", "estimate"], concepts=1,
        trick="(x² + 1)/x = 12/√11: the 12 is 11 + 1. Only option (a) has 12 on top and 11 underneath.",
        optvals=[_surd(t) for t in ("12√11/11", "11√11/12", "13√11/11", "14√11/11")],
        wrong={"b": mistake("Inverted the fraction: 11√11/12 ≈ 3.04 instead of 12√11/11 ≈ 3.62.", 11 * r11 / 12),
               "c": bound("Estimate: 3.317 + 0.302 ≈ 3.62, but 13√11/11 ≈ 3.92.", lambda v: abs(v - 3.619) > 0.2),
               "d": bound("Estimate: 3.317 + 0.302 ≈ 3.62, but 14√11/11 ≈ 4.22.", lambda v: abs(v - 3.619) > 0.2)}),
]


def practice_items():
    return []
