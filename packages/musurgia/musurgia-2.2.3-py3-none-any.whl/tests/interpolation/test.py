from unittest import TestCase

from quicktions import Fraction

from musurgia.interpolation import InterpolationGroup, RandomInterpolation, Interpolation


class Test(TestCase):

    def test_1(self):
        ig = InterpolationGroup()
        # ig.add_section(InterpolationSection(0, 100, 10))
        # ig.add_section(InterpolationSection(100, 50, 20))
        # ig.add_section(InterpolationSection(50, 200, 10))
        ig.add_section(0, 100, 10)
        ig.add_section(100, 50, 20)
        ig.add_section(50, 200, 10)

        test_case = [float(ig.__call__(x)) for x in range(0, 41)]
        expected = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 97.5, 95.0, 92.5, 90.0, 87.5,
                    85.0,
                    82.5, 80.0, 77.5, 75.0, 72.5, 70.0, 67.5, 65.0, 62.5, 60.0, 57.5, 55.0, 52.5, 50.0, 65.0, 80.0,
                    95.0,
                    110.0, 125.0, 140.0, 155.0, 170.0, 185.0, 200.0]

        self.assertEqual(expected, test_case)

    def test_2(self):
        ri = RandomInterpolation(start=[1, 2, 3], end=[7, 7, 7], periodicity=1, duration=20, seed=12)
        test_case = [ri.__call__(x) for x in range(0, 20)]
        expected = [2, 3, 2, 1, 3, 2, 3, 7, 3, 7, 3, 7, 3, 7, 3, 7, 3, 7, 7, 7]
        self.assertEqual(expected, test_case)

    def test_3(self):
        ri = RandomInterpolation(start=[60, 62, 66, 68], end=[67, 69, 73, 75], duration=13, seed=10)
        test_case = [ri.__call__(x) for x in range(0, 13)]
        expected = [60, 68, 67, 62, 66, 69, 67, 68, 66, 73, 69, 68, 73]
        self.assertEqual(expected, test_case)

    def test_4(self):
        interpolation = Interpolation(start=0, end=12, duration=12, grid=0.5)
        test_case = [interpolation.__call__(Fraction(x, 3)) for x in range(0, 12 * 3)]
        expected = [0.0, 0.5, 0.5, 1.0, 1.5, 1.5, 2.0, 2.5, 2.5, 3.0, 3.5, 3.5, 4.0, 4.5, 4.5, 5.0, 5.5, 5.5, 6.0, 6.5,
                    6.5, 7.0, 7.5, 7.5, 8.0, 8.5, 8.5, 9.0, 9.5, 9.5, 10.0, 10.5, 10.5, 11.0, 11.5, 11.5]
        self.assertEqual(expected, test_case)
