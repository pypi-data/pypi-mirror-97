from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        ft = FractalTree(proportions=[1, 2, 3], tree_permutation_order=[3, 1, 2], value=20)
        ft.add_layer()
        ft.get_children()[1].add_layer()
        self.ft = ft

    def test_1(self):
        self.assertIsNone(self.ft.get_previous_sibling())

    def test_2(self):
        self.assertIsNone(self.ft.get_children()[0].get_previous_sibling())

    def test_3(self):
        self.assertEqual(self.ft.get_children()[2].get_previous_sibling(), self.ft.get_children()[1])

    def test_4(self):
        self.assertEqual(self.ft.get_children()[1].get_children()[2].get_previous_sibling(),
                         self.ft.get_children()[1].get_children()[1])

    def test_5(self):
        self.assertIsNone(self.ft.get_children()[1].get_children()[0].get_previous_sibling())
