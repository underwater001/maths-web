"""Data interpretation: quiz tier."""
from bank import bound, mistake, pyq, ratio_val

TOPIC = "data-interpretation"
PREFIX = "di"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"
RY = "ry7300-ch24-data-interpretation"


def _interp(x, pts):
    """Linear interpolation between the two plotted points of a cumulative-frequency (ogive) graph that
    bracket x. pts must be sorted by x and span the needed range."""
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            return y0 + (x - x0) / (x1 - x0) * (y1 - y0)
    raise ValueError(f"{x} outside the plotted range")


NODES = {
    "c-di-sets": {"short": "Two-set table", "label": "Reading a two-set table", "kind": "concept", "parent": TOPIC, "order": 1,
                  "summary": "Who knows A, who knows B, who knows both. 'Only' groups and the 'both' group must be added back before comparing.", "links": []},
    "q-di-overlap": {"short": "Only / both", "label": "Totals from 'only' and 'both' groups", "kind": "qtype", "parent": "c-di-sets", "order": 1,
                     "summary": "A table gives 'A only', 'B only', 'both' and 'neither'; find a total for one skill or a ratio of totals.", "links": []},

    "c-di-basic": {"short": "Basic reads", "label": "Reading a value off a chart", "kind": "concept", "parent": TOPIC, "order": 2,
                   "summary": "A table, bar, pie or line chart gives numbers (or angles, or percentages) for several categories; read, scale or compare them directly. The chart type never changes the method.", "links": []},
    "q-di-lookup": {"short": "Direct read", "label": "Reading one value straight off the chart", "kind": "qtype", "parent": "c-di-basic", "order": 1,
                    "summary": "The answer is one bar, one bin, or one pie sector's value — no arithmetic beyond converting units or a sector's angle/percent to a count.", "links": []},
    "q-di-pctof": {"short": "% of total", "label": "One value as a % of another", "kind": "qtype", "parent": "c-di-basic", "order": 2,
                   "summary": "Divide a part by a whole (or by another part) and multiply by 100. Watch which total the question means — the category's own group, or the grand total.", "links": []},
    "q-di-pctchange": {"short": "% change", "label": "% increase or decrease between two values", "kind": "qtype", "parent": "c-di-basic", "order": 3,
                       "summary": "(new − old) ÷ old × 100. The 'old' value is always the one you are changing FROM, whether the two values are two years, two categories, or two chart series.", "links": []},
    "q-di-ratio": {"short": "Ratio", "label": "Ratio between two chart values", "kind": "qtype", "parent": "c-di-basic", "order": 4,
                   "summary": "Form the ratio of two values, two sums, or two averages, then cancel to lowest terms.", "links": []},
    "q-di-difference": {"short": "Difference", "label": "Absolute difference between two values", "kind": "qtype", "parent": "c-di-basic", "order": 5,
                        "summary": "Subtract one chart value (or sum, or average) from another — a plain difference, not a percentage.", "links": []},
    "q-di-average": {"short": "Average", "label": "Average across categories or years", "kind": "qtype", "parent": "c-di-basic", "order": 6,
                     "summary": "Sum every listed value and divide by how many there are.", "links": []},

    "c-di-compare": {"short": "Compare & search", "label": "Comparing categories across a chart", "kind": "concept", "parent": TOPIC, "order": 3,
                     "summary": "Find the extreme, count how many meet a condition, or search for a combination that matches a target — these need every category's value, not just one.", "links": []},
    "q-di-maxmin": {"short": "Max/min (raw)", "label": "Category with the highest or lowest raw value", "kind": "qtype", "parent": "c-di-compare", "order": 1,
                    "summary": "Scan every category's own printed value and pick the extreme — watch for a 'None of these' option when the true extreme isn't one of the categories listed.", "links": []},
    "q-di-maxmin-derived": {"short": "Max/min (derived)", "label": "Category whose AVERAGE or RATIO is extreme", "kind": "qtype", "parent": "c-di-compare", "order": 2,
                            "summary": "Compute a derived number (an average, a %, a ratio) for every category FIRST, then compare those — the raw totals or single years can mislead.", "links": []},
    "q-di-threshold-count": {"short": "Count by condition", "label": "How many categories satisfy a condition", "kind": "qtype", "parent": "c-di-compare", "order": 3,
                             "summary": "Test every category against a threshold (its own average, or 'demand > production') and count the ones that pass — sometimes as a ratio of two such counts.", "links": []},
    "q-di-truefalse": {"short": "True/false claim", "label": "Which listed statement is false", "kind": "qtype", "parent": "c-di-compare", "order": 4,
                       "summary": "Check each of four derived claims about the chart against the real numbers; only one is wrong.", "links": []},
    "q-di-logicaldeduction": {"short": "Logical deduction", "label": "Deducing an answer without the absolute values", "kind": "qtype", "parent": "c-di-compare", "order": 5,
                              "summary": "A chart of % CHANGES (not absolute values) can still answer some questions by pure logic — e.g. if every rate is positive, the last period must have the highest total, with no arithmetic at all.", "links": []},
    "q-di-findmatch": {"short": "Find the match", "label": "Search for a combination that fits a target", "kind": "qtype", "parent": "c-di-compare", "order": 6,
                       "summary": "Test each of the four option-combinations against a target sum or average; only one matches.", "links": []},

    "c-di-backsolve": {"short": "Back-solving", "label": "Working from a part to the whole", "kind": "concept", "parent": TOPIC, "order": 4,
                       "summary": "A chart gives shares (%, angles) but the question gives one share's actual value — use that pairing to recover the total, then use the total for whatever the question really asks.", "links": []},
    "q-di-reversetotal": {"short": "Find the total", "label": "Back-solving the chart's own total", "kind": "qtype", "parent": "c-di-backsolve", "order": 1,
                         "summary": "One sector's % (or angle) and its actual value are both given; divide to recover the grand total the whole chart represents.", "links": []},
    "q-di-twostep": {"short": "Two-step chain", "label": "Back-solve a total, then use it for a second value", "kind": "qtype", "parent": "c-di-backsolve", "order": 2,
                     "summary": "First recover an unknown base (from a given difference, a markup, or one known part), then apply the chart's own shares to that base to get the real target.", "links": []},
    "q-di-missingpart": {"short": "Missing slice", "label": "The one slice the chart doesn't label", "kind": "qtype", "parent": "c-di-backsolve", "order": 3,
                        "summary": "The labelled slices don't add to 100%; the gap is the unlabelled slice's share. A given raw count for that slice can cross-check the answer.", "links": []},
    "q-di-project": {"short": "Project forward", "label": "Projecting one more period at the same growth rate", "kind": "qtype", "parent": "c-di-backsolve", "order": 4,
                     "summary": "Find the multiplicative growth factor between two known periods, then apply that SAME factor one period further.", "links": []},

    "c-di-special": {"short": "Special chart types", "label": "Charts that need their own reading method", "kind": "concept", "parent": TOPIC, "order": 5,
                     "summary": "A few chart types — histograms, cumulative-frequency (ogive) graphs, distance-time graphs, and 'rate only' charts — need a method beyond simple lookup/compare.", "links": []},
    "q-di-datainadequate": {"short": "Data inadequate", "label": "Recognising when the chart can't answer the question", "kind": "qtype", "parent": "c-di-special", "order": 1,
                            "summary": "A chart of ratios or % rates alone never fixes an absolute value — the honest answer is 'cannot be determined', not a guess.", "links": []},
    "q-di-binsum": {"short": "Sum of bins", "label": "Adding histogram bars inside or above a range", "kind": "qtype", "parent": "c-di-special", "order": 2,
                   "summary": "Add up every bar (class interval) that falls inside the asked range, then compare that sum to the whole if a % is wanted.", "links": []},
    "q-di-ogivemedian": {"short": "Ogive interpolation", "label": "Interpolating on a cumulative-frequency graph", "kind": "qtype", "parent": "c-di-special", "order": 3,
                        "summary": "The target x (an income level, or the n/2-th person) usually falls BETWEEN two plotted points — interpolate along the straight segment joining them.", "links": []},
    "q-di-distancetime": {"short": "Distance-time graph", "label": "Reading where two travellers meet", "kind": "qtype", "parent": "c-di-special", "order": 4,
                          "summary": "Two plotted journeys cross where they are at the same place at the same time — read that single crossing point's time and distance straight off the graph.", "links": []},
}

