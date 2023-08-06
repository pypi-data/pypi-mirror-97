import os

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(duration=10)

    def test_1(self):
        self.fm.tempo = 70
        self.fm.add_layer()
        self.fm.change_quarter_duration(round(self.fm.quarter_duration))

        xml_path = path + '_test_1.xml'
        score = self.fm.get_score(show_fractal_orders=True)
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        self.fm.tempo = 70
        self.fm.add_layer()
        self.fm.add_layer()
        self.fm.quantize_children()
        xml_path = path + '_test_2.xml'
        score = self.fm.get_children_score(show_fractal_orders=True)
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
