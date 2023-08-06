import os
from itertools import cycle

from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction

from musurgia.chordfield.chordfield import ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])

fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5), tempo=56,
                  duration=45 / 2, multi=(2, 6), reading_direction='vertical')
fm.generate_children(number_of_children=4)
fm.quantize_children(grid_size=1)
selected_child = [ch for ch in fm.get_children() if ch.fractal_order == 4][0]
selected_child.midi_value = 0

selected_child.chord_field = ChordField(duration_generator=ValueGenerator(cycle([Fraction(1, 5)])),
                                        midi_generator=ValueGenerator(cycle([selected_child.midi_value])))

score = TreeScoreTimewise()
fm.get_simple_format(layer=fm.number_of_layers).to_stream_voice().add_to_score(score)

xml_path = path + '.xml'

score.write(xml_path)
