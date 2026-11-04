"""TEMPLATE for a new topic. Copy to tools/topics/<topic_with_underscores>.py, fill it in, then run
python3 tools/check.py. The topic must already exist as a node in data/tree.json (kind "topic").

What each part is for is explained in README.md ("Adding material"). The build refuses a topic whose PYQ answers,
wrong-option notes or practice answers cannot be reproduced in code.
"""
from fractions import Fraction as F

from bank import APPROX, bound, exact2, mistake, pyq, prac, variants   # also: inr, share, fmt_value

TOPIC = "topic-id-from-tree-json"
PREFIX = "xx"                                         # hand-written practice ids xx-p01, xx-p02 ... (only ever append); generated ones are xx-<template>-NN

NODES = {   # concepts hang off the topic; question types hang off a concept. Links may point to any node.
    # "c-xx-idea": {"short": "Idea", "label": "The idea in a phrase", "kind": "concept", "parent": TOPIC, "order": 1, "summary": "One sentence.", "links": []},
    # "q-xx-type": {"short": "Type", "label": "Question type", "kind": "qtype", "parent": "c-xx-idea", "order": 1, "summary": "One sentence.", "links": []},
}
FORMULAS = [   # {"id": "xx-f1", "node": "c-xx-idea", "text": "...", "note": "..."}
]
METHODS = {    # one per question type: cue (how to spot it), formulas, tech, standard, fast, ultra, eliminate, traps, (variations)
    # "q-xx-type": {"cue": "The wording that tells you this is the type.", "formulas": ["xx-f1"], "tech": ["multiplier"], "standard": "...", "fast": "...", "ultra": "...", "eliminate": "...", "traps": ["..."], "variations": ["..."]},
}
REFS = []      # [{"title": "...", "url": "...", "note": "what the page says, in your own words"}]

PYQS = [       # pyq(paper, qno, qtype, text, options, key, solution_lines, calc, expect, tol, tech=[], concepts=1, heavy=False, steps=None, wrong={...}, trick="")
]


# Practice. Every question type needs at least 3 same-level and 3 harder items, and one of them must score Hard.
# Write a few by hand and generate the rest from templates: a template is gen(rng) -> prac(...) or None (None = redraw).
# prac(qtype, "same"|"harder", text, correct, [(trap_value, "named mistake")] * 3, why, second_method_value,
#      fmt="inr"|"pct"|"pctsigned"|"num", tech=[], concepts=1, heavy=False, steps=None)
# `correct` and the traps are Fractions; the second-method value must be computed a different way (the build fails if they differ).
def _hand_items():
    return []


# def t_example(rng):
#     a, b = rng.choice([2, 3, 4]), rng.choice([5, 6, 7])
#     return prac("q-xx-type", "same", f"...{a}...{b}...", F(a * b), [(F(a + b), "Added instead of multiplied."), ...], "Why.", F(a) * F(b))


def practice_items():
    out = _hand_items()
    # out += variants(PREFIX, "example", 3, t_example)      # 3 deterministic items; unclean draws and duplicate texts are rejected
    return out
