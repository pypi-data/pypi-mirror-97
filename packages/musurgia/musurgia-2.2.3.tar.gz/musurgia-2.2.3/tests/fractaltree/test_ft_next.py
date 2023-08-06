from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(proportions=[1, 2, 3], tree_permutation_order=[3, 1, 2], value=10)

    def test_1(self):
        self.ft.add_layer()
        self.ft.get_children()[1].add_layer()

        selected = self.ft.get_children()[1].get_children()[0]
        self.assertEqual(selected.__next__.name, '2.2')
