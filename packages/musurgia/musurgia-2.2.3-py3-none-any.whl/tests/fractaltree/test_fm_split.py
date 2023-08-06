import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(tempo=60, quarter_duration=4)

    def test_1(self):
        self.fm.split(1, 2)
        score = TreeScoreTimewise()
        self.fm.get_score(score)
        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        self.fm.split(1, 2)[1].chord.to_rest()
        score = TreeScoreTimewise()
        self.fm.get_score(score)
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
