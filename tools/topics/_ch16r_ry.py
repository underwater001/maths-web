"""Rakesh Yadav 7300+ Chapter 16 (Algebra) additions to ratio-proportion. Generated once from the book; edit by hand afterwards."""
from bank import pyq

RY = "ry7300-ch16-algebra"

PYQS_RY = [
    pyq(RY, 97, "q-rp-basic", "If a/3 = b/2, the value of (2a + 3b)/(3a − 2b) is:", ["12/5", "5/12", "1", "12/7"], "a",
        ["a/3 = b/2 means a = 3k and b = 2k for some k.", "2a + 3b = 6k + 6k = 12k, and 3a − 2b = 9k − 4k = 5k.", "The ratio is 12k/5k = 12/5."],
        lambda: (2 * 3 + 3 * 2) / (3 * 3 - 2 * 2), 12 / 5, 1e-9, tech=["plug-numbers", "ratio-parts"], concepts=1,
        trick="Set a = 3k, b = 2k (k = 1 is the quickest choice) and the ratio drops straight out."),
    pyq(RY, 121, "q-rp-basic", "If 1.5x = 0.04y, the value of (y² − x²)/(y² + 2xy + x²) is:", ["730/77", "73/77", "73/770", "74/77"], "b",
        ["1.5x = 0.04y gives y = 1.5x/0.04 = 37.5x.", "The expression is (y − x)(y + x)/(y + x)² = (y − x)/(y + x).", "(37.5x − x)/(37.5x + x) = 36.5/38.5 = 73/77."],
        lambda: (37.5 - 1) / (37.5 + 1), 73 / 77, 1e-9, tech=["ratio-parts", "cancel-first"], concepts=1,
        trick="Factor top and bottom first (difference of squares over a perfect square) — then only the ratio y : x matters, not their actual sizes."),
    pyq(RY, 114, "q-rp-prop", "If x varies inversely as (y² − 1) and x = 24 when y = 10, the value of x when y = 5 is:", ["99", "12", "24", "100"], "a",
        ["Inverse variation means x(y² − 1) stays constant.", "At y = 10: constant = 24 × (100 − 1) = 24 × 99 = 2376.", "At y = 5: x = 2376/(25 − 1) = 2376/24 = 99."],
        lambda: (24 * (100 - 1)) / (25 - 1), 99, 1e-9, tech=["scaling"], concepts=1),
]
