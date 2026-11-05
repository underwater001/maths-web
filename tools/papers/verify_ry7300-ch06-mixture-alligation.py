#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 6 (Mixture & Alligation).

    python3 tools/papers/verify_ry7300-ch06-mixture-alligation.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch06-mixture-alligation.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; no printed key in this chapter disagreed with the recomputed answer.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._mx_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch06-mixture-alligation.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'b', 2: 'd', 3: 'd', 4: 'a', 5: 'b', 6: 'a', 7: 'b', 8: 'b', 9: 'd', 10: 'd', 11: 'c', 12: 'b', 13: 'c', 14: 'd', 15: 'b', 16: 'b', 17: 'a', 18: 'a', 19: 'a', 20: 'c', 21: 'c', 22: 'c', 23: 'a', 24: 'b', 25: 'a', 26: 'd', 27: 'a', 28: 'c', 29: 'b', 30: 'a', 31: 'd', 32: 'd', 33: 'c', 34: 'b', 35: 'd', 36: 'a', 37: 'd', 38: 'b', 39: 'a', 40: 'a', 41: 'a', 42: 'c', 43: 'a', 44: 'a', 45: 'c', 46: 'a', 47: 'c', 48: 'd', 49: 'c', 50: 'd', 51: 'c', 52: 'b', 53: 'd', 54: 'd', 55: 'b', 56: 'd', 57: 'b', 58: 'd', 59: 'a', 60: 'a', 61: 'a', 62: 'b', 63: 'a', 64: 'c', 65: 'd', 66: 'd', 67: 'a', 68: 'c', 69: 'b', 70: 'd', 71: 'c', 72: 'b', 73: 'a', 74: 'a', 75: 'd', 76: 'c', 77: 'a', 78: 'd', 79: 'b', 80: 'b'}
BOOK_KEY_WRONG = set()
bad, n = [], 0
for q in PYQS_RY:
    n += 1
    r = rows.get(q["qno"])
    if r is None: bad.append(f"Q{q['qno']}: not in the paper file"); continue
    got = q["_calc"]()
    vals = q["_optvals"]
    near = ["abcd"[k] for k, v in enumerate(vals) if abs(v - got) <= max(q["_tol"], 1e-9) + 1e-6 * abs(got)]
    if near != [r["key"]]: bad.append(f"Q{q['qno']}: recomputed {got}, matches {near}, paper key {r['key']}")
    if q["qno"] not in BOOK_KEY_WRONG and BOOK_KEY[q["qno"]] != r["key"]: bad.append(f"Q{q['qno']}: paper key {r['key']} differs from the book's printed key {BOOK_KEY[q['qno']]}")
    if r["answer"] != q["options"]["abcd".index(r["key"])]: bad.append(f"Q{q['qno']}: answer text differs")
    if len(set(q["options"])) != 4: bad.append(f"Q{q['qno']}: repeated option")
if set(rows) != {q["qno"] for q in PYQS_RY}: bad.append("paper rows and topic questions differ")
print(f"TOTAL {n} checked; {len(bad)} failed")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
