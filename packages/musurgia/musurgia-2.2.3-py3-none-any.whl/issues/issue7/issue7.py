from itertools import cycle

from musurgia.chordfield.chordfield import ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator

parent_chord_field = ChordField(duration_generator=ValueGenerator(cycle([0.5])))
parent_chord_field.add_child(ChordField(midi_generator=ValueGenerator(cycle([60]))))
parent_chord_field.add_child(ChordField(quarter_duration=4, midi_generator=ValueGenerator(cycle([60]))))
parent_chord_field.add_child(ChordField(quarter_duration=8, midi_generator=ValueGenerator(cycle([61]))))


print(id(parent_chord_field.duration_generator))
print([id(chfi.duration_generator) for chfi in parent_chord_field.children])
print([chfi._duration_generator for chfi in parent_chord_field.children])

copied_parent_chord_field = parent_chord_field.__deepcopy__()
print(id(copied_parent_chord_field.duration_generator))
print([id(chfi.duration_generator) for chfi in copied_parent_chord_field.children])
print([chfi._duration_generator for chfi in copied_parent_chord_field.children])

