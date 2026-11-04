"""Profit, loss & discount: question types, formulas, methods, PYQs and practice.

Same rules as every topic: PYQs are condensed restatements (own words, same numbers); every answer is
recomputed; every wrong-option note carries a check; every practice answer is found by two methods.
"""
from fractions import Fraction as F

from bank import bound, mistake, pyq, prac

TOPIC = "profit-loss"      # a topic node in data/tree.json
PREFIX = "pl"              # practice ids pl-p01, pl-p02, ... (append new items at the end so old ids never move)

NODES = {
    "c-pl-multiplier": {"short": "Multiplier", "label": "Everything is a multiplier", "kind": "concept", "parent": "profit-loss", "order": 1,
                        "summary": "A profit, a loss, a markup and a discount are all just numbers you multiply the cost by.", "links": ["percentage"]},
    "c-pl-quantity": {"short": "Quantity tricks", "label": "Quantity changes: false weight and free units", "kind": "concept", "parent": "profit-loss", "order": 2,
                      "summary": "The seller changes how much you get, not what you pay.", "links": []},
    "c-pl-rate": {"short": "Rates and mixing", "label": "Rates (n for ₹x) and mixing", "kind": "concept", "parent": "profit-loss", "order": 3,
                  "summary": "Buying and selling rates given as 'n for ₹x', or goods mixed before selling.", "links": ["mixture-alligation"]},
    "c-pl-symmetry": {"short": "Equal profit & loss", "label": "Equal profit and equal loss", "kind": "concept", "parent": "profit-loss", "order": 4,
                      "summary": "When two selling prices give the same profit and loss, the cost sits exactly between them.", "links": []},
    "q-pl-chain": {"short": "Markup–discount", "label": "Markup, discount and profit chain", "kind": "qtype", "parent": "c-pl-multiplier", "order": 1,
                   "summary": "Marked price above cost, one or more discounts, then profit % or cost price.", "links": []},
    "q-pl-weight": {"short": "False weight", "label": "Dishonest dealer: false weight", "kind": "qtype", "parent": "c-pl-quantity", "order": 1,
                    "summary": "A weight lighter than claimed, often with a markup or a discount on top.", "links": []},
    "q-pl-free": {"short": "Free units", "label": "Free units, donation and overall gain", "kind": "qtype", "parent": "c-pl-quantity", "order": 2,
                  "summary": "Buy n get f free, units given away, then the overall profit or loss.", "links": []},
    "q-pl-rate": {"short": "Rates n for ₹x", "label": "Rates 'n for ₹x' and mixed goods", "kind": "qtype", "parent": "c-pl-rate", "order": 1,
                  "summary": "Costs and selling price given as 'n for ₹x'; mix several kinds before selling.", "links": []},
    "q-pl-equal": {"short": "Equal P & L", "label": "Same profit and loss at two prices", "kind": "qtype", "parent": "c-pl-symmetry", "order": 1,
                   "summary": "Profit at one price equals loss at another; find cost, or the result at a third price.", "links": []},
}

