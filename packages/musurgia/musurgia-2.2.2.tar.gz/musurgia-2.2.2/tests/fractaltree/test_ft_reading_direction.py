from unittest import TestCase
import os

from musurgia.fractaltree.fractaltree import FractalTree

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def test_1(self):
        ft = FractalTree(reading_direction='vertical', value=10)
        ft.add_layer()
        permutation_orders = [child.permutation_order for child in ft.get_children()]
        result = [[2, 1, 3], [3, 2, 1], [1, 3, 2]]
        self.assertEqual(result, permutation_orders)
