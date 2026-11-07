"""Algebraic identities: quiz tier (past questions with checked answers, solutions and a short method per type)."""
import math, re
from bank import bound, mistake, pyq
from topics._ch16a_ry import PYQS_RY as PYQS_C16A

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
    "q-ai-recip-power": {"short": "Rational expression in x", "label": "A bigger expression in x, rewritten using x + 1/x", "kind": "qtype", "parent": "c-ai-reciprocal", "order": 2,
                         "summary": "A degree-4 (or higher) rational expression in x; divide through by the right power of x to land back on x + 1/x.", "links": []},
    "c-ai-operator": {"short": "Custom operators", "label": "A symbol defined by its own rule", "kind": "concept", "parent": TOPIC, "order": 3,
                      "summary": "*, ⊕, ⊗ and similar symbols are defined by a stated rule; substitute the two numbers exactly as given, in order.", "links": []},
    "q-ai-operator": {"short": "Evaluate a * b", "label": "Evaluate a custom operator", "kind": "qtype", "parent": "c-ai-operator", "order": 1,
                      "summary": "A rule like a * b = 2a − 3b + ab is given; evaluate it for stated numbers, in the order the rule names them.", "links": []},
    "c-ai-zerosq": {"short": "Sum of squares = 0", "label": "A sum of squares equal to zero", "kind": "concept", "parent": TOPIC, "order": 4,
                    "summary": "Complete the square on each variable; a sum of real squares is zero only when every square is, which pins down each variable.", "links": []},
    "q-ai-zerosq": {"short": "Complete the square", "label": "Pin down variables from a sum-of-squares equation", "kind": "qtype", "parent": "c-ai-zerosq", "order": 1,
                    "summary": "One equation mixes squares and linear terms; rewrite it as a sum of squares equal to 0 to find every variable at once.", "links": []},
    "c-ai-symmetric": {"short": "a + b + c = 0", "label": "a + b + c = 0 and symmetric functions", "kind": "concept", "parent": TOPIC, "order": 5,
                       "summary": "When a + b + c = 0, a³+b³+c³ = 3abc and a²+b²+c² = −2(ab+bc+ca); more generally a³+b³+c³−3abc = (a+b+c)(a²+b²+c²−ab−bc−ca).", "links": ["ratio-proportion"]},
    "q-ai-symmetric": {"short": "a + b + c = 0 corollary", "label": "An expression that collapses to a constant when a + b + c = 0", "kind": "qtype", "parent": "c-ai-symmetric", "order": 1,
                       "summary": "a + b + c = 0 (or three quantities built to sum to 0) is given; the asked expression is always the same number, whatever a, b, c are.", "links": []},
    "q-ai-symfunc": {"short": "Symmetric functions", "label": "Build a³+b³+c³ from the sum and the pair-sum", "kind": "qtype", "parent": "c-ai-symmetric", "order": 2,
                     "summary": "a+b+c, ab+bc+ca (or a²+b²+c²) and sometimes abc are given directly; combine the identities to reach a³+b³+c³ or similar.", "links": []},
    "c-ai-polynomial": {"short": "Factor & remainder theorem", "label": "Polynomials: factors, remainders and roots", "kind": "concept", "parent": TOPIC, "order": 6,
                        "summary": "p(k) = 0 exactly when (x − k) is a factor of p(x); otherwise p(k) is the remainder on dividing by (x − k).", "links": []},
    "q-ai-polynomial": {"short": "Remainder theorem", "label": "Use p(k) to find an unknown coefficient or a root sum", "kind": "qtype", "parent": "c-ai-polynomial", "order": 1,
                        "summary": "Two polynomials share a factor or a remainder at the same x = k, or roots of a quadratic are named inside the quadratic itself.", "links": []},
    "c-ai-minmax": {"short": "Maximum / minimum value", "label": "Extreme value of an expression under one constraint", "kind": "concept", "parent": TOPIC, "order": 7,
                    "summary": "For a fixed sum, a sum of squares is smallest when every part is equal; a factored inequality can have an exact boundary value as its extreme.", "links": []},
    "q-ai-minmax": {"short": "Extreme value", "label": "Find the greatest or least value an expression can take", "kind": "qtype", "parent": "c-ai-minmax", "order": 1,
                    "summary": "'Minimum value of a²+b²+c²' given a+b+c, or the smallest x satisfying a factored cubic inequality.", "links": []},
}
FORMULAS = [
    {"id": "ai-f1", "node": "c-ai-cubes", "text": "Last digit of a cube: digits 0 to 9 give 0, 1, 8, 7, 4, 5, 6, 3, 2, 9", "note": "Only 2↔8 and 3↔7 swap; the rest repeat. Use it to kill options in seconds."},
    {"id": "ai-f2", "node": "c-ai-cubes", "text": "a³ + b³ = (a + b)(a² − ab + b²)     a³ − b³ = (a − b)(a² + ab + b²)", "note": "Use when the numbers are related (a + b is round)."},
    {"id": "ai-f3", "node": "c-ai-cubes", "text": "If a + b + c = 0 then a³ + b³ + c³ = 3abc", "note": "Check this first: it turns three big cubes into one product."},
    {"id": "ai-f4", "node": "c-ai-reciprocal", "text": "x + 1/x = (x² + 1) ÷ x", "note": "When x² is a whole number (x = √11) the top is a whole number at once."},
    {"id": "ai-f5", "node": "c-ai-reciprocal", "text": "x² + 1/x² = (x + 1/x)² − 2     x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x)"},
    {"id": "ai-f6", "node": "c-ai-operator", "text": "A custom symbol is just its rule.", "note": "Substitute the two numbers exactly as the rule names them, in order — these symbols are rarely symmetric."},
    {"id": "ai-f7", "node": "c-ai-reciprocal", "text": "Divide a rational expression in x by the right power of x (usually x² or x³) to turn every term into x, 1/x or a power of (x + 1/x).", "note": "Works on both the top and the bottom of a fraction at once."},
    {"id": "ai-f8", "node": "c-ai-zerosq", "text": "For real numbers, p² + q² + r² = 0 only when p = q = r = 0.", "note": "Complete the square on each variable first to reach this shape."},
    {"id": "ai-f9", "node": "c-ai-symmetric", "text": "If a + b + c = 0 then a³ + b³ + c³ = 3abc and a² + b² + c² = −2(ab + bc + ca).", "note": "Also true with any three quantities built so that they add to 0, not just a, b, c themselves."},
    {"id": "ai-f10", "node": "c-ai-symmetric", "text": "a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca), with ab + bc + ca = [(a+b+c)² − (a²+b²+c²)] / 2", "note": "Build a²+b²+c² (or ab+bc+ca) from the other two sums first; do not expand a³+b³+c³ directly."},
    {"id": "ai-f11", "node": "c-ai-polynomial", "text": "Remainder theorem: dividing p(x) by (x − k) leaves remainder p(k). (x − k) is a factor of p(x) exactly when p(k) = 0.", "note": "For a quadratic x² + σx + β = 0, sum of roots = −σ and product of roots = β."},
    {"id": "ai-f12", "node": "c-ai-minmax", "text": "For a fixed sum a + b + c = S, a² + b² + c² is smallest when a = b = c = S/3, giving minimum S²/3.", "note": "Any unequal split makes the sum of squares larger."},
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
    "q-ai-recip-power": {
        "cue": "A fraction of degree-4 (or higher) polynomials in x, with x + 1/x (or x² + 1/x²) given.",
        "formulas": ["ai-f5", "ai-f7"], "tech": ["identity"],
        "standard": "Divide every term of the top and the bottom by the matching power of x, so each piece becomes a power of x plus the matching power of 1/x, then use x + 1/x and x² + 1/x².",
        "fast": "Spot the power to divide by from the highest power in the expression (x⁴ terms → divide by x²; x⁶ terms → divide by x³).",
        "eliminate": "Estimate x numerically from x + 1/x = k (the positive root of x² − kx + 1 = 0) and evaluate the original expression directly to check an option.",
        "traps": ["Dividing the top and bottom by different powers of x.", "Forgetting the −2 (or −3k) correction when converting x²+1/x² (or x³+1/x³).", "Losing track of a cyclic power pattern (x⁶ = −1, say) and trying to compute a huge power directly."]},
    "q-ai-operator": {
        "cue": "A symbol such as *, ⊕, ⊗ or ☉ is defined by a stated rule, then asked for at specific numbers.",
        "formulas": ["ai-f6"], "tech": ["plug-numbers"],
        "standard": "Substitute the two given numbers into the rule exactly as it names them (first number plays the first role, second the second), then simplify.",
        "fast": "There is no shortcut beyond careful substitution — these are arithmetic, not algebra, once the rule is read correctly.",
        "eliminate": "Redo the substitution a second time, swapping nothing, to catch an order slip before picking an option.",
        "traps": ["Swapping the two numbers' roles in an asymmetric rule.", "Mixing up the order of operations inside the rule.", "Applying the rule to the result of a previous custom operation instead of the original numbers, when the question asks for two separate evaluations added together."]},
    "q-ai-zerosq": {
        "cue": "One equation mixes squared terms with linear terms (no second equation given) and asks for the variables, or a combination of them.",
        "formulas": ["ai-f8"], "tech": ["identity", "sign-check"],
        "standard": "Move everything to one side, group each variable's square and linear terms, and complete the square on each to reach p² + q² + r² = 0.",
        "fast": "Since each square must be 0 individually, read off every variable's value directly from the completed squares.",
        "eliminate": "Check the completed form adds back up to the original equation before trusting the variable values.",
        "traps": ["Forgetting the constant left over after completing the square (it must also come out to 0).", "Stopping after finding one variable instead of all of them.", "Sign errors when completing the square on a negative linear term."]},
    "q-ai-symmetric": {
        "cue": "'a + b + c = 0' (or three quantities visibly built to sum to 0) is given, and the expression asked for looks like it should depend on the actual values but doesn't.",
        "formulas": ["ai-f9"], "tech": ["identity", "plug-numbers"],
        "standard": "Use a³+b³+c³ = 3abc and a²+b²+c² = −2(ab+bc+ca) to rewrite the expression; it collapses to a plain number.",
        "fast": "Plug in one simple set of numbers that satisfies a + b + c = 0 (e.g. 1, 1, −2) and evaluate the expression directly — the answer is the same for every valid choice.",
        "eliminate": "Try a second, different set of numbers summing to 0; if the expression gives the same value both times, that confirms the option.",
        "traps": ["Assuming the expression depends on the actual numbers and trying to solve for them.", "A sign slip in a² + b² + c² = −2(ab+bc+ca) (it is negative of the pair-sum, not equal to it).", "Forgetting that a + b + c = 0 can come disguised as three built quantities, not just a, b, c themselves."]},
    "q-ai-symfunc": {
        "cue": "a+b+c, ab+bc+ca (or a²+b²+c²) and sometimes abc are given as plain numbers (not necessarily summing to 0); a³+b³+c³ or a similar symmetric expression is asked for.",
        "formulas": ["ai-f10"], "tech": ["identity"],
        "standard": "Build a²+b²+c² from (a+b+c)² − 2(ab+bc+ca) if it isn't given directly, then use a³+b³+c³ − 3abc = (a+b+c)(a²+b²+c² − ab−bc−ca).",
        "fast": "Compute the three building blocks (sum, pair-sum, triple-product) once, then plug straight into the identity — no need to find a, b, c individually.",
        "eliminate": "Sanity-check the size: a³+b³+c³ should be roughly the cube of the typical size of a, b, c.",
        "traps": ["Using a²+b²+c² where ab+bc+ca was meant, or vice versa.", "Forgetting to add 3abc back after using the identity (it gives a³+b³+c³ − 3abc, not a³+b³+c³ itself).", "Assuming a+b+c = 0 when it is not (then the shortcut in q-ai-symmetric does not apply)."]},
    "q-ai-polynomial": {
        "cue": "Two polynomials share a factor or leave the same remainder at one value of x, or a quadratic's roots are named inside its own coefficients.",
        "formulas": ["ai-f11"], "tech": ["back-substitute", "identity"],
        "standard": "Put x = k (the shared root, or the divisor's root) into each polynomial and set the results equal, or equal to 0 for a factor; for named roots, write sum and product of roots from the coefficients and solve those two equations.",
        "fast": "A factor (x − k) always means 'put x = k and set to 0' — there is rarely a need to do the actual division.",
        "eliminate": "Check the found value by substituting back into the original condition (the shared remainder, or the quadratic itself).",
        "traps": ["Using x = −k instead of x = k for the factor (x − k).", "Mixing up sum of roots (−coefficient of x) and product of roots (constant term) for a non-monic quadratic.", "Stopping at one equation when two unknowns need two."]},
    "q-ai-minmax": {
        "cue": "'Minimum value of a²+b²+c²' with a fixed sum, or 'minimum/maximum x satisfying' a factored polynomial inequality.",
        "formulas": ["ai-f12"], "tech": ["bounds", "plug-numbers"],
        "standard": "For a fixed sum, split equally to minimise a sum of squares (S²/3). For an inequality, factor the polynomial fully and read off where each factor's sign allows the product to meet the inequality.",
        "fast": "A repeated factor like (x − k)² is never negative, so it alone can make the whole product meet a '≥ 0' at x = k, regardless of the other factor.",
        "eliminate": "Test the boundary values directly in the original inequality or expression to confirm which one is extremal.",
        "traps": ["Assuming the minimum of a sum of squares happens at the smallest listed option rather than at the equal split.", "Missing the extra solution a repeated factor contributes to an inequality.", "Confusing 'minimum value of the expression' with 'minimum value of x'."]},
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

PYQS = PYQS + PYQS_C16A


def practice_items():
    return []
