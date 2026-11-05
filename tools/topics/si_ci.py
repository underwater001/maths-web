"""Simple and compound interest: quiz tier."""
import math
from bank import bound, mistake, pyq
from topics._si_ry import PYQS_RY
from topics._ci_ry import PYQS_RY as PYQS_CI

TOPIC = "si-ci"
PREFIX = "ci"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-ci-growth": {"short": "Compound growth", "label": "Compound interest is repeated multiplication", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "Each year the amount is multiplied by the same factor (1 + r/100). So times and powers move together.", "links": ["percentage"]},
    "c-si-line": {"short": "Simple interest", "label": "Simple interest is a straight line", "kind": "concept", "parent": TOPIC, "order": 2,
                  "summary": "Interest = P × r × t ÷ 100. With several loans at one rate, add P × t for each and divide once.", "links": ["profit-loss"]},
    "q-ci-multiple": {"short": "Time to multiply", "label": "How long to grow k times?", "kind": "qtype", "parent": "c-ci-growth", "order": 1,
                      "summary": "It triples in 6 years; how long to become 27 times?", "links": []},
    "q-ci-find": {"short": "Find principal / rate", "label": "Principal or rate from two amounts", "kind": "qtype", "parent": "c-ci-growth", "order": 2,
                  "summary": "A sum becomes A₁ after n years and A₂ after n + 1 years; find the rate or the principal.", "links": []},
    "q-ci-fractional": {"short": "Years and months", "label": "Compound interest for years and months", "kind": "qtype", "parent": "c-ci-growth", "order": 3,
                        "summary": "2 years 9 months with annual compounding: compound the whole years, simple interest on the rest.", "links": []},
    "q-si-two": {"short": "Two loans", "label": "Simple interest on two loans at one rate", "kind": "qtype", "parent": "c-si-line", "order": 1,
                 "summary": "Two principals for different times, total interest known; find the rate.", "links": []},
    "q-si-basic": {"short": "Find P, R or T", "label": "Basic: interest, rate, time or principal", "kind": "qtype", "parent": "c-si-line", "order": 2,
                   "summary": "Three of P, R, T and the interest are given; find the fourth. Includes day counts, equal-interest pairs and rupee-years.", "links": []},
    "q-si-multiple": {"short": "Doubles / trebles", "label": "A sum becomes k times itself", "kind": "qtype", "parent": "c-si-line", "order": 3,
                      "summary": "Doubles in n years; find the rate or the time to become 3, 4 or 5 times. Also interest as a fraction of the sum.", "links": []},
    "q-si-difference": {"short": "Rate gap", "label": "Extra interest from a higher rate", "kind": "qtype", "parent": "c-si-line", "order": 4,
                        "summary": "A rate 2% higher (or one more year) gives Rs. X more; the extra interest is a percent of the principal.", "links": []},
    "q-si-parts": {"short": "Split the money", "label": "Money split into parts at different rates", "kind": "qtype", "parent": "c-si-line", "order": 5,
                   "summary": "A sum lent in parts at different rates; find a part, a missing rate or the average rate.", "links": ["mixture-alligation"]},
    "q-si-amounts": {"short": "Two amounts", "label": "Amounts given, find principal or rate", "kind": "qtype", "parent": "c-si-line", "order": 6,
                     "summary": "The amount after one time and after another (or a ratio of P : A) is given; the gap between them is the interest.", "links": []},
    "q-ci-basic": {"short": "Find CI / amount / sum", "label": "Basic compound interest: amount, interest or sum", "kind": "qtype", "parent": "c-ci-growth", "order": 4,
                   "summary": "Find the amount, the compound interest or the sum; includes changing rates by year and the matching simple interest.", "links": []},
    "q-ci-diff": {"short": "CI − SI difference", "label": "Difference between compound and simple interest", "kind": "qtype", "parent": "c-ci-growth", "order": 5,
                  "summary": "The gap between CI and SI for 2 or 3 years is known; find the sum or the rate. Also with half-yearly compounding.", "links": []},
    "q-ci-half": {"short": "Half-yearly / quarterly", "label": "Compounded half-yearly or quarterly", "kind": "qtype", "parent": "c-ci-growth", "order": 6,
                  "summary": "Halve (or quarter) the rate and double (or quadruple) the number of periods; also yearly versus half-yearly and years-and-months.", "links": []},
    "q-ci-install": {"short": "Equal instalments", "label": "Loans repaid in equal instalments", "kind": "qtype", "parent": "c-ci-growth", "order": 7,
                     "summary": "A loan repaid in two equal yearly instalments: the instalments, discounted year by year, add up to the loan.", "links": []},
    "q-ci-growth": {"short": "Growth and depreciation", "label": "Population, price or value growth", "kind": "qtype", "parent": "c-ci-growth", "order": 8,
                    "summary": "A value grows or falls by a fixed percent each year: multiply by (1 ± r/100) once per year.", "links": ["percentage"]},
}
FORMULAS = [
    {"id": "ci-f1", "node": "c-ci-growth", "text": "A = P(1 + r/100)ⁿ     CI = A − P", "note": "Growth factor per year = 1 + r/100."},
    {"id": "ci-f2", "node": "c-ci-growth", "text": "If the amount multiplies by m in t years, it multiplies by mᵏ in kt years", "note": "Triples in 6 years → 27 times (3³) in 18 years."},
    {"id": "ci-f3", "node": "c-ci-growth", "text": "r = (A₃ − A₂) ÷ A₂ × 100 for two consecutive years", "note": "The gain in one year on the earlier amount."},
    {"id": "ci-f4", "node": "c-ci-growth", "text": "Part of a year at the end: simple interest on the amount at the end of the whole years", "note": "2 y 9 m: compound 2 years, then SI for 9/12 year on that amount."},
    {"id": "ci-f5", "node": "c-si-line", "text": "Total SI = r × (P₁t₁ + P₂t₂) ÷ 100", "note": "One rate: add the P × t products before dividing."},
    {"id": "ci-f6", "node": "c-si-line", "text": "SI = P × R × T ÷ 100     A = P + SI = P(1 + RT/100)", "note": "R is a percent per year, T in years (months ÷ 12, days ÷ 365)."},
    {"id": "ci-f7", "node": "c-si-line", "text": "Interest = P × (R × T)%: treat R × T as the percent of P earned", "note": "6% for 5 years is 30% of P, so SI = 0.3 P."},
    {"id": "ci-f8", "node": "c-si-line", "text": "Doubles in n years → rate = 100 ÷ n %; becomes k times in (k − 1) × n years", "note": "Doubles in 10 y → trebles in 20 y, 5 times in 40 y."},
    {"id": "ci-f9", "node": "c-si-line", "text": "Amounts at two times: SI per year = (A₂ − A₁) ÷ (T₂ − T₁); P = A₁ − T₁ × (SI per year)", "note": "720 after 2 y, 1,020 after 7 y: Rs. 60 a year, P = 600."},
    {"id": "ci-f10", "node": "c-si-line", "text": "Extra rate d% for T years adds (d × T)% of P", "note": "3% more for 2 years gives Rs. 72 more: 6% of P = 72, P = 1,200."},
    {"id": "ci-f11", "node": "c-si-line", "text": "Equal instalments x for n years at r%: total paid = nx + r% × x × (0 + 1 + … + (n − 1))", "note": "4 years at 5%: 4x + 0.05 × 6x = 4.3x."},
    {"id": "ci-f12", "node": "c-ci-growth", "text": "2 years: CI − SI = P (r/100)²     3 years: CI − SI = P (3r² + r³) (r as a decimal)", "note": "5% for 2 years: 0.25% of P. 5% for 3 years: 0.7625% of P."},
    {"id": "ci-f13", "node": "c-ci-growth", "text": "CI − SI (2 years) = rate × one year's interest", "note": "SI 270 in 2 y → 135 a year; CI − SI = 12.15 → rate = 12.15 ÷ 135 = 9%."},
    {"id": "ci-f14", "node": "c-ci-growth", "text": "Half-yearly: rate ÷ 2, periods × 2.   Quarterly: rate ÷ 4, periods × 4", "note": "12% half-yearly for 1 year = 6% twice: 1.06² = 1.1236."},
    {"id": "ci-f15", "node": "c-ci-growth", "text": "Instalments x for n years: loan = x/(1 + r) + x/(1 + r)² + …", "note": "5%, 2 years: 1,859.4 per 1,000 of instalment; x = 12,300 ÷ 1.859 ≈ 6,615."},
    {"id": "ci-f16", "node": "c-ci-growth", "text": "Changing rates: multiply the yearly factors (1.04 × 1.05 × 1.06 for 4%, 5%, 6%)", "note": "Do not add the rates."},
    {"id": "ci-f17", "node": "c-ci-growth", "text": "Part of a year at the end: compound whole years, then simple interest on the amount", "note": "2 years 4 months at 15%: ×1.15² then ×(1 + 0.15 × 4/12)."},
]
METHODS = {
    "q-ci-multiple": {
        "cue": "'It triples (or doubles) in n years. When will it become k times?'",
        "formulas": ["ci-f2"], "tech": ["scaling", "standard-values"],
        "standard": "Triples in 6 years. 27 = 3 × 3 × 3, so three tripling periods: 3 × 6 = 18 years.",
        "fast": "Write the target as a power of the growth factor (27 = 3³) and multiply the time by the power.",
        "eliminate": "The answer is a whole multiple of 6, so only the option that is a multiple of 6 survives (18 of 18, 19, 20, 21).",
        "traps": ["Taking 27 ÷ 3 = 9 and then 9 × 6 = 54, treating growth as simple.", "Adding instead of multiplying (6 + 6 + 6 + 6 = 24)."]},
    "q-ci-find": {
        "cue": "Two amounts at consecutive years (7,200 after 2 years and 8,640 after 3).",
        "formulas": ["ci-f3", "ci-f1"], "tech": ["back-substitute", "estimate"],
        "standard": "Rate = (8,640 − 7,200) ÷ 7,200 = 20%. P = 7,200 ÷ 1.2² = 7,200 ÷ 1.44 = ₹5,000.",
        "fast": "7,200 ÷ 1.44: 1.44 × 5,000 = 7,200.",
        "eliminate": "The principal times 1.44 is 7,200. Test options: 5,000 × 1.44 = 7,200 exactly; 4,800 × 1.44 = 6,912 and 5,200 × 1.44 = 7,488.",
        "traps": ["Dividing by 1.2 once instead of twice.", "Using the 3-year amount with 2 years of growth.", "Calling the rate 1,440 ÷ 8,640."]},
    "q-ci-fractional": {
        "cue": "Time like 2 years 9 months, 'interest compounded annually'.",
        "formulas": ["ci-f1", "ci-f4"], "tech": ["multiplier", "estimate"],
        "standard": "Compound 2 years: 12,000 × 1.08² = 13,996.80. Then simple interest for 9 months at 8%: 13,996.80 × 8% × 9/12 = 839.81. CI = 13,996.80 + 839.81 − 12,000 ≈ ₹2,837.",
        "fast": "Multiplier = 1.1664 × 1.06 = 1.236384, so CI = 12,000 × 0.236384 ≈ ₹2,837.",
        "eliminate": "Two full years alone give about ₹1,997 (12,000 × 0.1664), and 9 more months add about 6% of ₹14,000 ≈ ₹840. That is just under ₹2,840, so only 2,837 fits.",
        "traps": ["Compounding the 9 months as (1.08)^(9/12).", "Using simple interest for all 2 y 9 m.", "Computing 9 months as 9% instead of 6% (8% × 9/12)."]},
    "q-si-two": {
        "cue": "Two loans (or investments) at the same simple-interest rate and one total interest.",
        "formulas": ["ci-f5"], "tech": ["cancel-first", "estimate"],
        "standard": "6,000 × 3 + 4,000 × 2 = 18,000 + 8,000 = 26,000. Rate = 2,000 × 100 ÷ 26,000 ≈ 7.69% → 8%.",
        "fast": "Interest 2,000 on 26,000 'rupee-years' is just under 8%.",
        "eliminate": "Even at 10%, 26,000 'rupee-years' would give ₹2,600. The actual ₹2,000 is lower, so the rate must be below 10%: only 8% fits.",
        "traps": ["Dividing by total principal 10,000 instead of rupee-years (gives 20%).", "Using the years separately instead of P × t."]},
    "q-si-basic": {
        "cue": "'Find the rate / time / principal / interest' with plain numbers, or two loans at one rate.",
        "formulas": ["ci-f6", "ci-f7"], "tech": ["units-first", "cancel-first", "common-unit"],
        "standard": "Rate = SI × 100 ÷ (P × T). For two deposits add the rupee-years first: 400 × 2 + 550 × 4 + 1,200 × 6 = 10,200, so 1,020 ÷ 10,200 = 10%.",
        "fast": "Turn R × T into one percent of P and cancel: 30% of 6,000 = 1,800 at once.",
        "eliminate": "Estimate the answer's size first: interest ÷ principal gives R × T, and the options usually differ by whole steps.",
        "traps": ["Leaving months or days unconverted (6 years 8 months is 6 2/3 years).", "Counting both end dates in a day-count (the first day is not counted).", "Dividing by the total principal instead of the rupee-years."]},
    "q-si-multiple": {
        "cue": "'Doubles / trebles in n years' or 'SI is 1/4 of the sum'.",
        "formulas": ["ci-f8", "ci-f7"], "tech": ["fraction-percent", "ratio-parts", "standard-values"],
        "standard": "Trebles in 15 years means interest 2P in 15 years, so P every 7.5 years. 5 times needs 4P: 4 × 7.5 = 30 years.",
        "fast": "Each 'P of interest' takes the same time. Doubles in n: k times in (k − 1)n.",
        "eliminate": "Time for k times is (k − 1) multiples of the doubling time, so the answer must be a multiple of it.",
        "traps": ["Taking trebles as 3 × the time (it is 2 × the doubling time).", "Using the amount, not the interest, as the multiple.", "When SI = P/4 and T = R: r² = 25, so r = 5, not 25."]},
    "q-si-difference": {
        "cue": "'Had the rate been x% higher it would have fetched Rs. … more' or 'the difference in interest is …'.",
        "formulas": ["ci-f10"], "tech": ["units-first"],
        "standard": "3% extra for 2 years = 6% of P = 72, so P = Rs. 1,200.",
        "fast": "Multiply the rate gap by the years and read it as a percent of the sum; divide the money gap by it.",
        "eliminate": "The answer must make the extra percent × P equal the gap exactly, so test one option.",
        "traps": ["Using the old rate instead of the gap.", "Forgetting to multiply by the years."]},
    "q-si-parts": {
        "cue": "'Divided into two parts / lends part at … and rest at …'.",
        "formulas": ["ci-f6", "ci-f7"], "tech": ["ratio-parts", "common-unit"],
        "standard": "Equal interest on two parts: P₁ × (R₁T₁) = P₂ × (R₂T₂), so P₁ : P₂ = R₂T₂ : R₁T₁. For 12,000 split at 3 y 12% and 4.5 y 16%: 72 : 36 = 2 : 1, so 8,000 and 4,000.",
        "fast": "The parts are inversely proportional to rate × time. For an average rate use weights (alligation).",
        "eliminate": "The larger part belongs to the smaller R × T.",
        "traps": ["Writing the ratio the wrong way round.", "Forgetting the second part's fraction is of the remainder (50% of the rest)."]},
    "q-si-amounts": {
        "cue": "'Amounts to … in … years and … in … years' or 'ratio of principal and amount is …'.",
        "formulas": ["ci-f9"], "tech": ["units-first", "multiplier"],
        "standard": "880 after 2 years, 920 after 3: interest per year = 40, P = 880 − 2 × 40 = 800.",
        "fast": "Subtract the two amounts to get interest per year; take away the earlier years' interest to reach P.",
        "eliminate": "P is always smaller than the smaller amount by (years × yearly interest).",
        "traps": ["Taking the later amount as the principal.", "Dividing the gap by the later time instead of the time difference."]},
    "q-ci-basic": {
        "cue": "'Find the amount / compound interest / sum'; rates that change each year; 'CI is … find the SI'.",
        "formulas": ["ci-f1", "ci-f16"], "tech": ["multiplier", "standard-values", "back-substitute"],
        "standard": "Chain the yearly multipliers: 10,000 × 1.04 × 1.05 × 1.06 = 11,575.20, so CI = 1,575.20. CI for 2 years at 5% is 10.25% of P; use it to get P and then the SI.",
        "fast": "Memorise 1.05² = 1.1025, 1.1² = 1.21, 1.1³ = 1.331, 1.2² = 1.44, 1.05³ = 1.157625. CI ÷ factor gives P, and the SI is just rate × years of P.",
        "eliminate": "SI for the same sum is always a little less than the CI; the amount is always above the sum, the interest is not.",
        "traps": ["Giving the amount when the interest is asked (6,655 for 1,655).", "Adding the yearly rates instead of multiplying the factors.", "Using the 2-year factor as 1 + 2r."]},
    "q-ci-diff": {
        "cue": "'The difference between compound and simple interest for 2 (or 3) years is Rs. …'.",
        "formulas": ["ci-f12", "ci-f13"], "tech": ["standard-values", "fraction-percent"],
        "standard": "2 years at 5%: CI − SI = P × 0.0025 = 15, so P = 6,000. 3 years at 5%: CI − SI = 0.007625 P = 36.60, so P = 4,800.",
        "fast": "2 years: the difference is the interest on the first year's interest, r% of one year's interest. 3 years at r%: P (3r² + r³).",
        "eliminate": "Try one option: for 2 years at r% the difference is exactly P × r²/10,000.",
        "traps": ["Using the 2-year formula for 3 years.", "Writing r as a percent in the formula (use 0.05).", "Mixing the sign: CI is the larger."]},
    "q-ci-half": {
        "cue": "'Compounded half-yearly / quarterly / semi-annually', or 'for 1 1/2 years' and '2 years 4 months'.",
        "formulas": ["ci-f14", "ci-f17"], "tech": ["standard-values", "multiplier"],
        "standard": "20% quarterly for 9 months: rate 5%, 3 periods. 1.05³ − 1 = 0.157625, so CI = 16,000 × 0.157625 = 2,522. For a time like 2 years 4 months at 15% yearly: 8,000 × 1.15² = 10,580, then × (1 + 0.15 × 4/12).",
        "fast": "Recognise the factor: 1.157625 = 1.05³ means 3 periods at 5%; the number of periods gives the time.",
        "eliminate": "Half-yearly gives a slightly larger amount than yearly at the same rate (not smaller).",
        "traps": ["Halving the rate but not doubling the periods.", "Using the annual rate for each half-year.", "Compounding the leftover months instead of simple interest on them."]},
    "q-ci-install": {
        "cue": "'Repaid in two equal annual instalments' at compound interest.",
        "formulas": ["ci-f15"], "tech": ["back-substitute", "multiplier"],
        "standard": "Loan = x/1.05 + x/1.05². For x = 17,640: 16,800 + 16,000 = 32,800. To find x: 12,300 = x × 1.859, so x = 6,615.",
        "fast": "To check an option, divide it by 1.05 once and twice and add. For a loan L: x = L × (1.05)² ÷ (2 + 0.05) = L × 1.1025 ÷ 2.05.",
        "eliminate": "Two instalments must add to more than the loan but less than loan × 1.1025.",
        "traps": ["Dividing the loan by 2 (ignores the interest).", "Applying one year's factor to both instalments.", "Using the same factor for the first and second payment."]},
    "q-ci-growth": {
        "cue": "'Value depreciates by 4% every year' / 'population increases by …'.",
        "formulas": ["ci-f1"], "tech": ["multiplier", "cancel-first"],
        "standard": "Depreciation multiplies by (1 − r/100) each year: 62,500 × 0.96² = 57,600.",
        "fast": "62,500 × 0.96 = 60,000, then 60,000 × 0.96 = 57,600. Go forward by multiplying, backward by dividing.",
        "eliminate": "Two falls of 4% take off a little less than 8% in all (7.84%), so the value is just above 92% of 62,500 = 57,500: only 57,600 fits.",
        "traps": ["Subtracting 8% in one step.", "Using 1.04 instead of 0.96."]},
}
PYQS = [
    pyq(S1, 60, "q-ci-multiple", "An amount triples in 6 years at compound interest. How many years will it take to become 27 times its original value?", ["18", "19", "20", "21"], "a",
        ["27 = 3 × 3 × 3 = 3³.", "Each tripling takes 6 years, so 3 × 6 = 18 years."], lambda: 6 * math.log(27, 3), 18, 1e-9, tech=["scaling"],
        trick="The time is a multiple of 6 (three tripling periods): only 18 qualifies.",
        wrong={k: bound(f"Three tripling periods of 6 years make 18 years, a multiple of 6; {o} is not.", lambda v: v % 6 != 0) for k, o in (("b", "19"), ("c", "20"), ("d", "21"))}),
    pyq(S1, 64, "q-ci-find", "A sum becomes ₹7,200 in 2 years and ₹8,640 in 3 years at compound interest. Find the original principal.", ["₹4,800", "₹5,000", "₹5,200", "₹5,500"], "b",
        ["The third year added 8,640 − 7,200 = ₹1,440 on ₹7,200: 20% a year.", "P × 1.2² = 7,200, so P = 7,200 ÷ 1.44 = ₹5,000."],
        lambda: 7200 / (8640 / 7200) ** 2, 5000, 1e-6, tech=["back-substitute", "scaling"],
        trick="Try 5,000: × 1.2 = 6,000, × 1.2 = 7,200 ✓."),
    pyq(S2, 59, "q-ci-fractional", "Find the compound interest on ₹12,000 at 8% per annum for 2 years 9 months, with interest compounded annually.", ["₹2,456", "₹2,598", "₹2,712", "₹2,837"], "d",
        ["After 2 years: 12,000 × 1.08² = ₹13,996.80.", "Simple interest on that for 9 months at 8%: 13,996.80 × 0.08 × 9/12 = ₹839.81.", "Total CI = 13,996.80 + 839.81 − 12,000 ≈ ₹2,837."],
        lambda: 12000 * 1.08 ** 2 * (1 + 0.08 * 9 / 12) - 12000, 2837, 1, tech=["multiplier", "estimate"], concepts=2, heavy=True,
        trick="Multiplier 1.1664 × 1.06 = 1.2364; 12,000 × 0.2364 ≈ ₹2,837.",
        wrong={k: bound(f"Two full years give about ₹1,997 and the extra 9 months about ₹840, so the CI is about ₹2,837. {o} is not near it.", lambda v: abs(v - 2836.6) > 1) for k, o in (("a", "₹2,456"), ("b", "₹2,598"), ("c", "₹2,712"))}),
    pyq(S3, 73, "q-si-two", "X lent ₹6,000 to Y for 3 years and ₹4,000 to Z for 2 years, both at the same simple interest rate. In total he received ₹2,000 as interest. Find the rate per annum (nearest integer).", ["8%", "10%", "12%", "15%"], "a",
        ["P × t: 6,000 × 3 = 18,000 and 4,000 × 2 = 8,000, so 26,000 in all.", "Rate = 2,000 × 100 ÷ 26,000 ≈ 7.69%, which is 8% to the nearest whole number."],
        lambda: 2000 / (6000 * 3 + 4000 * 2) * 100, 8, 0.5, tech=["cancel-first", "estimate"],
        trick="At 10% the interest would be ₹2,600, more than ₹2,000. So the rate is below 10%.",
        wrong={k: bound(f"At {o} the interest on 26,000 rupee-years would be ₹{int(o[:-1]) * 260:,}, more than ₹2,000.", lambda v: v >= 10) for k, o in (("b", "10%"), ("c", "12%"), ("d", "15%"))}),
]

PYQS = PYQS + PYQS_RY + PYQS_CI


def practice_items():
    return []
