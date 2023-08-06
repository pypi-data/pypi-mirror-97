import os
from itertools import cycle
from math import ceil

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.random import Random
from musurgia.unittest import TestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordField, ShortEndingError, LongEndingError
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.interpolation import Interpolation

path = str(os.path.abspath(__file__).split('.')[0])


def duration_generator(first_duration=1, delta=0.5):
    current_duration = first_duration
    while True:
        yield current_duration
        current_duration += delta


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        # chord_generator with matching quarter_duration
        field = ChordField(quarter_duration=11,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)))
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        field.simple_format.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        # chord_generator with too long quarter_duration:  mode : None
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)))
        with self.assertRaises(LongEndingError):
            list(field)

    def test_3(self):
        # chord_generator with too long quarter_duration:  mode : self_extend
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)),
                           long_ending_mode='self_extend')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_3.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        # chord_generator with too long quarter_duration:  mode : cut
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)),
                           long_ending_mode='cut')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_4.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        # chord_generator with too long quarter_duration:  mode : omit
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)),
                           long_ending_mode='omit')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_5.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        # chord_generator with too long quarter_duration:  mode : omit
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)),
                           long_ending_mode='omit_and_add_rest')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_6.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        # chord_generator with too long quarter_duration:  mode : omit
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2, 1, 2, 3, 4, 5]).chords)),
                           long_ending_mode='omit_and_stretch')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_7.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        # chord_generator with too short quarter_duration:  mode : None
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2]).chords)))
        with self.assertRaises(ShortEndingError):
            list(field)

    def test_9(self):
        # chord_generator with too short quarter_duration:  mode : self_shrink
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2]).chords)),
                           short_ending_mode='self_shrink')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_9.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_10(self):
        # chord_generator with too short quarter_duration:  mode : stretch
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2]).chords)),
                           short_ending_mode='stretch')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_10.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_11(self):
        # chord_generator with too short quarter_duration:  mode : rest
        field = ChordField(quarter_duration=10,
                           chord_generator=ValueGenerator(
                                iter(SimpleFormat(quarter_durations=[3, 2]).chords)),
                           short_ending_mode='add_rest')
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_11.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_12(self):
        field = ChordField(quarter_duration=10,
                           duration_generator=ValueGenerator(
                                cycle([1])),
                           midi_generator=ValueGenerator(
                                cycle([71]))
                           )
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=field.quarter_duration)
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_12.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_13(self):
        field = ChordField(quarter_duration=10,
                           duration_generator=ValueGenerator(
                                Random(pool=[0.2, 0.4, 0.8, 1.2, 1.6, 2], periodicity=3, seed=20)),
                           midi_generator=ValueGenerator(
                                cycle([71])),
                           long_ending_mode='self_extend'
                           )
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(field.quarter_duration))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_13.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_14(self):
        field = ChordField(quarter_duration=10,
                           duration_generator=ValueGenerator(duration_generator(first_duration=1, delta=0.2)
                                                              ),
                           midi_generator=ValueGenerator(cycle([71])),
                           long_ending_mode='omit_and_add_rest'
                           )
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(field.quarter_duration))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_14.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_15(self):
        field = ChordField(quarter_duration=10,
                           duration_generator=ValueGenerator(
                                Random(pool=[0.2, 0.4, 0.8, 1.2, 1.6, 2], periodicity=3, seed=20)),
                           midi_generator=ValueGenerator(
                                Interpolation(start=84, end=60, key=lambda x: int(x))),
                           long_ending_mode='self_extend'
                           )
        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(field.quarter_duration))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_15.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_16(self):
        field = ChordField(quarter_duration=10,
                           duration_generator=ValueGenerator(ArithmeticProgression(a1=0.2, an=2, correct_s=True)),
                           midi_generator=ValueGenerator(Interpolation(start=84, end=60,
                                                                        key=lambda midi: round(midi * 2) / 2)),
                           short_ending_mode=None)

        sf = field.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(field.quarter_duration))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_16.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_17(self):
        parent_field = ChordField()
        child_field_1 = ChordField(quarter_duration=5,
                                   duration_generator=ValueGenerator(cycle([1])),
                                   midi_generator=ValueGenerator(cycle([60]))
                                   )
        child_field_2 = ChordField(quarter_duration=10,
                                   duration_generator=ValueGenerator(cycle([2])),
                                   midi_generator=ValueGenerator(cycle([61]))
                                   )
        parent_field.add_child(child_field_1)
        parent_field.add_child(child_field_2)

        sf = parent_field.simple_format
        self.score.set_time_signatures(quarter_durations=ceil(parent_field.quarter_duration))
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_test_17.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
