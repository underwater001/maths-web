"""Average: quiz tier (past questions with checked answers, solutions and a short method per type)."""
from fractions import Fraction as F
from bank import bound, mistake, pyq
from topics._ch18av_ry import PYQS_RY as PYQS_C18AV

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
    "q-av-backsolve": {"short": "Backward alligation", "label": "Find a group's size or % from a combined average", "kind": "qtype", "parent": "c-av-weighted", "order": 2,
                       "summary": "Given two group averages and the combined average, find the ratio of group sizes (or a percentage split) — the weighted-average formula run backwards.", "links": ["mixture-alligation"]},
    "c-av-replace": {"short": "Replace or remove", "label": "A group's average changes when one member changes", "kind": "concept", "parent": TOPIC, "order": 4,
                     "summary": "Swapping out one member (or removing one, with no replacement) for another shifts the TOTAL by exactly (group size × change in average).", "links": []},
    "q-av-replace": {"short": "Replacement/removal", "label": "Find the new, old, or removed member's value", "kind": "qtype", "parent": "c-av-replace", "order": 1,
                     "summary": "The average rises or falls when a member is swapped out (for one or two others) or simply removed; find the value responsible.", "links": []},
    "c-av-series": {"short": "Series averages", "label": "Mean of a run of related numbers", "kind": "concept", "parent": TOPIC, "order": 5,
                    "summary": "Natural/whole/odd numbers in a run, their squares, or an odd count of consecutive integers — each has its own quick mean formula.", "links": ["number-system"]},
    "q-av-series": {"short": "First n naturals/odds/wholes", "label": "Mean of the first n naturals, whole numbers, or odd numbers", "kind": "qtype", "parent": "c-av-series", "order": 1,
                    "summary": "An evenly spaced run starting at a fixed point (0, 1, or the first odd number) — mean is (first + last)/2.", "links": []},
    "q-av-squares": {"short": "Mean of squares", "label": "Mean of the squares of the first n naturals", "kind": "qtype", "parent": "c-av-series", "order": 2,
                     "summary": "Needs the sum-of-squares formula, not the evenly-spaced-mean shortcut.", "links": []},
    "q-av-consec-mid": {"short": "Consecutive integers", "label": "Mean of an odd count of consecutive integers", "kind": "qtype", "parent": "c-av-series", "order": 3,
                        "summary": "The mean of an odd number of consecutive integers is simply the middle one.", "links": []},
    "c-av-overlap": {"short": "Overlapping groups", "label": "Two groups that share one member", "kind": "concept", "parent": TOPIC, "order": 6,
                     "summary": "'First k of a set' and 'last k of a set' can share one member (like day 4 of a 7-day week counted in both a first-4 and a last-4 average) — adding both group totals double-counts it.", "links": []},
    "q-av-overlap": {"short": "Shared-member average", "label": "Find the member two groups have in common", "kind": "qtype", "parent": "c-av-overlap", "order": 1,
                     "summary": "Given two overlapping groups' averages and the whole set's average, find the value of the member they share.", "links": []},
    "c-av-algebra": {"short": "Algebraic identities", "label": "Average expressed symbolically", "kind": "concept", "parent": TOPIC, "order": 7,
                     "summary": "Pure algebra facts about averages: shifting every term by a constant shifts the mean the same way; scaling every term scales the mean; deviations from the mean always sum to zero; two symbolic groups combine by adding their (symbolic) totals.", "links": []},
    "q-av-algebra": {"short": "Symbolic average identity", "label": "Average of x1…xn, or of two symbolic groups", "kind": "qtype", "parent": "c-av-algebra", "order": 1,
                     "summary": "No actual numbers — work out how the average transforms under a shift, a scaling, a deviation sum, or combining two algebraically-described groups.", "links": []},
}
FORMULAS = [
    {"id": "av-f1", "node": "c-av-total", "text": "Total = average × count     Average = total ÷ count", "note": "Convert every average to a total before doing anything else."},
    {"id": "av-f2", "node": "c-av-total", "text": "Missing part = total − (sum of the known parts)", "note": "Numbers that are given but not needed (a distractor) are common."},
    {"id": "av-f3", "node": "c-av-weighted", "text": "Weighted average = (n₁a₁ + n₂a₂ + …) ÷ (n₁ + n₂ + …)", "note": "A ratio 3 : 4 : 6 can be used as the n's directly."},
    {"id": "av-f4", "node": "c-av-spaced", "text": "Average of evenly spaced numbers = (first + last) ÷ 2", "note": "First multiple above the lower limit, last multiple below the upper limit. Also works for a plain run like 'first n naturals' or 'first n odd numbers' — just identify the first and last term."},
    {"id": "av-f10", "node": "c-av-weighted", "text": "A combined average splits the gap between two group averages in the INVERSE ratio of the two group sizes: size₁ : size₂ = (avg₂ − combined) : (combined − avg₁)", "note": "The alligation cross-rule applied to averages — use it to solve backward for an unknown size ratio or percentage split."},
    {"id": "av-f5", "node": "c-av-replace", "text": "Change in TOTAL = group size × change in average. If one member is swapped out for one other: new member's value = old member's value ± (change in total). If a member just leaves (no replacement): leaving member's value = old total − new total (group size drops by 1).", "note": "Works whether the average rises or falls — just keep the sign consistent."},
    {"id": "av-f6", "node": "c-av-series", "text": "Sum of squares of the first n natural numbers = n(n+1)(2n+1)/6", "note": "Divide by n for the mean of the squares."},
    {"id": "av-f7", "node": "c-av-series", "text": "The average of an ODD count of consecutive integers equals the middle term itself", "note": "With this, 'average = 26, find the smallest of 7 consecutive integers' is just 26 minus 3 steps — no equation needed."},
    {"id": "av-f8", "node": "c-av-overlap", "text": "If 'first k' and 'last k' of an (2k−1)-member set share exactly one member: shared member = (sum of first k) + (sum of last k) − (sum of the whole set)", "note": "Equivalently: k×(first-group average) + k×(last-group average) − (2k−1)×(whole-set average)."},
    {"id": "av-f9", "node": "c-av-algebra", "text": "Adding (or subtracting) a constant c to every term shifts the mean by c. Multiplying every term by c scales the mean by c. The sum of deviations from the mean, Σ(xᵢ − x̄), is always exactly 0. Two groups described only symbolically (sizes and averages both as letters) combine by weighted average exactly as with numbers: (size₁×avg₁ + size₂×avg₂)/(size₁+size₂).", "note": "None of these need the actual numbers or even the group size — they are pure identities."},
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
    "q-av-backsolve": {
        "cue": "Two sub-group averages are given (e.g. girls/boys, or two classes) along with the COMBINED average, and the question asks for a percentage split or a size ratio — the reverse of the usual weighted-average question.",
        "formulas": ["av-f10", "av-f3"], "tech": ["ratio-parts", "identity"],
        "standard": "Find how far the combined average sits from each group's average, then the group sizes are in the INVERSE of those two gaps.",
        "fast": "With three or more linked groups (pairwise combined averages given), convert each pairwise average into a small linear equation between two group sizes, then chain them into one overall ratio before doing the weighted average.",
        "eliminate": "The side with the SMALLER gap to the combined average is the LARGER group — a common sign-flip trap.",
        "traps": ["Reporting the wrong group's percentage (girls' instead of boys', or vice versa).", "Using the direct ratio of the gaps instead of the inverse.", "With three groups, trying to weighted-average before finding the size ratio from the pairwise averages."]},
    "q-av-replace": {
        "cue": "'The average of N … increases/decreases by … when one (or two) is replaced by a new one (or two new ones)', or '… one leaves and the average changes by …'.",
        "formulas": ["av-f5", "av-f1"], "tech": ["identity"],
        "standard": "Find the change in TOTAL first (group size × change in average), then add or subtract it from the old value(s) as the direction of the change requires.",
        "fast": "Rising average ⟹ new value is old value PLUS the total change; falling average ⟹ new value is old value MINUS it.",
        "eliminate": "When someone simply leaves (no replacement), the group size changes too — use the NEW, smaller count for the new total, not the original count.",
        "traps": ["Using the change in AVERAGE instead of the change in TOTAL as the adjustment.", "Getting the sign backwards (adding when the average fell, or vice versa).", "For a pair replaced, forgetting the question asks for their average, not their combined total.", "For someone leaving (not replaced), still using the original group size for the new total."]},
    "q-av-series": {
        "cue": "'Average of the first n natural/whole/odd numbers' (no actual list given, just a description of the run).",
        "formulas": ["av-f4"], "tech": ["identity"],
        "standard": "Identify the first and last term of the run (watch whether it starts at 0 or 1, or skips to the next odd/even number), then average = (first + last)/2.",
        "fast": "No need to add every term — just the two end values.",
        "eliminate": "'Whole numbers' start at 0, 'natural numbers' start at 1 — options built on the wrong starting point are a common distractor pair.",
        "traps": ["Confusing whole numbers (start at 0) with natural numbers (start at 1).", "Using the wrong last term for an odd/even run (e.g. 100 instead of 99 for odd numbers up to 100).", "Forgetting the −1 when converting 'first n' into the actual last term."]},
    "q-av-squares": {
        "cue": "'Average of the squares of the first n natural numbers.'",
        "formulas": ["av-f6"], "tech": ["standard-values"],
        "standard": "Apply n(n+1)(2n+1)/6 for the sum of squares, then divide by n for the mean.",
        "fast": "For small n, the n(n+1)(2n+1)/6 ÷ n simplifies to (n+1)(2n+1)/6 — one less multiplication.",
        "eliminate": "The mean of squares is always noticeably bigger than the square of the mean — a suspiciously small option is likely a sum-of-naturals mix-up instead of sum-of-squares.",
        "traps": ["Using the sum-of-naturals formula n(n+1)/2 by mistake instead of the sum-of-squares one.", "Forgetting to divide the sum of squares by n at the end.", "An off-by-one slip in n itself."]},
    "q-av-consec-mid": {
        "cue": "'The average of k consecutive (positive) integers is …' with k ODD, asking for the smallest, largest, or some other specific one.",
        "formulas": ["av-f7"], "tech": ["identity"],
        "standard": "The given average IS the middle term; count forward or back the right number of steps to reach the one asked for.",
        "fast": "No equation-solving needed at all — just count ± steps from the average.",
        "eliminate": "For k consecutive integers, smallest = average − (k−1)/2 and largest = average + (k−1)/2 — check the step count matches k.",
        "traps": ["Using the wrong number of steps (off by one from (k−1)/2).", "Trying to set up and solve an equation instead of using the direct middle-term shortcut.", "Mixing up which end (largest vs smallest) corresponds to adding vs subtracting the steps."]},
    "q-av-overlap": {
        "cue": "'The average of the first k days/items of a set is …, the average of the last k is …, the average of the WHOLE (2k−1-member) set is …' — find the one item common to both groups (day k, say).",
        "formulas": ["av-f8"], "tech": ["identity"],
        "standard": "Add the first-group total and the last-group total, then subtract the whole set's total — what's left over is exactly the shared member.",
        "fast": "k×(first avg) + k×(last avg) − (2k−1)×(whole avg), all in one line.",
        "eliminate": "Simply repeating one of the three given averages as the answer (a common wrong-option pattern) ignores that the shared member is usually a distinctly different value from all three.",
        "traps": ["Forgetting that the shared member is counted in BOTH group totals, so it must be subtracted out once via the whole-set total.", "Using the wrong total count for the whole set (it's 2k−1, not 2k, since one member is shared).", "Just picking one of the three given averages as a plausible-looking shortcut."]},
    "q-av-algebra": {
        "cue": "No actual numbers — the question is phrased with x₁, x₂, …, xₙ, x̄, or two groups described only by letters (x numbers averaging y, y numbers averaging x, etc.).",
        "formulas": ["av-f9"], "tech": ["identity"],
        "standard": "Match the question to the right identity: shift (add/subtract a constant), scale (multiply by a constant), the deviation-sum-is-zero fact, or the symbolic weighted-average combination — then substitute directly, no real arithmetic needed.",
        "fast": "These are pure recall once the matching identity is spotted; there's nothing to compute beyond simplifying the resulting expression.",
        "eliminate": "An option that still has the count n in it after a pure shift-by-constant question (where n should have cancelled out entirely) is a trap.",
        "traps": ["Confusing 'add a constant to every term' (mean shifts by that constant) with 'multiply every term by a constant' (mean scales by that constant).", "Forgetting the deviation-sum identity is a universal fact (always 0), not something that depends on the specific numbers.", "When combining two symbolic groups, forgetting that EACH group's own size is its own average's partner (x numbers go with average y, not with x)."]},
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

PYQS = PYQS + PYQS_C18AV


def practice_items():
    return []
