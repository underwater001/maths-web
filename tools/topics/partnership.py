"""Partnership: question types, formulas, methods, PYQs and practice.

Every PYQ is a condensed restatement (own words, same numbers) pointing at its paper and question number.
Every PYQ answer is recomputed from its own numbers; every wrong-option note carries a check; every
practice answer is found twice by different methods. tools/build_topic.py enforces all of it.
"""
from fractions import Fraction as F
from math import gcd

from bank import bound, inr, mistake, pyq, prac, share, variants

TOPIC = "partnership"      # a topic node in data/tree.json
PREFIX = "pt"              # practice ids: pt-p01, pt-p02, ... (append new items at the end so old ids never move)

NODES = {
    "c-capital-time": {"short": "Capital × time", "label": "Profit shares follow capital × time", "kind": "concept", "parent": "partnership", "order": 1,
                       "summary": "The one idea behind almost every partnership question.", "links": []},
    "c-late-entry": {"short": "Late entry", "label": "Late entry and changing capital", "kind": "concept", "parent": "partnership", "order": 2,
                     "summary": "Partners who join late, leave early or change their capital.", "links": []},
    "c-working-partner": {"short": "Working partner", "label": "Working partner's extra share", "kind": "concept", "parent": "partnership", "order": 3,
                          "summary": "A commission or salary comes off the top before the ratio split.", "links": []},
    "c-common-unit": {"short": "Common unit", "label": "Rent shared by animals: one common unit", "kind": "concept", "parent": "partnership", "order": 4,
                      "summary": "Pasture and rent questions are partnership with animals instead of money.", "links": []},
    "q-pt-two": {"short": "Two partners", "label": "Two partners: share or total profit", "kind": "qtype", "parent": "c-capital-time", "order": 1,
                 "summary": "Capitals and times given; find a share, or find the total profit from a share.", "links": []},
    "q-pt-late": {"short": "Joins late", "label": "Partners join at different times", "kind": "qtype", "parent": "c-late-entry", "order": 1,
                  "summary": "Two or three partners; some join after some months.", "links": []},
    "q-pt-working": {"short": "Extra % for work", "label": "One partner works for extra %", "kind": "qtype", "parent": "c-working-partner", "order": 1,
                     "summary": "A working partner takes a % of profit first, then shares the rest.", "links": []},
    "q-pt-pasture": {"short": "Pasture / rent", "label": "Pasture / rent with animal equivalence", "kind": "qtype", "parent": "c-common-unit", "order": 1,
                     "summary": "Different animals for different months; convert to one animal, then split rent.", "links": ["ratio-proportion"]},
}

# ----------------------------------------------------------------------------------------------
# Formulas
# ----------------------------------------------------------------------------------------------
FORMULAS = [
    {"id": "pt-f1", "node": "c-capital-time", "text": "Profit ratio = (C₁×T₁) : (C₂×T₂) : …   (capital × time, i.e. 'capital-months')",
     "note": "Equal time → ratio of capitals. Equal capital → ratio of times."},
    {"id": "pt-f2", "node": "c-capital-time", "text": "Partner's share = (his capital-months ÷ total capital-months) × total profit"},
    {"id": "pt-f3", "node": "c-capital-time", "text": "Total profit = known share × (sum of ratio parts) ÷ (his ratio part)",
     "note": "For questions that give one partner's share and ask for the total."},
    {"id": "pt-f4", "node": "c-late-entry", "text": "Joins after m months (of a 12-month year) → invests for (12 − m) months",
     "note": "'At the end of 7 months' means he is in for the remaining 5 months."},
    {"id": "pt-f5", "node": "c-late-entry", "text": "Capital that changes: add up (capital × months at that capital) for each stretch",
     "note": "A withdrawal after 4 months of ₹20,000 from ₹80,000 → 80,000×4 + 60,000×8."},
    {"id": "pt-f6", "node": "c-working-partner", "text": "Working partner's total = commission + his ratio share of the balance, where balance = profit − commission",
     "note": "The commission comes out before the ratio split. Never take his ratio share of the full profit."},
    {"id": "pt-f7", "node": "c-common-unit", "text": "If a animals of type A eat as much as b animals of type B, then 1 A = (b/a) B",
     "note": "3 cows = 7 goats means a cow counts as 7/3 goat (a cow is the bigger eater)."},
    {"id": "pt-f8", "node": "c-common-unit", "text": "Rent share ∝ (number of animals × months), after converting every animal to one common unit"},
]

