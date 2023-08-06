import os
from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def test_1(self):
        ft = FractalTree(proportions=(1, 2, 3, 4, 5), tree_permutation_order=(3, 5, 1, 2, 4), value=10)
        ft.add_layer()
        # ft.add_layer()
        # print(ft.get_leaves(key=lambda leaf: leaf.index))
        # print(ft.get_leaves(key=lambda leaf: leaf.fractal_order))
        # print(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)))
        ft.merge_children(1, 2, 2)
        # print(ft.get_leaves(key=lambda leaf: leaf.index))
        self.assertEqual(ft.get_leaves(key=lambda leaf: leaf.fractal_order), [3, 5, 2])
        self.assertEqual(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)), [2.0, 4.0, 4.0])