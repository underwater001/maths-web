#!/usr/bin/env python3
"""Partnership: the pilot topic's content (papers, nodes, formulas, methods, PYQs).

Built and verified by tools/build_partnership.py.

Every PYQ is stored as a condensed restatement (own words, same numbers) plus a pointer to the source
paper and question number; the source PDFs are not stored. Every PYQ answer and every practice answer
is recomputed here from the parameters of the question and compared with the keyed option.
"""
import json, os, random, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def inr(n):
    """Indian digit grouping: 1234567 -> 12,34,567."""
    n = int(round(n)); neg = n < 0; s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if neg else "") + "₹" + s


def share(cms, i, total):
    """Partner i's part of `total` when profit is shared in the ratio of capital-months `cms`."""
    return F(cms[i], sum(cms)) * total


# ----------------------------------------------------------------------------------------------
# Papers
# ----------------------------------------------------------------------------------------------
PAPERS = [
    {"id": "2025-09-12-S1", "exam": "SSC CGL Tier 1", "kind": "similar-paper", "publisher": "Adda247", "date": "2025-09-12", "shift": 1,
     "link": "https://drive.google.com/file/d/1fkM6ivOcsmfCOqyyY2L2hyHSlptncJ1G/view?usp=sharing", "quant": "Q51-Q75"},
    {"id": "2025-09-12-S2", "exam": "SSC CGL Tier 1", "kind": "similar-paper", "publisher": "Adda247", "date": "2025-09-12", "shift": 2,
     "link": "https://drive.google.com/file/d/1sj_z6jc-oEDs0gHYT8XWh0lzzr9QhEWC/view?usp=sharing", "quant": "Q51-Q75"},
    {"id": "2025-09-12-S3", "exam": "SSC CGL Tier 1", "kind": "similar-paper", "publisher": "Adda247", "date": "2025-09-12", "shift": 3,
     "link": "https://drive.google.com/file/d/1aXkj_ybp9ONrZajnBLiaEsHYYU4SprQk/view?usp=sharing", "quant": "Q51-Q75"},
]

