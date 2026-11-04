"""Partnership practice questions.

Each item has: the question, the correct value, three common-mistake values (they become the other
options), and `check`: the same answer found by a DIFFERENT method (month-by-month simulation, or
allocating the whole profit and adding it back up). The build refuses to run if the two disagree.
"""
from fractions import Fraction as F

from partnership_content import inr, share


def month_sim(schedules, i, total):
    """Partner i's share when profit accrues month by month in proportion to the capital in play.
    schedules[j] is a list with partner j's capital (or animals, in one unit) for each month."""
    n = max(len(s) for s in schedules)
    cap = [list(s) + [0] * (n - len(s)) for s in schedules]
    mine = sum(cap[i])
    everyone = sum(sum(c) for c in cap)
    return F(total) * F(mine) / F(everyone)


def month_sim_total(schedules, i, known_share):
    """Total profit when partner i's share is known."""
    n = max(len(s) for s in schedules)
    cap = [list(s) + [0] * (n - len(s)) for s in schedules]
    return F(known_share) * F(sum(sum(c) for c in cap)) / F(sum(cap[i]))


def P(qtype, level, text, correct, traps, why, check):
    return {"qtype": qtype, "level": level, "text": text, "correct": correct, "traps": traps, "why": why, "check": check}


def practice_items():
    out = []
    # ---------------- two partners ----------------
    cm = [60000 * 10, 80000 * 6]
    out.append(P("q-pt-two", "same", "A puts in ₹60,000 for 10 months and B puts in ₹80,000 for 6 months. Profit is ₹36,000. Find A's share.",
                 share(cm, 0, 36000), [share(cm, 1, 36000), share([60000, 80000], 0, 36000), share([10, 6], 0, 36000)],
                 "600 : 480 = 5 : 4, so A gets 5/9 of 36,000.",
                 month_sim([[60000] * 10, [80000] * 6], 0, 36000)))
    cm = [45000 * 8, 60000 * 9]
    out.append(P("q-pt-two", "same", "X invests ₹45,000 for 8 months and Y invests ₹60,000 for 9 months. Y's share of the profit is ₹31,500. Find the total profit.",
                 F(31500) / F(cm[1], sum(cm)), [F(31500) / F(60000, 105000), F(31500) / F(cm[0], sum(cm)), F(31500) / F(9, 17)],
                 "Capital-months 360 : 540 = 2 : 3. Y has 3 of 5 parts, so total = 31,500 × 5 ÷ 3.",
                 month_sim_total([[45000] * 8, [60000] * 9], 1, 31500)))
    out.append(P("q-pt-two", "same", "A, B and C invest ₹36,000, ₹54,000 and ₹90,000 for the same year. Profit is ₹1,08,000. Find C's share.",
                 share([36, 54, 90], 2, 108000), [share([36, 54, 90], 1, 108000), share([36, 54, 90], 0, 108000), F(108000, 3)],
                 "36 : 54 : 90 = 2 : 3 : 5, so C gets 5/10 of the profit.",
                 month_sim([[36000] * 12, [54000] * 12, [90000] * 12], 2, 108000)))
    cm = [80000 * 4 + 60000 * 8, 70000 * 12]
    out.append(P("q-pt-two", "harder", "A starts with ₹80,000 and withdraws ₹20,000 after 4 months. B keeps ₹70,000 in for the whole year. Profit is ₹82,000. Find A's share.",
                 share(cm, 0, 82000), [share([80000 * 12, 70000 * 12], 0, 82000), share([cm[1], cm[0]], 0, 82000), share([80000 * 8 + 60000 * 4, 70000 * 12], 0, 82000)],
                 "A: 80,000×4 + 60,000×8 = 8,00,000. B: 70,000×12 = 8,40,000. Ratio 20 : 21, so A gets 20/41.",
                 month_sim([[80000] * 4 + [60000] * 8, [70000] * 12], 0, 82000)))
    # ---------------- late entry ----------------
    cm = [50000 * 12, 60000 * 9]
    out.append(P("q-pt-late", "same", "A starts with ₹50,000. After 3 months B joins with ₹60,000. At the end of the year the profit is ₹57,000. Find A's share.",
                 share(cm, 0, 57000), [share([50000 * 12, 60000 * 3], 0, 57000), share(cm, 1, 57000), share([50000, 60000], 0, 57000)],
                 "A: 50×12 = 600. B: 60×9 = 540. Ratio 10 : 9, so A gets 10/19.",
                 month_sim([[50000] * 12, [0] * 3 + [60000] * 9], 0, 57000)))
    cm = [40000 * 12, 50000 * 8, 80000 * 6]
    out.append(P("q-pt-late", "same", "A invests ₹40,000. B joins after 4 months with ₹50,000 and C joins after 6 months with ₹80,000. Yearly profit is ₹1,02,000. Find B's share.",
                 share(cm, 1, 102000), [share(cm, 2, 102000), share([40000 * 12, 50000 * 4, 80000 * 6], 1, 102000), share([40000 * 12, 50000 * 7, 80000 * 5], 1, 102000)],
                 "480 : 400 : 480 = 6 : 5 : 6 (in thousands). B has 5 of 17 parts.",
                 month_sim([[40000] * 12, [0] * 4 + [50000] * 8, [0] * 6 + [80000] * 6], 1, 102000)))
    cm = [30000 * 12, 20000 * 12, 40000 * 6]
    out.append(P("q-pt-late", "same", "A and B start with ₹30,000 and ₹20,000. After 6 months C joins with ₹40,000. Year-end profit is ₹70,000. Find B's share.",
                 share(cm, 1, 70000), [share(cm, 0, 70000), share([30000, 20000, 40000], 1, 70000), share([30000 * 12, 20000 * 12, 40000 * 5], 1, 70000)],
                 "360 : 240 : 240 = 3 : 2 : 2, so B gets 2/7 of 70,000.",
                 month_sim([[30000] * 12, [20000] * 12, [0] * 6 + [40000] * 6], 1, 70000)))
    x = F(120000 * 12, 2 * 9)
    out.append(P("q-pt-late", "harder", "A starts with ₹1,20,000. After 3 months B joins with some capital. At year end the profit is shared 2 : 1 between A and B. Find B's investment.",
                 x, [F(120000, 2), F(120000 * 12, 2 * 3), F(2 * 120000 * 12, 9)],
                 "A : B = 1,20,000×12 : x×9 = 2 : 1, so 9x = 7,20,000 and x = 80,000.",
                 # check: with x invested for 9 months, A's share of 300 is exactly double B's
                 x if month_sim([[120000] * 12, [0] * 3 + [int(x)] * 9], 0, 300) == 2 * month_sim([[120000] * 12, [0] * 3 + [int(x)] * 9], 1, 300) else None))
    # ---------------- working partner ----------------
    def work_total(profit, comm, ratio, who):
        """Allocate the whole profit: commissions first, balance by ratio. Returns (who's total, sum of all)."""
        bal = F(profit) - sum(F(c) * profit for c in comm.values())
        tot = [F(ratio[k]) / sum(map(F, ratio)) * bal + F(comm.get(k, 0)) * profit for k in range(len(ratio))]
        assert sum(tot) == profit, "allocation does not add back to the profit"
        return tot[who]

    out.append(P("q-pt-working", "same", "P and Q invest in the ratio 3 : 5 and earn ₹96,000. P works and gets 10% of the profit extra. Find P's total.",
                 F(10, 100) * 96000 + F(3, 8) * (96000 * F(9, 10)), [F(10, 100) * 96000 + F(3, 8) * 96000, F(3, 8) * 96000, F(3, 8) * 96000 * F(9, 10)],
                 "Commission 9,600. Balance 86,400. P's part of the balance = 3/8 × 86,400 = 32,400. Total 42,000.",
                 work_total(96000, {0: F(1, 10)}, [3, 5], 0)))
    out.append(P("q-pt-working", "same", "A invests ₹40,000 and B invests ₹60,000. A manages the business and gets 20% of the profit. Profit is ₹50,000. Find A's total.",
                 F(2, 10) * 50000 + F(2, 5) * 40000, [F(2, 10) * 50000 + F(2, 5) * 50000, F(2, 5) * 50000, F(2, 5) * 40000],
                 "Commission 10,000. Balance 40,000 split 2 : 3, so A gets 16,000. Total 26,000.",
                 work_total(50000, {0: F(1, 5)}, [2, 3], 0)))
    prof = F(33000) / (F(3, 4) * F(88, 100))
    out.append(P("q-pt-working", "same", "A and B invest in the ratio 1 : 3. A works and gets 12% of the profit extra. B's share is ₹33,000. Find the total profit.",
                 prof, [F(33000) / F(3, 4), F(33000) / F(88, 100), F(33000) / F(3, 4) * F(112, 100)],
                 "B gets 3/4 of the balance, which is 88% of the profit: 0.75 × 0.88 = 0.66. Profit = 33,000 ÷ 0.66 = 50,000.",
                 prof if work_total(prof, {0: F(12, 100)}, [1, 3], 1) == 33000 else None))
    out.append(P("q-pt-working", "harder", "A, B and C invest in the ratio 2 : 3 : 5. A and B work and get 5% and 7% of the profit respectively. Profit is ₹1,00,000. Find B's total.",
                 7000 + F(3, 10) * (100000 - 12000), [7000 + F(3, 10) * 100000, F(3, 10) * 88000, 7000 + F(3, 10) * (100000 - 5000)],
                 "Commissions 5,000 + 7,000 = 12,000. Balance 88,000. B's part = 3/10 × 88,000 = 26,400. Total 33,400.",
                 work_total(100000, {0: F(5, 100), 1: F(7, 100)}, [2, 3, 5], 1)))
    # ---------------- pasture ----------------
    out.append(P("q-pt-pasture", "same", "P keeps 20 sheep for 6 months and Q keeps 18 sheep for 5 months. The rent is ₹8,400. Find Q's share.",
                 share([20 * 6, 18 * 5], 1, 8400), [share([20 * 6, 18 * 5], 0, 8400), share([20, 18], 1, 8400), share([6, 5], 1, 8400)],
                 "120 : 90 = 4 : 3, so Q pays 3/7 of 8,400.",
                 month_sim([[20] * 6, [18] * 5], 1, 8400)))
    # 2 horses = 3 cows  ->  1 horse = 3/2 cow; sim in half-cows (horse = 3, cow = 2)
    out.append(P("q-pt-pasture", "same", "X keeps 8 horses for 3 months and 10 cows for 4 months. Y keeps 12 cows for 5 months. 2 horses eat as much as 3 cows. The rent is ₹6,800. Find X's share.",
                 share([F(3, 2) * 8 * 3 + 40, 60], 0, 6800), [share([8 * 3 + 40, 60], 0, 6800), share([F(2, 3) * 8 * 3 + 40, 60], 0, 6800), share([F(3, 2) * 8 * 3 + 40, 60], 1, 6800)],
                 "1 horse = 3/2 cow. X = 8×3×1.5 + 10×4 = 76 cow-months. Y = 60. X pays 76/136 of 6,800.",
                 month_sim([[8 * 3 + 10 * 2] * 3 + [10 * 2] * 1, [12 * 2] * 5], 0, 6800)))
    # 3 cows = 5 goats -> cow = 5/3 goat; sim in thirds of a goat (cow = 5, goat = 3)
    out.append(P("q-pt-pasture", "same", "A keeps 12 cows for 5 months, B keeps 18 goats for 6 months and C keeps 8 cows for 9 months. 3 cows eat as much as 5 goats. Total rent is ₹16,400. Find B's share.",
                 share([12 * 5 * F(5, 3), 18 * 6, 8 * 9 * F(5, 3)], 1, 16400), [share([12 * 5, 18 * 6, 8 * 9], 1, 16400), share([12 * 5 * F(3, 5), 18 * 6, 8 * 9 * F(3, 5)], 1, 16400), share([12 * 5 * F(5, 3), 18 * 6, 8 * 9 * F(5, 3)], 0, 16400)],
                 "1 cow = 5/3 goat. A = 100, B = 108, C = 120 goat-months. B pays 108/328.",
                 month_sim([[12 * 5] * 5, [18 * 3] * 6, [8 * 5] * 9], 1, 16400)))
    # chain: 2 cows = 5 goats, 3 goats = 4 sheep -> thirds of a sheep: sheep 3, goat 4, cow 10
    out.append(P("q-pt-pasture", "harder", "X keeps 6 cows for 4 months and 12 goats for 3 months. Y keeps 20 sheep for 6 months. 2 cows eat as much as 5 goats, and 3 goats as much as 4 sheep. The rent is ₹18,600. Find X's share.",
                 share([6 * 4 * F(5, 2) + 12 * 3, 20 * 6 * F(3, 4)], 0, 18600),
                 [share([6 * 4 + 12 * 3, 20 * 6], 0, 18600), share([6 * 4 * F(5, 2) + 12 * 3, 20 * 6 * F(4, 3)], 0, 18600), share([6 * 4 * F(5, 2) + 12 * 3, 20 * 6 * F(3, 4)], 1, 18600)],
                 "In goats: X = 24 × 2.5 + 36 = 96; Y = 120 × 0.75 = 90. X pays 96/186 of 18,600.",
                 month_sim([[6 * 10 + 12 * 4] * 3 + [6 * 10] * 1, [20 * 3] * 6], 0, 18600)))
    return out