# ----------------------------------------------------------------------------------------------
# Methods for each question type
# ----------------------------------------------------------------------------------------------
METHODS = {
    "q-pt-two": {
        "cue": "Two or three people put in money for stated times and share a profit, or one person's share is given and the total profit is asked.",
        "formulas": ["pt-f1", "pt-f2", "pt-f3"],
        "tech": ["ratio-parts", "cancel-first", "bounds"],
        "standard": "Multiply each partner's capital by his months. Write the ratio, add the parts, take his part ÷ total × profit. For 'find total profit', divide the known share by his fraction.",
        "fast": "Cancel common factors before multiplying: 90,000×8 : 1,50,000×5 → 9×8 : 15×5 = 72 : 75 = 24 : 25. Drop zeros and common factors first, then work with the small numbers.",
        "ultra": "Profit ÷ (sum of parts) first, then multiply by his part: 50,000 ÷ 49 ≈ 1,020 → ×25 ≈ 25,510. If the given share divides exactly by his ratio part (18,900 ÷ 7 = 2,700) your ratio is almost certainly right.",
        "eliminate": "(1) Compare the capital-months roughly: 7,20,000 against 7,50,000 are close, so Q gets just over half of 50,000 (about 25,000 to 26,000). Only ₹25,510 is that close; ₹32,000 and ₹35,000 are far too big. (2) When the numbers are nice, a share is a whole multiple of profit ÷ sum of parts: 60,000 ÷ 5 = 12,000, so only ₹24,000 can be P's share.",
        "traps": ["Ignoring time and splitting by capital alone.", "Giving the answer for the wrong partner (read who the question asks for).", "In 'find total profit', multiplying by the wrong fraction (use his part, not the other partner's)."],
    },
    "q-pt-late": {
        "cue": 'Someone joins after some months, withdraws, or adds money part-way through the year.',
        "formulas": ["pt-f1", "pt-f4", "pt-f5"],
        "tech": ["ratio-parts", "bounds"],
        "standard": "Find each partner's months in the business (12 − months before joining). Multiply capital × months, make the ratio, then share the profit.",
        "fast": "Put the capitals in thousands and divide the capital-months by a common factor: 1,200 : 1,050 : 1,000 → ÷50 → 24 : 21 : 20. Tushar = 20 of 65 parts = 4/13.",
        "ultra": "Reduce the final fraction before multiplying: 20/65 = 4/13, then 1,50,000 ÷ 13 ≈ 11,538 → ×4 = 46,154. Use 1/13 ≈ 0.0769 as a quick check.",
        "eliminate": "(1) Tushar has the smallest capital-months (1,000 against 1,200 and 1,050), so his share is under one third of 1,50,000, which is ₹50,000. That drops ₹55,000. (2) The three are nearly equal, so he gets about 30%, around ₹45,000. That drops ₹35,500. (3) Between ₹46,154 and ₹45,250: the fraction 4/13 does not divide 1,50,000 evenly, so the exact answer is not a round number, which points to ₹46,154.",
        "traps": ["Counting months before joining instead of months after (joined at month 5 → he stays 7 months, not 5).", "Forgetting that the founder stays all 12 months.", "Using capitals only."],
    },
    "q-pt-working": {
        "cue": "One partner also 'works' or 'manages' the business and gets a percentage of the profit extra.",
        "formulas": ["pt-f6", "pt-f2"],
        "tech": ["bounds", "fraction-percent"],
        "standard": "Take the working partner's % off the profit first. Share the balance in the investment ratio. His total = commission + his share of the balance.",
        "fast": "Total fraction = c% + (1 − c%) × his ratio part. For 15% and 2 : 7 → 0.15 + 0.85 × 2/9 = 0.3389. Then × profit.",
        "ultra": "Choose the split that divides cleanly: 81,000 is a multiple of 9, so 2/9 of the balance is easy. 68,850 ÷ 9 = 7,650 → ×2 = 15,300; add 12,150 → 27,450.",
        "eliminate": "Squeeze 2/9 between 1/5 and 1/4. Then M's total is between 15% + 0.85 × 20% = 32% of the profit (₹25,920) and 15% + 0.85 × 25% = 36.25% (₹29,363). Only ₹27,450 fits; ₹24,000, ₹30,000 and ₹33,000 are all outside.",
        "traps": ["Taking his ratio share of the full profit and then adding the commission (double counting).", "Taking the commission as a % of his own share instead of the whole profit.", "Forgetting to add the commission to his total."],
    },
    "q-pt-pasture": {
        "cue": "Different animals kept for different months by different people, one rent shared, and an equivalence such as '3 cows = 7 goats'.",
        "formulas": ["pt-f7", "pt-f8", "pt-f1"],
        "tech": ["common-unit", "estimate"],
        "standard": "Pick one animal as the standard. Convert every other animal using the given equivalence. Multiply animals × months for each person, then split the rent in that ratio.",
        "fast": "Pick the unit so that every equivalent becomes a whole number. 2 oxen = 5 goats and 3 goats = 4 sheep → in 'thirds of a sheep': ox = 10, goat = 4, sheep = 3. Then no fractions appear anywhere.",
        "ultra": "After converting, cancel the common factor of the two totals: 1,140 : 1,212 → ÷12 → 95 : 101. Fraction = 95/196. Check the direction first: 3 cows = 7 goats means 1 cow = 7/3 goat, not the other way round.",
        "eliminate": "Estimate the fraction: X's total ≈ 285, Y's ≈ 303, so X ≈ 285/588 ≈ 0.485, a little under half. Any option above ½ or far below it is out. This leaves 90/196 (0.459) and 95/196 (0.485), and one rough division settles it.",
        "traps": ["Reading the equivalence upside down (cow worth 3/7 goat instead of 7/3).", "Leaving one animal type out of a person's total.", "Using animals but not months."],
    },
}


