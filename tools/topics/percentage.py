"""Percentage: quiz tier."""
from bank import bound, mistake, pyq

TOPIC = "percentage"
PREFIX = "pc"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-pc-of": {"short": "% of a number", "label": "Percent of a quantity, in money and distance", "kind": "concept", "parent": TOPIC, "order": 1,
                "summary": "A percent is a fraction of 100. Turn each percent into a small fraction first and the arithmetic usually cancels.", "links": ["profit-loss"]},
    "c-pc-change": {"short": "% change", "label": "Percentage change", "kind": "concept", "parent": TOPIC, "order": 2,
                    "summary": "A change of x% is a multiplier of (1 + x/100). Chain multipliers; weight them by size when parts differ.", "links": ["mensuration-2d", "ratio-proportion"]},
    "q-pc-calc": {"short": "% of numbers", "label": "Sum of percentages of quantities", "kind": "qtype", "parent": "c-pc-of", "order": 1,
                  "summary": "Several percents of several amounts, added; or commissions on items sold.", "links": []},
    "q-pc-money": {"short": "Price and rent", "label": "Percent in a money story", "kind": "qtype", "parent": "c-pc-of", "order": 2,
                   "summary": "A return, a price rise or a running cost; find the monthly rent or the extra expenditure.", "links": []},
    "q-pc-area": {"short": "Area change", "label": "Percentage change of an area", "kind": "qtype", "parent": "c-pc-change", "order": 1,
                  "summary": "A length changes by x%; the area changes by (1 + x)² − 1.", "links": ["mensuration-2d"]},
    "q-pc-mix": {"short": "Weighted change", "label": "Overall change when parts change differently", "kind": "qtype", "parent": "c-pc-change", "order": 2,
                 "summary": "Spending in a ratio; each part rises or falls by its own %; find the overall change.", "links": ["ratio-proportion"]},
}
FORMULAS = [
    {"id": "pc-f1", "node": "c-pc-of", "text": "x% of N = N × x ÷ 100     15⅓% = 46/300 = 23/150, 58⅓% = 7/12", "note": "Recognise the common fractions: 12½% = 1/8, 16⅔% = 1/6, 33⅓% = 1/3, 58⅓% = 7/12."},
    {"id": "pc-f2", "node": "c-pc-of", "text": "Increase in cost = (new rate − old rate) × quantity, with the quantity found first", "note": "Quantity = distance ÷ mileage."},
    {"id": "pc-f3", "node": "c-pc-change", "text": "New value = old × (1 + x/100); area scales as the square: (1 + x/100)² − 1", "note": "8% on a radius gives 1.08² = 1.1664 → 16.64%, not 8%."},
    {"id": "pc-f4", "node": "c-pc-change", "text": "Overall % change = (Σ part × part's % change) ÷ (Σ parts)", "note": "Use the ratio numbers as the parts. Falls count negative."},
]
METHODS = {
    "q-pc-calc": {
        "cue": "'Evaluate x% of A + y% of B' or 'x% commission on …, y% commission on …'.",
        "formulas": ["pc-f1"], "tech": ["fraction-percent", "cancel-first"],
        "standard": "Convert each percent into a fraction and multiply: 15⅓% × 480 = 73.6 and 58⅓% × 300 = 175; add.",
        "fast": "58⅓% = 7/12 → 300 × 7/12 = 175 at once. 15⅓% of 480 = 480 × 46/300 = 73.6.",
        "eliminate": "Round: 15% of 480 ≈ 72 and 58% of 300 ≈ 174, total ≈ 246. Only 248.6 is near.",
        "traps": ["Reading 15⅓% as 15% + 3%.", "Doing one week's commission when the question asks for 5 weeks.", "Using the wrong price for the wrong item."]},
    "q-pc-money": {
        "cue": "A return on a purchase plus a running cost; or a price rise on fuel with distance and mileage given.",
        "formulas": ["pc-f2", "pc-f1"], "tech": ["fraction-percent", "units-first"],
        "standard": "Rent: 10% of 12,00,000 = 1,20,000 a year = 10,000 a month; add the 2,500 maintenance → 12,500. Diesel: litres = 2880 ÷ 12 = 240; rise = 6% of 85 = 5.10 a litre; 240 × 5.10 = 1,224.",
        "fast": "Do it per month and per litre from the start, then add or multiply once.",
        "eliminate": "The rent must exceed the pure return (10,000) because maintenance is added: options at or below ₹10,000 are out. For diesel, estimate 240 litres × 5 = 1,200.",
        "traps": ["Forgetting that 10% is for a year and not for a month.", "Leaving out the maintenance.", "Taking 6% of the total monthly bill instead of the rise per litre times the litres."]},
    "q-pc-area": {
        "cue": "A radius or side is increased or decreased by x%; the percentage change of the area is asked.",
        "formulas": ["pc-f3"], "tech": ["multiplier", "estimate"],
        "standard": "Area ∝ r². New area = 1.08² = 1.1664 times the old, so +16.64%.",
        "fast": "x% on a length gives about 2x% + x²/100 on the area: 8 + 8 + 0.64 = 16.64%.",
        "eliminate": "The area change is a little more than double the length change (16 + a bit). 8% (the same as the length) and 15% (below 16) are out.",
        "traps": ["Giving the same % for the area as for the radius.", "Doubling the % without the small x²/100 term (16%).", "Cubing it (volume)."]},
    "q-pc-mix": {
        "cue": "Spending in a ratio like 3 : 5 : 2; each part rises or falls by a different %; the overall change is asked.",
        "formulas": ["pc-f4"], "tech": ["ratio-parts", "estimate"],
        "standard": "Use 3, 5, 2 as amounts (total 10). New amounts: 3×1.08 + 5×1.04 + 2×0.90 = 3.24 + 5.20 + 1.80 = 10.24. Change = 0.24 on 10 = +2.4%.",
        "fast": "Net change in the parts: 3×8 + 5×4 − 2×10 = 24 + 20 − 20 = 24 per 10 parts → +2.4%.",
        "eliminate": "Rent is the biggest part (5) and rises by 4%, groceries rise by 8%, only the smallest part falls. The net must be an increase, so the two 'decrease' options go.",
        "traps": ["Averaging the three percentages (8 + 4 − 10) ÷ 3.", "Ignoring the ratio weights.", "Treating the 10% fall as a rise."]},
}


