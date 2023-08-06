from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree, FractalTreeException, SetValueFirst


class Test(TestCase):
    def test_1(self):
        ft = FractalTree()
        ft.value = 50
        ft.add_layer()
        self.assertEqual(sum([leaf.value for leaf in ft.get_leaves()]), ft.value)

    def test_2(self):
        ft = FractalTree()
        ft.value = 50
        ft.add_layer()
        with self.assertRaises(FractalTreeException):
            ft.value = 100

    def test_3(self):
        ft = FractalTree()
        with self.assertRaises(SetValueFirst):
            ft.add_layer()
