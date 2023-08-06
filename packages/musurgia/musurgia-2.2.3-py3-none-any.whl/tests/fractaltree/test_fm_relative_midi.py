import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):

    def setUp(self) -> None:
        self.fm = FractalMusic(tempo=60, quarter_duration=12, tree_permutation_order=(3, 1, 4, 2),
                               proportions=[1, 2, 3, 4],
                               multi=(1, 1))
        self.fm.midi_generator.midi_range = [55, 55 + 24]
        self.fm.midi_generator.microtone = 4

    def add_infos(self, fm):
        for leaf in fm.traverse_leaves():
            leaf.chord.add_lyric(leaf.fractal_order, relative_y=20)
            leaf.chord.add_words(round(float(leaf.quarter_duration), 2), relative_y=30)
            leaf.chord.add_words(leaf.chord.midis[0].value, relative_y=50)

    def test_1(self):

        self.fm.midi_generator.set_directions(1, 1, 1, 1)
        self.fm.add_layer()

        self.add_infos(self.fm)
        self.fm.add_layer()
        self.add_infos(self.fm)
        score = TreeScoreTimewise()
        score.page_style.staff_distance = 150

        for layer in range(self.fm.number_of_layers + 1):
            sf = self.fm.get_simple_format(layer=layer)
            v = sf.to_stream_voice(1)
            v.add_to_score(score, 1, layer + 1)

        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    # def test_2(self):
    #     self.fm.midi_generator.directions = [1]
    #     self.fm.add_layer()
    #     print([round(float(chord.quarter_duration), 2) for chord in self.fm.simple_format.chords])
    #     print(basic_functions.xToD(self.fm.children_generated_midis))
    #     print(basic_functions.xToD([chord.midis[0].value for chord in self.fm.simple_format.chords]))
    #
    # def test_3(self):
    #     self.fm.midi_generator.directions = [1]
    #     self.fm.add_layer()
    #     self.fm.add_layer()
    #
    #     for node in self.fm.get_children():
    #         print([round(float(chord.quarter_duration), 2) for chord in node.simple_format.chords])
    #         print(basic_functions.xToD(node.children_generated_midis))
    #         print(basic_functions.xToD([chord.midis[0].value for chord in node.simple_format.chords]))
    #
    # def test_4(self):
    #     def print_infos(node):
    #         print(node.fractal_order)
    #         print('directions', node.midi_generator.directions)
    #         print('durations', [round(float(v), 2) for v in node.children_fractal_values])
    #         print('midis', node.children_generated_midis)
    #         print('intervals', basic_functions.xToD(node.children_generated_midis))
    #
    #     self.fm.midi_generator.directions = [1]
    #     self.fm.add_layer()
    #
    #     print_infos(self.fm)
    #
    #     for leaf in self.fm.traverse_leaves():
    #         print_infos(leaf)
    #
    #     self.fm.add_layer()
    #     for leaf in self.fm.traverse_leaves():
    #         print_infos(leaf)

    # def test_5(self):
    #     def print_infos(node):
    #         print(node.fractal_order)
    #         print('directions', node.midi_generator.directions)
    #         print('durations', [round(float(v), 2) for v in node.children_fractal_values])
    #         print('midis', node.children_generated_midis)
    #         print('intervals', basic_functions.xToD(node.children_generated_midis))
    #
    #     self.fm.midi_generator.directions = [1, -1]
    #     self.fm.add_layer()
    #
    #     print_infos(self.fm)
    #
    #     for leaf in self.fm.traverse_leaves():
    #         print_infos(leaf)
    #
    #     self.fm.add_layer()
    #     for leaf in self.fm.traverse_leaves():
    #         print_infos(leaf)
    #
    # def test_6(self):
    #     permutation_order = [8, 11, 7, 12, 10, 13, 9, 4, 1, 3, 6, 2, 5]
    #     fm = FractalMusic(tree_permutation_order=permutation_order, duration=900, proportions=list(range(1, 14)))
    #     fm.midi_generator.midi_range = [48, 84]
    #     fm.midi_generator.directions = [1, 1, -1, -1]
    #
    #     def print_infos(node):
    #         print(node.fractal_order)
    #         # print('directions', node.midi_generator.directions)
    #         durations = [round(float(v), 2) for v in node.children_fractal_values]
    #         # print('durations', durations)
    #         # print('midis', node.children_generated_midis)
    #         intervals = [round(float(v), 2) for v in basic_functions.xToD(node.children_generated_midis)]
    #         # print('intervals', intervals)
    #         print('durations,intervals',
    #               [(duration, interval) for duration, interval in zip(durations, intervals)])
    #         # print('durations/intervals',
    #         #       [Fraction(duration, interval) for duration, interval in zip(durations, intervals)])
    #
    #     fm.add_layer()
    #
    #     # print_infos(fm)
    #
    #     for leaf in fm.traverse_leaves():
    #         print_infos(leaf)
    #
    #     # self.fm.add_layer()
    #     # for leaf in self.fm.traverse_leaves():
    #     #     print_infos(leaf)

    def test_7(self):
        fm = FractalMusic(tempo=60, proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=20)
        fm.midi_generator.midi_range = [60, 79]
        fm.add_layer()
        fm.chord.add_words(fm.midi_generator.midi_range)

        for child in fm.get_children():
            child.chord.add_lyric(child.fractal_order)
            child.chord.add_words(child.midi_generator.midi_range)

        for index, node in enumerate(fm.get_children()):
            node.midi_generator.midi_range = [60 - index, 72 - index]

        fm.add_layer()
        for leaf in fm.traverse_leaves():
            leaf.chord.add_lyric(leaf.fractal_order)

        score = TreeScoreTimewise()

        for layer_number in range(0, fm.number_of_layers + 1):
            simple_format = fm.get_simple_format(layer_number)

            v = simple_format.to_stream_voice(1)
            v.add_to_score(score, 1, layer_number + 1)

        xml_path = path + '_test_7.xml'
        score.accidental_mode = 'normal'
        score.write(xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    def test_8(self):
        fm = FractalMusic(proportions=[1, 2, 3, 4, 5, 6, 7], tree_permutation_order=[3, 6, 1, 5, 7, 2, 4])
        fm.tempo = 60
        fm.quarter_duration = 350
        fm.midi_generator.midi_range = [60, 72]
        fm.midi_generator.microtone = 4
        fm.tree_directions = [1, 1, -1, -1]

        fm.add_layer()
        fm.round_leaves()

        partial = fm.get_children()[6]
        partial.add_layer()
        partial.reduce_children(lambda ch: ch.fractal_order > partial.fractal_order)
        partial.round_leaves()

        result = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.assertEqual(result, [node.midi_generator.microtone for node in fm.traverse()])

    def test_9(self):
        fm = FractalMusic(proportions=[1, 2, 3, 4, 5, 6, 7], tree_permutation_order=[3, 6, 2, 5, 1, 7, 4])

        fm.multi = (7, 4)
        fm.tempo = 60
        fm.quarter_duration = 70

        fm.midi_generator.microtone = 4
        # fm.quantize_leaves(0.5)
        fm.midi_generator.directions = [1, -1, 1, -1, 1, -1, 1]

        fm.midi_generator.midi_range = [36, 56]
        fm.add_layer()

        fm.reduce_children(lambda child: child.fractal_order > 4)
        fm.quantize_leaves(0.5)
        fm.get_children()[3].add_layer()
        fm.get_children()[3].reduce_children(lambda child: child.fractal_order > 4)
        for node in fm.traverse():
            node.chord.add_words(node.midi_value)
        text_path = path + '_test_9.txt'
        fm.write_infos(text_path)
        self.assertCompareFiles(actual_file_path=text_path)

        score = fm.get_score()
        xml_path = path + '_test_9.xml'
        score.write(xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    def test_10(self):
        fm = FractalMusic(proportions=[1, 2, 3], tree_permutation_order=[3, 1, 2])
        fm.tempo = 60
        fm.duration = 10
        fm.midi_generator.midi_range = (60, 72)
        fm.permute_directions = True
        fm.midi_generator.set_directions(-1, 1, -1)

        fm.add_layer()

        for node in fm.traverse():
            node.chord.add_lyric(node.midi_generator.directions)
            node.chord.add_words(node.children_generated_midis, relative_y=30)
            node.chord.add_words(node.midi_generator.midi_range, relative_y=60)

        fm.add_layer()

        score = TreeScoreTimewise()
        score.accidental_mode = 'modern'
        score = fm.get_score(score)
        score.page_style.staff_distance = 150
        xml_path = path + '_test_10.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
