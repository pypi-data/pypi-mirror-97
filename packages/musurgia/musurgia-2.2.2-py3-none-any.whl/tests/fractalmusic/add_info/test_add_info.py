import os

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        fm.add_info('fractal_order')
        score = fm.get_score(layer_number=fm.number_of_layers)
        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        fm.add_layer()
        fm.add_info('fractal_order')
        score = fm.get_score()
        xml_path = path + '_test_2.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        fm.add_layer()
        fm.add_info('midi_value')
        score = fm.get_score()
        xml_path = path + '_test_3.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        fm.add_layer()
        fm.add_info((lambda node: int(node.midi_value) if int(node.midi_value) == node.midi_value else node.midi_values,
                     'above'))
        score = fm.get_score()
        xml_path = path + '_test_4.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)
