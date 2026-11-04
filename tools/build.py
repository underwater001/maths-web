#!/usr/bin/env python3
"""Assemble the site's data from the topic shards and the paper files. Cheap: no question is re-verified here.

    python3 tools/build.py            # fail if any topic shard is stale, else write data/core.json and data/index/
    python3 tools/build.py --rebuild  # first rebuild the stale shards (tools/build_topic.py --all)

Inputs   data/tree.json            junctions and topics (hand-kept; a new topic is one new entry)
         data/papers/<id>.json     one file per paper: its details and one row per Quant question (topic, key, answer)
         data/shards/<topic>.json  built by tools/build_topic.py: concepts, question types, formulas, methods, PYQs, practice
Outputs  data/core.json            small, loaded at start: all nodes, paper list, likelihood stats, light question list
         data/index/<topic>.json   the indexed PYQs of each topic, even topics without a shard yet

The site loads core.json first and fetches a topic's shard only when that topic is opened, so the
start-up cost stays the same however many questions are added.
"""
import json, os, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

import bank
import build_topic as BT


def jload(p):
    with open(p, encoding="utf-8") as fp:
        return json.load(fp)


def write_if_changed(path, obj, indent=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=indent, separators=None if indent else (",", ":")) + "\n"
    if os.path.exists(path) and open(path, encoding="utf-8").read() == text:
        return False
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(text)
    return True


def stat_block(rows, qtype_of, level_of, n_papers):
    """Counts for one scope. A 'shift' is one paper; `shifts` is how many papers a topic or type appeared in."""
    topics, qtypes = {}, {}
    for r in rows:
        t = topics.setdefault(r["topic"], {"n": 0, "papers": set(), "kinds": Counter()})
        t["n"] += 1; t["papers"].add(r["paper"]); t["kinds"][r["kind"]] += 1
        qt = qtype_of.get(r["id"])
        if qt:
            q = qtypes.setdefault(qt, {"n": 0, "papers": set(), "kinds": Counter(), "levels": Counter()})
            q["n"] += 1; q["papers"].add(r["paper"]); q["kinds"][r["kind"]] += 1; q["levels"][level_of[r["id"]]] += 1
    def fin(d, per_shift):
        out = {}
        for k, v in sorted(d.items()):
            o = {"n": v["n"], "shifts": len(v["papers"]), "lik": bank.likelihood(len(v["papers"]), n_papers), "kinds": dict(v["kinds"])}
            if per_shift: o["perShift"] = round(v["n"] / n_papers, 2)
            if "levels" in v: o["levels"] = {lv: v["levels"].get(lv, 0) for lv in bank.LEVELS}
            out[k] = o
        return out
    return {"papers": n_papers, "questions": len(rows), "topics": fin(topics, True), "qtypes": fin(qtypes, False)}


