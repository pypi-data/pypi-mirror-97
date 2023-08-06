import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def test_1(self):
        fm = FractalMusic(tempo=60, proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=100)
        fm.midi_generator.midi_range = [60, 79]
        fm.add_layer()
        partial_fm = fm.get_leaves()[3]
        partial_fm.add_layer()
        for leaf in partial_fm.traverse():
            leaf.chord.add_lyric(leaf.fractal_order)
            leaf.chord.add_words(leaf.midi_generator.midi_range)
            # leaf.chord.add_words(leaf.midi_generator.directions, relative_y=30)
        # print([leaf.fractal_order for leaf in partial_fm.traverse_leaves()])
        score = TreeScoreTimewise()
        v = partial_fm.get_simple_format(0).to_stream_voice(1)
        v.add_to_score(score, 1, 1)

        v = partial_fm.get_simple_format().__deepcopy__().to_stream_voice(1)
        v.add_to_score(score, 1, 2)

        partial_fm.reduce_children(condition=lambda child: child.fractal_order > 2)
        v = partial_fm.get_simple_format().__deepcopy__().to_stream_voice(1)
        v.add_to_score(score, 1, 3)

        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    # def test_3(self):
    #     fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], duration=100)
    #     fm.midi_generator.midi_range = [60, 79]
    #     fm.midi_generator.directions = [1, 1, -1]
    #     fm.add_layer()
    #     print(fm.children_generated_midis)
    #     print(fm.children_fractal_values)
    #     fm.reduce_children(lambda child: child.fractal_order == 2)
    #     print(fm.children_fractal_values)
    #     print(fm.midi_generator.proportions)
    #     print(fm.midi_generator.directions)
    #     print(fm.children_generated_midis)
    #     print(fm.proportions)
    #     fm.add_layer()
    #     print([leaf.fractal_order for leaf in fm.traverse_leaves()])

    # print([leaf.fractal_order for leaf in fm.traverse_leaves()])
    #
    # fm.reduce_leaves(lambda leaf: leaf.fractal_order == 2)
    # print([leaf.midi_value for leaf in fm.traverse_leaves()])

    # def test_4(self):
    #     permutation_order = [8, 11, 7, 12, 10, 13, 9, 4, 1, 3, 6, 2, 5]
    #     fm = FractalMusic(tree_permutation_order=permutation_order, duration=900, proportions=list(range(1, 14)))
    #     fm.midi_generator.midi_range = [48, 84]
    #     fm.midi_generator.directions = [1, 1, -1, -1]
    #     fm.add_layer()
    #     part_fm = fm.get_children()[6]
    #     part_fm.add_layer()
    #     print([child.fractal_order for child in part_fm.get_children()])
    #     part_fm.reduce_children(lambda child: child.fractal_order < 5)
    #     print([child.fractal_order for child in part_fm.get_children()])
    #     print([round(float(duration), 2) for duration in part_fm.simple_format.durations])

    # fm.reduce_leaves(lambda leaf: leaf.fractal_order == 2)

    def test_5(self):
        score = TreeScoreTimewise()

        fm = FractalMusic(tempo=60, proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=20)
        fm.midi_generator.midi_range = [60, 79]
        fm.midi_generator.microtone = 4
        fm.add_layer()

        for child in fm.get_children():
            child.chord.add_lyric(child.fractal_order)

        simple_format = fm.get_simple_format(1)
        v = simple_format.to_stream_voice(1)
        v.add_to_score(score, 1, 1)

        fm.reduce_children(lambda child: child.fractal_order in [1])

        simple_format = fm.get_simple_format(1)
        v = simple_format.to_stream_voice(1)
        v.add_to_score(score, 1, 2)

        fm.add_layer()

        for leaf in fm.traverse_leaves():
            leaf.chord.add_lyric(leaf.fractal_order)
            # leaf.chord.add_words(leaf.midi_generator.midi_range[1])

        simple_format = fm.get_simple_format(2)
        v = simple_format.to_stream_voice(1)
        v.add_to_score(score, 1, 3)

        text_path = path + '_test_5.txt'
        fm.write_infos(text_path)
        self.assertCompareFiles(actual_file_path=text_path)

        xml_path = path + '_test_5.xml'
        score.max_division = 7
        score.write(xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    def test_6(self):
        fm = FractalMusic(reading_direction='vertical', tempo=120, value=1.5, proportions=(1, 2, 3, 4, 5, 6, 7),
                          tree_permutation_order=(2, 6, 4, 1, 3, 7, 5), multi=(1, 4))
        fm.midi_generator.midi_range = (62, 70)
        fm.add_layer()
        # fm.generate_children(number_of_children=1)
        fm.reduce_children(lambda child: child.fractal_order < 7)
        result = fm.get_children()[0].midi_generator.midi_range
        # not [62, 70] because of directions ([-1, ...])
        expected = [70, 62]
        self.assertEqual(expected, result)