# ----------------------------------------------------------------------------------------------
# Nodes (topic = partnership already exists in the seed tree)
# ----------------------------------------------------------------------------------------------
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
                 "summary": "Capitals and times given; find a share, or find the total profit from a share.", "links": [], "priority": "high"},
    "q-pt-late": {"short": "Joins late", "label": "Partners join at different times", "kind": "qtype", "parent": "c-late-entry", "order": 1,
                  "summary": "Two or three partners; some join after some months.", "links": [], "priority": "high"},
    "q-pt-working": {"short": "Extra % for work", "label": "One partner works for extra %", "kind": "qtype", "parent": "c-working-partner", "order": 1,
                     "summary": "A working partner takes a % of profit first, then shares the rest.", "links": [], "priority": "medium"},
    "q-pt-pasture": {"short": "Pasture / rent", "label": "Pasture / rent with animal equivalence", "kind": "qtype", "parent": "c-common-unit", "order": 1,
                     "summary": "Different animals for different months; convert to one animal, then split rent.", "links": ["ratio-proportion"], "priority": "medium"},
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
        "formulas": ["pt-f1", "pt-f2", "pt-f3"],
        "standard": "Multiply each partner's capital by his months. Write the ratio, add the parts, take his part ÷ total × profit. For 'find total profit', divide the known share by his fraction.",
        "fast": "Cancel common factors before multiplying: 90,000×8 : 1,50,000×5 → 9×8 : 15×5 = 72 : 75 = 24 : 25. Drop zeros and common factors first, then work with the small numbers.",
        "ultra": "Profit ÷ (sum of parts) first, then multiply by his part: 50,000 ÷ 49 ≈ 1,020 → ×25 ≈ 25,510. If the given share divides exactly by his ratio part (18,900 ÷ 7 = 2,700) your ratio is almost certainly right.",
        "eliminate": "(1) Compare the capital-months roughly: 7,20,000 against 7,50,000 are close, so Q gets just over half of 50,000 (about 25,000 to 26,000). Only ₹25,510 is that close; ₹32,000 and ₹35,000 are far too big. (2) When the numbers are nice, a share is a whole multiple of profit ÷ sum of parts: 60,000 ÷ 5 = 12,000, so only ₹24,000 can be P's share.",
        "traps": ["Ignoring time and splitting by capital alone.", "Giving the answer for the wrong partner (read who the question asks for).", "In 'find total profit', multiplying by the wrong fraction (use his part, not the other partner's)."],
    },
    "q-pt-late": {
        "formulas": ["pt-f1", "pt-f4", "pt-f5"],
        "standard": "Find each partner's months in the business (12 − months before joining). Multiply capital × months, make the ratio, then share the profit.",
        "fast": "Put the capitals in thousands and divide the capital-months by a common factor: 1,200 : 1,050 : 1,000 → ÷50 → 24 : 21 : 20. Tushar = 20 of 65 parts = 4/13.",
        "ultra": "Reduce the final fraction before multiplying: 20/65 = 4/13, then 1,50,000 ÷ 13 ≈ 11,538 → ×4 = 46,154. Use 1/13 ≈ 0.0769 as a quick check.",
        "eliminate": "(1) Tushar has the smallest capital-months (1,000 against 1,200 and 1,050), so his share is under one third of 1,50,000, which is ₹50,000. That drops ₹55,000. (2) The three are nearly equal, so he gets about 30%, around ₹45,000. That drops ₹35,500. (3) Between ₹46,154 and ₹45,250: the fraction 4/13 does not divide 1,50,000 evenly, so the exact answer is not a round number, which points to ₹46,154.",
        "traps": ["Counting months before joining instead of months after (joined at month 5 → he stays 7 months, not 5).", "Forgetting that the founder stays all 12 months.", "Using capitals only."],
    },
    "q-pt-working": {
        "formulas": ["pt-f6", "pt-f2"],
        "standard": "Take the working partner's % off the profit first. Share the balance in the investment ratio. His total = commission + his share of the balance.",
        "fast": "Total fraction = c% + (1 − c%) × his ratio part. For 15% and 2 : 7 → 0.15 + 0.85 × 2/9 = 0.3389. Then × profit.",
        "ultra": "Choose the split that divides cleanly: 81,000 is a multiple of 9, so 2/9 of the balance is easy. 68,850 ÷ 9 = 7,650 → ×2 = 15,300; add 12,150 → 27,450.",
        "eliminate": "Squeeze 2/9 between 1/5 and 1/4. Then M's total is between 15% + 0.85 × 20% = 32% of the profit (₹25,920) and 15% + 0.85 × 25% = 36.25% (₹29,363). Only ₹27,450 fits; ₹24,000, ₹30,000 and ₹33,000 are all outside.",
        "traps": ["Taking his ratio share of the full profit and then adding the commission (double counting).", "Taking the commission as a % of his own share instead of the whole profit.", "Forgetting to add the commission to his total."],
    },
    "q-pt-pasture": {
        "formulas": ["pt-f7", "pt-f8", "pt-f1"],
        "standard": "Pick one animal as the standard. Convert every other animal using the given equivalence. Multiply animals × months for each person, then split the rent in that ratio.",
        "fast": "Pick the unit so that every equivalent becomes a whole number. 2 oxen = 5 goats and 3 goats = 4 sheep → in 'thirds of a sheep': ox = 10, goat = 4, sheep = 3. Then no fractions appear anywhere.",
        "ultra": "After converting, cancel the common factor of the two totals: 1,140 : 1,212 → ÷12 → 95 : 101. Fraction = 95/196. Check the direction first: 3 cows = 7 goats means 1 cow = 7/3 goat, not the other way round.",
        "eliminate": "Estimate the fraction: X's total ≈ 285, Y's ≈ 303, so X ≈ 285/588 ≈ 0.485, a little under half. Any option above ½ or far below it is out. This leaves 90/196 (0.459) and 95/196 (0.485), and one rough division settles it.",
        "traps": ["Reading the equivalence upside down (cow worth 3/7 goat instead of 7/3).", "Leaving one animal type out of a person's total.", "Using animals but not months."],
    },
}

# ----------------------------------------------------------------------------------------------
# PYQs (condensed restatements with the original numbers) and their solutions
# ----------------------------------------------------------------------------------------------
def _pyq(paper, qno, qtype, text, options, key, solution, calc, expect, tol):
    """calc() recomputes the answer from the question's numbers; it must match `expect` (within tol)."""
    return {"id": f"{paper}-Q{qno}", "paper": paper, "qno": qno, "qtype": qtype, "text": text, "options": options, "key": key,
            "solution": solution, "_calc": calc, "_expect": expect, "_tol": tol}


