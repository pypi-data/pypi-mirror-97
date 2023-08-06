from fractions import Fraction
from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic


def get_infos(fm):
    return [fm.tempo, fm.quarter_duration, fm.duration]


def print_infos(fm):
    print('tempo={}; quarter_duration={}; duration={};'.format(
        *get_infos(fm)))


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(tree_permutation_order=[3, 1, 2], proportions=[1, 2, 3], duration=20)

    def test_1(self):
        # print(self.fm.tempo)
        # print(self.fm.quarter_duration)
        # print(self.fm.duration)
        # print_infos(self.fm)
        self.fm.tempo = 60
        result = [60, Fraction(20, 1), Fraction(20, 1)]
        self.assertEqual(result, get_infos(self.fm))

    def test_2(self):
        self.fm.tempo = 60
        self.fm.duration = 10
        # print_infos(self.fm)
        result = [60, Fraction(10, 1), Fraction(10, 1)]
        # print(get_infos(self.fm))
        self.assertEqual(result, get_infos(self.fm))

    def test_3(self):
        self.fm.duration = 10
        self.fm.tempo = 72
        # print_infos(self.fm)
        result = [72, Fraction(12, 1), Fraction(10, 1), ]
        # print(get_infos(self.fm))
        self.assertEqual(result, get_infos(self.fm))

    def test_5(self):
        self.fm.duration = 10
        self.fm.tempo = 72
        self.fm.quarter_duration = 30
        # print_infos(self.fm)
        result = [72, 30, 25]
        # print(get_infos(self.fm))
        self.assertEqual(result, get_infos(self.fm))

    def test_6(self):
        self.fm.duration = 10
        self.fm.tempo = 72
        self.fm.quarter_duration = 40
        self.fm.duration = 20
        # print_infos(self.fm)
        result = [72, 24, 20]
        # print(get_infos(self.fm))
        self.assertEqual(result, get_infos(self.fm))