FORMULAS = [
    {"id": "pl-f1", "node": "c-pl-multiplier", "text": "SP = CP × (1 + p) for a profit p, SP = CP × (1 − l) for a loss l.   Profit % = (SP ÷ CP − 1) × 100",
     "note": "Always find the multiplier SP ÷ CP first. 1.144 means 14.4% profit; 0.93 means 7% loss."},
    {"id": "pl-f2", "node": "c-pl-multiplier", "text": "MP = CP × (1 + m) and SP = MP × (1 − d), so SP = CP × (1 + m)(1 − d)",
     "note": "Chain the multipliers. Never add and subtract the percentages."},
    {"id": "pl-f3", "node": "c-pl-multiplier", "text": "Net % = m − d − (m × d) ÷ 100   (markup m %, discount d %)",
     "note": "The same thing as (1 + m)(1 − d) − 1. For 30 and 12: 30 − 12 − 3.6 = 14.4."},
    {"id": "pl-f4", "node": "c-pl-multiplier", "text": "Successive discounts d₁ and d₂ together = d₁ + d₂ − (d₁ × d₂) ÷ 100",
     "note": "20% then 15%: 20 + 15 − 3 = 32%, not 35%. The order does not matter."},
    {"id": "pl-f5", "node": "c-pl-multiplier", "text": "A flat discount in ₹: SP = CP × (1 + m)(1 − d) − flat.  With profit p: CP = flat ÷ [(1 + m)(1 − d) − (1 + p)]",
     "note": "Profit % = (chain % − 100 × flat ÷ CP): a bigger CP gives a bigger profit, which helps pick among options."},
    {"id": "pl-f6", "node": "c-pl-quantity", "text": "False weight: the customer pays for the true weight and receives the false weight. Profit % = (true − false) ÷ false × 100",
     "note": "Divide by the false weight (what the dealer really gave), not the true one. 25% short means false = ¾ of true, so profit = ⅓ = 33⅓%."},
    {"id": "pl-f7", "node": "c-pl-quantity", "text": "False weight with markup and discount: multiplier = (1 + m)(1 − d) × true ÷ false.  Profit % = multiplier − 1",
     "note": "6% discount and a weight 25% short: 0.94 × 4/3 = 1.2533, i.e. 25.33%."},
    {"id": "pl-f8", "node": "c-pl-quantity", "text": "Buy n, get f free: each unit received costs the buyer price × n ÷ (n + f)",
     "note": "3 free with every 10 means 13 units for the price of 10."},
    {"id": "pl-f9", "node": "c-pl-rate", "text": "'n for ₹x' means ₹x ÷ n each. To compare two rates, use the LCM of the two quantities so that both are whole numbers",
     "note": "5 for ₹40 is ₹8 each. Selling 4 for ₹10 against buying 3 for ₹10: take 12 articles, cost ₹40, sale ₹30."},
    {"id": "pl-f10", "node": "c-pl-rate", "text": "Goods mixed in the ratio a : b : c cost (a·c₁ + b·c₂ + c·c₃) ÷ (a + b + c) per unit",
     "note": "The cost of the mix always lies between the cheapest and the dearest component. That alone decides profit or loss in many questions."},
    {"id": "pl-f11", "node": "c-pl-symmetry", "text": "Profit at SP₁ equals loss at SP₂ ⇒ CP = (SP₁ + SP₂) ÷ 2.   Profit % at SP₁ = (SP₁ − SP₂) ÷ (SP₁ + SP₂) × 100",
     "note": "Selling at the midpoint of the two prices is selling at cost: no profit, no loss."},
    {"id": "pl-f12", "node": "c-pl-symmetry", "text": "Two articles sold at the same price, one at x % profit and one at x % loss ⇒ net loss of x² ÷ 100 % of the total cost",
     "note": "20% and 20% gives a 4% loss. It is never a gain and never zero."},
    {"id": "pl-f13", "node": "c-pl-quantity", "text": "Overall profit % = (total money received − total cost) ÷ total cost × 100",
     "note": "Add up what came in and what went out first, then compare. Donated units bring nothing in; free units bring nothing in either."},
]

