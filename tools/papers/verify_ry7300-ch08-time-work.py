#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 8 (Time & Work).

    python3 tools/papers/verify_ry7300-ch08-time-work.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch08-time-work.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; two printed keys (Q114, Q117) disagree with the recomputed answer and are listed in BOOK_KEY_WRONG.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._tw_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch08-time-work.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'c', 2: 'a', 3: 'c', 4: 'a', 5: 'c', 6: 'c', 7: 'c', 8: 'd', 9: 'b', 10: 'b', 11: 'b', 12: 'c', 13: 'd', 14: 'd', 15: 'a', 16: 'b', 17: 'd', 18: 'a', 19: 'c', 20: 'c', 21: 'c', 22: 'a', 23: 'c', 24: 'a', 25: 'b', 26: 'b', 27: 'c', 28: 'c', 29: 'c', 30: 'a', 31: 'b', 32: 'b', 33: 'c', 34: 'c', 35: 'a', 36: 'c', 37: 'c', 38: 'a', 39: 'a', 40: 'c', 41: 'a', 42: 'd', 43: 'c', 44: 'd', 45: 'a', 46: 'a', 47: 'd', 48: 'b', 49: 'd', 50: 'b', 51: 'c', 52: 'c', 53: 'c', 54: 'b', 55: 'a', 56: 'a', 57: 'c', 58: 'c', 59: 'd', 60: 'd', 61: 'd', 62: 'c', 63: 'd', 64: 'b', 65: 'b', 66: 'd', 67: 'a', 68: 'c', 69: 'a', 70: 'd', 71: 'd', 72: 'c', 73: 'c', 74: 'a', 75: 'd', 76: 'a', 77: 'd', 78: 'c', 79: 'a', 80: 'b', 81: 'b', 82: 'b', 83: 'a', 84: 'b', 85: 'b', 86: 'c', 87: 'd', 88: 'd', 89: 'b', 90: 'b', 91: 'a', 92: 'c', 93: 'd', 94: 'c', 95: 'd', 96: 'a', 97: 'c', 98: 'a', 99: 'b', 100: 'c', 101: 'c', 102: 'b', 103: 'b', 104: 'a', 105: 'b', 106: 'b', 107: 'b', 108: 'b', 109: 'b', 110: 'c', 111: 'a', 112: 'a', 113: 'a', 114: 'd', 115: 'c', 116: 'c', 117: 'd', 118: 'c', 119: 'c', 120: 'd', 121: 'a', 122: 'c', 123: 'a', 124: 'a', 125: 'a', 126: 'c', 127: 'a', 128: 'a', 129: 'c', 130: 'c', 131: 'c', 132: 'c', 133: 'b', 134: 'a', 135: 'b', 136: 'a', 137: 'c', 138: 'a', 139: 'd', 140: 'a', 141: 'd', 142: 'a', 143: 'b', 144: 'b', 145: 'd', 146: 'b', 147: 'b', 148: 'c', 149: 'd', 150: 'd', 151: 'd', 152: 'c', 153: 'c', 154: 'a', 155: 'b', 156: 'c', 157: 'c', 158: 'b', 159: 'a', 160: 'c', 161: 'a', 162: 'd', 163: 'c', 164: 'd', 165: 'b', 166: 'd', 167: 'c', 168: 'b', 169: 'b', 170: 'c', 171: 'd', 172: 'b', 173: 'b', 174: 'a', 175: 'b', 176: 'b', 177: 'd', 178: 'b', 179: 'd', 180: 'a', 181: 'c', 182: 'a', 183: 'a', 184: 'b', 185: 'd', 186: 'c', 187: 'd', 188: 'c', 189: 'b', 190: 'c', 191: 'c', 192: 'a', 193: 'c', 194: 'a', 195: 'b', 196: 'd', 197: 'd', 198: 'a', 199: 'b', 200: 'c', 201: 'c', 202: 'c', 203: 'a', 204: 'c', 205: 'a', 206: 'a', 207: 'c', 208: 'c', 209: 'd', 210: 'a', 211: 'c', 212: 'b', 213: 'b', 214: 'a', 215: 'd', 216: 'a', 217: 'a', 218: 'd', 219: 'a', 220: 'd', 221: 'b', 222: 'd', 223: 'b', 224: 'a', 225: 'b', 226: 'c', 227: 'b', 228: 'd', 229: 'c', 230: 'a', 231: 'b', 232: 'b', 233: 'a', 234: 'd', 235: 'b', 236: 'a', 237: 'b', 238: 'b', 239: 'd', 240: 'a', 241: 'd', 242: 'b', 243: 'c', 244: 'c', 245: 'a', 246: 'c', 247: 'a', 248: 'c', 249: 'c', 250: 'c', 251: 'a', 252: 'a', 253: 'c', 254: 'b', 255: 'd', 256: 'b', 257: 'c', 258: 'd', 259: 'a', 260: 'b', 261: 'b', 262: 'b', 263: 'd', 264: 'b', 265: 'a', 266: 'd', 267: 'c', 268: 'a', 269: 'b', 270: 'a', 271: 'c', 272: 'c', 273: 'b', 274: 'c'}
# The printed key is wrong for these: Q114 and Q117 both ask for HALF the work, but the printed key (d) is the time for the whole
# work (8 months and 11 1/13 months). Half the work takes 4 months (b) and 5 7/13 months (c).
BOOK_KEY_WRONG = {114, 117}
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
