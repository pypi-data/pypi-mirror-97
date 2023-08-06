from unittest import TestCase

from musurgia.permutation import LimitedPermutation, self_permute, get_self_multiplied_permutation, \
    get_reordered_self_multiplied_permutation, get_vertical_self_multiplied_permutation


class Test(TestCase):
    def test_1_1(self):
        permutation_order = [3, 1, 2]
        self_permutation = self_permute(permutation_order)
        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3]]
        self.assertEqual(result, self_permutation)

    def test_1_2(self):
        permutation_order = [3, 1, 2]
        self_multiplied_permutation = get_self_multiplied_permutation(permutation_order)
        result = [[[1, 2, 3], [3, 1, 2], [2, 3, 1]],
                  [[2, 3, 1], [1, 2, 3], [3, 1, 2]],
                  [[3, 1, 2], [2, 3, 1], [1, 2, 3]]]
        self.assertEqual(result, self_multiplied_permutation)

    def test_1_3(self):
        permutation_order = [3, 1, 2]
        reordered_self_multiplied_permutation = get_reordered_self_multiplied_permutation(permutation_order)
        result = [[[3, 1, 2], [2, 3, 1], [1, 2, 3]],
                  [[1, 2, 3], [3, 1, 2], [2, 3, 1]],
                  [[2, 3, 1], [1, 2, 3], [3, 1, 2]]]
        self.assertEqual(result, reordered_self_multiplied_permutation)

    def test_1_4(self):
        permutation_order = [3, 1, 2]
        vertical_self_multiplied_permutation = get_vertical_self_multiplied_permutation(permutation_order)
        result = [[[1, 3, 2], [2, 1, 3], [3, 2, 1]],
                  [[2, 1, 3], [3, 2, 1], [1, 3, 2]],
                  [[3, 2, 1], [1, 3, 2], [2, 1, 3]]]
        self.assertEqual(result, vertical_self_multiplied_permutation)

    def test_2_1(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1])
        result = [[3, 1, 2], [2, 3, 1], [1, 2, 3], [1, 2, 3], [3, 1, 2], [2, 3, 1], [2, 3, 1], [1, 2, 3], [3, 1, 2]]
        self.assertEqual(result, perm.multiplied_orders)

    def test_2_2(self):
        perm = LimitedPermutation(['a', 'b', 'c'], [3, 1, 2], multi=[1, 1], reading_direction='vertical')

        result = [[1, 3, 2], [2, 1, 3], [3, 2, 1], [2, 1, 3], [3, 2, 1], [1, 3, 2], [3, 2, 1], [1, 3, 2], [2, 1, 3]]
        self.assertEqual(result, perm.multiplied_orders)

    def test_3_1(self):
        permutation_order = [3, 4, 2, 1]
        self_multiplied_permutation = get_self_multiplied_permutation(permutation_order)
        result = [[[4, 3, 1, 2], [1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 2, 1]],
                  [[2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4], [4, 3, 1, 2]],
                  [[1, 2, 3, 4], [4, 3, 1, 2], [3, 4, 2, 1], [2, 1, 4, 3]],
                  [[3, 4, 2, 1], [2, 1, 4, 3], [4, 3, 1, 2], [1, 2, 3, 4]]]
        self.assertEqual(result, self_multiplied_permutation)

    def test_3_2(self):
        permutation_order = [3, 4, 2, 1]
        reordered_self_multiplied_permutation = get_reordered_self_multiplied_permutation(permutation_order)
        result = [[[3, 4, 2, 1], [2, 1, 4, 3], [4, 3, 1, 2], [1, 2, 3, 4]],
                  [[4, 3, 1, 2], [1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 2, 1]],
                  [[2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4], [4, 3, 1, 2]],
                  [[1, 2, 3, 4], [4, 3, 1, 2], [3, 4, 2, 1], [2, 1, 4, 3]]]
        self.assertEqual(result, reordered_self_multiplied_permutation)

    def test_3_3(self):
        permutation_order = [3, 4, 2, 1]
        vertical_self_multiplied_permutation = get_vertical_self_multiplied_permutation(permutation_order)
        result = [[[4, 1, 2, 3], [3, 2, 1, 4], [1, 3, 4, 2], [2, 4, 3, 1]],
                  [[2, 3, 1, 4], [1, 4, 2, 3], [4, 2, 3, 1], [3, 1, 4, 2]],
                  [[1, 4, 3, 2], [2, 3, 4, 1], [3, 1, 2, 4], [4, 2, 1, 3]],
                  [[3, 2, 4, 1], [4, 1, 3, 2], [2, 4, 1, 3], [1, 3, 2, 4]]]
        self.assertEqual(result, vertical_self_multiplied_permutation)

    def test_4_1(self):
        permutation_order = [4, 3, 2, 1]
        self_multiplied_permutation = get_self_multiplied_permutation(permutation_order)
        result = [[[1, 2, 3, 4], [4, 3, 2, 1], [1, 2, 3, 4], [4, 3, 2, 1]],
                  [[4, 3, 2, 1], [1, 2, 3, 4], [4, 3, 2, 1], [1, 2, 3, 4]],
                  [[1, 2, 3, 4], [4, 3, 2, 1], [1, 2, 3, 4], [4, 3, 2, 1]],
                  [[4, 3, 2, 1], [1, 2, 3, 4], [4, 3, 2, 1], [1, 2, 3, 4]]]
        self.assertEqual(result, self_multiplied_permutation)

    def test_4_2(self):
        permutation_order = [4, 3, 2, 1]
        vertical_self_multiplied_permutation = get_vertical_self_multiplied_permutation(permutation_order)
        result = [[[1, 4, 1, 4], [2, 3, 2, 3], [3, 2, 3, 2], [4, 1, 4, 1]],
                  [[4, 1, 4, 1], [3, 2, 3, 2], [2, 3, 2, 3], [1, 4, 1, 4]],
                  [[1, 4, 1, 4], [2, 3, 2, 3], [3, 2, 3, 2], [4, 1, 4, 1]],
                  [[4, 1, 4, 1], [3, 2, 3, 2], [2, 3, 2, 3], [1, 4, 1, 4]]]
        self.assertEqual(result, vertical_self_multiplied_permutation)

    def test_5(self):
        size = 3
        tree_permutation_order = (3, 1, 2)
        multi = (3, 4)

        permutation = LimitedPermutation(input_list=list(range(1, size + 1)),
                                         main_permutation_order=tree_permutation_order,
                                         multi=multi)
        result = permutation.multi
        expected = (1, 1)
        self.assertEqual(expected, result)

    def test_6(self):
        size = 3
        tree_permutation_order = (3, 1, 2)
        multi = (2, 4)

        permutation = LimitedPermutation(input_list=list(range(1, size + 1)),
                                         main_permutation_order=tree_permutation_order,
                                         multi=multi)
        result = permutation.multi
        expected = (3, 1)
        self.assertEqual(expected, result)