METHODS = {
    "q-pl-chain": {
        "formulas": ["pl-f1", "pl-f2", "pl-f3", "pl-f4", "pl-f5"],
        "tech": ["multiplier", "estimate", "back-substitute", "cancel-first"],
        "standard": "Call the cost 100 (or CP). Marked price = CP × (1 + m). Selling price = marked price × (1 − d). Profit % = SP ÷ CP − 1. If the SP is given and the CP asked, divide the SP by the chain multiplier.",
        "fast": "Multiply the decimals once: 1.3 × 0.88 = 1.144, so 14.4%. For two discounts use 0.8 × 0.85 = 0.68 (32% off), never 35%. If the SP is given, CP = SP ÷ multiplier.",
        "ultra": "Net % = m − d − md ÷ 100: 30 − 12 − 3.6 = 14.4. When the SP is large and the CP is asked, round the multiplier: 1.156 ≈ 1.16, so 39,312 ÷ 1.16 ≈ 33,900, and pick the nearest option.",
        "eliminate": "(1) With a discount the net profit is always below the markup, so any option at or above the markup is out. (2) Estimate the multiplier and divide: options far from the result are out. (3) When the equation has a flat ₹ discount, profit grows with CP, so test the biggest and smallest option first.",
        "traps": ["Adding and subtracting percentages (30 − 12 = 18) instead of chaining them.",
                  "Giving the discount amount as a % of cost (12% of 130 = 15.6) instead of the profit.",
                  "Adding two successive discounts (20% + 15% = 35%) instead of combining them (32%).",
                  "Taking the discount on the cost price instead of the marked price.",
                  "Dividing by the multiplier when the question wants you to multiply, and the reverse."],
        "variations": ["Profit given on the selling price instead of the cost price.",
                       "Cost of x articles equals the selling price of y articles.",
                       "Discount plus overheads (transport, repairs) added to the cost before the profit.",
                       "Find the marked price for a target profit after a given discount.",
                       "Two successive discounts equal to one single discount."],
    },
    "q-pl-weight": {
        "formulas": ["pl-f6", "pl-f7", "pl-f1"],
        "tech": ["fraction-percent", "multiplier"],
        "standard": "Say the dealer charges for 1 kg but gives less. Money received for the goods he handed over, divided by what those goods cost him, gives the multiplier. With a discount, multiply by (1 − d) first.",
        "fast": "25% less means he hands over ¾ of what he charges for, so multiply by 4/3: 94 × 4 ÷ 3 = 125.33 → 25.33%.",
        "ultra": "Turn the shortage into a fraction (25% = ¼, so false = ¾ of true), then multiply the 'sold at' percentage by the inverse: 94 × 4 ÷ 3 by hand is 376 ÷ 3.",
        "eliminate": "When the options are only about 1% apart, estimates cannot separate them, so use the decimal tail: 94 × 4 ÷ 3 ends in .33, and only one option ends that way. Also check the sign: a short weight can only add profit, never remove it.",
        "traps": ["Dividing by the true weight instead of the false weight (25% short gives 33⅓%, not 25%).",
                  "Treating the shortage as the profit itself (25% short is not 25% profit).",
                  "Subtracting the discount from the gain: 33⅓ − 6 = 27⅓ is wrong; the effects multiply.",
                  "Ignoring the markup when one is given."],
        "variations": ["A weight that is x grams short per kg, with no discount (pure gain).",
                       "Dishonest dealer who also claims to sell at cost price.",
                       "False weight with a markup and a discount together.",
                       "Cheating both ways: buys with a heavier weight and sells with a lighter one."],
    },
    "q-pl-free": {
        "formulas": ["pl-f8", "pl-f13", "pl-f1"],
        "tech": ["sign-check", "multiplier", "estimate"],
        "standard": "Work out the cost of everything, then the money that came in: units sold × price after discount, spread over the free units (money = units handed out × price × n ÷ (n + f)). Overall % = (money in − cost) ÷ cost.",
        "fast": "Do the money in once: 1,200 × 93.5 × 10/13 ≈ 86,308. Loss = (1,20,000 − 86,308) ÷ 1,20,000 = 28.08%.",
        "ultra": "Sign first. Even with no free units the receipts (1,200 × 93.5 = ₹1,12,200) are below the cost (₹1,20,000), so it is a loss. The free units can only make it worse.",
        "eliminate": "(1) Sign check: if the best case already loses money, every 'profit' option is out. (2) The free units cut the receipts by 3/13 (about 23%), so the loss must be well above the no-free-units loss of 6.5%.",
        "traps": ["Counting all the units as sold, including the donated ones.",
                  "Forgetting the free units (gives a 6.5% loss instead of 28.08%).",
                  "Treating '3 free with 10' as 30% off instead of 13 units for the price of 10.",
                  "Using the marked price instead of the discounted price."],
        "variations": ["Buy 3 get 1 free with a further percentage discount.",
                       "Some units spoil or are given away before the sale.",
                       "A bulk discount on the whole order and free units on top.",
                       "Overall profit when only part of the stock is sold at a loss."],
    },
    "q-pl-rate": {
        "formulas": ["pl-f9", "pl-f10", "pl-f1"],
        "tech": ["sign-check", "common-unit", "estimate"],
        "standard": "Find the cost per piece of each kind (x ÷ n). Mix in the given ratio to get the cost per piece of the mix. Find the selling price per piece. Profit % = SP ÷ CP − 1.",
        "fast": "Costs ₹8, ₹7.50, ₹9 per piece; mix 2 : 2 : 3 costs (16 + 15 + 27) ÷ 7 = 58/7. Selling price 32/3. Multiply both by 21: cost 174, sale 224, so 50/174 ≈ 28.7%.",
        "ultra": "Multiply both prices by the LCM of the denominators (7 and 3 give 21) so no fraction appears: 174 and 224.",
        "eliminate": "(1) Sign check: if the selling price per piece is above every cost per piece, it is a profit, and every loss option is out. (2) The mix cost lies between the cheapest and the dearest; use it to bound the profit %.",
        "traps": ["Using the simple average of the costs instead of the weighted one.",
                  "Reading 'n for ₹x' upside down (5 for ₹40 is ₹8 each, not ₹0.125).",
                  "Comparing a price for one count with a price for another count without a common unit."],
        "variations": ["Same quantity bought at two rates and the whole lot sold at a third rate.",
                       "Two kinds of grain mixed in a ratio and sold at a given rate.",
                       "Buys at n for ₹x and sells at m for ₹y; find the profit %.",
                       "Find the selling rate for a target profit."],
    },
    "q-pl-equal": {
        "formulas": ["pl-f11", "pl-f12", "pl-f1"],
        "tech": ["symmetry", "sign-check"],
        "standard": "Profit at SP₁ is SP₁ − CP; loss at SP₂ is CP − SP₂. Set them equal: CP = (SP₁ + SP₂) ÷ 2. Then find the result at any third price from that CP.",
        "fast": "The cost is the midpoint of the two prices: (2,400 + 2,000) ÷ 2 = 2,200.",
        "ultra": "Add and halve. If the third price is also the midpoint, the answer is 'no profit, no loss' before you calculate anything.",
        "eliminate": "Look at the third price first: if it is exactly halfway between the two given prices, only the 'no profit, no loss' option can be right.",
        "traps": ["Assuming the cost equals one of the two selling prices.",
                  "Finding the profit % on the selling price instead of the cost.",
                  "Thinking that equal profit % and loss % on two articles cancel each other (they do not: it is a net loss)."],
        "variations": ["Same profit at one price and loss at another, then a target profit %.",
                       "Two articles at the same selling price, one at x% profit and one at x% loss.",
                       "Profit % at one price is double the loss % at another."],
    },
}

