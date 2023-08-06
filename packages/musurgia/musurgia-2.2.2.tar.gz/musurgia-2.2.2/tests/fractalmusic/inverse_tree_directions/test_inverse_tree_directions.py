import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.fm = FractalMusic(tempo=60, quarter_duration=10)
        self.fm.midi_generator.midi_range = [60, 71]
        self.fm.add_layer()
        self.copied = self.fm.__deepcopy__()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        self.fm.quantize_children(1)
        self.score.set_time_signatures([child.quarter_duration for child in self.fm.get_children()])

        self.copied.inverse_tree_directions()
        self.copied.quantize_children(1)
        self.fm.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=1)
        self.copied.get_simple_format().to_stream_voice().add_to_score(score=self.score, staff_number=2)
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
