#!/usr/bin/env python3
"""Verify one topic module and write its data shard.

    python3 tools/build_topic.py partnership          # build (skipped if nothing changed)
    python3 tools/build_topic.py partnership --force  # rebuild anyway
    python3 tools/build_topic.py --all                # every topic whose shard is stale or missing
    python3 tools/build_topic.py partnership --check  # verify only, write nothing

A topic lives entirely in tools/topics/<topic>.py (see tools/topics/_template.py) and builds to
data/shards/<topic>.json. Nothing else is touched, so adding a topic or growing one never forces a
rebuild of the others. The shard records a hash of its sources; tools/build.py refuses to assemble the
site from a stale shard.

Checks, in order. Any failure stops the build before anything is written.
  1. PYQs: the answer recomputed from the question's own numbers matches the keyed option and no other;
     the paper and question number exist in data/papers and have the same topic and key.
  2. Wrong-option notes: every note's check holds for the option it is attached to.
  3. Practice: the main method and a second, different method agree; four distinct options.
  4. Nodes, formulas, methods and techniques all reference things that exist.
  5. The topic's shortcut tests (tools/shortcuts/<topic>.py) pass.

Two tiers (TIER in the module). "full" (default): every type has the whole method and at least 3 same-level and 3 harder
practice questions, one Hard. "quiz": past questions with checked answers, solutions and a short method per type, so a
topic can go live the same day its questions arrive; practice and the ultra-calc layer are added when the topic is upgraded.
A full topic may list QUIZ_TYPES (question-type ids) that are held to the quiz standard until they are upgraded.
"""
import hashlib, importlib, json, os, random, sys, zlib
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

import bank

METHOD_KEYS = ["formulas", "cue", "standard", "fast", "ultra", "eliminate", "traps"]       # full tier
QUIZ_KEYS = ["formulas", "cue", "standard", "fast", "eliminate", "traps"]                    # quiz tier: ultra-calc layer comes later
MIN_SAME, MIN_HARDER = 3, 3      # every question type needs at least this many extra practice questions of each kind, one of them Hard


def jload(p):
    with open(p, encoding="utf-8") as fp:
        return json.load(fp)


def mod(topic):
    """Module file name for a topic id: profit-loss -> profit_loss."""
    return topic.replace("-", "_")


def all_topics():
    return sorted(f[:-3].replace("_", "-") for f in os.listdir(os.path.join(HERE, "topics")) if f.endswith(".py") and not f.startswith("_"))


def source_hash(topic):
    h = hashlib.sha1()
    for p in (os.path.join(HERE, "topics", mod(topic) + ".py"), os.path.join(HERE, "shortcuts", mod(topic) + ".py"),
              os.path.join(HERE, "bank.py"), os.path.abspath(__file__)):
        if os.path.exists(p):
            h.update(open(p, "rb").read())
    return h.hexdigest()[:16]


def papers_index():
    """{paper id: {qno: row}} from data/papers/*.json."""
    out = {}
    pdir = os.path.join(DATA, "papers")
    for f in sorted(os.listdir(pdir)):
        if f.endswith(".json"):
            p = jload(os.path.join(pdir, f))
            out[p["id"]] = {r["qno"]: r for r in p["rows"]}
    return out


def check_pyqs(M, errs):
    idx = papers_index()
    seen = set()
    for q in M.PYQS:
        i = q["id"]
        if i in seen: errs.append(f"{i}: duplicate PYQ id")
        seen.add(i)
        row = idx.get(q["paper"], {}).get(q["qno"])
        if row is None:
            errs.append(f"{i}: no such question in data/papers/{q['paper']}.json"); continue
        if row["topic"] != M.TOPIC: errs.append(f"{i}: the paper file puts it in topic {row['topic']!r}, not {M.TOPIC!r}")
        if row["key"] != q["key"]: errs.append(f"{i}: key {q['key']!r} differs from the paper file's {row['key']!r}")
        if len(q["options"]) != 4: errs.append(f"{i}: needs four options")
        if q["qtype"] not in M.NODES or M.NODES[q["qtype"]]["kind"] != "qtype": errs.append(f"{i}: qtype {q['qtype']} is not a question type of this topic")
        for t in q["tech"]:
            if t not in bank.TECHNIQUES: errs.append(f"{i}: unknown technique {t!r}")
        # 1. recompute and match exactly one option
        try:
            got = q["_calc"]()
        except Exception as e:  # a broken calc must fail the build, not skip the check
            errs.append(f"{i}: calc() raised {e!r}"); continue
        if abs(got - q["_expect"]) > q["_tol"] + 1e-9:
            errs.append(f"{i}: recomputed {got} but expected {q['_expect']}")
        vals = q["_optvals"] if q["_optvals"] is not None else [bank.num(o) for o in q["options"]]
        if len(vals) != 4: errs.append(f"{i}: optvals needs four values"); continue
        near = [k for k, v in enumerate(vals) if abs(v - got) <= max(q["_tol"], 1e-9) + 1e-6 * abs(got)]
        if near != ["abcd".index(q["key"])]:
            errs.append(f"{i}: options matching the recomputed answer {got} are {near}, the key is {'abcd'.index(q['key'])}")
        # 2. wrong-option notes
        for letter, w in q["wrong"].items():
            if letter == q["key"] or letter not in "abcd": errs.append(f"{i}: note on {letter!r}, which is not a wrong option"); continue
            v = vals["abcd".index(letter)]
            if not w["_ok"](v): errs.append(f"{i}: the note on option {letter} ({q['options']['abcd'.index(letter)]}) fails its check: {w['note'][:60]}")


