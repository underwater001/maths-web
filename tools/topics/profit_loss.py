"""Profit, loss & discount: question types, formulas, methods, PYQs and practice.

Same rules as every topic: PYQs are condensed restatements (own words, same numbers); every answer is
recomputed; every wrong-option note carries a check; every practice answer is found by two methods.
"""
from fractions import Fraction as F
from math import gcd

from bank import APPROX, bound, exact2, fmt_value, inr, mistake, pyq, prac, variants
from topics._pl_ry import PYQS_RY

TOPIC = "profit-loss"      # a topic node in data/tree.json
QUIZ_TYPES = ("q-pl-basic", "q-pl-swap", "q-pl-ratio", "q-pl-reprice", "q-pl-difference", "q-pl-profit-in-articles", "q-pl-partial",
              "q-pl-profit-on-sp", "q-pl-sellers", "q-pl-successive", "q-pl-quantity")   # from the Rakesh Yadav book: past questions and a short method, practice comes later
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
    "c-pl-basic": {"short": "Basic relations", "label": "Cost, selling price and gain: the basic relations", "kind": "concept", "parent": "profit-loss", "order": 5,
                   "summary": "The one-step and two-step relations every other profit and loss question is built from.", "links": ["percentage"]},
    "q-pl-basic": {"short": "Basic profit & loss", "label": "Cost, selling price, profit and loss", "kind": "qtype", "parent": "c-pl-basic", "order": 1,
                   "summary": "Find the cost, selling price, profit % or loss % from the figures given, including overheads and damaged goods.", "links": []},
    "q-pl-swap": {"short": "CP of n = SP of m", "label": "Cost of n articles equals selling price of m", "kind": "qtype", "parent": "c-pl-basic", "order": 2,
                  "summary": "Cost of one number of articles equals the selling price of another number.", "links": []},
    "q-pl-ratio": {"short": "CP : SP ratio", "label": "Ratio of cost to selling price", "kind": "qtype", "parent": "c-pl-basic", "order": 3,
                   "summary": "CP : SP is given, or SP is a multiple or fraction of CP; find the profit % or the other ratio.", "links": []},
    "q-pl-reprice": {"short": "New selling price", "label": "Selling price for a new profit or loss", "kind": "qtype", "parent": "c-pl-basic", "order": 4,
                     "summary": "A profit or loss is given at one price; find the price that gives a different profit.", "links": []},
    "q-pl-difference": {"short": "Price changes by ₹d", "label": "A change of ₹d moves the result from loss to gain", "kind": "qtype", "parent": "c-pl-basic", "order": 5,
                        "summary": "Sold for ₹d more, the loss becomes a gain (or the gain gets bigger); find the cost.", "links": []},
    "q-pl-profit-in-articles": {"short": "Profit = price of n", "label": "Profit or loss equal to the price of some articles", "kind": "qtype", "parent": "c-pl-basic", "order": 6,
                                "summary": "The profit (or loss) on a lot equals the cost or selling price of a few articles.", "links": []},
    "q-pl-partial": {"short": "Part at a gain, part at a loss", "label": "Parts of a stock sold at different profits", "kind": "qtype", "parent": "c-pl-basic", "order": 7,
                     "summary": "A fraction of the stock sold at one rate and the rest at another; find the overall result or the total value.", "links": []},
    "q-pl-profit-on-sp": {"short": "Profit on SP", "label": "Profit as a percent of the selling price", "kind": "qtype", "parent": "c-pl-basic", "order": 8,
                          "summary": "Profit is quoted on the selling price, or the cost is given as a fraction of the selling price.", "links": []},
    "q-pl-sellers": {"short": "Chain of sellers", "label": "Goods passing through several sellers", "kind": "qtype", "parent": "c-pl-basic", "order": 9,
                     "summary": "A sells to B, B sells to C, each at a profit or loss; find any one price or percent.", "links": []},
    "q-pl-successive": {"short": "Successive discounts", "label": "Successive discounts and the single equal discount", "kind": "qtype", "parent": "c-pl-multiplier", "order": 2,
                        "summary": "Two or three discounts one after another, or the single discount that equals them.", "links": []},
    "q-pl-quantity": {"short": "Price and quantity", "label": "Price changes and the quantity bought", "kind": "qtype", "parent": "c-pl-quantity", "order": 3,
                      "summary": "A price changes and the quantity or the spend changes with it; find the new rate or the percent change.", "links": []},
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
    {"id": "pl-f14", "node": "c-pl-basic", "text": "Cost of n articles = selling price of m articles ⇒ profit % = (n − m) ÷ m × 100  (a loss if n is smaller than m)",
     "note": "Divide by the number on the SELLING side. SP of 8 = CP of 10 gives 2/8 = 25% profit; SP of 15 = CP of 10 gives a loss of 5/15 = 33⅓%."},
    {"id": "pl-f15", "node": "c-pl-basic", "text": "CP : SP = a : b ⇒ profit % = (b − a) ÷ a × 100  (loss % = (a − b) ÷ a × 100)",
     "note": "Put the cost at 100 (or at a) and read the profit off the difference. CP is 80% of SP means CP : SP = 4 : 5, a profit of 25%."},
    {"id": "pl-f16", "node": "c-pl-basic", "text": "A swing of ₹d between two selling prices that give profits p₁ and p₂ ⇒ CP = d ÷ (p₂ − p₁)  (a loss counts as a negative profit)",
     "note": "A loss of 20% becoming a gain of 15% is a swing of 35% of the cost. If ₹70 caused it, CP = 70 ÷ 0.35 = ₹200."},
    {"id": "pl-f17", "node": "c-pl-basic", "text": "Profit on N articles equals the selling price of n of them ⇒ profit % = n ÷ (N − n) × 100.  If it equals the cost of n: profit % = n ÷ N × 100",
     "note": "Profit on 20 = SP of 5: 5 ÷ 15 = 33⅓%. The same relation with a loss gives loss % = n ÷ (N + n) × 100 when the loss equals the SP of n."},
    {"id": "pl-f18", "node": "c-pl-basic", "text": "Parts of a stock sold at different rates: total profit = sum of (part × rate); overall % = total profit ÷ total cost × 100",
     "note": "Use the cost of each part as its weight. A loss part subtracts. Never average the rates unless the parts have the same cost."},
    {"id": "pl-f19", "node": "c-pl-basic", "text": "Profit of p % on the SELLING price ⇒ CP = SP × (100 − p) ÷ 100, and profit on cost = p ÷ (100 − p) × 100",
     "note": "20% on selling price is 25% on cost. 10% on selling price turns a cost of ₹27 into SP = 27 ÷ 0.9 = ₹30."},
    {"id": "pl-f20", "node": "c-pl-quantity", "text": "If the price rises p %, spending stays the same when consumption falls by p ÷ (100 + p) × 100 %.  If it falls p %, consumption can rise by p ÷ (100 − p) × 100 %",
     "note": "A 20% rise needs a 16⅔% cut in use. Spend = price × quantity, so the two change in opposite ratios."},
]

