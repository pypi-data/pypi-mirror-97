import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = os.path.abspath(__file__).split('.')[0]


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(tempo=60, tree_permutation_order=[3, 1, 2], proportions=[1, 2, 3], quarter_duration=20)
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.fm.add_layer()
        self.fm.get_children()[1].reduce_children(lambda node: node.fract_order < 3)
        self.fm.add_layer()
        self.fm.add_layer()
        sf = self.fm.get_simple_format(layer=1)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)
