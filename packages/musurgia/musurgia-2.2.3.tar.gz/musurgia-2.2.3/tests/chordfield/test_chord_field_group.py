import os
from fractions import Fraction
from itertools import cycle
from math import ceil

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.random import Random
from musurgia.unittest import TestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordField, Breathe
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.interpolation import RandomInterpolation

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        # fields: midi_generators
        # group: no generators
        cfg = ChordField()
        cf_1 = ChordField(quarter_duration=3,
                          midi_generator=ValueGenerator(cycle([60, 61, 64, 66])),
                          duration_generator=ValueGenerator(cycle([1]))
                          )
        cf_2 = ChordField(quarter_duration=6,
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
                          duration_generator=ValueGenerator(cycle([1]))
                          )
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        xml_path = path + 'test_1.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        # fields: midi_generators
        # group: duration_generator with __next__
        cfg = ChordField(
            duration_generator=ValueGenerator(Random(pool=[0.2, 0.4, 0.8, 1.6], seed=10))
        )
        cf_1 = ChordField(quarter_duration=3,
                          midi_generator=ValueGenerator(cycle([60, 61, 64, 66])),
                          long_ending_mode='self_extend'
                          )
        cf_2 = ChordField(quarter_duration=6,
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
                          long_ending_mode='self_extend')

        # cfg = ChordFieldGroup(duration_generator=Random(pool=[0.2, 0.4, 0.8, 1.6], seed=10))
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        simple_format = cfg.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(cfg.quarter_duration))
        xml_path = path + 'test_2.xml'
        simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        # fields: both with midi_generators, one duration_generator
        # group: duration_generator with __next__ (Random)
        cfg = ChordField(
            duration_generator=ValueGenerator(Random(pool=[0.2, 0.4, 0.8, 1.6], seed=10))
        )

        cf_1 = ChordField(quarter_duration=3,
                          midi_generator=ValueGenerator(cycle([60, 61, 64, 66])),
                          duration_generator=ValueGenerator(cycle([1]))
                          )
        cf_2 = ChordField(quarter_duration=6,
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
                          long_ending_mode='cut'
                          )

        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        sf_1 = cf_1.simple_format
        sf_2 = cf_2.simple_format
        sf = SimpleFormat()
        sf.extend(sf_1)
        sf.extend(sf_2)
        xml_path = path + 'test_3.xml'
        # cfg.simple_format.to_stream_voice().add_to_score(self.score)
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        # fields: midi_generators, first one with ending_mode 'post'
        # group: duration_generator with __next__ (Arithmetic Progression)
        cfg = ChordField(
            duration_generator=ValueGenerator(ArithmeticProgression(a1=0.3, an=1.5, correct_s=True))
        )

        cf_1 = ChordField(quarter_duration=3,
                          midi_generator=ValueGenerator(cycle([60, 61, 64, 66])),
                          long_ending_mode='self_extend'
                          )
        cf_2 = ChordField(quarter_duration=6,
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
                          short_ending_mode='add_rest',

                          )
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        sf = SimpleFormat()
        sf.extend(cf_1.simple_format)
        sf.extend(cf_2.simple_format)
        xml_path = path + 'test_4.xml'
        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        # breathing manually
        times = [3, 7, 3, 10, 3]
        cf_1 = ChordField(quarter_duration=times[0],
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])))
        cf_2 = ChordField(quarter_duration=times[1],
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])))
        cf_3 = ChordField(quarter_duration=times[2],
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])))
        cf_4 = ChordField(quarter_duration=times[3],
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])))
        cf_5 = ChordField(quarter_duration=times[4],
                          midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])))
        points = [1.5, 0.2, 1.5]
        cf_1.duration_generator = ValueGenerator(ArithmeticProgression(a1=points[0], an=points[0], correct_s=True))
        cf_2.duration_generator = ValueGenerator(ArithmeticProgression(a1=points[0], an=points[1], correct_s=True))
        cf_3.duration_generator = ValueGenerator(ArithmeticProgression(a1=points[1], an=points[1], correct_s=True))
        cf_4.duration_generator = ValueGenerator(ArithmeticProgression(a1=points[1], an=points[0], correct_s=True))
        cf_5.duration_generator = ValueGenerator(ArithmeticProgression(a1=points[0], an=points[0], correct_s=True))
        cfg = ChordField()
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        cfg.add_child(cf_3)
        cfg.add_child(cf_4)
        cfg.add_child(cf_5)
        #
        # for fractal_tree in cfg.children:
        #     print(fractal_tree.duration_generator.generator.parameters_dict)
        #     values = [float(chord.quarter_duration) for chord in list(fractal_tree)]
        #     print(values)
        #     print(sum(values))

        xml_path = path + 'test_5.xml'
        self.score.set_time_signatures(quarter_durations=times)
        cfg.simple_format.to_stream_voice().add_to_score(self.score, part_number=1)

        self.score.max_division = 5
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        # breathing: duration_generator automatically, midi_generator: InterpolationGroup(2 x RandomInterpolations)
        breathing_proportions = [3, 7, 3, 10, 3]
        breathing_break_points = [1.5, 0.2, 1.5]
        breathing = Breathe(quarter_duration=sum(breathing_proportions), proportions=breathing_proportions,
                            breakpoints=breathing_break_points)

        midi_generator = ValueGenerator()

        midi_generator.add_child(
            ValueGenerator(RandomInterpolation(start=[60, 62, 66, 68], end=[67, 69, 73, 75], seed=10), duration=10)
        )

        midi_generator.add_child(
            ValueGenerator(RandomInterpolation(start=[67, 69, 73, 75], end=[60, 62, 66, 68], seed=11), duration=10)
        )

        breathing.midi_generator = midi_generator
        xml_path = path + 'test_6.xml'
        self.score.set_time_signatures(quarter_durations=breathing_proportions)
        breathing.simple_format.to_stream_voice().add_to_score(self.score)

        self.score.max_division = 5
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        # fields: midi_generators
        # group: duration_generator with __call__ RandomInterpolation
        cfg = ChordField(
            duration_generator=ValueGenerator(
                RandomInterpolation(start=[0.25, 0.25, 0.5], end=[0.5, 0.75, 1], seed=20)))
        cf_1 = ChordField(
            quarter_duration=3,
            midi_generator=ValueGenerator(cycle([60, 61, 64, 66])))
        cf_2 = ChordField(
            quarter_duration=6,
            midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
            long_ending_mode='self_extend')

        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        xml_path = path + 'test_7.xml'
        cfg.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        # fields: midi_generators
        # group: duration_generator with __call__ RandomInterpolation
        # output of fields not group

        cfg = ChordField(
            duration_generator=ValueGenerator(
                RandomInterpolation(start=[0.25, 0.25, 0.5], end=[0.5, 0.75, 1], seed=20)))

        cf_1 = ChordField(
            quarter_duration=3,
            midi_generator=ValueGenerator(cycle([60, 61, 64, 66])))
        cf_2 = ChordField(
            quarter_duration=6,
            midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
            long_ending_mode='self_extend')

        cfg.add_child(cf_1)
        cfg.add_child(cf_2)

        xml_path = path + 'test_8.xml'
        simple_format = SimpleFormat()
        simple_format.extend(cf_1.simple_format)
        simple_format.extend(cf_2.simple_format)
        simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_9(self):
        # fields: duration_generators
        # group: midi_generator
        cfg = ChordField(
        )
        cf_1 = ChordField(
            quarter_duration=3,
            duration_generator=ValueGenerator(ArithmeticProgression(a1=0.5, an=1, correct_s=True))
        )
        cf_2 = ChordField(
            quarter_duration=6,
            duration_generator=ValueGenerator(ArithmeticProgression(a1=1, an=1, correct_s=True))
        )
        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        cfg.midi_generator = ValueGenerator(cycle([60]))
        simple_format = cfg.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(cfg.quarter_duration))
        xml_path = path + 'test_9.xml'
        simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_10(self):
        midi_generator = ValueGenerator()

        midi_generator.add_child(
            ValueGenerator(RandomInterpolation(start=[60, 62, 66, 68], end=[67, 69, 73, 75], seed=10), duration=10)
        )

        midi_generator.add_child(
            ValueGenerator(RandomInterpolation(start=[67, 69, 73, 75], end=[60, 62, 66, 68], seed=11), duration=10)
        )

        cfg = ChordField(
        )
        cf_1 = ChordField(
            quarter_duration=3,
            duration_generator=ValueGenerator(ArithmeticProgression(a1=0.5, an=1, correct_s=True))
        )
        cf_2 = ChordField(
            quarter_duration=6,
            duration_generator=ValueGenerator(ArithmeticProgression(a1=1, an=1, correct_s=True))
        )

        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        cfg.midi_generator = midi_generator
        cfg.__next__()

    def test_11(self):
        cfg = ChordField(
            duration_generator=ValueGenerator(
                RandomInterpolation(start=[0.25, 0.25, 0.5], end=[0.5, 0.75, 1], seed=20)))
        cf_1 = ChordField(
            quarter_duration=3,
            midi_generator=ValueGenerator(cycle([60, 61, 64, 66])))
        cf_2 = ChordField(
            quarter_duration=6,
            midi_generator=ValueGenerator(cycle([72, 73, 74, 73, 72])),
            long_ending_mode='self_extend')

        cfg.add_child(cf_1)
        cfg.add_child(cf_2)
        xml_path = path + 'test_11.xml'
        copied = cfg.__deepcopy__()
        copied.simple_format.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_12(self):
        # breathing: duration_generator automatically, midi_generator: InterpolationGroup(2 x RandomInterpolations)
        breathing_proportions = [3, 7, 3, 10, 3]
        breathing_break_points = [1.5, 0.2, 1.5]
        breathing = Breathe(quarter_duration=sum(breathing_proportions), proportions=breathing_proportions,
                            breakpoints=breathing_break_points)

        midi_generator = ValueGenerator()

        midi_generator.add_child(
            ValueGenerator(RandomInterpolation(start=[60, 62, 66, 68], end=[67, 69, 73, 75], seed=10), duration=10)
        )

        midi_generator.add_child(
            ValueGenerator(RandomInterpolation(start=[67, 69, 73, 75], end=[60, 62, 66, 68], seed=11), duration=10)
        )

        breathing.midi_generator = midi_generator
        copied = breathing.__deepcopy__()
        xml_path = path + 'test_12.xml'
        self.score.set_time_signatures(quarter_durations=breathing_proportions)
        copied.simple_format.to_stream_voice().add_to_score(self.score)

        self.score.max_division = 5
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_13(self):
        proportions = (1, 3, 1, 5, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=20)
        expected = 20
        actual = breathe.quarter_duration
        self.assertEqual(expected, actual)

    def test_14(self):
        proportions = (1, 3, 1, 5, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=20, quantize=1)
        expected = [2, 5, 2, 9, 2]
        actual = [child.quarter_duration for child in breathe.children]
        self.assertEqual(expected, actual)

    def test_15(self):
        field = ChordField()
        child_1 = field.add_child(ChordField(
            midi_generator=ValueGenerator(cycle([71])),
            duration_generator=ValueGenerator(cycle([1])),
            quarter_duration=1))
        child_2 = field.add_child(ChordField(
            midi_generator=ValueGenerator(cycle([71])),
            duration_generator=ValueGenerator(cycle([1])),
            quarter_duration=1))
        actual = field.chords
        expected = child_1.chords + child_2.chords
        self.assertEqual(expected, actual)
