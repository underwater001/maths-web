#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 1 (Percentage).

    python3 tools/papers/verify_ry7300-ch01-percentage.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch01-percentage.json, and no other option. It also checks that the paper file and the topic agree.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._pc_ry import PYQS_RY

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch01-percentage.json")))
rows = {r["qno"]: r for r in paper["rows"]}
bad, n = [], 0
for q in PYQS_RY:
    n += 1
    r = rows.get(q["qno"])
    if r is None: bad.append(f"Q{q['qno']}: not in the paper file"); continue
    got = q["_calc"]()
    vals = q["_optvals"]
    near = ["abcd"[k] for k, v in enumerate(vals) if abs(v - got) <= max(q["_tol"], 1e-9) + 1e-6 * abs(got)]
    if near != [r["key"]]: bad.append(f"Q{q['qno']}: recomputed {got}, matches {near}, paper key {r['key']}")
    if r["answer"] != q["options"]["abcd".index(r["key"])]: bad.append(f"Q{q['qno']}: answer text differs")
    if len(set(q["options"])) != 4: bad.append(f"Q{q['qno']}: repeated option")
if set(rows) != {q["qno"] for q in PYQS_RY}: bad.append("paper rows and topic questions differ")
print(f"TOTAL {n} checked; {len(bad)} failed")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
