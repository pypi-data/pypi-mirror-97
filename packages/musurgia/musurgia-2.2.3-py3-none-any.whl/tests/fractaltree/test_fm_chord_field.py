import os
from itertools import cycle
from math import ceil

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction

from musurgia.agunittest import AGTestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.basic_functions import slice_list
from musurgia.chordfield.chordfield import ChordField, Breathe
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.interpolation import Interpolation, RandomInterpolation

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        fm = FractalMusic(quarter_duration=20, tempo=80)
        fm.midi_generator.midi_range = [60, 84]
        fm.add_layer()
        sorted_children = sorted(fm.get_children(), key=lambda child: child.fractal_order)
        chord_field = ChordField(
            quarter_duration=10,
            duration_generator=ValueGenerator(ArithmeticProgression(a1=0.2, an=2)),
            midi_generator=ValueGenerator(Interpolation(start=84, end=60,
                                                        key=lambda midi: round(midi * 2) / 2)),
            short_ending_mode='add_rest'
        )
        sorted_children[-1].chord_field = chord_field
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        def add_chord_field(child):
            child.chord_field = ChordField(duration_generator=ValueGenerator(ArithmeticProgression(a1=0.2, an=2)),
                                           midi_generator=ValueGenerator(
                                                Interpolation(start=child.midi_generator.midi_range[0],
                                                              end=child.midi_generator.midi_range[1],
                                                              duration=None,
                                                              key=lambda
                                                                  midi: round(midi * 2) / 2)),
                                           short_ending_mode='stretch')

        fm = FractalMusic(quarter_duration=20, tempo=80, proportions=[1, 2, 3, 4, 5],
                          tree_permutation_order=[3, 1, 5, 2, 4])
        fm.midi_generator.midi_range = [60, 84]
        fm.add_layer()
        sorted_children = sorted(fm.get_children(), key=lambda child: child.fractal_order)
        add_chord_field(sorted_children[-1])

        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        # node.chord_fields are part of a group
        cfg = ChordField(
            duration_generator=ValueGenerator(RandomInterpolation(start=[0.25, 0.25], end=[0.75, 1], seed=20)))
        cf_1 = ChordField(
            midi_generator=ValueGenerator(cycle([60])))
        cf_2 = ChordField(
            midi_generator=ValueGenerator(cycle([72])),
            long_ending_mode='cut')

        cfg.add_child(cf_1)
        cfg.add_child(cf_2)

        fm = FractalMusic(quarter_duration=20, tempo=80)
        fm.add_layer()
        fm.get_children()[0].chord_field = cf_1
        fm.get_children()[1].chord_field = cf_2
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + 'test_3.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        cf_1 = ChordField(
            quarter_duration=10,
            midi_generator=ValueGenerator(cycle([60, 61, 64, 66])),
            long_ending_mode='self_extend',
            short_ending_mode='self_shrink'
        )
        cf_2 = ChordField(
            quarter_duration=3,
            midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
            long_ending_mode='self_extend',
            short_ending_mode='self_shrink'
        )

        breathe_unit = Fraction(1, 5)
        breathe_breakpoints = (5 * breathe_unit, breathe_unit, 5 * breathe_unit)
        breathe_proportions = [2, 4, 1, 7, 2]

        breathe = Breathe(proportions=breathe_proportions,
                          quarter_duration=13,
                          breakpoints=breathe_breakpoints)
        cfg = ChordField(duration_generator=breathe.duration_generator)
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)

        simple_format = SimpleFormat()
        simple_format.extend(cf_1.simple_format)
        simple_format.extend(cf_2.simple_format)

        self.score.set_time_signatures(ceil(simple_format.quarter_duration))
        simple_format.to_stream_voice().add_to_score(self.score)
        xml_path = path + 'test_4.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        # node.chord_fields are part of a breathe group
        fm = FractalMusic(quarter_duration=20, tempo=80)
        fm.add_layer()
        fm.quantize_children(grid_size=1)

        node_groups = slice_list(fm.get_children(), (2, 1))

        cf_1 = ChordField(
            midi_generator=ValueGenerator(cycle([60, 61, 64, 66])),
            long_ending_mode='self_extend',
            short_ending_mode='self_shrink'
        )
        cf_2 = ChordField(
            midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
            long_ending_mode='self_extend',
            short_ending_mode='self_shrink'
        )

        breathe_unit = Fraction(1, 5)
        breathe_breakpoints = (5 * breathe_unit, breathe_unit, 5 * breathe_unit)
        breathe_proportions = [2, 4, 1, 7, 2]

        breathe = Breathe(proportions=breathe_proportions,
                          quarter_duration=sum([node.chord.quarter_duration for node in node_groups[0]]),
                          breakpoints=breathe_breakpoints)

        cfg = ChordField(duration_generator=breathe.duration_generator)
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)

        fm.get_children()[0].chord_field = cf_1
        fm.get_children()[1].chord_field = cf_2
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + 'test_5.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
