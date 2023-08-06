from unittest import TestCase

from quicktions import Fraction

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10)

    def test_1(self):
        self.assertEqual([self.ft], self.ft.get_leaves())

    def test_2(self):
        self.assertEqual([self.ft.value], self.ft.get_leaves(key=lambda leaf: leaf.value))

    def test_3(self):
        self.ft.add_layer()
        [child for child in self.ft.get_children() if child.fractal_order == 1][0].fertile = False
        self.ft.add_layer()
        result = [[Fraction(5, 6), Fraction(5, 3), Fraction(5, 2)], Fraction(5, 3),
                  [Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)]]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.value))
