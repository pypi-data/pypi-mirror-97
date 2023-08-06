from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(4, 2, 7, 1, 6, 3, 5))

    def test_1(self):
        actual = self.ft._get_merge_lengths(number_of_children=1, merge_index=4)
        expected = [7]
        self.assertEqual(expected, actual)

    def test_2(self):
        actual = self.ft._get_merge_lengths(number_of_children=2, merge_index=0)
        expected = [6, 1]
        self.assertEqual(expected, actual)

    def test_3(self):
        actual = self.ft._get_merge_lengths(number_of_children=2, merge_index=4)
        expected = [4, 3]
        self.assertEqual(expected, actual)

    def test_4(self):
        actual = self.ft._get_merge_lengths(number_of_children=3, merge_index=2)
        expected = [1, 1, 5]
        self.assertEqual(expected, actual)

    def test_5(self):
        actual = self.ft._get_merge_lengths(number_of_children=3, merge_index=3)
        expected = [2, 1, 4]
        self.assertEqual(expected, actual)

    def test_6(self):
        actual = self.ft._get_merge_lengths(number_of_children=3, merge_index=1)
        expected = [1, 5, 1]
        self.assertEqual(expected, actual)

    def test_7(self):
        actual = self.ft._get_merge_lengths(number_of_children=6, merge_index=3)
        expected = [1, 1, 1, 2, 1, 1]
        self.assertEqual(expected, actual)

    def test_8(self):
        actual = self.ft._get_merge_lengths(number_of_children=7, merge_index=3)
        expected = [1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(expected, actual)

    def test_9(self):
        actual = self.ft._get_merge_lengths(number_of_children=4, merge_index=5)
        expected = [3, 1, 1, 2]
        self.assertEqual(expected, actual)
