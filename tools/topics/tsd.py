"""Time, Speed and Distance: quiz tier."""
from bank import bound, mistake, pyq

TOPIC = "tsd"
PREFIX = "sd"
TIER = "quiz"
S1, S2, S3 = "2025-09-12-S1", "2025-09-12-S2", "2025-09-12-S3"

NODES = {
    "c-sd-basic": {"short": "Speed = distance ÷ time", "label": "Speed, distance and time: units first", "kind": "concept", "parent": TOPIC, "order": 1,
                   "summary": "One formula and one habit: write minutes and hours in the same unit before dividing.", "links": []},
    "c-sd-relative": {"short": "Relative speed", "label": "Relative speed: meeting and chasing", "kind": "concept", "parent": TOPIC, "order": 2,
                      "summary": "Towards each other speeds add; in the same direction they subtract.", "links": ["algebraic-identities"]},
    "c-sd-circular": {"short": "Circular track", "label": "Overtaking on a track", "kind": "concept", "parent": TOPIC, "order": 3,
                      "summary": "The faster one overtakes after closing the gap between them at the relative speed.", "links": []},
    "q-sd-convert": {"short": "Change the speed", "label": "Same distance, different time or route", "kind": "qtype", "parent": "c-sd-basic", "order": 1,
                     "summary": "Distance changes by a percentage, time is fixed, find the new speed.", "links": ["percentage"]},
    "q-sd-units": {"short": "Rate to long time", "label": "A rate in short time scaled to a long time", "kind": "qtype", "parent": "c-sd-basic", "order": 2,
                   "summary": "Distance in 1 minute; find the distance in hours.", "links": []},
    "q-sd-meet": {"short": "Two start points", "label": "Two bodies meet: opposite or same direction", "kind": "qtype", "parent": "c-sd-relative", "order": 1,
                  "summary": "Two meeting times give two equations: sum and difference of speeds.", "links": ["linear-equations"]},
    "q-sd-overtake": {"short": "Overtaking on a track", "label": "First overtake on a circular track", "kind": "qtype", "parent": "c-sd-circular", "order": 1,
                      "summary": "Gap ÷ relative speed gives the time; times the faster speed gives the distance.", "links": []},
}
FORMULAS = [
    {"id": "sd-f1", "node": "c-sd-basic", "text": "Distance = speed × time     1 km/h = 5/18 m/s", "note": "Put minutes and hours in one unit first."},
    {"id": "sd-f2", "node": "c-sd-basic", "text": "Same time: speed ∝ distance     Same distance: speed ∝ 1 ÷ time", "note": "25% more distance in the same time needs 25% more speed."},
    {"id": "sd-f3", "node": "c-sd-relative", "text": "Opposite: relative speed = u + v     Same direction: = u − v", "note": "Meeting time = gap ÷ relative speed."},
    {"id": "sd-f4", "node": "c-sd-circular", "text": "First overtake: time = gap ÷ (u − v); distance by the faster = u × time", "note": "The track length matters only if the gap is more than one lap."},
]
METHODS = {
    "q-sd-convert": {
        "cue": "'Distance increases by 25%… must still arrive in the same time. New speed?'",
        "formulas": ["sd-f2"], "tech": ["multiplier", "fraction-percent"],
        "standard": "Same time, so speed grows with distance: 200 × 1.25 = 250 km/h.",
        "fast": "The 40 minutes cancels. Raise the speed by the same 25%: 200 + 50.",
        "eliminate": "More distance in the same time means a higher speed, so the answer is above 200, and 25% of 200 is exactly 50.",
        "traps": ["Taking 25% of the time instead of the distance.", "Working out time from the 40 minutes and not cancelling it."]},
    "q-sd-units": {
        "cue": "'A train covers 1.2 km in 1 minute. How far in 2 h 15 min?'",
        "formulas": ["sd-f1"], "tech": ["units-first", "multiplier"],
        "standard": "2 h 15 min = 135 minutes. 1.2 × 135 = 162 km.",
        "fast": "1.2 × 100 = 120, 1.2 × 35 = 42, total 162.",
        "eliminate": "1.2 km a minute is 72 km/h. In 2.25 hours that is between 72 × 2 = 144 and 72 × 2.5 = 180, and 72 × 2.25 is exactly 162.",
        "traps": ["Reading 2 h 15 min as 2.15 hours.", "Treating 1.2 km as 1.2 km/h without the minute."]},
    "q-sd-meet": {
        "cue": "Two bodies start a fixed distance apart; one meeting time towards each other and another in the same direction.",
        "formulas": ["sd-f3"], "tech": ["relative", "back-substitute"],
        "standard": "Towards: u + v = 480 ÷ 5 = 96. Same direction: u − v = 480 ÷ 15 = 32. So u = (96 + 32) ÷ 2 = 64.",
        "fast": "The faster speed is the average of the sum and the difference: (96 + 32)/2.",
        "eliminate": "The faster speed must exceed half the sum (48) and be less than the sum (96). Test each option: v = 96 − u must be below u and u − v must equal 32.",
        "traps": ["Taking 96 as the faster speed.", "Using 480 ÷ 15 as one of the speeds.", "Choosing the slower speed, 32, as the answer."]},
    "q-sd-overtake": {
        "cue": "A circular track, two starts with the second ahead by some distance, and 'when does he overtake for the first time'.",
        "formulas": ["sd-f4"], "tech": ["relative"],
        "standard": "Relative speed 20 − 8 = 12 m/s. Gap 500 m, so time = 500 ÷ 12. Distance of the motorcycle = 20 × 500/12 = 833.33 m.",
        "fast": "Distance = gap × u ÷ (u − v) = 500 × 20/12 = 833.33.",
        "eliminate": "The motorcycle covers more than the 500 m gap (it must close it at 12 of its 20 m/s), so it travels about 500 × 20/12 ≈ 833 m. 800 m is too short and 1,800 m is far too long.",
        "traps": ["Giving the truck's distance (333.33 m) rather than the motorcycle's.", "Adding the speeds, as if they met head on.", "Using the track length of 2.2 km, which is irrelevant here."]},
}
PYQS = [
    pyq(S1, 65, "q-sd-convert", "An express train covers a fixed distance in 40 minutes at an average speed of 200 km/h. The route is diverted, increasing the distance by 25%. If the train must still arrive in 40 minutes, what should its new average speed be?", ["250 km/h", "260 km/h", "270 km/h", "280 km/h"], "a",
        ["Time is fixed, so speed is proportional to distance.", "New speed = 200 × 1.25 = 250 km/h."], lambda: (200 * 40 / 60 * 1.25) / (40 / 60), 250, 1e-9, tech=["multiplier", "fraction-percent"],
        trick="Same time, so just add 25% to the speed."),
    pyq(S1, 67, "q-sd-meet", "Two motorcycles M and N start from points 480 km apart. Moving towards each other they meet in 5 hours; moving in the same direction they meet in 15 hours. What is the speed of M, the faster motorcycle?", ["55 km/h", "64 km/h", "70 km/h", "80 km/h"], "b",
        ["Towards each other: M + N = 480 ÷ 5 = 96 km/h.", "Same direction: M − N = 480 ÷ 15 = 32 km/h.", "M = (96 + 32) ÷ 2 = 64 km/h (and N = 32 km/h)."], lambda: (480 / 5 + 480 / 15) / 2, 64, 1e-9,
        tech=["relative"], concepts=1, trick="Faster speed = average of (sum, difference) = (96 + 32)/2.",
        wrong={"a": bound("M = 55 makes N = 41 and M − N = 14, not 32.", lambda v: abs(v - 64) > 1e-9)}),
    pyq(S2, 69, "q-sd-overtake", "On a circular track a motorcycle starts from X and a truck from Y, which is 500 m ahead of X in the direction of motion. The motorcycle's speed is 20 m/s, the truck's 8 m/s and the track is 2.2 km long. How far will the motorcycle have travelled when it overtakes the truck for the first time?", ["845.5 m", "1,800 m", "800 m", "833.33 m"], "d",
        ["Relative speed = 20 − 8 = 12 m/s.", "Time to close the 500 m gap = 500 ÷ 12 s.", "Distance of the motorcycle = 20 × 500/12 = 833.33 m."], lambda: 20 * 500 / (20 - 8), 833.33, 0.01,
        tech=["relative"], concepts=1, trick="Gap × faster ÷ (faster − slower) = 500 × 20/12.",
        wrong={"b": mistake("This is 20 × 90, a time with no basis in the gap.", 1800, 0)}),
    pyq(S3, 60, "q-sd-units", "A train covers 1.2 km in 1 minute. How far will it travel in 2 hours 15 minutes?", ["162 km", "156 km", "171 km", "168 km"], "a",
        ["2 h 15 min = 135 minutes.", "Distance = 1.2 × 135 = 162 km."], lambda: 1.2 * 135, 162, 1e-9, tech=["units-first", "multiplier"],
        trick="1.2 × 135 = 120 + 42.", wrong={"b": mistake("1.2 × 130, losing 5 minutes.", 156, 0)}),
]


def practice_items():
    return []
