import os

from musicscore.musicxml.elements.note import Notehead

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        for child in fm.get_children():
            child.add_gliss(grid=0.5, show_heads=True)
            child.chord_field.chords[0].add_articulation('accent')
        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        fm = FractalMusic(tempo=60, quarter_duration=10, multi=(1, 2))
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        for child in fm.get_children():
            child.chord.add_articulation('accent')
            child.chord.add_dynamics('f')
        for child in fm.get_children():
            child.add_gliss()
        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        xml_path = path + '_test_2.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        fm = FractalMusic(tempo=60, quarter_duration=10, multi=(1, 3))
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        for child in fm.get_children():
            for midi in child.chord.midis:
                midi.notehead = Notehead('diamond', filled='no')
        for child in fm.get_children():
            child.add_gliss()

        fm.get_children()[-1].chord_field.chords[-1].get_post_grace_chords()[0].midis[0].notehead = Notehead('diamond',
                                                                                                             filled='no')
        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        xml_path = path + '_test_3.xml'
        score.write(path=xml_path)
        self.assertCompareFiles(xml_path)