def main():
    if "--rebuild" in sys.argv:
        if subprocess.call([sys.executable, os.path.join(HERE, "build_topic.py"), "--all"]) != 0: sys.exit(1)
    errs = []
    tree = jload(os.path.join(DATA, "tree.json"))

    # ---- shards: must exist and be current for every topic module --------------------------------
    modules = BT.all_topics()
    shards = {}
    for t in modules:
        p = os.path.join(DATA, "shards", t + ".json")
        if not os.path.exists(p): errs.append(f"topic {t}: no shard. Run: python3 tools/build_topic.py {t}"); continue
        s = jload(p)
        if s["src_hash"] != BT.source_hash(t): errs.append(f"topic {t}: shard is stale. Run: python3 tools/build_topic.py {t}"); continue
        shards[t] = s
    for f in os.listdir(os.path.join(DATA, "shards")) if os.path.isdir(os.path.join(DATA, "shards")) else []:
        if f[:-5] not in modules: errs.append(f"shard {f} has no module in tools/topics/")

    # ---- nodes: tree + shard nodes, links mirrored ----------------------------------------------
    nodes = {k: dict(v) for k, v in tree.items()}
    for t, s in shards.items():
        for k, n in s["nodes"].items():
            if k in nodes: errs.append(f"node id {k} is used by two topics")
            nodes[k] = dict(n)
    for k, n in nodes.items():
        n["links"] = list(n.get("links", []))
        if n["parent"] != "hub" and n["parent"] not in nodes: errs.append(f"node {k}: parent {n['parent']} missing")
        if n["kind"] == "junction" and ("hue" not in n or n["parent"] != "hub"): errs.append(f"junction {k}: needs hue and parent hub")
        if n["kind"] == "topic" and nodes.get(n["parent"], {}).get("kind") != "junction": errs.append(f"topic {k}: parent must be a junction")
    for k, n in list(nodes.items()):
        for l in n["links"]:
            if l not in nodes: errs.append(f"node {k}: link {l} missing")
            elif k not in nodes[l]["links"]: nodes[l]["links"].append(k)      # links are written on one side only; mirror them
    for n in nodes.values(): n["links"].sort()

    # ---- papers ---------------------------------------------------------------------------------
    papers, rows = [], []
    for f in sorted(os.listdir(os.path.join(DATA, "papers"))):
        if not f.endswith(".json"): continue
        p = jload(os.path.join(DATA, "papers", f))
        if p["id"] + ".json" != f: errs.append(f"papers/{f}: id {p['id']} does not match the file name")
        seen = set()
        for r in p["rows"]:
            if r["qno"] in seen: errs.append(f"{p['id']}: question {r['qno']} appears twice")
            seen.add(r["qno"])
            if nodes.get(r["topic"], {}).get("kind") != "topic": errs.append(f"{p['id']} Q{r['qno']}: {r['topic']!r} is not a topic in data/tree.json")
            rows.append({"id": f"{p['id']}-Q{r['qno']}", "paper": p["id"], "kind": p["kind"], "exam": p["exam"], "topic": r["topic"]})
        papers.append({k: v for k, v in p.items() if k != "rows"} | {"n": len(p["rows"])})
    if errs:
        print("BUILD FAILED"); [print(" -", e) for e in errs]; sys.exit(1)

    # ---- stats: how often each topic and question type appears, per exam and overall ------------
    qtype_of = {q["id"]: q["qtype"] for s in shards.values() for q in s["pyqs"]}
    level_of = {q["id"]: q["level"] for s in shards.values() for q in s["pyqs"]}
    scopes = {"all": rows}
    for r in rows: scopes.setdefault(r["exam"], [])
    for r in rows:
        if r["exam"] != "all": scopes[r["exam"]] = scopes.get(r["exam"], []) + [r]
    stats = {}
    for name, rs in scopes.items():
        n_papers = len({r["paper"] for r in rs}) if rs else 0
        if n_papers: stats[name] = stat_block(rs, qtype_of, level_of, n_papers)

    # ---- the light question list used by the bank's filters (details are in the shards) ----------
    cols = ["id", "topic", "qtype", "level", "src", "tech"]
    bank_rows = []
    for t, s in shards.items():
        for q in s["pyqs"]: bank_rows.append([q["id"], t, q["qtype"], q["level"], "pyq", q["tech"]])
        for q in s["practice"]: bank_rows.append([q["id"], t, q["qtype"], q["level"], "practice", q["tech"]])

    topics_meta = {}
    by_topic = defaultdict(list)
    for p in sorted(os.listdir(os.path.join(DATA, "papers"))):
        pj = jload(os.path.join(DATA, "papers", p))
        for r in pj["rows"]:
            by_topic[r["topic"]].append({"id": f"{pj['id']}-Q{r['qno']}", "paper": pj["id"], "qno": r["qno"], "key": r["key"], "answer": r["answer"], "verified": r["verified"]})
    for t, rs in sorted(by_topic.items()):
        write_if_changed(os.path.join(DATA, "index", t + ".json"), rs)
    for k, n in nodes.items():
        if n["kind"] == "topic":
            s = shards.get(k)
            topics_meta[k] = {"indexed": len(by_topic.get(k, [])), "built": bool(s), "pyqs": len(s["pyqs"]) if s else 0, "practice": len(s["practice"]) if s else 0, **({"v": s["src_hash"]} if s else {})}

    core = {"nodes": nodes, "papers": papers, "stats": stats, "topics": topics_meta, "bank": {"cols": cols, "rows": bank_rows},
            "techniques": bank.TECHNIQUES,
            "rubric": {"steps": "1–2 steps = 1 point, 3–4 = 2, 5 or more = 3", "concepts": "+1 for each extra concept combined", "heavy": "+1 for big or awkward numbers",
                       "trap": "+1 if a wrong option is the result of a common mistake", "levels": "up to 2 Easy, 3–4 Medium, 5 or more Hard"},
            "likelihood": "High if the type appeared in at least 2/3 of the analysed shifts, Medium if at least 1/3, Low otherwise. Always read it with the number of shifts."}
    changed = write_if_changed(os.path.join(DATA, "core.json"), core)
    print(f"{'wrote' if changed else 'unchanged'}: core.json ({len(nodes)} nodes, {len(papers)} papers, {len(bank_rows)} questions in the bank); topics built: {', '.join(shards) or 'none'}")


if __name__ == "__main__":
    main()
