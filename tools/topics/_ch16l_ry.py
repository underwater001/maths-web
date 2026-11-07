"""Rakesh Yadav 7300+ Chapter 16 (Algebra) additions to linear-equations. Generated once from the book; edit by hand afterwards."""
from bank import pyq

RY = "ry7300-ch16-algebra"

PYQS_RY = [
    pyq(RY, 406, "q-le-point", "The graph of the linear equation y = x passes through the point:", ["(3/2, -3/2)", "(0, -3/2)", "(1, 1)", "(-1/2, 1/2)"], "c",
        ["Any point on y = x has equal coordinates.", "(1, 1): 1 = 1. True. None of the other three points have matching coordinates."],
        lambda: 1 * 1000 + 1, 1001, 1e-9, tech=["back-substitute"], concepts=1,
        optvals=[1.5 * 1000 - 1.5, 0 * 1000 - 1.5, 1 * 1000 + 1, -0.5 * 1000 + 0.5],
        trick="On y = x the two coordinates are simply equal — scan the options for a matching pair."),
    pyq(RY, 374, "q-le-system", "The area (in sq. units) of the triangle formed by the graphs of the equations x = 4, y = 3 and 3x + 4y = 12 is:", ["24", "6", "12", "3"], "b",
        ["x = 4 and y = 3 meet at (4, 3).", "x = 4 and 3x + 4y = 12 meet at (4, 0); y = 3 and 3x + 4y = 12 meet at (0, 3).", "The triangle (4,3), (4,0), (0,3) is right-angled, with legs 3 (along x = 4) and 4 (along y = 3): area = ½ × 3 × 4 = 6."],
        lambda: 0.5 * 3 * 4, 6, 1e-9, tech=["back-substitute", "identity"], concepts=2,
        trick="x = 4 and y = 3 are already two of the triangle's sides (vertical and horizontal), so its legs are just read off directly."),
]