def _chg(t):
    v = float(t.split("%")[0]); return -v if "decrease" in t else v


OPT68 = ["1% decrease", "2.4% increase", "1.2% increase", "0.8% decrease"]
PYQS = [
    pyq(S1, 55, "q-pc-money", "A landlord bought a property for ₹12,00,000. He wants a 10% annual return on his investment after paying ₹2,500 a month for maintenance. What monthly rent should he charge?",
        ["₹9,500", "₹10,000", "₹12,500", "₹11,000"], "c",
        ["Yearly return = 10% of 12,00,000 = ₹1,20,000, which is ₹10,000 a month.", "Rent must also cover the ₹2,500 maintenance: 10,000 + 2,500 = ₹12,500."],
        lambda: 1200000 * 0.10 / 12 + 2500, 12500, 1e-9, tech=["fraction-percent"],
        trick="The pure return is ₹10,000 a month, and rent must be higher than that because maintenance comes on top.",
        wrong={"b": mistake("Only the return (₹10,000 a month) with the maintenance left out.", 10000), "a": bound("Rent must exceed the pure monthly return of ₹10,000.", lambda v: v <= 10000)}),
    pyq(S2, 64, "q-pc-money", "Diesel was ₹85 a litre and its price rose by 6%. A person drives 2,880 km a month and his vehicle gives 12 km a litre. Find the increase in his monthly fuel expenditure (to the nearest ₹).",
        ["₹1,224", "₹1,428", "₹1,530", "₹1,632"], "a",
        ["Litres used = 2,880 ÷ 12 = 240 a month.", "Price rise = 6% of 85 = ₹5.10 a litre.", "Extra cost = 240 × 5.10 = ₹1,224."],
        lambda: 85 * 0.06 * 2880 / 12, 1224, 1, tech=["fraction-percent", "units-first"],
        trick="240 litres × ₹5 is ₹1,200, so the answer is just above 1,200."),
    pyq(S3, 55, "q-pc-calc", "Evaluate: 15⅓% of 480 km + 58⅓% of 300 km.", ["266.6 km", "285.5 km", "248.6 km", "320 km"], "c",
        ["15⅓% = 46/300, so 480 × 46/300 = 73.6 km.", "58⅓% = 7/12, so 300 × 7/12 = 175 km.", "Total = 73.6 + 175 = 248.6 km."],
        lambda: (46 / 3 / 100) * 480 + (175 / 3 / 100) * 300, 248.6, 0.05, tech=["fraction-percent", "estimate"],
        trick="Round: 15% of 480 ≈ 72 and 58⅓% of 300 is exactly 175; the total is about 248."),
    pyq(S3, 56, "q-pc-calc", "A sales agent earns 3% commission on laptops priced at ₹40,000 each and 8% on printers priced at ₹8,000 each. In a week he sells 4 laptops and 10 printers. Find his total commission for 5 such weeks.",
        ["₹52,000", "₹50,400", "₹56,000", "₹51,200"], "c",
        ["Laptops: 4 × 40,000 × 3% = ₹4,800.", "Printers: 10 × 8,000 × 8% = ₹6,400.", "One week = ₹11,200, so 5 weeks = ₹56,000."],
        lambda: 5 * (4 * 40000 * 0.03 + 10 * 8000 * 0.08), 56000, 1e-6, tech=["cancel-first"], trick="A week is ₹11,200 and 5 weeks is 5 times it: an exact multiple of 5,600 (the weekly half).",
        wrong={"a": bound("One week is ₹11,200 and 5 weeks must be a multiple of ₹5,600; ₹52,000 is not.", lambda v: v % 5600 != 0), "b": bound("Five weeks of ₹11,200 must be a multiple of ₹5,600, which ₹50,400 is, but it is 4.5 weeks of earnings.", lambda v: v != 56000),
               "d": bound("Five weeks of ₹11,200 must be a multiple of ₹5,600; ₹51,200 is not.", lambda v: v % 5600 != 0)}),
    pyq(S3, 57, "q-pc-area", "The radius of a circular plate is increased by 8%. What is the approximate percentage increase in its area?", ["8%", "15%", "16.64%", "17.28%"], "c",
        ["Area ∝ r², so the area multiplier is 1.08² = 1.1664.", "Increase = 16.64%."],
        lambda: (1.08 ** 2 - 1) * 100, 16.64, 1e-9, tech=["multiplier", "estimate"], trick="8 + 8 + 8×8/100 = 16.64.",
        wrong={"a": mistake("Gave the radius change (8%) as the area change.", 8), "b": bound("Area change is a little over 2 × 8 = 16%, so 15% is too low.", lambda v: v < 16),
               "d": bound("The area change is 16.64%; 17.28% would need a 1.1728 multiplier.", lambda v: abs(v - 16.64) > 0.01)}),
    pyq(S3, 68, "q-pc-mix", "A family spends on groceries, rent and other expenses in the ratio 3 : 5 : 2. Next year groceries rise by 8%, rent by 4% and other expenses fall by 10%. What is the overall percentage change in total expenditure?",
        OPT68, "b",
        ["Use 3, 5, 2 as amounts (total 10).", "New amounts: 3 × 1.08 + 5 × 1.04 + 2 × 0.90 = 3.24 + 5.20 + 1.80 = 10.24.", "Change = 0.24 ÷ 10 = +2.4%, an increase."],
        lambda: (3 * 1.08 + 5 * 1.04 + 2 * 0.9 - 10) / 10 * 100, 2.4, 1e-9, tech=["ratio-parts", "sign-check"], concepts=2, heavy=False,
        optvals=[_chg(t) for t in OPT68], trick="Weighted: 3×8 + 5×4 − 2×10 = 24 over 10 parts → +2.4%.",
        wrong={"a": bound("The two rises (3 × 8 and 5 × 4 = 44) outweigh the fall (2 × 10 = 20), so the total rises. A decrease cannot be right.", lambda v: v < 0),
               "d": bound("The rises 3 × 8 + 5 × 4 = 44 outweigh the fall 2 × 10 = 20, so the total rises.", lambda v: v < 0)}),
]


def practice_items():
    return []
