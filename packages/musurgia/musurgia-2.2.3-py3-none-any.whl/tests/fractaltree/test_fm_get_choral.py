import os

from musicscore.musictree.midi import C

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=20,
                               tempo=70)
        self.fm.midi_generator.midi_range = [36, 60]

    def test_1(self):
        self.fm.add_layer()
        score = self.fm.get_score(layer_number=1)

        for leaf in self.fm.traverse_leaves():
            leaf.set_chord(leaf.get_choral(range_factor=1.5, direction=1, last=True))

        sf = self.fm.get_simple_format()

        v = sf.to_stream_voice(1)
        v.add_to_score(score, 1, 2)

        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)

        self.assertCompareFiles(actual_file_path=xml_path)

    def test_2(self):
        self.fm.midi_generator.midi_range = [C(4).value, C(6).value]
        self.fm.midi_generator.directions = [1, -1, 1]
        self.fm.add_layer()
        score = self.fm.get_score(layer_number=1)

        for leaf in self.fm.traverse_leaves():
            leaf.set_chord(leaf.get_choral(range_factor=1, direction=1, last=False))
        sf = self.fm.get_simple_format()

        v = sf.to_stream_voice(1)
        v.add_to_score(score, 1, 2)

        for leaf in self.fm.traverse_leaves():
            leaf.add_layer()

        sf = self.fm.get_simple_format()

        v = sf.to_stream_voice(1)
        v.add_to_score(score, 1, 3)

        xml_path = path + '_test_2.xml'
        score.write(path=xml_path)

        self.assertCompareFiles(actual_file_path=xml_path)

    def test_3(self):
        fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
                          quarter_duration=30, tempo=80)
        fm.midi_generator.midi_range = (60, 72)
        fm.midi_generator.microtone = 4
        fm.add_layer()
        fm.quantize_children(grid_size=1)
        expected = [child.get_choral_midis() for child in fm.get_children()]
        actual = [child.get_choral_midis() for child in fm.get_children()]
        self.assertEqual(expected, actual)
