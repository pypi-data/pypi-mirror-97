from unittest import TestCase

from quicktions import Fraction

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10)

    def test_1(self):
        self.ft.change_value(20)
        result = 20
        self.assertEqual(result, self.ft.value)

    def test_2(self):
        self.ft.add_layer()
        self.ft.get_children()[0].change_value(10)
        expected = 15
        self.assertEqual(expected, self.ft.value)

    def test_3(self):
        self.ft.add_layer()
        self.ft.get_children()[0].change_value(10)
        expected = [Fraction(10, 1), Fraction(5, 3), Fraction(10, 3)]
        self.assertEqual(expected, [child.value for child in self.ft.get_children()])

    def test_4(self):
        self.ft.add_layer()
        self.ft.change_value(15)
        expected = [Fraction(15, 2), Fraction(5, 2), Fraction(5, 1)]
        self.assertEqual(expected, [child.value for child in self.ft.get_children()])

    def test_5(self):
        self.ft.add_layer()
        self.ft.add_layer()
        self.ft.get_children()[0].change_value(10)
        expected = [[Fraction(15, 1)],
                    [10, Fraction(5, 3), Fraction(10, 3)],
                    [[Fraction(5, 3), Fraction(10, 3), Fraction(5, 1)],
                     [Fraction(5, 6), Fraction(5, 18), Fraction(5, 9)],
                     [Fraction(10, 9), Fraction(5, 3), Fraction(5, 9)]]]
        self.assertEqual(expected,
                         [self.ft.get_layer(layer=i, key='value') for i in range(self.ft.number_of_layers + 1)])
