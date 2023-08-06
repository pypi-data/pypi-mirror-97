import os
from fractions import Fraction
from itertools import cycle

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.chordfield.chordfield import Breathe, ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator

path = str(os.path.abspath(__file__).split('.')[0])
score = TreeScoreTimewise()
proportions = (0, 2, 2, 0, 0)
breakpoints = (1, Fraction(1, 4), 1)
quarter_durations = [2, 4]
breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=sum(quarter_durations),
                  quantize=1)
###
breathe = breathe.__deepcopy__()
breathe.midi_generator = ValueGenerator(cycle([60]))
###
parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
# parent_chord_field = ChordField(
#     duration_generator=ValueGenerator(iter(list(breathe.duration_generator.__deepcopy__()))))
for i in range(len(quarter_durations)):
    quarter_duration = quarter_durations[i]
    midi = 60 + i
    parent_chord_field.add_child(
        ChordField(midi_generator=ValueGenerator(cycle([midi])), long_ending_mode='self_extend',
                   short_ending_mode='self_shrink', quarter_duration=quarter_duration))
####
copy_parent_chord_field = parent_chord_field.__deepcopy__()
####

####
breathe.simple_format.to_stream_voice().add_to_score(score=score, part_number=1)
parent_chord_field.simple_format.to_stream_voice().add_to_score(score=score, part_number=2)


# print(sum([fractal_tree.quarter_duration for fractal_tree in copy_parent_chord_field.children]))
# # print(copy_parent_chord_field.children[0].simple_format.quarter_duration)
# print(([float(fractal_tree.quarter_duration) for fractal_tree in copy_parent_chord_field.children]))
# print(float(copy_parent_chord_field.children[0].simple_format.quarter_duration))
# print(([float(fractal_tree.quarter_duration) for fractal_tree in copy_parent_chord_field.children]))
# print(float(copy_parent_chord_field.children[1].simple_format.quarter_duration))
# print(([float(fractal_tree.quarter_duration) for fractal_tree in copy_parent_chord_field.children]))
def iterate(chord_field):
    while True:
        try:
            print('pos:{}, pospar:{}, genpos {}'.format(chord_field.position, chord_field.position_in_parent,
                                                        chord_field.duration_generator.position,
                                                        ))
            next = chord_field.__next__()
            print('next duration:{}'.format(next.quarter_duration))
        except StopIteration:
            break


iterate(copy_parent_chord_field.children[0])
print()
iterate(copy_parent_chord_field.children[1])
simple_format = SimpleFormat()
for child in copy_parent_chord_field.children:
    simple_format.extend(child.simple_format)
simple_format.to_stream_voice().add_to_score(score=score, part_number=3)
print(float(sum([child.quarter_duration for child in copy_parent_chord_field.children])))
##

xml_path = path + '_test_1.xml'
score.write(xml_path)