S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
PYQS = [
    _pyq(S1, 51, "q-pt-two", "P puts in ₹90,000 for 8 months and Q puts in ₹1,50,000 for 5 months. Profit is ₹50,000. Find Q's share (approximate).",
         ["₹20,000", "₹32,000", "₹35,000", "₹25,510"], "d",
         ["Capital-months: P = 90,000×8 = 7,20,000; Q = 1,50,000×5 = 7,50,000.", "Ratio 720 : 750 = 24 : 25.", "Q's share = 25/49 × 50,000 ≈ ₹25,510."],
         lambda: float(share([90000 * 8, 150000 * 5], 1, 50000)), 25510, 1),
    _pyq(S2, 61, "q-pt-two", "P and Q invest ₹50,000 and ₹75,000 for the same period. Find P's share of a ₹60,000 profit.",
         ["₹18,000", "₹22,000", "₹24,000", "₹26,000"], "c",
         ["Time is equal, so the ratio is the capital ratio 50 : 75 = 2 : 3.", "P's share = 2/5 × 60,000 = ₹24,000."],
         lambda: float(share([50000, 75000], 0, 60000)), 24000, 0),
    _pyq(S3, 69, "q-pt-two", "C invests ₹1,40,000 for 9 months and D invests ₹1,80,000 for 8 months. C's share of profit is ₹18,900. Find the total profit.",
         ["₹40,500", "₹36,000", "₹34,200", "₹38,400"], "a",
         ["Capital-months: C = 1,40,000×9, D = 1,80,000×8 → 14×9 : 18×8 = 126 : 144 = 7 : 8.", "C has 7 of 15 parts. Total = 18,900 × 15 ÷ 7 = ₹40,500."],
         lambda: float(F(18900) / F(1260000, 1260000 + 1440000)), 40500, 0),
    _pyq(S1, 52, "q-pt-late", "Rajesh starts with ₹1,00,000. Suresh joins after 5 months with ₹1,50,000. Tushar joins at the end of 7 months with ₹2,00,000. Yearly profit ₹1,50,000. Find Tushar's share (approximate).",
         ["₹55,000", "₹46,154", "₹45,250", "₹35,500"], "b",
         ["Months in business: Rajesh 12, Suresh 12 − 5 = 7, Tushar 12 − 7 = 5.", "Capital-months (in thousands): 100×12 : 150×7 : 200×5 = 1,200 : 1,050 : 1,000 = 24 : 21 : 20.", "Tushar = 20/65 = 4/13 of 1,50,000 ≈ ₹46,154."],
         lambda: float(share([100000 * 12, 150000 * 7, 200000 * 5], 2, 150000)), 46154, 1),
    _pyq(S2, 57, "q-pt-working", "M and N invest in the ratio 2 : 7 and earn ₹81,000. M works in the business and gets 15% of the profit extra. Find M's total share.",
         ["₹24,000", "₹27,450", "₹30,000", "₹33,000"], "b",
         ["Commission = 15% of 81,000 = ₹12,150. Balance = ₹68,850.", "M's part of the balance = 2/9 × 68,850 = ₹15,300.", "M's total = 12,150 + 15,300 = ₹27,450."],
         lambda: 0.15 * 81000 + float(F(2, 9)) * (81000 - 0.15 * 81000), 27450, 1e-6),
    _pyq(S3, 61, "q-pt-pasture", "X keeps 18 oxen for 5 months and 20 goats for 3 months. Y keeps 24 goats for 7 months and 30 sheep for 6 months. 2 oxen eat as much as 5 goats, and 3 goats as much as 4 sheep. What fraction of the rent does X pay?",
         ["90/196", "95/196", "10/196", "111/196"], "b",
         ["Use units of one-third sheep: sheep = 3, goat = 4 (3 goats = 4 sheep), ox = 10 (1 ox = 2.5 goats).", "X = 18×5×10 + 20×3×4 = 900 + 240 = 1,140. Y = 24×7×4 + 30×6×3 = 672 + 540 = 1,212.", "X : Y = 1,140 : 1,212 = 95 : 101, so X pays 95/196."],
         lambda: float(F(18 * 5 * 10 + 20 * 3 * 4, 18 * 5 * 10 + 20 * 3 * 4 + 24 * 7 * 4 + 30 * 6 * 3)), 95 / 196, 1e-12),
    _pyq(S3, 75, "q-pt-pasture", "M keeps 12 cows for 4 months and 18 goats for 5 months. N keeps 26 goats for 7 months. 3 cows are equivalent to 7 goats. Find M's share of the rent.",
         ["101/192", "110/192", "105/192", "60/192"], "a",
         ["Use units of one-third goat: goat = 3, cow = 7 (1 cow = 7/3 goat).", "M = 12×4×7 + 18×5×3 = 336 + 270 = 606. N = 26×7×3 = 546.", "M : N = 606 : 546 = 101 : 91, so M's share = 101/192."],
         lambda: float(F(12 * 4 * 7 + 18 * 5 * 3, 12 * 4 * 7 + 18 * 5 * 3 + 26 * 7 * 3)), 101 / 192, 1e-12),
]

