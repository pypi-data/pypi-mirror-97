from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def test_1(self):
        ft = FractalTree()
        self.assertEqual(3, ft.size)