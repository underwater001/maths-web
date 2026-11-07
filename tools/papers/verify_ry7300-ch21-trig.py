#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 21 (Trigonometry).

    python3 tools/papers/verify_ry7300-ch21-trig.py

Each question carries its own recompute (a short lambda written from the question text, not from the
book's working). This script runs them again against the paper file: the recomputed value must equal
exactly the option keyed in data/papers/ry7300-ch21-trig.json, and no other option. That independent
recomputation is the primary check and the only thing that can fail this script.

The book prints a full answer key for this chapter (pp.689-690, Q1-273). BOOK_KEY below is that table,
transcribed for every one of the 21 filed questions, and used only as a bonus cross-check (printed as
informational, never a failure) - exactly the same role it played for Chapter 19.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ch21tr_ry import PYQS_RY as ALL_Q

# Transcribed from the book's own answer key, pp.689-690 (PDF pp.692-693), for the filed questions only.
BOOK_KEY = {
    1: "c", 3: "d", 4: "b", 5: "c", 6: "c", 9: "d", 10: "b", 32: "a", 34: "d", 42: "d",
    69: "c", 70: "a", 75: "b", 76: "d", 130: "b", 146: "b", 159: "d", 202: "b", 210: "b", 212: "b", 229: "d",
}

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch21-trig.json")))
rows = {r["qno"]: r for r in paper["rows"]}

bad, info, n = [], [], 0
qnos_seen = set()
for q in ALL_Q:
    n += 1
    qnos_seen.add(q["qno"])
    r = rows.get(q["qno"])
    if r is None: bad.append(f"Q{q['qno']}: not in the paper file"); continue
    if r["topic"] != "trig-ratios": bad.append(f"Q{q['qno']}: paper topic {r['topic']} != trig-ratios")
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
    if bk is not None and bk != r["key"]:
        info.append(f"Q{q['qno']}: filed key {r['key']} but printed book key says {bk}")

if set(rows) != qnos_seen: bad.append(f"paper rows and module questions differ: {set(rows) ^ qnos_seen}")
print(f"TOTAL {n} checked; {len(bad)} failed")
for b in bad: print("  ", b)
if info:
    print(f"INFO: {len(info)} book-key disagreement(s):")
    for i in info: print("  ", i)
sys.exit(1 if bad else 0)
