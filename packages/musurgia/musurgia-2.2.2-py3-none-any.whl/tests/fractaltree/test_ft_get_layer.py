from fractions import Fraction
from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(proportions=[1, 2, 3], tree_permutation_order=[3, 1, 2], value=10)

    def test_0(self):
        with self.assertRaises(Exception):
            self.ft.get_layer(1)

    def test_1(self):
        self.assertEqual([self.ft], self.ft.get_layer(0))

    def test_2(self):
        self.ft.add_layer()
        result = self.ft.get_children()
        self.assertEqual(result, self.ft.get_layer(1))

    def test_3(self):
        for i in range(3):
            self.ft.add_layer()

        result = self.ft.get_children()
        self.assertEqual(result, self.ft.get_layer(1))

    def test_4(self):
        for i in range(3):
            self.ft.add_layer()
        result = [child.get_children() for child in self.ft.get_children()]

        self.assertEqual(result, self.ft.get_layer(2))

    def test_5(self):
        for i in range(3):
            self.ft.add_layer()
        result = self.ft.get_leaves()

        self.assertEqual(result, self.ft.get_layer(3))

    def test_6(self):
        for i in range(3):
            self.ft.add_layer()

        with self.assertRaises(ValueError):
            self.ft.get_layer(4)

    def test_7(self):
        self.ft.add_layer()
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        self.ft.add_layer(lambda n: True if n.fractal_order > 1 else False)
        result = [[['1.1'], [['1.2.1'], ['1.2.2.1', '1.2.2.2', '1.2.2.3'], ['1.2.3.1', '1.2.3.2', '1.2.3.3']], [['1.3.1.1', '1.3.1.2', '1.3.1.3'], ['1.3.2'], ['1.3.3.1', '1.3.3.2', '1.3.3.3']]], '2', [[['3.1.1'], ['3.1.2.1', '3.1.2.2', '3.1.2.3'], ['3.1.3.1', '3.1.3.2', '3.1.3.3']], [['3.2.1.1', '3.2.1.2', '3.2.1.3'], ['3.2.2'], ['3.2.3.1', '3.2.3.2', '3.2.3.3']], ['3.3']]]
        self.assertEqual(result, [name for name in self.ft.get_layer(4, key='name')])


    def test_7_1(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.assertEqual([10], self.ft.get_layer(0, key='value'))

    def test_7_2(self):
        self.ft.add_layer()
        self.ft.add_layer()
        result = [Fraction(5, 1), Fraction(5, 3), Fraction(10, 3)]
        self.assertEqual(result, self.ft.get_layer(1, key='value'))

    def test_7_3(self):
        self.ft.add_layer()
        self.ft.add_layer()
        result = [[Fraction(5, 6), Fraction(5, 3), Fraction(5, 2)], [Fraction(5, 6), Fraction(5, 18), Fraction(5, 9)],
                  [Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)]]
        self.assertEqual(result, self.ft.get_layer(2, key='value'))

