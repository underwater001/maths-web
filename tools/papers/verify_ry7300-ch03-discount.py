#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 3 (Discount).

    python3 tools/papers/verify_ry7300-ch03-discount.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch03-discount.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key pages). Every filed question's
keyed option must equal the book's key, except the questions in BOOK_KEY_WRONG, where the recomputed answer was checked by hand
and the printed key is wrong (Q207: the printed key says (c) 20 : 99, but the book's own solution works it out as 100 : 99, which is option (d)).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ds_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch03-discount.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'b', 2: 'd', 3: 'b', 4: 'b', 5: 'c', 6: 'c', 7: 'd', 8: 'c', 9: 'c', 10: 'c', 11: 'b', 12: 'b', 13: 'c', 14: 'c', 15: 'c', 16: 'd', 17: 'd', 18: 'b', 19: 'a', 20: 'c', 21: 'a', 22: 'b', 23: 'c', 24: 'b', 25: 'b', 26: 'd', 27: 'b', 28: 'a', 29: 'a', 30: 'd', 31: 'c', 32: 'c', 33: 'c', 34: 'b', 35: 'c', 36: 'b', 37: 'b', 38: 'a', 39: 'a', 40: 'c', 41: 'a', 42: 'c', 43: 'd', 44: 'd', 45: 'b', 46: 'b', 47: 'd', 48: 'd', 49: 'd', 50: 'b', 51: 'd', 52: 'c', 53: 'b', 54: 'c', 55: 'd', 56: 'd', 57: 'b', 58: 'a', 59: 'a', 60: 'c', 61: 'b', 62: 'c', 63: 'c', 64: 'a', 65: 'b', 66: 'c', 67: 'a', 68: 'a', 69: 'a', 70: 'd', 71: 'a', 72: 'c', 73: 'a', 74: 'c', 75: 'd', 76: 'c', 77: 'b', 78: 'a', 79: 'a', 80: 'c', 81: 'c', 82: 'd', 83: 'a', 84: 'b', 85: 'a', 86: 'd', 87: 'c', 88: 'd', 89: 'b', 90: 'c', 91: 'a', 92: 'a', 93: 'b', 94: 'a', 95: 'c', 96: 'c', 97: 'b', 98: 'c', 99: 'd', 100: 'c', 101: 'c', 102: 'd', 103: 'b', 104: 'c', 105: 'b', 106: 'b', 107: 'd', 108: 'd', 109: 'b', 110: 'c', 111: 'd', 112: 'a', 113: 'd', 114: 'b', 115: 'a', 116: 'c', 117: 'd', 118: 'b', 119: 'c', 120: 'b', 121: 'a', 122: 'd', 123: 'a', 124: 'a', 125: 'd', 126: 'b', 127: 'a', 128: 'c', 129: 'c', 130: 'a', 131: 'c', 132: 'a', 133: 'c', 134: 'c', 135: 'a', 136: 'b', 137: 'c', 138: 'c', 139: 'd', 140: 'a', 141: 'c', 142: 'c', 143: 'c', 144: 'c', 145: 'd', 146: 'b', 147: 'c', 148: 'd', 149: 'd', 150: 'd', 151: 'a', 152: 'a', 153: 'a', 154: 'b', 155: 'c', 156: 'a', 157: 'a', 158: 'b', 159: 'b', 160: 'c', 161: 'a', 162: 'a', 163: 'c', 164: 'a', 165: 'd', 166: 'b', 167: 'c', 168: 'a', 169: 'a', 170: 'c', 171: 'c', 172: 'b', 173: 'd', 174: 'c', 175: 'c', 176: 'c', 177: 'd', 178: 'b', 179: 'b', 180: 'b', 181: 'd', 182: 'c', 183: 'c', 184: 'b', 185: 'c', 186: 'd', 187: 'b', 188: 'b', 189: 'a', 190: 'd', 191: 'c', 192: 'd', 193: 'a', 194: 'd', 195: 'c', 196: 'c', 197: 'b', 198: 'b', 199: 'a', 200: 'b', 201: 'c', 202: 'b', 203: 'd', 204: 'c', 205: 'a', 206: 'a', 207: 'c', 208: 'd', 209: 'c', 210: 'a', 211: 'd', 212: 'a', 213: 'b', 214: 'b', 215: 'a', 216: 'a', 217: 'c'}
BOOK_KEY_WRONG = {207}
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