REFS = [
    {"title": "SATHEE (IIT Kanpur): topic weightage in SSC CGL from past papers", "url": "https://satheessc.iitk.ac.in/sathee-ssc/ssc-exams/ssc-cgl/ssc-details/analysis-of-weightage-of-topics-based-on-previous-year-questions",
     "note": "Says Profit & Loss is usually 1–2 questions per Tier 1 paper, with successive discount 0–1 more. Tier 1 only; the page does not cite its own source, so treat it as a rough outside figure, not a count."},
    {"title": "SpeedMath: 10 profit and loss shortcut formulas", "url": "https://speedmath.in/blog/profit-and-loss-10-shortcut-formulas-every-exam-aspirant-must-know",
     "note": "Source of the pattern list: net % from markup and discount, equal % profit and loss at one price, mixed purchases at one rate, overheads, target selling price. Every shortcut used here is re-derived and random-tested, not copied."},
    {"title": "Cracku: profit and loss questions for SSC CGL", "url": "https://cracku.in/blog/profit-and-loss-questions-for-ssc-cgl-pdf/",
     "note": "Pattern list for the exam: successive discount, markup and discount, discount plus overheads, cost of x equals selling price of y, price against quantity changes."},
    {"title": "Cracku: Tier 2 profit and loss questions", "url": "https://cracku.in/blog/?p=42842", "note": "Tier 2 style questions to practise from (not yet analysed here; no Tier 2 paper has been sent)."},
]

# ----------------------------------------------------------------------------------------------
# PYQs
# ----------------------------------------------------------------------------------------------
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"


def _money_in_s1_61():
    sold = 1500 - 300
    paid_for = F(sold * 10, 13)                  # 3 free with every 10 bought: 13 units go out for 10 paid
    return float((paid_for * F(110) * F(85, 100) - 120000) / 120000 * 100)


