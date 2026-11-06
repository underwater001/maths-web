#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 14 (Simplification).

    python3 tools/papers/verify_ry7300-ch14-simplification.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch14-simplification.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; no printed key among the filed questions disagrees with the recomputed answer (BOOK_KEY_WRONG is empty). Q274, whose printed key is wrong, is not filed (see the paper's note).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._sm_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch14-simplification.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'a', 2: 'a', 3: 'c', 4: 'a', 5: 'c', 6: 'c', 7: 'a', 8: 'c', 9: 'c', 10: 'a', 11: 'd', 12: 'a', 13: 'a', 14: 'b', 15: 'd', 16: 'c', 17: 'b', 18: 'c', 19: 'd', 20: 'b', 21: 'd', 22: 'b', 23: 'a', 24: 'a', 25: 'd', 26: 'c', 27: 'c', 28: 'b', 29: 'a', 30: 'd', 31: 'd', 32: 'b', 33: 'd', 34: 'd', 35: 'd', 36: 'd', 37: 'c', 38: 'd', 39: 'a', 40: 'd', 41: 'c', 42: 'a', 43: 'a', 44: 'c', 45: 'd', 46: 'b', 47: 'a', 48: 'a', 49: 'd', 50: 'c', 51: 'b', 52: 'b', 53: 'b', 54: 'c', 55: 'c', 56: 'b', 57: 'c', 58: 'a', 59: 'c', 60: 'b', 61: 'd', 62: 'c', 63: 'c', 64: 'a', 65: 'd', 66: 'c', 67: 'c', 68: 'b', 69: 'd', 70: 'b', 71: 'c', 72: 'c', 73: 'c', 74: 'b', 75: 'b', 76: 'd', 77: 'b', 78: 'b', 79: 'a', 80: 'd', 81: 'd', 82: 'a', 83: 'b', 84: 'c', 85: 'c', 86: 'b', 87: 'b', 88: 'a', 89: 'c', 90: 'a', 91: 'd', 92: 'b', 93: 'a', 94: 'd', 95: 'b', 96: 'b', 97: 'a', 98: 'b', 99: 'd', 100: 'b', 101: 'c', 102: 'a', 103: 'b', 104: 'd', 105: 'b', 106: 'b', 107: 'a', 108: 'd', 109: 'd', 110: 'c', 111: 'b', 112: 'd', 113: 'b', 114: 'b', 115: 'd', 116: 'b', 117: 'd', 118: 'b', 119: 'c', 120: 'd', 121: 'c', 122: 'c', 123: 'c', 124: 'c', 125: 'b', 126: 'a', 127: 'c', 128: 'a', 129: 'd', 130: 'a', 131: 'a', 132: 'c', 133: 'd', 134: 'c', 135: 'b', 136: 'a', 137: 'b', 138: 'a', 139: 'd', 140: 'c', 141: 'a', 142: 'd', 143: 'c', 144: 'b', 145: 'd', 146: 'c', 147: 'd', 148: 'd', 149: 'd', 150: 'a', 151: 'd', 152: 'c', 153: 'c', 154: 'b', 155: 'c', 156: 'b', 157: 'd', 158: 'c', 159: 'c', 160: 'c', 161: 'b', 162: 'a', 163: 'b', 164: 'd', 165: 'd', 166: 'b', 167: 'd', 168: 'c', 169: 'c', 170: 'c', 171: 'a', 172: 'b', 173: 'a', 174: 'c', 175: 'a', 176: 'a', 177: 'd', 178: 'd', 179: 'a', 180: 'd', 181: 'c', 182: 'a', 183: 'b', 184: 'b', 185: 'a', 186: 'd', 187: 'd', 188: 'c', 189: 'c', 190: 'c', 191: 'c', 192: 'd', 193: 'b', 194: 'c', 195: 'a', 196: 'b', 197: 'b', 198: 'b', 199: 'c', 200: 'a', 201: 'b', 202: 'a', 203: 'd', 204: 'a', 205: 'b', 206: 'b', 207: 'a', 208: 'c', 209: 'd', 210: 'b', 211: 'c', 212: 'b', 213: 'd', 214: 'c', 215: 'c', 216: 'b', 217: 'b', 218: 'b', 219: 'a', 220: 'b', 221: 'a', 222: 'c', 223: 'c', 224: 'a', 225: 'c', 226: 'c', 227: 'a', 228: 'b', 229: 'b', 230: 'a', 231: 'd', 232: 'c', 233: 'd', 234: 'b', 235: 'a', 236: 'd', 237: 'd', 238: 'c', 239: 'd', 240: 'c', 241: 'a', 242: 'a', 243: 'b', 244: 'b', 245: 'a', 246: 'a', 247: 'c', 248: 'b', 249: 'b', 250: 'd', 251: 'b', 252: 'b', 253: 'a', 254: 'a', 255: 'd', 256: 'c', 257: 'a', 258: 'b', 259: 'd', 260: 'b', 261: 'd', 262: 'd', 263: 'b', 264: 'c', 265: 'd', 266: 'c', 267: 'a', 268: 'b', 269: 'd', 270: 'a', 271: 'a', 272: 'a', 273: 'd', 274: 'd'}
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
