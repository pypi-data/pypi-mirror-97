import os
from itertools import cycle

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator

path = str(os.path.abspath(__file__).split('.')[0])
score = TreeScoreTimewise()
parent_chord_field = ChordField(duration_generator=ValueGenerator(ArithmeticProgression(n=5, a1=0.5, correct_s=True)))
# parent_chord_field = ChordField(duration_generator=ValueGenerator(iter([0.5, 1, 1.5])))
quarter_durations = [3, 2, 3]
for i in range(len(quarter_durations)):
    quarter_duration = quarter_durations[i]
    midi = 60 + i
    parent_chord_field.add_child(
        ChordField(midi_generator=ValueGenerator(cycle([midi])), long_ending_mode='self_extend',
                   short_ending_mode='self_shrink', quarter_duration=quarter_duration))
###
print(list(parent_chord_field.duration_generator.__deepcopy__()))
simple_format = SimpleFormat()
for child in parent_chord_field.children:
    simple_format.extend(child.simple_format)
simple_format.to_stream_voice().add_to_score(score=score, part_number=3)
print(simple_format.quarter_duration)
print(float(simple_format.quarter_duration))
###

xml_path = path + '_test_2.xml'
score.write(xml_path)
