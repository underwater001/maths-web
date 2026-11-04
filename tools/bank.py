"""Shared library for the question bank: the rubrics, vocabularies, parsing and formatting that every topic uses.

A topic lives in tools/topics/<name>.py and is built with `python3 tools/build_topic.py <name>`.
See README.md for the module interface.
"""
import random, re, zlib
from fractions import Fraction as F

# ----------------------------------------------------------------------------------------------
# Technique vocabulary: the quick-solving ideas a question can be filtered by
# ----------------------------------------------------------------------------------------------
TECHNIQUES = {
    "unit-digit": "Unit digit check",
    "divisibility": "Divisibility check",
    "bounds": "Bounds (squeeze the answer)",
    "estimate": "Rough estimate",
    "back-substitute": "Try the options",
    "cancel-first": "Cancel before multiplying",
    "multiplier": "Multiplier method",
    "fraction-percent": "Fraction and percent swap",
    "ratio-parts": "Ratio parts",
    "common-unit": "One common unit",
    "symmetry": "Symmetry and midpoint",
    "sign-check": "Profit or loss? Check the sign",
    "identity": "Use an identity",
    "plug-numbers": "Plug in a convenient number",
    "units-first": "Convert units first",
    "rationalise": "Rationalise the denominator",
    "lcm-units": "Work in LCM units",
    "relative": "Relative speed",
    "scaling": "Scale the numbers",
    "standard-values": "Standard values and triples",
}

# ----------------------------------------------------------------------------------------------
# Difficulty rubric (announced to the user, applied the same way to every question)
#   steps    = lines in the written standard solution   1-2 -> 1 point, 3-4 -> 2, 5+ -> 3
#   concepts = distinct concepts the question needs     +1 for each beyond the first
#   heavy    = big numbers or fractions that do not cancel   +1
#   trap     = at least one wrong option is the checked result of a common mistake   +1
#   score <= 2 Easy, 3-4 Medium, >= 5 Hard
# ----------------------------------------------------------------------------------------------
def step_points(n):
    return 1 if n <= 2 else 2 if n <= 4 else 3


def score(steps, concepts, heavy, trap):
    return step_points(steps) + max(concepts - 1, 0) + (1 if heavy else 0) + (1 if trap else 0)


def level(sc):
    return "Easy" if sc <= 2 else "Medium" if sc <= 4 else "Hard"


LEVELS = ["Easy", "Medium", "Hard"]


def bump(lv):
    return LEVELS[min(LEVELS.index(lv) + 1, 2)]


# ----------------------------------------------------------------------------------------------
# Likelihood: share of the analysed shifts in which a question type appeared
# ----------------------------------------------------------------------------------------------
def likelihood(shifts, total):
    if total <= 0 or shifts <= 0:
        return "not seen"
    r = shifts / total
    return "high" if r >= 2 / 3 else "medium" if r >= 1 / 3 else "low"


# ----------------------------------------------------------------------------------------------
# Option text -> number, so a recomputed answer can be matched to exactly one option
# ----------------------------------------------------------------------------------------------
def num(text):
    t = str(text).strip()
    low = t.lower()
    if re.search(r"no (profit|loss)", low):
        return 0.0
    t2 = t.replace("₹", "").replace(",", "")
    m = re.search(r"-?\d+(?:\.\d+)?(?:\s*/\s*\d+(?:\.\d+)?)?", t2)
    if not m:
        raise ValueError(f"no number in option {text!r}")
    s = m.group(0).replace(" ", "")
    v = float(F(s.split("/")[0]) / F(s.split("/")[1])) if "/" in s else float(s)
    if "loss" in low and v > 0:
        v = -v
    return v


def ratio_val(t):
    """A ratio such as '5 : 4 : 16' as one number, so equal ratios (10:8:32) match and different ones do not."""
    parts = [F(x) for x in re.findall(r"\d+(?:\.\d+)?", str(t))]
    return float(sum(p / parts[0] * F(1000) ** i for i, p in enumerate(parts)))


def mixed_val(t):
    """'15 5/6 days' -> 15.833..., '18 days' -> 18, '47/48 hours' -> 0.979."""
    m = re.search(r"(\d+)\s+(\d+)\s*/\s*(\d+)", str(t))
    return int(m[1]) + int(m[2]) / int(m[3]) if m else num(t)


# ----------------------------------------------------------------------------------------------
# Formatting of computed answers into options
# ----------------------------------------------------------------------------------------------
def inr(n):
    """Indian digit grouping: 1234567 -> 12,34,567."""
    n = int(round(float(n))); neg = n < 0; s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if neg else "") + "₹" + s


def _pct(v):
    return f"{abs(float(v)):.2f}".rstrip("0").rstrip(".") + "%"


