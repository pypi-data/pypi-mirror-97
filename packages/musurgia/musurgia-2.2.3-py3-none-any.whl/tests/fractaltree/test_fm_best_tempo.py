import os

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], duration=10.4)

    def test_1(self):
        self.fm.tempo = self.fm.find_best_tempo_in_range()
        self.assertEqual(10.4, self.fm.duration)

    def test_2(self):
        self.fm.tempo = self.fm.find_best_tempo_in_range()
        self.fm.change_quarter_duration(round(self.fm.quarter_duration))
        self.assertEqual(13, self.fm.quarter_duration)

    def test_3(self):
        self.fm.add_layer()
        for child in self.fm.get_children():
            best_tempo = child.find_best_tempo_in_range()
            child.tempo = best_tempo
        # print([leaf.quarter_duration for leaf in self.fm.get_children()])
        self.fm.round_leaves()
        result = [4.0, 1.0, 7.0, 2.0]
        self.assertEqual(result, [child.quarter_duration for child in self.fm.get_children()])

    def test_4(self):
        self.fm.add_layer()
        for child in self.fm.get_children():
            best_tempo = child.find_best_tempo_in_range()
            child.tempo = best_tempo
        self.fm.round_leaves()
        xml_path = path + '_test_4.xml'
        score = self.fm.get_children_score()
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        best_tempi = self.fm.find_best_tempi_in_list(tempi=[50, 60, 70, 80, 90, 100])
        self.assertEqual([70, 80], best_tempi)

