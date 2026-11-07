#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 19 (LCM & HCF).

    python3 tools/papers/verify_ry7300-ch19-lcm-hcf.py

Each question carries its own recompute (a short lambda written from the question text, not from the
book's working). This script runs them again against the paper file: the recomputed value must equal
exactly the option keyed in data/papers/ry7300-ch19-lcm-hcf.json, and no other option. That independent
recomputation is the primary check and the only thing that can fail this script.

A genuine printed answer-key table was found for this chapter (book pp.650-651, covering Q1-146, with
Q41-49 illegible in the scan) - the first time one has turned up for Chapters 17-20. BOOK_KEY below is
that table, transcribed directly from the scan. It is used only as a bonus cross-check, printed as an
informational mismatch rather than a failure: two batch-1 answers (Q23, Q31) disagree with the printed
key, and in both cases the independent recomputation is unambiguous plain arithmetic while the book key
looks like its own printing error (see the paper file's "note" field for the detail). So BOOK_KEY
agreement is a confidence booster, never a source of truth that overrides recomputation.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ch19lh_ry import PYQS_RY as ALL_Q1
from topics._ch19lh2_ry import PYQS_RY as ALL_Q2
ALL_Q = ALL_Q1 + ALL_Q2

# Transcribed from book pp.650-651 (PDF pp.653-654). Q41-49 were not legible in the scan.
BOOK_KEY = {
    1: "c", 2: "c", 3: "c", 4: "b", 5: "c", 6: "d", 7: "a", 8: "d", 9: "d", 10: "a",
    11: "b", 12: "d", 13: "a", 14: "c", 15: "b", 16: "a", 17: "c", 18: "c", 19: "b", 20: "d",
    21: "a", 22: "c", 23: "a", 24: "a", 25: "a", 26: "b", 27: "b", 28: "c", 29: "a", 30: "b",
    31: "b", 32: "d", 33: "c", 34: "d", 35: "c", 36: "c", 37: "c", 38: "c", 39: "b", 40: "d",
    50: "d",
    51: "b", 52: "a", 53: "d", 54: "d", 55: "b", 56: "d", 57: "a", 58: "a", 59: "d", 60: "b",
    61: "b", 62: "b", 63: "a", 64: "a", 65: "c", 66: "c", 67: "c", 68: "b", 69: "c", 70: "a",
    71: "c", 72: "c", 73: "c", 74: "b", 75: "a", 76: "d", 77: "a", 78: "a", 79: "d", 80: "c",
    81: "c", 82: "a", 83: "d", 84: "b", 85: "d", 86: "a", 87: "b", 88: "d", 89: "c", 90: "b",
    91: "c", 92: "a", 93: "c", 94: "a", 95: "d", 96: "b", 97: "b", 98: "d", 99: "d", 100: "b",
    101: "b", 102: "a", 103: "b", 104: "c", 105: "b", 106: "c", 107: "b", 108: "d", 109: "c", 110: "c",
    111: "d", 112: "c", 113: "b", 114: "a", 115: "d", 116: "b", 117: "b", 118: "a", 119: "b", 120: "b",
    121: "b", 122: "c", 123: "d", 124: "a", 125: "b", 126: "a", 127: "c", 128: "b", 129: "c", 130: "c",
    131: "b", 132: "c", 133: "d", 134: "a", 135: "c", 136: "b", 137: "a", 138: "a", 139: "a", 140: "a",
    141: "b", 142: "a", 143: "c", 144: "c", 145: "b", 146: "d",
}
# Known, already-investigated disagreements between BOOK_KEY and the filed (independently recomputed)
# answer: plain arithmetic favours the filed answer in both cases (see module docstring above).
KNOWN_BOOK_KEY_MISMATCH = {23, 31}

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch19-lcm-hcf.json")))
rows = {r["qno"]: r for r in paper["rows"]}

bad, info, n = [], [], 0
qnos_seen = set()
for q in ALL_Q:
    n += 1
    qnos_seen.add(q["qno"])
    r = rows.get(q["qno"])
    if r is None: bad.append(f"Q{q['qno']}: not in the paper file"); continue
    if r["topic"] != "hcf-lcm": bad.append(f"Q{q['qno']}: paper topic {r['topic']} != hcf-lcm")
    got = q["_calc"]()
    vals = q["_optvals"] if q["_optvals"] is not None else [bank.num(o) for o in q["options"]]
    near = ["abcd"[k] for k, v in enumerate(vals) if abs(v - got) <= max(q["_tol"], 1e-9) + 1e-6 * abs(got)]
    if near != [r["key"]]: bad.append(f"Q{q['qno']}: recomputed {got}, matches {near}, paper key {r['key']}")
    if r["answer"] != q["options"]["abcd".index(r["key"])]: bad.append(f"Q{q['qno']}: answer text differs")
    if len(set(q["options"])) != 4: bad.append(f"Q{q['qno']}: repeated option")
    for letter, w in q.get("wrong", {}).items():
        if letter == q["key"] or letter not in "abcd": bad.append(f"Q{q['qno']}: wrong-note on invalid/key letter {letter}"); continue
        v = vals["abcd".index(letter)]
        if not w["_ok"](v): bad.append(f"Q{q['qno']}: wrong-note on {letter} fails its own check")

    bk = BOOK_KEY.get(q["qno"])
    if bk is not None and bk != r["key"] and q["qno"] not in KNOWN_BOOK_KEY_MISMATCH:
        info.append(f"Q{q['qno']}: filed key {r['key']} but printed book key says {bk} (new disagreement, not yet investigated)")

if set(rows) != qnos_seen: bad.append(f"paper rows and module questions differ: {set(rows) ^ qnos_seen}")
print(f"TOTAL {n} checked; {len(bad)} failed")
for b in bad: print("  ", b)
if info:
    print(f"INFO: {len(info)} book-key disagreement(s) not previously investigated:")
    for i in info: print("  ", i)
sys.exit(1 if bad else 0)