def fmt_value(v, fmt="inr"):
    v = float(v)
    if fmt == "inr": return inr(v)
    if fmt == "pct": return _pct(v)
    if fmt == "pctsigned":
        return "No profit, no loss" if abs(v) < 1e-9 else (f"Profit of {_pct(v)}" if v > 0 else f"Loss of {_pct(v)}")
    if fmt == "inrsigned":
        return "No profit, no loss" if abs(v) < 1e-9 else (f"Profit of {inr(v)}" if v > 0 else f"Loss of {inr(-v)}")
    if fmt == "num":
        return f"{v:.2f}".rstrip("0").rstrip(".")
    raise ValueError(fmt)


# ----------------------------------------------------------------------------------------------
# Month-by-month simulation, used as the second method in partnership checks
# ----------------------------------------------------------------------------------------------
def share(cms, i, total):
    """Partner i's part of `total` when profit is shared in the ratio of capital-months `cms`."""
    return F(cms[i], sum(cms)) * total


# ----------------------------------------------------------------------------------------------
# Wrong-option notes. Every note carries a CHECK that the build runs against the option's number,
# so a note can never describe an option that it does not actually describe.
#   mistake(note, value, tol)  the option IS the result of a named common mistake (counts as a trap for difficulty)
#   bound(note, pred)          the option is ruled out by a bound / sign / estimate; pred(option_value) must be True
# ----------------------------------------------------------------------------------------------
def mistake(note, value, tol=1e-9):
    return {"kind": "mistake", "note": note, "_ok": lambda v, value=float(value), tol=tol: abs(v - value) <= tol + 1e-9}


def bound(note, pred):
    return {"kind": "bound", "note": note, "_ok": pred}


# ----------------------------------------------------------------------------------------------
# A PYQ (previous-year question), as a condensed restatement with the original numbers.
#   calc()    recomputes the answer from the question's own numbers; it must match `expect` within `tol`,
#             and the options near that value must be the keyed option and no other.
#   tech      technique tags (keys of TECHNIQUES) that make the question quick
#   concepts  how many distinct concepts the question combines   heavy  big or awkward numbers
#   steps     only if the written solution understates the real work (default: len(solution))
#   wrong     {letter: mistake(...) | bound(...)} for the non-key options
#   trick     one line: the fastest way in
#   optvals   the number each option stands for, when the option text is not a plain number (a ratio 5:9, a mixed number,
#             an ordering, a relation). Compute it from the option text in code so the check is real.
# ----------------------------------------------------------------------------------------------
def pyq(paper, qno, qtype, text, options, key, solution, calc, expect, tol=0, *, tech=(), concepts=1, heavy=False, steps=None, wrong=None, trick="", optvals=None):
    return {"id": f"{paper}-Q{qno}", "paper": paper, "qno": qno, "qtype": qtype, "text": text, "options": options, "key": key,
            "solution": solution, "tech": list(tech), "concepts": concepts, "heavy": heavy, "steps": steps or len(solution),
            "wrong": wrong or {}, "trick": trick, "_calc": calc, "_expect": expect, "_tol": tol, "_optvals": optvals}


# ----------------------------------------------------------------------------------------------
# A practice item. `correct` is found by the main method; `check` by a DIFFERENT method. `traps` are
# (value, note) pairs, the result of a named mistake, which become the other three options.
#   fmt  how values are shown (see fmt_value)   variant  "same" level as the PYQs, or "harder"
# ----------------------------------------------------------------------------------------------
def prac(qtype, variant, text, correct, traps, why, check, fmt="inr", tech=(), concepts=None, heavy=False, steps=None, uid=None):
    """Difficulty uses the same rubric as PYQs: steps default to the sentences of `why`, concepts to 1 (2 for a
    'harder' item), and the three traps always count as a trap."""
    return {"qtype": qtype, "variant": variant, "text": text, "correct": correct, "traps": traps, "why": why, "check": check,
            "fmt": fmt, "tech": list(tech), "concepts": concepts or (2 if variant == "harder" else 1), "heavy": heavy,
            "steps": steps or max(1, len(re.findall(r"\.(?:\s|$)", why))), "uid": uid}


def variants(prefix, name, n, gen):
    """n fresh, deterministic practice items from one template. gen(rng) draws parameters and returns prac(...), or None
    to reject the draw (numbers not clean). Ids are f"{prefix}-{name}-NN", so adding more of one template never moves
    another's. The second-method check inside each item is still enforced by the build."""
    out, seen = [], set()
    for i in range(n):
        base = zlib.crc32(f"{prefix}:{name}:{i}".encode())
        for attempt in range(600):
            p = gen(random.Random(base + attempt * 7919))
            if p is None or p["text"] in seen: continue
            if len({fmt_value(v, p["fmt"]) for v in [p["correct"]] + [t[0] for t in p["traps"]]}) != 4: continue
            p["uid"] = f"{prefix}-{name}-{i + 1:02d}"; seen.add(p["text"]); out.append(p); break
        else:
            raise RuntimeError(f"template {name}: no clean draw found for variant {i + 1}")
    return out


def exact2(v):
    """True if v (as a percentage or amount) is exact to two decimals, so the question needs no 'approximately'."""
    return (F(v) * 100).denominator == 1


APPROX = " Give the answer correct to two decimal places."
