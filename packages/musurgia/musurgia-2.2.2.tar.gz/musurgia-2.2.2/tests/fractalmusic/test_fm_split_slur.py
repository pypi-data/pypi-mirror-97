import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        self.fm.duration = 10
        self.fm.tempo = 60
        self.fm.midi_generator.midi_range = [60, 67]
        self.fm.add_layer()
        self.score = TreeScoreTimewise()
        self.score.set_time_signatures(quarter_durations=[self.fm.quarter_duration])

    def test_1(self):

        sp = self.fm.get_children()[0].split(1, 1, 1, 1, 1)
        sp[0].chord.add_dynamics('pp')
        sp[0].chord.add_slur('start')
        sp[-1].chord.add_slur('stop')
        sf = self.fm.get_simple_format()
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1)

        xml_path = path + '_test_1.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)

    def test_2(self):
        def add_repetition(node):
            node.chord.add_articulation('tenuto')
            duration = node.chord.quarter_duration
            lengths = int(duration) * [1]
            if len(lengths) > 1:
                diff = duration - int(duration)
                if diff > 0:
                    lengths[-1] += diff
                sp = node.split(lengths)
                sp[0].chord.add_slur('start')
                sp[-1].chord.add_slur('stop')

        for child in self.fm.get_children():
            add_repetition(child)

        sf = self.fm.get_simple_format()
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1)

        xml_path = path + '_test_2.xml'
        self.score.write(path=xml_path)
        self.assertCompareFiles(actual_file_path=xml_path)
