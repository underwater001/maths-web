#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 5 (Compound Interest).

    python3 tools/papers/verify_ry7300-ch05-compound-interest.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch05-compound-interest.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; no printed key in this chapter disagreed with the recomputed answer.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ci_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch05-compound-interest.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'd', 2: 'd', 3: 'a', 4: 'd', 5: 'b', 6: 'b', 7: 'c', 8: 'a', 9: 'a', 10: 'a', 11: 'c', 12: 'd', 13: 'b', 14: 'b', 15: 'c', 16: 'a', 17: 'c', 18: 'd', 19: 'a', 20: 'c', 21: 'b', 22: 'c', 23: 'd', 24: 'd', 25: 'c', 26: 'c', 27: 'a', 28: 'c', 29: 'c', 30: 'b', 31: 'c', 32: 'a', 33: 'c', 34: 'd', 35: 'a', 36: 'b', 37: 'b', 38: 'b', 39: 'a', 40: 'b', 41: 'c', 42: 'c', 43: 'b', 44: 'a', 45: 'c', 46: 'b', 47: 'a', 48: 'a', 49: 'c', 50: 'c', 51: 'c', 52: 'a', 53: 'a', 54: 'b', 55: 'c', 56: 'd', 57: 'c', 58: 'a', 59: 'c', 60: 'c', 61: 'd', 62: 'd', 63: 'd', 64: 'a', 65: 'd', 66: 'c', 67: 'b', 68: 'b', 69: 'a', 70: 'a', 71: 'd', 72: 'd', 73: 'a', 74: 'b', 75: 'b', 76: 'a', 77: 'b', 78: 'c', 79: 'b', 80: 'b', 81: 'b', 82: 'c', 83: 'c', 84: 'd', 85: 'b', 86: 'd', 87: 'c', 88: 'a', 89: 'd', 90: 'd', 91: 'c', 92: 'd', 93: 'a', 94: 'b', 95: 'b', 96: 'a', 97: 'a', 98: 'b', 99: 'a', 100: 'a', 101: 'c', 102: 'b', 103: 'b', 104: 'b', 105: 'c', 106: 'b', 107: 'b', 108: 'a', 109: 'd', 110: 'a', 111: 'c', 112: 'a', 113: 'b', 114: 'd', 115: 'd', 116: 'a', 117: 'a', 118: 'a', 119: 'a', 120: 'b', 121: 'b', 122: 'a', 123: 'c', 124: 'b', 125: 'c', 126: 'a', 127: 'c', 128: 'b', 129: 'b', 130: 'b', 131: 'a', 132: 'c'}
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
