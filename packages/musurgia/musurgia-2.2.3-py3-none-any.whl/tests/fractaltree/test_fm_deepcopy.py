from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic


class Test(TestCase):
    def setUp(self) -> None:
        fm = FractalMusic(value=10, reading_direction='vertical')
        fm.add_layer()
        fm.add_layer()
        self.fm = fm.get_children()[1]
        self.deep_copied = self.fm.__deepcopy__()

    def test(self, exp=None, act=None):
        if not exp:
            exp = self.fm

        if not act:
            act = self.deep_copied

        self.assertEqual(exp.value, act.value)
        self.assertEqual(exp.proportions, act.proportions)
        self.assertEqual(exp.value, act.value)
        self.assertEqual(exp.proportions, act.proportions)
        self.assertEqual(exp.tree_permutation_order, act.tree_permutation_order)
        self.assertEqual(exp.fractal_order, act.fractal_order)
        self.assertEqual(exp.reading_direction, act.reading_direction)
        self.assertEqual(exp._name, act._name)

        self.assertEqual(exp.tree_directions, act.tree_directions)
        self.assertEqual(exp.tempo, act.tempo)
        self.assertEqual(exp.midi_value, act.midi_value)

    def test_1(self):
        self.assertIsNone(self.deep_copied.up)

    def test_2(self):
        self.assertNotEqual(self.deep_copied.__name__, self.fm.__name__)
