#!/usr/bin/env python3
"""Verify and write the Partnership pilot topic.

    python3 tools/build_partnership.py           # verify, then write the data files
    python3 tools/build_partnership.py --check   # verify only

Verification, in order (any failure stops the build and nothing is written):
  1. Every PYQ: the answer recomputed from its numbers equals the keyed option, and no other option.
  2. Every practice item: the answer from the main method equals the answer from a second method
     (month-by-month simulation, or allocating the whole profit and adding it back up).
  3. Every formula, method and node references things that exist.
"""
import json, os, re, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

import partnership_content as C
import partnership_practice as PR


def num(text):
    """Numeric value of an option such as '₹25,510', '90/196' or '4:3'."""
    t = text.replace("₹", "").replace(",", "").replace("%", "").strip()
    if "/" in t:
        a, b = t.split("/"); return float(F(int(a), int(b)))
    return float(t)


def verify():
    errs = []
    for q in C.PYQS:
        got = q["_calc"]()
        if abs(got - q["_expect"]) > q["_tol"] + 1e-9:
            errs.append(f"{q['id']}: recomputed {got} but expected {q['_expect']}")
        idx = "abcd".index(q["key"])
        close = [i for i, o in enumerate(q["options"]) if abs(num(o) - got) <= max(q["_tol"], 1e-9) + 1e-6 * abs(got)]
        if close != [idx]:
            errs.append(f"{q['id']}: options matching the recomputed answer {got} are {close}, key is {idx}")
    items = PR.practice_items()
    for i, p in enumerate(items, 1):
        if p["check"] is None or F(p["correct"]) != F(p["check"]):
            errs.append(f"practice {i}: main {p['correct']} vs second method {p['check']}")
    nodes = set(C.NODES)
    for f in C.FORMULAS:
        if f["node"] not in nodes: errs.append(f"formula {f['id']}: unknown node {f['node']}")
    fids = {f["id"] for f in C.FORMULAS}
    for k, m in C.METHODS.items():
        if k not in nodes: errs.append(f"methods: unknown qtype {k}")
        for fid in m["formulas"]:
            if fid not in fids: errs.append(f"methods {k}: unknown formula {fid}")
    for q in C.PYQS:
        if q["qtype"] not in nodes: errs.append(f"{q['id']}: unknown qtype")
    return errs, len(C.PYQS), len(items)


def load(p):
    with open(p, encoding="utf-8") as fp: return json.load(fp)


def save(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fp: fp.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def main():
    errs, npyq, nprac = verify()
    if errs:
        print("VERIFY FAILED"); [print(" -", e) for e in errs]; sys.exit(1)
    print(f"verified: {npyq} PYQs, {nprac} practice questions (two methods agree), references intact")
    practice = PR_items()          # also checks the four options of every item are distinct
    if "--check" in sys.argv: return
    # nodes: merge, keep order/links symmetric
    nodes = load(os.path.join(DATA, "nodes.json"))
    nodes.update(C.NODES)
    for k, v in nodes.items():
        for l in v.get("links", []):
            if k not in nodes[l]["links"]: nodes[l]["links"].append(k)
    save(os.path.join(DATA, "nodes.json"), nodes)
    save(os.path.join(DATA, "papers.json"), C.PAPERS)
    save(os.path.join(DATA, "formulas.json"), [f for f in C.FORMULAS])
    save(os.path.join(DATA, "methods.json"), C.METHODS)
    save(os.path.join(DATA, "pyqs", "partnership.json"),
         [{k: v for k, v in q.items() if not k.startswith("_")} for q in C.PYQS])
    save(os.path.join(DATA, "practice", "partnership.json"), practice)
    print("written: nodes, papers, formulas, methods, pyqs/partnership, practice/partnership")


def PR_items():
    import random
    rng = random.Random(20250912)
    out = []
    for i, p in enumerate(PR.practice_items(), 1):
        vals = [p["correct"]] + p["traps"]
        shown = [C.inr(float(v)) for v in vals]
        if len(set(shown)) != 4:
            sys.exit(f"practice {i}: options not distinct: {shown}")
        order = list(range(4)); rng.shuffle(order)
        out.append({"id": f"pt-p{i:02d}", "qtype": p["qtype"], "level": p["level"], "text": p["text"],
                    "options": [shown[j] for j in order], "key": "abcd"[order.index(0)], "solution": p["why"]})
    return out


if __name__ == "__main__":
    main()
