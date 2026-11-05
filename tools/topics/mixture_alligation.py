"""Mixture and alligation: quiz tier."""
from bank import bound, mistake, pyq, ratio_val
from topics._mx_ry import PYQS_RY

TOPIC = "mixture-alligation"
PREFIX = "mx"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-mx-ratio": {"short": "Quantities", "label": "Mixtures of one liquid in another", "kind": "concept", "parent": TOPIC, "order": 1,
                   "summary": "Keep track of the part that does not change (the juice, or the milk-to-water balance) and let the other part move.", "links": ["ratio-proportion"]},
    "c-mx-cost": {"short": "Cost and alligation", "label": "Mixing at different prices", "kind": "concept", "parent": TOPIC, "order": 2,
                  "summary": "The mean price lies between the two prices. Alligation reads the ratio off the gaps to the mean.", "links": ["profit-loss", "average"]},
    "q-mx-add": {"short": "Add to change ratio", "label": "Add one liquid to change the ratio", "kind": "qtype", "parent": "c-mx-ratio", "order": 1,
                 "summary": "A mixture in a ratio; add water (or juice) until another ratio is reached.", "links": []},
    "q-mx-replace": {"short": "Remove and replace", "label": "Remove some mixture, replace with one liquid", "kind": "qtype", "parent": "c-mx-ratio", "order": 2,
                     "summary": "Some mixture is taken out and replaced by pure milk; the final ratio is known.", "links": []},
    "q-mx-profit": {"short": "Profit on a mix", "label": "Profit or loss on a mixed lot", "kind": "qtype", "parent": "c-mx-cost", "order": 1,
                    "summary": "Two lots at different costs are combined and sold at one rate.", "links": ["profit-loss"]},
    "q-mx-allig": {"short": "Alligation", "label": "Ratio or quantity from a target gain", "kind": "qtype", "parent": "c-mx-cost", "order": 2,
                   "summary": "A gain % on the mix fixes the mean cost; find the ratio of the two ingredients or how much of one to add.", "links": ["profit-loss"]},
    "q-mx-basic": {"short": "Parts of a mixture", "label": "How much of one ingredient is in a mixture", "kind": "qtype", "parent": "c-mx-ratio", "order": 3,
                   "summary": "Percent or ratio of an ingredient is given; find the quantity of the mixture or of the ingredient.", "links": ["percentage"]},
    "q-mx-repeat": {"short": "Repeated replacement", "label": "Remove and replace more than once", "kind": "qtype", "parent": "c-mx-ratio", "order": 4,
                    "summary": "The same fraction of the mixture is taken out and replaced again and again; the original liquid is multiplied by (1 − fraction) each time.", "links": []},
    "q-mx-vessels": {"short": "Mix two mixtures", "label": "Mixing two or more mixtures, vessels or alloys", "kind": "qtype", "parent": "c-mx-cost", "order": 3,
                     "summary": "Alloys or vessels in given ratios are mixed; find the mixing ratio for a target or the ratio in the final mixture.", "links": ["ratio-proportion"]},
}
FORMULAS = [
    {"id": "mx-f1", "node": "c-mx-ratio", "text": "In a ratio a : b of a 𝑇-litre mixture, first liquid = 𝑇a/(a + b), second = 𝑇b/(a + b)", "note": "50 L at 3 : 2 → 30 L juice and 20 L water."},
    {"id": "mx-f2", "node": "c-mx-ratio", "text": "After removing x of T and replacing: the unchanged liquid's amount = original × (1 − x/T)", "note": "Water 10 → 5 means the mixture was thinned to half: (1 − x/80) = 1/2."},
    {"id": "mx-f3", "node": "c-mx-cost", "text": "Cheaper : dearer = (dearer − mean) : (mean − cheaper)", "note": "The mean is the cost price of the mix, not the selling price."},
    {"id": "mx-f4", "node": "c-mx-cost", "text": "Cost of a mix = (q₁c₁ + q₂c₂) ÷ (q₁ + q₂)     Cost price from gain g%: CP = SP ÷ (1 + g/100)", "note": "Selling at ₹54 with 20% gain means CP = ₹45."},
    {"id": "mx-f5", "node": "c-mx-cost", "text": "Alligation on the share of one ingredient: Mixture 1 : Mixture 2 = (share₂ − target) : (target − share₁)", "note": "Milk shares 4/9 and 5/6, target 5/9 → 5/18 : 1/9 = 5 : 2. Works for prices, percents and carats too."},
    {"id": "mx-f6", "node": "c-mx-ratio", "text": "Repeated replacement of x from T, n times: left = original × (1 − x/T)ⁿ", "note": "60 kg, replace 6 kg three times: 60 × 0.9³ = 43.74 kg."},
    {"id": "mx-f7", "node": "c-mx-ratio", "text": "Adding one liquid: the other (unchanged) liquid stays fixed; set it equal to its new share", "note": "40 L at 10% water; 36 L milk must be 80% afterwards: total 45 L, so 5 L water added."},
]
METHODS = {
    "q-mx-add": {
        "cue": "'How much water must be added to change the ratio of … to …?'",
        "formulas": ["mx-f1"], "tech": ["ratio-parts", "back-substitute"],
        "standard": "Juice = 30 L stays. New ratio juice : water = 3 : 4 → water = 40 L. Added = 40 − 20 = 20 L.",
        "fast": "Keep the unchanged part fixed: 30 L is 3 parts, so 1 part = 10 L and 4 parts = 40 L of water.",
        "eliminate": "The new water is 40 L and the old was 20 L, so the answer is exactly the old water amount here (20). Any answer below 20 would leave the ratio too small.",
        "traps": ["Adding to the juice instead.", "Using the total 50 as one of the parts.", "Taking 4 − 2 = 2 parts as litres."]},
    "q-mx-replace": {
        "cue": "'Some quantity is removed and replaced with pure …; the new ratio is …'.",
        "formulas": ["mx-f2"], "tech": ["ratio-parts", "back-substitute"],
        "standard": "Water = 80 × 1/8 = 10 L. Final water is 1/16 of 80 = 5 L. Water halved, so half the mixture was replaced: 40 L.",
        "fast": "Follow the liquid that is not added (water): it falls from 10 to 5, i.e. by half. So half of the 80 L was replaced.",
        "eliminate": "Replaced amount x must satisfy 10 × (1 − x/80) = 5, so x is a whole fraction of 80. Of the options only 40 (1/2) gives a clean halving.",
        "traps": ["Following the milk instead of the water.", "Taking the difference 15 − 7 = 8 as the answer.", "Using the ratio parts as litres."]},
    "q-mx-profit": {
        "cue": "'She bought … litres at ₹… and … litres at ₹…, mixed them and sold at ₹…. Profit or loss?'",
        "formulas": ["mx-f4"], "tech": ["sign-check", "cancel-first"],
        "standard": "Cost = 30 × 50 + 20 × 55 = 1,500 + 1,100 = ₹2,600. Revenue = 50 × 54 = ₹2,700. Profit = ₹100.",
        "fast": "Mean cost = ₹52 a litre; selling at ₹54 gains ₹2 on each of 50 litres = ₹100.",
        "eliminate": "Mean cost lies between 50 and 55 (closer to 50), about ₹52. Selling at ₹54 is above that, so it is a profit: both 'Loss' options go.",
        "traps": ["Using the simple average (50 + 55) ÷ 2 = 52.5 as the cost.", "Forgetting the quantities.", "Mixing up profit and loss."]},
    "q-mx-allig": {
        "cue": "'Sold at ₹… gaining …% … what ratio / how many kg?'",
        "formulas": ["mx-f3", "mx-f4"], "tech": ["ratio-parts", "back-substitute"],
        "standard": "Spices at 80 and 160, sold at 140 with 25% profit: mean cost = 140 ÷ 1.25 = 112. Cheaper : dearer = (160 − 112) : (112 − 80) = 48 : 32 = 3 : 2. Wheat at 52 with 30 kg at 40, sold at 54 with 20% gain: mean = 45. 52x + 1,200 = 45(x + 30) gives x = 150/7 ≈ 21.4 kg.",
        "fast": "Alligation on the mean cost: the gap to the dearer one is the quantity of the cheaper one. Mean 112: gaps 48 (to 160) and 32 (to 80) → 3 : 2.",
        "eliminate": "The mean cost 112 is nearer ₹80 (gap 32) than ₹160 (gap 48), so the cheaper spice is the bigger share and the ratio cheaper : dearer is above 1 : 1. That removes 1 : 2.",
        "traps": ["Using the selling price 140 as the mean (gives 3 : 1).", "Reading the ratio the wrong way round.", "Dropping the gain % and taking the selling price as the cost."]},
    "q-mx-basic": {
        "cue": "'12% copper … how much alloy for 69 kg copper', or 'which container has the least milk'.",
        "formulas": ["mx-f1"], "tech": ["cancel-first", "ratio-parts", "fraction-percent"],
        "standard": "Quantity = part ÷ share: 69 ÷ 0.12 = 575 kg. For 'more spirit than water' in 3 : 2, the difference is 1 part, so 3 litres = 1 part and spirit = 9 litres.",
        "fast": "Use the share as a fraction (12% = 3/25: 69 × 25/3 = 575).",
        "eliminate": "The mixture is always larger than the ingredient, and the ingredient share is only a part of it.",
        "traps": ["Multiplying instead of dividing.", "Using the total parts instead of the difference of parts."]},
    "q-mx-repeat": {
        "cue": "'The process is repeated', 'again one-third of the mixture is extracted'.",
        "formulas": ["mx-f6"], "tech": ["multiplier", "ratio-parts"],
        "standard": "12 L of 60 L taken out each time: milk × 4/5 per round. After 2 rounds milk = 60 × 16/25 = 38.4 L and water 21.6 L: 16 : 9.",
        "fast": "Multiply the fraction left each round and square (or cube) it: (4/5)² = 16/25, so the ratio is 16 : 9.",
        "eliminate": "After n rounds the original liquid is (1 − f)ⁿ of the total, so test whether an option's share equals a power of a simple fraction.",
        "traps": ["Taking out 12 L twice as 24 L from the original milk (it ignores the water removed in round 2).", "Adding the fractions instead of multiplying."]},
    "q-mx-vessels": {
        "cue": "'In what ratio should the mixtures in two vessels be mixed to get …?' or 'equal quantities of all are mixed'.",
        "formulas": ["mx-f5", "mx-f1"], "tech": ["ratio-parts", "lcm-units"],
        "standard": "Convert each ratio to the share of one ingredient and use alligation: A = 4/9 milk, B = 5/6, target 5/9 → A : B = (5/6 − 5/9) : (5/9 − 4/9) = 5 : 2. For equal quantities, pick a common amount (e.g. 120 L of each) and add the parts.",
        "fast": "Put the shares over one denominator, subtract in the cross pattern and read the ratio off the gaps.",
        "eliminate": "The target share lies between the two shares, so the nearer vessel gets the larger quantity.",
        "traps": ["Using the raw ratios (4 : 5, 5 : 1) in the alligation instead of the shares.", "Reading A : B the wrong way round (the nearer one has more).", "Treating 'equal quantities' as equal parts of one ingredient."]},
}
OPT68 = ["3:2", "2:1", "1:2", "3:1"]
PYQS = [
    pyq(S1, 62, "q-mx-add", "A 50-litre mixture contains juice and water in the ratio 3 : 2. How much water (in litres) must be added to change the ratio of juice to water to 3 : 4?", ["12 litres", "15 litres", "18 litres", "20 litres"], "d",
        ["Juice = 50 × 3/5 = 30 L and water = 20 L.", "Juice stays 30 L. For 3 : 4 the water must be 30 × 4/3 = 40 L.", "Water to add = 40 − 20 = 20 L."],
        lambda: 30 * 4 / 3 - 20, 20, 1e-9, tech=["ratio-parts"], trick="Juice is 3 parts = 30 L, so a part is 10 L; 4 parts of water = 40 L, minus the 20 L already there."),
    pyq(S1, 63, "q-mx-profit", "Priya bought 30 litres of honey at ₹50 a litre and 20 litres at ₹55 a litre, mixed them and sold all of it at ₹54 a litre. What was her total profit or loss?",
        ["Loss of ₹60", "Profit of ₹100", "Profit of ₹120", "Loss of ₹120"], "b",
        ["Cost = 30 × 50 + 20 × 55 = 1,500 + 1,100 = ₹2,600.", "Revenue = 50 × 54 = ₹2,700.", "Profit = 2,700 − 2,600 = ₹100."],
        lambda: 50 * 54 - (30 * 50 + 20 * 55), 100, 1e-9, tech=["sign-check", "cancel-first"], trick="The mix costs about ₹52 a litre, so selling at ₹54 is a profit. Both loss options go.",
        wrong={"a": bound("The mean cost is ₹52, below the selling price ₹54, so this is a profit, not a loss.", lambda v: v < 0), "d": bound("The mean cost is ₹52, below the selling price ₹54, so this is a profit, not a loss.", lambda v: v < 0)}),
    pyq(S1, 68, "q-mx-allig", "Two spices priced at ₹80 and ₹160 a kg are blended and sold at ₹140 a kg, making a 25% profit. In what ratio were the spices mixed?", OPT68, "a",
        ["Cost price of the mix = 140 ÷ 1.25 = ₹112 a kg.", "Cheaper : dearer = (160 − 112) : (112 − 80) = 48 : 32 = 3 : 2."],
        lambda: ratio_val("48:32"), ratio_val("3:2"), 1e-9, tech=["ratio-parts"], optvals=[ratio_val(t) for t in OPT68],
        trick="Mean cost 112 is nearer 80, so more of the cheaper spice: ratio above 1.",
        wrong={"d": mistake("Used the selling price ₹140 as the mean: (140 − 80) : (160 − 140) = 3 : 1.", ratio_val("3:1"), 1e-9), "c": bound("The mean cost ₹112 is nearer the cheaper spice, so there is more of it: the ratio cheaper : dearer is above 1.", lambda v: v > ratio_val("1:1") + 1)}),
    pyq(S2, 60, "q-mx-replace", "An 80-litre mixture contains milk and water in the ratio 7 : 1. Some of it is removed and replaced with pure milk, and the milk-to-water ratio becomes 15 : 1. How many litres of the mixture were replaced?",
        ["40 litres", "18 litres", "32 litres", "46 litres"], "a",
        ["Water = 80 ÷ 8 = 10 L. In the final mixture water is 1/16 of 80 = 5 L.", "Water fell to half, so half of the mixture was removed.", "Replaced = 40 L."],
        lambda: 80 * (1 - (80 / 16) / 10), 40, 1e-9, tech=["ratio-parts"], trick="Follow the water, since only milk is added: 10 L → 5 L, so exactly half was replaced."),
    pyq(S3, 65, "q-mx-allig", "How many kilograms of wheat costing ₹52 a kg must be mixed with 30 kg of wheat costing ₹40 a kg so that a 20% gain is made by selling the mixture at ₹54 a kg?", ["18.2 kg", "21.4 kg", "24 kg", "28.5 kg"], "b",
        ["Cost price of the mix = 54 ÷ 1.2 = ₹45 a kg.", "52x + 40 × 30 = 45(x + 30), so 52x + 1,200 = 45x + 1,350.", "7x = 150, so x = 150/7 ≈ 21.4 kg."],
        lambda: 150 / 7, 21.4, 0.05, tech=["ratio-parts", "back-substitute"], concepts=2, heavy=True,
        trick="Alligation on 45: the dearer wheat is ₹7 above the mean, the cheaper ₹5 below. Quantities are in the ratio 5 : 7 (dearer : cheaper)… so x = 30 × 5/7 ≈ 21.4."),
]

PYQS = PYQS + PYQS_RY


def practice_items():
    return []