def build_pyqs(M):
    out = []
    for q in M.PYQS:
        trap = any(w["kind"] == "mistake" for w in q["wrong"].values())
        sc = bank.score(q["steps"], q["concepts"], q["heavy"], trap)
        out.append({"id": q["id"], "paper": q["paper"], "qno": q["qno"], "qtype": q["qtype"], "text": q["text"], "options": q["options"],
                    "key": q["key"], "solution": q["solution"], "tech": q["tech"], "trick": q["trick"],
                    "wrong": {**{k: {"kind": "bound", "note": f"Does not match the worked answer, which is option ({q['key']}) {q['options']['abcd'.index(q['key'])]}."} for k in "abcd" if k != q["key"] and k not in q["wrong"]},
                              **{k: {"kind": w["kind"], "note": w["note"]} for k, w in q["wrong"].items()}},
                    "score": sc, "level": bank.level(sc), "why": {"steps": q["steps"], "concepts": q["concepts"], "heavy": q["heavy"], "trap": trap}})
    return out


def build_practice(M, pyqs, errs):
    out = []
    seen_ids = set()
    for n, p in enumerate(M.practice_items(), 1):
        iid = p.get("uid") or f"{M.PREFIX}-p{n:02d}"
        if iid in seen_ids: errs.append(f"{iid}: duplicate practice id"); continue
        seen_ids.add(iid)
        if p["qtype"] not in M.NODES or M.NODES[p["qtype"]]["kind"] != "qtype":
            errs.append(f"{iid}: qtype {p['qtype']} is not a question type of this topic"); continue
        if p["check"] is None or F(p["correct"]) != F(p["check"]):
            errs.append(f"{iid}: main method {p['correct']} vs second method {p['check']}"); continue
        for t in p["tech"]:
            if t not in bank.TECHNIQUES: errs.append(f"{iid}: unknown technique {t!r}")
        vals = [p["correct"]] + [v for v, _ in p["traps"]]
        if len(vals) != 4: errs.append(f"{iid}: needs exactly three traps"); continue
        shown = [bank.fmt_value(v, p["fmt"]) for v in vals]
        if len(set(shown)) != 4:
            errs.append(f"{iid}: options not distinct: {shown}"); continue
        order = list(range(4))
        random.Random(zlib.crc32(iid.encode())).shuffle(order)      # stable per id, so adding items never reshuffles old ones
        key = "abcd"[order.index(0)]
        wrong = {"abcd"[pos]: {"kind": "mistake", "note": p["traps"][j - 1][1]} for pos, j in enumerate(order) if j != 0}
        sc = bank.score(p["steps"], p["concepts"], p["heavy"], True)
        out.append({"id": iid, "qtype": p["qtype"], "variant": p["variant"], "score": sc, "level": bank.level(sc), "tech": p["tech"], "text": p["text"],
                    "options": [shown[j] for j in order], "key": key, "solution": p["why"], "wrong": wrong})
    for qt in ([k for k, n in M.NODES.items() if n["kind"] == "qtype" and k not in getattr(M, "QUIZ_TYPES", ())] if getattr(M, "TIER", "full") == "full" else []):
        mine = [x for x in out if x["qtype"] == qt]
        same, harder = sum(x["variant"] == "same" for x in mine), sum(x["variant"] == "harder" for x in mine)
        if same < MIN_SAME or harder < MIN_HARDER: errs.append(f"{qt}: needs at least {MIN_SAME} same-level and {MIN_HARDER} harder practice questions, has {same} and {harder}")
        if mine and not any(x["level"] == "Hard" for x in mine): errs.append(f"{qt}: needs at least one practice question that scores Hard")
    return out