FORMULAS = [
    {"id": "di-f1", "node": "c-di-sets", "text": "Total for A = (A only) + (both)     Total for B = (B only) + (both)", "note": "Whoever is in 'both' is counted in each total."},
    {"id": "di-f2", "node": "c-di-sets", "text": "Total sample = A only + B only + both + neither", "note": "Use it to check the table before you start: 80 + 70 + 50 + 50 = 250."},
    {"id": "di-f3", "node": "c-di-basic", "text": "% of a part = (part ÷ whole) × 100", "note": "Check which 'whole' the question actually means — a category's own sub-total, or the chart's grand total."},
    {"id": "di-f4", "node": "c-di-basic", "text": "% change = (new − old) ÷ old × 100", "note": "'old' is the value you are changing FROM — using the wrong one as the base is the single most common DI mistake."},
    {"id": "di-f6", "node": "c-di-basic", "text": "Pie sector value = (sector's angle ÷ 360°) × total = (sector's %) × total", "note": "Angle and % always carry the same information — convert whichever one the chart gives you."},
    {"id": "di-f5", "node": "c-di-backsolve", "text": "Whole = known part's actual value ÷ known part's share (as a fraction)", "note": "This is how a chart's total is recovered when the chart shows shares but the question gives one share's real number."},
    {"id": "di-f7", "node": "c-di-compare", "text": "Average = (sum of all listed values) ÷ (how many values)", "note": "Compute it once, then compare every category to this single number."},
    {"id": "di-f8", "node": "c-di-special", "text": "Between two plotted points (x₀,y₀) and (x₁,y₁): y = y₀ + (x − x₀)/(x₁ − x₀) × (y₁ − y₀)", "note": "Linear interpolation — the standard way to read a value that falls between two points on an ogive."},
    {"id": "di-f9", "node": "c-di-special", "text": "Two travellers' paths cross at one point: that point's x is the meeting time, its y is the meeting distance", "note": "No separate 'solve for the meeting point' algebra is needed once the crossing point is read off the graph."},
    {"id": "di-f10", "node": "c-di-basic", "text": "Ratio A : B = A ÷ B, written in lowest terms", "note": "The same idea whether A and B are raw values, sums, or averages."},
    {"id": "di-f11", "node": "c-di-basic", "text": "Difference = (larger value) − (smaller value)", "note": "No percentage step — stop once you have the subtraction."},
    {"id": "di-f12", "node": "c-di-compare", "text": "To find an extreme, test a claim, or find a matching combination: compare the chart's own plotted/printed values directly", "note": "There is no computation beyond reading and comparing every relevant category."},
    {"id": "di-f13", "node": "c-di-compare", "text": "If every period's rate of change shares the same sign, the quantity is monotonic throughout: strictly increasing (all positive) or strictly decreasing (all negative)", "note": "This lets some questions be answered from the signs of a %-change chart alone, with no absolute values at all."},
    {"id": "di-f14", "node": "c-di-backsolve", "text": "Next period's total = this period's total × (this period's total ÷ previous period's total)", "note": "The same growth multiplier applied one period further — multiply by the ratio again, don't add the same absolute increase again."},
    {"id": "di-f15", "node": "c-di-special", "text": "A chart of only ratios or only % rates between two quantities never fixes either quantity's absolute value", "note": "Without at least one anchor absolute figure, no absolute value or % change can be recovered — the honest answer is 'data inadequate'."},
]

