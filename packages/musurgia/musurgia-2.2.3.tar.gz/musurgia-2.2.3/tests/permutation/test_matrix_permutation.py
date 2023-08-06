from unittest import TestCase

from musurgia.permutation import permute_matrix_columnwise, permute_matrix_rowwise, invert_matrix, permute_matrix


class Test(TestCase):
    def setUp(self) -> None:
        self.main_permutation_order = (2, 6, 4, 1, 3, 7, 5)
        self.matrix = [[(i, j) for i in range(1, 8) for j in range(1, 8)][k * 7:k * 7 + 7] for k in range(7)]

    def test_1(self):
        result = invert_matrix(self.matrix)
        expected = [((1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)),
                    ((1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)),
                    ((1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3)),
                    ((1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)),
                    ((1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)),
                    ((1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)),
                    ((1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7))]
        self.assertEqual(expected, result)

    def test_2(self):
        result = permute_matrix_rowwise(self.matrix, self.main_permutation_order)
        expected = [[(1, 2), (1, 6), (1, 4), (1, 1), (1, 3), (1, 7), (1, 5)],
                    [(2, 6), (2, 7), (2, 1), (2, 2), (2, 4), (2, 5), (2, 3)],
                    [(3, 7), (3, 5), (3, 2), (3, 6), (3, 1), (3, 3), (3, 4)],
                    [(4, 5), (4, 3), (4, 6), (4, 7), (4, 2), (4, 4), (4, 1)],
                    [(5, 3), (5, 4), (5, 7), (5, 5), (5, 6), (5, 1), (5, 2)],
                    [(6, 4), (6, 1), (6, 5), (6, 3), (6, 7), (6, 2), (6, 6)],
                    [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]]
        self.assertEqual(expected, result)

    def test_3(self):
        result = permute_matrix_columnwise(self.matrix, self.main_permutation_order)
        expected = [((2, 1), (6, 2), (7, 3), (5, 4), (3, 5), (4, 6), (1, 7)),
                    ((6, 1), (7, 2), (5, 3), (3, 4), (4, 5), (1, 6), (2, 7)),
                    ((4, 1), (1, 2), (2, 3), (6, 4), (7, 5), (5, 6), (3, 7)),
                    ((1, 1), (2, 2), (6, 3), (7, 4), (5, 5), (3, 6), (4, 7)),
                    ((3, 1), (4, 2), (1, 3), (2, 4), (6, 5), (7, 6), (5, 7)),
                    ((7, 1), (5, 2), (3, 3), (4, 4), (1, 5), (2, 6), (6, 7)),
                    ((5, 1), (3, 2), (4, 3), (1, 4), (2, 5), (6, 6), (7, 7))]
        self.assertEqual(expected, result)

    def test_4(self):
        result = permute_matrix(self.matrix, self.main_permutation_order)
        expected = [((2, 6), (6, 1), (7, 3), (5, 5), (3, 1), (4, 4), (1, 5)),
                    ((6, 4), (7, 2), (5, 7), (3, 6), (4, 2), (1, 7), (2, 3)),
                    ((4, 5), (1, 6), (2, 1), (6, 3), (7, 5), (5, 1), (3, 4)),
                    ((1, 2), (2, 7), (6, 5), (7, 4), (5, 6), (3, 3), (4, 1)),
                    ((3, 7), (4, 3), (1, 4), (2, 2), (6, 7), (7, 6), (5, 2)),
                    ((7, 1), (5, 4), (3, 2), (4, 7), (1, 3), (2, 5), (6, 6)),
                    ((5, 3), (3, 5), (4, 6), (1, 1), (2, 4), (6, 2), (7, 7))]
        self.assertEqual(expected, result)
