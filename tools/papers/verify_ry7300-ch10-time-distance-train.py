#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 10 (Time, Distance & Train).

    python3 tools/papers/verify_ry7300-ch10-time-distance-train.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch10-time-distance-train.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; one printed key (Q256) disagrees with the recomputed answer and is listed in BOOK_KEY_WRONG.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._tsd_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch10-time-distance-train.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'b', 2: 'd', 3: 'c', 4: 'c', 5: 'd', 6: 'b', 7: 'c', 8: 'd', 9: 'd', 10: 'd', 11: 'b', 12: 'c', 13: 'b', 14: 'a', 15: 'c', 16: 'b', 17: 'd', 18: 'd', 19: 'c', 20: 'd', 21: 'd', 22: 'd', 23: 'd', 24: 'a', 25: 'c', 26: 'b', 27: 'c', 28: 'b', 29: 'b', 30: 'a', 31: 'c', 32: 'c', 33: 'd', 34: 'a', 35: 'a', 36: 'd', 37: 'c', 38: 'd', 39: 'c', 40: 'a', 41: 'b', 42: 'b', 43: 'c', 44: 'b', 45: 'c', 46: 'd', 47: 'c', 48: 'a', 49: 'c', 50: 'b', 51: 'b', 52: 'd', 53: 'd', 54: 'b', 55: 'b', 56: 'c', 57: 'c', 58: 'b', 59: 'a', 60: 'c', 61: 'c', 62: 'b', 63: 'c', 64: 'a', 65: 'd', 66: 'a', 67: 'b', 68: 'c', 69: 'b', 70: 'b', 71: 'a', 72: 'b', 73: 'd', 74: 'a', 75: 'd', 76: 'c', 77: 'c', 78: 'a', 79: 'c', 80: 'a', 81: 'a', 82: 'd', 83: 'd', 84: 'c', 85: 'b', 86: 'a', 87: 'c', 88: 'a', 89: 'c', 90: 'a', 91: 'c', 92: 'd', 93: 'b', 94: 'b', 95: 'c', 96: 'c', 97: 'c', 98: 'b', 99: 'b', 100: 'a', 101: 'b', 102: 'c', 103: 'b', 104: 'a', 105: 'a', 106: 'b', 107: 'c', 108: 'd', 109: 'b', 110: 'd', 111: 'd', 112: 'c', 113: 'a', 114: 'b', 115: 'b', 116: 'c', 117: 'a', 118: 'd', 119: 'd', 120: 'a', 121: 'd', 122: 'c', 123: 'b', 124: 'c', 125: 'd', 126: 'c', 127: 'c', 128: 'c', 129: 'd', 130: 'a', 131: 'b', 132: 'c', 133: 'b', 134: 'b', 135: 'a', 136: 'c', 137: 'a', 138: 'b', 139: 'c', 140: 'b', 141: 'c', 142: 'b', 143: 'a', 144: 'c', 145: 'b', 146: 'b', 147: 'b', 148: 'c', 149: 'c', 150: 'a', 151: 'b', 152: 'a', 153: 'a', 154: 'b', 155: 'b', 156: 'b', 157: 'b', 158: 'c', 159: 'c', 160: 'a', 161: 'a', 162: 'b', 163: 'a', 164: 'a', 165: 'a', 166: 'b', 167: 'a', 168: 'b', 169: 'c', 170: 'b', 171: 'd', 172: 'c', 173: 'd', 174: 'c', 175: 'c', 176: 'c', 177: 'a', 178: 'b', 179: 'b', 180: 'a', 181: 'a', 182: 'b', 183: 'c', 184: 'c', 185: 'a', 186: 'c', 187: 'c', 188: 'b', 189: 'c', 190: 'b', 191: 'd', 192: 'd', 193: 'b', 194: 'b', 195: 'a', 196: 'a', 197: 'd', 198: 'b', 199: 'a', 200: 'd', 201: 'd', 202: 'c', 203: 'a', 204: 'b', 205: 'd', 206: 'a', 207: 'd', 208: 'b', 209: 'c', 210: 'c', 211: 'b', 212: 'c', 213: 'a', 214: 'c', 215: 'b', 216: 'b', 217: 'b', 218: 'b', 219: 'c', 220: 'b', 221: 'a', 222: 'c', 223: 'c', 224: 'd', 225: 'a', 226: 'b', 227: 'b', 228: 'd', 229: 'c', 230: 'b', 231: 'c', 232: 'b', 233: 'b', 234: 'a', 235: 'a', 236: 'a', 237: 'b', 238: 'b', 239: 'b', 240: 'a', 241: 'a', 242: 'c', 243: 'b', 244: 'c', 245: 'c', 246: 'a', 247: 'b', 248: 'c', 249: 'b', 250: 'b', 251: 'c', 252: 'b', 253: 'c', 254: 'a', 255: 'c', 256: 'c', 257: 'b'}
# Q256: the printed key (c, 3 lakh) is wrong; the recomputed answer is d (1 1/2 lakh).
BOOK_KEY_WRONG = {256}
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
