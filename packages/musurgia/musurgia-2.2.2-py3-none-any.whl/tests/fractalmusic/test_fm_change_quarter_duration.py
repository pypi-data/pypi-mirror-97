from unittest import TestCase

from quicktions import Fraction

from musurgia.fractaltree.fractalmusic import FractalMusic


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(tempo=72, quarter_duration=10)

    def test_1(self):
        self.fm.change_quarter_duration(20)
        expected = 20
        self.assertEqual(expected, self.fm.quarter_duration)

    def test_2(self):
        self.fm.add_layer()
        self.fm.get_children()[0].change_quarter_duration(10)
        expected = 15
        self.assertEqual(expected, self.fm.quarter_duration)

    def test_3(self):
        self.fm.add_layer()
        self.fm.get_children()[0].change_quarter_duration(10)
        expected = [Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)]
        self.assertEqual(expected, [child.quarter_duration for child in self.fm.get_children()])

    def test_4(self):
        self.fm.add_layer()
        self.fm.change_quarter_duration(15)
        expected = [Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)]
        self.assertEqual(expected, [child.quarter_duration for child in self.fm.get_children()])

    def test_5(self):
        self.fm.add_layer()
        self.fm.add_layer()
        self.fm.get_children()[0].change_quarter_duration(10)
        expected = [[Fraction(15, 1)],
                    [10, Fraction(5, 3), Fraction(10, 3)],
                    [[Fraction(5, 3), Fraction(10, 3), Fraction(5, 1)],
                     [Fraction(5, 6), Fraction(5, 18), Fraction(5, 9)],
                     [Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)]]]
        self.assertEqual(expected,
                         [self.fm.get_layer(layer=i, key='quarter_duration') for i in
                          range(self.fm.number_of_layers + 1)])
