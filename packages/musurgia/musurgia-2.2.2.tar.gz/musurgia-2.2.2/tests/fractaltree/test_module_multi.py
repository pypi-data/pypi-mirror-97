import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.fractaltree.fractalmusicsquare import Square

path = str(os.path.abspath(__file__).split('.')[0])


def set_tempo(square):
    for module in square.get_all_modules():
        module.tempo = 72


def add_info(module):
    for index, leaf in enumerate(module.traverse_leaves()):
        leaf.chord.add_lyric(leaf.fractal_order)
        if index == 0:
            leaf.chord.add_words(module.multi)


def generate_score(modules):
    score = TreeScoreTimewise()
    for index, module in enumerate(modules):
        module.get_simple_format(
            layer=module.number_of_layers
        ).to_stream_voice().add_to_score(score=score, part_number=index + 1)

    score.finish()
    partwise = score.to_partwise()
    return partwise


def forward_multi(module, multi_addition):
    m1, m2 = module.multi
    module.multi = (m1, m2 + multi_addition)


class Test(TestCase):
    def setUp(self) -> None:
        self.square = Square(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2), duration=40)
        set_tempo(self.square)
        self.copied_square = self.square.__deepcopy__()

    def test_1(self):
        modules = [self.square.get_module(2, 2), self.copied_square.get_module(2, 2)]
        for module in modules:
            module.add_layer()

        for module in modules:
            add_info(module)

        xml_path = path + '_test_1.xml'
        generate_score(modules).write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        modules = [self.square.get_module(2, 2), self.copied_square.get_module(2, 2)]
        multi_additions = [0, 1]
        for module, multi_addition in zip(modules, multi_additions):
            forward_multi(module, multi_addition)
        for module in modules:
            module.add_layer()

        for module in modules:
            add_info(module)

        xml_path = path + '_test_2.xml'
        generate_score(modules).write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        modules = [self.square.get_module(2, 2), self.copied_square.get_module(2, 2)]
        for module in modules:
            module.children_fractal_values
        multi_additions = [0, 1]
        for module, multi_addition in zip(modules, multi_additions):
            forward_multi(module, multi_addition)
        for module in modules:
            module.add_layer()

        for module in modules:
            add_info(module)

        xml_path = path + '_test_3.xml'
        generate_score(modules).write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        fm_1 = FractalMusic(multi=(1, 2), tempo=60, quarter_duration=10)
        fm_2 = FractalMusic(multi=(1, 1), tempo=60, quarter_duration=10)
        fms = [fm_1, fm_2]

        for fm in fms:
            fm.midi_generator.midi_range = [60, 72]

        fm_2.multi = fm_1.multi

        self.assertEqual(fm_2.children_fractal_values, fm_1.children_fractal_values)
        self.assertEqual(fm_2.children_fractal_orders, fm_1.children_fractal_orders)
        self.assertEqual(fm_2.midi_generator.midi_range, fm_1.midi_generator.midi_range)
        self.assertEqual(fm_2.children_generated_midis, fm_1.children_generated_midis)
