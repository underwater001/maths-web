"""Ratio and proportion: quiz tier."""
from bank import bound, mistake, pyq, ratio_val

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
}
FORMULAS = [
    {"id": "rp-f1", "node": "c-rp-change", "text": "Quantities a : b : c = ak : bk : ck. After adding x to one quantity, form the new ratio and cross-multiply.", "note": "One equation in k, then the rest follows."},
    {"id": "rp-f2", "node": "c-rp-change", "text": "If a : b becomes c : d after adding, then (ak + p)/(bk + q) = c/d", "note": "Use the pair whose added amounts are known first."},
    {"id": "rp-f3", "node": "c-rp-equal", "text": "If x% of P = y% of Q = z% of R = k, then P : Q : R = 1/x : 1/y : 1/z", "note": "Bigger percentage → smaller quantity."},
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


def practice_items():
    return []
