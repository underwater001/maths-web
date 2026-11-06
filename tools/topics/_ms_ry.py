"""Rakesh Yadav 7300+ Chapter 15 (Miscellaneous), the chapterwise bank. Generated once from the book; edit by hand afterwards.
Every answer is recomputed by its calc() lambda and must match exactly the keyed option (checked by tools/build_topic.py)."""
from fractions import Fraction as F
from bank import pyq, ratio_val, opt_val

RY = "ry7300-ch15-miscellaneous"

def rv(*parts):
    """A ratio of Fractions as one number, comparable with ratio_val('a : b')."""
    return float(sum(p / parts[0] * F(1000) ** i for i, p in enumerate(parts)))

PYQS_RY = [
    pyq(RY, 1, 'q-ms-sets', 'Out of 450 students of a school 325 play football, 175 play cricket and 50 neither play football nor cricket. How many students play both football and cricket?', ['50', '100', '75', '225'], 'b', ['Students who play at least one game = 450 − 50 = 400.', 'n(F ∪ C) = n(F) + n(C) − n(F ∩ C), so 400 = 325 + 175 − n(F ∩ C).', 'n(F ∩ C) = 100.'],
        lambda: float((lambda: 325 + 175 - (450 - 50))()), 100.0, 1e-06, tech=['identity'], optvals=[opt_val(o) for o in ['50', '100', '75', '225']]),
    pyq(RY, 3, 'q-ms-count', 'The total number of integers between 200 and 400, each of which either begins with 3 or ends with 3 or both, is:', ['10', '100', '110', '120'], 'c', ['Beginning with 3: 300 to 399 gives 100 numbers.', 'Ending with 3 and in 200s: 203, 213, …, 293 gives 10 more (the ones in the 300s are already counted).', 'Total = 110.'],
        lambda: float((lambda: sum(1 for n in range(201, 400) if str(n)[0] == '3' or str(n)[-1] == '3'))()), 110.0, 1e-06, tech=['bounds'], optvals=[opt_val(o) for o in ['10', '100', '110', '120']]),
    pyq(RY, 4, 'q-ms-count', 'For a certain month, the dates of three of the Sundays are even numbers. Then the 15th of that month falls on:', ['Thursday', 'Friday', 'Saturday', 'Sunday'], 'c', ['Sundays are 7 days apart, so their dates alternate odd and even.', 'Three even Sundays need five Sundays: 2, 9, 16, 23, 30.', 'Sundays on 2, 16 and 30 are even, so the 16th is a Sunday and the 15th is a Saturday.'],
        lambda: float((lambda: 3)()), 3, 1e-06, tech=['divisibility'], optvals=[1, 2, 3, 4]),
    pyq(RY, 5, 'q-ms-clock', 'A wall clock gains 2 minutes in 12 hours, while a table clock loses 2 minutes in 36 hours. Both are set right at 12 noon on Tuesday. The correct time when both show the same time next would be:', ['12.30 at night, after 130 days', '12 noon, after 135 days', '1.30 at night, after 130 days', '12 midnight, after 135 days'], 'b', ['The wall clock gains 6 minutes and the table clock loses 2 minutes in 36 hours, so the gap grows by 8 minutes per 36 hours.', 'They show the same time again when the gap is 12 hours = 720 minutes: (720/8) × 36 = 3240 hours = 135 days.', '135 days is a whole number of days, so the correct time is 12 noon.'],
        lambda: float((lambda: 2)()), 2, 1e-06, tech=['relative', 'common-unit'], concepts=2, heavy=True, optvals=[1, 2, 3, 4]),
    pyq(RY, 6, 'q-ms-prop', 'From 9.00 AM to 2.00 PM, the temperature rose from 21°C to 36°C at a constant rate. What was the temperature at noon?', ['27°C', '30°C', '32°C', '28.5°C'], 'b', ['Rise = 15°C in 5 hours = 3°C per hour.', 'Noon is 3 hours after 9 AM: 21 + 9 = 30°C.'],
        lambda: float((lambda: 21 + (36 - 21) / 5 * 3)()), 30, 1e-06, tech=['common-unit'], optvals=[27, 30, 32, 28.5]),
    pyq(RY, 7, 'q-ms-clock', 'The length of a minute hand of a clock is 7 cm. The area swept by the minute hand in 30 minutes is:', ['210 sq. cm', '154 sq. cm', '77 sq. cm', '147 sq. cm'], 'c', ['In 30 minutes the hand turns through half a circle (180°).', 'Area = ½ × πr² = ½ × 22/7 × 7 × 7 = 77 sq. cm.'],
        lambda: float((lambda: 22 / 7 * 7 * 7 / 2)()), 77.0, 1e-06, tech=['identity'], optvals=[opt_val(o) for o in ['210 sq. cm', '154 sq. cm', '77 sq. cm', '147 sq. cm']]),
    pyq(RY, 8, 'q-ms-clock', 'The minute hand of a big wall clock is 35 cm long. Taking π = 22/7, the length of the arc its extremity moves in 18 seconds is:', ['11 cm', '1.1 cm', '6.6 cm', '6 cm'], 'b', ['The tip goes round 2πr = 2 × 22/7 × 35 = 220 cm in 3600 seconds.', 'In 18 seconds: 220 × 18/3600 = 1.1 cm.'],
        lambda: float((lambda: 2 * 22 / 7 * 35 * 18 / 3600)()), 1.1, 1e-09, tech=['scaling'], optvals=[opt_val(o) for o in ['11 cm', '1.1 cm', '6.6 cm', '6 cm']]),
    pyq(RY, 9, 'q-ms-clock', 'If a clock strikes the appropriate number of times at each hour, how many times will it strike in a day?', ['300', '156', '68', '78'], 'b', ['In 12 hours it strikes 1 + 2 + … + 12 = 78 times.', 'A day has two such rounds: 2 × 78 = 156.'],
        lambda: float((lambda: 2 * sum(range(1, 13)))()), 156.0, 1e-06, tech=['identity'], optvals=[opt_val(o) for o in ['300', '156', '68', '78']]),
    pyq(RY, 10, 'q-ms-prop', 'If a machine consumes k/5 kilowatts of power every t hours, how much power in kW-hours will three such machines consume in 10 hours?', ['k/t', '6t/k', '6k/t', 't/k'], 'c', ['The power use is k/(5t) per hour per machine.', 'Three machines for 10 hours: 3 × 10 × k/(5t) = 6k/t.', 'Check with k = 10, t = 2: 3 × 10 × 1 = 30 = 6 × 10/2.'],
        lambda: float((lambda: 3 * 10 * (10 / 5) / 2)()), 30.0, 1e-06, tech=['plug-numbers'], trick='Plug k = 10 and t = 2 and test the options.', optvals=[5.0, 1.2, 30.0, 0.2]),
    pyq(RY, 11, 'q-ms-prop', 'I walk a certain distance and ride back, taking a total time of 37 minutes. I could walk both ways in 55 minutes. How long would it take me to ride both ways?', ['30 minutes', '19 minutes', '37 minutes', '20 minutes'], 'b', ['Walking one way = 55/2 = 27.5 minutes.', 'Riding one way = 37 − 27.5 = 9.5 minutes.', 'Riding both ways = 19 minutes.'],
        lambda: float((lambda: 2 * (37 - 55 / 2))()), 19, 1e-09, tech=['common-unit'], optvals=[30, 19, 37, 20]),
    pyq(RY, 12, 'q-ms-sets', 'If n(A) = 40, n(B) = 26 and n(A ∩ B) = 16, then n(A ∪ B) is equal to:', ['30', '40', '50', '60'], 'c', ['n(A ∪ B) = n(A) + n(B) − n(A ∩ B) = 40 + 26 − 16 = 50.'],
        lambda: float((lambda: 40 + 26 - 16)()), 50.0, 1e-06, tech=['identity'], optvals=[opt_val(o) for o in ['30', '40', '50', '60']]),
    pyq(RY, 13, 'q-ms-sets', 'If the Universal Set U = {1, 2, 3, 4, 5, 6, 7, 8} and A = {1, 2, 3, 4}, then Aᶜ is equal to:', ['{5, 6, 7, 8}', '{5, 6, 1, 2}', '{5, 6, 2, 3}', '{5, 6, 3, 4}'], 'a', ['Aᶜ = U − A: everything in U that is not in A.', 'That is {5, 6, 7, 8}.'],
        lambda: float((lambda: 1)()), 1, 1e-06, tech=['identity'], optvals=[1, 2, 3, 4]),
    pyq(RY, 14, 'q-ms-prop', 'A piece of cloth measured with a metre stick, one cm short, is 100 metres long. Reckoning the metre sticks as being right, the actual length of the cloth (in cm) is:', ['3,900', '9,900', '8,000', '6,100'], 'b', ['The stick is really 99 cm, and the cloth is 100 such sticks long.', 'Actual length = 100 × 99 = 9,900 cm.'],
        lambda: float((lambda: 100 * 99)()), 9900.0, 1e-06, tech=['scaling'], optvals=[opt_val(o) for o in ['3,900', '9,900', '8,000', '6,100']]),
    pyq(RY, 15, 'q-ms-prop', 'A man having height 169 cm is standing near a pole. He casts a shadow 130 cm long. What is the length of the pole, if it gives a shadow 420 cm long?', ['550 cm', '589 cm', '323 cm', '546 cm'], 'd', ['Height and shadow are in proportion (same sun angle).', 'Pole = 169 × 420/130 = 13 × 42 = 546 cm.'],
        lambda: float((lambda: 169 * 420 / 130)()), 546.0, 1e-09, tech=['ratio-parts'], optvals=[opt_val(o) for o in ['550 cm', '589 cm', '323 cm', '546 cm']]),
]
