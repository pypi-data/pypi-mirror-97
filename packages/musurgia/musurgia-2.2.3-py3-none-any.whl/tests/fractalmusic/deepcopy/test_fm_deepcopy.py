import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        fm = FractalMusic(tempo=60, quarter_duration=10, reading_direction='vertical')
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
        self.assertNotEqual(self.deep_copied.name, self.fm.name)

    def test_3(self):
        for leaf in self.fm.traverse_leaves():
            leaf.chord.add_words(leaf.fractal_order)

        copied = self.fm.__deepcopy__()
        copied.get_simple_format().to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        expected_path = path + '_test_3_expected.xml'
        expected_score = TreeScoreTimewise()
        self.fm.get_simple_format().to_stream_voice().add_to_score(expected_score)
        expected_score.write(expected_path)
        self.assertCompareFiles(xml_path, expected_path)