METHODS = {
    "q-di-overlap": {
        "cue": "A table with 'only', 'and' and 'neither' rows; the question asks about everyone who knows one skill.",
        "formulas": ["di-f1", "di-f2"], "tech": ["ratio-parts", "cancel-first"],
        "standard": "Add the 'both' group to each 'only' group to get each skill's total, then form the ratio and cancel.",
        "fast": "Both groups share the same 50, so Python : R = (80 + 50) : (70 + 50) = 130 : 120 = 13 : 12.",
        "eliminate": "The ratio must be above 1 (80 > 70 and the 'both' group is common). That removes 12 : 13 and 7 : 8. The ratio 8 : 7 is only the 'only' groups.",
        "traps": ["Using only the 'only' groups (80 : 70 = 8 : 7).", "Inverting the ratio (R : Python).", "Counting the 'neither' group."]},

    "q-di-lookup": {
        "cue": "The question names one category (or one bin) and asks only for ITS value — no second value, no comparison.",
        "formulas": ["di-f6"], "tech": [],
        "standard": "Find the named category on the chart. If it's a pie slice, convert its angle or % to a count (value = share × total); if it's a bar or a histogram bin, its height IS the answer.",
        "fast": "There is nothing to compute beyond unit conversion — read it straight off.",
        "eliminate": "Every wrong option is usually a DIFFERENT category's value read by mistake — check you matched the right label, not just a nearby bar.",
        "traps": ["Reading the adjacent bar or bin instead of the one actually asked for.", "Confusing a slice's angle for its percentage (forgetting to divide by 360° first)."]},

    "q-di-pctof": {
        "cue": "The question asks 'what % of X is Y' (or '... out of the total'), for values already on the chart.",
        "formulas": ["di-f3"], "tech": ["fraction-percent"],
        "standard": "Identify the part and the correct whole, divide, and multiply by 100.",
        "fast": "If the part and the whole share an obvious common factor, cancel before multiplying by 100.",
        "eliminate": "A wrong option is almost always the right fraction but against the WRONG whole (a sub-group's total instead of the grand total, or vice versa) — recheck which total the question names.",
        "traps": ["Taking the % of a sub-group's total instead of the chart's grand total (or the reverse).", "Using a different category's count in the numerator by mistake."]},

    "q-di-pctchange": {
        "cue": "Two values for the same thing — two years, two categories, two chart series — and the question asks for a % increase or decrease (or 'exceeds by what %').",
        "formulas": ["di-f4"], "tech": ["fraction-percent"],
        "standard": "Subtract to get the change, divide by the OLD/base value, multiply by 100.",
        "fast": "If the change is a clean fraction of the base (quarter, fifth, tenth), the % follows immediately without long division.",
        "eliminate": "A wrong option almost always divides by the wrong value (the new figure instead of the old one) — that number is always smaller than the correct %, since the base used was bigger.",
        "traps": ["Dividing by the new (later/larger) value instead of the old (base) value.", "Forgetting to multiply by 100."]},

    "q-di-ratio": {
        "cue": "The question asks for a ratio between two chart values, two sums, or two averages.",
        "formulas": ["di-f10"], "tech": ["ratio-parts", "cancel-first"],
        "standard": "Write the two quantities as a fraction (in the order asked) and cancel to lowest terms.",
        "fast": "Cancel common factors before looking for a match among the options — most DI ratio options are already in lowest terms.",
        "eliminate": "An inverted ratio (the two numbers swapped) is the single most common wrong option.",
        "traps": ["Giving the ratio inverted (B : A instead of A : B).", "Using a different category's value for one side of the ratio."]},

    "q-di-difference": {
        "cue": "The question asks 'by how much' or 'exceeds ... by' with a plain number or amount expected, not a percentage.",
        "formulas": ["di-f11"], "tech": ["common-unit"],
        "standard": "Subtract the smaller value from the larger.",
        "fast": "No percentage step is needed here — stop as soon as you have the subtraction.",
        "eliminate": "A wrong option is usually the difference computed against the wrong category, or the sum instead of the difference.",
        "traps": ["Adding the two values instead of subtracting.", "Comparing against a different category by mistake."]},

    "q-di-average": {
        "cue": "The question asks for the average (or mean) of a list of chart values.",
        "formulas": ["di-f7"], "tech": ["common-unit"],
        "standard": "Add every listed value, divide by the count of values.",
        "fast": "Pair values that are symmetric around a round middle number to add them mentally.",
        "eliminate": "A wrong option often divides by the wrong count (one too many or too few categories).",
        "traps": ["Dividing by the wrong number of categories.", "Leaving out one category's value from the sum."]},

    "q-di-maxmin": {
        "cue": "The question asks which single category has the highest or lowest value, among values given directly on the chart.",
        "formulas": ["di-f12"], "tech": [],
        "standard": "Scan every category's own value (no computation needed) and pick the extreme one.",
        "fast": "Eyeball the chart for the tallest/shortest bar or the biggest/smallest printed number.",
        "eliminate": "If the true extreme belongs to a category not named in the options, the answer is 'None of these' — don't force a match onto a close-but-wrong option.",
        "traps": ["Picking the category with the 2nd-highest (or 2nd-lowest) value.", "Overlooking that the true extreme isn't one of the named options, and guessing the closest one instead."]},

    "q-di-maxmin-derived": {
        "cue": "The question asks for the max/min 'on average' or 'by ratio' — the raw yearly figures alone don't decide it.",
        "formulas": ["di-f7"], "tech": [],
        "standard": "Compute the derived number (average, ratio, or % change) for every category first, THEN compare those derived numbers — never the raw figures directly.",
        "fast": "Comparing the SUMS (skipping the ÷n) gives the same ranking as comparing the averages, since every category is divided by the same n.",
        "eliminate": "A wrong option is usually the category with the highest single YEAR's value, which need not be the one with the highest AVERAGE.",
        "traps": ["Picking the category with the single highest value in one year, confusing it for the highest average.", "Comparing raw sums when the counts of years being summed differ."]},

    "q-di-threshold-count": {
        "cue": "The question asks 'in how many years/categories is X true', possibly then asking for the ratio of two such counts.",
        "formulas": ["di-f7"], "tech": [],
        "standard": "Compute the threshold (often the overall average) once, then test every category/year against it and count the passes.",
        "fast": "Once the average is found, a quick glance at which values sit clearly above or below it is enough — no need to recompute the % for each one.",
        "eliminate": "A wrong count usually comes from treating a value exactly equal to the average as 'above' (or 'below') it when it should be excluded from both.",
        "traps": ["Counting a value equal to the threshold as satisfying a strict '>' or '<' condition.", "Swapping which count goes first in the final ratio."]},

    "q-di-truefalse": {
        "cue": "Four statements are given about the same chart, and exactly one is false.",
        "formulas": ["di-f12"], "tech": [],
        "standard": "Check each statement's claim against the real totals/values one at a time; the false one will contradict the numbers.",
        "fast": "Check the statement that makes the strongest, most checkable claim (a superlative like 'highest' or 'no change') first — superlatives are the easiest to disprove.",
        "eliminate": "The three TRUE statements each check out exactly against the chart; don't stop checking after confirming just one.",
        "traps": ["Stopping at the first statement that looks plausible without actually verifying it against the numbers."]},

    "q-di-logicaldeduction": {
        "cue": "The chart gives only % CHANGES or growth RATES from period to period — never an absolute value — yet the question still has a definite logical answer.",
        "formulas": ["di-f13"], "tech": [],
        "standard": "Decide what can be deduced from the SIGN of the rates alone, without needing the actual base value: if every rate is positive, the quantity only ever grows, so the last period is the highest and no period shows a decrease.",
        "fast": "Scan just the signs of the given rates — a single negative entry is all that's needed to answer 'how many decreases', with no arithmetic at all.",
        "eliminate": "Any answer that tries to state an absolute value (a population count, a production figure) from a rate-only chart is wrong by construction — the chart simply doesn't carry that information.",
        "traps": ["Trying to compute an absolute value from % change figures alone, when the base is never given.", "Assuming the year with the highest % increase is the year with the highest absolute value."]},

    "q-di-findmatch": {
        "cue": "The question gives a target (a sum, an average, a %) and asks WHICH of four listed combinations produces it.",
        "formulas": ["di-f12"], "tech": ["back-substitute"],
        "standard": "Compute the target value once, then test each of the four option-combinations against it until one matches exactly.",
        "fast": "Estimate roughly first to discard combinations that are obviously too big or too small, then verify the 1-2 remaining candidates exactly.",
        "eliminate": "A combination that is close but not exact is still wrong — DI 'find the match' questions always have exactly one combination that lands exactly on the target.",
        "traps": ["Accepting a combination that is merely close to the target instead of checking it lands exactly on it."]},

    "q-di-reversetotal": {
        "cue": "A chart gives shares (%, or angles) of a whole, and the question gives one share's actual value — then asks for the chart's grand total.",
        "formulas": ["di-f5", "di-f6"], "tech": ["multiplier"],
        "standard": "Convert the named share to a fraction (% ÷ 100, or angle ÷ 360°), then divide the given actual value by that fraction to get the whole.",
        "fast": "If the share is a clean fraction (a quarter, a fifth), multiply up directly instead of dividing by a decimal.",
        "eliminate": "A wrong option divides by the wrong sector's share — double-check you used the share of the SAME sector whose value was given.",
        "traps": ["Dividing the given value by a different sector's share.", "Using the share as a percentage when it was printed as a raw angle, or vice versa."]},

    "q-di-twostep": {
        "cue": "The question gives one extra fact (a markup %, or a difference between two shares' values) that first has to be turned into the chart's own total, before the real target can be computed.",
        "formulas": ["di-f5", "di-f6"], "tech": ["multiplier"],
        "standard": "First solve for the hidden base value (strip off a markup, or convert a given difference into a per-unit rate), then apply the chart's own shares to that base to reach the asked-for value.",
        "fast": "Keep the base as a single unresolved number through the first step and only plug in its numeric value once, right before the final multiplication.",
        "eliminate": "A wrong option usually skips the first (back-solving) step and applies the chart's share directly to the GIVEN figure instead of the recovered base.",
        "traps": ["Applying the final share to the originally-given value instead of first recovering the true base.", "Stopping after the first step's intermediate result, without computing the actually-asked-for quantity."]},

    "q-di-missingpart": {
        "cue": "The chart's labelled %/angle slices don't add up to 100% (or 360°); the gap is an un-named slice's share.",
        "formulas": ["di-f6"], "tech": ["fraction-percent"],
        "standard": "Subtract the sum of every labelled share from 100% (or 360°) — that gap is the missing slice's own share.",
        "fast": "If the missing slice's actual count is also given, cross-check: (missing count) ÷ (100% − sum of the rest) should reproduce the chart's own total.",
        "eliminate": "Forgetting even one labelled slice when summing 'the rest' throws off the gap by exactly that slice's share — recount every labelled slice before subtracting.",
        "traps": ["Missing one of the labelled slices when adding up 'the rest', which shifts the computed gap."]},

    "q-di-project": {
        "cue": "Two consecutive periods' totals are given, and the question asks to project ONE MORE period assuming the SAME rate of growth continues.",
        "formulas": ["di-f14"], "tech": ["multiplier"],
        "standard": "Divide the later total by the earlier one to get the growth multiplier, then multiply the later total by that same multiplier again.",
        "fast": "Keep the multiplier as a fraction rather than rounding it early — rounding the growth rate before the final multiplication is the usual source of a slightly-off answer.",
        "eliminate": "A wrong option often ADDS the same absolute increase again instead of multiplying by the same ratio again — the two give different answers whenever the base is changing.",
        "traps": ["Adding the same absolute increase again instead of applying the same percentage growth again."]},

    "q-di-datainadequate": {
        "cue": "The chart gives only a RATIO (or only a % rate) between two quantities, never either quantity's actual value — and the question asks for an absolute value or a % change in one of them.",
        "formulas": ["di-f15"], "tech": [],
        "standard": "Check whether the question needs an absolute value the chart never supplies. If the base (the actual income, or the actual population) is never given anywhere, no computation can recover it — the honest answer is 'data inadequate' / 'cannot be determined'.",
        "fast": "Before calculating anything, ask: does this chart give even ONE absolute figure to anchor the ratio/rate to? If not, stop — the answer is the 'cannot be determined' option.",
        "eliminate": "Any option that states a specific number is wrong by construction when the chart supplies only ratios or rates — don't be tempted by an option that merely looks plausible.",
        "traps": ["Computing a number from the given ratios anyway, as if the missing base didn't matter.", "Assuming last year's rate can stand in for an unknown base value."]},

    "q-di-binsum": {
        "cue": "A histogram (or grouped frequency table) with several bins/classes, and the question asks for a count or % within or above/below a range spanning more than one bin.",
        "formulas": ["di-f3"], "tech": ["common-unit"],
        "standard": "Add up every bin that falls fully inside the asked range (check the range's boundaries carefully against the bin edges), then convert to a % of the grand total if asked.",
        "fast": "If the range is 'above X', it's often quicker to subtract the bins BELOW X from the grand total than to add up every bin above it.",
        "eliminate": "A wrong option usually comes from including (or excluding) one boundary bin that the range's wording doesn't actually cover.",
        "traps": ["Including one bin just outside the asked range, or leaving out one bin just inside it.", "Forgetting to convert the raw bin-sum to a % when the question asks for a percentage."]},

    "q-di-ogivemedian": {
        "cue": "A cumulative-frequency ('less than X, Y people') graph or table, and the question asks for a value (median, or a % in a range) that falls BETWEEN two of the listed cumulative points.",
        "formulas": ["di-f8"], "tech": [],
        "standard": "Find the two plotted points that bracket the target x (or target rank), then interpolate linearly along the straight line joining them.",
        "fast": "For a median of n items, the target rank is simply n/2 — no need to re-derive it from first principles each time.",
        "eliminate": "Rounding to the nearer plotted point instead of interpolating between the two bracketing points gives a close-but-wrong answer — DI ogive questions are built so the two are distinguishable.",
        "traps": ["Reading off the nearest plotted point instead of interpolating between the two points that actually bracket the target.", "Using n (not n/2) as the target rank for a median."]},

    "q-di-distancetime": {
        "cue": "A distance-time graph plots two travellers' journeys from the same start, and the question asks about when/where they meet, or about one traveller's speed or total time.",
        "formulas": ["di-f9"], "tech": ["relative"],
        "standard": "For a meeting-point question, read the (time, distance) co-ordinates of the one point where the two plotted paths cross — no algebra needed. For speed or total time, use the straight-line traveller's own start and end points: speed = distance ÷ time taken.", "fast": "The crossing point IS the answer to 'when/where do they meet' — there's nothing to solve for.",
        "eliminate": "A wrong option is often the time (or distance) read at a DIFFERENT point on one of the two paths, not at the actual crossing.",
        "traps": ["Reading a point on only one traveller's path, not the point where the two paths actually cross.", "Using the chart's full x-axis span rather than only the straight-line traveller's own start-to-finish span to find the speed."]},
}

