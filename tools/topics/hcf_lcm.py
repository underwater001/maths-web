"""HCF & LCM: quiz tier. Remainder problems solved with the LCM, finding the two numbers
from their HCF/LCM, and word problems that apply the HCF or LCM directly."""
import math
from fractions import Fraction as F
from bank import bound, mistake, pyq
from topics._ch19lh_ry import PYQS_RY as PYQS_C19LH
from topics._ch19lh2_ry import PYQS_RY as PYQS_C19LH2

TOPIC = "hcf-lcm"
PREFIX = "hl"
TIER = "quiz"
K1 = "kiran-ch01-t01"

NODES = {
    "c-hl-rem": {"short": "LCM and remainders", "label": "Remainder problems: the LCM sets the period", "kind": "concept", "parent": TOPIC, "order": 1,
                 "summary": "Numbers that leave the same pattern of remainders repeat every LCM of the divisors, so find one such number and add multiples of the LCM.", "links": ["number-system"]},
    "q-hl-lcm-offset": {"short": "Same gap, add or subtract", "label": "Divisor minus remainder is the same every time", "kind": "qtype", "parent": "c-hl-rem", "order": 1,
                        "summary": "Each remainder is the same amount short of (or over) its divisor, so N = LCM × k ∓ that amount.", "links": []},
    "q-hl-two-rem": {"short": "Different remainders", "label": "Different remainders for different divisors", "kind": "qtype", "parent": "c-hl-rem", "order": 2,
                     "summary": "Find the first number that fits both remainders, then step by the LCM; count or find the largest.", "links": []},
    "q-hl-common-rem": {"short": "Same remainder every time", "label": "Every divisor leaves the same remainder", "kind": "qtype", "parent": "c-hl-rem", "order": 3,
                        "summary": "N = LCM × k + r (the common remainder); pick k for the size asked (least, or greatest under a digit limit).", "links": []},
    "q-hl-remainder-extra": {"short": "Remainder pattern plus one more filter", "label": "Common remainder (or gap), with an extra multiple condition", "kind": "qtype", "parent": "c-hl-rem", "order": 4,
                             "summary": "Build the usual remainder form from the LCM first, then filter k so the result also divides evenly by one more given number.", "links": []},

    "c-hl-find-numbers": {"short": "Finding the numbers themselves", "label": "Recovering the two numbers from their HCF and LCM", "kind": "concept", "parent": TOPIC, "order": 2,
                          "summary": "HCF × LCM always equals the product of the two numbers; writing them as HCF × (a coprime pair) turns most of these into a short search.", "links": []},
    "q-hl-hcf-lcm-relation": {"short": "HCF × LCM = product", "label": "Use HCF × LCM = product of the numbers", "kind": "qtype", "parent": "c-hl-find-numbers", "order": 1,
                              "summary": "Given three of {number 1, number 2, HCF, LCM}, the fourth is a single division away.", "links": []},
    "q-hl-sum-diff": {"short": "Coprime pair under a condition", "label": "Write the numbers as HCF × (coprime pair)", "kind": "qtype", "parent": "c-hl-find-numbers", "order": 2,
                      "summary": "The numbers are HCF × a and HCF × b with a, b coprime and ab = LCM ÷ HCF; try the coprime factor pairs of that ratio until one matches the extra condition (sum, difference, product, or a range).", "links": []},
    "q-hl-ratio-numbers": {"short": "Numbers given by a ratio", "label": "Numbers already given in a ratio", "kind": "qtype", "parent": "c-hl-find-numbers", "order": 3,
                           "summary": "For numbers in ratio a : b, LCM = HCF × a × b (when a, b are coprime); solve for whichever piece is missing.", "links": []},
    "q-hl-count-pairs": {"short": "How many such pairs exist", "label": "Counting the number-pairs with a given HCF and sum/product", "kind": "qtype", "parent": "c-hl-find-numbers", "order": 4,
                        "summary": "Write the numbers as HCF × a, HCF × b with a, b coprime; the extra condition pins down a + b or a × b, and the answer is how many coprime pairs satisfy it.", "links": []},
    "q-hl-ratio-sum": {"short": "HCF + LCM given as a sum", "label": "The HCF and LCM are linked by a sum and a multiple", "kind": "qtype", "parent": "c-hl-find-numbers", "order": 5,
                      "summary": "HCF + LCM = S and LCM = k × HCF together pin down the HCF by a single division, before the usual other-number step.", "links": []},

    "c-hl-apply": {"short": "Applying HCF and LCM", "label": "Word problems that use the HCF or LCM directly", "kind": "concept", "parent": TOPIC, "order": 3,
                   "summary": "HCF is the largest exact unit that measures several quantities or divides several numbers; LCM is when several repeating things next coincide.", "links": []},
    "q-hl-hcf-container": {"short": "Largest exact measuring unit", "label": "Biggest container, tile or group size that fits exactly", "kind": "qtype", "parent": "c-hl-apply", "order": 1,
                           "summary": "The largest size that measures or paves several quantities exactly is their HCF.", "links": []},
    "q-hl-hcf-remainder-diff": {"short": "HCF with remainders", "label": "Greatest divisor leaving given (or equal) remainders", "kind": "qtype", "parent": "c-hl-apply", "order": 2,
                                "summary": "Equal grouping is a plain HCF; a stated remainder is subtracted first; an unknown but equal remainder means taking the HCF of the pairwise differences instead.", "links": []},
    "q-hl-bells": {"short": "When do they next coincide", "label": "Several things repeating on different periods", "kind": "qtype", "parent": "c-hl-apply", "order": 3,
                  "summary": "Bells, lights, or runners that repeat on different periods next coincide after the LCM of those periods (LCM of fractions = LCM of numerators ÷ HCF of denominators).", "links": []},
    "q-hl-perfect-square": {"short": "Least perfect square multiple", "label": "Smallest perfect square (or cube) divisible by given numbers", "kind": "qtype", "parent": "c-hl-apply", "order": 4,
                            "summary": "Take the LCM, then multiply by whichever primes still have an odd power in its factorisation, so every power becomes even.", "links": []},
    "q-hl-exact-divide": {"short": "Plain LCM divisibility", "label": "Least number exactly divisible by several numbers", "kind": "qtype", "parent": "c-hl-apply", "order": 5,
                          "summary": "The least number exactly divisible by several numbers is their LCM; some versions scale the number first, or add one more remainder condition on top.", "links": []},
    "q-hl-nearest": {"short": "Nearest multiple of the LCM", "label": "Number nearest to a target, exactly divisible by several numbers", "kind": "qtype", "parent": "c-hl-apply", "order": 6,
                     "summary": "Divide the target by the LCM and round to the nearest whole multiple, checking both neighbours when the target sits close to the midpoint.", "links": []},

    "c-hl-misc": {"short": "HCF/LCM facts", "label": "Quick conceptual checks", "kind": "concept", "parent": TOPIC, "order": 4,
                 "summary": "A short fact about how HCF and LCM relate, used as a trap rather than a calculation.", "links": []},
    "q-hl-never-lcm": {"short": "LCM must be a multiple of the HCF", "label": "Which value can never be the LCM", "kind": "qtype", "parent": "c-hl-misc", "order": 1,
                      "summary": "The LCM of two numbers is always an exact multiple of their HCF; an option that doesn't divide evenly by the HCF can never be the LCM.", "links": []},

    "c-hl-fraction": {"short": "HCF and LCM of fractions", "label": "HCF/LCM of fractions, not whole numbers", "kind": "concept", "parent": TOPIC, "order": 5,
                     "summary": "HCF of fractions pairs HCF with LCM crosswise (HCF of numerators over LCM of denominators); LCM of fractions pairs the opposite way.", "links": []},
    "q-hl-fraction": {"short": "HCF or LCM of fractions", "label": "Find the HCF or LCM of two or three fractions", "kind": "qtype", "parent": "c-hl-fraction", "order": 1,
                     "summary": "HCF of fractions = HCF(numerators) ÷ LCM(denominators); LCM of fractions = LCM(numerators) ÷ HCF(denominators).", "links": []},

    "c-hl-algebra": {"short": "HCF/LCM identities", "label": "Symbolic and conceptual HCF-LCM reasoning", "kind": "concept", "parent": TOPIC, "order": 6,
                    "summary": "HCF × LCM = product holds for algebraic expressions and prime-power forms exactly as it does for plain numbers.", "links": []},
    "q-hl-algebra": {"short": "Algebraic HCF/LCM identity", "label": "HCF/LCM reasoning with expressions or prime powers", "kind": "qtype", "parent": "c-hl-algebra", "order": 1,
                    "summary": "Apply HCF × LCM = product symbolically; for prime-power forms, HCF takes the lower power of each shared prime and LCM the higher power.", "links": []},
}
FORMULAS = [
    {"id": "hl-f1", "node": "c-hl-rem", "text": "If every remainder = divisor − c (or + c) then N = k × LCM − c (or + c).", "note": "Check the gap with each divisor before using it."},
    {"id": "hl-f2", "node": "c-hl-rem", "text": "If the remainders differ: find the smallest N that fits, then all N = smallest + k × LCM.", "note": "Count of terms = (last − first) ÷ LCM + 1."},
    {"id": "hl-f3", "node": "c-hl-rem", "text": "If every divisor leaves the same remainder r: N = k × LCM + r.", "note": "The least case is k = 1 (N = LCM + r)."},
    {"id": "hl-f4", "node": "c-hl-rem", "text": "Build the usual remainder form first, then pick k so the result also satisfies one more divisibility condition.", "note": "Work the extra condition mod the extra divisor."},
    {"id": "hl-f5", "node": "c-hl-find-numbers", "text": "HCF × LCM = (number 1) × (number 2), always.", "note": "True only for exactly two numbers, never for three or more."},
    {"id": "hl-f6", "node": "c-hl-find-numbers", "text": "Numbers = HCF × a, HCF × b with a, b coprime and a × b = LCM ÷ HCF.", "note": "List the coprime factor pairs of LCM ÷ HCF, then pick the pair that fits the extra clue."},
    {"id": "hl-f7", "node": "c-hl-find-numbers", "text": "For numbers in ratio a : b (coprime terms), LCM = HCF × a × b.", "note": "The numbers themselves are HCF × a and HCF × b."},
    {"id": "hl-f8", "node": "c-hl-apply", "text": "Largest exact measuring/paving/grouping unit for several quantities = their HCF.", "note": "Convert to one unit first (e.g. metres to centimetres) before taking the HCF."},
    {"id": "hl-f9", "node": "c-hl-apply", "text": "Greatest number dividing several numbers leaving the SAME given remainder each time: subtract the remainder from each, then take the HCF.", "note": "If the remainder itself is unknown, take the HCF of the pairwise differences instead."},
    {"id": "hl-f10", "node": "c-hl-apply", "text": "Several repeating things next coincide after LCM of their periods; for periods as fractions, LCM = LCM(numerators) ÷ HCF(denominators).", "note": "Convert every period to the same unit first."},
    {"id": "hl-f11", "node": "c-hl-apply", "text": "Least perfect square divisible by N: take LCM/N's prime factorisation and multiply by every prime left with an odd power.", "note": "Same idea for a perfect cube, but fixing powers to multiples of 3."},
    {"id": "hl-f12", "node": "c-hl-misc", "text": "LCM is always an exact multiple of the HCF.", "note": "A quick way to rule out options without computing the real LCM."},
    {"id": "hl-f13", "node": "c-hl-find-numbers", "text": "To count number-pairs with a given HCF and sum/product: write them as HCF × a, HCF × b with a, b coprime, then count the coprime pairs meeting the reduced condition.", "note": "A pair that shares a factor other than 1 doesn't count, even if it meets the sum or product."},
    {"id": "hl-f14", "node": "c-hl-find-numbers", "text": "If HCF + LCM = S and LCM = k × HCF, then HCF = S ÷ (k + 1) and LCM = S − HCF.", "note": "Solve for the HCF and LCM first, then apply HCF × LCM = product as usual."},
    {"id": "hl-f15", "node": "c-hl-apply", "text": "Nearest multiple of the LCM to a target: divide the target by the LCM and round to the nearest whole multiple.", "note": "Compare both neighbouring multiples directly when the target is close to the midpoint."},
    {"id": "hl-f16", "node": "c-hl-fraction", "text": "HCF of fractions = HCF(numerators) ÷ LCM(denominators); LCM of fractions = LCM(numerators) ÷ HCF(denominators).", "note": "The two formulas pair HCF with LCM crosswise — easy to swap by mistake."},
    {"id": "hl-f17", "node": "c-hl-algebra", "text": "HCF × LCM = product of the two quantities holds for algebraic expressions too; in prime-power form, HCF takes the lower shared power of each prime and LCM the higher.", "note": "A prime missing from one side still appears in the LCM but drops out of the HCF entirely."},
]
METHODS = {
    "q-hl-lcm-offset": {
        "cue": "'Least number which when increased by 1 is divisible by …' or 'leaves remainders one less than each divisor'.",
        "formulas": ["hl-f1"], "tech": ["lcm-units"],
        "standard": "Find the LCM of the divisors. The number is LCM × k − c, with k chosen to meet the size condition (least, 4-digit, largest 3-digit).",
        "fast": "Compute the LCM, then pick the right multiple of it with a quick division.",
        "eliminate": "N + c must be divisible by every divisor, so test one option: option + c ÷ divisor.",
        "traps": ["Adding the gap instead of subtracting it.", "Using the product of the divisors instead of the LCM."]},
    "q-hl-two-rem": {
        "cue": "Different remainders for different divisors, then 'largest / how many / remainder with another number'.",
        "formulas": ["hl-f2"], "tech": ["lcm-units", "back-substitute"],
        "standard": "List the numbers 12m + 7 (for example) until one leaves the other remainder. Add multiples of the LCM to reach the size limit.",
        "fast": "List at most as many terms as the smaller divisor, because the pattern then repeats.",
        "eliminate": "A candidate must satisfy both remainders; test the options on both.",
        "traps": ["Counting one too few or too many when the first or last term is at the limit.", "Stepping by the product instead of the LCM when the divisors share factors."]},
    "q-hl-common-rem": {
        "cue": "'Least/greatest number which when divided by … leaves remainder r in each case' with the SAME r every time.",
        "formulas": ["hl-f3"], "tech": ["lcm-units"],
        "standard": "Find the LCM of the divisors, then add the common remainder. For a 'greatest under a digit limit' version, take the largest multiple of the LCM under that limit first.",
        "fast": "Compute the LCM once; the answer is LCM × k + r for whichever k the size condition picks.",
        "eliminate": "Subtract the remainder from each option; the result must divide exactly by every divisor.",
        "traps": ["Reporting the bare LCM and forgetting to add the remainder.", "Using the product of the divisors instead of their LCM."]},
    "q-hl-remainder-extra": {
        "cue": "A remainder/gap pattern (common remainder, or divisor-minus-remainder constant) PLUS one more condition, such as 'and is also a multiple of 13'.",
        "formulas": ["hl-f4"], "tech": ["lcm-units"],
        "standard": "Write the number in its usual LCM-based form with an unknown k, then solve the extra divisibility condition for k using modular arithmetic.",
        "fast": "Reduce the LCM mod the extra divisor first, so the condition on k is a small arithmetic check rather than large numbers.",
        "eliminate": "Check each option against the simple remainder pattern first — most will fail that alone before the extra condition even matters.",
        "traps": ["Stopping at the bare LCM-based form and forgetting the extra multiple condition entirely.", "Solving the modular condition for the wrong sign of the gap."]},
    "q-hl-hcf-lcm-relation": {
        "cue": "'LCM of two numbers is … and HCF is … . If one number is …, the other is' (or any one of the four quantities missing).",
        "formulas": ["hl-f5"], "tech": ["hcf-lcm-product"],
        "standard": "Use HCF × LCM = product of the numbers; divide by whichever one is known to get the other, or divide the product by the HCF to get the LCM.",
        "fast": "One division, directly from the formula — no factor search needed.",
        "eliminate": "Multiply each option by the known number and check it equals HCF × LCM.",
        "traps": ["Giving back one of the known quantities (HCF, LCM, or the given number) instead of computing the missing one.", "Multiplying the two given numbers together instead of HCF and LCM."]},
    "q-hl-sum-diff": {
        "cue": "HCF and LCM given, plus a sum, difference, product, or range — and the actual numbers (or their sum/difference) are asked for.",
        "formulas": ["hl-f6"], "tech": ["hcf-lcm-product"],
        "standard": "Compute LCM ÷ HCF, list its coprime factor pairs, multiply each by the HCF, and keep the pair that satisfies the extra condition.",
        "fast": "Most papers intend the 'obvious' coprime pair (not 1 × n); check that one first.",
        "eliminate": "Test each option pair: both numbers must be multiples of the HCF, and their product must equal HCF × LCM.",
        "traps": ["Using the trivial pair 1 × n instead of searching for the coprime pair the condition actually picks out.", "Reporting the sum when the difference was asked, or vice versa."]},
    "q-hl-ratio-numbers": {
        "cue": "'Two numbers are in the ratio a : b' together with their HCF or LCM (or the LCM's 'other two factors').",
        "formulas": ["hl-f7"], "tech": ["hcf-lcm-product"],
        "standard": "LCM = HCF × a × b for the ratio's coprime terms; solve for whichever piece is missing, then recover the numbers as HCF × a and HCF × b.",
        "fast": "Divide the given LCM by (a × b) to get the HCF directly, or vice versa.",
        "eliminate": "Check the option numbers are in the stated ratio and that their HCF/LCM matches what's given.",
        "traps": ["Treating the ratio terms as the HCF multiplier when they're coprime parts, and vice versa.", "Adding instead of multiplying when recombining the two numbers."]},
    "q-hl-hcf-container": {
        "cue": "Largest container, tile, rope-length, or group size that measures several quantities exactly, with no leftover.",
        "formulas": ["hl-f8"], "tech": ["hcf-units"],
        "standard": "Convert every quantity to the same unit, then take their HCF.", "fast": "Factorise quickly and take the common prime powers.",
        "eliminate": "An option must divide every given quantity exactly; test the largest option first.",
        "traps": ["Forgetting to convert to a common unit before taking the HCF (e.g. mixing metres and centimetres).", "Picking a common factor that isn't the greatest one."]},
    "q-hl-hcf-remainder-diff": {
        "cue": "'Greatest number which divides … leaving remainder(s) …' — either a stated remainder for each number, or the SAME unstated remainder for every number.",
        "formulas": ["hl-f9"], "tech": ["hcf-units"],
        "standard": "If remainders are given, subtract each from its number first and take the HCF of the results. If the remainder is the same but unknown, take the HCF of the pairwise differences instead.",
        "fast": "Factorise the (smaller) differences rather than the original large numbers.",
        "eliminate": "Divide each original number by the option; the remainder must match what's given (or be the same for every number).",
        "traps": ["Taking the HCF of the original numbers instead of subtracting the remainders first.", "Taking the HCF of the numbers instead of their pairwise differences when the remainder is unknown."]},
    "q-hl-bells": {
        "cue": "Bells, lights, buzzers, or runners on a track that start together and are asked when they will next coincide.",
        "formulas": ["hl-f10"], "tech": ["lcm-units"],
        "standard": "Convert every repeat-period to the same unit and take their LCM; for periods given as fractions (such as hours for a runner), use LCM(numerators) ÷ HCF(denominators).",
        "fast": "Spot a common unit quickly (seconds, or a common fraction) before computing.",
        "eliminate": "The answer must be an exact multiple of every individual period.",
        "traps": ["Taking the LCM of the numerators alone without dividing by the HCF of the denominators for fractional periods.", "Mixing units (seconds vs. minutes, or hours vs. a fraction of an hour) before computing the LCM."]},
    "q-hl-perfect-square": {
        "cue": "'Least perfect square number divisible by …' (or least perfect cube).",
        "formulas": ["hl-f11"], "tech": ["lcm-units"],
        "standard": "Find the LCM, factorise it into primes, and multiply by whichever primes have an odd power so every power becomes even.",
        "fast": "Only the primes with an odd exponent need fixing — leave the rest of the LCM alone.",
        "eliminate": "Divide each option by the LCM; the quotient must itself be a perfect square (an integer whose square root is exact).",
        "traps": ["Stopping at the bare LCM without checking whether it's already a perfect square.", "Multiplying by the wrong prime (one that already has an even power)."]},
    "q-hl-never-lcm": {
        "cue": "'The HCF of two numbers is … . Which of the following can never be their LCM?'",
        "formulas": ["hl-f12"], "tech": ["hcf-lcm-product"],
        "standard": "Divide each option by the given HCF; whichever doesn't divide evenly can never be the LCM.",
        "fast": "A quick divisibility check by the HCF, no factorisation needed.",
        "eliminate": "Discard any option that is an exact multiple of the HCF — only the one that isn't is the answer.",
        "traps": ["Checking whether the HCF divides the option the wrong way round.", "Assuming the largest or smallest option must be the odd one out without actually dividing."]},
    "q-hl-exact-divide": {
        "cue": "'Least number exactly divisible by …', sometimes with an extra twist: the number itself is scaled first, or it must leave one more remainder.",
        "formulas": ["hl-f1", "hl-f10"], "tech": ["lcm-units"],
        "standard": "Take the LCM of the given divisors; if the number is scaled (such as 'when doubled'), divide the LCM by that scale factor instead; if there's one more remainder condition, filter k the same way as q-hl-remainder-extra.",
        "fast": "Compute the LCM once and reuse it for every twist on the same question.",
        "eliminate": "The answer (after undoing any scaling) must divide exactly by every divisor listed.",
        "traps": ["Forgetting to divide the LCM by the scale factor when the number itself is scaled before the divisibility condition applies.", "Ignoring the one extra remainder condition and stopping at the bare LCM."]},
    "q-hl-count-pairs": {
        "cue": "'How many pairs of numbers have HCF … and sum/product …?'",
        "formulas": ["hl-f13"], "tech": ["hcf-lcm-product"],
        "standard": "Write the numbers as HCF × a, HCF × b with a, b coprime; the extra condition pins down a + b or a × b. List every pair of positive integers meeting that and keep only the coprime ones.",
        "fast": "For a sum N, list (a, N−a) for a from 1 up to half of N and keep only the coprime pairs; for a product, list its coprime factor pairs directly.",
        "eliminate": "Each candidate pair, multiplied back by the HCF, must give the stated sum/product with exactly the stated HCF — not a smaller common factor.",
        "traps": ["Counting a pair that shares a factor other than 1, so it isn't actually coprime.", "Counting both orderings of the same pair as two different pairs when the question means unordered pairs."]},
    "q-hl-ratio-sum": {
        "cue": "'LCM is k times the HCF' together with 'the sum of the HCF and LCM is S', then one number given, the other asked.",
        "formulas": ["hl-f14"], "tech": ["hcf-lcm-product"],
        "standard": "Solve HCF × (1 + k) = S for the HCF, get the LCM as k × HCF, then use HCF × LCM = product of the numbers as usual.",
        "fast": "The HCF is just S ÷ (k + 1) — one division before the usual other-number step.",
        "eliminate": "Check the candidate HCF and LCM add to S and that one of them divides the given number evenly.",
        "traps": ["Swapping which of HCF/LCM the multiplier k belongs to.", "Using the sum S directly as the LCM without solving for the HCF first."]},
    "q-hl-nearest": {
        "cue": "'The number nearest to N which is exactly divisible by …'",
        "formulas": ["hl-f15"], "tech": ["lcm-units"],
        "standard": "Find the LCM of the given divisors, divide the target by it, and round to the nearest whole multiple — check both neighbouring multiples if the target is near the midpoint.",
        "fast": "Only the remainder of the target on division by the LCM matters: more than half the LCM rounds up, otherwise down.",
        "eliminate": "An option must itself be an exact multiple of the LCM; discard any that fails that alone, then pick whichever is closest.",
        "traps": ["Rounding to the multiple below the target by habit, without checking which neighbour is actually closer.", "Picking a multiple of the LCM that isn't actually the nearest one to the target."]},
    "q-hl-fraction": {
        "cue": "'HCF' or 'LCM' asked of two or three fractions, not whole numbers.",
        "formulas": ["hl-f16"], "tech": ["hcf-units", "lcm-units"],
        "standard": "For HCF: HCF of the numerators over LCM of the denominators. For LCM: LCM of the numerators over HCF of the denominators.",
        "fast": "Only two small HCF/LCM computations are needed — one on the numerators, one on the denominators.",
        "eliminate": "For HCF, each given fraction divided by the candidate must be a whole number; for LCM, the candidate divided by each given fraction must be a whole number.",
        "traps": ["Swapping the two formulas — pairing HCF with HCF and LCM with LCM instead of crosswise.", "Treating the fractions as decimals and taking a plain HCF/LCM of those instead of working on numerators and denominators."]},
    "q-hl-algebra": {
        "cue": "A conceptual or symbolic HCF/LCM question — algebraic expressions, prime-power notation, or a stated relation between the HCF, LCM and the original quantities.",
        "formulas": ["hl-f17"], "tech": ["hcf-lcm-product"],
        "standard": "Apply HCF × LCM = product exactly as for numbers; for prime-power notation, HCF takes the lower power and LCM the higher power of each prime (a prime missing from one side drops out of the HCF but still appears in the LCM).",
        "fast": "Translate the relation into the same HCF-LCM identity used for plain numbers, then read off the answer.",
        "eliminate": "Test the claimed identity on a small worked numerical example of the same shape before trusting it symbolically.",
        "traps": ["Assuming HCF and LCM simply swap the two original quantities instead of checking the real identity.", "Taking the higher shared power of a prime for the HCF, or the lower for the LCM — the two are swapped from what's needed."]},
}
REFS = []
PYQS = [
    pyq(K1, 12, "q-hl-lcm-offset", 'Find the least number which, when increased by 1, is exactly divisible by 22, 17, 33 and 34.', ['1120', '1122', '1121', '1123'], "c",
        ['LCM of 22, 17, 33, 34 = 2 × 3 × 11 × 17 = 1122.', 'The number is one less than the LCM: 1122 − 1 = 1121.'],
        lambda: math.lcm(22, 17, 33, 34) - 1, 1121, 0, tech=['lcm-units'], trick='N + 1 = LCM, so N = LCM − 1.'),
    pyq(K1, 35, "q-hl-lcm-offset", 'N is the least 4-digit number which, divided by 3, 6, 9 and 12, leaves remainders 2, 5, 8 and 11. What is the remainder when N is divided by 11?', ['10', '8', '6', '5'], "c",
        ['Each remainder is one less than its divisor, so N + 1 is a multiple of LCM(3, 6, 9, 12) = 36.', 'Least 4-digit: N + 1 = 36 × 28 = 1008, N = 1007.', '1007 ÷ 11 leaves remainder 6.'],
        lambda: ((1001 + 35) // 36 * 36 - 1) % 11, 6, 0, tech=['lcm-units'], trick='Remainder = divisor − 1 each time → N = LCM × k − 1.', concepts=2),
    pyq(K1, 36, "q-hl-lcm-offset", 'N is the largest 3-digit number which, divided by 6, 8 and 12, leaves remainders 3, 5 and 9. What is the remainder when N is divided by 7?', ['6', '4', '2', '1'], "d",
        ['Each remainder is 3 less than its divisor, so N + 3 is a multiple of LCM(6, 8, 12) = 24.', '24 × 42 = 1008 would make N = 1005, which has four digits, so the largest is N + 3 = 24 × 41 = 984, N = 981.', '981 ÷ 7 leaves remainder 1.'],
        lambda: ((999 + 3) // 24 * 24 - 3) % 7, 1, 0, tech=['lcm-units'], trick='Divisor − remainder is 3 every time → N = 24k − 3; largest 3-digit is 981.', concepts=2),
    pyq(K1, 37, "q-hl-two-rem", 'N is the least number which, divided by 7, leaves remainder 4 and, divided by 12, leaves remainder 7. What is the remainder when N is divided by 13?', ['1', '2', '6', '11'], "b",
        ['N = 12m + 7 and it must leave 4 on division by 7. Try m = 0, 1, 2…: 7, 19, 31, 43, 55, 67 → 67 = 7 × 9 + 4.', 'N = 67, and 67 ÷ 13 leaves remainder 2.'],
        lambda: (12 * 5 + 7) % 13, 2, 0, tech=['back-substitute'], trick='List 12m + 7 (7, 19, 31, 43, 55, 67) until one is 4 mod 7.', concepts=2),
    pyq(K1, 43, "q-hl-two-rem", 'N is the largest three-digit number which, divided by 8 and 6, leaves remainders 1 and 3. What is the remainder when N is divided by 5?', ['1', '2', '3', '4'], "c",
        ['8k + 1 = 6m + 3. The smallest such number is 9; the numbers repeat every LCM(8, 6) = 24, so N = 24p + 9.', 'Largest below 1000: p = 41 → N = 993. 993 ÷ 5 leaves remainder 3.'],
        lambda: (24 * 41 + 9) % 5, 3, 0, tech=['lcm-units'], trick='Find the first common number (9), then step by the LCM (24).', concepts=2),
    pyq(K1, 44, "q-hl-two-rem", 'How many numbers lie between 10 and 1000 which, divided by 6 and 8, leave remainders 1 and 3?', ['40', '41', '42', '45'], "b",
        ['6k + 1 = 8m + 3. The smallest above 10 is 19; the numbers repeat every LCM(6, 8) = 24, so N = 24p + 19.', 'Largest below 1000: p = 40 → 979. p runs 0 to 40: 41 numbers.'],
        lambda: (979 - 19) // 24 + 1, 41, 0, tech=['lcm-units'], trick='First common number 19, then step 24 up to 979: (979 − 19) ÷ 24 + 1.', concepts=2),
]
PYQS = PYQS + PYQS_C19LH + PYQS_C19LH2


def practice_items():
    return []
