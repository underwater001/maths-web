#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 18 (Average).

    python3 tools/papers/verify_ry7300-ch18-average.py

Each question carries its own recompute (a short lambda written from the question text, not from the
book's working). This script runs them again against the paper file: the recomputed value must equal
exactly the option keyed in data/papers/ry7300-ch18-average.json, and no other option.

As with Chapter 17, no compact printed answer-key table was located for the question range this
selection draws from, so there is no BOOK_KEY here — every filed answer was verified only the primary
way, by independent recomputation matching exactly one of the four printed options (see the paper
file's own "note" field).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ch18av_ry import PYQS_RY as ALL_Q

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch18-average.json")))
rows = {r["qno"]: r for r in paper["rows"]}

bad, n = [], 0
qnos_seen = set()
for q in ALL_Q:
    n += 1
    qnos_seen.add(q["qno"])
    r = rows.get(q["qno"])
    if r is None: bad.append(f"Q{q['qno']}: not in the paper file"); continue
    if r["topic"] != "average": bad.append(f"Q{q['qno']}: paper topic {r['topic']} != average")
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

if set(rows) != qnos_seen: bad.append(f"paper rows and module questions differ: {set(rows) ^ qnos_seen}")
print(f"TOTAL {n} checked; {len(bad)} failed")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
