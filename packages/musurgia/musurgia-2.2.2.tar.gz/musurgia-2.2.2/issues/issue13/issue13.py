import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])

fm = FractalMusic(tempo=72, quarter_duration=10)
fm.midi_generator.midi_range = [60, 72]
fm.add_layer()
node = fm.get_children()[-1]
node.chord.add_grace_chords(TreeChord(midis=node.midi_generator.midi_range[1]), mode='post')
print(node.chord.get_post_grace_chords())
print(fm.get_simple_format().chords[-1].get_post_grace_chords())
score = TreeScoreTimewise()
# fm.get_simple_format().to_stream_voice().add_to_score(score)
simple_format = SimpleFormat(quarter_durations=[1, 4])
simple_format.chords[-1].add_grace_chords(TreeChord(midis=[66]), mode='post')
simple_format.to_stream_voice().add_to_score(score)
# score = fm.get_score(layer_number=fm.number_of_layers)
xml_path = path + '.xml'
score.write(xml_path)
