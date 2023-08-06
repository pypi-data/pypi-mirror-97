from musicscore.musictree.treechord import TreeChord

from musurgia.fractaltree.fractalmusic import FractalMusic

fm = FractalMusic(tempo=60, quarter_duration=10)
fm.add_layer()
fm.get_children()[1].chord.add_grace_chords(chords=[TreeChord(midis=[63, 65]), TreeChord(midis=[64]), TreeChord(midis=[66])])
