from unittest import TestCase

from musurgia.fractaltree.fractalmusicsquare import Square


class Test(TestCase):
    def setUp(self) -> None:
        self.square = Square(duration=100, proportions=(1, 2), tree_permutation_order=(2, 1))
        self.copied_square = self.square.__deepcopy__()

    def test_1(self):
        self.assertNotEqual(self.square, self.copied_square)

    def test_2(self):
        self.assertNotEqual(self.square.rows, self.copied_square.rows)

    def test_3(self):
        self.assertNotEqual(self.square.get_all_modules(), self.copied_square.get_all_modules())

    def test_4(self):
        first_module = self.square.get_module(1, 1)
        old_duration = first_module.duration
        first_module.duration = 20
        self.assertEqual(old_duration, self.copied_square.get_module(1, 1).duration)

    def test_5(self):
        self.square.get_module(1, 1).duration = 20
        copied_square = self.square.__deepcopy__()
        self.assertEqual(20, copied_square.get_module(1, 1).duration)

    def test_6(self):
        for row in self.square.rows:
            row.set_name('L {} L'.format(row.number))
        copied_square = self.square.__deepcopy__()
        expected = [row.name for row in self.square.rows]
        result = [row.name for row in copied_square.rows]
        self.assertEqual(expected, result)
