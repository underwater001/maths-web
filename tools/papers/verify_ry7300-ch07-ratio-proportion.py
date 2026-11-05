#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 7 (Ratio & Proportion).

    python3 tools/papers/verify_ry7300-ch07-ratio-proportion.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch07-ratio-proportion.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; two printed keys (Q113, Q242) disagree with the recomputed answer and are listed in BOOK_KEY_WRONG; Q128's key is hidden by the book's watermark (taken as c).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._rp_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch07-ratio-proportion.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'a', 2: 'c', 3: 'c', 4: 'b', 5: 'c', 6: 'b', 7: 'd', 8: 'b', 9: 'c', 10: 'd', 11: 'a', 12: 'c', 13: 'a', 14: 'c', 15: 'c', 16: 'c', 17: 'c', 18: 'c', 19: 'c', 20: 'd', 21: 'a', 22: 'c', 23: 'd', 24: 'a', 25: 'b', 26: 'd', 27: 'a', 28: 'c', 29: 'c', 30: 'c', 31: 'a', 32: 'c', 33: 'd', 34: 'd', 35: 'a', 36: 'a', 37: 'b', 38: 'b', 39: 'b', 40: 'c', 41: 'c', 42: 'd', 43: 'c', 44: 'b', 45: 'b', 46: 'a', 47: 'd', 48: 'a', 49: 'a', 50: 'c', 51: 'a', 52: 'b', 53: 'a', 54: 'd', 55: 'c', 56: 'a', 57: 'd', 58: 'b', 59: 'c', 60: 'c', 61: 'a', 62: 'd', 63: 'd', 64: 'a', 65: 'b', 66: 'c', 67: 'b', 68: 'c', 69: 'c', 70: 'd', 71: 'c', 72: 'b', 73: 'a', 74: 'a', 75: 'd', 76: 'c', 77: 'd', 78: 'd', 79: 'd', 80: 'a', 81: 'c', 82: 'd', 83: 'a', 84: 'c', 85: 'b', 86: 'b', 87: 'b', 88: 'a', 89: 'a', 90: 'c', 91: 'c', 92: 'b', 93: 'a', 94: 'c', 95: 'b', 96: 'c', 97: 'd', 98: 'd', 99: 'd', 100: 'a', 101: 'a', 102: 'd', 103: 'c', 104: 'a', 105: 'c', 106: 'd', 107: 'b', 108: 'b', 109: 'b', 110: 'b', 111: 'b', 112: 'a', 113: 'b', 114: 'a', 115: 'b', 116: 'd', 117: 'd', 118: 'd', 119: 'c', 120: 'c', 121: 'c', 122: 'c', 123: 'a', 124: 'a', 125: 'd', 126: 'd', 127: 'c', 128: 'c', 129: 'a', 130: 'c', 131: 'b', 132: 'c', 133: 'c', 134: 'd', 135: 'a', 136: 'c', 137: 'b', 138: 'd', 139: 'c', 140: 'a', 141: 'b', 142: 'c', 143: 'a', 144: 'c', 145: 'c', 146: 'c', 147: 'a', 148: 'd', 149: 'd', 150: 'b', 151: 'b', 152: 'd', 153: 'a', 154: 'b', 155: 'd', 156: 'b', 157: 'c', 158: 'a', 159: 'b', 160: 'd', 161: 'd', 162: 'c', 163: 'c', 164: 'd', 165: 'c', 166: 'a', 167: 'c', 168: 'b', 169: 'c', 170: 'c', 171: 'c', 172: 'c', 173: 'a', 174: 'b', 175: 'a', 176: 'd', 177: 'b', 178: 'a', 179: 'a', 180: 'c', 181: 'b', 182: 'a', 183: 'b', 184: 'd', 185: 'c', 186: 'c', 187: 'a', 188: 'a', 189: 'a', 190: 'c', 191: 'a', 192: 'b', 193: 'd', 194: 'a', 195: 'd', 196: 'c', 197: 'c', 198: 'b', 199: 'a', 200: 'c', 201: 'a', 202: 'c', 203: 'd', 204: 'b', 205: 'c', 206: 'c', 207: 'b', 208: 'd', 209: 'a', 210: 'c', 211: 'a', 212: 'd', 213: 'b', 214: 'c', 215: 'b', 216: 'a', 217: 'c', 218: 'c', 219: 'a', 220: 'd', 221: 'd', 222: 'c', 223: 'b', 224: 'a', 225: 'a', 226: 'b', 227: 'c', 228: 'c', 229: 'a', 230: 'd', 231: 'c', 232: 'b', 233: 'd', 234: 'a', 235: 'd', 236: 'a', 237: 'b', 238: 'b', 239: 'd', 240: 'd', 241: 'a', 242: 'd', 243: 'c', 244: 'c', 245: 'd', 246: 'b', 247: 'b', 248: 'd', 249: 'b', 250: 'b', 251: 'b', 252: 'b', 253: 'b', 254: 'c', 255: 'c', 256: 'b', 257: 'd', 258: 'a', 259: 'b', 260: 'c', 261: 'b', 262: 'a', 263: 'a', 264: 'b', 265: 'd', 266: 'd', 267: 'c', 268: 'a', 269: 'a', 270: 'c', 271: 'd', 272: 'd', 273: 'b', 274: 'd', 275: 'd', 276: 'c', 277: 'b', 278: 'a', 279: 'a', 280: 'd', 281: 'b', 282: 'a', 283: 'c', 284: 'a', 285: 'b', 286: 'b', 287: 'a', 288: 'a', 289: 'c', 290: 'a', 291: 'b', 292: 'b', 293: 'c', 294: 'a', 295: 'a', 296: 'd', 297: 'a', 298: 'a', 299: 'b', 300: 'b', 301: 'd', 302: 'c', 303: 'b', 304: 'b', 305: 'c', 306: 'c'}
# The printed key is wrong for these (see the paper note): Q113 printed b (150 is not a multiple of 29; the answer is a, 145)
# and Q242 printed d (Rs. 180 is the wheat share; rice is c, Rs. 200).
BOOK_KEY_WRONG = {113, 242}
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
