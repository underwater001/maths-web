"""Time and Work: quiz tier."""
from fractions import Fraction as F
from bank import bound, mistake, pyq, mixed_val
from topics._tw_ry import PYQS_RY

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
    "c-tw-manday": {"short": "Men, women, days", "label": "Man-days: men × days (× hours) stays constant", "kind": "concept", "parent": TOPIC, "order": 4,
                    "summary": "Work = people × days × hours. Convert women and children into men, then scale or split the work into stretches.", "links": ["ratio-proportion"]},
    "c-tw-wage": {"short": "Sharing wages", "label": "Wages shared in proportion to work done", "kind": "concept", "parent": TOPIC, "order": 5,
                  "summary": "Money is shared by work done (rate × days), not by days alone.", "links": ["ratio-proportion"]},
    "q-tw-pairs": {"short": "Pair rates", "label": "A + B, B + C and C + A given", "kind": "qtype", "parent": "c-tw-rate", "order": 3,
                   "summary": "Add the three pair rates and halve to get A + B + C; subtract a pair to isolate one worker.", "links": []},
    "q-tw-others": {"short": "One versus the rest", "label": "A takes k times as long as B and C together", "kind": "qtype", "parent": "c-tw-rate", "order": 4,
                    "summary": "'k times as long as the others together' means that person does 1/(k + 1) of the combined rate.", "links": []},
    "q-tw-less": {"short": "Takes d days less", "label": "One worker takes d days less than another", "kind": "qtype", "parent": "c-tw-rate", "order": 5,
                  "summary": "1/x + 1/(x + d) = 1/t. Try the options, or use t squared = product of the two gaps.", "links": []},
    "q-tw-hours": {"short": "Hours a day", "label": "Different hours a day: work in man-hours", "kind": "qtype", "parent": "c-tw-rate", "order": 6,
                   "summary": "Convert each time to total hours (days × hours a day), then use rates per hour.", "links": []},
    "q-tw-helpers": {"short": "Extra helpers needed", "label": "How many helpers to finish in a given time", "kind": "qtype", "parent": "c-tw-rate", "order": 7,
                     "summary": "Required rate minus the rate already there, divided by one helper's rate.", "links": []},
    "q-tw-undo": {"short": "Undoing work", "label": "One person builds while another destroys", "kind": "qtype", "parent": "c-tw-pattern", "order": 2,
                  "summary": "Destroying is a negative rate: net work = builder's rate minus destroyer's rate for those days.", "links": []},
    "q-tw-alt": {"short": "Alternate days", "label": "Workers take turns, one day each", "kind": "qtype", "parent": "c-tw-pattern", "order": 3,
                 "summary": "Work of one pair of days, count the whole pairs, then see who works next.", "links": []},
    "q-tw-manday": {"short": "Men, women, boys", "label": "Men, women and boys on the same work", "kind": "qtype", "parent": "c-tw-manday", "order": 1,
                    "summary": "Fix 1 man = × women = y boys, express everyone as men, then use man-days.", "links": []},
    "q-tw-mdh": {"short": "Men × days × hours", "label": "Scaling men, days and hours", "kind": "qtype", "parent": "c-tw-manday", "order": 2,
                 "summary": "men × days × hours ÷ work is the same for both cases; use it to find the unknown.", "links": []},
    "q-tw-teams": {"short": "Strength changes", "label": "Men join or leave, or work is split in stretches", "kind": "qtype", "parent": "c-tw-manday", "order": 3,
                   "summary": "Work out how many man-days are done, subtract from the total, and divide by the new strength.", "links": []},
    "q-tw-more": {"short": "More men, fewer days", "label": "Extra men finish the job earlier", "kind": "qtype", "parent": "c-tw-manday", "order": 4,
                  "summary": "Total man-days stay fixed: n × d = (n + k)(d − e).", "links": []},
    "q-tw-wage": {"short": "Wages by work", "label": "Share a payment between workers", "kind": "qtype", "parent": "c-tw-wage", "order": 1,
                  "summary": "Shares are in the ratio of work done: rate × days worked for each.", "links": []},
}
FORMULAS = [
    {"id": "tw-f1", "node": "c-tw-rate", "text": "Rate = 1 ÷ days. Together: 1/a + 1/b + 1/c per day", "note": "Time together = 1 ÷ (sum of rates)."},
    {"id": "tw-f2", "node": "c-tw-rate", "text": "Efficiency ∝ 1 ÷ days: efficiency A : B = days B : days A", "note": "4 : 3 efficiency means 3 : 4 time."},
    {"id": "tw-f3", "node": "c-tw-lcm", "text": "Total work = LCM of the times; rate = LCM ÷ days", "note": "For 12 and 18: total 36, rates 3 and 2."},
    {"id": "tw-f4", "node": "c-tw-pattern", "text": "Cycle work = sum of the work done over one repeat; days = whole cycles × length + part of the next", "note": "Finish inside a day by dividing the remaining work by that day's rate."},
    {"id": "tw-f5", "node": "c-tw-rate", "text": "A + B + C = (sum of the three pair rates) ÷ 2", "note": "Then C = (A + B + C) − (A + B)."},
    {"id": "tw-f6", "node": "c-tw-manday", "text": "Work = men × days × hours, so M1 D1 H1 ÷ W1 = M2 D2 H2 ÷ W2", "note": "Men and days are inverse; work is direct."},
    {"id": "tw-f7", "node": "c-tw-wage", "text": "Share of money = share of work = rate × days worked", "note": "Wages per day are equal only if the workers are equally efficient."},
    {"id": "tw-f8", "node": "c-tw-rate", "text": "A takes k times as long as the others together: A's rate = total rate ÷ (k + 1)", "note": "Two or three such statements fix every rate."},
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
    "q-tw-pairs": {
        "cue": "'A and B in 12 days, B and C in 15 days, C and A in 20 days. All three together?'",
        "formulas": ["tw-f1", "tw-f5"], "tech": ["lcm-units", "identity"],
        "standard": "2(A + B + C) = 1/12 + 1/15 + 1/20 = 12/60, so A + B + C = 1/10 a day: 10 days.",
        "fast": "LCM 60: the pairs do 5, 4 and 3 units, which add to 12, so one of each does 6 a day: 60 ÷ 6 = 10 days.",
        "eliminate": "All three together must beat every pair, so the answer is below 12 days; strike any option at or above the smallest pair time.",
        "traps": ["Forgetting to halve the sum of the pair rates.", "Adding the three pair times.", "Finding A + B + C but answering for one worker."]},
    "q-tw-others": {
        "cue": "'B takes three times as long as A and C together, and C twice as long as A and B together. All three together take 10 days.'",
        "formulas": ["tw-f8"], "tech": ["lcm-units", "ratio-parts"],
        "standard": "B is 1/4 and C is 1/3 of the total rate 1/10, so A = 1/10 × (1 − 1/4 − 1/3) = 1/24: 24 days.",
        "fast": "Take 120 units: all three do 12 a day. B does 1/4 of that (3), C does 1/3 (4), so A does 5 a day and takes 120 ÷ 5 = 24 days.",
        "eliminate": "A alone must take longer than the 10 days the three need together, and A is the fastest of the three here, so the answer lies between 10 and 30: strike 5, 8 and any option above B or C's time.",
        "traps": ["Using 1/3 instead of 1/(3 + 1) for 'three times as long'.", "Subtracting the fractions from 1 without scaling by the combined rate."]},
    "q-tw-less": {
        "cue": "'A takes 10 days less than B. Together they take 12 days. How long does B take?'",
        "formulas": ["tw-f1"], "tech": ["back-substitute", "standard-values"],
        "standard": "1/x + 1/(x + 10) = 1/12 gives x² − 14x − 120 = 0, so x = 20 and B takes 30 days.",
        "fast": "Test option pairs: B = 30 means A = 20 and 1/20 + 1/30 = 1/12 ✓. If only 'together' time t is asked after extra hours a and b: t² = a × b.",
        "eliminate": "Each worker takes more than the combined time, so A is above 12 days and B above 22; strike options that break this.",
        "traps": ["Taking A = B − 10 but adding the days instead of the rates.", "Answering for A when B is asked."]},
    "q-tw-hours": {
        "cue": "'Working 7 hours a day, A takes 6 days, B takes 8 days. Together, working 8 hours a day?'",
        "formulas": ["tw-f1", "tw-f6"], "tech": ["units-first", "scaling"],
        "standard": "A needs 42 hours, B needs 56 hours: together 1/42 + 1/56 = 1/24 per hour, so 24 hours = 3 days at 8 hours a day.",
        "fast": "Total hours first (days × hours), then LCM 168: A = 4, B = 3, together 7 an hour: 24 hours.",
        "eliminate": "Together they need fewer days than the faster worker alone at 8 hours a day (under 5.25 days).",
        "traps": ["Combining the days (6 and 8) without allowing for the changed hours.", "Dividing 24 hours by 7 instead of 8."]},
    "q-tw-helpers": {
        "cue": "'A man, a woman and a boy do a job in 3, 4 and 12 days. How many boys must assist 1 man and 1 woman to finish in 1/4 of a day?'",
        "formulas": ["tw-f1", "tw-f3"], "tech": ["lcm-units", "scaling"],
        "standard": "Needed rate = 4 a day (one job in 1/4 day). Man + woman = 1/3 + 1/4 = 7/12. Boys give 4 − 7/12 = 41/12, and each does 1/12, so 41 boys.",
        "fast": "LCM 12: man 4, woman 3, boy 1 a day. The job (12 units) in 1/4 day needs 48 a day; man + woman give 7, so 41 boys.",
        "eliminate": "The man and woman supply only 7 of the 48 units a day needed, so most of the work falls on boys: the answer is large, strike small options.",
        "traps": ["Taking the needed rate as 1/4 instead of 1 ÷ (1/4) = 4.", "Forgetting to subtract what the man and woman already do."]},
    "q-tw-undo": {
        "cue": "'A builds in 8 days which B destroys in 3 days. A worked 6 days, the last 2 with B destroying. How many more days must A work?'",
        "formulas": ["tw-f1", "tw-f3"], "tech": ["lcm-units", "sign-check"],
        "standard": "LCM 24: A builds 3 a day, B destroys 8 a day. Four plain days = 12; two days with B = 2 × (3 − 8) = −10. Net 2, so 22 remain: 22 ÷ 3 = 7 1/3 days.",
        "fast": "Treat the destroyer as a negative rate, then continue with A alone.",
        "eliminate": "Net progress is tiny after the destruction, so the extra time is nearly the whole job (about 8 days): strike options under 7.",
        "traps": ["Adding B's rate instead of subtracting it.", "Forgetting the days A worked before the destruction began."]},
    "q-tw-alt": {
        "cue": "'A and B take 9 and 12 days. They work alternately a day each, A first. How long to finish?'",
        "formulas": ["tw-f3", "tw-f4"], "tech": ["lcm-units"],
        "standard": "LCM 36: A = 4, B = 3. A pair of days = 7. Five pairs (10 days) = 35, then A needs 1 more unit: 1/4 day. Total 10 1/4 days.",
        "fast": "Find the whole pairs, then check who works next and finish the remainder at his rate.",
        "eliminate": "A pair of days does 7 of the 36 units, so the job needs just over 10 days (35 units in 10 days, with a part-day left): strike every option below 10.",
        "traps": ["Taking the remaining work at the wrong person's rate.", "Counting a part-day as a full day."]},
    "q-tw-manday": {
        "cue": "'12 men or 20 women do a job in 15 and 12 days. 5 men and 5 women together?'",
        "formulas": ["tw-f6"], "tech": ["scaling", "lcm-units"],
        "standard": "12 men × 15 = 180 man-days = 20 women × 12 = 240 woman-days, so 1 man = 4/3 women. Convert everyone to one kind, then divide the total work by their combined rate.",
        "fast": "Fix 1 man = x women, express all in the smaller unit, then use total units ÷ combined units per day.",
        "eliminate": "A mixed group of equal numbers of two kinds works at a speed between the two kinds, so the time lies between the two single-type times.",
        "traps": ["Treating men and women as equal.", "Taking the 'or' as 'and' (adding the times)."]},
    "q-tw-mdh": {
        "cue": "'(x + 4) men in (x + 5) days = (x − 5) men in (x + 20) days. Find x.' or 'm men, d days, h hours a day'.",
        "formulas": ["tw-f6"], "tech": ["scaling", "back-substitute"],
        "standard": "Men × days (× hours) is the same for equal work: (x + 4)(x + 5) = (x − 5)(x + 20) gives x = 20.",
        "fast": "Test the options: x = 20 gives 24 × 25 = 600 = 15 × 40.",
        "eliminate": "x must exceed 5, since (x − 5) men must be positive; strike small options first.",
        "traps": ["Setting up men ÷ days instead of men × days.", "Forgetting the hours a day."]},
    "q-tw-teams": {
        "cue": "'40 men can do a job in 40 days, but at the end of every 10th day 5 men leave. How long?'",
        "formulas": ["tw-f6"], "tech": ["scaling", "lcm-units"],
        "standard": "Total 40 × 40 = 1,600 man-days. Day-blocks of 10 days do 400, 350, 300, 250, 200 (total 1,500 in 50 days); the last 100 with 15 men takes 6 2/3 days: 56 2/3.",
        "fast": "Write man-days per stretch and subtract from the total until what is left fits inside one stretch.",
        "eliminate": "Strength only falls, so the job takes more than 40 days: strike 40 and below.",
        "traps": ["Forgetting that the strength keeps falling every stretch.", "Counting the last part-stretch as a full stretch."]},
    "q-tw-more": {
        "cue": "'Some men finish in 30 days; with 5 more men, 10 days less. How many men at the start?'",
        "formulas": ["tw-f6"], "tech": ["back-substitute", "scaling"],
        "standard": "n × 30 = (n + 5) × 20, so 30n = 20n + 100 and n = 10.",
        "fast": "The days drop in ratio 3 : 2, so the men rise in ratio 2 : 3: the 5 extra men are the 1 part, so the start was 2 parts = 10.",
        "eliminate": "Extra men cut the time by a third, so the extra men are half of the original: the original is 2 × 5 = 10.",
        "traps": ["Writing n/30 = (n + 5)/20 (direct instead of inverse).", "Answering with n + 5."]},
    "q-tw-wage": {
        "cue": "'A and B finish a job in 15 and 10 days for ₹ 30,000. What is A's share?'",
        "formulas": ["tw-f1", "tw-f7"], "tech": ["ratio-parts", "lcm-units"],
        "standard": "Rates 1/15 : 1/10 = 2 : 3, so A gets 2/5 of 30,000 = ₹ 12,000.",
        "fast": "Share ∝ rate, and rate ∝ 1/days: the ratio of shares is the reverse of the days ratio, 10 : 15 = 2 : 3.",
        "eliminate": "A is the slower worker, so A gets less than half: strike any option above half the total.",
        "traps": ["Sharing in the ratio of the days (15 : 10) instead of the reverse.", "Ignoring a helper's work when three workers are involved."]},
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

PYQS = PYQS + PYQS_RY


def practice_items():
    return []
