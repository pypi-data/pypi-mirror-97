import os
from unittest import TestCase

from musicscore.musictree.midi import B, A, C, F
from musicscore.musictree.treechord import TreeChord

from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic(tempo=60, quarter_duration=10, proportions=(1, 2, 3), tree_permutation_order=(3, 1, 2))
        fm.add_layer()
        midis = [B(4), A(4, 'b'), C(4, '#'), A(3), F(4)]
        fm.get_children()[0].add_layer()
        for leaf, midi in zip(fm.traverse_leaves(), midis):
            leaf.set_chord(TreeChord(midi))
        score = fm.get_score(show_fractal_orders=True)
        xml_path = path + '_test_.xml'
        score.write(path=xml_path)
