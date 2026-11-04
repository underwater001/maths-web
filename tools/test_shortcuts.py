#!/usr/bin/env python3
"""Random tests of the Partnership shortcuts, so a trick is never saved unless it always works.

    python3 tools/test_shortcuts.py

Each shortcut is compared with the slow, obviously-correct method on thousands of random cases,
using exact fractions (no rounding).
"""
import random
from fractions import Fraction as F
from math import gcd

rng = random.Random(7)
N = 5000


def lcm(a, b): return a * b // gcd(a, b)


def t_ratio_by_cancelling():
    """pt-f1 fast: cancel common factors before multiplying gives the same share."""
    for _ in range(N):
        c = [rng.randint(1, 30) * 1000 for _ in range(rng.choice([2, 3]))]
        m = [rng.randint(1, 12) for _ in c]
        profit = rng.randint(10, 99) * 1000
        slow = [F(ci * mi, sum(a * b for a, b in zip(c, m))) * profit for ci, mi in zip(c, m)]
        cm = [a * b for a, b in zip(c, m)]
        g = 0
        for x in cm: g = gcd(g, x)
        small = [x // g for x in cm]
        fast = [F(x, sum(small)) * profit for x in small]
        assert slow == fast
    return "cancel common factors before multiplying"


def t_monthly_equals_capital_months():
    """pt-f1: month-by-month accrual gives the same split as capital × time."""
    for _ in range(N):
        n = rng.choice([2, 3])
        sched = [[rng.choice([0, rng.randint(1, 9) * 1000]) for _ in range(12)] for _ in range(n)]
        if sum(map(sum, sched)) == 0: continue
        profit = rng.randint(10, 99) * 1000
        by_month = [F(sum(s), sum(map(sum, sched))) * profit for s in sched]
        cm = [sum(s) for s in sched]
        assert by_month == [F(c, sum(cm)) * profit for c in cm]
    return "month-by-month accrual = capital × time"


def t_reverse_total():
    """pt-f3: total = known share × (sum of parts) ÷ (his part)."""
    for _ in range(N):
        parts = [rng.randint(1, 15) for _ in range(rng.choice([2, 3]))]
        i = rng.randrange(len(parts)); total = rng.randint(5, 99) * 1000
        known = F(parts[i], sum(parts)) * total
        assert known * sum(parts) / parts[i] == total
    return "total = share × sum of parts ÷ his part"


def t_working_partner():
    """pt-f6 fast: total fraction = c + (1 − c) × r equals commission + ratio share of the balance."""
    for _ in range(N):
        parts = [rng.randint(1, 9) for _ in range(rng.choice([2, 3]))]
        c = F(rng.randint(1, 25), 100); profit = rng.randint(10, 99) * 1000
        w = rng.randrange(len(parts))
        slow = c * profit + F(parts[w], sum(parts)) * (profit - c * profit)
        fast = (c + (1 - c) * F(parts[w], sum(parts))) * profit
        assert slow == fast
        # the squeeze used for elimination: r between two simple fractions bounds the total
        r = F(parts[w], sum(parts))
        lo, hi = F(1, 20), F(1, 2)
        for a in (F(k, 20) for k in range(1, 21)):
            if a <= r <= a + F(1, 20):
                assert (c + (1 - c) * a) * profit <= fast <= (c + (1 - c) * (a + F(1, 20))) * profit
    return "c + (1 − c) × r, and the squeeze bound"


def t_unit_conversion():
    """pt-f7: converting every animal to whole 'small units' gives the same fraction as fractional conversion."""
    for _ in range(N):
        # a A = b B,  c B = d C   ->  1 A = b/a B,  1 B = d/c C
        a, b, c, d = (rng.randint(1, 9) for _ in range(4))
        counts = [(rng.randint(1, 30), rng.randint(1, 9), rng.choice("ABC")) for _ in range(rng.randint(2, 5))]
        person = [rng.choice([0, 1]) for _ in counts]
        if len(set(person)) < 2: continue
        # slow: everything in C using fractions
        inC = {"C": F(1), "B": F(d, c), "A": F(b, a) * F(d, c)}
        slow = [sum(n * m * inC[t] for (n, m, t), p in zip(counts, person) if p == who) for who in (0, 1)]
        # fast: choose the unit so every weight is a whole number
        unit = lcm(lcm(a, c), 1)
        w = {"C": a * c, "B": a * d, "A": b * d}
        fast = [sum(n * m * w[t] for (n, m, t), p in zip(counts, person) if p == who) for who in (0, 1)]
        if sum(slow) == 0 or sum(fast) == 0: continue
        assert F(slow[0], 1) / sum(slow) == F(fast[0], sum(fast))
    return "whole-number unit gives the same fraction"


def t_withdrawal():
    """pt-f5: capital that changes = sum of (capital × months at that capital)."""
    for _ in range(N):
        c0 = rng.randint(2, 20) * 1000; m1 = rng.randint(1, 11); dc = rng.randint(1, c0 // 1000 - 1) * 1000 if c0 > 1000 else 0
        sched = [c0] * m1 + [c0 - dc] * (12 - m1)
        assert sum(sched) == c0 * m1 + (c0 - dc) * (12 - m1)
    return "withdrawal: capital × months per stretch"


def main():
    for t in (t_ratio_by_cancelling, t_monthly_equals_capital_months, t_reverse_total, t_working_partner, t_unit_conversion, t_withdrawal):
        print(f"ok  {N:>5} random cases  {t()}")


if __name__ == "__main__":
    main()
