"""Percentage: quiz tier."""
from bank import bound, mistake, pyq
from topics._pc_ry import PYQS_RY

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
    "c-pc-use": {"short": "% in situations", "label": "Percent in exams, income, votes and mixtures", "kind": "concept", "parent": TOPIC, "order": 3,
                 "summary": "The story gives percents of one whole. Work on a base of 100 (or the total), keep what does not change fixed, and add or subtract the percents.", "links": ["average", "mixture-alligation", "ratio-proportion"]},
    "q-pc-basic": {"short": "Equal percents", "label": "Percent equations: 'x% of A = y% of B'", "kind": "qtype", "parent": "c-pc-of", "order": 3,
                   "summary": "Two percents of two numbers are equal, or a number is x% of another; find the ratio or the percent.", "links": ["ratio-proportion"]},
    "q-pc-compare": {"short": "More / less than", "label": "A is x% more than B; how much is B less than A?", "kind": "qtype", "parent": "c-pc-change", "order": 3,
                     "summary": "Chains such as A is 40% more than B and B is 20% less than C; the reverse comparison; a number reduced and increased.", "links": ["ratio-proportion"]},
    "q-pc-price": {"short": "Price & consumption", "label": "Price change, consumption, expenditure and revenue", "kind": "qtype", "parent": "c-pc-change", "order": 4,
                   "summary": "Price rises or falls and the quantity bought changes; successive changes; 'buys more for the same money'.", "links": ["profit-loss"]},
    "q-pc-growth": {"short": "Population & depreciation", "label": "Population growth and depreciation", "kind": "qtype", "parent": "c-pc-change", "order": 5,
                    "summary": "A yearly rate applied n times, forwards (grows to) or backwards (was); a rate found from two values.", "links": ["si-ci"]},
    "q-pc-sets": {"short": "Pass / fail", "label": "Pass marks, pass and fail in two subjects", "kind": "qtype", "parent": "c-pc-use", "order": 1,
                  "summary": "Pass mark found from a shortfall; passed in one subject, in the other, in both; the percent who failed.", "links": []},
    "q-pc-income": {"short": "Income & savings", "label": "Spending, savings and what is left", "kind": "qtype", "parent": "c-pc-use", "order": 2,
                    "summary": "A person spends parts of his income in turn; find the income, the savings, or how the savings change when income and spending change.", "links": []},
    "q-pc-election": {"short": "Elections", "label": "Votes polled, majority and non-voters", "kind": "qtype", "parent": "c-pc-use", "order": 3,
                      "summary": "Two candidates share the valid votes; the margin is the difference of their percents.", "links": []},
    "q-pc-solution": {"short": "Mixtures by %", "label": "Percent of a substance in a mixture", "kind": "qtype", "parent": "c-pc-use", "order": 4,
                      "summary": "Water, milk, sugar, copper: add or remove one part and find the new quantity; mix two strengths.", "links": ["mixture-alligation"]},
    "q-pc-groups": {"short": "Groups & totals", "label": "Percent of groups added to give a total", "kind": "qtype", "parent": "c-pc-use", "order": 5,
                    "summary": "Boys and girls, men and women, sections of a class, each with its own percent; find the overall percent or the total.", "links": ["average"]},
}
FORMULAS = [
    {"id": "pc-f1", "node": "c-pc-of", "text": "x% of N = N × x ÷ 100     15⅓% = 46/300 = 23/150, 58⅓% = 7/12", "note": "Recognise the common fractions: 12½% = 1/8, 16⅔% = 1/6, 33⅓% = 1/3, 58⅓% = 7/12."},
    {"id": "pc-f2", "node": "c-pc-of", "text": "Increase in cost = (new rate − old rate) × quantity, with the quantity found first", "note": "Quantity = distance ÷ mileage."},
    {"id": "pc-f3", "node": "c-pc-change", "text": "New value = old × (1 + x/100); area scales as the square: (1 + x/100)² − 1", "note": "8% on a radius gives 1.08² = 1.1664 → 16.64%, not 8%."},
    {"id": "pc-f4", "node": "c-pc-change", "text": "Overall % change = (Σ part × part's % change) ÷ (Σ parts)", "note": "Use the ratio numbers as the parts. Falls count negative."},
    {"id": "pc-f5", "node": "c-pc-change", "text": "x% more going up ⇔ x/(100 + x) less coming down;  x% less ⇔ x/(100 − x) more", "note": "1/5 more ⇔ 1/6 less;  1/6 less ⇔ 1/5 more;  25% less ⇔ 33⅓% more."},
    {"id": "pc-f6", "node": "c-pc-change", "text": "Price up x%: cut consumption by x/(100 + x) × 100% to keep spending;  price down x%: raise it by x/(100 − x) × 100%", "note": "Same rule as pc-f5. Expenditure = price × quantity."},
    {"id": "pc-f7", "node": "c-pc-change", "text": "Two successive changes of a% and b%:  net = a + b + ab/100  (a fall is negative)", "note": "+20% then −20% = 20 − 20 − 4 = −4%. Equal rise and fall of x% always loses x²/100."},
    {"id": "pc-f8", "node": "c-pc-change", "text": "After n years at r%:  N × (1 ± r/100)ⁿ.  Years ago:  divide by (1 ± r/100)ⁿ", "note": "Spot cubes and squares: 1.1³ = 1.331, 0.9³ = 0.729, 1.2³ = 1.728, 1.04³ = 1.124864; 64000 = 40³ and 1.025 = 41/40."},
    {"id": "pc-f9", "node": "c-pc-use", "text": "Passed in A or B = A + B − both;  failed in both = 100 − (A + B − both)", "note": "Fail in a subject = 100 − pass in it. Pass mark = marks got + marks short."},
    {"id": "pc-f10", "node": "c-pc-use", "text": "Majority = (winner% − loser%) of the valid votes;  valid votes = votes polled = total voters − non-voters", "note": "In a two-candidate contest loser% = 100 − winner% of the polled votes."},
    {"id": "pc-f11", "node": "c-pc-use", "text": "Savings = Income − Expenditure;  take income as 100 (or the ratio numbers) and recompute both after the changes", "note": "Savings can change by far more than income does."},
    {"id": "pc-f12", "node": "c-pc-use", "text": "In a mixture, the part that does not change (milk, copper, dry matter, water in sugar solutions) is fixed; set it equal to the new % of the new total", "note": "Two strengths a% and b% mixed to c%:  quantity ratio = (b − c) : (c − a)."},
    {"id": "pc-f13", "node": "c-pc-use", "text": "Overall % = (Σ group size × group %) ÷ (Σ group sizes)", "note": "Use real or ratio sizes; never average the percents."},
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
    "q-pc-basic": {
        "cue": "'If x% of A = y% of B…', 'A is what percent of B', 'what percent of x is y', or a nested 'x% of y% of N'.",
        "formulas": ["pc-f1"], "tech": ["fraction-percent", "ratio-parts"],
        "standard": "Write the equation with 0.8A = 0.5B, so B/A = 80/50 = 1.6: B is 160% of A. For 'x% of A = y% of B' the ratio A : B is y : x.",
        "fast": "Cross-multiply the percents and read the ratio straight off: 30% of A = 25% of B gives A : B = 25 : 30 = 5 : 6.",
        "eliminate": "If the left side has the bigger percent, its number must be the smaller one. That removes half the options at once.",
        "traps": ["Putting the ratio the wrong way round (A : B instead of B : A).", "Dividing by 100 in only one place.", "Reading 'what percent of B is A' as A ÷ (A + B)."]},
    "q-pc-compare": {
        "cue": "'A is x% more than B and B is y% less than C', 'by how much percent is B less than A', 'a number reduced by x% becomes N'.",
        "formulas": ["pc-f5", "pc-f7"], "tech": ["multiplier", "ratio-parts"],
        "standard": "Take the base as 100. A = 140 when B = 100, B = 80 when C = 100, so A = 112 when C = 100. For the reverse comparison, divide the difference by the new base: 40 on 140 or 40 on 60.",
        "fast": "Write the percents as fractions and multiply: 7/5 × 4/5 = 28/25. For the reverse, 1/5 more ⇔ 1/6 less (x/(100 + x)).",
        "eliminate": "Going back from 'x% less' is always more than x% (the same difference on a smaller base), and from 'x% more' it is always less than x%. Options with the wrong side of x% are out.",
        "traps": ["Reversing a percent without changing the base (A is 25% less than B ⇒ B is 25% more than A).", "Adding the two percents of a chain (20% and 25% make 50%, not 45%).", "Taking the percent on the wrong quantity."]},
    "q-pc-price": {
        "cue": "'Price rises by x%… reduce consumption', 'revenue/expenditure changes', 'two successive increases', 'buy 5 kg more for ₹320'.",
        "formulas": ["pc-f6", "pc-f7", "pc-f5"], "tech": ["multiplier", "ratio-parts"],
        "standard": "Expenditure = price × quantity. Multiply the two multipliers: 0.75 × 1.3 = 0.975, a 2.5% fall. To hold spending after a 20% rise, quantity falls by 20/120 = 16⅔%. For 'buys more kg for ₹X': old price p, new price p', X/p' − X/p = extra kg.",
        "fast": "a + b + ab/100 for two changes (10, 10 gives 21). Spot 'x% rise ⇒ x/(100 + x) fall' straight: 25% up ⇒ 20% down, 20% up ⇒ 16⅔% down.",
        "eliminate": "A rise followed by an equal fall always loses, so 'no change' is wrong. After a price rise with a cut in use, the percent cut is less than the price rise.",
        "traps": ["Cutting consumption by the same percent as the price rise (20% rise ⇒ 20% cut).", "Adding percents of successive changes without the ab/100 term.", "Mixing up the old and new price in 'buys more for the same money'."]},
    "q-pc-growth": {
        "cue": "'Population increases by r% per annum', 'value depreciates', 'the population two years ago was…', 'rate of growth per annum'.",
        "formulas": ["pc-f8"], "tech": ["multiplier", "cancel-first"],
        "standard": "Forward: N × (1 + r)ⁿ, e.g. 50,000 × 1.04² = 54,080. Backward: divide by (1 ± r)ⁿ, e.g. 5,832 ÷ 0.9³ = 8,000. For the rate, take the n-th root of the ratio: (48,400/40,000)^½ = 1.1.",
        "fast": "Look for perfect powers: 64,000 = 40³ and 1.025 = 41/40, so the answer is 41³. 17,576 = 26³ and 1.04 = 26/25, so the earlier value is 25³.",
        "eliminate": "Growth gives a bigger number forward and a smaller one backward; depreciation the reverse. Of the options, only those on the correct side of the given value can work.",
        "traps": ["Multiplying simple interest style (N × r × n).", "Dividing instead of multiplying (or the other way) when going backward.", "Using (1 − r)ⁿ for growth."]},
    "q-pc-sets": {
        "cue": "'Passes in English and Maths… fail in both', 'must secure x% to pass; gets N and fails by M', 'boys and girls, % passed'.",
        "formulas": ["pc-f9", "pc-f1"], "tech": ["bounds"],
        "standard": "Pass mark = N + M, and this equals x% of the total, so total = (N + M) ÷ x%. With two subjects, passed in at least one = A + B − both; failed in both = 100 − that. For boys and girls, count the failures of each and divide by the total.",
        "fast": "Do it on a base of 100. 60 + 45 − 25 = 80 passed in at least one, so 20% failed in both.",
        "eliminate": "The percent who failed both cannot exceed the smaller of the two failure percents; the percent who passed both cannot exceed the smaller pass percent.",
        "traps": ["Using the marks got (not the pass mark) as x% of the total.", "Adding the two pass percents and forgetting to subtract the overlap.", "Mixing 'failed' with 'passed' when the question says fail."]},
    "q-pc-income": {
        "cue": "'spends x% on food, y% on rent… savings ₹N', 'gives 20% to elder son, 30% of the remaining…', 'income rises 20%, expenditure 10%: savings change'.",
        "formulas": ["pc-f11", "pc-f1"], "tech": ["multiplier", "ratio-parts"],
        "standard": "For 'remaining' chains, multiply: 0.8 × 0.7 × 0.9 = 0.504 of the income is left, so income = left ÷ 0.504. For changes in savings: take income 100, expenditure E, savings 100 − E; recompute after the changes and compare the savings.",
        "fast": "Savings % = 100 − (sum of the spending percents) when all are of the whole income. Build savings on a base of 100 (or 8 with a 5 : 3 ratio) so the arithmetic is whole numbers.",
        "eliminate": "Savings change by more than income does, and in the same direction when expenditure rises less than income. If the income rises more than spending, the percent rise in savings is larger than the percent rise in income.",
        "traps": ["Adding 20% + 30% + 10% when the later percents are of what remains.", "Applying the change to the savings directly instead of income and expenditure.", "Forgetting the unchanged portion."]},
    "q-pc-election": {
        "cue": "'two candidates, one got x% and won by N votes', 'y% of voters did not vote', 'three candidates'.",
        "formulas": ["pc-f10"], "tech": ["fraction-percent"],
        "standard": "With two candidates and no invalid votes, the loser has (100 − x)%, so the margin is (2x − 100)% of the votes polled. Margin = N gives the votes polled. Non-voters: the winner's and loser's percents are of the total voters, so use their difference directly.",
        "fast": "60% to win ⇒ margin 20% of the votes. 38% ⇒ margin 24%. Votes polled = margin ÷ margin%.",
        "eliminate": "The votes polled must exceed the margin, and the winner's votes must exceed half the votes polled. This cuts options that are too small.",
        "traps": ["Taking N as the margin of x% instead of (2x − 100)%.", "Dividing by the winner's percent instead of the margin's.", "Forgetting that non-voters are part of the total voters but not of the votes polled."]},
    "q-pc-solution": {
        "cue": "'a mixture contains 10% water… how much water must be added', 'fresh fruit has 68% water, dry fruit 20%', 'two solutions of 15% and 40% to give 30%'.",
        "formulas": ["pc-f12"], "tech": ["ratio-parts"],
        "standard": "Find the part that stays the same (milk, copper, dry matter, the water in a sugar solution). Make it equal to its new percent of the new total: 36 litres of milk = 80% of the new mixture ⇒ mixture = 45 litres, water added = 5 litres.",
        "fast": "For two strengths, alligation: ratio = (b − c) : (c − a) as the quantity of a and b. 15% and 40% to 30% ⇒ 10 : 15 = 2 : 3.",
        "eliminate": "Adding water lowers the strength, so the new total must exceed the old one; adding the pure part (sugar, glycerine) raises the strength. The amount added is always smaller than the new total.",
        "traps": ["Setting the added quantity equal to the new percent of the old total.", "Taking the fixed part as the changing one (for sugar added, water is fixed).", "Mixing up which strength gets which share in the alligation ratio."]},
    "q-pc-groups": {
        "cue": "'1100 boys and 900 girls, 50% of boys and 40% of girls passed', 'sections of 20 and 30 students', 'a capital invested at 3%, 5% and 11%'.",
        "formulas": ["pc-f13"], "tech": ["ratio-parts", "estimate"],
        "standard": "Convert each percent into a count for its group, add the counts, and divide by the total: (20 × 80% + 30 × 60%) ÷ 50 = 68%.",
        "fast": "The answer is a weighted average, so it lies between the smallest and largest group percents and is closer to the bigger group's.",
        "eliminate": "An answer outside the range of the group percents is impossible. With two groups, it must lie nearer the larger group's percent.",
        "traps": ["Averaging the percents without weights (80 + 60) ÷ 2 = 70.", "Using the percent of the wrong group.", "Computing the passed percent when the question asks for the failed."]},}


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

PYQS = PYQS + PYQS_RY


def practice_items():
    return []