# ----------------------------------------------------------------------------------------------
# PYQs
# ----------------------------------------------------------------------------------------------
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
PYQS = [
    pyq(S1, 51, "q-pt-two", "P puts in ₹90,000 for 8 months and Q puts in ₹1,50,000 for 5 months. Profit is ₹50,000. Find Q's share (approximate).",
        ["₹20,000", "₹32,000", "₹35,000", "₹25,510"], "d",
        ["Capital-months: P = 90,000×8 = 7,20,000; Q = 1,50,000×5 = 7,50,000.", "Ratio 720 : 750 = 24 : 25.", "Q's share = 25/49 × 50,000 ≈ ₹25,510."],
        lambda: float(share([90000 * 8, 150000 * 5], 1, 50000)), 25510, 1,
        tech=["ratio-parts", "cancel-first", "bounds"], concepts=1, heavy=True,
        trick="Compare 7,20,000 with 7,50,000 first: nearly equal, so the answer is just over half of ₹50,000.",
        wrong={"a": bound("Q's capital-months (7,50,000) are larger than P's (7,20,000), so Q gets more than half of ₹50,000. ₹20,000 is below half.", lambda v: v < 25000),
               "b": bound("The two capital-months are within 4% of each other (24 : 25), so Q's share is only just over half. ₹32,000 would be 64%.", lambda v: v > 26500),
               "c": bound("Same reason: ₹35,000 would be 70% of the profit, far from a 24 : 25 split.", lambda v: v > 26500)}),
    pyq(S2, 61, "q-pt-two", "P and Q invest ₹50,000 and ₹75,000 for the same period. Find P's share of a ₹60,000 profit.",
        ["₹18,000", "₹22,000", "₹24,000", "₹26,000"], "c",
        ["Time is equal, so the ratio is the capital ratio 50 : 75 = 2 : 3.", "P's share = 2/5 × 60,000 = ₹24,000."],
        lambda: float(share([50000, 75000], 0, 60000)), 24000, 0,
        tech=["ratio-parts", "divisibility"], concepts=1, heavy=False,
        trick="2 : 3 means 5 equal parts of ₹12,000. P's share must be a multiple of ₹12,000, and only ₹24,000 is.",
        wrong={k: bound(f"2 : 3 makes 5 parts of ₹12,000 each, so P's share is a multiple of ₹12,000. {o} is not.", lambda v: v % 12000 != 0)
               for k, o in (("a", "₹18,000"), ("b", "₹22,000"), ("d", "₹26,000"))}),
    pyq(S3, 69, "q-pt-two", "C invests ₹1,40,000 for 9 months and D invests ₹1,80,000 for 8 months. C's share of profit is ₹18,900. Find the total profit.",
        ["₹40,500", "₹36,000", "₹34,200", "₹38,400"], "a",
        ["Capital-months: C = 1,40,000×9, D = 1,80,000×8 → 14×9 : 18×8 = 126 : 144 = 7 : 8.", "C has 7 of 15 parts. Total = 18,900 × 15 ÷ 7 = ₹40,500."],
        lambda: float(F(18900) / F(1260000, 1260000 + 1440000)), 40500, 0,
        tech=["ratio-parts", "divisibility", "back-substitute"], concepts=1, heavy=False,
        trick="C has 7 of 15 parts, so 18,900 ÷ 7 = 2,700 a part. The total is 15 × 2,700.",
        wrong={k: bound(f"With a total of {o}, C (7 of 15 parts) would get ₹{float(x) * 7 / 15:,.0f}, not ₹18,900.", lambda v: abs(v * 7 / 15 - 18900) > 1)
               for k, o, x in (("b", "₹36,000", 36000), ("c", "₹34,200", 34200), ("d", "₹38,400", 38400))}),
    pyq(S1, 52, "q-pt-late", "Rajesh starts with ₹1,00,000. Suresh joins after 5 months with ₹1,50,000. Tushar joins at the end of 7 months with ₹2,00,000. Yearly profit ₹1,50,000. Find Tushar's share (approximate).",
        ["₹55,000", "₹46,154", "₹45,250", "₹35,500"], "b",
        ["Months in business: Rajesh 12, Suresh 12 − 5 = 7, Tushar 12 − 7 = 5.", "Capital-months (in thousands): 100×12 : 150×7 : 200×5 = 1,200 : 1,050 : 1,000 = 24 : 21 : 20.", "Tushar = 20/65 = 4/13 of 1,50,000 ≈ ₹46,154."],
        lambda: float(share([100000 * 12, 150000 * 7, 200000 * 5], 2, 150000)), 46154, 1,
        tech=["ratio-parts", "bounds", "estimate"], concepts=2, heavy=True,
        trick="Three nearly equal capital-months with Tushar the smallest: expect just under a third of ₹1,50,000.",
        wrong={"a": bound("Tushar has the smallest capital-months (1,000 against 1,200 and 1,050), so he gets less than a third of ₹1,50,000, i.e. under ₹50,000.", lambda v: v > 50000),
               "c": bound("A near miss: ₹45,250 is 30.2% of the profit, but Tushar's fraction is 20/65 = 30.8%.", lambda v: abs(v - 150000 * 4 / 13) > 200),
               "d": bound("Tushar holds about 31% of the capital-months (1,000 of 3,250), so he gets over ₹45,000. ₹35,500 is only 24%.", lambda v: v < 40000)}),
    pyq(S2, 57, "q-pt-working", "M and N invest in the ratio 2 : 7 and earn ₹81,000. M works in the business and gets 15% of the profit extra. Find M's total share.",
        ["₹24,000", "₹27,450", "₹30,000", "₹33,000"], "b",
        ["Commission = 15% of 81,000 = ₹12,150. Balance = ₹68,850.", "M's part of the balance = 2/9 × 68,850 = ₹15,300.", "M's total = 12,150 + 15,300 = ₹27,450."],
        lambda: 0.15 * 81000 + float(F(2, 9)) * (81000 - 0.15 * 81000), 27450, 1e-6,
        tech=["bounds", "fraction-percent"], concepts=2, heavy=True,
        trick="Squeeze 2/9 between 1/5 and 1/4: M gets 15% + 0.85 × (20% to 25%) = 32% to 36% of ₹81,000.",
        wrong={"a": bound("M's total is at least 15% + 0.85 × 20% = 32% of the profit = ₹25,920. ₹24,000 is below that.", lambda v: v < 25920),
               "c": bound("M's total is at most 15% + 0.85 × 25% = 36.25% of the profit = ₹29,363. ₹30,000 is above that.", lambda v: v > 29363),
               "d": bound("Above the same ceiling of ₹29,363; ₹33,000 would be 41% of the profit.", lambda v: v > 29363)}),
    pyq(S3, 61, "q-pt-pasture", "X keeps 18 oxen for 5 months and 20 goats for 3 months. Y keeps 24 goats for 7 months and 30 sheep for 6 months. 2 oxen eat as much as 5 goats, and 3 goats as much as 4 sheep. What fraction of the rent does X pay?",
        ["90/196", "95/196", "10/196", "111/196"], "b",
        ["Use units of one-third sheep: sheep = 3, goat = 4 (3 goats = 4 sheep), ox = 10 (1 ox = 2.5 goats).", "X = 18×5×10 + 20×3×4 = 900 + 240 = 1,140. Y = 24×7×4 + 30×6×3 = 672 + 540 = 1,212.", "X : Y = 1,140 : 1,212 = 95 : 101, so X pays 95/196."],
        lambda: float(F(18 * 5 * 10 + 20 * 3 * 4, 18 * 5 * 10 + 20 * 3 * 4 + 24 * 7 * 4 + 30 * 6 * 3)), 95 / 196, 1e-12,
        tech=["common-unit", "ratio-parts", "estimate"], concepts=2, heavy=True, steps=6,
        trick="After converting, 1,140 : 1,212 is nearly 1 : 1, so X pays just under half. Cancel ÷12 to get 95 : 101.",
        wrong={"a": bound("A rough count puts X at 1,140 and Y at 1,212 units, so X pays about 48.5%. 90/196 is 45.9%.", lambda v: abs(v - 95 / 196) > 0.01),
               "c": bound("Both keep many animals for many months, so X pays close to half, not 5%.", lambda v: v < 0.3),
               "d": bound("X's total (1,140) is smaller than Y's (1,212), so X pays less than half. 111/196 is above half.", lambda v: v > 0.5)}),
    pyq(S3, 75, "q-pt-pasture", "M keeps 12 cows for 4 months and 18 goats for 5 months. N keeps 26 goats for 7 months. 3 cows are equivalent to 7 goats. Find M's share of the rent.",
        ["101/192", "110/192", "105/192", "60/192"], "a",
        ["Use units of one-third goat: goat = 3, cow = 7 (1 cow = 7/3 goat).", "M = 12×4×7 + 18×5×3 = 336 + 270 = 606. N = 26×7×3 = 546.", "M : N = 606 : 546 = 101 : 91, so M's share = 101/192."],
        lambda: float(F(12 * 4 * 7 + 18 * 5 * 3, 12 * 4 * 7 + 18 * 5 * 3 + 26 * 7 * 3)), 101 / 192, 1e-12,
        tech=["common-unit", "estimate"], concepts=2, heavy=False, steps=4,
        trick="Cow ≈ 2.3 goats, so M ≈ 112 + 90 = 202 against N = 182: M pays about 52.6%.",
        wrong={"b": bound("Estimate: a cow is about 2.3 goats, so M ≈ 202 and N = 182 goat-months, i.e. M ≈ 52.6%. 110/192 is 57%.", lambda v: v > 0.54),
               "c": bound("Same estimate gives about 52.6%; 105/192 is 54.7%.", lambda v: v > 0.54),
               "d": bound("M keeps more animals for more months than N's share would allow at 31%.", lambda v: v < 0.4)}),
]


