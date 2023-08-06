from unittest import TestCase

from musurgia.timing import Clock, Timing


class Test(TestCase):
    def test_1(self):
        seconds = 180
        self.assertEqual(Timing.get_clock(seconds), '''0:3':00"''')

    def test_2(self):
        t = Timing(quarter_duration=1, duration=0.65)
        result = 92.3076923076923
        self.assertEqual(result, t.tempo)

    def test_3(self):
        clock = Clock()
        clock.duration = 37
        result = (0, 0, 37)
        self.assertEqual(result, clock.clock)

    def test_4(self):
        clock1 = Clock(clock=(0, 2, 31))
        clock2 = Clock(clock=(0, 3, 11))
        clock3 = clock2.subtract(clock1)
        result = (0, 0, 40)
        self.assertEqual(result, clock3.clock)