PYQS = [
    pyq(S1, 56, "q-di-overlap", "From a sample of 250 data scientists, find the ratio of those proficient in Python to those proficient in R. (Python and R: 50; Python only: 80; R only: 70; neither: 50; total 250.)",
        ["13:12", "12:13", "8:7", "7:8"], "a",
        ["Python total = Python only + both = 80 + 50 = 130.", "R total = R only + both = 70 + 50 = 120.", "Ratio = 130 : 120 = 13 : 12."],
        lambda: ratio_val("130:120"), ratio_val("13:12"), 1e-9, tech=["ratio-parts", "cancel-first"],
        optvals=[ratio_val(t) for t in ("13:12", "12:13", "8:7", "7:8")],
        trick="Add the common 50 to each 'only' group: 130 : 120. The 'neither' row and the 250 are not needed.",
        wrong={"b": mistake("The ratio turned upside down: R to Python instead of Python to R.", ratio_val("12:13"), 1e-9),
               "c": mistake("Used only the 'only' groups, 80 : 70 = 8 : 7, and left out the 50 who know both.", ratio_val("8:7"), 1e-9),
               "d": mistake("Only-groups ratio 8 : 7 and then turned upside down.", ratio_val("7:8"), 1e-9)}),

    # ---- q-di-lookup ----
    pyq(RY, 133, "q-di-lookup", "A pie chart shows a state's annual agricultural production of 9000 tonnes, split by crop (by central angle): Wheat 110°, Sugarcane 100°, Gram 50°, Rice 60°, Maize 40°. How many tonnes of wheat were produced?",
        ["2750", "2500", "2250", "3000"], "a",
        ["Wheat's share = 110°/360° = 11/36 of the total.", "Wheat produced = 11/36 × 9000 = 2750 tonnes."],
        lambda: 110 / 360 * 9000, 2750.0, 1e-6,
        trick="110/360 of 9000 — cancel the common 10 first: 11/36 × 9000 = 2750.",
        wrong={"b": mistake("Used Sugarcane's angle (100°) instead of Wheat's (110°).", 100 / 360 * 9000, 1e-6)}),

    pyq(RY, 351, "q-di-lookup", "A histogram (class width 10) of students' marks shows: 20-30:10, 30-40:30, 40-50:20, 50-60:60, 60-70:40, 70-80:10, 80-90:30, 90-100:10 (the 0-10 and 10-20 classes have no students). How many students scored between 90 and 100?",
        ["10", "40", "30", "20"], "a",
        ["Read the 90-100 bar directly: 10 students."],
        lambda: 10, 10, 0,
        trick="Just read the named bar — no arithmetic needed.",
        wrong={"b": mistake("Read the 60-70 bar instead of 90-100.", 40, 0),
               "c": mistake("Read the 30-40 (or 80-90) bar instead of 90-100.", 30, 0),
               "d": mistake("Read the 40-50 bar instead of 90-100.", 20, 0)}),

    # ---- q-di-pctof ----
    pyq(RY, 25, "q-di-pctof", "600 students passed an exam; a pie chart splits them by subject: Mathematics 150, Bengali 240, English 90, History 120. What % passed in English?",
        ["15%", "20%", "5%", "12%"], "a",
        ["English share = 90/600.", "90/600 × 100 = 15%."],
        lambda: 90 / 600 * 100, 15.0, 1e-9,
        trick="90/600 cancels to 3/20 = 15%.",
        wrong={"b": mistake("Used History's count (120) instead of English's (90): 120/600 = 20%.", 120 / 600 * 100, 1e-9)}),

    pyq(RY, 69, "q-di-pctof", "Students per section of Class VI: A=34, B=35, C=31, D=32, E=33, F=34 (total 199). What % of the class is in section C?",
        ["17.58%", "16.08%", "16.58%", "15.58%"], "d",
        ["Section C's share = 31/199.", "31/199 × 100 ≈ 15.58%."],
        lambda: 31 / 199 * 100, 31 / 199 * 100, 0.005,
        trick="31/199 is already close to 31/200 ≈ 15.5%, so 15.58% is the only option in range.",
        optvals=[35 / 199 * 100, 32 / 199 * 100, 33 / 199 * 100, 31 / 199 * 100],
        wrong={"a": mistake("Used section B's count (35) instead of C's (31).", 35 / 199 * 100, 0.005),
               "b": mistake("Used section D's count (32) instead of C's (31).", 32 / 199 * 100, 0.005),
               "c": mistake("Used section E's count (33) instead of C's (31).", 33 / 199 * 100, 0.005)}),

    pyq(RY, 230, "q-di-pctof", "800 employees are split by department (%): Accounts 16, Production 35, HR 5, IT 20, Marketing 24. Male employees by department: Production 245, HR 12, IT 74, Marketing 165, Accounts 93. What % of the TOTAL 800 employees (not just IT's own staff) are female employees working in IT?",
        ["10.25%", "10.75%", "15.25%", "15.75%"], "b",
        ["IT department's total staff = 20% × 800 = 160.", "Females in IT = 160 − 74 = 86.", "As a % of the GRAND total: 86/800 × 100 = 10.75%."],
        lambda: (0.20 * 800 - 74) / 800 * 100, 10.75, 1e-9,
        trick="Find IT's own headcount (160) first, subtract the 74 males, then divide by 800 — not by 160.",
        wrong={"d": mistake("Used 25% as IT's share of the workforce instead of its actual 20%.", (0.25 * 800 - 74) / 800 * 100, 1e-9)}),

    # ---- q-di-pctchange ----
    pyq(RY, 8, "q-di-pctchange", "Wheat production was 680 million tonnes in 1991 and 860 million tonnes in 1992. What was the % increase?",
        ["26.47%", "20.92%", "23.67%", "18.74%"], "a",
        ["Increase = 860 − 680 = 180.", "% increase = 180/680 × 100 ≈ 26.47%."],
        lambda: (860 - 680) / 680 * 100, (860 - 680) / 680 * 100, 0.01,
        trick="180/680 — both divisible by 20, giving 9/34 ≈ 26.47%.",
        wrong={"b": mistake("Used 1992 (the later, larger year) as the base instead of 1991: 180/860.", (860 - 680) / 860 * 100, 0.02)}),

    pyq(RY, 450, "q-di-pctchange", "Average petrol price was ₹36.49 in 2004 and ₹73.70 in 2014. Approximately what % higher was the 2014 price?",
        ["98%", "100%", "102%", "105%"], "c",
        ["Increase = 73.70 − 36.49 = 37.21.", "% increase = 37.21/36.49 × 100 ≈ 102%."],
        lambda: (73.70 - 36.49) / 36.49 * 100, (73.70 - 36.49) / 36.49 * 100, 1.0,
        trick="37.21 is a little more than 36.49 itself, so the increase is a little over 100%."),

    pyq(RY, 116, "q-di-pctchange", "2160 students travel to school: Walk 480, Bus 540, Car 420, Train 720 (from a pie chart: Walk 80°, Bus 90°, Car 70°, Train 120°). By what % does the number taking the Bus exceed the number who Walk?",
        ["10%", "12.5%", "15%", "20%"], "b",
        ["Difference = 540 − 480 = 60.", "% excess (over Walk's own 480) = 60/480 × 100 = 12.5%."],
        lambda: (540 - 480) / 480 * 100, 12.5, 1e-9,
        trick="60 is exactly 1/8 of 480, and 1/8 = 12.5%."),

    # ---- q-di-ratio ----
    pyq(RY, 118, "q-di-ratio", "A college's pie chart (by central angle) shows students by faculty: Education 30°, Law 45°, Arts 120°, Commerce 65°, Science 100°. Find the ratio of Science students to Arts students.",
        ["6:5", "5:4", "4:5", "5:6"], "d",
        ["Ratio = Science's angle : Arts's angle = 100° : 120°.", "100 : 120 = 5 : 6."],
        lambda: ratio_val("100:120"), ratio_val("5:6"), 1e-9,
        optvals=[ratio_val(t) for t in ("6:5", "5:4", "4:5", "5:6")],
        trick="Angles compare the same way the underlying counts do — no need to convert to students first.",
        wrong={"a": mistake("Gave Arts : Science (120:100 = 6:5), the ratio inverted.", ratio_val("6:5"), 1e-9)}),

    pyq(RY, 67, "q-di-ratio", "Sections A and C of Class VI have 34 and 31 students respectively (out of six sections A-F). Find the ratio A : C.",
        ["34:35", "32:35", "31:35", "34:31"], "d",
        ["Ratio A : C = 34 : 31 directly — it's already in lowest terms (34 and 31 share no common factor)."],
        lambda: ratio_val("34:31"), ratio_val("34:31"), 1e-9,
        optvals=[ratio_val(t) for t in ("34:35", "32:35", "31:35", "34:31")],
        trick="34 and 31 are coprime, so the ratio is already fully reduced.",
        wrong={"a": mistake("Used section B's count (35) instead of C's (31).", ratio_val("34:35"), 1e-9)}),

    pyq(RY, 257, "q-di-ratio", "A company's income and expenditure (₹crore), 2005-2009: Income 35,50,45,60,60; Expenditure 25,40,40,50,55. Find the ratio of TOTAL income to TOTAL expenditure over the 5 years.",
        ["21:25", "25:21", "26:21", "25:22"], "b",
        ["Total income = 35+50+45+60+60 = 250.", "Total expenditure = 25+40+40+50+55 = 210.", "Ratio = 250 : 210 = 25 : 21."],
        lambda: ratio_val(f"{35+50+45+60+60}:{25+40+40+50+55}"), ratio_val("25:21"), 1e-9,
        optvals=[ratio_val(t) for t in ("21:25", "25:21", "26:21", "25:22")],
        trick="Add each column's own total first, then form the ratio once — not year by year.",
        wrong={"a": mistake("Gave the ratio inverted (expenditure : income).", ratio_val("21:25"), 1e-9)}),

    # ---- q-di-difference ----
    pyq(RY, 16, "q-di-difference", "500 students failed an exam, split by subject: Science 160, Mathematics 150, Language 180, Other 10. By how many does the Mathematics-fail count fall short of the Language-fail count?",
        ["20", "40", "30", "50"], "c",
        ["Difference = 180 − 150 = 30."],
        lambda: 180 - 150, 30, 0),

    pyq(RY, 65, "q-di-difference", "Company XYZ's sales (₹crore): Year 4 = 1841, Year 8 = 5345 (among 11 years charted). By how much did Year 8's sales exceed Year 4's?",
        ["3608cr", "3504cr", "3127cr", "3427cr"], "b",
        ["Difference = 5345 − 1841 = 3504."],
        lambda: 5345 - 1841, 3504, 0),

    # ---- q-di-average ----
    pyq(RY, 347, "q-di-average", "2nd-term marks (out of 100) in 5 subjects: English 80, Maths 80, Physics 75, Chemistry 65, Biology 60. Find the average.",
        ["65", "73", "62", "72"], "d",
        ["Sum = 80+80+75+65+60 = 360.", "Average = 360/5 = 72."],
        lambda: sum([80, 80, 75, 65, 60]) / 5, 72.0, 1e-9),

    pyq(RY, 177, "q-di-average", "Monthly income (₹thousand) of 5 persons: 5, 7.25, 5.5, 8.75, 4.25. Find the average monthly income, in rupees.",
        ["₹5775", "₹6000", "₹6150", "₹6250"], "c",
        ["Sum = 5+7.25+5.5+8.75+4.25 = 30.75 thousand.", "Average = 30.75/5 = 6.15 thousand = ₹6150."],
        lambda: sum([5, 7.25, 5.5, 8.75, 4.25]) / 5 * 1000, 6150.0, 1e-6),

    # ---- q-di-maxmin ----
    pyq(RY, 248, "q-di-maxmin", "Sales (lakh bottles) of a soft drink 'Cool-up' by year: 1988=25, 1989=6, 1990=19, 1991=15, 1992=25, 1993=30. In which of these years was Cool-up's sale MINIMUM?",
        ["1990", "1992", "1993", "None of these"], "d",
        ["Scan all six years: the true minimum is 1989 (6 lakh bottles).", "1989 isn't one of the three named years, so the answer is 'None of these'."],
        lambda: min({1988: 25, 1989: 6, 1990: 19, 1991: 15, 1992: 25, 1993: 30},
                    key=lambda y: {1988: 25, 1989: 6, 1990: 19, 1991: 15, 1992: 25, 1993: 30}[y]),
        1989, 0, optvals=[1990, 1992, 1993, 1989],
        trick="Check EVERY year before picking from the three named options — the real minimum (1989) is a trap left out of the list.",
        wrong={"a": mistake("Picked 1990, the smallest value among only the three named options, without checking 1989 and 1991 too.", 1990, 0)}),

    pyq(RY, 75, "q-di-maxmin", "Wheat production (quintals) by year: 1995=1200, 1996=600, 1997=500, 1998=1000, 1999=1500, 2000=1300, 2001=600. In which year was production MAXIMUM?",
        ["1995", "1997", "1999", "2000"], "c",
        ["Scan all seven years: 1999's 1500 is the highest."],
        lambda: max({1995: 1200, 1996: 600, 1997: 500, 1998: 1000, 1999: 1500, 2000: 1300, 2001: 600},
                    key=lambda y: {1995: 1200, 1996: 600, 1997: 500, 1998: 1000, 1999: 1500, 2000: 1300, 2001: 600}[y]),
        1999, 0, optvals=[1995, 1997, 1999, 2000],
        wrong={"d": mistake("Picked 2000 (the 2nd-highest, 1300), overlooking that 1999 (1500) is higher still.", 2000, 0)}),

    # ---- q-di-maxmin-derived ----
    pyq(RY, 249, "q-di-maxmin-derived", "Sales (lakh bottles), 1988-1993: Cool-up 25,6,19,15,25,30; Pep-up 30,35,30,25,20,20; Dew-drop 10,15,15,15,30,25. For which drink was the AVERAGE annual sale maximum?",
        ["Pep-up only", "Pep-up and Dew-drop", "Cool-up only", "Cool-up and Pep-up"], "a",
        ["Totals over the 6 years: Cool-up=120, Pep-up=150, Dew-drop=110.", "Pep-up's total (and so its average) is the highest, and uniquely so."],
        lambda: 1 if sum([30, 35, 30, 25, 20, 20]) > max(sum([25, 6, 19, 15, 25, 30]), sum([10, 15, 15, 15, 30, 25])) else 2,
        1, 0, optvals=[1, 2, 3, 4],
        trick="Compare the three TOTALS directly (120, 150, 110) — dividing all three by the same 6 years doesn't change which is biggest."),

    pyq(RY, 300, "q-di-maxmin-derived", "Runs scored (1st innings / 2nd innings): Dhoni 60/80, Kohli 50/50, Pujara 70/10, Dhawan 30/20. Find the average of the player who has the HIGHEST average (across the two innings).",
        ["85", "70", "75", "80"], "b",
        ["Averages: Dhoni=(60+80)/2=70, Kohli=(50+50)/2=50, Pujara=(70+10)/2=40, Dhawan=(30+20)/2=25.", "Dhoni's average (70) is the highest, so the answer is 70."],
        lambda: max((60 + 80) / 2, (50 + 50) / 2, (70 + 10) / 2, (30 + 20) / 2), 70.0, 1e-9,
        trick="Pujara's single-innings 70 looks big, but his AVERAGE (40) is well below Dhoni's (70) — always average both innings before comparing."),

    # ---- q-di-threshold-count ----
    pyq(RY, 153, "q-di-threshold-count", "Potato production (quintals), 2000-2006: 1244,1085,720,1640,1240,1345,1560. In how many of these 7 years was production ABOVE the 7-year average?",
        ["1", "2", "3", "4"], "c",
        ["Average = (1244+1085+720+1640+1240+1345+1560)/7 = 8834/7 ≈ 1262.", "Years above 1262: 1640, 1345, 1560 — three years."],
        lambda: sum(1 for v in [1244, 1085, 720, 1640, 1240, 1345, 1560] if v > sum([1244, 1085, 720, 1640, 1240, 1345, 1560]) / 7),
        3, 0),

    pyq(RY, 381, "q-di-threshold-count", "Demand & Production (units) of 5 companies: Demand — A 3000, B 600, C 2500, D 1200, E 3300; Production — A 1500, B 1800, C 1000, D 2700, E 2200. Find the ratio of (companies where demand exceeds production) to (companies where production exceeds demand).",
        ["2:2", "3:2", "2:3", "4:1"], "b",
        ["Demand > Production: A (3000>1500), C (2500>1000), E (3300>2200) — 3 companies.", "Production > Demand: B (1800>600), D (2700>1200) — 2 companies.", "Ratio = 3 : 2."],
        lambda: ratio_val(f"{sum(1 for x, y in zip([3000, 600, 2500, 1200, 3300], [1500, 1800, 1000, 2700, 2200]) if x > y)}:"
                           f"{sum(1 for x, y in zip([3000, 600, 2500, 1200, 3300], [1500, 1800, 1000, 2700, 2200]) if y > x)}"),
        ratio_val("3:2"), 1e-9, optvals=[ratio_val(t) for t in ("2:2", "3:2", "2:3", "4:1")],
        trick="Just classify each of the 5 companies as D>P or P>D and count — no need to compute by how much."),

    pyq(RY, 263, "q-di-threshold-count", "Demand & Production (units) of colour TVs, companies A-E: Demand — A 3300, B 1200, C 3000, D 600, E 2500; Production — A 2200, B 2700, C 1500, D 1800, E 1000. Find the ratio of (companies with demand MORE than production) to (companies with production MORE than demand).",
        ["2:3", "4:1", "1:1", "3:2"], "d",
        ["Demand > Production: A (3300>2200), C (3000>1500), E (2500>1000) — 3 companies.", "Production > Demand: B (2700>1200), D (1800>600) — 2 companies.", "Ratio = 3 : 2."],
        lambda: ratio_val(f"{sum(1 for x, y in zip([3300, 1200, 3000, 600, 2500], [2200, 2700, 1500, 1800, 1000]) if x > y)}:"
                           f"{sum(1 for x, y in zip([3300, 1200, 3000, 600, 2500], [2200, 2700, 1500, 1800, 1000]) if y > x)}"),
        ratio_val("3:2"), 1e-9, optvals=[ratio_val(t) for t in ("2:3", "4:1", "1:1", "3:2")]),

    # ---- q-di-truefalse ----
    pyq(RY, 268, "q-di-truefalse", "Cotton production ('000 bales) by state, 1992-93/1993-94/1994-95: A 6/14/21, B 12/18/18, C 5/9/15, D 16/9/12, E 8/14/7. Which ONE of these statements about the 3-year totals is FALSE? (a) A and E produced the same amount in 1993-94 (14 each) (b) State B shows no change from 1993-94 to 1994-95 (18 both years) (c) State A's 3-year total is the highest of all five states (d) C+D's 1993-94 production (9+9=18) equals B's 1993-94 production (18)",
        ["Statement (a)", "Statement (b)", "Statement (c)", "Statement (d)"], "c",
        ["3-year totals: A=6+14+21=41, B=12+18+18=48, C=5+9+15=29, D=16+9+12=37, E=8+14+7=29.", "B's total (48) is actually the highest, not A's (41) — so statement (c) is the false one; (a), (b), (d) all check out exactly."],
        lambda: 3 if sum([6, 14, 21]) != max(sum([6, 14, 21]), sum([12, 18, 18]), sum([5, 9, 15]), sum([16, 9, 12]), sum([8, 14, 7])) else 0,
        3, 0, optvals=[1, 2, 3, 4],
        trick="A superlative claim ('the highest') is the quickest one to disprove — total every state once and compare."),

    # ---- q-di-logicaldeduction ----
    pyq(RY, 456, "q-di-logicaldeduction", "A chart gives only the YEARLY % INCREASE in a town's population (never the population itself): 2004=4%, 2005=6%, 2006=3%, 2007=4%, 2008=8%, 2009=3%, 2010=5%, 2011=6% — every single year is an increase. Which of these 8 years had the town's HIGHEST population?",
        ["2008", "2005", "2010", "2011"], "d",
        ["Every year's rate is positive, so the population only ever grows, year after year.", "With no decrease anywhere, the LAST year charted (2011) must be the highest — regardless of how big or small each individual rate was."],
        lambda: 2011 if all(r > 0 for r in [4, 6, 3, 4, 8, 3, 5, 6]) else None,
        2011, 0, optvals=[2008, 2005, 2010, 2011],
        trick="Don't chase the year with the biggest % increase (2008, at 8%) — a monotonically growing series is always highest at its LAST point."),

    pyq(RY, 459, "q-di-logicaldeduction", "Using the same yearly-%-increase chart (2004=4%, 2005=6%, 2006=3%, 2007=4%, 2008=8%, 2009=3%, 2010=5%, 2011=6%), how many of these 8 years show a DECREASE in population?",
        ["1", "2", "3", "0"], "d",
        ["Every one of the 8 listed rates is positive (an increase).", "A decrease would show up as a negative rate — there isn't one, so the count is 0."],
        lambda: sum(1 for r in [4, 6, 3, 4, 8, 3, 5, 6] if r < 0), 0, 0),

    # ---- q-di-findmatch ----
    pyq(RY, 402, "q-di-findmatch", "Fertilizer production ('0000 tonnes): 1995=25, 1996=40, 1997=60, 1998=45, 1999=65, 2000=50, 2001=75, 2002=80. The average of 1996 & 1997's production exactly equals the average production of which OTHER pair of years?",
        ["2000 & 2001", "1995 & 1999", "1995 & 2001", "1999 & 2000"], "c",
        ["Target average = (40+60)/2 = 50.", "Check each option pair: (25+75)/2 = 50 — that's 1995 & 2001.", "(No other listed pair also averages to 50.)"],
        lambda: (lambda d: next(i for i, (y1, y2) in enumerate([(2000, 2001), (1995, 1999), (1995, 2001), (1999, 2000)])
                                if abs((d[y1] + d[y2]) / 2 - (d[1996] + d[1997]) / 2) < 1e-9))(
            {1995: 25, 1996: 40, 1997: 60, 1998: 45, 1999: 65, 2000: 50, 2001: 75, 2002: 80}),
        2, 0, optvals=[0, 1, 2, 3],
        trick="Compute the target average (50) once, then just test each candidate pair against it."),

    pyq(RY, 29, "q-di-findmatch", "A pie chart shows India's foodgrain-export share (%) by crop: A 20, B 20, C 10, D 5, E 5, F 12.5, Others 27.5. Which THREE crops together make up exactly 50% of the exports?",
        ["A, F, Others", "B, C, F", "A, B, C", "E, F, Others"], "c",
        ["A+B+C = 20+20+10 = 50% — an exact match.", "(The other three combinations add to 60%, 42.5%, and 45% respectively — none of them hit 50%.)"],
        lambda: (lambda pct: next(i for i, combo in enumerate([("A", "F", "Others"), ("B", "C", "F"), ("A", "B", "C"), ("E", "F", "Others")])
                                  if abs(sum(pct[x] for x in combo) - 50) < 1e-9))(
            {"A": 20, "B": 20, "C": 10, "D": 5, "E": 5, "F": 12.5, "Others": 27.5}),
        2, 0, optvals=[0, 1, 2, 3]),

    # ---- q-di-reversetotal ----
    pyq(RY, 38, "q-di-reversetotal", "A publisher's cost breakdown (%): Paper 20, Printing 25, Binding 30, Misc 10, Royalty 15. If Printing+Binding together cost ₹110 for one book, what is the TOTAL production cost per book?",
        ["₹250", "₹200", "₹110", "₹550"], "b",
        ["Printing+Binding's combined share = 25%+30% = 55%.", "Total = 110 ÷ 0.55 = ₹200."],
        lambda: 110 / (0.25 + 0.30), 200.0, 1e-6,
        trick="55% of the total is ₹110, so the whole total is 110 × (100/55) = ₹200."),

    pyq(RY, 406, "q-di-reversetotal", "A pie chart shows Central Govt revenue sources (%): A 14, Other 14, Income Tax 26, Corporation Tax 9, Excise Duty 41. If revenue from Excise Duty is ₹28,618 crore, what is the TOTAL revenue?",
        ["58900", "47200", "69800", "45600"], "c",
        ["Excise Duty's share = 41% of the total.", "Total = 28618 ÷ 0.41 = ₹69,800 crore."],
        lambda: 28618 / 0.41, 69800.0, 1e-3),

    pyq(RY, 119, "q-di-reversetotal", "A college's faculty-wise pie chart (by central angle): Education 30°, Law 45°, Arts 120°, Commerce 65°, Science 100°. If 1000 students are enrolled in Science, what is the TOTAL number of students in the college?",
        ["3000", "3200", "3600", "3800"], "c",
        ["Science's share = 100°/360°.", "Total = 1000 ÷ (100/360) = 1000 × 360/100 = 3600."],
        lambda: 1000 * 360 / 100, 3600.0, 1e-6,
        trick="This is the same 'part ÷ its share = whole' idea as a %-based reverse-total — just convert the angle to a fraction of 360° first."),

    # ---- q-di-twostep ----
    pyq(RY, 134, "q-di-twostep", "A publisher's expenditure breakdown (%): Royalty 15, Printing 20, Transport 10, Promotion 10, Paper Cost 15, Binding 30. A book's marked price is 20% above its cost price. If the marked price is ₹180, what is the Paper Cost per copy?",
        ["₹18", "₹20", "₹22.50", "₹25"], "c",
        ["Cost price = 180 ÷ 1.20 = ₹150 (strip off the 20% markup first).", "Paper Cost = 15% of ₹150 = ₹22.50."],
        lambda: (180 / 1.2) * 0.15, 22.5, 1e-9,
        trick="Always recover the COST price from the marked price first — applying the chart's % directly to the marked price (₹180) would be wrong."),

    pyq(RY, 302, "q-di-twostep", "A family's monthly-expenditure pie chart (by central angle): Education 70°, Food 120°, Other 36°, Savings 60°, Housing 54°, Clothing 20°. If Education expenditure exceeds Housing expenditure by ₹1,600, find the expenditure on Food.",
        ["₹6000", "₹3333", "₹7000", "₹12000"], "d",
        ["Education − Housing = 70°−54° = 16°, which equals ₹1,600 → 1° = ₹100.", "Food = 120° = 120 × ₹100 = ₹12,000."],
        lambda: (1600 / (70 - 54)) * 120, 12000.0, 1e-6,
        trick="Turn the GIVEN difference (16° worth ₹1,600) into a per-degree rate first, then scale Food's own 120° by that rate."),

    # ---- q-di-datainadequate ----
    pyq(RY, 147, "q-di-datainadequate", "A line graph gives only the RATIO of a company's Income to Expenditure each year (never the actual income or expenditure): 2000=0.50, 2001=1.0, 2002=0.70, 2003=2.60, 2004=1.75, 2005=1.50. What was the % decrease in Income from 2001 to 2002?",
        ["50%", "33%", "25%", "Data inadequate"], "d",
        ["The chart gives only the ratio Income÷Expenditure for each year — never the actual Income figure.", "Expenditure itself could be anything and could differ between the two years, so the actual Income values (and hence their % change) can't be recovered.", "The honest answer is: data inadequate."],
        lambda: -999.0, -999.0, 0, optvals=[50.0, 33.0, 25.0, -999.0],
        trick="Before calculating, check whether even ONE absolute rupee figure is given anywhere on this chart — here, none is."),

    pyq(RY, 457, "q-di-datainadequate", "A bar chart gives only the YEARLY % INCREASE in a town's population (never the population itself): 2004=4%, 2005=6%, 2006=3%, 2007=4%, 2008=8%, 2009=3%, 2010=5%, 2011=6%. What was the population of the town in 2009?",
        ["3", "5", "4", "Can't be determined"], "d",
        ["The chart never states the population in any year — only year-to-year % increases.", "Without one anchor year's actual population, no year's absolute population can be recovered.", "The answer is: can't be determined."],
        lambda: -999.0, -999.0, 0, optvals=[3.0, 5.0, 4.0, -999.0]),

    # ---- q-di-binsum ----
    pyq(RY, 196, "q-di-binsum", "A histogram of 50 students' marks: 20-30:1, 30-40:4, 40-50:2, 50-60:8, 60-70:10, 70-80:12, 80-90:5, 90-100:8. What % of students scored ABOVE 60 marks?",
        ["60%", "80%", "70%", "75%"], "c",
        ["Bins above 60: 60-70(10)+70-80(12)+80-90(5)+90-100(8) = 35.", "% = 35/50 × 100 = 70%."],
        lambda: sum([10, 12, 5, 8]) / 50 * 100, 70.0, 1e-9),

    pyq(RY, 291, "q-di-binsum", "A histogram of 35 hospital patients' ages: 30-35:1, 35-40:4, 40-45:8, 45-50:7, 50-55:5, 55-60:4, 60-65:3, 65-70:2, 70-75:1. How many patients are OLDER than 40 but YOUNGER than 55?",
        ["20", "30", "15", "12"], "a",
        ["Bins strictly between 40 and 55: 40-45(8)+45-50(7)+50-55(5) = 20."],
        lambda: sum([8, 7, 5]), 20, 0),

    pyq(RY, 353, "q-di-binsum", "A histogram of 210 students' marks: 20-30:10, 30-40:30, 40-50:20, 50-60:60, 60-70:40, 70-80:10, 80-90:30, 90-100:10. What % of students scored LESS than 50 marks?",
        ["28 4/7%", "27 5/7%", "23 13/21%", "47 13/21%"], "a",
        ["Bins below 50: 20-30(10)+30-40(30)+40-50(20) = 60.", "% = 60/210 × 100 = 200/7 = 28 4/7%."],
        lambda: sum([10, 30, 20]) / 210 * 100, 200 / 7, 1e-6,
        optvals=[200 / 7, 27 + 5 / 7, 23 + 13 / 21, 47 + 13 / 21]),

    # ---- q-di-ogivemedian ----
    pyq(RY, 145, "q-di-ogivemedian", "A cumulative-frequency graph of 50 factory workers' daily income: by ₹120 — 12 workers; by ₹140 — 26; by ₹160 — 34; by ₹180 — 40; by ₹200 — 50 (all of them). Interpolating linearly between the plotted points, what % of workers earn BETWEEN ₹150 and ₹180?",
        ["6%", "16%", "12%", "20%"], "d",
        ["At ₹150 (between the ₹140 and ₹160 points): 26 + (150−140)/(160−140) × (34−26) = 26+4 = 30 workers.", "At ₹180: exactly 40 workers (a plotted point).", "Workers between ₹150 and ₹180 = 40−30 = 10.", "% = 10/50 × 100 = 20%."],
        lambda: (_interp(180, [(120, 12), (140, 26), (160, 34), (180, 40), (200, 50)])
                 - _interp(150, [(120, 12), (140, 26), (160, 34), (180, 40), (200, 50)])) / 50 * 100,
        20.0, 1e-6),

    pyq(RY, 146, "q-di-ogivemedian", "Using the same cumulative-frequency graph (by ₹120 — 12 workers; by ₹140 — 26; by ₹160 — 34; by ₹180 — 40; by ₹200 — 50), find the MEDIAN daily income of the 50 workers.",
        ["₹140", "₹138", "₹150", "₹160"], "b",
        ["The median is the income of the 25th worker (50/2).", "25 falls between the ₹120 point (12 workers) and the ₹140 point (26 workers).", "Interpolating: 120 + (25−12)/(26−12) × (140−120) ≈ ₹138.6, i.e. ₹138."],
        lambda: 120 + (25 - 12) / (26 - 12) * (140 - 120), 138.5714, 1.0,
        trick="The target rank for a median of 50 workers is simply 25 — then interpolate exactly as for any other in-between value."),

    # ---- q-di-distancetime ----
    pyq(RY, 57, "q-di-distancetime", "A motorist and a scooterist both start a 120 km journey at 9:00 am from the same point. The scooterist travels at one constant speed the whole way; the motorist's speed varies. A distance-time graph shows the scooterist's (straight-line) path crossing the motorist's (plotted) path at exactly (10:30 am, 80 km). At what time do the two meet en route?",
        ["10:30am", "10:45am", "10:15am", "10:20am"], "a",
        ["The two travellers are at the same place at the same time only where their two plotted paths cross.", "That crossing point is given as (10:30 am, 80 km), so they meet at 10:30 am."],
        lambda: 1030, 1030, 0, optvals=[1030, 1045, 1015, 1020]),

    pyq(RY, 58, "q-di-distancetime", "Same journey as above: the scooterist covers the full 120 km, starting 9:00 am and finishing 11:30 am (2.5 hours), at a constant speed. What is the scooterist's speed?",
        ["45", "48", "42", "46"], "b",
        ["Speed = distance ÷ time = 120 km ÷ 2.5 hr = 48 km/h."],
        lambda: 120 / 2.5, 48.0, 1e-9),

    pyq(RY, 59, "q-di-distancetime", "Same journey: the scooterist starts at 9:00 am and finishes the 120 km journey at 11:30 am. How long did the scooterist's full journey take?",
        ["3", "2", "2.5", "3.5"], "c",
        ["11:30 am − 9:00 am = 2.5 hours."],
        lambda: 2.5, 2.5, 1e-9),

    pyq(RY, 60, "q-di-distancetime", "Same journey: the motorist and the scooterist's plotted paths cross at the point (10:30 am, 80 km). At what distance from the start do they meet?",
        ["75", "70", "90", "80"], "d",
        ["The crossing point's distance co-ordinate is 80 km."],
        lambda: 80, 80, 0),

    # ---- q-di-project ----
    pyq(RY, 423, "q-di-project", "District B's total infrastructure investment (₹crore) was 7081.6 in 1995 and 8352.0 in 1996. If 1997's investment grows at the SAME percentage rate as 1996 did over 1995, approximately what will the 1997 investment be?",
        ["₹10,020cr", "₹8,540cr", "₹9,850cr", "₹9,170cr"], "c",
        ["Growth factor 1995→1996 = 8352.0 ÷ 7081.6 ≈ 1.1794.", "Apply the SAME factor again: 8352.0 × 1.1794 ≈ ₹9,850 crore."],
        lambda: 8352.0 * (8352.0 / 7081.6), 9850.3, 1.0,
        trick="Multiply by the same RATIO again (not add the same absolute increase again) to keep the growth rate constant."),

    # ---- q-di-missingpart ----
    pyq(RY, 374, "q-di-missingpart", "At a college, a pie chart shows club membership: Football-only 15%, Cricket-only 5%, Both clubs 75%, and the rest of the students belong to neither club — exactly 40 students. What % of students belong to NEITHER club?",
        ["10%", "6%", "5%", "8%"], "c",
        ["The three labelled slices add to 15%+5%+75% = 95%.", "The missing (unlabelled) slice = 100% − 95% = 5%.", "(Cross-check: 5% of the college's total equals the given 40 students, so the total is 800 — self-consistent.)"],
        lambda: 100 - (15 + 5 + 75), 5.0, 1e-9),
]


def practice_items():
    return []
