#!/usr/bin/env python3
"""Validate the whole data set and write data/manifest.json (the list of per-topic detail files).

    python3 tools/build.py

Checks: every node's parent and links exist and links are symmetric; every formula, method, PYQ and
practice item points at a real node; every PYQ-index row names a real topic and a real paper; the
per-topic files exist. Any problem stops the build before the manifest is written.
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
load = lambda p: json.load(open(os.path.join(D, p), encoding="utf-8"))


def main():
    errs = []
    nodes, formulas, methods = load("nodes.json"), load("formulas.json"), load("methods.json")
    idx, papers = load("pyq_index.json"), load("papers.json")
    pids = {p["id"] for p in papers}
    for k, n in nodes.items():
        if n["parent"] != "hub" and n["parent"] not in nodes: errs.append(f"node {k}: parent {n['parent']} missing")
        for l in n.get("links", []):
            if l not in nodes: errs.append(f"node {k}: link {l} missing")
            elif k not in nodes[l]["links"]: errs.append(f"node {k}: link to {l} is not mirrored")
        if n["parent"] == "hub" and "hue" not in n: errs.append(f"junction {k}: no hue")
    for f in formulas:
        if f["node"] not in nodes: errs.append(f"formula {f['id']}: node {f['node']} missing")
    fids = {f["id"] for f in formulas}
    for k, m in methods.items():
        if nodes.get(k, {}).get("kind") != "qtype": errs.append(f"methods {k}: not a question-type node")
        for x in m["formulas"]:
            if x not in fids: errs.append(f"methods {k}: formula {x} missing")
    for r in idx:
        if r["topic"] not in nodes or nodes[r["topic"]]["kind"] != "topic": errs.append(f"index {r['id']}: topic {r['topic']} not a topic")
        if r["paper"] not in pids: errs.append(f"index {r['id']}: paper {r['paper']} missing")
        if "qtype" in r and r["qtype"] not in nodes: errs.append(f"index {r['id']}: qtype {r['qtype']} missing")
    manifest = {"topics": {}}
    for path in sorted(glob.glob(os.path.join(D, "pyqs", "*.json"))):
        t = os.path.basename(path)[:-5]
        prac = os.path.join(D, "practice", t + ".json")
        if t not in nodes: errs.append(f"pyqs/{t}.json: no topic node {t}")
        if not os.path.exists(prac): errs.append(f"practice/{t}.json missing")
        for q in json.load(open(path, encoding="utf-8")):
            if q["qtype"] not in nodes: errs.append(f"{q['id']}: qtype missing")
            if q["paper"] not in pids: errs.append(f"{q['id']}: paper missing")
        manifest["topics"][t] = {"pyqs": f"pyqs/{t}.json", "practice": f"practice/{t}.json"}
    if errs:
        print("BUILD FAILED"); [print(" -", e) for e in errs]; sys.exit(1)
    with open(os.path.join(D, "manifest.json"), "w", encoding="utf-8") as fp:
        fp.write(json.dumps(manifest, indent=2) + "\n")
    print(f"ok: {len(nodes)} nodes, {len(formulas)} formulas, {len(methods)} methods, {len(idx)} indexed PYQs, topics built: {', '.join(manifest['topics'])}")


if __name__ == "__main__":
    main()
