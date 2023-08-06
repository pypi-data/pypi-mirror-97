from musurgia.fractaltree.fractalmusic import FractalMusic

fm = FractalMusic(tempo=72, quarter_duration=10)
fm.add_layer()

copied = fm.__deepcopy__()

print(fm.get_children())