# ----------------------------------------------------------------------------------------------
# Practice: main method first, then a second, different method as the check
# ----------------------------------------------------------------------------------------------
def month_sim(schedules, i, total):
    """Partner i's share when profit accrues month by month in proportion to the capital in play.
    schedules[j] lists partner j's capital (or animals, in one unit) for each month."""
    n = max(len(s) for s in schedules)
    cap = [list(s) + [0] * (n - len(s)) for s in schedules]
    return F(total) * F(sum(cap[i])) / F(sum(sum(c) for c in cap))


def month_sim_total(schedules, i, known_share):
    n = max(len(s) for s in schedules)
    cap = [list(s) + [0] * (n - len(s)) for s in schedules]
    return F(known_share) * F(sum(sum(c) for c in cap)) / F(sum(cap[i]))


def work_total(profit, comm, ratio, who):
    """Allocate the whole profit (commissions first, balance by ratio), check it adds back, return who's total."""
    bal = F(profit) - sum(F(c) * profit for c in comm.values())
    tot = [F(ratio[k]) / sum(map(F, ratio)) * bal + F(comm.get(k, 0)) * profit for k in range(len(ratio))]
    assert sum(tot) == profit, "allocation does not add back to the profit"
    return tot[who]


OTHER = "That is the other partner's share. Read who the question asks for."
CAPONLY = "Split by capital alone and ignored the time."
TIMEONLY = "Split by time alone and ignored the capital."
NOTADD = "Ignored the months the late partner was absent."


