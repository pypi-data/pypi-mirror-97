import os

from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])

fm = FractalMusic(tempo=72, quarter_duration=18, tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
                  proportions=(1, 2, 3, 4, 5, 6, 7), multi=(1, 3), reading_direction='vertical')
fm.midi_generator.set_directions(-1, -1, -1, -1, -1, -1, -1)
fm.midi_generator.midi_range = [60, 72]
fm.generate_children(number_of_children=3)
for child in fm.get_children():
    child.add_gliss()

xml_path = path + '.xml'

score = fm.get_score(layer_number=fm.number_of_layers)
score.max_division = 5
score.write(xml_path)
