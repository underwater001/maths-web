#!/usr/bin/env python3
"""Run the random tests of every topic's shortcuts (tools/shortcuts/<topic>.py, each exposing TESTS).

    python3 tools/test_shortcuts.py            # all topics
    python3 tools/test_shortcuts.py partnership
"""
import importlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    names = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "shortcuts")) if f.endswith(".py") and not f.startswith("_"))
    for n in names:
        m = importlib.import_module("shortcuts." + n.replace("-", "_"))
        for t in m.TESTS:
            print(f"ok  {n:<12} {getattr(m, 'N', '')!s:>5} random cases  {t()}")


if __name__ == "__main__":
    main()