def check_structure(M, tree, errs):
    if M.TOPIC not in tree or tree[M.TOPIC]["kind"] != "topic": errs.append(f"{M.TOPIC} is not a topic in data/tree.json")
    for k, n in M.NODES.items():
        if k in tree: errs.append(f"node {k} collides with a node in data/tree.json")
        if n["kind"] not in ("concept", "qtype"): errs.append(f"node {k}: kind must be concept or qtype")
        par = n["parent"]
        if par != M.TOPIC and par not in M.NODES: errs.append(f"node {k}: parent {par} is not this topic or one of its nodes")
        elif n["kind"] == "concept" and par != M.TOPIC: errs.append(f"node {k}: a concept hangs directly off its topic")
        elif n["kind"] == "qtype" and (par not in M.NODES or M.NODES[par]["kind"] != "concept"): errs.append(f"node {k}: a question type hangs off a concept")
        for l in n.get("links", []):
            if l not in M.NODES and l not in tree: errs.append(f"node {k}: link {l} does not exist")
        for f in ("short", "label", "summary"):
            if not n.get(f): errs.append(f"node {k}: missing {f}")
    fids = {f["id"] for f in M.FORMULAS}
    if len(fids) != len(M.FORMULAS): errs.append("duplicate formula ids")
    for f in M.FORMULAS:
        if f["node"] not in M.NODES: errs.append(f"formula {f['id']}: unknown node {f['node']}")
    qtypes = [k for k, n in M.NODES.items() if n["kind"] == "qtype"]
    for k in qtypes:
        m = M.METHODS.get(k)
        if not m: errs.append(f"question type {k} has no method"); continue
        for key in (METHOD_KEYS if getattr(M, "TIER", "full") == "full" and k not in getattr(M, "QUIZ_TYPES", ()) else QUIZ_KEYS):
            if not m.get(key): errs.append(f"methods {k}: missing {key}")
        for x in m.get("formulas", []):
            if x not in fids: errs.append(f"methods {k}: unknown formula {x}")
        for t in m.get("tech", []):
            if t not in bank.TECHNIQUES: errs.append(f"methods {k}: unknown technique {t!r}")
    for k in M.METHODS:
        if k not in qtypes: errs.append(f"methods {k}: not a question type of this topic")


def run_shortcuts(topic, errs):
    if not os.path.exists(os.path.join(HERE, "shortcuts", mod(topic) + ".py")): return 0
    m = importlib.import_module(f"shortcuts.{mod(topic)}")
    n = 0
    for t in m.TESTS:
        try: t(); n += 1
        except AssertionError as e: errs.append(f"shortcut test {t.__name__} failed {e}")
    return n


def build(topic, force=False, check_only=False):
    path = os.path.join(DATA, "shards", topic + ".json")
    h = source_hash(topic)
    if not force and not check_only and os.path.exists(path) and jload(path).get("src_hash") == h:
        print(f"{topic}: up to date"); return True
    M = importlib.import_module(f"topics.{mod(topic)}")
    if M.TOPIC != topic: print(f"{topic}: TOPIC in the module is {M.TOPIC!r}"); return False
    tree = jload(os.path.join(DATA, "tree.json"))
    errs = []
    check_structure(M, tree, errs)
    check_pyqs(M, errs)
    pyqs = build_pyqs(M)
    practice = build_practice(M, pyqs, errs)
    nshort = run_shortcuts(topic, errs)
    if errs:
        print(f"{topic}: BUILD FAILED"); [print(" -", e) for e in errs]; return False
    indexed = sum(1 for p in papers_index().values() for r in p.values() if r["topic"] == topic)
    shard = {"topic": topic, "tier": getattr(M, "TIER", "full"), "src_hash": h, "nodes": M.NODES, "formulas": M.FORMULAS, "methods": M.METHODS,
             "pyqs": pyqs, "practice": practice, "refs": getattr(M, "REFS", [])}
    print(f"{topic}: verified {len(pyqs)} PYQs (of {indexed} indexed), {len(practice)} practice (two methods agree), {nshort} shortcut tests")
    if len(pyqs) < indexed: print(f"  note: {indexed - len(pyqs)} indexed PYQs of this topic are not ported yet")
    if check_only: return True
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(json.dumps(shard, ensure_ascii=False, separators=(",", ":")) + "\n")
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    topics = args
    if "--all" in flags:
        topics = all_topics()
    if not topics: sys.exit(__doc__)
    ok = all([build(t, "--force" in flags, "--check" in flags) for t in topics])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
