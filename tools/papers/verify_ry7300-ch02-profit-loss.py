#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 2 (Profit and Loss).

    python3 tools/papers/verify_ry7300-ch02-profit-loss.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch02-profit-loss.json, and no other option. It also checks that the paper file and the topic agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the answer-key pages). Every filed question's
keyed option must equal the book's key, except the questions in BOOK_KEY_WRONG, where the recomputed answer was checked by hand
and the printed key is wrong (Q243: 143 ÷ (12/5 − 5/3) = 195 eggs, the book prints 190; Q329: 880 against 1000 is a 12% loss, the
printed key points to 17 1/2; Q384: the loss item cost 320 and sold for 288, the printed key points to 200, which is the other item's cost).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._pl_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch02-profit-loss.json")))
rows = {r["qno"]: r for r in paper["rows"]}
BOOK_KEY = {1: 'a', 2: 'c', 3: 'd', 4: 'b', 5: 'c', 6: 'b', 7: 'a', 8: 'a', 9: 'd', 10: 'd', 11: 'd', 12: 'b', 13: 'a', 14: 'a', 15: 'd', 16: 'd', 17: 'd', 18: 'a', 19: 'b', 20: 'b', 21: 'd', 22: 'b', 23: 'b', 24: 'd', 25: 'c', 26: 'd', 27: 'd', 28: 'b', 29: 'd', 30: 'c', 31: 'c', 32: 'c', 33: 'c', 34: 'c', 35: 'd', 36: 'a', 37: 'c', 38: 'd', 39: 'c', 40: 'b', 41: 'c', 42: 'b', 43: 'c', 44: 'd', 45: 'a', 46: 'c', 47: 'b', 48: 'b', 49: 'd', 50: 'b', 51: 'd', 52: 'd', 53: 'd', 54: 'c', 55: 'c', 56: 'b', 57: 'd', 58: 'd', 59: 'a', 60: 'd', 61: 'a', 62: 'c', 63: 'd', 64: 'c', 65: 'a', 66: 'd', 67: 'b', 68: 'a', 69: 'c', 70: 'c', 71: 'b', 72: 'b', 73: 'c', 74: 'a', 75: 'b', 76: 'c', 77: 'c', 78: 'b', 79: 'c', 80: 'a', 81: 'a', 82: 'c', 83: 'd', 84: 'b', 85: 'd', 86: 'c', 87: 'd', 88: 'b', 89: 'c', 90: 'a', 91: 'a', 92: 'c', 93: 'b', 94: 'd', 95: 'd', 96: 'c', 97: 'c', 98: 'b', 99: 'b', 100: 'a', 101: 'a', 102: 'b', 103: 'b', 104: 'a', 105: 'b', 106: 'b', 107: 'a', 108: 'b', 109: 'c', 110: 'a', 111: 'b', 112: 'd', 113: 'c', 114: 'c', 115: 'c', 116: 'a', 117: 'b', 118: 'c', 119: 'a', 120: 'c', 121: 'a', 122: 'b', 123: 'c', 124: 'a', 125: 'a', 126: 'b', 127: 'a', 128: 'b', 129: 'b', 130: 'b', 131: 'd', 132: 'd', 133: 'a', 134: 'b', 135: 'b', 136: 'd', 137: 'c', 138: 'd', 139: 'b', 140: 'b', 141: 'd', 142: 'a', 143: 'd', 144: 'b', 145: 'c', 146: 'd', 147: 'd', 148: 'a', 149: 'a', 150: 'a', 151: 'd', 152: 'c', 153: 'd', 154: 'b', 155: 'd', 156: 'a', 157: 'c', 158: 'd', 159: 'd', 160: 'a', 161: 'c', 162: 'c', 163: 'c', 164: 'b', 165: 'd', 166: 'd', 167: 'c', 168: 'c', 169: 'd', 170: 'a', 171: 'd', 172: 'c', 173: 'c', 174: 'c', 175: 'a', 176: 'c', 177: 'd', 178: 'd', 179: 'b', 180: 'b', 181: 'b', 182: 'd', 183: 'a', 184: 'a', 185: 'b', 186: 'd', 187: 'c', 188: 'c', 189: 'c', 190: 'a', 191: 'a', 192: 'a', 193: 'd', 194: 'd', 195: 'c', 196: 'c', 197: 'c', 198: 'c', 199: 'c', 200: 'a', 201: 'a', 202: 'c', 203: 'c', 204: 'd', 205: 'b', 206: 'c', 207: 'd', 208: 'd', 209: 'c', 210: 'c', 211: 'd', 212: 'b', 213: 'd', 214: 'd', 215: 'a', 216: 'b', 217: 'b', 218: 'c', 219: 'd', 220: 'b', 221: 'c', 222: 'c', 223: 'a', 224: 'b', 225: 'a', 226: 'a', 227: 'c', 228: 'b', 229: 'c', 230: 'c', 231: 'c', 232: 'a', 233: 'd', 234: 'c', 235: 'd', 236: 'b', 237: 'c', 238: 'd', 239: 'a', 240: 'b', 241: 'c', 242: 'c', 243: 'd', 244: 'a', 245: 'd', 246: 'c', 247: 'd', 248: 'd', 249: 'd', 250: 'c', 251: 'c', 252: 'a', 253: 'b', 254: 'd', 255: 'a', 256: 'd', 257: 'c', 258: 'd', 259: 'c', 260: 'a', 261: 'a', 262: 'a', 263: 'a', 264: 'a', 265: 'c', 266: 'a', 267: 'a', 268: 'c', 269: 'b', 270: 'c', 271: 'b', 272: 'b', 273: 'b', 274: 'a', 275: 'd', 276: 'c', 277: 'a', 278: 'c', 279: 'c', 280: 'c', 281: 'd', 282: 'b', 283: 'a', 284: 'd', 285: 'c', 286: 'a', 287: 'a', 288: 'd', 289: 'b', 290: 'b', 291: 'd', 292: 'd', 293: 'd', 294: 'd', 295: 'b', 296: 'c', 297: 'b', 298: 'c', 299: 'c', 300: 'b', 301: 'a', 302: 'a', 303: 'd', 304: 'a', 305: 'c', 306: 'b', 307: 'd', 308: 'd', 309: 'c', 310: 'b', 311: 'a', 312: 'a', 313: 'c', 314: 'b', 315: 'c', 316: 'b', 317: 'b', 318: 'a', 319: 'c', 320: 'b', 321: 'a', 322: 'a', 323: 'a', 324: 'c', 325: 'd', 326: 'a', 327: 'd', 328: 'c', 329: 'c', 330: 'b', 331: 'd', 332: 'd', 333: 'c', 334: 'a', 335: 'c', 336: 'd', 337: 'c', 338: 'b', 339: 'c', 340: 'c', 341: 'a', 342: 'd', 343: 'c', 344: 'd', 345: 'c', 346: 'b', 347: 'b', 348: 'b', 349: 'b', 350: 'a', 351: 'b', 352: 'a', 353: 'b', 354: 'b', 355: 'c', 356: 'b', 357: 'd', 358: 'c', 359: 'c', 360: 'a', 361: 'd', 362: 'c', 363: 'd', 364: 'b', 365: 'd', 366: 'c', 367: 'b', 368: 'c', 369: 'a', 370: 'c', 371: 'b', 372: 'd', 373: 'b', 374: 'd', 375: 'c', 376: 'b', 377: 'a', 378: 'b', 379: 'd', 380: 'a', 381: 'c', 382: 'b', 383: 'c', 384: 'd', 385: 'b'}
BOOK_KEY_WRONG = {243, 329, 384}
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
