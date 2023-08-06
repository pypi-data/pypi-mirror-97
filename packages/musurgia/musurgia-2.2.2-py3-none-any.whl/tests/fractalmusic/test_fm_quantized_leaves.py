import os
from unittest import TestCase

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.fractaltree.fractalmusic import FractalMusic

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        fm = FractalMusic(proportions=[1, 2, 3], tree_permutation_order=[3, 1, 2], duration=12, tempo=72)
        fm.quarter_duration = round(fm.quarter_duration)
        fm.add_layer()
        quarter_durations = [float(leaf.quarter_duration) for leaf in fm.traverse_leaves()]
        # print(quarter_durations)
        # print(sum(quarter_durations))
        fm.quantize_leaves(grid_size=0.5)
        quarter_durations = [float(leaf.quarter_duration) for leaf in fm.traverse_leaves()]
        self.assertEqual(quarter_durations, [7.0, 2.5, 4.5])
        # print([leaf.chord.quarter_duration for leaf in fm.traverse_leaves()])