PYQS = [
    pyq(S1, 61, "q-pl-free", "A company made 1,500 units at a total cost of ₹1,20,000 and donated 300 units to an NGO. The rest was sold at a 15% discount on the market price of ₹110 a unit, with 3 units free for every 10 bought. If all 1,500 units were distributed, what is the overall gain or loss %?",
        ["25% loss", "15% profit", "28.08% loss", "36.6% profit"], "c",
        ["Cost per unit = 1,20,000 ÷ 1,500 = ₹80. The 300 donated units bring in nothing, so 1,200 units reach buyers.",
         "Price after the 15% discount = 110 × 0.85 = ₹93.50.",
         "3 free with every 10 bought: buyers get 13 units for 10 paid, so only 1,200 × 10/13 ≈ 923.08 units are paid for.",
         "Money received = 923.08 × 93.5 ≈ ₹86,308.",
         "Loss = (1,20,000 − 86,308) ÷ 1,20,000 ≈ 28.08%."],
        _money_in_s1_61, -28.08, 0.01,
        tech=["sign-check", "multiplier", "estimate"], concepts=3, heavy=True,
        trick="Sign first: even with no free units, 1,200 × ₹93.50 = ₹1,12,200 is below the ₹1,20,000 cost. Both 'profit' options are out in ten seconds.",
        wrong={"a": bound("Only the exact working separates this one: 25% loss would need receipts of ₹90,000, and the real receipts are about ₹86,308 (a 28.08% loss).", lambda v: abs(v + 28.08) > 1),
               "b": bound("Sign check: the best case, with no free units at all, is 1,200 × ₹93.50 = ₹1,12,200 against a cost of ₹1,20,000. That is already a loss, so no profit option can be right.", lambda v: v > 0),
               "d": bound("Same sign check: receipts cannot beat the cost here, so a profit is impossible.", lambda v: v > 0)}),
    pyq(S1, 71, "q-pl-chain", "A retailer marks a laptop 70% above its cost and gives a first discount of 20% on the marked price. In a sale a further 15% is taken off the discounted price. If the final selling price is ₹39,312, what is the approximate cost price?",
        ["₹28,000", "₹34,000", "₹32,000", "₹35,000"], "b",
        ["Chain the multipliers: 1.7 × 0.8 × 0.85 = 1.156, so SP = 1.156 × CP.",
         "CP = 39,312 ÷ 1.156 ≈ ₹34,009.",
         "The nearest option is ₹34,000."],
        lambda: 39312 / (1.7 * 0.8 * 0.85), 34008.65, 500,
        tech=["multiplier", "estimate", "back-substitute"], concepts=1, heavy=True,
        trick="The multiplier is about 1.16, so CP ≈ 39,312 ÷ 1.16 ≈ ₹33,900. The nearest option is ₹34,000.",
        wrong={"a": bound("₹28,000 would need a multiplier of 39,312 ÷ 28,000 = 1.40, but the chain 1.7 × 0.8 × 0.85 gives only 1.156.", lambda v: abs(39312 / v - 1.156) > 0.05),
               "c": bound("₹32,000 would need a multiplier of 1.23; the chain gives 1.156.", lambda v: abs(39312 / v - 1.156) > 0.05),
               "d": mistake("Added the two discounts (20% + 15% = 35%) instead of chaining them (32% off): 39,312 ÷ (1.7 × 0.65) ≈ ₹35,577, nearest to ₹35,000.", 39312 / (1.7 * 0.65), 600)}),
    pyq(S2, 70, "q-pl-rate", "A baker buys wheat flour at 5 for ₹40, rye flour at 6 for ₹45 and oats flour at 4 for ₹36. He mixes them in the ratio 2 : 2 : 3 and sells all of it at 3 for ₹32. What is his approximate profit or loss %?",
        ["Loss of 28%", "Profit of 27%", "Profit of 29%", "Loss of 19%"], "c",
        ["Cost per piece: wheat 40 ÷ 5 = ₹8, rye 45 ÷ 6 = ₹7.50, oats 36 ÷ 4 = ₹9.",
         "Mix of 7 pieces (2 : 2 : 3): cost = 16 + 15 + 27 = ₹58, so 58/7 per piece.",
         "Selling price per piece = 32/3.",
         "Multiply both by 21: cost 174, selling 224.",
         "Profit = (224 − 174) ÷ 174 ≈ 28.7%, about 29%."],
        lambda: (F(32, 3) / F(58, 7) - 1) * 100, 28.74, 0.5,
        tech=["sign-check", "common-unit", "estimate"], concepts=2, heavy=True,
        trick="The selling price per piece (₹10.67) is above every cost (₹7.50, ₹8, ₹9), so both loss options are out. Against an average cost near ₹8.3 the profit is about 29%.",
        wrong={"a": bound("Sign check: ₹10.67 per piece is above even the dearest cost of ₹9, so this cannot be a loss.", lambda v: v < 0),
               "b": bound("Close, but the weighted cost is 58/7 = ₹8.29 and ₹10.67 ÷ 8.29 = 1.287. A 27% profit would need a cost of ₹8.40.", lambda v: abs(v - 28.74) > 1),
               "d": bound("Sign check: the selling price beats every cost, so this cannot be a loss.", lambda v: v < 0)}),
    pyq(S3, 51, "q-pl-weight", "A shopkeeper sells rice at a 6% discount on the marked price but uses a weight that is 25% less than the actual weight. Find his overall profit %.",
        ["20.5%", "22.5%", "25.3%", "26.5%"], "c",
        ["A weight 25% short means he hands over ¾ of what he charges for.",
         "He receives 0.94 of the marked price for goods that are worth 0.75 of it.",
         "Profit = 0.94 ÷ 0.75 − 1 = 25.33%."],
        lambda: (0.94 / 0.75 - 1) * 100, 25.333, 0.1,
        tech=["fraction-percent", "multiplier"], concepts=2, heavy=False,
        trick="25% less is ¾, so multiply by 4/3: 94 × 4 ÷ 3 = 125.33. Only one option has the tail .33.",
        wrong={k: bound(f"{o} is a near miss: the exact profit is 25.33% (94 × 4 ÷ 3 = 125.33).", lambda v: abs(v - 25.333) > 0.5)
               for k, o in (("a", "20.5%"), ("b", "22.5%"), ("d", "26.5%"))}),
    pyq(S3, 52, "q-pl-equal", "The profit made on an article sold for ₹2,400 equals the loss made when it is sold for ₹2,000. What is the profit or loss % if it is sold for ₹2,200?",
        ["Profit of 2.5%", "Profit of 3.125%", "Loss of 3.125%", "No loss, no profit"], "d",
        ["₹2,400 − CP = CP − ₹2,000, so CP = (2,400 + 2,000) ÷ 2 = ₹2,200.",
         "Selling at ₹2,200 is selling at cost: no profit, no loss."],
        lambda: (2200 - (2400 + 2000) / 2) / ((2400 + 2000) / 2) * 100, 0, 0,
        tech=["symmetry"], concepts=1, heavy=False,
        trick="The cost is the midpoint of the two prices. ₹2,200 is that midpoint.",
        wrong={k: bound(f"₹2,200 is exactly halfway between ₹2,400 and ₹2,000, so it is the cost. Any profit or loss figure ({o}) cannot be right.", lambda v: v != 0)
               for k, o in (("a", "Profit of 2.5%"), ("b", "Profit of 3.125%"), ("c", "Loss of 3.125%"))}),
    pyq(S3, 70, "q-pl-chain", "A television is sold for ₹Q at a 25% profit. In a clearance sale the shopkeeper marks the same set at 1.4Q and allows a 15% discount on the marked price. What is his profit % in the sale?",
        ["45.75%", "40%", "48.75%", "50%"], "c",
        ["SP = Q gives a 25% profit, so CP = Q ÷ 1.25 = 0.8Q.",
         "New price = 1.4Q × 0.85 = 1.19Q.",
         "Profit = (1.19Q − 0.8Q) ÷ 0.8Q = 48.75%."],
        lambda: (1.4 * 0.85 / (1 / 1.25) - 1) * 100, 48.75, 0,
        tech=["multiplier", "bounds", "back-substitute"], concepts=2, heavy=False,
        trick="Cost is 0.8Q and the new price is 1.19Q. 1.19 ÷ 0.8 is just under 1.5, so the profit is just under 50%.",
        wrong={"a": bound("45.75% would need a selling price of 0.8 × 1.4575 = 1.166Q; the real price is 1.19Q.", lambda v: v < 48),
               "b": mistake("This is the markup percentage itself. It ignores both the 15% discount and the fact that the cost is 0.8Q, not Q.", 40),
               "d": bound("50% profit would need a price of 1.2Q (1.5 × 0.8Q). The discounted price is 1.19Q, a little less.", lambda v: v >= 50)}),
    pyq(S3, 71, "q-pl-chain", "A trader marks his goods 30% above the cost price and then allows a discount of 12%. What is his profit %?",
        ["14.4%", "15.6%", "16.5%", "18.0%"], "a",
        ["Multiplier = 1.3 × 0.88 = 1.144.", "Profit = 14.4%."],
        lambda: (1.3 * 0.88 - 1) * 100, 14.4, 0.01,
        tech=["multiplier", "fraction-percent"], concepts=1, heavy=False, steps=2,
        trick="Net % = 30 − 12 − (30 × 12) ÷ 100 = 30 − 12 − 3.6 = 14.4.",
        wrong={"b": mistake("Gave the discount amount instead of the profit: 12% of 130 = 15.6, as a % of cost.", 15.6),
               "c": bound("12% off a price that is 130% of cost takes off 15.6% of cost, so the profit is 30 − 15.6 = 14.4. Anything above 15 is out.", lambda v: v > 15),
               "d": mistake("Subtracted the percentages: 30 − 12 = 18. The discount is on the marked price, which is already 30% above cost.", 18)}),
    pyq(S3, 72, "q-pl-chain", "A shopkeeper marks his products 50% above cost and allows a 20% discount on the marked price. He also gives an extra cash discount of ₹120 and still makes a 16% profit on cost. What is the cost price?",
        ["₹1,800", "₹3,000", "₹2,200", "₹2,400"], "b",
        ["SP = 1.5 × 0.8 × CP − 120 = 1.2 CP − 120.",
         "A 16% profit means SP = 1.16 CP.",
         "1.2 CP − 120 = 1.16 CP, so 0.04 CP = 120 and CP = ₹3,000."],
        lambda: 120 / (1.5 * 0.8 - 1.16), 3000, 1e-6,
        tech=["back-substitute", "bounds", "multiplier"], concepts=2, heavy=False,
        trick="Profit % = 20 − 12,000 ÷ CP. A bigger CP gives a bigger profit, and even ₹2,400 only reaches 15%, so the answer is the biggest option.",
        wrong={k: bound(f"Substituting {o}: profit = 20% − 12,000 ÷ {x} = {20 - 12000 / x:.2f}%, not 16%.", lambda v: abs((20 - 12000 / v) - 16) > 0.5)
               for k, o, x in (("a", "₹1,800", 1800), ("c", "₹2,200", 2200), ("d", "₹2,400", 2400))}),
]


