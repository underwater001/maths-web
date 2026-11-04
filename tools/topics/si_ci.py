"""Simple and compound interest: quiz tier."""
import math
from bank import bound, mistake, pyq

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
}
FORMULAS = [
    {"id": "ci-f1", "node": "c-ci-growth", "text": "A = P(1 + r/100)ⁿ     CI = A − P", "note": "Growth factor per year = 1 + r/100."},
    {"id": "ci-f2", "node": "c-ci-growth", "text": "If the amount multiplies by m in t years, it multiplies by mᵏ in kt years", "note": "Triples in 6 years → 27 times (3³) in 18 years."},
    {"id": "ci-f3", "node": "c-ci-growth", "text": "r = (A₃ − A₂) ÷ A₂ × 100 for two consecutive years", "note": "The gain in one year on the earlier amount."},
    {"id": "ci-f4", "node": "c-ci-growth", "text": "Part of a year at the end: simple interest on the amount at the end of the whole years", "note": "2 y 9 m: compound 2 years, then SI for 9/12 year on that amount."},
    {"id": "ci-f5", "node": "c-si-line", "text": "Total SI = r × (P₁t₁ + P₂t₂) ÷ 100", "note": "One rate: add the P × t products before dividing."},
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


def practice_items():
    return []
