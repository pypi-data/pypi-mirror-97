import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.fm_3 = FractalMusic(value=10)
        self.fm_3.tempo = 60

        self.fm_7 = FractalMusic(value=30, proportions=(1, 2, 3, 4, 5, 6, 7),
                                 tree_permutation_order=(3, 1, 6, 5, 7, 4, 2))
        self.fm_7.tempo = 72

    def test_1(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=0)
        score = fm.get_score(show_fractal_orders=True)
        score = fm.get_score()
        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=1)
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=2)
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_3.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=3)
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_4.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        fm = self.fm_3
        with self.assertRaises(ValueError):
            fm.generate_children(number_of_children=4)

    def test_6(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=(1, 1, 1))
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_6.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=(0, 1, 2))
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_7.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=(1, 2, (1, 2, 3)))
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_8.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_9(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_9.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_10(self):
        fm = self.fm_3
        with self.assertRaisesRegex(expected_exception=ValueError, expected_regex="['reduce', 'merge']"):
            fm.generate_children(number_of_children=3, mode='bla')

    def test_11(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=3, mode='merge')
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_11.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_12(self):
        fm = self.fm_3
        fm.generate_children(number_of_children=2, mode='merge', merge_index=0)
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_12.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_13(self):
        fm = self.fm_7.__deepcopy__()
        fm.add_layer()
        score = fm.get_score(show_fractal_orders=True, layer_number=1)
        fm = self.fm_7.__deepcopy__()
        fm.generate_children(number_of_children=4, mode='merge', merge_index=5)
        for leaf in fm.traverse_leaves():
            leaf.chord.add_lyric(leaf.fractal_order)
        sf = fm.get_simple_format()
        sf.to_stream_voice().add_to_score(score, part_number=2)

        xml_path = path + '_test_13.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_14(self):
        fm = self.fm_7.__deepcopy__()
        fm.add_layer()
        score = fm.get_score(show_fractal_orders=True, layer_number=1)
        fm = self.fm_7.__deepcopy__()
        fm.generate_children(number_of_children=(4, 2), mode='merge', merge_index=5)

        for leaf in fm.traverse_leaves():
            leaf.chord.add_lyric(leaf.fractal_order)
        sf = fm.get_simple_format(layer=1)
        sf.to_stream_voice().add_to_score(score, part_number=2)
        sf = fm.get_simple_format(layer=2)
        sf.to_stream_voice().add_to_score(score, part_number=3)

        xml_path = path + '_test_14.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_15(self):
        self.fm_7.quarter_duration = 10
        score = TreeScoreTimewise()
        score.add_title('reduce backwards')
        score.page_style.orientation = 'portrait'
        score.set_time_signatures(barline_style='light-light', quarter_durations=self.fm_7.quarter_duration)
        for i in range(1, 8):
            fm = self.fm_7.__deepcopy__()
            fm.generate_children(number_of_children=i, mode='reduce_backwards')
            for leaf in fm.traverse_leaves():
                leaf.chord.add_lyric(leaf.fractal_order)
            sf = fm.get_simple_format(layer=fm.number_of_layers)
            sf.to_stream_voice().add_to_score(score, part_number=i)

        xml_path = path + '_test_15.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_16(self):
        self.fm_7.quarter_duration = 10
        score = TreeScoreTimewise()
        score.add_title('reduce forwards')
        score.page_style.orientation = 'portrait'
        score.set_time_signatures(barline_style='light-light', quarter_durations=self.fm_7.quarter_duration)
        for i in range(1, 8):
            fm = self.fm_7.__deepcopy__()
            fm.generate_children(number_of_children=i, mode='reduce_forwards')
            for leaf in fm.traverse_leaves():
                leaf.chord.add_lyric(leaf.fractal_order)
            sf = fm.get_simple_format(layer=fm.number_of_layers)
            sf.to_stream_voice().add_to_score(score, part_number=i)

        xml_path = path + '_test_16.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_17(self):
        self.fm_7.quarter_duration = 10
        score = TreeScoreTimewise()
        score.add_title('reduce sieve')
        score.page_style.orientation = 'portrait'
        score.set_time_signatures(barline_style='light-light', quarter_durations=self.fm_7.quarter_duration)
        for i in range(1, 8):
            fm = self.fm_7.__deepcopy__()
            fm.generate_children(number_of_children=i, mode='reduce_sieve')
            for leaf in fm.traverse_leaves():
                leaf.chord.add_lyric(leaf.fractal_order)
            sf = fm.get_simple_format(layer=fm.number_of_layers)
            sf.to_stream_voice().add_to_score(score, part_number=i)

        xml_path = path + '_test_17.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

