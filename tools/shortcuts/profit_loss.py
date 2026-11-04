"""Random tests of the Profit, loss & discount shortcuts: each is compared with the slow, obviously correct method
on thousands of random cases, using exact fractions (no rounding)."""
import random
from fractions import Fraction as F
from math import gcd

rng = random.Random(11)
N = 4000


def lcm(a, b): return a * b // gcd(a, b)


def t_net_percent():
    """pl-f3: net % = m − d − md/100 equals the multiplier chain (1+m)(1−d) − 1."""
    for _ in range(N):
        m, d = F(rng.randint(1, 90)), F(rng.randint(1, 60))
        assert m - d - m * d / 100 == ((1 + m / 100) * (1 - d / 100) - 1) * 100
    return "net % = m − d − md/100"


def t_successive_discount():
    """pl-f4: two successive discounts = d1 + d2 − d1·d2/100; order does not matter."""
    for _ in range(N):
        a, b = F(rng.randint(1, 70)), F(rng.randint(1, 70))
        single = a + b - a * b / 100
        assert (1 - single / 100) == (1 - a / 100) * (1 - b / 100) == (1 - b / 100) * (1 - a / 100)
        assert single < a + b                      # the trap: the sum overstates it
    return "successive discount, order-free, always below the sum"


def t_false_weight():
    """pl-f6, pl-f7: profit = (true − false)/false, and with a discount the multiplier is (1−d)·true/false."""
    for _ in range(N):
        true = 1000; false = rng.randint(500, 990); d = F(rng.randint(0, 30), 100); m = F(rng.randint(0, 50), 100)
        cost_of_goods_given = F(false)                      # ₹1 per gram
        receipts = (1 + m) * (1 - d) * true                 # charged for `true` grams, marked up then discounted
        slow = (receipts - cost_of_goods_given) / cost_of_goods_given
        fast = (1 + m) * (1 - d) * F(true, false) - 1
        assert slow == fast
        if m == 0 and d == 0: assert slow == F(true - false, false)
    return "false weight: (1+m)(1−d)·true/false − 1"


def t_equal_profit_loss():
    """pl-f11: profit at SP1 = loss at SP2 ⇒ CP is the midpoint, and profit % at SP1 = (SP1 − SP2)/(SP1 + SP2)."""
    for _ in range(N):
        cp = F(rng.randint(100, 9000)); k = F(rng.randint(1, 99), 100) * cp
        sp1, sp2 = cp + k, cp - k
        assert (sp1 + sp2) / 2 == cp
        assert (sp1 - cp) / cp == (sp1 - sp2) / (sp1 + sp2)
        mid = (sp1 + sp2) / 2
        assert mid - cp == 0                                # selling at the midpoint is selling at cost
    return "CP = midpoint; profit % = (SP1 − SP2)/(SP1 + SP2)"


def t_same_sp_net_loss():
    """pl-f12: two articles sold at the same price, one at x% profit and one at x% loss ⇒ net loss x²/100 % of total cost."""
    for _ in range(N):
        x = F(rng.randint(1, 60)); sp = F(rng.randint(100, 9999))
        cp1, cp2 = sp / (1 + x / 100), sp / (1 - x / 100)
        net = (2 * sp - (cp1 + cp2)) / (cp1 + cp2) * 100
        assert net == -x * x / 100
    return "same SP, +x% and −x%: net loss x²/100 %"


def t_free_units():
    """pl-f8: buy n get f free ⇒ price per unit received = price·n/(n+f)."""
    for _ in range(N):
        n, f = rng.randint(1, 12), rng.randint(1, 6); price = F(rng.randint(5, 500))
        deals = rng.randint(1, 9)
        slow = deals * n * price / (deals * (n + f))
        assert slow == price * F(n, n + f)
    return "free units: price × n/(n+f)"


def t_rates_lcm():
    """pl-f9: 'n for ₹x' compared on the LCM of the quantities gives the same profit % as per-piece prices."""
    for _ in range(N):
        n1, n2 = rng.randint(2, 12), rng.randint(2, 12); x1, x2 = rng.randint(5, 90), rng.randint(5, 90)
        slow = (F(x2, n2) / F(x1, n1) - 1) * 100
        L = lcm(n1, n2); cost = F(x1, n1) * L; sell = F(x2, n2) * L
        assert cost.denominator == 1 and sell.denominator == 1
        assert (sell - cost) / cost * 100 == slow
    return "n for ₹x: LCM makes whole numbers, same profit %"


def t_mixed_cost():
    """pl-f10: cost of a mix = weighted average of the costs, and money in the whole mix agrees."""
    for _ in range(N):
        k = rng.choice([2, 3]); w = [rng.randint(1, 6) for _ in range(k)]; c = [F(rng.randint(5, 90)) for _ in range(k)]
        avg = sum(a * b for a, b in zip(w, c)) / sum(w)
        assert avg * sum(w) == sum(a * b for a, b in zip(w, c))
        assert min(c) <= avg <= max(c)                      # the sign-check bound used in elimination
    return "weighted mix cost, and it lies between the dearest and cheapest"


def t_flat_discount():
    """pl-f5: SP = CP(1+m)(1−d) − flat and profit p ⇒ CP = flat ÷ ((1+m)(1−d) − (1+p)); and profit % = k − 100·flat/CP."""
    for _ in range(N):
        m, d, p = (F(rng.randint(1, 80), 100), F(rng.randint(1, 40), 100), F(rng.randint(1, 30), 100))
        if (1 + m) * (1 - d) <= 1 + p: continue
        flat = F(rng.randint(10, 900))
        cp = flat / ((1 + m) * (1 - d) - (1 + p))
        assert (1 + m) * (1 - d) * cp - flat == (1 + p) * cp
        k = ((1 + m) * (1 - d) - 1) * 100
        assert k - 100 * flat / cp == p * 100            # profit % = k − 100·flat/CP: grows with CP (used to pick the largest option)
    assert (F(3, 2) * F(4, 5) - 1) * 100 - 100 * F(120, 3000) == 16      # the S3-72 case
    return "flat discount: CP = flat ÷ (chain − (1+p)), profit % = k − 100·flat/CP"


TESTS = [t_net_percent, t_successive_discount, t_false_weight, t_equal_profit_loss, t_same_sp_net_loss, t_free_units, t_rates_lcm, t_mixed_cost, t_flat_discount]
