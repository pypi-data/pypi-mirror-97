import os
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.fractaltree.fractalmusic import FractalMusic, MergeTempoException
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=(1, 2, 3, 4, 5), tree_permutation_order=(3, 5, 1, 2, 4))
        self.fm.duration = 10
        self.fm.midi_generator.midi_range = [60, 72]

    def test_1(self):
        fm = self.fm
        fm.add_layer()
        fm.tempo = 60
        for ch in fm.get_children():
            ch.chord.add_words(ch.fractal_order)

        score = TreeScoreTimewise()
        fm.get_simple_format().to_stream_voice().add_to_score(score)

        fm.merge_children(2, 1, 2)
        # print(fm.get_leaves(key=lambda leaf: leaf.index))
        # print(fm.get_leaves(key=lambda leaf: leaf.fractal_order))
        # print(fm.get_leaves(key=lambda leaf: round(float(leaf.value), 2)))
        # print(fm.get_leaves(key=lambda leaf: round(float(leaf.duration), 2)))
        # print(fm.get_leaves(key=lambda leaf: round(float(leaf.chord.quarter_duration), 2)))
        fm.get_simple_format().to_stream_voice().add_to_score(score, part_number=2)
        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
        # # ft.add_layer()
        # # print(ft.get_leaves(key=lambda leaf: leaf.index))
        # # print(ft.get_leaves(key=lambda leaf: leaf.fractal_order))
        # # print(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)))
        # ft.merge_children(1, 2, 2)
        # # print(ft.get_leaves(key=lambda leaf: leaf.index))
        # self.assertEqual(ft.get_leaves(key=lambda leaf: leaf.fractal_order), [3, 5, 2])
        # self.assertEqual(ft.get_leaves(key=lambda leaf: round(float(leaf.value), 2)), [2.0, 4.0, 4.0])

    def test_2(self):
        self.fm.duration = 20
        self.fm.add_layer()
        self.fm.get_children()[1].tempo = 72
        self.fm.set_none_tempi(60)
        with self.assertRaises(MergeTempoException):
            self.fm.merge_children(2, 1, 2)
