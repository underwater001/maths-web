#!/usr/bin/env python3
"""Run every check in one go. This is the only command to run after adding or changing anything.

    python3 tools/check.py            # rebuild stale topics, test shortcuts, verify every paper, assemble data/core.json
    python3 tools/check.py --browser  # also run the browser test (needs Playwright and Chrome)

Stops at the first failing step. Topics whose sources have not changed are skipped, so this stays fast as the bank grows.
"""
import glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
py = sys.executable
steps = [("verify every paper's answers", [[py, p] for p in sorted(glob.glob(os.path.join(HERE, "papers", "verify_*.py")))]),
         ("topics (verify PYQs, notes, practice, shortcuts)", [[py, os.path.join(HERE, "build_topic.py"), "--all"]]),
         ("assemble the site data", [[py, os.path.join(HERE, "build.py")]])]
if "--browser" in sys.argv: steps.append(("browser test", [[py, os.path.join(HERE, "render_test.py")]]))
for name, cmds in steps:
    print(f"== {name}")
    for c in cmds:
        r = subprocess.run(c, capture_output=True, text=True)
        out = (r.stdout or "").rstrip().splitlines()
        print("\n".join(out[-4:] if len(out) > 8 and "verify_" in c[-1] else out))
        if r.returncode != 0:
            print(r.stderr[-800:]); sys.exit(f"FAILED at: {name}")
print("\nall good")
