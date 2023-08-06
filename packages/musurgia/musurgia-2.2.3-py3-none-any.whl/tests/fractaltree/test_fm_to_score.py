import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic, SetTempoFirstException

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):

    def setUp(self) -> None:
        self.fm = FractalMusic(tempo=60, quarter_duration=12, tree_permutation_order=(3, 1, 2), proportions=[1, 2, 3])
        self.fm.midi_generator.set_directions(1, 1, -1)
        self.fm.midi_generator.midi_range = [55, 72]

    def test_1(self):
        fm = self.fm
        fm.add_layer()

        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        # for node in fm.traverse():
        #     node.chord.add_words(node.midi_generator.midi_range)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)

        # for node in fm.traverse():
        #     node.chord.add_words(node.children_generated_midis)
        #     node.chord.add_words(node.midi_generator.directions, relative_y=30)
        #     node.chord.add_words(node.children_generated_midis)
        #     node.chord.add_words(node.permutation_order, relative_y=60)

        score = TreeScoreTimewise()
        score = fm.get_score(score=score, show_fractal_orders=False)

        text_path = path + '_test_1.txt'
        fm.write_infos(text_path)
        self.assertCompareFiles(actual_file_path=text_path)

        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    def test_2(self):
        fm = self.fm
        fm.add_layer()
        score_1 = fm.get_children()[0].get_score()
        xml_path = path + '_test_2.xml'
        score_1.write(path=xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    def test_3(self):
        fm = FractalMusic(duration=30)
        fm.add_layer()
        with self.assertRaises(SetTempoFirstException):
            fm.get_score()

    def test_4(self):
        fm = FractalMusic(duration=30)
        fm.add_layer()
        fm.get_children()[1].tempo = 72
        fm.set_none_tempi(80)
        fm.quantize_leaves(0.5)
        fm.add_layer()
        score = fm.get_root_score(layer_number=1, show_fractal_orders=True)
        xml_path = path + '_test_4.xml'
        score.write(path=xml_path)
        with self.assertRaises(SetTempoFirstException):
            fm.get_score()
