#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 13 (Power, Indices & Surds).

    python3 tools/papers/verify_ry7300-ch13-power-indices-surds.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch13-power-indices-surds.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; no printed key in this chapter disagrees with the recomputed answer (BOOK_KEY_WRONG is empty).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ix_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch13-power-indices-surds.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'c', 2: 'a', 3: 'a', 4: 'c', 5: 'c', 6: 'b', 7: 'd', 8: 'c', 9: 'c', 10: 'c', 11: 'b', 12: 'a', 13: 'b', 14: 'a', 15: 'd', 16: 'b', 17: 'c', 18: 'b', 19: 'b', 20: 'c', 21: 'a', 22: 'a', 23: 'c', 24: 'c', 25: 'b', 26: 'b', 27: 'a', 28: 'd', 29: 'a', 30: 'a', 31: 'c', 32: 'c', 33: 'a', 34: 'a', 35: 'c', 36: 'd', 37: 'c', 38: 'c', 39: 'a', 40: 'c', 41: 'a', 42: 'd', 43: 'a', 44: 'b', 45: 'b', 46: 'b', 47: 'a', 48: 'b', 49: 'b', 50: 'a', 51: 'a', 52: 'd', 53: 'c', 54: 'a', 55: 'c', 56: 'd', 57: 'a', 58: 'a', 59: 'a', 60: 'c', 61: 'c', 62: 'b', 63: 'c', 64: 'b', 65: 'c', 66: 'd', 67: 'a', 68: 'c', 69: 'b', 70: 'd', 71: 'c', 72: 'b', 73: 'a', 74: 'd', 75: 'a', 76: 'd', 77: 'c', 78: 'a', 79: 'c', 80: 'b', 81: 'd', 82: 'b', 83: 'd', 84: 'c', 85: 'c', 86: 'a', 87: 'c', 88: 'd', 89: 'a', 90: 'b', 91: 'b', 92: 'c', 93: 'd', 94: 'c', 95: 'b', 96: 'c', 97: 'b', 98: 'b', 99: 'a', 100: 'c', 101: 'd', 102: 'c', 103: 'c', 104: 'b', 105: 'a', 106: 'b', 107: 'b', 108: 'a', 109: 'c', 110: 'b', 111: 'a', 112: 'c', 113: 'c', 114: 'a', 115: 'd', 116: 'b', 117: 'a', 118: 'b', 119: 'a', 120: 'c', 121: 'd', 122: 'a', 123: 'd', 124: 'a', 125: 'a', 126: 'c', 127: 'a', 128: 'd', 129: 'a', 130: 'd', 131: 'a', 132: 'd', 133: 'a', 134: 'b', 135: 'd', 136: 'a', 137: 'c', 138: 'b', 139: 'b', 140: 'd', 141: 'd', 142: 'b', 143: 'b', 144: 'c', 145: 'a', 146: 'b', 147: 'b', 148: 'b', 149: 'b', 150: 'c', 151: 'b', 152: 'b', 153: 'c', 154: 'd', 155: 'b', 156: 'd', 157: 'b', 158: 'a', 159: 'c', 160: 'a', 161: 'c', 162: 'd', 163: 'b', 164: 'b', 165: 'c', 166: 'c', 167: 'b', 168: 'c', 169: 'a', 170: 'a', 171: 'a', 172: 'd', 173: 'd', 174: 'c', 175: 'b', 176: 'b', 177: 'b', 178: 'c', 179: 'c', 180: 'a', 181: 'c', 182: 'a', 183: 'b', 184: 'd', 185: 'b', 186: 'c', 187: 'b', 188: 'a', 189: 'd', 190: 'd', 191: 'a', 192: 'a', 193: 'a', 194: 'd', 195: 'b', 196: 'c', 197: 'c', 198: 'd', 199: 'd', 200: 'd', 201: 'a', 202: 'd', 203: 'a', 204: 'a', 205: 'a', 206: 'c', 207: 'c', 208: 'c', 209: 'b', 210: 'c', 211: 'd', 212: 'd', 213: 'c'}
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
