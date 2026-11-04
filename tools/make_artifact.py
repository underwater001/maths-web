#!/usr/bin/env python3
"""Write one self-contained HTML page (index.html with every data file inlined) for publishing as an Artifact.

    python3 tools/make_artifact.py OUT.html

The page reads window.__DATA__[path] before it tries to fetch, so the inlined copy behaves exactly like the site.
Only the data the page can ask for is inlined: core.json, every shard and every index file.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
title = re.search(r"<title>(.*?)</title>", src).group(1)
links = "".join(re.findall(r"<link [^>]*>", src))
styles = "".join(re.findall(r"<style[^>]*>.*?</style>", src, flags=re.S))
body = re.search(r"<body>(.*)</body>", src, flags=re.S).group(1)
data = {}
for sub in ("", "shards", "index"):
    d = os.path.join(ROOT, "data", sub)
    for f in sorted(os.listdir(d)):
        if f.endswith(".json") and (sub or f == "core.json"):
            data["data/" + (sub + "/" if sub else "") + f] = json.load(open(os.path.join(d, f), encoding="utf-8"))
inject = "<script>window.__DATA__=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";</script>\n"
marker = "<script>\n(function(){"
assert body.count(marker) == 1, "script marker not found"
body = body.replace(marker, inject + marker)
open(out, "w", encoding="utf-8").write(f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{links}\n{styles}\n{body}')
print(f"{os.path.getsize(out):,} bytes, {len(data)} data files inlined")
