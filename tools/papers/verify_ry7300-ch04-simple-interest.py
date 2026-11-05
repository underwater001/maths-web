#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 4 (Simple Interest).

    python3 tools/papers/verify_ry7300-ch04-simple-interest.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch04-simple-interest.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; no printed key in this chapter disagreed with the recomputed answer.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._si_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch04-simple-interest.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'b', 2: 'a', 3: 'd', 4: 'c', 5: 'a', 6: 'c', 7: 'b', 8: 'c', 9: 'a', 10: 'c', 11: 'a', 12: 'd', 13: 'b', 14: 'b', 15: 'a', 16: 'c', 17: 'c', 18: 'd', 19: 'd', 20: 'c', 21: 'a', 22: 'd', 23: 'a', 24: 'c', 25: 'd', 26: 'c', 27: 'a', 28: 'd', 29: 'd', 30: 'a', 31: 'a', 32: 'c', 33: 'a', 34: 'a', 35: 'c', 36: 'c', 37: 'b', 38: 'c', 39: 'd', 40: 'c', 41: 'd', 42: 'a', 43: 'a', 44: 'd', 45: 'd', 46: 'a', 47: 'a', 48: 'b', 49: 'c', 50: 'c', 51: 'b', 52: 'c', 53: 'c', 54: 'c', 55: 'c', 56: 'a', 57: 'b', 58: 'b', 59: 'd', 60: 'c', 61: 'c', 62: 'd', 63: 'd', 64: 'a', 65: 'c', 66: 'a', 67: 'b', 68: 'c', 69: 'a', 70: 'd', 71: 'd', 72: 'a', 73: 'c', 74: 'c', 75: 'c', 76: 'c', 77: 'c', 78: 'b', 79: 'd', 80: 'a', 81: 'b', 82: 'c', 83: 'a', 84: 'a', 85: 'b', 86: 'b', 87: 'c', 88: 'b', 89: 'b', 90: 'c', 91: 'b', 92: 'd', 93: 'a', 94: 'c', 95: 'd', 96: 'b', 97: 'd', 98: 'b', 99: 'c', 100: 'd', 101: 'c', 102: 'b', 103: 'a', 104: 'd', 105: 'a', 106: 'd', 107: 'c', 108: 'c', 109: 'a', 110: 'a', 111: 'a', 112: 'a', 113: 'd', 114: 'd', 115: 'b', 116: 'd', 117: 'd', 118: 'd', 119: 'c', 120: 'a', 121: 'c', 122: 'c', 123: 'a', 124: 'd', 125: 'b', 126: 'a', 127: 'a', 128: 'c', 129: 'b', 130: 'a', 131: 'a', 132: 'a', 133: 'd', 134: 'c', 135: 'b', 136: 'a', 137: 'c'}
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
