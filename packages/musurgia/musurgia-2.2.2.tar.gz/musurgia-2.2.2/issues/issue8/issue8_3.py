import os
from itertools import cycle

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.chordfield import ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator

path = str(os.path.abspath(__file__).split('.')[0])
score = TreeScoreTimewise()
arth_durations = [2, 4]
new_child_durations = [1, 5]

arith_chord_field = ChordField()
for arth_duration in arth_durations:
    arith_chord_field.add_child(ChordField(quarter_duration=arth_duration,
                                           duration_generator=ValueGenerator(
                                               ArithmeticProgression(a1=1, an=0.25, correct_s=True))))

arith_chord_field.midi_generator = ValueGenerator(cycle([60]))
# copied_arith_chord_field = arith_chord_field.__deepcopy__()
# print([float(x) for x in (list(arith_chord_field.duration_generator.__deepcopy__()))])
# print(sum(list(arith_chord_field.duration_generator.__deepcopy__())))
new_chord_field = ChordField(duration_generator=arith_chord_field.duration_generator.__deepcopy__())
# new_chord_field = ChordField(duration_generator=arith_chord_field.duration_generator)
for i, new_child_duration in enumerate(new_child_durations):
    midi = 60 + i
    new_chord_field.add_child(ChordField(quarter_duration=new_child_duration,
                                         midi_generator=ValueGenerator(cycle([midi])),
                                         long_ending_mode='self_extend',
                                         short_ending_mode='self_shrink'))

arith_chord_field.simple_format.to_stream_voice().add_to_score(score=score, part_number=1)
# copied_arith_chord_field.simple_format.to_stream_voice().add_to_score(score=score, part_number=1)
simple_format = SimpleFormat()
for child in new_chord_field.children:
    simple_format.extend(child.simple_format)

simple_format.to_stream_voice().add_to_score(score=score, part_number=2)
xml_path = path + '.xml'
score.write(xml_path)
