from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def test_1(self):
        ft = FractalTree(value=100)
        self.assertEqual(100, ft.value)

    def test_2(self):
        fm = FractalMusic(value=100)
        self.assertEqual(100, fm.value)

    def test_3(self):
        fm = FractalMusic(duration=100)
        self.assertEqual(100, fm.value)

    def test_4(self):
        fm = FractalMusic(value=100)
        self.assertEqual(100, fm.duration)
