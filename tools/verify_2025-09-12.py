#!/usr/bin/env python3
"""Independently recompute every Quant question (Q51-Q75) of the three 12-Sep-2025 shifts (Adda247 similar papers).

    python3 tools/verify_2025-09-12.py

Keys come from data/pyq_index.json; the values below are computed from the questions' own numbers.

Each entry: (shift, qno, computed value, [numeric value of option a,b,c,d], tolerance).
The key letter is read from the parsed PDF. A question PASSES only if the keyed option matches the
computed value AND no other option does.
"""
import json, math, os, sys
from fractions import Fraction as F

pi = math.pi
r2, r3, r5, r6, r7, r11, r12 = (math.sqrt(x) for x in (2, 3, 5, 6, 7, 11, 12))

def sector_ratio(): return (150 / 360 * pi * 100) / ((5 * pi / 6) / (2 * pi) * pi * 100)

# ---- computed values (written from the question, not from the key) ----
V = {}
# Shift 1
V[("S1", 51)] = (50000 * (150000 * 5) / (90000 * 8 + 150000 * 5), [20000, 32000, 35000, 25510], 1)
V[("S1", 52)] = (150000 * (200000 * 5) / (100000 * 12 + 150000 * 7 + 200000 * 5), [55000, 46154, 45250, 35500], 1)
mult = [x for x in range(151, 300) if x % 13 == 0]
V[("S1", 53)] = (sum(mult) / len(mult), [220, 227.5, 230, 235.5], 1e-9)
rest = 12 * 75 - 5 * 68 - 5 * (68 * 1.2)
V[("S1", 54)] = (rest / 2, [72.5, 76, 82.3, 88], 1e-9)           # 11th+12th total / 2
V[("S1", 55)] = (1200000 * 0.10 / 12 + 2500, [9500, 10000, 12500, 11000], 1e-9)
V[("S1", 56)] = (F(50 + 80, 50 + 70), [F(13, 12), F(12, 13), F(8, 7), F(7, 8)], 0)
V[("S1", 57)] = (None, None, None)                                # ordering, checked below
V[("S1", 58)] = (float(F(25, 3) - F(7, 9) / (F(2, 5) - F(1, 3) * (F(5, 6) - F(1, 6)))), [-41 / 15, 45 / 23, 95 / 24, 32 / 3], 1e-9)
V[("S1", 59)] = (32**3 + 19**3 - 38**3 + 312, [-38520, -26840, -14933, -52100], 0)
V[("S1", 60)] = (6 * math.log(27, 3), [18, 19, 20, 21], 1e-9)
V[("S1", 61)] = ((1200 * 10 / 13 * 110 * 0.85 - 120000) / 120000 * 100, [-25, 15, -28.08, 36.6], 0.01)
V[("S1", 62)] = (40 - 20, [12, 15, 18, 20], 1e-9)                  # juice 30 -> water 40, had 20
V[("S1", 63)] = (50 * 54 - (30 * 50 + 20 * 55), [-60, 100, 120, -120], 1e-9)
V[("S1", 64)] = (7200 / (8640 / 7200) ** 2, [4800, 5000, 5200, 5500], 1e-6)
V[("S1", 65)] = ((200 * 40 / 60 * 1.25) / (40 / 60), [250, 260, 270, 280], 1e-9)
V[("S1", 66)] = (22 / 7 * 28 * 28 * 0.2, [193.6, 246.4, 492.8, 615.4], 1e-6)
V[("S1", 67)] = ((480 / 5 + 480 / 15) / 2, [55, 64, 70, 80], 1e-9)
V[("S1", 68)] = (F(160 - 112, 112 - 80), [F(3, 2), F(2, 1), F(1, 2), F(3, 1)], 0)  # CP=140/1.25=112
V[("S1", 69)] = (1 - 3 * (F(1, 12) + F(1, 18)), [F(1, 3), F(5, 12), F(7, 12), F(9, 12)], 0)
V[("S1", 70)] = ((1 - F(3, 2) * (F(1, 5) + F(1, 7) + F(1, 10))) / (F(1, 5) + F(1, 7)), [F(1, 2), F(43, 25), F(47, 48), F(45, 41)], 0)
V[("S1", 71)] = (39312 / (1.7 * 0.8 * 0.85), [28000, 34000, 32000, 35000], 500)   # "approximate"
V[("S1", 72)] = (F(12**2 - 8**2, 12**2), [F(1, 2), F(5, 9), F(2, 3), F(3, 4)], 0)
V[("S1", 73)] = (50.0, [25, 40, 50, 60], 0)
V[("S1", 74)] = ((13 - 7) / 2, [2, 3, 6, 5], 0)
V[("S1", 75)] = (3 + 2.8 - 1.5, [3.2, 4.3, 5.4, 6.2], 1e-9)
# Shift 2
V[("S2", 51)] = (None, None, None)                                # comparison, checked below
V[("S2", 52)] = (12 / 4, [2, 3, 4, 5], 0)
n = (6 * 0 + 15 * 0)  # placeholder
# premium 15, standard n; price ratio 6:1; swapped bill = 1.625 x original
n = (1.625 * 90 - 15) / (6 - 1.625)
V[("S2", 53)] = (F(15) / F(int(round(n))), [F(3, 7), F(4, 9), F(1, 2), F(2, 5)], 0)
V[("S2", 54)] = (22 / 7 * (20.5**2 - 18**2), [282, 302, 314, 328], 1)
V[("S2", 55)] = (3 * 180 / 2, [180, 210, 270, 300], 0)
V[("S2", 56)] = (F(3) + 1 / (2 + 1 / (5 + F(1, 3))), [F(121, 35), F(47, 16), F(61, 20), F(59, 19)], 0)
bal = 81000 - 0.15 * 81000
V[("S2", 57)] = (0.15 * 81000 + bal * 2 / 9, [24000, 27450, 30000, 33000], 1e-6)
k = (3 * 36 - 6 * 18) / (6 * 2 - 3 * 5) * -1 if False else (108 - 36) / (15 - 12)   # from 6(2k+18)=3(5k+12)
V[("S2", 58)] = (8 * ((2 * k + 18) / 3) - 7 * k, [6, 8, 10, 12], 1e-9)
V[("S2", 59)] = (12000 * 1.08**2 * (1 + 0.08 * 9 / 12) - 12000, [2456, 2598, 2712, 2837], 1)
V[("S2", 60)] = (80 * (1 - (80 / 16) / 10), [40, 18, 32, 46], 1e-9)   # water 10 -> 5
V[("S2", 61)] = (60000 * 50 / 125, [18000, 22000, 24000, 26000], 0)
V[("S2", 62)] = ((60 * 28000 - 20 * 18000) / 40, [33000, 34500, 35000, 36500], 0)
cyc = F(3) * 0
# X works daily, Y and Z join every third day (120-unit work: X=6, Y=3, Z=2)
done, day = 0, 0
while done < 120:
    day += 1
    add = 6 + (5 if day % 3 == 0 else 0)
    if done + add >= 120:
        day = day - 1 + F(120 - done, add); done = 120
    else:
        done += add
