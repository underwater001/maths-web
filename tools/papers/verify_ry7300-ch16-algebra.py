#!/usr/bin/env python3
"""Recompute every filed question of Rakesh Yadav '7300+ Maths', Chapter 16 (Algebra).

    python3 tools/papers/verify_ry7300-ch16-algebra.py

Each question carries its own recompute (a short lambda written from the question text, not from the book's working).
This script runs them again against the paper file: the recomputed value must equal exactly the option keyed in
data/papers/ry7300-ch16-algebra.json, and no other option. It also checks that the paper file and the three topics
(algebraic-identities, ratio-proportion, linear-equations) that this chapter's questions were split across agree.

Independent check: BOOK_KEY is the book's own printed answer key (read from the two-page answer-key table at the end
of the chapter, at 130-150 dpi). Every filed question's keyed option must equal the book's key; no printed key among
the filed questions disagrees with the recomputed answer (BOOK_KEY_WRONG is empty) — this chapter's book key was
double-checked question by question against an independent recomputation before any question was filed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import bank
from topics._ch16a_ry import PYQS_RY as A
from topics._ch16r_ry import PYQS_RY as R
from topics._ch16l_ry import PYQS_RY as L

ALL = [(q, "algebraic-identities") for q in A] + [(q, "ratio-proportion") for q in R] + [(q, "linear-equations") for q in L]

paper = json.load(open(os.path.join(HERE, "..", "..", "data", "papers", "ry7300-ch16-algebra.json")))
rows = {r["qno"]: r for r in paper["rows"]}

BOOK_KEY = {1: 'a', 2: 'c', 19: 'c', 5: 'd', 97: 'a', 114: 'a', 119: 'b', 121: 'b', 128: 'c', 131: 'b', 132: 'c',
            134: 'a', 167: 'd', 174: 'a', 230: 'c', 374: 'b', 396: 'd', 406: 'c', 412: 'a', 417: 'a', 420: 'c', 422: 'c',
            423: 'b', 433: 'b', 437: 'c', 438: 'a'}
BOOK_KEY_WRONG = set()

bad, n = [], 0
qnos_seen = set()
for q, topic in ALL:
    n += 1
    qnos_seen.add(q["qno"])
    r = rows.get(q["qno"])
    if r is None: bad.append(f"Q{q['qno']}: not in the paper file"); continue
    if r["topic"] != topic: bad.append(f"Q{q['qno']}: paper topic {r['topic']} != module topic {topic}")
    got = q["_calc"]()
    vals = q["_optvals"] if q["_optvals"] is not None else [bank.num(o) for o in q["options"]]
    near = ["abcd"[k] for k, v in enumerate(vals) if abs(v - got) <= max(q["_tol"], 1e-9) + 1e-6 * abs(got)]
    if near != [r["key"]]: bad.append(f"Q{q['qno']}: recomputed {got}, matches {near}, paper key {r['key']}")
    if q["qno"] in BOOK_KEY and q["qno"] not in BOOK_KEY_WRONG and BOOK_KEY[q["qno"]] != r["key"]:
        bad.append(f"Q{q['qno']}: paper key {r['key']} differs from the book's printed key {BOOK_KEY[q['qno']]}")
    if r["answer"] != q["options"]["abcd".index(r["key"])]: bad.append(f"Q{q['qno']}: answer text differs")
    if len(set(q["options"])) != 4: bad.append(f"Q{q['qno']}: repeated option")

if set(rows) != qnos_seen: bad.append(f"paper rows and topic questions differ: {set(rows) ^ qnos_seen}")
if set(BOOK_KEY) != qnos_seen: bad.append(f"BOOK_KEY and filed questions differ: {set(BOOK_KEY) ^ qnos_seen}")
print(f"TOTAL {n} checked; {len(bad)} failed")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
