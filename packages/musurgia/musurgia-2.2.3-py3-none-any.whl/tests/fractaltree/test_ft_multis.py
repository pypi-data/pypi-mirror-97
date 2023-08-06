from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(tree_permutation_order=[3, 1, 2], proportions=[1, 2, 3], value=10)

    def test_1(self):
        self.ft.add_layer()
        result = [(2, 1), (2, 2), (2, 3)]
        self.assertEqual(result, [child.multi for child in self.ft.get_children()])

    def test_2(self):
        self.ft.multi = (1, 7)
        self.ft.add_layer()
        result = [leaf.value for leaf in self.ft.traverse_leaves()]
        ft = FractalTree(value=10, multi=(3, 1))
        ft.add_layer()
        expected = [leaf.value for leaf in ft.traverse_leaves()]
        self.assertEqual(expected, result)

    def test_3(self):
        self.ft.multi = (4, 1)
        self.ft.add_layer()
        result = [leaf.value for leaf in self.ft.traverse_leaves()]
        ft = FractalTree(value=10, multi=(1, 1))
        ft.add_layer()
        expected = [leaf.value for leaf in ft.traverse_leaves()]
        self.assertEqual(expected, result)

    def test_4(self):
        self.ft.multi = (3, 4)
        self.ft.add_layer()
        result = [leaf.value for leaf in self.ft.traverse_leaves()]
        ft = FractalTree(value=10, multi=(1, 1))
        ft.add_layer()
        expected = [leaf.value for leaf in ft.traverse_leaves()]
        self.assertEqual(expected, result)