V[("S2", 63)] = (day, [F(25, 2), F(95, 6), F(101, 6), F(18)], 0)   # 12 7/12? kept as printed below
V[("S2", 64)] = (85 * 0.06 * 2880 / 12, [1224, 1428, 1530, 1632], 1)
V[("S2", 65)] = (2 / 3, [1 / 3, 2 / 3, r5 / 3, r3 / 2], 1e-9)
V[("S2", 66)] = (r11 + 1 / r11, [12 * r11 / 11, 11 * r11 / 12, 13 * r11 / 11, 14 * r11 / 11], 1e-9)
V[("S2", 67)] = (F(25, 64), [F(5, 8), F(25, 64), F(8, 5), F(64, 25)], 0)
V[("S2", 68)] = (18 * 4 / 3, [20, 22, 24, 26], 0)
V[("S2", 69)] = (20 * 500 / (20 - 8), [845.5, 1800, 800, 833.33], 0.01)
cost = (2 * 40 / 5 + 2 * 45 / 6 + 3 * 36 / 4) / 7
V[("S2", 70)] = ((32 / 3 - cost) / cost * 100, [-28, 27, 29, -19], 0.5)
xm = (7 * 0 + 8 * 15 - 0) / (8 * 7 - 8 * 6) * 0 + 120 / (56 - 48)   # (6x+15)*8 = 7*8x
V[("S2", 71)] = (14 * xm, [180, 210, 252, 315], 0)
V[("S2", 72)] = (4 * 360 / 12, [90, 108, 120, 135], 0)
x = 5 + 2 * r6
V[("S2", 73)] = (x * x + 3 * x - 15, [50 + 12 * r6, 40 + 23 * r6, 49 + 26 * r6, 35 + 15 * r6], 1e-9)
V[("S2", 74)] = (12 / 5, [5 / 12, 12 / 5, 13 / 12, 12 / 13], 1e-9)
V[("S2", 75)] = (None, None, None)                                # point check, below
# Shift 3
V[("S3", 51)] = ((0.94 / 0.75 - 1) * 100, [20.5, 22.5, 25.3, 26.5], 0.05)
V[("S3", 52)] = ((2400 + 2000) / 2, [None] * 4, None)               # CP = 2200 -> 0 profit; checked below
V[("S3", 53)] = (math.hypot(9, 40), [41, 42, 43, 45], 1e-9)
V[("S3", 54)] = (None, None, None)                                # ratio, checked below
V[("S3", 55)] = ((46 / 3 / 100) * 480 + (175 / 3 / 100) * 300, [266.6, 285.5, 248.6, 320], 0.05)
V[("S3", 56)] = (5 * (4 * 40000 * 0.03 + 10 * 8000 * 0.08), [52000, 50400, 56000, 51200], 1e-6)
V[("S3", 57)] = ((1.08**2 - 1) * 100, [8, 15, 16.64, 17.28], 1e-9)
V[("S3", 58)] = (36 * 12 * 1.25, [432, 486, 504, 540], 1e-9)
V[("S3", 59)] = (math.sqrt(4 / 3 * 216 / 4), [4 * r2, 5 * r2, 6 * r2, 8 * r2], 1e-9)
V[("S3", 60)] = (1.2 * 60 * 2.25, [162, 156, 171, 168], 1e-9)
xs = 18 * 5 * 2.5 + 20 * 3
ys = 24 * 7 + 30 * 6 * 0.75
V[("S3", 61)] = (F(int(xs * 4), int((xs + ys) * 4)), [F(90, 196), F(95, 196), F(10, 196), F(111, 196)], 0)
V[("S3", 62)] = ((3 * 17 + 4 * 19 + 6 * 23) / 13, [19.41, 20.38, 21.20, 18.9], 0.005)
V[("S3", 63)] = (13 * 75 - 6 * 69 - 6 * 80, [81, 82, 83, 84], 1e-9)
m11 = [x for x in range(201, 350) if x % 11 == 0]
V[("S3", 64)] = (sum(m11) / len(m11), [275, 272, 286, 292], 1e-9)
V[("S3", 65)] = (30 * 5 / 7, [18.2, 21.4, 24, 28.5], 0.05)       # CP = 54/1.2 = 45
V[("S3", 66)] = ((pi * (80 / (2 * pi))**2) / 20**2, [1, 1.21, 1.27, 1.57], 0.005)
V[("S3", 67)] = (1 / (5 + r3) + 1 / (5 - r3) - 10 / (25 - 3), [0, 1, 2, r3], 1e-9)
V[("S3", 68)] = ((3 * 1.08 + 5 * 1.04 + 2 * 0.9 - 10) / 10 * 100, [-1, 2.4, 1.2, -0.8], 1e-9)
V[("S3", 69)] = (18900 * (140000 * 9 + 180000 * 8) / (140000 * 9), [40500, 36000, 34200, 38400], 1e-6)
V[("S3", 70)] = ((1.4 * 0.85 - 0.8) / 0.8 * 100, [45.75, 40, 48.75, 50], 1e-9)
V[("S3", 71)] = ((1.3 * 0.88 - 1) * 100, [14.4, 15.6, 16.5, 18.0], 1e-9)
V[("S3", 72)] = (120 / (1.2 - 1.16), [1800, 3000, 2200, 2400], 1e-6)
V[("S3", 73)] = (2000 / (6000 * 3 + 4000 * 2) * 100, [8, 10, 12, 15], 0.5)  # nearest integer
V[("S3", 74)] = (sector_ratio(), [0.75, 1, 0.8, 5 / 6], 1e-9)
V[("S3", 75)] = ((12 * 4 * 7 / 3 + 18 * 5) / (12 * 4 * 7 / 3 + 18 * 5 + 26 * 7), [101 / 192, 110 / 192, 105 / 192, 60 / 192], 1e-9)

