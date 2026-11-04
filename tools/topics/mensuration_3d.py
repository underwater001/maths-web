"""Mensuration 3D (cone, prism, sphere in a cylinder): quiz tier."""
import math
from bank import bound, mistake, pyq

TOPIC = "mensuration-3d"
PREFIX = "m3"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
r2 = math.sqrt(2)

NODES = {
    "c-m3-solids": {"short": "Solids and formulas", "label": "Cone, prism and sphere: the formulas that matter", "kind": "concept", "parent": TOPIC, "order": 1,
                    "summary": "A handful of formulas cover the exam: cone slant height, prism volume, sphere and cylinder volumes.", "links": ["mensuration-2d"]},
    "c-m3-displace": {"short": "Displacement", "label": "Immersed solid: volume in = volume of water raised", "kind": "concept", "parent": TOPIC, "order": 2,
                      "summary": "A solid dropped into a vessel raises the water by exactly its own volume.", "links": []},
    "q-m3-cone": {"short": "Cone slant height", "label": "Slant height, radius or height of a cone", "kind": "qtype", "parent": "c-m3-solids", "order": 1,
                  "summary": "Two of radius, height and slant height are known; find the third (Pythagoras).", "links": []},
    "q-m3-prism": {"short": "Prism volume", "label": "Prism or cuboid volume after a change", "kind": "qtype", "parent": "c-m3-solids", "order": 2,
                   "summary": "Base area and height give the volume; a height change scales it.", "links": ["percentage"]},
    "q-m3-displace": {"short": "Sphere in a vessel", "label": "Sphere dropped into a cylinder of water", "kind": "qtype", "parent": "c-m3-displace", "order": 1,
                      "summary": "Sphere volume equals cylinder volume of the water rise; solve for the radius.", "links": []},
}
FORMULAS = [
    {"id": "m3-f1", "node": "c-m3-solids", "text": "Cone: l² = r² + h²     V = ⅓πr²h     curved area = πrl", "note": "Triples to know: (9, 40, 41), (5, 12, 13), (8, 15, 17), (7, 24, 25)."},
    {"id": "m3-f2", "node": "c-m3-solids", "text": "Prism / cylinder: V = base area × height     Cylinder: V = πr²h", "note": "Height up 25% means volume × 1.25 with the same base."},
    {"id": "m3-f3", "node": "c-m3-solids", "text": "Sphere: V = (4/3)πr³     surface = 4πr²", "note": "r = 6 gives 4/3 × 216 = 288π."},
    {"id": "m3-f4", "node": "c-m3-displace", "text": "Sphere in cylinder: (4/3)πr³ = πR² × (rise)", "note": "π cancels from both sides."},
]
METHODS = {
    "q-m3-cone": {
        "cue": "'A right circular cone has radius … and height …. Slant height?'",
        "formulas": ["m3-f1"], "tech": ["standard-values", "estimate"],
        "standard": "l = √(9² + 40²) = √(81 + 1600) = √1681 = 41 cm.",
        "fast": "Recognise the triple 9–40–41; no squaring needed.",
        "eliminate": "The slant height is just over the height (40) because the radius is small: l is between 40 and 49. Only 41 is just above 40.",
        "traps": ["Adding radius and height (49).", "Giving the height of 40 as the slant height.", "Using the volume formula with a ⅓ instead of Pythagoras."]},
    "q-m3-prism": {
        "cue": "A base area and a height, and the height changes by a percentage.",
        "formulas": ["m3-f2"], "tech": ["fraction-percent", "multiplier"],
        "standard": "New height = 12 × 1.25 = 15 cm; V = 36 × 15 = 540 cm³.",
        "fast": "Original volume 36 × 12 = 432; 25% more is 432 + 108 = 540.",
        "eliminate": "Volume must rise by exactly 25% from 432, so it is above 432 and below 600. Strike 432 (no change).",
        "traps": ["Giving the original volume 432.", "Adding 25 cm instead of 25%.", "Using the ⅓ factor of a pyramid."]},
    "q-m3-displace": {
        "cue": "'A solid sphere is completely immersed in a cylindrical vessel…water level rises by…'.",
        "formulas": ["m3-f3", "m3-f4"], "tech": ["cancel-first", "estimate"],
        "standard": "(4/3)π × 6³ = πR² × 4, so 288 = 4R², R² = 72, R = 6√2 cm.",
        "fast": "Volume of the sphere ÷ rise = πR²: 288 ÷ 4 = 72 gives R² = 72 = 36 × 2.",
        "eliminate": "R² = 72 lies between 64 and 81, so R lies between 8 and 9. Check the options: 6√2 ≈ 8.49 fits; 4√2 ≈ 5.7 and 5√2 ≈ 7.1 are too small, and 8√2 ≈ 11.3 is too large.",
        "traps": ["Forgetting the 4/3 factor.", "Using the sphere's radius as the cylinder's radius.", "Leaving R² = 72 without taking the root."]},
}
PYQS = [
    pyq(S3, 53, "q-m3-cone", "A right circular cone has a radius of 9 cm and a height of 40 cm. What is its slant height?", ["41 cm", "42 cm", "43 cm", "45 cm"], "a",
        ["l² = 9² + 40² = 81 + 1,600 = 1,681.", "l = 41 cm (the triple 9, 40, 41)."], lambda: math.hypot(9, 40), 41, 1e-9, tech=["standard-values"],
        trick="Spot the triple 9–40–41.", wrong={"d": bound("The slant height is just above the height (40) when the radius is small, so it is well under 45.", lambda v: v >= 45)}),
    pyq(S3, 58, "q-m3-prism", "A rectangular prism has a base area of 36 cm². If its height is increased by 25% from the original height of 12 cm, what is the new volume?", ["432 cm³", "486 cm³", "504 cm³", "540 cm³"], "d",
        ["New height = 12 × 1.25 = 15 cm.", "Volume = 36 × 15 = 540 cm³."], lambda: 36 * 12 * 1.25, 540, 1e-9, tech=["fraction-percent", "multiplier"],
        trick="432 plus a quarter of 432 (108) is 540.", wrong={"a": mistake("The original volume 36 × 12, before the height rose.", 432, 1e-9)}),
    pyq(S3, 59, "q-m3-displace", "A solid metal sphere of radius 6 cm is completely immersed in a vertical cylindrical vessel containing water, causing the water level to rise by 4 cm. What is the radius of the cylinder?", ["4√2 cm", "5√2 cm", "6√2 cm", "8√2 cm"], "c",
        ["Volume of the sphere = (4/3)π × 6³ = 288π cm³.", "Water raised = πR² × 4 = 4πR².", "4R² = 288, R² = 72, R = 6√2 cm."], lambda: math.sqrt(4 / 3 * 216 / 4), 6 * r2, 1e-9,
        tech=["cancel-first"], concepts=1, optvals=[4 * r2, 5 * r2, 6 * r2, 8 * r2], trick="R² = 288 ÷ 4 = 72 = 36 × 2.",
        wrong={"a": mistake("Too small: it gives R² = 32 instead of 72.", 4 * r2, 1e-9)}),
]


def practice_items():
    return []