# ----------------------------------------------------------------------------------------------
# Practice: the main method gives `correct`; a different method gives `check`
# ----------------------------------------------------------------------------------------------
def rupee_chain(cp, m, discounts):
    """Follow the rupees: cost, marked price, then each discount in turn. Returns the final selling price."""
    sp = F(cp) * (1 + F(m, 100))
    for d in discounts:
        sp -= sp * F(d, 100)
    return sp


def practice_items():
    out = []
    # ---------------- markup, discount, profit ----------------
    out.append(prac("q-pl-chain", "same", "A trader marks goods 40% above cost and allows a discount of 10%. Find his profit %.",
                    (F(14, 10) * F(9, 10) - 1) * 100,
                    [(F(30), "Subtracted the percentages: 40 − 10."), (F(14), "Gave the discount amount as a % of cost: 10% of 140."), ((F(14, 10) / F(9, 10) - 1) * 100, "Divided by (1 − d) instead of multiplying.")],
                    "1.4 × 0.9 = 1.26, so 26% profit.", rupee_chain(100, 40, [10]) - 100, fmt="pct", tech=["multiplier", "fraction-percent"]))
    out.append(prac("q-pl-chain", "same", "The marked price of a jacket is ₹1,200. It is sold after successive discounts of 20% and 10%, which gives a profit of 8%. Find the cost price.",
                    F(1200) * F(8, 10) * F(9, 10) / F(108, 100),
                    [(F(1200) * F(7, 10) / F(108, 100), "Added the discounts: 20% + 10% = 30% (it is 28%)."), (F(1200) * F(8, 10) * F(9, 10) * F(108, 100), "Multiplied by 1.08 instead of dividing."), (F(864) - F(8, 100) * 864, "Took 8% off the selling price instead of dividing by 1.08.")],
                    "SP = 1,200 × 0.8 × 0.9 = 864. CP = 864 ÷ 1.08 = ₹800.",
                    F(1200) * (F(100) * F(8, 10) * F(9, 10) / F(108, 100)) / 100, tech=["multiplier", "cancel-first"]))
    out.append(prac("q-pl-chain", "same", "A shopkeeper marks goods 50% above cost and gives a 20% discount, and earns ₹300 profit on an article. Find its cost price.",
                    F(300) / ((F(15, 10) * F(8, 10) - 1)),
                    [(F(300) / F(3, 10), "Used 50 − 20 = 30% as the profit."), (F(300) / F(5, 10), "Used the 50% markup as the profit."), (F(300) / (F(5, 10) * F(8, 10)), "Multiplied 50% by 0.8 instead of chaining 1.5 × 0.8.")],
                    "1.5 × 0.8 = 1.2, so the profit is 20% of CP. CP = 300 ÷ 0.2 = ₹1,500.",
                    F(100) * 300 / (rupee_chain(100, 50, [20]) - 100), tech=["multiplier"]))
    cp_flat = F(360) / (F(16, 10) * F(75, 100) - F(108, 100))
    out.append(prac("q-pl-chain", "same", "A shopkeeper marks goods 60% above cost, allows a 25% discount and a further ₹360 off, and still makes an 8% profit. Find the cost price.",
                    cp_flat,
                    [(F(360) / (F(16, 10) * F(75, 100) - 1), "Forgot the 8% profit that is still made."), (F(360) / F(35, 100), "Used 60 − 25 = 35% as the margin."), (F(360) / F(8, 100), "Took the whole ₹360 as the 8% profit.")],
                    "SP = 1.6 × 0.75 × CP − 360 = 1.2 CP − 360. Set it equal to 1.08 CP: 0.12 CP = 360, CP = ₹3,000.",
                    cp_flat if rupee_chain(cp_flat, 60, [25]) - 360 == F(108, 100) * cp_flat else None, tech=["back-substitute", "bounds"], concepts=2))
    out.append(prac("q-pl-chain", "harder", "A dealer marks a watch 80% above cost, then gives two successive discounts of 20% and 10%. Find his profit %.",
                    (F(18, 10) * F(8, 10) * F(9, 10) - 1) * 100,
                    [(F(50), "Subtracted: 80 − 20 − 10."), ((F(18, 10) * F(7, 10) - 1) * 100, "Combined the discounts as 20 + 10 = 30% instead of 28%."), ((F(18, 10) * F(8, 10) - 1) * 100, "Applied only the first discount.")],
                    "1.8 × 0.8 × 0.9 = 1.296, so a 29.6% profit.", (rupee_chain(1000, 80, [20, 10]) - 1000) / 10, fmt="pct", tech=["multiplier", "cancel-first"]))
    # ---------------- false weight ----------------
    out.append(prac("q-pl-weight", "same", "A dishonest dealer sells at cost price but uses a 900 g weight for 1 kg. Find his gain %.",
                    F(1000 - 900, 900) * 100,
                    [(F(10), "Divided by the true weight (1,000) instead of the false weight (900)."), (F(90), "Took the weight ratio 900/1,000 as the gain."), (F(1000, 900) * 100, "Inverted the fraction: 1,000/900 = 111.11%.")],
                    "He charges for 1,000 g but hands over 900 g. Gain = 100 ÷ 900 = 11.11%.", (F(1000) - F(900)) / F(900) * 100, fmt="pct", tech=["fraction-percent"]))
    out.append(prac("q-pl-weight", "harder", "A dealer marks goods 20% above cost, allows a 15% discount and uses an 800 g weight for 1 kg. Find his profit %.",
                    (F(12, 10) * F(85, 100) * F(1000, 800) - 1) * 100,
                    [((F(12, 10) * F(85, 100) - 1) * 100, "Ignored the false weight."), (F(30), "Added the percentages: 20 − 15 + 25."), ((F(12, 10) * F(85, 100) * F(12, 10) - 1) * 100, "Took the 200 g shortage as a 20% gain instead of 25%.")],
                    "1.2 × 0.85 = 1.02, and the weight gives × 1,000/800 = 1.25. 1.02 × 1.25 = 1.275, so 27.5%.",
                    (rupee_chain(1000, 20, [15]) - F(800)) / F(800) * 100, fmt="pct", tech=["multiplier", "fraction-percent"], concepts=3))
    # ---------------- free units ----------------
    out.append(prac("q-pl-free", "same", "A trader gives 1 article free with every 5 bought, selling each at its cost price. Find his loss %.",
                    F(1, 6) * 100,
                    [(F(20), "Divided the free article by the 5 bought, not the 6 given."), (F(5, 6) * 100, "Gave the money received as a fraction of cost instead of the loss."), (F(6, 5) * 100, "Inverted the fraction: 6/5 = 120%.")],
                    "Buyers get 6 articles for the price of 5. Loss = 1 ÷ 6 = 16.67%.", (F(60) - F(50)) / F(60) * 100, fmt="pct", tech=["fraction-percent", "sign-check"]))
    out.append(prac("q-pl-free", "harder", "Goods cost ₹100 each. The marked price is 30% above cost, a 10% discount is given, and the offer is buy 3, get 1 free. Find the overall profit or loss %.",
                    (F(117) * 3 - F(400)) / F(400) * 100,
                    [(F(17), "Ignored the free unit."), (F(-5, 2), "Forgot the 10% discount: 1.3 × 3/4 = 0.975."), (F(-22), "Treated 'buy 3 get 1 free' as 33⅓% off.")],
                    "Marked ₹130, after 10% off ₹117. Buyers pay for 3 and get 4: receipts 3 × 117 = 351 against cost 400. Loss = 49 ÷ 400 = 12.25%.",
                    (F(117) * 9 - F(1200)) / F(1200) * 100, fmt="pctsigned", tech=["sign-check", "multiplier"], concepts=3))
    # ---------------- rates ----------------
    out.append(prac("q-pl-rate", "same", "Pencils are bought at 4 for ₹10 and sold at 3 for ₹10. Find the profit %.",
                    (F(10, 3) / F(10, 4) - 1) * 100,
                    [(F(25), "Divided the gain in pieces by 4 instead of 3."), (F(10, 3) / F(10, 4) * 100, "Gave SP ÷ CP as a percentage (133.33%) instead of the profit."), (F(75), "Gave CP ÷ SP as a percentage (75%).")],
                    "Per pencil: cost ₹2.50, sale ₹3.33. 3.33 ÷ 2.5 = 1.333, so 33.33%.", (F(40) - F(30)) / F(30) * 100, fmt="pct", tech=["common-unit"]))
    out.append(prac("q-pl-rate", "harder", "Two kinds of rice costing ₹20 and ₹30 a kg are mixed in the ratio 3 : 2 and sold at ₹27 a kg. Find the profit %.",
                    (F(27) / ((F(3 * 20 + 2 * 30, 5))) - 1) * 100,
                    [((F(27) / F(25) - 1) * 100, "Used the simple average ₹25 instead of the weighted cost ₹24."), ((F(27) / F(2 * 20 + 3 * 30, 5) - 1) * 100, "Mixed the ratio the wrong way round: 2 : 3."), (F(3), "Gave the profit per kg (₹3) as a percentage.")],
                    "Cost of the mix = (3 × 20 + 2 × 30) ÷ 5 = ₹24. Profit = 3 ÷ 24 = 12.5%.", (F(5 * 27) - F(3 * 20 + 2 * 30)) / F(3 * 20 + 2 * 30) * 100, fmt="pct", tech=["sign-check", "estimate"]))
    # ---------------- equal profit and loss ----------------
    cp_eq = F(5400 + 4600, 2)
    out.append(prac("q-pl-equal", "same", "The profit made when an article is sold for ₹5,400 equals the loss made when it is sold for ₹4,600. Find its cost price.",
                    cp_eq, [(F(5400), "Took the higher price."), (F(4600), "Took the lower price."), (F(5400 + 4600), "Added the two prices without halving.")],
                    "CP is the midpoint: (5,400 + 4,600) ÷ 2 = ₹5,000.", cp_eq if (5400 - cp_eq) == (cp_eq - 4600) else None, tech=["symmetry"]))
    out.append(prac("q-pl-equal", "same", "The profit made at a selling price of ₹5,400 equals the loss made at ₹4,600. Find the profit % at ₹5,400.",
                    (F(5400) - cp_eq) / cp_eq * 100,
                    [(F(400, 5400) * 100, "Took the profit on the selling price instead of the cost."), (F(400, 4600) * 100, "Divided by the lower selling price."), (F(16), "Doubled it: used the gap between the two prices (800) as the profit.")],
                    "CP = ₹5,000 and the profit is ₹400, so 8%.", F(5400 - 4600, 5400 + 4600) * 100, fmt="pct", tech=["symmetry", "fraction-percent"]))
    sp_eq = F(1200)
    cp1, cp2 = sp_eq / F(120, 100), sp_eq / F(80, 100)
    out.append(prac("q-pl-equal", "harder", "Two articles are sold at ₹1,200 each, one at a 20% profit and the other at a 20% loss. Find the overall result.",
                    (2 * sp_eq - cp1 - cp2) / (cp1 + cp2) * 100,
                    [(F(0), "Thought +20% and −20% cancel."), (F(4), "Got the size right but the sign wrong."), ((2 * sp_eq - cp1 - cp2) / (2 * sp_eq) * 100, "Took the loss on the total selling price instead of the total cost.")],
                    "Costs: 1,200 ÷ 1.2 = 1,000 and 1,200 ÷ 0.8 = 1,500. Total cost 2,500, receipts 2,400. Loss = 100 ÷ 2,500 = 4%.",
                    -F(20 * 20, 100), fmt="pctsigned", tech=["symmetry", "sign-check"]))
    return out
