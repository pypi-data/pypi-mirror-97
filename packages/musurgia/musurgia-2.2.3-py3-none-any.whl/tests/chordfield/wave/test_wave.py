from pathlib import Path

from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction

from musurgia.chordfield.chordfield import HalfWave, Wave
from musurgia.unittest import TestCase

path = Path(__file__)


class TestWave(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_half_up(self):
        w = HalfWave(quarter_duration=10,
                     proportions=[7, 5, 3, 1],
                     duration_units=[Fraction(1, 7), Fraction(1, 6), Fraction(1, 5), Fraction(1, 4)],
                     min_midi=60,
                     max_midi=76,
                     show_last_note=True)
        w.simple_format.to_stream_voice().add_to_score(self.score)
        with self.file_path(path, 'half_up', 'xml') as xml_path:
            self.score.write(xml_path)

    def test_half_down(self):
        w = HalfWave(quarter_duration=10,
                     proportions=[7, 5, 3, 1],
                     duration_units=[Fraction(1, 7), Fraction(1, 6), Fraction(1, 5), Fraction(1, 4)],
                     min_midi=60,
                     max_midi=76,
                     direction='down',
                     show_last_note=True)
        w.simple_format.to_stream_voice().add_to_score(self.score)
        with self.file_path(path, 'half_down', 'xml') as xml_path:
            self.score.write(xml_path)

    def test_simple(self):
        w = Wave(quarter_duration=13, field_proportions=[1, 1], show_last_note=True)
        w.rising_field.proportions = [5, 4, 3, 2, 1]
        w.falling_field.proportions = [5, 4, 3, 2, 1]
        w.simple_format.to_stream_voice().add_to_score(self.score)
        with self.file_path(path, 'simple', 'xml') as xml_path:
            self.score.write(xml_path)

    def test_simple_down(self):
        w = Wave(quarter_duration=13, field_proportions=[1, 1], show_last_note=True, direction='down')
        w.rising_field.proportions = [5, 3, 2, 1]
        w.falling_field.proportions = [5, 3, 2, 1]
        w.simple_format.to_stream_voice().add_to_score(self.score)
        with self.file_path(path, 'simple_down', 'xml') as xml_path:
            self.score.write(xml_path)

    def test_units(self):
        w = Wave(quarter_duration=13, field_proportions=[1, 1], show_last_note=True)
        w.rising_field.proportions = [5, 4, 3, 2, 1]
        w.rising_field.duration_units = [Fraction(1, 7), Fraction(1, 6), Fraction(1, 5), Fraction(1, 4)]
        w.falling_field.proportions = [5, 4, 3, 2, 1]
        w.falling_field.duration_units = w.rising_field.duration_units
        w.simple_format.to_stream_voice().add_to_score(self.score)
        with self.file_path(path, 'units', 'xml') as xml_path:
            self.score.write(xml_path)