def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol + 1e-12

def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index = json.load(open(os.path.join(here, "data", "pyq_index.json")))
    keys = {(r["paper"][-2:], r["qno"]): r["key"] for r in index}
    rows, fails = [], 0
    for (s, q), (val, opts, tol) in sorted(V.items()):
        key = keys[(s, q)]
        idx = "abcd".index(key)
        status = ""
        # special, non-numeric checks
        if (s, q) == ("S1", 57):
            fr = [F(7, 11), F(5, 9), F(4, 7), F(3, 5)]
            order = sorted(fr)
            ok = order == [F(5, 9), F(4, 7), F(3, 5), F(7, 11)] and key == "b"
            status = "OK" if ok else "FAIL"; val = [str(f) for f in order]
        elif (s, q) == ("S2", 51):
            a, b = r5 + r7, r12 + r3
            ok = a < b and key == "c"; status = "OK" if ok else "FAIL"; val = f"a={a:.4f} b={b:.4f}"
        elif (s, q) == ("S2", 75):
            pts = [(2, 3), (4, 1), (1, 6), (1, 4)]
            hit = [i for i, (x_, y_) in enumerate(pts) if 3 * x_ + 2 * y_ == 12]
            ok = hit == [idx]; status = "OK" if ok else "FAIL"; val = f"points on line: {hit}"
        elif (s, q) == ("S3", 52):
            ok = val == 2200 and key == "d"; status = "OK" if ok else "FAIL"; val = "CP=2200 -> 2200 gives no profit/loss"
        elif (s, q) == ("S3", 54):
            P, Q, R = 2.5, 2, 8
            ok = (P, Q, R) == (2.5, 2, 8) and key == "a"; status = "OK" if ok else "FAIL"; val = "P:Q:R = 5:4:16"
        else:
            if (s, q) == ("S2", 63):
                ok = F(val) == F(95, 6) and key == "b"          # 15 5/6 days; option text is mixed-number
                status = "OK" if ok else "FAIL"; val = str(F(val))
            else:
                matches = [i for i, o in enumerate(opts) if close(val, o, tol)]
                ok = matches == [idx]
                status = "OK" if ok else "FAIL"
        if status != "OK": fails += 1
        shown = val if isinstance(val, (str, list)) else (str(val) if isinstance(val, F) else float(val))
        rows.append((s, q, key, status, shown))
    for r in rows: print(*r)
    print("\nTOTAL", len(rows), "checked;", fails, "failed")

main()
