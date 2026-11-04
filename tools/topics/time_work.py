"""Time and Work: quiz tier."""
from fractions import Fraction as F
from bank import bound, mistake, pyq, mixed_val

TOPIC = "time-work"
PREFIX = "tw"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-tw-rate": {"short": "Work per day", "label": "One day's work: rate = 1 ÷ days", "kind": "concept", "parent": TOPIC, "order": 1,
                  "summary": "Convert every time to a work rate and add rates when people work together.", "links": ["ratio-proportion"]},
    "c-tw-lcm": {"short": "LCM units", "label": "Total work as the LCM: units of work", "kind": "concept", "parent": TOPIC, "order": 2,
                 "summary": "Pick the total work as the LCM of the times; every rate becomes a whole number.", "links": ["number-system"]},
    "c-tw-pattern": {"short": "Alternating work", "label": "People joining on a pattern or leaving midway", "kind": "concept", "parent": TOPIC, "order": 3,
                     "summary": "Work out one full cycle, count whole cycles, then finish the remainder.", "links": []},
    "q-tw-together": {"short": "Together, remaining", "label": "Working together for some time: fraction left", "kind": "qtype", "parent": "c-tw-rate", "order": 1,
                      "summary": "Add the rates, multiply by the time, subtract from 1.", "links": []},
    "q-tw-efficiency": {"short": "Efficiency ratio", "label": "Efficiency ratio against days", "kind": "qtype", "parent": "c-tw-rate", "order": 2,
                        "summary": "Efficiency is inversely proportional to days; swap the ratio.", "links": []},
    "q-tw-leave": {"short": "Leaves midway", "label": "One worker or pump stops partway", "kind": "qtype", "parent": "c-tw-lcm", "order": 1,
                   "summary": "Work done by all, then the remainder done by the rest. Pipes and cisterns are the same.", "links": []},
    "q-tw-cycle": {"short": "Join every third day", "label": "Workers join in a repeating pattern", "kind": "qtype", "parent": "c-tw-pattern", "order": 1,
                   "summary": "One cycle's work, whole cycles, then a part-day.", "links": []},
}
FORMULAS = [
    {"id": "tw-f1", "node": "c-tw-rate", "text": "Rate = 1 ÷ days. Together: 1/a + 1/b + 1/c per day", "note": "Time together = 1 ÷ (sum of rates)."},
    {"id": "tw-f2", "node": "c-tw-rate", "text": "Efficiency ∝ 1 ÷ days: efficiency A : B = days B : days A", "note": "4 : 3 efficiency means 3 : 4 time."},
    {"id": "tw-f3", "node": "c-tw-lcm", "text": "Total work = LCM of the times; rate = LCM ÷ days", "note": "For 12 and 18: total 36, rates 3 and 2."},
    {"id": "tw-f4", "node": "c-tw-pattern", "text": "Cycle work = sum of the work done over one repeat; days = whole cycles × length + part of the next", "note": "Finish inside a day by dividing the remaining work by that day's rate."},
]
METHODS = {
    "q-tw-together": {
        "cue": "'X takes … days, Y takes … days. They work together for … days. What fraction remains?'",
        "formulas": ["tw-f1", "tw-f3"], "tech": ["lcm-units", "fraction-percent"],
        "standard": "Rates 1/12 + 1/18 = 5/36 per day; in 3 days 15/36 = 5/12 is done; remaining 1 − 5/12 = 7/12.",
        "fast": "LCM 36: X = 3, Y = 2, together 5 a day; 3 days = 15 of 36, so 21/36 = 7/12 is left.",
        "eliminate": "Together they need under 7.2 days, so 3 days is less than half the work done: the remaining fraction must be above 1/2, which strikes 1/3 and 5/12.",
        "traps": ["Giving the fraction done (5/12) rather than the fraction left.", "Adding the days instead of the rates.", "Mixing both times into one rate before taking the LCM."]},
    "q-tw-efficiency": {
        "cue": "'The ratio of efficiencies of A and B is 4 : 3. If A takes 18 days, how long does B take?'",
        "formulas": ["tw-f2"], "tech": ["ratio-parts", "scaling"],
        "standard": "Efficiency is inverse to days: A : B days = 3 : 4; A = 18 days is 3 parts, so 1 part = 6 and B = 24 days.",
        "fast": "The slower worker (B) takes more days: 18 × 4/3 = 24.",
        "eliminate": "B is less efficient, so takes more than 18 days; and 18 × 4/3 is exactly 24. Strike options that make B faster.",
        "traps": ["Multiplying by 3/4 (13.5) instead of 4/3.", "Treating the ratio as the days ratio."]},
    "q-tw-leave": {
        "cue": "Several pumps or workers, one leaves after some time, how much more time to finish?",
        "formulas": ["tw-f1", "tw-f3"], "tech": ["lcm-units", "relative"],
        "standard": "All three: 1/5 + 1/7 + 1/10 = 31/70 per hour. In 1.5 h they do 93/140, leaving 47/140. A + B = 12/35 = 48/140 per hour, so the time is 47/48 hour.",
        "fast": "LCM 70: A = 14, B = 10, C = 7, all three 31 per hour; 1.5 h = 46.5 done, 23.5 left; A + B = 24, so 23.5 ÷ 24 = 47/48 h.",
        "eliminate": "After C stops, A + B still does 24 of 70 per hour, and well under half the work remains, so the extra time is under 1 hour. That strikes 43/25 hours and leaves 47/48, 45/41 or 1/2.",
        "traps": ["Using all three rates for the remaining work.", "Forgetting the first 1.5 hours.", "Adding the three times together."]},
    "q-tw-cycle": {
        "cue": "'X works every day, Y and Z join X every third day.' How long to finish?",
        "formulas": ["tw-f3", "tw-f4"], "tech": ["lcm-units", "ratio-parts"],
        "standard": "LCM 120: X 6, Y 3, Z 2 per day. Three days of the cycle: 6 + 6 + 11 = 23. Five cycles = 15 days = 115 units; the 5 left need 5/6 of the 16th day (X alone does 6). Total 15 5/6 days.",
        "fast": "23 units every 3 days, so 115 by day 15; the last 5 at X's rate of 6 per day is 5/6.",
        "eliminate": "The average rate is under 8 a day, so 120 units take more than 15 days; strike any answer under 15. And the pattern ends mid-day, so a whole-number answer such as 18 days is too long.",
        "traps": ["Counting the extra day as a whole day (16).", "Using all three workers on the last day.", "Taking 20 ÷ (1/20 + 1/40 + 1/60) with everyone working daily."]},
}
PYQS = [
    pyq(S1, 69, "q-tw-together", "X is able to complete a task in 12 days, while Y takes 18 days to finish the same task. If they work together for 3 days, what fraction of the work will still remain?", ["1/3", "5/12", "7/12", "9/12"], "c",
        ["LCM of 12 and 18 = 36 units: X does 3 a day, Y does 2 a day.", "Together 5 a day; in 3 days 15 units of 36 are done.", "Remaining = 21/36 = 7/12."], lambda: 1 - 3 * (F(1, 12) + F(1, 18)), F(7, 12), 0,
        tech=["lcm-units"], optvals=[F(1, 3), F(5, 12), F(7, 12), F(9, 12)], trick="Take total work 36; the pair does 5 a day.",
        wrong={"b": mistake("That is the fraction already done (15/36), not the fraction left.", F(5, 12), 0)}),
    pyq(S1, 70, "q-tw-leave", "Three pumps A, B and C fill a reservoir in 5, 7 and 10 hours. All three work together for 1.5 hours, then C is closed. How much more time is needed to fill the reservoir?", ["1/2 hours", "43/25 hours", "47/48 hours", "45/41 hours"], "c",
        ["LCM 70: A = 14, B = 10, C = 7 per hour; all three = 31 per hour.", "In 1.5 hours: 46.5 units, so 23.5 are left.", "A + B = 24 per hour, so time = 23.5 ÷ 24 = 47/48 hour."],
        lambda: (1 - F(3, 2) * (F(1, 5) + F(1, 7) + F(1, 10))) / (F(1, 5) + F(1, 7)), F(47, 48), 0, tech=["lcm-units"], concepts=1, heavy=True,
        optvals=[F(1, 2), F(43, 25), F(47, 48), F(45, 41)], trick="Total 70: 46.5 done, 23.5 left, A + B do 24.",
        wrong={"b": bound("Under half the work remains and A + B does about a third each hour, so the time is under 1 hour.", lambda v: v >= 1)}),
    pyq(S2, 63, "q-tw-cycle", "X, Y and Z can complete a project in 20, 40 and 60 days. X works every day, while Y and Z join X every third day. How long will it take to finish the project?", ["12 1/2 days", "15 5/6 days", "16 1/6 days", "18 days"], "b",
        ["LCM 120: X = 6, Y = 3, Z = 2 per day.", "A 3-day cycle: 6 + 6 + (6 + 3 + 2) = 23 units. Five cycles (15 days) = 115 units.", "5 units left at X's rate of 6 per day = 5/6 day. Total = 15 5/6 days.", "(The paper prints option (a) oddly, as '12 7/2 days'; either way it is not the answer.)"],
        lambda: F(95, 6), F(95, 6), 0, tech=["lcm-units", "ratio-parts"], concepts=2, heavy=True, optvals=[F(25, 2), F(95, 6), F(101, 6), F(18)],
        trick="23 units every 3 days; 115 units at day 15, then 5/6 of a day.",
        wrong={"d": bound("The pattern ends part-way through a day, so a whole number of days overshoots.", lambda v: v == 18)}),
    pyq(S2, 68, "q-tw-efficiency", "The ratio of efficiencies of workers A and B is 4 : 3. If A can finish a task in 18 days, in how many days will B finish the same task alone?", ["20 days", "22 days", "24 days", "26 days"], "c",
        ["Efficiency and time are inversely proportional, so A : B days = 3 : 4.", "3 parts = 18 days, 1 part = 6, so B = 4 × 6 = 24 days."], lambda: 18 * 4 / 3, 24, 1e-9, tech=["ratio-parts", "scaling"],
        trick="B is slower, so 18 × 4/3 = 24.", wrong={"a": mistake("Not the inverse: B is only 3/4 as fast as A.", 20, 0)}),
]


def practice_items():
    return []
