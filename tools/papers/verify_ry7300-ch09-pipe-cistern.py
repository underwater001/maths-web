#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 9 (Pipe & Cistern).

    python3 tools/papers/verify_ry7300-ch09-pipe-cistern.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch09-pipe-cistern.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; none disagrees with the recomputed answer (BOOK_KEY_WRONG is empty).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._pcs_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch09-pipe-cistern.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'b', 2: 'b', 3: 'c', 4: 'a', 5: 'b', 6: 'c', 7: 'b', 8: 'b', 9: 'd', 10: 'c', 11: 'd', 12: 'b', 13: 'd', 14: 'c', 15: 'b', 16: 'c', 17: 'd', 18: 'a', 19: 'd', 20: 'd', 21: 'b', 22: 'd', 23: 'c', 24: 'a', 25: 'd', 26: 'c', 27: 'd', 28: 'd', 29: 'c', 30: 'c', 31: 'a', 32: 'a', 33: 'b', 34: 'a', 35: 'c', 36: 'd', 37: 'd', 38: 'b', 39: 'd', 40: 'b', 41: 'c', 42: 'a', 43: 'c', 44: 'a', 45: 'b', 46: 'd', 47: 'a', 48: 'a', 49: 'b', 50: 'c', 51: 'c', 52: 'a', 53: 'd', 54: 'b', 55: 'a', 56: 'd', 57: 'b', 58: 'c', 59: 'b', 60: 'd', 61: 'b', 62: 'd', 63: 'd', 64: 'c', 65: 'c', 66: 'a', 67: 'd', 68: 'a'}
# Every printed key agrees with the recomputed answer for this chapter.
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
