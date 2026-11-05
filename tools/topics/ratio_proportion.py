"""Ratio and proportion: quiz tier."""
from bank import bound, mistake, pyq, ratio_val
from topics._rp_ry import PYQS_RY

TOPIC = "ratio-proportion"
PREFIX = "rp"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-rp-change": {"short": "After a change", "label": "Ratios after something is added", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "Write the old quantities as ratio × k (the unknown multiplier), apply the change, and match the new ratio.", "links": ["algebraic-identities"]},
    "c-rp-equal": {"short": "Equal parts", "label": "Several quantities tied by percentages", "kind": "concept", "parent": TOPIC, "order": 2,
                   "summary": "40% of P = 0.5 of Q = 1/8 of R: set them all equal to one number k and read off the ratio.", "links": ["percentage"]},
    "q-rp-add": {"short": "Add and re-ratio", "label": "Ratio changes after adding", "kind": "qtype", "parent": "c-rp-change", "order": 1,
                 "summary": "Quantities in a ratio; some are added and the ratio changes; find a number added or the original total.", "links": []},
    "q-rp-swap": {"short": "Swapped order", "label": "Numbers and prices swapped", "kind": "qtype", "parent": "c-rp-change", "order": 2,
                  "summary": "A price ratio and a bill that changes by a % when the quantities are interchanged.", "links": ["percentage"]},
    "q-rp-chain": {"short": "Linked by %", "label": "P : Q : R from percentage links", "kind": "qtype", "parent": "c-rp-equal", "order": 1,
                   "summary": "Percentages or fractions of three quantities are equal; find their ratio.", "links": []},
    "q-rp-age": {"short": "Ages", "label": "Ages in a ratio, now and later", "kind": "qtype", "parent": "c-rp-change", "order": 3,
                 "summary": "Ages are in a ratio now; after or before some years the ratio changes; find a present age.", "links": []},
    "c-rp-basic": {"short": "Basic ratios", "label": "Reading, linking and combining ratios", "kind": "concept", "parent": TOPIC, "order": 3,
                   "summary": "Write the quantities as ratio × k; join A : B and B : C by making the common term equal; plug in numbers for expression questions.", "links": ["algebraic-identities"]},
    "q-rp-basic": {"short": "Chains and plug-in", "label": "A : B : C chains, expressions and equations", "kind": "qtype", "parent": "c-rp-basic", "order": 1,
                   "summary": "Join two ratios into one, find a value of x : y expressions, reciprocal ratios, equal-fraction chains and ratio equations.", "links": ["algebraic-identities"]},
    "c-rp-share": {"short": "Shares", "label": "Dividing a sum and money in a ratio", "kind": "concept", "parent": TOPIC, "order": 4,
                   "summary": "Divide a total in a ratio, find a part from a difference, handle coins by value and incomes against expenditure.", "links": ["percentage", "profit-loss"]},
    "q-rp-share": {"short": "Dividing a sum", "label": "Divide a sum among two or more people", "kind": "qtype", "parent": "c-rp-share", "order": 1,
                   "summary": "A total or a difference of two shares is given; find a share, a total or the ratio of the shares.", "links": []},
    "q-rp-group": {"short": "Coins, income and expense", "label": "Coins by value, income against expenditure", "kind": "qtype", "parent": "c-rp-share", "order": 2,
                   "summary": "Coins whose values or numbers are in a ratio; savings from incomes and expenditures in ratios; averages by ratio of groups.", "links": ["percentage"]},
    "c-rp-prop": {"short": "Proportion", "label": "Fourth, third and mean proportionals", "kind": "concept", "parent": TOPIC, "order": 5,
                  "summary": "A proportion a : b :: c : d means ad = bc; continued proportion a, b, c means b² = ac.", "links": []},
    "q-rp-prop": {"short": "Proportionals", "label": "Fourth, third, mean proportionals and tests", "kind": "qtype", "parent": "c-rp-prop", "order": 1,
                  "summary": "Find the missing term, check whether four numbers form a proportion, or the number added to make them proportional.", "links": []},
}
FORMULAS = [
    {"id": "rp-f1", "node": "c-rp-change", "text": "Quantities a : b : c = ak : bk : ck. After adding x to one quantity, form the new ratio and cross-multiply.", "note": "One equation in k, then the rest follows."},
    {"id": "rp-f2", "node": "c-rp-change", "text": "If a : b becomes c : d after adding, then (ak + p)/(bk + q) = c/d", "note": "Use the pair whose added amounts are known first."},
    {"id": "rp-f3", "node": "c-rp-equal", "text": "If x% of P = y% of Q = z% of R = k, then P : Q : R = 1/x : 1/y : 1/z", "note": "Bigger percentage → smaller quantity."},
    {"id": "rp-f4", "node": "c-rp-basic", "text": "A : B = a : b and B : C = c : d  ⇒  A : B : C = ac : bc : bd", "note": "Make the common term equal first, using the LCM of its two values."},
    {"id": "rp-f5", "node": "c-rp-basic", "text": "If 2A = 3B = 4C then A : B : C = 1/2 : 1/3 : 1/4 = 6 : 4 : 3. If A/2 = B/3 = C/4 the ratio is simply 2 : 3 : 4.", "note": "Equal products give reciprocals; equal fractions give the denominators."},
    {"id": "rp-f6", "node": "c-rp-share", "text": "A total T in the ratio a : b : c gives the first share T × a/(a + b + c). A given difference of two shares equals the difference of their ratio terms in parts.", "note": "Find one part first; every share is a multiple of it."},
    {"id": "rp-f7", "node": "c-rp-share", "text": "Ratio of coin values v1 : v2 : v3 with coin values c1, c2, c3 gives numbers v1/c1 : v2/c2 : v3/c3. If the ratio is of numbers, the values are n1 c1 + n2 c2 + n3 c3.", "note": "Read whether the ratio is of values or of numbers before anything else."},
    {"id": "rp-f8", "node": "c-rp-share", "text": "Incomes a x and b x, expenditures c y and d y, equal savings S: a x − c y = S and b x − d y = S. Solve the pair or test the options.", "note": "Savings = income − expenditure, never the ratio terms themselves."},
    {"id": "rp-f9", "node": "c-rp-prop", "text": "a : b :: c : d ⇔ ad = bc. Fourth proportional = bc/a, third proportional of a and b = b²/a, mean proportional = √(ab). Continued proportion a, b, c: b² = ac.", "note": "Cross-multiply to test or to solve for the missing term."},
    {"id": "rp-f10", "node": "c-rp-change", "text": "Ages a : b now; after t years the ratio is c : d: (ak + t)/(bk + t) = c/d. The difference of the two ages never changes.", "note": "Add or subtract t from each real age, not from the ratio terms."},
]
METHODS = {
    "q-rp-add": {
        "cue": "'Ratio … becomes … after 18 are added' or 'joined by 15 more'.",
        "formulas": ["rp-f1", "rp-f2"], "tech": ["scaling", "back-substitute"],
        "standard": "Pens 2k : 5k : 7k. Yellow and red give (2k + 18)/(5k + 12) = 3/6 = 1/2, so 4k + 36 = 5k + 12, k = 24. New blue = 8 × (2k + 18)/3 = 176, so 176 − 168 = 8 were added.",
        "fast": "Pick the two quantities whose additions are both known and solve k from them alone; do the third afterwards.",
        "eliminate": "Test options in the final equation: blue 7k + x must be a multiple of 8 in the new ratio. With k = 24, 168 + x ≡ 0 (mod 8), so x is a multiple of 8.",
        "traps": ["Adding to the ratio numbers instead of to the real quantities (k × ratio).", "Using the wrong pair and losing the unknown.", "Taking the new ratio as the old one plus the additions."]},
    "q-rp-swap": {
        "cue": "Two kinds of items with a price ratio; the numbers are interchanged and the bill rises by some %.",
        "formulas": ["rp-f1"], "tech": ["scaling", "back-substitute"],
        "standard": "Let a standard machine cost 1 and a premium 6. Original bill 15×6 + n = 90 + n. Swapped bill n×6 + 15 = 1.625(90 + n). So 6n + 15 = 146.25 + 1.625n and n = 30. Ratio 15 : 30 = 1 : 2.",
        "fast": "Try the option ratios: 1 : 2 means n = 30, original 120, swapped 195, and 195 ÷ 120 = 1.625. ✓",
        "eliminate": "The bill goes up, so premium machines were fewer than standard ones originally: the ratio is below 1 : 1. All options are, so test them one by one starting with the simplest.",
        "traps": ["Inverting the ratio asked (standard : premium).", "Using 62.5% as 6.25 or 0.625 in the equation.", "Forgetting to swap the 15 as well."]},
    "q-rp-chain": {
        "cue": "'40% of P = 0.5 of Q = 1/8 of R. Find P : Q : R.'",
        "formulas": ["rp-f3"], "tech": ["scaling", "back-substitute"],
        "standard": "Let each equal k. P = k/0.4 = 2.5k, Q = k/0.5 = 2k, R = 8k. Ratio 2.5 : 2 : 8 = 5 : 4 : 16.",
        "fast": "Take k = 4: P = 10, Q = 8, R = 32 → 5 : 4 : 16.",
        "eliminate": "40% is less than 50%, so P must be bigger than Q. Every option with the first term smaller than the second (4 : 5 : 16, 2 : 5 : 8, 4 : 5 : 8) is out at once.",
        "traps": ["Taking P : Q : R = 40 : 50 : 12.5, i.e. the percentages themselves, instead of their reciprocals.", "Mixing percent with fractions without converting (0.5 versus 50)."]},
    "q-rp-age": {
        "cue": "'Ratio of ages is 5 : 6 now; after 7 years it becomes 6 : 7. Find the present age.'",
        "formulas": ["rp-f10", "rp-f1"], "tech": ["back-substitute", "ratio-parts"],
        "standard": "Ages 5k and 6k: (5k + 7)/(6k + 7) = 6/7, so 35k + 49 = 36k + 42 and k = 7. A is 35.",
        "fast": "Test the options: 35 and 42 give 42 : 49 = 6 : 7. When the difference is known (1 part = 6 years) read the ages straight from it.",
        "eliminate": "The age must be a multiple of the ratio term (35 is 5 × 7). Options that are not multiples of 5 cannot be A's age.",
        "traps": ["Adding the years to the ratio terms instead of to the real ages.", "Answering with the ratio of the later ages when the question asks for present age.", "Forgetting that 'ago' means subtract."]},
    "q-rp-basic": {
        "cue": "'If A : B = 3 : 4 and B : C = 6 : 5, find A : B : C' or 'If x : y = 3 : 4 find (5x − 2y)/(7x + 2y)' or '2A = 3B = 4C'.",
        "formulas": ["rp-f4", "rp-f5"], "tech": ["lcm-units", "plug-numbers", "ratio-parts"],
        "standard": "A : B = 3 : 4, B : C = 6 : 5. Make B the LCM 12: A : B = 9 : 12 and B : C = 12 : 10, so A : B : C = 9 : 12 : 10.",
        "fast": "For x : y expressions put x and y equal to the ratio terms (x = 3, y = 4) and evaluate; for 2A = 3B = 4C set each to the LCM 12.",
        "eliminate": "Check the order asked (C : A, not A : C). A chain of three terms must keep the given pair: the right option reduces back to both original ratios.",
        "traps": ["Joining ratios without making the common term equal.", "Reading 3x = 5y = 4z as x : y : z = 3 : 5 : 4 (it is the reciprocal, 20 : 12 : 15).", "Giving the ratio in the order the book states but not the order asked."]},
    "q-rp-share": {
        "cue": "'₹ 738 is divided among A, B, C in the ratio 2 : 3 : 4. B's share is?' or 'A gets ₹ 7 more than B...'.",
        "formulas": ["rp-f6"], "tech": ["ratio-parts", "lcm-units", "back-substitute"],
        "standard": "Parts 2 + 3 + 4 = 9, one part = 738 ÷ 9 = 82, B = 3 × 82 = ₹ 246.",
        "fast": "Find one part, then read the share. When only a difference is given, divide it by the difference of the ratio terms to get the part.",
        "eliminate": "A share must be a whole multiple of the part: 738 ÷ 9 = 82 divides every correct share. Options that are not multiples of 82 are out.",
        "traps": ["Dividing by the number of people instead of the sum of the ratio terms.", "Using the ratio terms as shares when the given difference is not the total.", "For fractional ratios (1/2 : 1/3 : 1/4) forgetting to clear the fractions first."]},
    "q-rp-group": {
        "cue": "'Coins of ₹ 1, 50 paise, 25 paise; the ratio of their values is 13 : 11 : 7' or 'each saves ₹ 500 ...'.",
        "formulas": ["rp-f7", "rp-f8"], "tech": ["units-first", "back-substitute", "ratio-parts"],
        "standard": "Values 13 : 11 : 7 with coin values 1, 0.5, 0.2 give counts 13 : 22 : 35. 70 parts = 420 coins, so one part = 6 and 50 paise coins = 132.",
        "fast": "For incomes and expenditures with equal savings subtract: (income terms) − (expenditure terms) must be the same for both people, then solve the two equations.",
        "eliminate": "Counts must be whole: the number of coins of each kind is divisible by the part. Test an option: the savings of both people must come out equal.",
        "traps": ["Mixing up a ratio of values with a ratio of numbers.", "Using paise and rupees together (convert everything to rupees).", "Treating savings as the ratio difference without solving for both people."]},
    "q-rp-prop": {
        "cue": "'Third proportional to 12 and 18' or 'What number added to each of 6, 14, 18, 38 makes them proportional?'",
        "formulas": ["rp-f9"], "tech": ["back-substitute", "cancel-first"],
        "standard": "Third proportional x of 12 and 18: 12 : 18 = 18 : x so x = 18² ÷ 12 = 27.",
        "fast": "For 'add a number' questions: test the small option in the cross-product (6 + x)(38 + x) = (14 + x)(18 + x), or just try each option once.",
        "eliminate": "Products of extremes and of means must agree; check the units digits of both products to reject an option quickly.",
        "traps": ["Third proportional of a and b is b²/a, not a²/b.", "Mixing mean proportional (√(ab)) with the fourth proportional.", "Equal ratios written in the wrong order (a : b :: c : d means ad = bc)."]},
}
OPT54 = ["5 : 4 : 16", "4 : 5 : 16", "2 : 5 : 8", "4 : 5 : 8"]
PYQS = [
    pyq(S2, 53, "q-rp-swap", "A firm ordered 15 premium machines and some standard machines. A premium machine costs 6 times a standard one. By mistake the numbers of premium and standard machines were interchanged, which raised the bill by 62.5%. Find the ratio of premium to standard machines originally ordered.",
        ["3:7", "4:9", "1:2", "2:5"], "c",
        ["Let a standard machine cost 1 and a premium 6, and let there be n standard machines. Original bill = 15 × 6 + n = 90 + n.", "Swapped bill = 6n + 15 = 1.625 × (90 + n) = 146.25 + 1.625n.", "4.375n = 131.25, so n = 30.", "Premium : standard = 15 : 30 = 1 : 2."],
        lambda: ratio_val(f"15:{round((1.625 * 90 - 15) / (6 - 1.625))}"), ratio_val("1:2"), 1e-9, tech=["scaling", "back-substitute"], concepts=2, heavy=True,
        optvals=[ratio_val(t) for t in ("3:7", "4:9", "1:2", "2:5")],
        trick="Test 1 : 2: n = 30, original bill 120, swapped bill 195, and 195 ÷ 120 = 1.625.",
        wrong={}),
    pyq(S2, 58, "q-rp-add", "The numbers of yellow, red and blue pens in a box are in the ratio 2 : 5 : 7. 18 yellow, 12 red and some blue pens are added, and the ratio becomes 3 : 6 : 8. How many blue pens were added?",
        ["6", "8", "10", "12"], "b",
        ["Pens are 2k, 5k, 7k. Yellow and red give (2k + 18)/(5k + 12) = 3/6 = 1/2.", "4k + 36 = 5k + 12, so k = 24: 48, 120 and 168 pens.", "New yellow = 66 = 3 parts, so a part is 22 and new blue = 8 × 22 = 176.", "Blue added = 176 − 168 = 8."],
        lambda: 8 * ((2 * 24 + 18) / 3) - 7 * 24, 8, 1e-9, tech=["scaling"], concepts=1, heavy=True,
        trick="Use only yellow and red to get k = 24 first; blue then falls out as 176 − 168."),
    pyq(S2, 71, "q-rp-add", "The ratio of male to female employees in a company is 8 : 6. When 15 more female employees join, the ratio becomes 8 : 7. Find the original total number of employees.",
        ["180", "210", "252", "315"], "b",
        ["Males 8k, females 6k. After the change 8k/(6k + 15) = 8/7.", "7 × 8k = 8 × (6k + 15), so 56k = 48k + 120 and k = 15.", "Total = 14k = 210."],
        lambda: 14 * (120 / (56 - 48)), 210, 0, tech=["scaling", "divisibility"],
        trick="Males do not change, so 8 parts stay put: 7 new parts of female = 6 parts + 15, so one part is 15. Total 14 × 15.",
        wrong={"a": bound("The total must be 14 × 15 = 210; 180 is not a multiple of 14.", lambda v: v % 14 != 0),
               "d": bound("The total of 14 parts must be divisible by 14; 315 is 22.5 parts.", lambda v: v % 14 != 0)}),
    pyq(S3, 54, "q-rp-chain", "If 40% of P = 0.5 of Q = 1/8 of R, find P : Q : R.", OPT54, "a",
        ["Let all three equal k. P = k ÷ 0.4 = 2.5k, Q = k ÷ 0.5 = 2k, R = 8k.", "P : Q : R = 2.5 : 2 : 8 = 5 : 4 : 16."],
        lambda: ratio_val("5:4:16"), ratio_val("5:4:16"), 1e-9, tech=["scaling"], optvals=[ratio_val(t) for t in OPT54],
        trick="Take k = 4 so everything is whole: P = 10, Q = 8, R = 32.",
        wrong={"b": mistake("Took P : Q from 40 : 50 = 4 : 5, the percentages themselves instead of their reciprocals.", ratio_val("4:5:16"), 1e-9)}),
]

PYQS = PYQS + PYQS_RY


def practice_items():
    return []
