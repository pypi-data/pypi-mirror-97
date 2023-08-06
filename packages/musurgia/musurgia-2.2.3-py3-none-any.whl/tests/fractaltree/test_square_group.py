from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusicsquare import SquareGroup, Square


class Test(TestCase):
    def setUp(self) -> None:
        self.square_group = SquareGroup(
            Square(duration=10, name='red', tree_permutation_order=(3, 1, 2), proportions=(1, 2, 3)),
            Square(duration=10, name='blue', tree_permutation_order=(3, 1, 2), proportions=(1, 2, 3)),
            Square(duration=10, name='green', tree_permutation_order=(3, 1, 2), proportions=(1, 2, 3)),
        )

    def test_1(self):
        expected = self.square_group.squares[0].rows + self.square_group.squares[1].rows + self.square_group.squares[2].rows
        result = self.square_group.get_all_rows()
        self.assertEqual(expected, result)
