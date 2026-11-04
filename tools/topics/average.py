"""Average: quiz tier (past questions with checked answers, solutions and a short method per type)."""
from fractions import Fraction as F
from bank import bound, mistake, pyq

TOPIC = "average"
PREFIX = "av"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-av-total": {"short": "Work with totals", "label": "Average is total ÷ count: work with totals", "kind": "concept", "parent": TOPIC, "order": 1,
                   "summary": "Turn every average into a total (average × count). Missing parts are then plain subtraction.", "links": []},
    "c-av-weighted": {"short": "Weighted average", "label": "Weighted average", "kind": "concept", "parent": TOPIC, "order": 2,
                      "summary": "Groups of different sizes: weigh each group's average by its size.", "links": ["mixture-alligation", "ratio-proportion"]},
    "c-av-spaced": {"short": "Evenly spaced", "label": "Evenly spaced numbers", "kind": "concept", "parent": TOPIC, "order": 3,
                    "summary": "For numbers in steps (multiples of 13, odd numbers…) the average is the middle: (first + last) ÷ 2.", "links": []},
    "q-av-parts": {"short": "Missing part", "label": "Find a missing number or a group's average", "kind": "qtype", "parent": "c-av-total", "order": 1,
                   "summary": "Overall average, some group averages known; find the number or the average that is left.", "links": []},
    "q-av-weighted": {"short": "Weighted", "label": "Average of groups in a ratio", "kind": "qtype", "parent": "c-av-weighted", "order": 1,
                      "summary": "Group averages and a ratio of group sizes; find the overall average.", "links": []},
    "q-av-spaced": {"short": "Multiples in a range", "label": "Average of multiples between two numbers", "kind": "qtype", "parent": "c-av-spaced", "order": 1,
                    "summary": "All integers between two limits that are divisible by k.", "links": ["number-system"]},
}
FORMULAS = [
    {"id": "av-f1", "node": "c-av-total", "text": "Total = average × count     Average = total ÷ count", "note": "Convert every average to a total before doing anything else."},
    {"id": "av-f2", "node": "c-av-total", "text": "Missing part = total − (sum of the known parts)", "note": "Numbers that are given but not needed (a distractor) are common."},
    {"id": "av-f3", "node": "c-av-weighted", "text": "Weighted average = (n₁a₁ + n₂a₂ + …) ÷ (n₁ + n₂ + …)", "note": "A ratio 3 : 4 : 6 can be used as the n's directly."},
    {"id": "av-f4", "node": "c-av-spaced", "text": "Average of evenly spaced numbers = (first + last) ÷ 2", "note": "First multiple above the lower limit, last multiple below the upper limit."},
]
METHODS = {
    "q-av-parts": {
        "cue": "An average of some numbers, averages of some of them, and a number or a sub-group's average is asked.",
        "formulas": ["av-f1", "av-f2"], "tech": ["cancel-first", "estimate"],
        "standard": "Total = average × count for the whole set and for each known part. Subtract the known parts from the whole, then divide by how many numbers are left.",
        "fast": "Work with the differences from the overall average: each part's surplus or deficit must cancel. 13 numbers at 75: the six at 69 are 6×(−6) = −36 and the six at 80 are 6×5 = +30, so the 7th is 75 + 6 = 81.",
        "eliminate": "The missing value must lie on the other side of the overall average from the part that is short. If the known groups average below the overall average, the leftover is above it.",
        "traps": ["Using the wrong count when dividing (11th and 12th are two numbers, not one).", "Using a clue that is not needed, such as '11th is 12 more than the 12th', when only the sum of the two matters.", "Treating 20% more as +20 instead of × 1.2."]},
    "q-av-weighted": {
        "cue": "Several groups with their own averages and sizes (or a ratio of sizes), and the overall average is asked.",
        "formulas": ["av-f3"], "tech": ["ratio-parts", "estimate"],
        "standard": "Multiply each group's average by its weight, add, divide by the total weight.",
        "fast": "Start from the lowest average and add the surplus: 17 + (0×3 + 2×4 + 6×6) ÷ 13 = 17 + 44/13 = 20.38.",
        "eliminate": "The overall average is pulled towards the biggest group, here 23 (weight 6), so it is above the simple mean 19.67. Strike options below it.",
        "traps": ["Taking the simple mean of the group averages.", "Dividing by the number of groups instead of the total weight."]},
    "q-av-spaced": {
        "cue": "'Average of all integers between a and b that are divisible by k.'",
        "formulas": ["av-f4"], "tech": ["divisibility", "estimate"],
        "standard": "List the first and last multiples inside the range, then the average is their mean.",
        "fast": "First multiple = k × (smallest whole number above a/k); last = k × (largest below b/k). 150 ÷ 13 ≈ 11.5 → 13×12 = 156; 300 ÷ 13 ≈ 23.07 → 13×23 = 299. (156 + 299) ÷ 2 = 227.5.",
        "eliminate": "The answer is the middle of the two end multiples, so it sits near the middle of the range and is a multiple of 0.5 (k × (m + n) ÷ 2).",
        "traps": ["Using the limits themselves (150 and 300) instead of the first and last multiples.", "Including a limit that is not a multiple."]},
}
PYQS = [
    pyq(S1, 53, "q-av-spaced", "What is the average of all integers between 150 and 300 that are exactly divisible by 13?", ["220", "227.5", "230", "235.5"], "b",
        ["Multiples of 13 in range: 13×12 = 156 up to 13×23 = 299.", "They are evenly spaced, so the average is (156 + 299) ÷ 2 = 227.5."],
        lambda: sum(x for x in range(151, 300) if x % 13 == 0) / len([x for x in range(151, 300) if x % 13 == 0]), 227.5, 1e-9, tech=["divisibility", "estimate"],
        trick="Find only the two end multiples (156 and 299) and halve their sum."),
    pyq(S1, 54, "q-av-parts", "The average of 12 numbers is 75. The average of the first 5 is 68. The average of the next 5 is 20% more than the average of the first 5. The 11th number is 12 more than the 12th. Find the average of the 11th and 12th numbers.",
        ["72.5", "76", "82.3", "88"], "b",
        ["Total of 12 numbers = 12 × 75 = 900. First five total = 5 × 68 = 340.", "Next five average = 68 × 1.2 = 81.6, total = 408.", "Last two total = 900 − 340 − 408 = 152, so their average = 76. (The '12 more' clue is not needed.)"],
        lambda: (12 * 75 - 5 * 68 - 5 * (68 * 1.2)) / 2, 76, 1e-9, tech=["cancel-first"], concepts=1, heavy=True,
        trick="The 11th and 12th together are all that is left, so only their sum matters; ignore the '12 more' clue."),
    pyq(S2, 62, "q-av-parts", "In a group of 60 workers the average monthly income is ₹28,000. If 20 junior workers average ₹18,000 each, find the average income of the senior workers.",
        ["₹33,000", "₹34,500", "₹35,000", "₹36,500"], "a",
        ["Total income = 60 × 28,000 = ₹16,80,000. Juniors' total = 20 × 18,000 = ₹3,60,000.", "Seniors' total = 16,80,000 − 3,60,000 = ₹13,20,000 for 40 workers.", "Average = ₹33,000."],
        lambda: (60 * 28000 - 20 * 18000) / 40, 33000, 0, tech=["cancel-first"],
        trick="Juniors are 10,000 below 28,000 and there are 20 of them; the 40 seniors must make it up: 20 × 10,000 ÷ 40 = 5,000 above, so 33,000."),
    pyq(S3, 62, "q-av-weighted", "Three batches of students have average ages 17, 19 and 23 years, and their numbers are in the ratio 3 : 4 : 6. Find the overall average age.",
        ["19.41", "20.38", "21.20", "18.9"], "b",
        ["Use the ratio as weights: 3×17 + 4×19 + 6×23 = 51 + 76 + 138 = 265.", "Total weight = 13, so the average = 265 ÷ 13 ≈ 20.38."],
        lambda: (3 * 17 + 4 * 19 + 6 * 23) / 13, 20.38, 0.005, tech=["ratio-parts", "estimate"], concepts=1, heavy=True,
        trick="The biggest batch (weight 6) is the oldest, so the average is well above 19.67. That removes 19.41 and 18.9.",
        wrong={"a": bound("The oldest batch is also the biggest, so the average must be above the simple mean 19.67. 19.41 is below it.", lambda v: v < 19.67),
               "d": bound("The average must be above the simple mean 19.67, because the biggest batch is the oldest. 18.9 is below it.", lambda v: v < 19.67)}),
    pyq(S3, 63, "q-av-parts", "The average of 13 numbers is 75. The average of the first six is 69 and the average of the last six is 80. Find the 7th number.",
        ["81", "82", "83", "84"], "a",
        ["Total = 13 × 75 = 975. First six = 6 × 69 = 414. Last six = 6 × 80 = 480.", "7th number = 975 − 414 − 480 = 81."],
        lambda: 13 * 75 - 6 * 69 - 6 * 80, 81, 0, tech=["cancel-first"],
        trick="Differences from 75: six numbers at −6 give −36, six at +5 give +30. The 7th is 75 + 6 = 81."),
    pyq(S3, 64, "q-av-spaced", "What is the average of all integers between 200 and 350 that are exactly divisible by 11?", ["275", "272", "286", "292"], "a",
        ["First multiple above 200 is 11 × 19 = 209. Last below 350 is 11 × 31 = 341.", "Average = (209 + 341) ÷ 2 = 275."],
        lambda: sum(x for x in range(201, 350) if x % 11 == 0) / len([x for x in range(201, 350) if x % 11 == 0]), 275, 1e-9, tech=["divisibility", "estimate"],
        trick="The answer is the midpoint of 209 and 341, and the midpoint of two multiples of 11 with an odd count is a multiple of 11 itself. Only 275 and 286 are, and 286 is too high.",
        wrong={"b": bound("The average of evenly spaced multiples of 11 with an odd count of terms is itself a multiple of 11, and 272 is not.", lambda v: v % 11 != 0),
               "d": bound("Same test: 292 is not a multiple of 11.", lambda v: v % 11 != 0)}),
]


def practice_items():
    return []
