import os
from unittest import TestCase
from quicktions import Fraction

from musurgia.fractaltree.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def test_1(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2), value=10)
        ft.add_layer()
        ft.add_layer()
        for node in ft.get_layer(1):
            node.reduce_children(condition=lambda node: node.fractal_order == 1)
        self.assertEqual([node.fractal_order for node in ft.traverse_leaves()], [2, 3, 3, 2, 2, 3])

    def test_2(self):
        ft = FractalTree(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2), value=10)
        ft.add_layer()
        ft.add_layer()
        for node in ft.get_layer(1):
            node.reduce_children(condition=lambda node: node.fractal_order == 1)
        actual = [node.value for node in ft.traverse_leaves()]
        expected = [Fraction(2, 1),
                    Fraction(3, 1),
                    Fraction(1, 1),
                    Fraction(2, 3),
                    Fraction(4, 3),
                    Fraction(2, 1)]
        self.assertEqual(actual, expected)

    def test_3(self):
        ft = FractalTree(proportions=[1, 2, 3, 4, 5, 6], tree_permutation_order=[4, 1, 5, 3, 6, 2], value=20,
                         multi=(4, 3))
        ft.add_layer()
        ft.reduce_children(lambda child: child.fractal_order not in [2, 3])
        actual = [node.value for node in ft.get_children()]
        expected = [12, 8]
        self.assertEqual(actual, expected)