def _hand_items():
    out = []
    # ---------------- two partners ----------------
    cm = [60000 * 10, 80000 * 6]
    out.append(prac("q-pt-two", "same", "A puts in ₹60,000 for 10 months and B puts in ₹80,000 for 6 months. Profit is ₹36,000. Find A's share.",
                    share(cm, 0, 36000), [(share(cm, 1, 36000), OTHER), (share([60000, 80000], 0, 36000), CAPONLY), (share([10, 6], 0, 36000), TIMEONLY)],
                    "600 : 480 = 5 : 4, so A gets 5/9 of 36,000.", month_sim([[60000] * 10, [80000] * 6], 0, 36000), tech=["ratio-parts", "cancel-first"]))
    cm = [45000 * 8, 60000 * 9]
    out.append(prac("q-pt-two", "same", "X invests ₹45,000 for 8 months and Y invests ₹60,000 for 9 months. Y's share of the profit is ₹31,500. Find the total profit.",
                    F(31500) / F(cm[1], sum(cm)),
                    [(F(31500) / F(60000, 105000), "Used Y's capital share (4/7) instead of his capital-months share (3/5)."), (F(31500) / F(cm[0], sum(cm)), "Divided by X's fraction instead of Y's."), (F(31500) / F(9, 17), "Used the months alone (9 of 17).")],
                    "Capital-months 360 : 540 = 2 : 3. Y has 3 of 5 parts, so total = 31,500 × 5 ÷ 3.", month_sim_total([[45000] * 8, [60000] * 9], 1, 31500), tech=["ratio-parts", "divisibility"]))
    out.append(prac("q-pt-two", "same", "A, B and C invest ₹36,000, ₹54,000 and ₹90,000 for the same year. Profit is ₹1,08,000. Find C's share.",
                    share([36, 54, 90], 2, 108000), [(share([36, 54, 90], 1, 108000), OTHER), (share([36, 54, 90], 0, 108000), OTHER), (F(108000, 3), "Split equally between the three partners.")],
                    "36 : 54 : 90 = 2 : 3 : 5, so C gets 5/10 of the profit.", month_sim([[36000] * 12, [54000] * 12, [90000] * 12], 2, 108000), tech=["ratio-parts", "cancel-first"]))
    cm = [80000 * 4 + 60000 * 8, 70000 * 12]
    out.append(prac("q-pt-two", "harder", "A starts with ₹80,000 and withdraws ₹20,000 after 4 months. B keeps ₹70,000 in for the whole year. Profit is ₹82,000. Find A's share.",
                    share(cm, 0, 82000),
                    [(share([80000 * 12, 70000 * 12], 0, 82000), "Ignored the withdrawal and used ₹80,000 for all 12 months."), (share([cm[1], cm[0]], 0, 82000), "Swapped the two partners' capital-months."),
                     (share([80000 * 8 + 60000 * 4, 70000 * 12], 0, 82000), "Put the withdrawal at the wrong end: 8 months at ₹80,000 and 4 at ₹60,000.")],
                    "A: 80,000×4 + 60,000×8 = 8,00,000. B: 70,000×12 = 8,40,000. Ratio 20 : 21, so A gets 20/41.", month_sim([[80000] * 4 + [60000] * 8, [70000] * 12], 0, 82000), tech=["ratio-parts"]))
    # ---------------- late entry ----------------
    cm = [50000 * 12, 60000 * 9]
    out.append(prac("q-pt-late", "same", "A starts with ₹50,000. After 3 months B joins with ₹60,000. At the end of the year the profit is ₹57,000. Find A's share.",
                    share(cm, 0, 57000), [(share([50000 * 12, 60000 * 3], 0, 57000), NOTADD + " B was in for 3 months, not 9."), (share(cm, 1, 57000), OTHER), (share([50000, 60000], 0, 57000), CAPONLY)],
                    "A: 50×12 = 600. B: 60×9 = 540. Ratio 10 : 9, so A gets 10/19.", month_sim([[50000] * 12, [0] * 3 + [60000] * 9], 0, 57000), tech=["ratio-parts", "cancel-first"]))
    cm = [40000 * 12, 50000 * 8, 80000 * 6]
    out.append(prac("q-pt-late", "same", "A invests ₹40,000. B joins after 4 months with ₹50,000 and C joins after 6 months with ₹80,000. Yearly profit is ₹1,02,000. Find B's share.",
                    share(cm, 1, 102000),
                    [(share(cm, 2, 102000), OTHER), (share([40000 * 12, 50000 * 4, 80000 * 6], 1, 102000), "Counted the 4 months before joining instead of the 8 after."), (share([40000 * 12, 50000 * 7, 80000 * 5], 1, 102000), "Used 7 months for B and 5 for C: mixed up the two joining times.")],
                    "480 : 400 : 480 = 6 : 5 : 6 (in thousands). B has 5 of 17 parts.", month_sim([[40000] * 12, [0] * 4 + [50000] * 8, [0] * 6 + [80000] * 6], 1, 102000), tech=["ratio-parts", "cancel-first"]))
    cm = [30000 * 12, 20000 * 12, 40000 * 6]
    out.append(prac("q-pt-late", "same", "A and B start with ₹30,000 and ₹20,000. After 6 months C joins with ₹40,000. Year-end profit is ₹70,000. Find B's share.",
                    share(cm, 1, 70000), [(share(cm, 0, 70000), OTHER), (share([30000, 20000, 40000], 1, 70000), CAPONLY), (share([30000 * 12, 20000 * 12, 40000 * 5], 1, 70000), "Gave C 5 months instead of 6.")],
                    "360 : 240 : 240 = 3 : 2 : 2, so B gets 2/7 of 70,000.", month_sim([[30000] * 12, [20000] * 12, [0] * 6 + [40000] * 6], 1, 70000), tech=["ratio-parts"]))
    x = F(120000 * 12, 2 * 9)
    out.append(prac("q-pt-late", "harder", "A starts with ₹1,20,000. After 3 months B joins with some capital. At year end the profit is shared 2 : 1 between A and B. Find B's investment.",
                    x, [(F(120000, 2), "Halved A's capital and ignored time."), (F(120000 * 12, 2 * 3), "Gave B 3 months instead of 9."), (F(2 * 120000 * 12, 9), "Multiplied by 2 instead of dividing: the ratio is A : B = 2 : 1, so B's part is the smaller one.")],
                    "A : B = 1,20,000×12 : x×9 = 2 : 1, so 9x = 7,20,000 and x = 80,000.",
                    x if month_sim([[120000] * 12, [0] * 3 + [int(x)] * 9], 0, 300) == 2 * month_sim([[120000] * 12, [0] * 3 + [int(x)] * 9], 1, 300) else None, tech=["ratio-parts"]))
    # ---------------- working partner ----------------
    out.append(prac("q-pt-working", "same", "P and Q invest in the ratio 3 : 5 and earn ₹96,000. P works and gets 10% of the profit extra. Find P's total.",
                    F(10, 100) * 96000 + F(3, 8) * (96000 * F(9, 10)),
                    [(F(10, 100) * 96000 + F(3, 8) * 96000, "Took the ratio share of the full profit and added the commission (double counting)."), (F(3, 8) * 96000, "Forgot the commission."), (F(3, 8) * 96000 * F(9, 10), "Forgot to add the commission to P's share of the balance.")],
                    "Commission 9,600. Balance 86,400. P's part of the balance = 3/8 × 86,400 = 32,400. Total 42,000.", work_total(96000, {0: F(1, 10)}, [3, 5], 0), tech=["fraction-percent"]))
    out.append(prac("q-pt-working", "same", "A invests ₹40,000 and B invests ₹60,000. A manages the business and gets 20% of the profit. Profit is ₹50,000. Find A's total.",
                    F(2, 10) * 50000 + F(2, 5) * 40000,
                    [(F(2, 10) * 50000 + F(2, 5) * 50000, "Took A's share of the full profit and added the commission."), (F(2, 5) * 50000, "Forgot the commission."), (F(2, 5) * 40000, "Forgot to add the commission to A's share of the balance.")],
                    "Commission 10,000. Balance 40,000 split 2 : 3, so A gets 16,000. Total 26,000.", work_total(50000, {0: F(1, 5)}, [2, 3], 0), tech=["fraction-percent"]))
    prof = F(33000) / (F(3, 4) * F(88, 100))
    out.append(prac("q-pt-working", "same", "A and B invest in the ratio 1 : 3. A works and gets 12% of the profit extra. B's share is ₹33,000. Find the total profit.",
                    prof, [(F(33000) / F(3, 4), "Forgot that the balance is only 88% of the profit."), (F(33000) / F(88, 100), "Forgot that B has only 3/4 of the balance."), (F(33000) / F(3, 4) * F(112, 100), "Added the 12% instead of taking it off.")],
                    "B gets 3/4 of the balance, which is 88% of the profit: 0.75 × 0.88 = 0.66. Profit = 33,000 ÷ 0.66 = 50,000.",
                    prof if work_total(prof, {0: F(12, 100)}, [1, 3], 1) == 33000 else None, tech=["fraction-percent"]))
    out.append(prac("q-pt-working", "harder", "A, B and C invest in the ratio 2 : 3 : 5. A and B work and get 5% and 7% of the profit respectively. Profit is ₹1,00,000. Find B's total.",
                    7000 + F(3, 10) * (100000 - 12000),
                    [(7000 + F(3, 10) * 100000, "Took B's share of the full profit."), (F(3, 10) * 88000, "Forgot B's own commission."), (7000 + F(3, 10) * (100000 - 5000), "Took off A's commission only, not B's.")],
                    "Commissions 5,000 + 7,000 = 12,000. Balance 88,000. B's part = 3/10 × 88,000 = 26,400. Total 33,400.", work_total(100000, {0: F(5, 100), 1: F(7, 100)}, [2, 3, 5], 1), tech=["fraction-percent"]))
    # ---------------- pasture ----------------
    out.append(prac("q-pt-pasture", "same", "P keeps 20 sheep for 6 months and Q keeps 18 sheep for 5 months. The rent is ₹8,400. Find Q's share.",
                    share([20 * 6, 18 * 5], 1, 8400), [(share([20 * 6, 18 * 5], 0, 8400), OTHER), (share([20, 18], 1, 8400), "Counted animals only, ignored the months."), (share([6, 5], 1, 8400), "Counted months only, ignored the animals.")],
                    "120 : 90 = 4 : 3, so Q pays 3/7 of 8,400.", month_sim([[20] * 6, [18] * 5], 1, 8400), tech=["ratio-parts"]))
    out.append(prac("q-pt-pasture", "same", "X keeps 8 horses for 3 months and 10 cows for 4 months. Y keeps 12 cows for 5 months. 2 horses eat as much as 3 cows. The rent is ₹6,800. Find X's share.",
                    share([F(3, 2) * 8 * 3 + 40, 60], 0, 6800),
                    [(share([8 * 3 + 40, 60], 0, 6800), "Treated a horse and a cow as the same."), (share([F(2, 3) * 8 * 3 + 40, 60], 0, 6800), "Read the equivalence upside down: a horse is 3/2 cow, not 2/3."), (share([F(3, 2) * 8 * 3 + 40, 60], 1, 6800), OTHER)],
                    "1 horse = 3/2 cow. X = 8×3×1.5 + 10×4 = 76 cow-months. Y = 60. X pays 76/136 of 6,800.", month_sim([[8 * 3 + 10 * 2] * 3 + [10 * 2] * 1, [12 * 2] * 5], 0, 6800), tech=["common-unit"]))
    out.append(prac("q-pt-pasture", "same", "A keeps 12 cows for 5 months, B keeps 18 goats for 6 months and C keeps 8 cows for 9 months. 3 cows eat as much as 5 goats. Total rent is ₹16,400. Find B's share.",
                    share([12 * 5 * F(5, 3), 18 * 6, 8 * 9 * F(5, 3)], 1, 16400),
                    [(share([12 * 5, 18 * 6, 8 * 9], 1, 16400), "Treated cows and goats as the same."), (share([12 * 5 * F(3, 5), 18 * 6, 8 * 9 * F(3, 5)], 1, 16400), "Read the equivalence upside down: a cow is 5/3 goat."), (share([12 * 5 * F(5, 3), 18 * 6, 8 * 9 * F(5, 3)], 0, 16400), OTHER)],
                    "1 cow = 5/3 goat. A = 100, B = 108, C = 120 goat-months. B pays 108/328.", month_sim([[12 * 5] * 5, [18 * 3] * 6, [8 * 5] * 9], 1, 16400), tech=["common-unit"]))
    out.append(prac("q-pt-pasture", "harder", "X keeps 6 cows for 4 months and 12 goats for 3 months. Y keeps 20 sheep for 6 months. 2 cows eat as much as 5 goats, and 3 goats as much as 4 sheep. The rent is ₹18,600. Find X's share.",
                    share([6 * 4 * F(5, 2) + 12 * 3, 20 * 6 * F(3, 4)], 0, 18600),
                    [(share([6 * 4 + 12 * 3, 20 * 6], 0, 18600), "Treated all three animals as the same."), (share([6 * 4 * F(5, 2) + 12 * 3, 20 * 6 * F(4, 3)], 0, 18600), "Used the sheep equivalence upside down: a sheep is 3/4 goat."), (share([6 * 4 * F(5, 2) + 12 * 3, 20 * 6 * F(3, 4)], 1, 18600), OTHER)],
                    "In goats: X = 24 × 2.5 + 36 = 96; Y = 120 × 0.75 = 90. X pays 96/186 of 18,600.", month_sim([[6 * 10 + 12 * 4] * 3 + [6 * 10] * 1, [20 * 3] * 6], 0, 18600), tech=["common-unit"]))
    return out


