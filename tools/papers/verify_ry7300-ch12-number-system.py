#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 12 (Number System).

    python3 tools/papers/verify_ry7300-ch12-number-system.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch12-number-system.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key page at 220 dpi). Every filed question's
keyed option must equal the book's key; one printed key (Q160) disagrees with the recomputed answer and is listed in BOOK_KEY_WRONG.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ns_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch12-number-system.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'd', 2: 'a', 3: 'b', 4: 'a', 5: 'd', 6: 'c', 7: 'c', 8: 'a', 9: 'c', 10: 'a', 11: 'd', 12: 'a', 13: 'a', 14: 'a', 15: 'a', 16: 'a', 17: 'a', 18: 'c', 19: 'b', 20: 'a', 21: 'c', 22: 'c', 23: 'c', 24: 'd', 25: 'd', 26: 'd', 27: 'a', 28: 'c', 29: 'c', 30: 'c', 31: 'd', 32: 'a', 33: 'b', 34: 'c', 35: 'd', 36: 'b', 37: 'b', 38: 'c', 39: 'd', 40: 'c', 41: 'c', 42: 'd', 43: 'b', 44: 'c', 45: 'c', 46: 'c', 47: 'c', 48: 'c', 49: 'b', 50: 'c', 51: 'd', 52: 'b', 53: 'b', 54: 'b', 55: 'b', 56: 'b', 57: 'd', 58: 'a', 59: 'b', 60: 'b', 61: 'b', 62: 'a', 63: 'b', 64: 'b', 65: 'c', 66: 'd', 67: 'b', 68: 'a', 69: 'b', 70: 'c', 71: 'c', 72: 'd', 73: 'd', 74: 'b', 75: 'd', 76: 'b', 77: 'b', 78: 'd', 79: 'b', 80: 'd', 81: 'a', 82: 'c', 83: 'b', 84: 'd', 85: 'b', 86: 'd', 87: 'c', 88: 'b', 89: 'b', 90: 'b', 91: 'b', 92: 'a', 93: 'c', 94: 'd', 95: 'b', 96: 'c', 97: 'a', 98: 'd', 99: 'c', 100: 'b', 101: 'b', 102: 'c', 103: 'd', 104: 'b', 105: 'a', 106: 'b', 107: 'c', 108: 'c', 109: 'c', 110: 'c', 111: 'b', 112: 'c', 113: 'b', 114: 'd', 115: 'b', 116: 'c', 117: 'd', 118: 'a', 119: 'b', 120: 'd', 121: 'b', 122: 'a', 123: 'c', 124: 'c', 125: 'a', 126: 'a', 127: 'd', 128: 'b', 129: 'c', 130: 'b', 131: 'd', 132: 'b', 133: 'd', 134: 'd', 135: 'b', 136: 'c', 137: 'b', 138: 'd', 139: 'b', 140: 'c', 141: 'd', 142: 'a', 143: 'b', 144: 'b', 145: 'b', 146: 'd', 147: 'a', 148: 'a', 149: 'd', 150: 'd', 151: 'a', 152: 'b', 153: 'c', 154: 'b', 155: 'c', 156: 'c', 157: 'd', 158: 'c', 159: 'a', 160: 'd', 161: 'b', 162: 'b', 163: 'a', 164: 'c', 165: 'c', 166: 'b', 167: 'a', 168: 'b', 169: 'c', 170: 'd', 171: 'a', 172: 'd', 173: 'd', 174: 'b', 175: 'c', 176: 'b', 177: 'b', 178: 'c', 179: 'd', 180: 'd', 181: 'c', 182: 'c', 183: 'b', 184: 'c', 185: 'a', 186: 'd', 187: 'b', 188: 'c', 189: 'c', 190: 'c', 191: 'a', 192: 'b', 193: 'd', 194: 'a', 195: 'a', 196: 'd', 197: 'd', 198: 'b', 199: 'a', 200: 'b', 201: 'd', 202: 'c', 203: 'd', 204: 'c', 205: 'd', 206: 'a', 207: 'b', 208: 'b', 209: 'a', 210: 'c', 211: 'b', 212: 'c', 213: 'c', 214: 'b', 215: 'a', 216: 'c', 217: 'b', 218: 'c', 219: 'c', 220: 'd', 221: 'd', 222: 'd', 223: 'b', 224: 'a', 225: 'a', 226: 'b', 227: 'd', 228: 'c', 229: 'a', 230: 'a', 231: 'b', 232: 'b', 233: 'd', 234: 'b', 235: 'd', 236: 'a', 237: 'd', 238: 'c', 239: 'b', 240: 'c', 241: 'b', 242: 'b', 243: 'c', 244: 'c', 245: 'b', 246: 'a', 247: 'c', 248: 'b', 249: 'a', 250: 'd', 251: 'c', 252: 'a', 253: 'b', 254: 'a', 255: 'd', 256: 'b', 257: 'd', 258: 'd', 259: 'd', 260: 'd', 261: 'b', 262: 'a', 263: 'a', 264: 'd', 265: 'b', 266: 'c', 267: 'c', 268: 'b', 269: 'c', 270: 'd', 271: 'b', 272: 'b', 273: 'c', 274: 'c', 275: 'b', 276: 'a', 277: 'd', 278: 'a', 279: 'd', 280: 'b', 281: 'b', 282: 'b', 283: 'a', 284: 'a', 285: 'b', 286: 'b', 287: 'b', 288: 'c', 289: 'b', 290: 'a', 291: 'd', 292: 'd', 293: 'd', 294: 'c', 295: 'd', 296: 'a', 297: 'a', 298: 'c', 299: 'd', 300: 'a', 301: 'd', 302: 'a', 303: 'b', 304: 'c', 305: 'b', 306: 'a', 307: 'b', 308: 'a', 309: 'b', 310: 'c', 311: 'b', 312: 'c', 313: 'b', 314: 'd', 315: 'd', 316: 'c', 317: 'd', 318: 'b', 319: 'c', 320: 'b', 321: 'd', 322: 'b', 323: 'b', 324: 'c', 325: 'b', 326: 'a', 327: 'c', 328: 'a', 329: 'a', 330: 'b', 331: 'a', 332: 'c', 333: 'c', 334: 'c', 335: 'c', 336: 'c', 337: 'd', 338: 'c', 339: 'b', 340: 'a', 341: 'a', 342: 'c', 343: 'a', 344: 'a', 345: 'b', 346: 'c', 347: 'c', 348: 'c', 349: 'a', 350: 'c', 351: 'd', 352: 'd', 353: 'd', 354: 'a', 355: 'b', 356: 'b', 357: 'd', 358: 'a', 359: 'b', 360: 'b', 361: 'b', 362: 'c', 363: 'c', 364: 'a', 365: 'd', 366: 'c', 367: 'b', 368: 'a', 369: 'b', 370: 'a', 371: 'b', 372: 'd', 373: 'd', 374: 'c', 375: 'a', 376: 'c', 377: 'c', 378: 'd', 379: 'a', 380: 'c', 381: 'a', 382: 'b', 383: 'b', 384: 'a', 385: 'a', 386: 'c', 387: 'c', 388: 'd', 389: 'b'}
# Q160: the printed key (d, 48) is wrong; n = 5 gives 1,704, which 48 does not divide. The greatest common divisor is 24 (b).
BOOK_KEY_WRONG = {160}
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