METHODS = {
    "q-pl-chain": {
        "cue": 'A marked price above cost, one or more discounts (maybe a flat ₹ off), then the profit % or the cost price is asked.',
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
        "cue": "'Uses a weight of 900 g for 1 kg', or 'a weight 25% less than the actual', possibly with a markup or discount as well.",
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
        "cue": "'Buy 3 get 1 free', units donated or given away, and the overall profit or loss on the whole lot.",
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
        "cue": "Prices given as 'n for ₹x', or several kinds of goods mixed in a ratio and sold at one rate.",
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
        "cue": "'Profit at one price equals the loss at another', or two articles sold at the same price with equal % profit and loss.",
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
    "q-pl-basic": {
        "cue": "Cost, selling price, profit or loss given in rupees or articles, sometimes with overheads, damaged goods or a split of money.",
        "formulas": ["pl-f1", "pl-f13"],
        "tech": ["units-first", "estimate", "back-substitute"],
        "standard": "Add every cost (price, repairs, transport) to get the true cost. Subtract any goods that cannot be sold when working out what comes in. Then profit % = (money in − cost) ÷ cost × 100.",
        "fast": "Find the multiplier SP ÷ CP once and read the profit from it. When the answer must be a cost, divide the selling price by (1 ± the rate).",
        "eliminate": "Check the sign first: if the money in is below the cost it is a loss and every 'profit' option is out. Then test the options against the cost, not against the selling price.",
        "traps": ["Leaving out the repair or transport cost.", "Dividing the profit by the selling price.", "Counting damaged goods as sold.", "Using the dozen price as if it were the price of one."],
        "variations": ["Best transaction by percentage profit (compare ratios, not rupees).", "Two items with equal profit amounts at different rates.", "Cost shared in a ratio and one price given."],
    },
    "q-pl-swap": {
        "cue": "'The cost price of 15 articles equals the selling price of 10 articles', or 'sells 8 at the price of 10'.",
        "formulas": ["pl-f14"],
        "tech": ["ratio-parts", "sign-check"],
        "standard": "Take the price of one article as 1 on the side given. If the cost of n equals the SP of m, then SP of one = n ÷ m times its cost. Profit % = (n − m) ÷ m × 100.",
        "fast": "Subtract the two numbers, divide by the number on the selling side: 15 and 10 give 5 ÷ 10 = 50%. Larger number on the cost side means a profit; larger on the selling side means a loss.",
        "eliminate": "Sign check: the bigger count on the cost side is a profit, otherwise a loss. Then divide by the selling count: options that use the cost count are out.",
        "traps": ["Dividing by the cost count instead of the selling count (10 and 15 gives 33⅓% instead of 50%).", "Reversing profit and loss.", "Treating the difference in numbers as the profit % directly."],
        "variations": ["SP of n articles equals CP of m articles (the same relation read the other way).", "Large counts such as 2750 and 2500: cancel the common factor first.", "'Sells x at the cost of y' wording."],
    },
    "q-pl-ratio": {
        "cue": "'CP : SP is 5 : 6', 'SP is 8/5 of CP', 'CP is 80% of SP', or a profit % asked as a ratio of prices.",
        "formulas": ["pl-f15", "pl-f1"],
        "tech": ["ratio-parts", "fraction-percent"],
        "standard": "Write CP and SP as the numbers of the ratio, or as 100 and the multiplier. Profit % = (SP − CP) ÷ CP × 100. To go the other way, turn the profit % into a multiplier and write the ratio.",
        "fast": "5 : 6 means profit 1 on 5 = 20%. 'CP is 80% of SP' means CP : SP = 4 : 5, a profit of 25%, not 20%.",
        "eliminate": "A profit % found on the SP is always smaller than the profit on cost, so any option equal to (SP − CP) ÷ SP is a trap.",
        "traps": ["Dividing by SP (80% gives 20%, but the profit on cost is 25%).", "Reversing the ratio (SP : CP).", "Reading 200% profit as SP = 2 × CP (it is 3 × CP)."],
        "variations": ["Ratio of two selling prices that give a profit and a loss.", "SP is a multiple of CP.", "Profit given, ratio SP : CP asked."],
    },
    "q-pl-reprice": {
        "cue": "'Sold at a loss of 10% for ₹240; at what price will he gain 20%?' or 'wanted a profit but sold at a loss'.",
        "formulas": ["pl-f1"],
        "tech": ["multiplier", "ratio-parts"],
        "standard": "Find the cost from the given price (price ÷ multiplier). Then the new price = cost × new multiplier.",
        "fast": "Scale directly: new price = given price × new multiplier ÷ old multiplier = 240 × 1.2 ÷ 0.9 = 320.",
        "eliminate": "The new price must lie above the given one when the new profit is higher, and below when it is lower. Test only the options on the correct side.",
        "traps": ["Adding the two percentages to the given price instead of finding the cost first.", "Applying the new % to the given price instead of the cost."],
        "variations": ["Wanted a profit, sold at an equal loss for ₹x: find the intended price.", "Two prices give a profit % and a loss %: find the cost.", "Selling price for a target profit after an overhead."],
    },
    "q-pl-difference": {
        "cue": "'If sold for ₹10 more, he would gain 10% instead of losing 10%', or 'a gain of 5% instead of a loss of 5% gives ₹5 more'.",
        "formulas": ["pl-f16"],
        "tech": ["ratio-parts", "back-substitute"],
        "standard": "The extra rupees are the swing between the two rates, taken as a percent of the cost. Cost = extra ÷ (swing %).",
        "fast": "Swing = 10% + 10% = 20% of CP = ₹10, so CP = ₹50. Gain 5% instead of loss 5% is a 10% swing: ₹5 ÷ 0.1 = ₹50.",
        "eliminate": "Plug each option into the swing: swing % × option must equal the extra rupees. Only one option does.",
        "traps": ["Using only one of the two rates (loss alone, or gain alone).", "Using the extra amount as a percent of the selling price."],
        "variations": ["Loss becomes gain after a price rise of ₹d.", "Both prices given as ₹ values and both profits as %.", "Selling price raised by a % instead of ₹."],
    },
    "q-pl-profit-in-articles": {
        "cue": "'The profit on 17 balls equals the cost of 5', 'a profit equal to the selling price of 5 books'.",
        "formulas": ["pl-f17", "pl-f1"],
        "tech": ["ratio-parts", "cancel-first"],
        "standard": "Write the total profit (or loss) in terms of the cost or price of one article, set it equal to the article count in the statement, and solve for the price. Use total SP − total CP = profit.",
        "fast": "Loss equal to the cost of 5 on 17 balls: the 17 balls sold for the cost of 12, so cost per ball = 720 ÷ 12 = ₹60.",
        "eliminate": "Divide the total selling price by the number of 'effective' articles: the options far from that quotient are out.",
        "traps": ["Mixing up cost and selling price in the statement.", "Using all 17 articles as the base instead of the effective 12."],
        "variations": ["Profit equal to the selling price of n articles.", "Loss equal to the selling price of n articles.", "Find the profit % from the statement alone."],
    },
    "q-pl-partial": {
        "cue": "'One third at 4, half at 5, the rest at cost', or 'two-thirds sold at 5% profit and the rest at 2% loss, total profit ₹400'.",
        "formulas": ["pl-f18", "pl-f1"],
        "tech": ["multiplier", "common-unit", "back-substitute"],
        "standard": "Split the stock into the given parts. Find the profit (or loss) on each part using that part's cost. Add the profits and subtract the losses. Overall % = net ÷ total cost.",
        "fast": "Take the total cost as 1 (or as a convenient number like 120). Then each part's contribution is part × rate. Two-thirds at +5% and one-third at −2% gives 10/3 − 2/3 = 8/3 = 2.667% of the whole.",
        "eliminate": "The overall % lies between the smallest and the largest of the part rates. Options outside that band are out.",
        "traps": ["Averaging the rates without weighting by the part sizes.", "Treating the loss part as a profit.", "Weighting by selling price instead of cost."],
        "variations": ["Part of the stock goes bad before sale.", "Overall profit given; find the total value or one part's rate.", "Three or more parts with the rest sold at cost."],
    },
    "q-pl-profit-on-sp": {
        "cue": "'Profit of 10% on the selling price', 'cost is 13/15 of the selling price'.",
        "formulas": ["pl-f19"],
        "tech": ["fraction-percent", "ratio-parts"],
        "standard": "Convert to cost basis: if the profit is p % of SP, then CP = SP × (100 − p) ÷ 100 and profit on cost = p ÷ (100 − p) × 100. Then solve as a normal profit question.",
        "fast": "10% on SP means CP is 90% of SP, so SP = 27 ÷ 0.9 = ₹30.",
        "eliminate": "Profit quoted on SP is smaller than the same figure on cost, so a profit on cost of 10% gives a smaller price than a profit on SP of 10%: use that to reject the wrong pair.",
        "traps": ["Treating the 10% as a profit on cost (27 × 1.1 = 29.70).", "Using 110% instead of 90% for the SP."],
        "variations": ["Cost given as a fraction of SP.", "Profit on SP converted to profit on cost.", "Two selling prices, one quoted on cost and one on SP."],
    },
    "q-pl-sellers": {
        "cue": "'A sells to B at a profit of 10%, B sells to C at a loss of 10%', 'C paid ₹91', or a jewel passing through three hands.",
        "formulas": ["pl-f1", "pl-f2"],
        "tech": ["multiplier", "sign-check"],
        "standard": "Each seller's selling price is the next seller's cost. Multiply the multipliers in order: price paid by C = A's cost × m₁ × m₂. Divide to go backwards.",
        "fast": "1.10 × 0.90 = 0.99: the first seller ends up 1% better off than the starting price. Use the product, not the sum, of the percentages.",
        "eliminate": "Equal profit and loss in a chain never cancel: 10% up then 10% down leaves a 1% drop. Any 'no change' option is out unless the multipliers cancel exactly.",
        "traps": ["Adding and subtracting the percentages (10% − 10% = 0).", "Applying the second % to the original cost instead of to the new price.", "Dividing when the chain asks you to multiply."],
        "variations": ["Goods rising 65% over three hands with two known profits.", "Buy-back at a loss.", "Final price given; find the first cost."],
    },
    "q-pl-successive": {
        "cue": "'Successive discounts of 10%, 20% and 25%', or 'find the single discount equivalent to…'.",
        "formulas": ["pl-f4", "pl-f2"],
        "tech": ["multiplier", "estimate"],
        "standard": "Convert each discount into a multiplier (90% = 0.9) and multiply: 0.9 × 0.8 × 0.75 = 0.54, so the single discount is 46%.",
        "fast": "For two discounts: d₁ + d₂ − d₁d₂ ÷ 100. For three, do the first two, then combine that with the third.",
        "eliminate": "The combined discount is always less than the sum of the discounts and more than the largest one. Both bounds remove options.",
        "traps": ["Adding the discounts (10 + 20 + 25 = 55%).", "Taking the second discount on the original price instead of the reduced price.", "Using the rate as a multiplier instead of (1 − rate)."],
        "variations": ["Discount on a bundle given the price of three.", "A discount then a free item.", "Equivalent single discount given and one unknown."],
    },
    "q-pl-quantity": {
        "cue": "'A 20% fall in the price lets him buy 4 kg more for ₹100', 'salary reduced by 10%: how much must it rise to return?'.",
        "formulas": ["pl-f20", "pl-f1"],
        "tech": ["multiplier", "fraction-percent", "back-substitute"],
        "standard": "Spend = price × quantity. Write the price change as a multiplier, the quantity change as its inverse, and equate the spend. Solve for the unknown rate or the percent.",
        "fast": "A fall of p % in price lets you buy p ÷ (100 − p) more: 20% fall lets you buy 25% more. To undo a 10% cut you need 10 ÷ 90 = 11⅑%.",
        "eliminate": "The rise needed to undo a fall of p % is always bigger than p %; the cut needed to offset a rise of p % is always smaller. Both remove options.",
        "traps": ["Using the same percent both ways (a 10% cut is not undone by a 10% rise).", "Applying the new price to the old quantity."],
        "variations": ["Consumption cut needed to keep spending the same after a rise.", "Price falls and the extra quantity is given in kg.", "Salary or income cut and restored."],
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

PYQS = PYQS + PYQS_RY


# ----------------------------------------------------------------------------------------------
# Practice: the main method gives `correct`; a different method gives `check`
# ----------------------------------------------------------------------------------------------
def rupee_chain(cp, m, discounts):
    """Follow the rupees: cost, marked price, then each discount in turn. Returns the final selling price."""
    sp = F(cp) * (1 + F(m, 100))
    for d in discounts:
        sp -= sp * F(d, 100)
    return sp


def _hand_items():
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


# ----------------------------------------------------------------------------------------------
# Generated practice (see tools/bank.variants): clean numbers, three named-mistake traps, a second-method check.
# ----------------------------------------------------------------------------------------------
def pc(x):
    """A fraction of 1 as a percentage Fraction."""
    return F(x) * 100


def _ap(v):
    return "" if exact2(v) else APPROX


def t_chain_profit(rng):
    m, d = rng.choice([20, 25, 30, 40, 50, 60, 80]), rng.choice([5, 10, 12, 15, 20, 25])
    ans = pc((1 + F(m, 100)) * (1 - F(d, 100)) - 1)
    if ans <= 0: return None
    item = rng.choice(["a fan", "a bag", "a pair of shoes", "a clock", "a mixer"])
    return prac("q-pl-chain", "same", f"A shopkeeper marks {item} {m}% above its cost and allows a discount of {d}% on the marked price. Find his profit %." + _ap(ans),
                ans, [(F(m - d), f"Subtracted the percentages: {m} − {d}."), (F(d * (100 + m), 100), f"Gave the discount amount as a % of cost: {d}% of {100 + m}."), (pc((1 + F(m, 100)) / (1 - F(d, 100)) - 1), "Divided by (1 − d) instead of multiplying.")],
                f"Multiplier = {100 + m}% × {100 - d}% = {float((1 + F(m, 100)) * (1 - F(d, 100))):.4g}. Profit = {float(ans):.4g}%.", rupee_chain(1000, m, [d]) / 10 - 100, fmt="pct", tech=["multiplier", "fraction-percent"])


def t_chain_flat(rng):
    m, d, p = rng.choice([40, 50, 60, 70, 80]), rng.choice([10, 20, 25, 30]), rng.choice([5, 8, 10, 12, 15])
    k = (1 + F(m, 100)) * (1 - F(d, 100)) - (1 + F(p, 100))
    if k <= 0: return None
    flat = rng.choice([60, 90, 120, 150, 180, 240, 300, 360, 450, 600]); cp = flat / k
    if cp.denominator != 1 or cp % 50 or cp < 600: return None
    ch = (1 + F(m, 100)) * (1 - F(d, 100)) - 1
    return prac("q-pl-chain", "harder", f"A shopkeeper marks goods {m}% above cost, allows a {d}% discount and a further ₹{flat} off, and still makes a {p}% profit. Find the cost price.",
                cp, [(F(flat) / ch, f"Forgot the {p}% profit that is still made."), (F(flat) / (F(m - d, 100)), f"Used {m} − {d} = {m - d}% as the margin."), (F(flat) / F(p, 100), f"Took the whole ₹{flat} as the {p}% profit.")],
                f"SP = {1 + F(m, 100)} × {1 - F(d, 100)} × CP − {flat} = {float(ch + 1):.4g} CP − {flat}. Set it equal to {1 + F(p, 100)} CP. Then {float(k):.4g} CP = {flat}. CP = {int(cp)}. Check: {float(ch + 1):.4g} × {int(cp)} − {flat} is {1 + F(p, 100)} × {int(cp)}.",
                cp if rupee_chain(cp, m, [d]) - flat == (1 + F(p, 100)) * cp else None, concepts=2, steps=5, tech=["back-substitute", "bounds"])


def t_two_disc_cp(rng):
    d1, d2, p = rng.choice([10, 20, 25]), rng.choice([5, 10, 15, 20]), rng.choice([5, 8, 10, 12, 20])
    cp = rng.choice([800, 1000, 1200, 1500, 2000, 2400, 3000, 4000]); mp = F(cp) * (1 + F(p, 100)) / ((1 - F(d1, 100)) * (1 - F(d2, 100)))
    if mp.denominator != 1 or mp % 10: return None
    sp = mp * (1 - F(d1, 100)) * (1 - F(d2, 100))
    return prac("q-pl-chain", "harder", f"The marked price of an article is {inr(mp)}. After successive discounts of {d1}% and {d2}% it is sold at a {p}% profit. Find the cost price.",
                F(cp), [(mp * (1 - F(d1 + d2, 100)) / (1 + F(p, 100)), f"Added the discounts: {d1}% + {d2}% = {d1 + d2}%."), (sp * (1 + F(p, 100)), "Multiplied by (1 + p) instead of dividing."), (sp - F(p, 100) * sp, f"Took {p}% off the selling price instead of dividing by {1 + F(p, 100)}.")],
                f"SP = {int(mp)} × {1 - F(d1, 100)} × {1 - F(d2, 100)} = {int(sp)}. SP is {100 + p}% of CP. CP = {int(sp)} ÷ {1 + F(p, 100)} = {cp}. The successive discounts together are {d1 + d2 - F(d1 * d2, 100)}%, not {d1 + d2}%. That is why CP is not the sum-based value.",
                F(mp) * (F(100 - d1) * F(100 - d2) / 100) / (100 + p) * F(100, 100) * 1 if False else F(sp * 100, 100 + p), concepts=2, steps=5, tech=["multiplier", "cancel-first"])


def t_weight_simple(rng):
    w, p = rng.choice([800, 840, 880, 900, 920, 950, 960]), rng.choice([0, 0, 10, 20, 25])
    ans = pc((1 + F(p, 100)) * F(1000, w) - 1); sh = F(1000 - w, 10)
    nm = f"sells at cost price" if p == 0 else f"sells at a {p}% profit on the cost of what he hands over"
    return prac("q-pl-weight", "same", f"A dishonest dealer uses a {w} g weight for 1 kg and {nm}. Find his overall gain %." + _ap(ans),
                ans, [(F(p) + sh, "Added the shortage % to the profit % instead of multiplying."), (pc(F(1000 - w, w)) if p else pc(F(1000 - w, 1000)), "Ignored the profit." if p else "Divided by the true weight (1,000) instead of the false weight."), (pc((1 + F(p, 100)) * F(1000, w)), "Gave the multiplier as a percentage without taking off 100.")],
                f"He charges for 1,000 g but hands over {w} g. Multiplier = {1 + F(p, 100)} × 1000/{w} = {float((1 + F(p, 100)) * F(1000, w)):.5g}. Gain = {float(ans):.4g}%.",
                (F(1000 * (100 + p), 100) - F(w)) / F(w) * 100, fmt="pct", tech=["fraction-percent", "multiplier"])


def t_weight_discount(rng):
    m, d, w = rng.choice([10, 20, 25, 30, 40]), rng.choice([5, 10, 15, 20]), rng.choice([800, 840, 900, 920, 950])
    mult = (1 + F(m, 100)) * (1 - F(d, 100)) * F(1000, w); ans = pc(mult - 1)
    return prac("q-pl-weight", "harder", f"A dealer marks goods {m}% above cost, allows a {d}% discount and uses a {w} g weight for 1 kg. Find his profit %." + _ap(ans),
                ans, [(pc((1 + F(m, 100)) * (1 - F(d, 100)) - 1), "Ignored the false weight."), (F(m - d) + F(1000 - w, 10), "Added the percentages."), (pc((1 + F(m, 100)) * (1 - F(d, 100)) * (1 + F(1000 - w, 1000)) - 1), "Took the shortage as a gain on the true weight instead of dividing by the false weight.")],
                f"Markup and discount: {1 + F(m, 100)} × {1 - F(d, 100)} = {float((1 + F(m, 100)) * (1 - F(d, 100))):.4g}. False weight: × 1000/{w}. Multiplier = {float(mult):.5g}. Profit = {float(ans):.4g}%. The effects multiply; they do not add.",
                (rupee_chain(1000, m, [d]) - F(w)) / F(w) * 100, fmt="pct", concepts=3, steps=5, tech=["multiplier", "fraction-percent"])


def t_weight_both(rng):
    b, s, p = rng.choice([1050, 1100, 1200]), rng.choice([800, 900, 950]), rng.choice([0, 0, 10, 20])
    ans = pc((1 + F(p, 100)) * F(b, s) - 1)
    at = "at cost price" if p == 0 else f"at a {p}% profit"
    # second method: buy b-gram-for-1-kg lots until the sold kilos are whole, then count the rupees
    lots = s // gcd(s, b) if False else s
    cost = F(1000) * s                       # buy s lots of 'one kg' (each pays 1000, receives b grams)
    grams = F(b) * s
    sold_kg = grams / s                       # each sold 'kg' is s grams
    receipts = sold_kg * F(1000) * (1 + F(p, 100))
    return prac("q-pl-weight", "harder", f"A dishonest dealer buys with a {b} g weight for 1 kg and sells {at} using a {s} g weight for 1 kg. Find his gain %." + _ap(ans),
                ans, [(pc(F(1000, s) * (1 + F(p, 100)) - 1), "Counted only the cheating on the selling side."), (pc(F(b - 1000, 1000)) + pc(F(1000 - s, 1000)) + F(p), "Added the buying and selling shortages."), (pc((1 + F(p, 100)) * F(s, b) - 1), "Inverted the ratio of the two weights.")],
                f"Paying for 1,000 g he receives {b} g. Selling a 'kilo' he gives only {s} g. So the {b} g he receives is sold as {b}/{s} kilos. Multiplier = {1 + F(p, 100)} × {b}/{s} = {float((1 + F(p, 100)) * F(b, s)):.5g}. Gain = {float(ans):.4g}%.",
                (receipts - cost) / cost * 100, fmt="pct", concepts=2, steps=5, heavy=True, tech=["multiplier", "fraction-percent"])


def t_free_loss(rng):
    n, f_, m, d = rng.choice([3, 4, 5, 6, 9, 10]), rng.choice([1, 2]), rng.choice([0, 20, 25, 30, 40]), rng.choice([0, 10, 20])
    if m == 0 and d: return None
    mult = (1 + F(m, 100)) * (1 - F(d, 100)) * F(n, n + f_); ans = pc(mult - 1)
    if ans == 0: return None
    pre = f"goods marked {m}% above cost, a {d}% discount, and the offer" if (m and d) else (f"goods marked {m}% above cost and the offer" if m else "goods at cost and the offer")
    txt = f"A trader sells {pre} of buy {n}, get {f_} free. Find his overall profit or loss %." + _ap(ans)
    free_unit = F(1) - F(n, n + f_)
    base = (1 + F(m, 100)) * (1 - F(d, 100))
    return prac("q-pl-free", "same", txt, ans,
                [(pc(base - 1), "Ignored the free units."), (pc(base * (1 - F(f_, n)) - 1), f"Took the free units as {f_}/{n} off instead of {f_} in {n + f_}."), (pc(mult), "Gave the multiplier as a percentage without taking off 100.")],
                f"Buyers pay for {n} and receive {n + f_}, so each unit brings {n}/{n + f_} of the price. Price per unit after markup and discount = {float(base):.4g} × cost. Multiplier = {float(base):.4g} × {n}/{n + f_} = {float(mult):.5g}. Result = {float(ans):.4g}%.",
                (base * n * 7 - F(n + f_) * 7) / (F(n + f_) * 7) * 100, fmt="pctsigned", tech=["sign-check", "multiplier"])


def t_free_donation(rng):
    n, f_ = rng.choice([(10, 3), (5, 1), (4, 1), (3, 1), (9, 1)]); U = rng.choice([800, 1000, 1200, 1500, 2000]); don = rng.choice([100, 150, 200, 300])
    cu = rng.choice([40, 50, 60, 80]); mp = rng.choice([70, 80, 100, 110, 120]); d = rng.choice([10, 15, 20])
    out_units = U - don
    if out_units % (n + f_): return None
    payers = F(out_units * n, n + f_); recv = payers * mp * (1 - F(d, 100)); cost = F(U * cu)
    ans = (recv - cost) / cost * 100
    if ans == 0: return None
    pu = mp * (1 - F(d, 100))
    return prac("q-pl-free", "harder", f"A company makes {U} units at ₹{cu} each and donates {don} units. It sells the rest at a {d}% discount on the market price of ₹{mp} a unit, with {f_} units free for every {n} bought. All {U} units are distributed. Find the overall profit or loss %." + _ap(ans),
                ans, [((F(U - don) * pu - cost) / cost * 100, "Ignored the free units."), ((F(U * n, n + f_) * pu - cost) / cost * 100, "Counted the donated units as sold as well."), ((F(out_units) * mp * F(n, n + f_) - cost) / cost * 100, "Forgot the discount.")],
                f"Cost = {U} × {cu} = {int(cost)}. Donated units earn nothing, so {out_units} units reach buyers. Price after discount = {float(pu):.4g}. {f_} free with every {n}: buyers pay for {n} of every {n + f_}, so {float(payers):.5g} units are paid for. Receipts = {float(recv):.6g}. Result = {float(ans):.4g}%.",
                (F(out_units) / (F(n + f_, n)) * pu - cost) / cost * 100, fmt="pctsigned", concepts=3, heavy=True, steps=5, tech=["sign-check", "multiplier", "estimate"])


def t_rate_simple(rng):
    n1, x1, n2, x2 = rng.choice([2, 3, 4, 5, 6, 8, 12]), rng.choice([10, 15, 20, 30, 40, 45]), rng.choice([2, 3, 4, 5, 6, 8, 10]), rng.choice([10, 15, 20, 30, 40, 45, 50])
    ans = pc(F(x2, n2) / F(x1, n1) - 1)
    if ans == 0 or abs(ans) > 120: return None
    it = rng.choice(["pencils", "oranges", "eggs", "pens", "mangoes"])
    L = n1 * n2 // gcd(n1, n2)
    return prac("q-pl-rate", "same", f"{it.capitalize()} are bought at {n1} for ₹{x1} and sold at {n2} for ₹{x2}. Find the profit or loss %." + _ap(ans),
                ans, [(pc(F(x1, n1) / F(x2, n2) - 1), "Divided by the selling price instead of the cost price."), (pc(F(x2, n2) / F(x1, n1)), "Gave SP ÷ CP as a percentage without taking off 100."), (pc(F(n1 - n2, n1)), "Compared the numbers of pieces instead of the prices.")],
                f"Per piece: cost ₹{float(F(x1, n1)):.4g}, sale ₹{float(F(x2, n2)):.4g}. Take {L} pieces: cost {F(x1 * L, n1)}, sale {F(x2 * L, n2)}. Result = {float(ans):.4g}%.",
                (F(x2 * L, n2) - F(x1 * L, n1)) / F(x1 * L, n1) * 100, fmt="pctsigned", tech=["common-unit"])


def t_rate_mix(rng):
    c1, c2 = rng.choice([20, 24, 30, 36, 40, 48]), rng.choice([30, 36, 42, 50, 60, 72]); r1, r2 = rng.choice([(3, 2), (2, 3), (1, 2), (2, 1), (3, 1), (1, 3), (4, 1)])
    if c1 == c2: return None
    avg = F(c1 * r1 + c2 * r2, r1 + r2); sp = rng.choice([x for x in range(25, 80) if x != avg])
    ans = pc(F(sp) / avg - 1)
    simple = F(c1 + c2, 2)
    return prac("q-pl-rate", "harder", f"Two kinds of rice costing ₹{c1} and ₹{c2} a kg are mixed in the ratio {r1} : {r2} and sold at ₹{sp} a kg. Find the profit or loss %." + _ap(ans),
                ans, [(pc(F(sp) / simple - 1), f"Used the simple average ₹{float(simple):.4g} instead of the weighted cost ₹{float(avg):.4g}."), (pc(F(sp) / F(c1 * r2 + c2 * r1, r1 + r2) - 1), "Mixed the ratio the wrong way round."), (F(sp) - avg, "Gave the profit per kg as a percentage.")],
                f"Cost of the mix = ({c1}×{r1} + {c2}×{r2}) ÷ {r1 + r2} = ₹{float(avg):.5g} a kg. The mix always costs between ₹{min(c1, c2)} and ₹{max(c1, c2)}. Result = ({sp} − {float(avg):.5g}) ÷ {float(avg):.5g} = {float(ans):.4g}%.",
                (F(sp) * (r1 + r2) - F(c1 * r1 + c2 * r2)) / F(c1 * r1 + c2 * r2) * 100, fmt="pctsigned", concepts=2, steps=5, tech=["sign-check", "estimate"])


def t_rate_mix3(rng):
    kinds = rng.sample([("wheat", 5, 40), ("rye", 6, 45), ("oats", 4, 36), ("maize", 8, 56), ("barley", 3, 27), ("millet", 10, 90)], 3)
    w = rng.choice([(2, 2, 3), (1, 2, 3), (3, 1, 2), (2, 3, 4)]); ns, xs = rng.choice([3, 4, 5, 6]), rng.choice([20, 24, 25, 28, 30, 32, 40])
    costs = [F(x, n) for _, n, x in kinds]; avg = sum(a * b for a, b in zip(w, costs)) / sum(w); sp = F(xs, ns)
    ans = pc(sp / avg - 1)
    if ans == 0 or abs(ans) > 150: return None
    simple = sum(costs) / 3
    L = 1
    for d_ in [avg.denominator, sp.denominator]: L = L * d_ // gcd(L, d_)
    return prac("q-pl-rate", "harder", f"A baker buys " + ", ".join(f"{k} at {n} for ₹{x}" for k, n, x in kinds) + f", mixes them in the ratio {w[0]} : {w[1]} : {w[2]} and sells all of it at {ns} for ₹{xs}. Find the profit or loss %." + _ap(ans),
                ans, [(pc(sp / simple - 1), "Used the simple average of the three costs."), (pc(sp / (sum(a * b for a, b in zip(w[::-1], costs)) / sum(w)) - 1), "Used the ratio in the wrong order."), (pc(sp / max(costs) - 1), "Took the dearest cost as the cost of the mix.")],
                "Cost per piece: " + ", ".join(f"{k} {float(c):.4g}" for (k, _, _), c in zip(kinds, costs)) + f". Mix of {sum(w)} pieces costs {float(avg * sum(w)):.5g}, i.e. {float(avg):.5g} each. Selling price per piece = {float(sp):.5g}. Multiply both by {L} to clear fractions: cost {avg * L}, sale {sp * L}. Result = {float(ans):.4g}%.",
                ((sp * L) - (avg * L)) / (avg * L) * 100, fmt="pctsigned", concepts=2, heavy=True, steps=5, tech=["sign-check", "common-unit", "estimate"])


def t_equal_cp(rng):
    cp = rng.choice([1500, 2000, 2400, 2500, 3000, 3600, 4000, 5000, 6400]); k = rng.choice([100, 150, 200, 250, 300, 400, 500, 600])
    if k >= cp: return None
    s1, s2 = cp + k, cp - k
    if rng.random() < 0.5:
        return prac("q-pl-equal", "same", f"The profit made when an article is sold for ₹{s1} equals the loss made when it is sold for ₹{s2}. Find its cost price.",
                    F(cp), [(F(s1), "Took the higher price."), (F(s2), "Took the lower price."), (F(s1 + s2), "Added the two prices without halving.")],
                    f"₹{s1} − CP = CP − ₹{s2}, so CP = ({s1} + {s2}) ÷ 2 = ₹{cp}.", F(cp) if (s1 - cp) == (cp - s2) else None, tech=["symmetry"])
    ans = F(k, cp) * 100
    return prac("q-pl-equal", "same", f"The profit made at a selling price of ₹{s1} equals the loss made at ₹{s2}. Find the profit % at ₹{s1}." + _ap(ans),
                ans, [(F(s1 - cp, s1) * 100, "Took the profit on the selling price instead of the cost."), (F(s1 - cp, s2) * 100, "Divided by the lower selling price."), (F(s1 - s2, cp) * 100, "Used the gap between the two prices as the profit.")],
                f"CP = ({s1} + {s2}) ÷ 2 = {cp}. Profit = {s1} − {cp} = {k}. Profit % = {k} ÷ {cp} × 100 = {float(ans):.4g}%.", F(s1 - s2, s1 + s2) * 100, fmt="pct", tech=["symmetry", "fraction-percent"])


def t_equal_target(rng):
    cp = rng.choice([1500, 2000, 2400, 2500, 3000, 4000, 5000, 6400]); k = rng.choice([100, 150, 200, 250, 300, 400, 500]); p = rng.choice([5, 10, 12, 15, 20, 25])
    if k >= cp: return None
    s1, s2 = cp + k, cp - k; target = F(cp) * (1 + F(p, 100))
    if target.denominator != 1: return None
    return prac("q-pl-equal", "harder", f"The profit at a selling price of ₹{s1} equals the loss at ₹{s2}. At what selling price will there be a {p}% profit?",
                target, [(F(s1) * (1 + F(p, 100)), f"Took {p}% on the higher price."), (F(cp) + p, f"Added {p} rupees instead of {p}%."), (F(s1 + s2) * (1 + F(p, 100)), "Skipped the halving when finding the cost.")],
                f"CP = ({s1} + {s2}) ÷ 2 = {cp}. A {p}% profit means SP = {cp} × {1 + F(p, 100)}. SP = ₹{int(target)}. The cost is the midpoint, so no calculation with the higher or lower price is needed. Only the cost matters.",
                F(cp + (s1 - cp) * 0) * (100 + p) / 100 if (s1 - cp) == (cp - s2) else None, concepts=2, steps=5, tech=["symmetry", "multiplier"])


def t_equal_same_sp(rng):
    x = rng.choice([10, 20, 25, 40, 50]); sp = rng.choice([900, 1200, 1500, 1800, 2400, 3000, 3600, 4500])
    c1, c2 = F(sp) / (1 + F(x, 100)), F(sp) / (1 - F(x, 100))
    if c1.denominator != 1 or c2.denominator != 1: return None
    loss = c1 + c2 - 2 * sp
    return prac("q-pl-equal", "harder", f"Two articles are sold at ₹{sp} each, one at a {x}% profit and the other at a {x}% loss. Find the total gain or loss in rupees.",
                -loss, [(F(0), f"Thought +{x}% and −{x}% cancel."), (loss, "Got the size right but the sign wrong."), (-F(x * 2 * sp, 100), f"Took {x}% of the total selling price.")],
                f"Costs: {sp} ÷ {1 + F(x, 100)} = {int(c1)} and {sp} ÷ {1 - F(x, 100)} = {int(c2)}. Total cost = {int(c1 + c2)}. Total selling price = {2 * sp}. The difference is a loss of {int(loss)}. As a % of total cost it is {x}²/100 = {F(x * x, 100)}%. It is never a gain.",
                -(F(x * x, 100) / 100) * (c1 + c2), fmt="inrsigned", concepts=2, steps=5, tech=["symmetry", "sign-check"])


def practice_items():
    out = _hand_items()
    out += variants(PREFIX, "chain-profit", 2, t_chain_profit)
    out += variants(PREFIX, "chain-flat", 2, t_chain_flat)
    out += variants(PREFIX, "two-disc-cp", 2, t_two_disc_cp)
    out += variants(PREFIX, "weight-simple", 3, t_weight_simple)
    out += variants(PREFIX, "weight-discount", 2, t_weight_discount)
    out += variants(PREFIX, "weight-both", 2, t_weight_both)
    out += variants(PREFIX, "free-loss", 3, t_free_loss)
    out += variants(PREFIX, "free-donation", 3, t_free_donation)
    out += variants(PREFIX, "rate-simple", 3, t_rate_simple)
    out += variants(PREFIX, "rate-mix", 2, t_rate_mix)
    out += variants(PREFIX, "rate-mix3", 2, t_rate_mix3)
    out += variants(PREFIX, "equal-cp", 2, t_equal_cp)
    out += variants(PREFIX, "equal-target", 2, t_equal_target)
    out += variants(PREFIX, "equal-same-sp", 2, t_equal_same_sp)
    return out