# ----------------------------------------------------------------------------------------------
# Generated practice: each template draws clean numbers, builds the question, three named-mistake traps and
# a second-method check. tools/bank.variants() makes them deterministic and refuses unclean or colliding draws.
# ----------------------------------------------------------------------------------------------
def _names(rng, k):
    return rng.sample(["A", "B", "C", "P", "Q", "R", "X", "Y", "M", "N", "S", "T"], k)


def _parts(cm):
    g = 0
    for x in cm: g = gcd(g, int(x))
    return [int(x) // g for x in cm]


def _profit(rng, parts_sum, units):
    """A total that splits into whole rupees for the given ratio parts, and is not tiny."""
    u = rng.choice(units)
    return parts_sum * u * max(1, -(-12000 // (parts_sum * u)))


def t_two_share(rng):
    a, b = _names(rng, 2)
    c1, c2 = rng.choice([20, 25, 30, 40, 45, 50, 60, 75, 80, 90]), rng.choice([20, 25, 30, 40, 45, 50, 60, 75, 80, 90])
    m1, m2 = rng.randint(3, 12), rng.randint(3, 12)
    cm = [c1 * m1, c2 * m2]
    if c1 == c2 or m1 == m2 or cm[0] == cm[1]: return None
    pr = _parts(cm); profit = _profit(rng, sum(pr), [300, 500, 600, 1000, 1200]); who = rng.randint(0, 1); nm = (a, b)
    ans = share(cm, who, profit)
    return prac("q-pt-two", "same", f"{a} invests {inr(c1 * 1000)} for {m1} months and {b} invests {inr(c2 * 1000)} for {m2} months. The profit is {inr(profit)}. Find {nm[who]}'s share.",
                ans, [(share(cm, 1 - who, profit), "That is the other partner's share. Read who the question asks for."), (share([c1, c2], who, profit), "Split by capital alone and ignored the time."), (share([m1, m2], who, profit), "Split by time alone and ignored the capital.")],
                f"Capital-months (in thousands): {a} = {c1}×{m1} = {cm[0]}, {b} = {c2}×{m2} = {cm[1]}. Ratio {pr[0]} : {pr[1]}. {nm[who]} gets {pr[who]}/{sum(pr)} of {inr(profit)}.",
                month_sim([[c1 * 1000] * m1, [c2 * 1000] * m2], who, profit), tech=["ratio-parts", "cancel-first"])


def t_two_total(rng):
    c1, c2, t, d = rng.choice([40, 60, 80, 100, 120]), rng.choice([50, 60, 70, 90, 100]), rng.randint(3, 8), rng.choice([-30, -20, 20, 30, 40])
    if c1 + d <= 0: return None
    cmA, cmB = c1 * t + (c1 + d) * (12 - t), c2 * 12
    pr = _parts([cmA, cmB]); unit = rng.choice([400, 500, 800, 1000]); S, T = pr[1] * unit, sum(pr) * unit
    verb = "adds" if d > 0 else "withdraws"
    wrong1 = F(S) * (c1 * 12 + c2 * 12) / (c2 * 12)
    return prac("q-pt-two", "harder", f"A starts with {inr(c1 * 1000)} and {verb} {inr(abs(d) * 1000)} after {t} months. B keeps {inr(c2 * 1000)} for the whole year. B's share of the year's profit is {inr(S)}. Find the total profit.",
                F(T), [(wrong1, "Ignored the change in A's capital and used it for all 12 months."), (F(S) * sum(pr) / pr[0], "Used A's fraction instead of B's."), (F(S) * (c1 * (12 - t) + (c1 + d) * t + c2 * 12) / (c2 * 12), f"Swapped the stretches: used the new capital for {t} months and the old for {12 - t}.")],
                f"A: {c1}×{t} + {c1 + d}×{12 - t} = {cmA} (thousands). B: {c2}×12 = {cmB}. Ratio {pr[0]} : {pr[1]}. B has {pr[1]} of {sum(pr)} parts. Total = {S} × {sum(pr)} ÷ {pr[1]} = {T}.",
                month_sim_total([[c1 * 1000] * t + [(c1 + d) * 1000] * (12 - t), [c2 * 1000] * 12], 1, S), concepts=2, steps=5, tech=["ratio-parts"])


def t_late_share(rng):
    a, b = _names(rng, 2); c1, c2, m = rng.choice([30, 40, 50, 60, 75, 80]), rng.choice([40, 50, 60, 70, 90, 100]), rng.randint(2, 8)
    cm = [c1 * 12, c2 * (12 - m)]
    if cm[0] == cm[1] or c1 == c2: return None
    pr = _parts(cm); profit = _profit(rng, sum(pr), [500, 600, 1000, 1500]); who = rng.randint(0, 1); nm = (a, b)
    return prac("q-pt-late", "same", f"{a} starts a business with {inr(c1 * 1000)}. After {m} months {b} joins with {inr(c2 * 1000)}. The profit at the end of the year is {inr(profit)}. Find {nm[who]}'s share.",
                share(cm, who, profit), [(share(cm, 1 - who, profit), "That is the other partner's share."), (share([c1 * 12, c2 * m], who, profit), f"Gave {b} {m} months instead of {12 - m}."), (share([c1, c2], who, profit), "Split by capital alone.")],
                f"{a}: {c1}×12 = {cm[0]}. {b}: {c2}×{12 - m} = {cm[1]}. Ratio {pr[0]} : {pr[1]}. {nm[who]} gets {pr[who]}/{sum(pr)} of {inr(profit)}.",
                month_sim([[c1 * 1000] * 12, [0] * m + [c2 * 1000] * (12 - m)], who, profit), tech=["ratio-parts", "cancel-first"])


def t_late_unknown(rng):
    c1, x, m = rng.choice([40, 60, 80, 100, 120]), rng.choice([30, 40, 50, 60, 80, 90]), rng.randint(2, 8)
    cm = [c1 * 12, x * (12 - m)]; pr = _parts(cm)
    if pr[0] == pr[1] or max(pr) > 12: return None
    ok = month_sim([[c1 * 1000] * 12, [0] * m + [x * 1000] * (12 - m)], 0, 100 * sum(pr)) == F(pr[0]) * 100
    return prac("q-pt-late", "harder", f"A starts a business with {inr(c1 * 1000)}. After {m} months B joins with some capital. At the end of the year the profit is shared {pr[0]} : {pr[1]} between A and B. Find B's investment.",
                F(x * 1000), [(F(c1 * 1000 * pr[1], pr[0]), "Ignored the months: treated both as in for the full year."), (F(c1 * 12 * 1000 * pr[1], pr[0] * m), f"Used {m} months for B instead of {12 - m}."), (F(c1 * 12 * 1000 * pr[0], pr[1] * (12 - m)), "Inverted the ratio.")],
                f"A : B = {c1}×12 : x×{12 - m} = {pr[0]} : {pr[1]}. So x × {12 - m} × {pr[0]} = {c1 * 12} × {pr[1]}. B's months are {12 - m}, not {m}. x = {x} thousand, i.e. {inr(x * 1000)}.",
                F(x * 1000) if ok else None, concepts=2, steps=5, tech=["ratio-parts"])


def t_working_total(rng):
    r = rng.choice([(2, 3), (3, 5), (1, 3), (2, 7), (3, 4), (4, 5)]); c = rng.choice([5, 10, 12, 15, 20]); k = rng.randint(2, 9)
    profit = 1000 * sum(r) * k; w = rng.randint(0, 1); nm = rng.sample(["P", "Q", "A", "B", "X", "Y"], 2)
    comm = F(c, 100) * profit; bal = profit - comm; ans = comm + F(r[w], sum(r)) * bal
    return prac("q-pt-working", "same", f"{nm[0]} and {nm[1]} invest in the ratio {r[0]} : {r[1]} and earn {inr(profit)}. {nm[w]} works in the business and gets {c}% of the profit extra. Find {nm[w]}'s total.",
                ans, [(comm + F(r[w], sum(r)) * profit, "Took the ratio share of the full profit and added the commission (double counting)."), (F(r[w], sum(r)) * profit, "Forgot the commission."), (F(r[w], sum(r)) * bal, "Forgot to add the commission to the ratio share of the balance.")],
                f"Commission = {c}% of {profit} = {int(comm)}. Balance = {int(bal)}. {nm[w]}'s part = {r[w]}/{sum(r)} × {int(bal)} = {int(F(r[w], sum(r)) * bal)}. Total = {int(ans)}.",
                work_total(profit, {w: F(c, 100)}, list(r), w), tech=["fraction-percent"])


def t_working_find(rng):
    r = rng.choice([(2, 3, 5), (1, 2, 3), (3, 4, 5), (2, 2, 1), (1, 1, 2)]); x = rng.choice([4, 5, 8, 10, 12, 15]); k = rng.randint(3, 9)
    P = 100 * sum(r) * k * 10; S = F(r[2], sum(r)) * (P - F(x, 100) * P)
    frac = F(r[2], sum(r))
    return prac("q-pt-working", "harder", f"A, B and C invest in the ratio {r[0]} : {r[1]} : {r[2]}. A works in the business and gets {x}% of the profit extra. C's share is {inr(S)}. Find the total profit.",
                F(P), [(S / frac, "Forgot the commission and divided by C's fraction alone."), (S / (frac * (1 + F(x, 100))), "Added the commission instead of taking it off."), (S / frac * (1 - F(x, 100)), "Multiplied by (1 − commission) instead of dividing.")],
                f"C has {r[2]}/{sum(r)} of the balance. The balance is {100 - x}% of the profit. So C's share = {r[2]}/{sum(r)} × {100 - x}% × profit. Profit = {int(S)} ÷ ({r[2]}/{sum(r)} × {100 - x}/100). That gives {P}.",
                F(P) if work_total(P, {0: F(x, 100)}, list(r), 2) == S else None, concepts=2, steps=5, tech=["fraction-percent"])


_ONE = {"cows": "cow", "goats": "goat", "horses": "horse", "oxen": "ox", "sheep": "sheep", "buffaloes": "buffalo", "camels": "camel"}
_ANIMALS = [("cows", "goats"), ("horses", "cows"), ("oxen", "sheep"), ("buffaloes", "goats"), ("camels", "horses")]


def t_pasture_simple(rng):
    A, B = rng.choice(_ANIMALS); a, b = rng.choice([(2, 3), (3, 5), (3, 4), (2, 5), (3, 7), (4, 7), (5, 8)])
    n1, t1, n2, t2 = rng.randint(4, 20), rng.randint(2, 9), rng.randint(6, 30), rng.randint(2, 9)
    X, Y = n1 * t1 * b, n2 * t2 * a
    if X == Y: return None
    pr = _parts([X, Y]); rent = sum(pr) * rng.choice([200, 300, 400, 500]); n1_, n2_ = "X", "Y"
    return prac("q-pt-pasture", "same", f"X keeps {n1} {A} for {t1} months and Y keeps {n2} {B} for {t2} months in a field. {a} {A} eat as much as {b} {B}. The rent is {inr(rent)}. Find X's share.",
                share([X, Y], 0, rent), [(share([n1 * t1, n2 * t2], 0, rent), "Treated both animals as the same."), (share([n1 * t1 * a, n2 * t2 * b], 0, rent), "Read the equivalence upside down."), (share([X, Y], 1, rent), "That is Y's share.")],
                f"{a} {A} = {b} {B}, so use units where 1 {_ONE[A]} = {b} and 1 {_ONE[B]} = {a}. X = {n1}×{t1}×{b} = {X}. Y = {n2}×{t2}×{a} = {Y}. X pays {pr[0]}/{sum(pr)} of {inr(rent)}.",
                month_sim([[n1 * b] * t1, [n2 * a] * t2], 0, rent), tech=["common-unit", "ratio-parts"])


def t_pasture_chain(rng):
    a, b, c, d = rng.choice([2, 3, 4]), rng.choice([3, 5, 7]), rng.choice([2, 3, 4]), rng.choice([3, 4, 5, 7])
    n1, t1, n2, t2, n3, t3 = rng.randint(4, 12), rng.randint(2, 6), rng.randint(6, 20), rng.randint(2, 6), rng.randint(10, 30), rng.randint(3, 9)
    wA, wB, wC = b * d, a * d, a * c                              # a A = b B, c B = d C  ->  units of 1/(ac) of a C
    X = n1 * t1 * wA + n2 * t2 * wB; Y = n3 * t3 * wC
    if X == Y or a == b or c == d: return None
    pr = _parts([X, Y]); rent = sum(pr) * rng.choice([100, 200, 300])
    mon = lambda lst: [sum(n * w for (n, w, tt) in lst if i < tt) for i in range(max(tt for _, _, tt in lst))]
    return prac("q-pt-pasture", "harder", f"X keeps {n1} oxen for {t1} months and {n2} goats for {t2} months. Y keeps {n3} sheep for {t3} months. {a} oxen eat as much as {b} goats, and {c} goats as much as {d} sheep. The rent is {inr(rent)}. Find X's share.",
                share([X, Y], 0, rent), [(share([n1 * t1 + n2 * t2, n3 * t3], 0, rent), "Treated all three animals as the same."), (share([n1 * t1 * wB + n2 * t2 * wC, n3 * t3 * wC], 0, rent), "Used only the second equivalence for the oxen."), (share([X, Y], 1, rent), "That is Y's share.")],
                f"Units: sheep = {wC}, goat = {wB}, ox = {wA} (from {a} oxen = {b} goats and {c} goats = {d} sheep). X = {n1}×{t1}×{wA} + {n2}×{t2}×{wB} = {X}. Y = {n3}×{t3}×{wC} = {Y}. X pays {pr[0]}/{sum(pr)} of {inr(rent)}.",
                month_sim([mon([(n1, wA, t1), (n2, wB, t2)]), [n3 * wC] * t3], 0, rent), concepts=2, heavy=True, steps=6, tech=["common-unit", "ratio-parts"])


def practice_items():
    out = _hand_items()
    out += variants(PREFIX, "two-share", 2, t_two_share)
    out += variants(PREFIX, "two-total", 3, t_two_total)
    out += variants(PREFIX, "late-share", 2, t_late_share)
    out += variants(PREFIX, "late-unknown", 3, t_late_unknown)
    out += variants(PREFIX, "work-total", 2, t_working_total)
    out += variants(PREFIX, "work-find", 3, t_working_find)
    out += variants(PREFIX, "pasture-simple", 2, t_pasture_simple)
    out += variants(PREFIX, "pasture-chain", 3, t_pasture_chain)
    return out
