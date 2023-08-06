import os
from unittest import TestCase

from quicktions import Fraction

from musurgia.fractaltree.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def test_1(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.tempo = 60
        ft.value = 10
        ft.add_layer()
        ft.add_layer()
        self.assertEqual([node.fractal_order for node in ft.traverse_leaves()], [1, 2, 3, 3, 1, 2, 2, 3, 1])

    def test_2(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.tempo = 60
        ft.value = 10
        ft.add_layer()
        ft.add_layer()
        self.assertEqual([node.value for node in ft.traverse_leaves()],
                         [Fraction(5, 6), Fraction(5, 3), Fraction(5, 2), Fraction(5, 6), Fraction(5, 18),
                          Fraction(5, 9),
                          Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)])

    def test_3(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        ft.add_layer()
        ft.get_children()[0].add_layer()
        expected = [[0.8333333333333334, 1.6666666666666667, 2.5], 1.6666666666666667, 3.3333333333333335]
        result = ft.get_leaves(key=lambda leaf: float(leaf.value))
        self.assertEqual(expected, result)
