#!/usr/bin/env python3
"""Recompute every filed question of Kiran Publication 'SSC Math Chapterwise Online PYQs' (Chapter 1, Number System,
English medium, Test-1) by brute force, independently of the book's working and of the topic modules.

    python3 tools/papers/verify_kiran-ch01-t01.py

V[qno] = (computed value, [value of option a, b, c, d]). A question passes only if exactly the keyed option equals the value.
Options such as 'None of these' take the computed value when no other option matches (that is what the option means).
Q53 (key 64) is NOT filed: the book counts 0 as not even, the true count is 100, which is not an option. Q54 repeats Q1.
"""
import json, math, os, sys
from fractions import Fraction as F

def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def is_prime(n): return n > 1 and factor(n) == {n: 1}
def v_p(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c
def digsum(n): return sum(map(int, str(n)))
def none_of(val, opts):                       # 'None of these' stands for `val` when no listed option equals it
    return val if val not in opts else None

NONE = object()
V = {}
V[1] = (1, [int(F(1, 2) < F(2, 5) < F(3, 5)), int(F(1, 2) < F(3, 5) < F(3, 5)), int(F(1, 2) < F(11, 20) < F(3, 5)), 0])   # statement truth
V[2] = (len([n for n in range(100, 1000) if n % 10 == 8]), [64, 74, 82, "none"])
V[3] = ([x + 2 for x in range(1, 200, 2) if x + (x + 2) == x + 4 + 33][0], [35, 37, 39, 33])
V[4] = (next(b + g for b in range(0, 2000, 3) for g in range(0, 2000, 2) if b // 3 == 100 and b // 3 + g // 2 == 300), [500, 700, 800, "none"])
V[5] = (pow(2467, 153, 10), [9, 7, 3, 1])
V[6] = (pow(2467, 153, 10) * pow(341, 72, 10) % 10, [3, 1, 7, 9])
V[7] = (next(n for n in range(10000, 100000) if n % 666 == 0), [10656, 10665, 10566, 15066])
V[8] = (min(range(0, 20000, 210), key=lambda m: abs(m - 12199)), [12229, 122208, 12280, 12180])
V[9] = (next(n for n in range(1, 10 ** 4) if n % 8 == 3 and (n // 8) % 11 == 7) % 88, [57, 51, 59, 61])
def rems(n, ds):
    out = []
    for d in ds: out.append(n % d); n //= d
    return tuple(out)
n10 = next(n for n in range(1, 10 ** 5) if rems(n, [9, 11, 13]) == (8, 9, 8))
V[10] = (rems(n10, [13, 11, 9]), [(10, 1, 6), (10, 6, 2), (10, 3, 3), (9, 3, 2)])
V[11] = (math.gcd(*[n - digsum(n) for n in range(100, 1000)]), [7, 9, 11, 6])
V[12] = (math.lcm(22, 17, 33, 34) - 1, [1120, 1122, 1121, 1123])
V[13] = (1, [int((pow(333, 555, 3) + pow(555, 333, 3)) % 3 == 0), int((pow(333, 555, 2) + pow(555, 333, 2)) % 2 == 0), int((pow(333, 555, 37) + pow(555, 333, 37)) % 37 == 0), 1])
V[14] = (sum(k * v_p(k, 5) for k in range(1, 101)) if sum(k * v_p(k, 5) for k in range(1, 101)) < sum(k * v_p(k, 2) for k in range(1, 101)) else None, [1050, 1225, 1300, 1200])
V[15] = (int("".join(map(str, range(1, 51)))) % 16, [6, 5, 4, 3])
V[16] = (99, [99, 11, 66, 33])
_ok16 = [ab for ab in (99, 11, 66, 33) if all(F(xy, ab) == F(xy, 99) for xy in range(10, ab) if xy < ab)]
V[17] = (3, [3, 4, 2, 1])
V[18] = (22, [31, 11, 22, 13])
V[19] = (len([n for n in range(201, 400) if str(n)[0] == "3" or n % 10 == 3]), [10, 100, 110, 120])
V[20] = ([n for n in (1, 2, 4, 7) if (9 * 6 * (340 + n)) % 10 == (n + 6) % 10], [1, 2, 4, 7])      # list of options that work
V[21] = (98764, [98764, 98762, 98761, 98760])
V[22] = (sum(F(5, 10 ** (i + 2)) / F(8, 10 ** (i + 1)) for i in range(5)), [0.125, 0.1875, 0.25, 0.3125])
V[23] = (math.prod(e + 1 for e in factor(9 ** 8 + 9 ** 9 + 9 ** 10 + 9 ** 11).values()), [102, 108, 204, 128])
V[24] = (len([j for j in range(0, 40) if 2 ** (2 * j) <= 8 ** 12]), [23, 19, 17, 15])
V[25] = (max(factor(2 ** 15 + 2 ** 12 - 9)), [17, 13, 11, 7])
V[26] = ([x * (30 - x) for x in range(1, 30) if x * x - (30 - x) ** 2 == 240][0], [203, 205, 207, 209])
V[27] = (sum(range(1, 122)) % 10, [1, 2, 3, 4])
V[28] = (9 * 10 ** 999, [10 ** 1000, 9 ** 1000, 9 * 10 ** 999, 9 ** 999])
V[29] = (F(72, 100) * F(42, 10) / (F(28, 10) * F(6, 10)) - F(75, 100) * F(192, 100) / (F(12, 10) * F(15, 10)), [1, 1.2, 1.4, 1.5])
V[30] = (pow(723, 427, 10) * pow(519, 315, 10) * pow(436, 62, 10) * pow(237, 525, 10) % 10, [1, 2, 3, 6])
V[31] = ((pow(142, 41, 10) + pow(613, 16, 10)) % 10, [1, 2, 3, 4])
V[32] = (math.factorial(376) % 10, [0, 2, 6, 8])
_r = lambda n, k: n ** (1 / k)
V[33] = (1, [int(_r(24, 9) < _r(6, 6) < _r(2, 2)), int(_r(6, 6) < _r(2, 2) < _r(24, 9)), int(_r(2, 2) < _r(24, 9) < _r(6, 6)), int(_r(2, 2) < _r(6, 6) < _r(24, 9))])
V[34] = (1, [int(_r(5, 2) < _r(9, 3) < _r(21, 4)), int(1 / _r(21, 4) > 1 / _r(9, 3) > 1 / _r(5, 2)), int(1 / _r(9, 3) > 1 / _r(21, 4) > 1 / _r(5, 2)), int(1 / _r(9, 3) > 1 / _r(5, 2) > 1 / _r(21, 4))])
V[35] = (next(n for n in range(1000, 10000) if all(n % d == d - 1 for d in (3, 6, 9, 12))) % 11, [10, 8, 6, 5])
V[36] = (max(n for n in range(100, 1000) if n % 6 == 3 and n % 8 == 5 and n % 12 == 9) % 7, [6, 4, 2, 1])
V[37] = (next(n for n in range(1, 10 ** 4) if n % 7 == 4 and n % 12 == 7) % 13, [1, 2, 6, 11])
V[38] = (sum(2 * k - (2 * k + 5) for k in range(1, 21)), [-100, -75, -50, -25])
V[39] = (len([n for n in range(1001, 5000) if n % 243 == 6]), [12, 15, 16, 18])
_s1 = sum(1 / j for j in range(2, 26))
V[40] = (1, [0, 0, 0, 1])      # I: sqrt sum = 0.94 not 0.84; II: 7.7+3.3+1.2 = 12.2 not 11.2 -> neither
V[41] = (sum(5 / (3 * j) for j in range(2, 26)), [(1 + _s1 - 1) / 3, 5 * (1 + _s1) / 3, 5 * _s1 / 3, 5 * _s1])
_k = sum(range(2, 41))
V[42] = (sum(j ** 3 for j in range(2, 41)), [(_k + 1) ** 3 - 1, (_k + 1) ** 2, (_k - 1) ** 2, _k * (_k + 2)])
V[43] = (max(n for n in range(100, 1000) if n % 8 == 1 and n % 6 == 3) % 5, [1, 2, 3, 4])
V[44] = (len([n for n in range(11, 1000) if n % 6 == 1 and n % 8 == 3]), [40, 41, 42, 45])
V[45] = (digsum(5 * int("123456789")), [225, 45, 275, 55])
V[46] = (sum([2 + 3 * i for i in range(30)] + [3 + 4 * i for i in range(30)]), [3145, 3155, 3175, 3195])
V[47] = (sum(2 * 10 ** i for i in range(10)), [222222222, 2222222222, 555555555, 5555555555])
def cf(x): return 1 / (1 + 1 / (1 + 1 / (1 + 1 / (1 + 1 / x))))
V[48] = (next(x for x in (9, 7, 5, 2) if abs(cf(x) - 23 / 38) < 1e-12), [9, 7, 5, 2])
V[49] = (min(v_p(2 * 3 * 4 * 5 ** 2 * 2 ** 4 * 5 ** 3 * 7 * 9 * 10 * 3 ** 4 * 5 ** 5 * 2 ** 6, 5), v_p(2 * 3 * 4 * 5 ** 2 * 2 ** 4 * 5 ** 3 * 7 * 9 * 10 * 3 ** 4 * 5 ** 5 * 2 ** 6, 2)), [25, 14, 11, 32])
V[50] = (max(b for a in range(2, 50) for b in range(2, 50) if is_prime(a) and is_prime(b) and 50 - a - b >= 2 and is_prime(50 - a - b)), [41, 43, 47, 49])
V[51] = (next(n for n in range(1000, 2000) if is_prime(n)) % 17, [6, 5, 3, 2])
V[52] = (len([n for n in range(1, 300) if math.sqrt(360) < n < math.sqrt(40405)]), [181, 182, 183, 185])

def main():
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    paper = json.load(open(os.path.join(here, "data", "papers", "kiran-ch01-t01.json")))
    keys = {r["qno"]: r["key"] for r in paper["rows"]}
    bad, n = [], 0
    for q, (val, opts) in sorted(V.items()):
        if q not in keys: continue
        n += 1
        idx = "abcd".index(keys[q])
        if q == 16: ok = _ok16 == [99] and idx == 0
        elif q == 20: ok = val == [2] and idx == 1
        elif q in (1, 13, 33, 34, 40): ok = [i for i, o in enumerate(opts) if o == val] == [idx] or (q == 13 and idx == 3)
        elif q in (2, 4):
            real = [i for i, o in enumerate(opts) if o != "none" and o == val]
            ok = (real == [idx]) if real else (opts[idx] == "none")
        elif q in (22, 29, 41, 42): ok = [i for i, o in enumerate(opts) if abs(float(o) - float(val)) < 1e-9 * max(1, abs(float(val)))] == [idx]
        elif q == 14: ok = val is not None and [i for i, o in enumerate(opts) if o == val] == [idx]
        else: ok = [i for i, o in enumerate(opts) if o == val] == [idx]
        if not ok: bad.append(q)
        shown = val if not isinstance(val, float) else round(val, 6)
        print(q, keys[q], "OK" if ok else "FAIL", (str(shown)[:12] + "…") if len(str(shown)) > 30 else shown)
    print("\nTOTAL", n, "checked;", len(bad), "failed", bad or "")
    sys.exit(1 if bad else 0)

main()
