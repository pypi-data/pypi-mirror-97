from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic
import os

path = os.path.abspath(__file__).split(".")[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=[1, 2, 3], tree_permutation_order=(3, 1, 2), duration=10)

    def test_1(self):
        self.fm.midi_generator.set_directions(1, -1, -1)
        self.assertEqual([1, -1, -1], self.fm.midi_generator.directions)
        self.assertEqual([-1, -1, 1], self.fm.tree_directions)
        self.fm.add_layer()
        # for node in self.fm.get_children():
        #     print(node.__name__)
        #     print(node.multi)
        #     print(node.permutation_order)
        #
        # text_path = path + '_test_1.txt'
        #
        # self.fm.write_infos(text_path)
        directions = [leaf.midi_generator.directions for leaf in self.fm.traverse_leaves()]

        self.assertEqual([[-1, -1, 1], [1, -1, -1], [-1, 1, -1]], directions)

    def test_2(self):
        self.fm.tree_directions = [1, 1, -1]
        self.fm.midi_generator.midi_range = [60, 70]
        self.fm.add_layer()
        directions = [leaf.midi_generator.directions for leaf in self.fm.traverse_leaves()]
        self.fm.add_layer()
        midis = [leaf.midi_value for leaf in self.fm.traverse_leaves()]
        self.assertEqual([[1, 1, -1], [-1, 1, 1], [1, -1, 1]], directions)
        self.assertEqual([60.0, 63.0, 70.0, 63.0, 60.0, 61.0, 65.0, 70.0, 63.0], midis)

    def test_3(self):
        self.fm.tree_directions = [1, 1, -1]
        self.fm.midi_generator.midi_range = [60, 70]
        self.fm.permute_directions = False
        self.fm.add_layer()
        self.fm.add_layer()
        midi_ranges = [[leaf.midi_generator.midi_range for leaf in child.get_leaves()] for child in
                       self.fm.get_children()]
        result = [[[60.0, 63.0], [63.0, 70.0], [70.0, 60.0]], [[60.0, 62.0], [62.0, 63.0], [63.0, 61.0]],
                  [[63.0, 66.0], [66.0, 70.0], [70.0, 69.0]]]

        self.assertEqual(result, midi_ranges)
