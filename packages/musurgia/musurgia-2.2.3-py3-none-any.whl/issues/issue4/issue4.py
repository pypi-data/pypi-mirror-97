from musurgia.fractaltree.fractalmusic import FractalMusic

fm = FractalMusic(quarter_duration=10, tempo=60)
fm.midi_generator.midi_range = [60, 84]
fm.add_layer()
node = fm.get_children()[0]

copy = node.__deepcopy__()
print(copy.midi_generator.midi_range)
# copy.midi_generator.midi_range = node.midi_generator.midi_range
node.add_layer()
print([child.midi_value for child in node.get_children()])

copy.add_layer()
print([child.midi_value for child in copy.get_children()])
