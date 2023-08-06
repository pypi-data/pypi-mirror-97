from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10)

    def test_1(self):
        # with self.assertRaises(ValueError):
        self.ft.generate_children(number_of_children=0)
        result = [None]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_2(self):
        ft = self.ft
        ft.generate_children(number_of_children=1)
        result = [3]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_3(self):
        ft = self.ft
        ft.generate_children(number_of_children=2)
        result = [3, 2]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_4(self):
        ft = self.ft
        ft.generate_children(number_of_children=3)
        result = [3, 1, 2]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_5(self):
        ft = self.ft
        with self.assertRaises(ValueError):
            ft.generate_children(number_of_children=4)

    def test_6(self):
        ft = self.ft
        ft.generate_children(number_of_children=(1, 1, 1))
        result = [[3], [3], [3]]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_7(self):
        ft = self.ft
        ft.generate_children(number_of_children=(0, 1, 2))
        result = [[2, 3], 1, [3]]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_8(self):
        ft = self.ft
        ft.generate_children(number_of_children=(1, 2, (1, 2, 3)))
        result = [
            [[3], [2, 3], [3, 1, 2]],
            [3],
            [2, 3]
        ]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_9(self):
        ft = self.ft
        ft.generate_children(
            number_of_children=(
                (1, 3),
                2,
                (1,
                 (1, 3),
                 3)
            )
        )
        result = [
            [
                [3],
                [
                    [3],
                    [2, 3, 1]
                ],
                [3, 1, 2]
            ],
            [
                [3, 1, 2],
                [3]
            ],
            [2, 3]
        ]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_10(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5))
        ft.generate_children(mode='merge', number_of_children=2)
        test_case = ft.get_leaves(key=lambda leaf: float(leaf.value))
        expected = [8.214285714285714, 1.7857142857142858]
        self.assertEqual(expected, test_case)

    def test_11(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5))
        output = []
        for i in range(7):
            ft_copy = ft.__deepcopy__()
            ft_copy.generate_children(mode='merge', number_of_children=2, merge_index=i)
            output.append(ft_copy.get_leaves(key=lambda leaf: float(leaf.value)))
        test_case = output
        # ft.add_layer()
        # print(ft.get_leaves(key=lambda leaf: float(leaf.value)))
        # print(output)
        expected = [[8.214285714285714, 1.7857142857142858],
                    [0.7142857142857143, 9.285714285714286],
                    [2.857142857142857, 7.142857142857143],
                    [4.285714285714286, 5.714285714285714],
                    [4.642857142857143, 5.357142857142857],
                    [5.714285714285714, 4.285714285714286],
                    [8.214285714285714, 1.7857142857142858]]
        self.assertEqual(expected, test_case)
