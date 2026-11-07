"""Chapter 17 (Geometry) additions filed under polygons: regular-polygon angle algebra, cyclic
quadrilateral/trapezium angle facts, and rhombus angle/diagonal problems."""
import math
from bank import mistake, pyq

RY = "ry7300-ch17-geometry"


def _impossible_interior(a):
    """1 if `a` degrees can never be a regular polygon's interior angle (360/(180-a) is not a whole n >= 3), else 0."""
    n = 360 / (180 - a)
    return 0 if abs(n - round(n)) < 1e-9 and round(n) >= 3 else 1


PYQS_RY = [
    pyq(RY, 2, "q-pg-sides", "In a regular polygon, the exterior and interior angles are in the ratio 1 : 4. The number of sides of the polygon is",
        ["5", "10", "3", "8"], "b",
        ["Exterior + interior = 180°, and they are in the ratio 1 : 4, so exterior = 180° × 1/5 = 36°.",
         "Number of sides = 360° ÷ exterior angle = 360° ÷ 36° = 10."],
        lambda: 360 / (180 * (1 / 5)), 10, 0, tech=["ratio-parts"],
        trick="Exterior angle alone decides n = 360/exterior; interior angle is only needed to set up the ratio.",
        wrong={"a": mistake("Used interior angle's share (4/5 of 180° = 144°) as if it were the exterior angle: 360/144 is not even on the list.", 5),
               "c": mistake("Divided 360° by the ratio sum (1+4=5), not by the exterior angle itself.", 3),
               "d": mistake("Took exterior angle as 180° × 2/9 by a wrong split of the ratio.", 8)}),
    pyq(RY, 13, "q-pg-sides", "If the sum of the interior angles of a regular polygon be 1080°, the number of sides of the polygon is",
        ["6", "8", "10", "12"], "b",
        ["Sum of interior angles of an n-sided polygon = (n − 2) × 180°.", "(n − 2) × 180° = 1080° ⟹ n − 2 = 6 ⟹ n = 8."],
        lambda: 1080 / 180 + 2, 8, 0, tech=["back-substitute"],
        trick="1080 ÷ 180 = 6 exactly, so n − 2 = 6 reads off at once.",
        wrong={"a": mistake("Took n − 2 = 1080/180 − 2 = 4, an extra subtraction of 2.", 6),
               "c": mistake("Added 2 twice: 1080/180 + 2 + 2.", 10), "d": mistake("Divided by 90° instead of 180°, then halved wrongly.", 12)}),
    pyq(RY, 17, "q-pg-sides", "Measure of each interior angle of a regular polygon can never be:",
        ["150°", "105°", "108°", "144°"], "b",
        ["A regular polygon's interior angle a must give a whole number of sides n = 360/(180 − a), with n ≥ 3.",
         "150° ⟹ n = 360/30 = 12 ✓. 108° ⟹ n = 360/72 = 5 ✓. 144° ⟹ n = 360/36 = 10 ✓.",
         "105° ⟹ n = 360/75 = 4.8, not a whole number — impossible."],
        lambda: 1, 1, 0, tech=["divisibility"], optvals=[_impossible_interior(150), _impossible_interior(105), _impossible_interior(108), _impossible_interior(144)],
        trick="180 − a must divide 360 exactly. 180 − 105 = 75, and 75 does not divide 360.",
        wrong={}),
    pyq(RY, 20, "q-pg-cyclic", "ABCD is a cyclic trapezium such that AD ∥ BC. If ∠ABC = 70°, then the value of ∠BCD is:",
        ["60°", "70°", "40°", "80°"], "b",
        ["A cyclic trapezium is always isosceles (AB = DC), so its base angles at B and C — both touching BC — are equal.",
         "∠BCD = ∠ABC = 70° directly; no further computation is needed."],
        lambda: 70, 70, 0, tech=["symmetry"],
        trick="Cyclic + trapezium ⟹ isosceles trapezium, so the two base angles on BC are simply equal — read the answer straight off.",
        wrong={"a": mistake("Guessed a round number instead of using the isosceles-trapezium equal-base-angle rule.", 60),
               "c": mistake("Computed 180° − 2×70° by a wrong angle-sum attempt.", 40), "d": mistake("Added 10° for no stated reason.", 80)}),
    pyq(RY, 21, "q-pg-cyclic", "ABCD is a cyclic trapezium whose sides AD and BC are parallel to each other. If ∠ABC = 72°, then the measure of ∠BCD is",
        ["162°", "18°", "108°", "72°"], "d",
        ["Same fact as before: AD ∥ BC and ABCD cyclic ⟹ isosceles trapezium ⟹ base angles at B and C are equal.",
         "∠BCD = ∠ABC = 72°."],
        lambda: 72, 72, 0, tech=["symmetry"],
        trick="Same shortcut again — the two base angles on BC match, so ∠BCD = ∠ABC.",
        wrong={"a": mistake("180° + 90° − 108°, an unmotivated combination.", 162), "b": mistake("90° − 72°, treating the angles as complementary.", 18),
               "c": mistake("180° − 72° = 108°, treating B and C as the co-interior (supplementary) pair instead of the equal base-angle pair.", 108)}),
    pyq(RY, 22, "q-pg-cyclic", "If an exterior angle of a cyclic quadrilateral is 50°, then the interior opposite angle is:",
        ["130°", "40°", "50°", "90°"], "c",
        ["In a cyclic quadrilateral, the exterior angle at a vertex equals the interior angle at the OPPOSITE vertex",
         "(because the interior angle at the same vertex and that opposite interior angle are supplementary, and the exterior angle is also supplementary to the same-vertex interior angle).",
         "So the interior opposite angle = 50°, the same as the exterior angle."],
        lambda: 50, 50, 0, tech=["identity"],
        trick="Exterior angle of a cyclic quadrilateral = interior OPPOSITE angle — a direct equality, not a subtraction from 180°.",
        wrong={"a": mistake("180° − 50°, confusing this with the interior angle at the SAME vertex.", 130),
               "b": mistake("90° − 50°, treating the angles as complementary.", 40), "d": mistake("Unrelated guess of a right angle.", 90)}),
    pyq(RY, 25, "q-pg-rhombus", "The ratio of the angles ∠A and ∠B of a non-square rhombus ABCD is 4 : 5, then the value of ∠C is:",
        ["50°", "45°", "80°", "95°"], "c",
        ["Adjacent angles of a rhombus (a parallelogram) are supplementary: ∠A + ∠B = 180°.", "In the ratio 4 : 5, ∠A = 180° × 4/9 = 80°.",
         "Opposite angles of a rhombus are equal, so ∠C = ∠A = 80°."],
        lambda: 180 * (4 / 9), 80, 1e-9, tech=["ratio-parts", "identity"],
        trick="∠C is opposite ∠A, so it equals ∠A — only the ratio split of 180° into 4 : 5 needs computing.",
        wrong={"a": mistake("Took ∠C as the 5-part share instead of the 4-part share: 180×5/9=100, then halved by mistake.", 50),
               "b": mistake("Divided 180° by the ratio sum (9) alone.", 45), "d": mistake("Used ∠B (the 5-part angle, 100°) scaled down instead of ∠A.", 95)}),
    pyq(RY, 26, "q-pg-rhombus", "ABCD is a rhombus whose side AB = 4 cm and ∠ABC = 120°, then the length of diagonal BD is equal to:",
        ["1 cm", "2 cm", "3 cm", "4 cm"], "d",
        ["Consecutive angles of a rhombus are supplementary, so ∠A = 180° − 120° = 60°.",
         "In triangle ABD, AB = AD = 4 cm (rhombus sides) with the included angle A = 60°.",
         "By the cosine rule, BD² = 4² + 4² − 2·4·4·cos60° = 32 − 16 = 16, so BD = 4 cm."],
        lambda: math.sqrt(2 * 4 ** 2 * (1 - math.cos(math.radians(60)))), 4, 1e-9, tech=["standard-values"], heavy=True,
        trick="∠A = 60° makes triangle ABD equilateral (two sides 4 cm with a 60° included angle) — so BD = AB = 4 cm with no cosine rule needed.",
        wrong={"a": mistake("Took BD as a small fraction of AB with no real computation.", 1), "b": mistake("Guessed half of AB.", 2),
               "c": mistake("Guessed three-quarters of AB.", 3)}),
]
