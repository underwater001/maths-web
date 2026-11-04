"""TEMPLATE for a new topic. Copy to tools/topics/<topic_with_underscores>.py, fill it in, then run
python3 tools/check.py. The topic must already exist as a node in data/tree.json (kind "topic").

What each part is for is explained in README.md ("Adding material"). The build refuses a topic whose PYQ answers,
wrong-option notes or practice answers cannot be reproduced in code.
"""
from fractions import Fraction as F

from bank import bound, mistake, pyq, prac          # also: inr, share, fmt_value

TOPIC = "topic-id-from-tree-json"
PREFIX = "xx"                                         # practice ids xx-p01, xx-p02 ... (only ever append)

NODES = {   # concepts hang off the topic; question types hang off a concept. Links may point to any node.
    # "c-xx-idea": {"short": "Idea", "label": "The idea in a phrase", "kind": "concept", "parent": TOPIC, "order": 1, "summary": "One sentence.", "links": []},
    # "q-xx-type": {"short": "Type", "label": "Question type", "kind": "qtype", "parent": "c-xx-idea", "order": 1, "summary": "One sentence.", "links": []},
}
FORMULAS = [   # {"id": "xx-f1", "node": "c-xx-idea", "text": "...", "note": "..."}
]
METHODS = {    # one per question type: formulas, tech, standard, fast, ultra, eliminate, traps, (variations)
    # "q-xx-type": {"formulas": ["xx-f1"], "tech": ["multiplier"], "standard": "...", "fast": "...", "ultra": "...", "eliminate": "...", "traps": ["..."], "variations": ["..."]},
}
REFS = []      # [{"title": "...", "url": "...", "note": "what the page says, in your own words"}]

PYQS = [       # pyq(paper, qno, qtype, text, options, key, solution_lines, calc, expect, tol, tech=[], concepts=1, heavy=False, steps=None, wrong={...}, trick="")
]


def practice_items():   # prac(qtype, "same"|"harder", text, correct, [(trap_value, "mistake it comes from")] * 3, why, second_method_value, fmt="inr"|"pct"|"pctsigned"|"num")
    return []
