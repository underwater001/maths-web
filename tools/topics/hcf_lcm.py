"""HCF & LCM: quiz tier. Remainder problems solved with the LCM."""
import math
from fractions import Fraction as F
from bank import bound, mistake, pyq

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
}
FORMULAS = [
    {"id": "hl-f1", "node": "c-hl-rem", "text": "If every remainder = divisor − c (or + c) then N = k × LCM − c (or + c).", "note": "Check the gap with each divisor before using it."},
    {"id": "hl-f2", "node": "c-hl-rem", "text": "If the remainders differ: find the smallest N that fits, then all N = smallest + k × LCM.", "note": "Count of terms = (last − first) ÷ LCM + 1."},
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


def practice_items():
    return []
