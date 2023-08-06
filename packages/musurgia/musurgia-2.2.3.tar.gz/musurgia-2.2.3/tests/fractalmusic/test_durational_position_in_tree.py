from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.unittest import TestCase


class Test(TestCase):
    def test_get_durational_position_in_tree(self):
        fm = FractalMusic(duration=10)
        fm.add_layer()
        actual = fm.get_children()[2].durational_position_in_tree
        expected = sum(ch.duration for ch in fm.get_children()[:2])
        self.assertEqual(expected, actual)
