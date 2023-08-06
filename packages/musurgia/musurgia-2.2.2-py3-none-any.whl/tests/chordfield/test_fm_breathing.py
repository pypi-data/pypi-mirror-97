import os
from itertools import cycle

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from quicktions import Fraction

from musurgia.unittest import TestCase
from musurgia.chordfield.chordfield import Breathe, ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.interpolation import RandomInterpolation

path = str(os.path.abspath(__file__).split('.')[0])


class TestFMBreathing(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.fm = FractalMusic(quarter_duration=24, tempo=40)

    def test_1(self):
        proportions = (1, 3, 1, 5, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        quarter_durations = [8, 12]
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=sum(quarter_durations),
                          quantize=1)
        breathe.midi_generator = ValueGenerator(cycle([71]))
        test_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        for i in range(len(quarter_durations)):
            quarter_duration = quarter_durations[i]
            midi = 60 + i
            test_chord_field.add_child(
                ChordField(midi_generator=ValueGenerator(cycle([midi])), long_ending_mode='self_extend',
                           short_ending_mode='self_shrink', quarter_duration=quarter_duration))

        test_chord_field_2 = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        for i in range(len(quarter_durations)):
            quarter_duration = quarter_durations[i]
            midi = 72 + i
            test_chord_field_2.add_child(
                ChordField(midi_generator=ValueGenerator(cycle([midi])), long_ending_mode='cut',
                           short_ending_mode='add_rest', quarter_duration=quarter_duration))
        breathe.simple_format.to_stream_voice().add_to_score(score=self.score, part_number=1)
        test_chord_field.simple_format.to_stream_voice().add_to_score(score=self.score, part_number=2)

        simple_format = SimpleFormat()
        for child in test_chord_field_2.children:
            simple_format.extend(child.simple_format)

        simple_format.to_stream_voice().add_to_score(score=self.score, part_number=3)
        xml_path = path + '_test_1.xml'
        self.score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        self.fm.add_layer()
        self.fm.quantize_children(grid_size=1)
        proportions = (1, 3, 1, 5, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        selected_nodes = self.fm.get_children()[:2]
        breath_quarter_duration = sum([node.quarter_duration for node in selected_nodes])
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=breath_quarter_duration,
                          quantize=1)
        parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        for i in range(len(selected_nodes)):
            midi = 60 + i
            chord_field = ChordField(midi_generator=ValueGenerator(cycle([midi])), long_ending_mode='self_extend',
                                     short_ending_mode='self_shrink')
            parent_chord_field.add_child(chord_field)
            node = selected_nodes[i]
            node.chord_field = chord_field

        score = self.fm.get_score(show_fractal_orders=True, layer_number=self.fm.number_of_layers)
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        def get_children_midis(node):
            copy = node.__deepcopy__()
            copy.midi_generator.midi_range = node.midi_generator.midi_range
            copy.add_layer()

            output = [child.chord.midis[0].value for child in copy.get_children()]
            return output

        self.fm.multi = (self.fm.multi[0], self.fm.multi[1] + 1)
        self.fm.midi_generator.midi_range = (60, 72)
        self.fm.add_layer()
        self.fm.quantize_children(grid_size=1)
        proportions = (1, 3, 1, 3, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        selected_nodes = self.fm.get_children()[:2]
        breath_quarter_duration = sum([node.quarter_duration for node in selected_nodes])
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=breath_quarter_duration,
                          quantize=1)
        parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        for i in range(len(selected_nodes)):
            node = selected_nodes[i]
            start_chord = get_children_midis(node)
            next_node = node.next_sibling
            if next_node:
                end_chord = get_children_midis(next_node)
            else:
                end_chord = start_chord

            chord_field = ChordField(
                midi_generator=ValueGenerator(RandomInterpolation(start=start_chord, end=end_chord, seed=10)),
                long_ending_mode='self_extend',
                short_ending_mode='self_shrink')
            parent_chord_field.add_child(chord_field)

            node.chord_field = chord_field

        score = self.fm.get_score(show_fractal_orders=True, layer_number=self.fm.number_of_layers)
        score.max_division = 7
        xml_path = path + '_test_3.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        # self.fm.multi = (self.fm.multi[0], self.fm.multi[1] + 1)
        def get_chord_stamp():
            node = fm.__copy__()
            node.midi_generator.midi_range = fm.midi_generator.midi_range
            node.midi_generator.microtone = 4
            node.add_layer()
            chord_midis = [child.midi_value for child in node.get_children()]
            output = [chord_midi - chord_midis[node.size // 2] for chord_midi in chord_midis]
            return output

        fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
                          quarter_duration=30, tempo=80)
        fm.midi_generator.midi_range = (60, 72)
        fm.midi_generator.microtone = 4
        fm.add_layer()
        fm.quantize_children(grid_size=1)
        proportions = (1, 10, 1, 7, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        selected_nodes = fm.get_children()[1:3]

        breath_quarter_duration = sum([node.quarter_duration for node in selected_nodes])
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=breath_quarter_duration,
                          quantize=1)
        parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        for i in range(len(selected_nodes)):
            node = selected_nodes[i]
            start_chord = [stamp + node.midi_value for stamp in get_chord_stamp()]
            next_node = node.next_sibling
            if next_node:
                end_chord = [stamp + node.midi_value for stamp in get_chord_stamp()]
            else:
                end_chord = start_chord

            chord_field = ChordField(
                midi_generator=ValueGenerator(RandomInterpolation(start=start_chord, end=end_chord, seed=10)),
                long_ending_mode='self_extend',
                short_ending_mode='self_shrink')
            parent_chord_field.add_child(chord_field)

            node.chord_field = chord_field

        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        score.max_division = 7
        score.finish()
        partwise = score.to_partwise()
        xml_path = path + '_test_4.xml'
        partwise.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):

        def get_chord(node):
            output = fm.get_choral_midis(range_factor=1)
            transposition = node.midi_value - output[3]
            output = [midi + transposition for midi in output]
            # output = node.get_choral_midis(range_factor=8 - node.fractal_order)
            return output

        fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
                          quarter_duration=30, tempo=72)
        # fm.multi = (self.fm.multi[0], self.fm.multi[1] + 1)
        fm.midi_generator.midi_range = (62, 62 + 11)
        fm.midi_generator.microtone = 4
        fm.add_layer()
        fm.quantize_children(grid_size=1)
        selected_nodes = fm.get_children()[2:5]

        proportions = (1, 10, 1, 7, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        breath_quarter_duration = sum([node.quarter_duration for node in selected_nodes])
        breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=breath_quarter_duration,
                          quantize=1)
        parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
        for i in range(len(selected_nodes)):
            node = selected_nodes[i]
            start_chord = get_chord(node)
            next_node = node.next_sibling
            if next_node:
                end_chord = get_chord(next_node)
            else:
                end_chord = start_chord

            chord_field = ChordField(
                midi_generator=ValueGenerator(RandomInterpolation(start=start_chord, end=end_chord, seed=10)),
                long_ending_mode='self_extend',
                short_ending_mode='self_shrink')
            parent_chord_field.add_child(chord_field)

            node.chord_field = chord_field

        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        score.max_division = 7
        score.finish()
        partwise = score.to_partwise()
        xml_path = path + '_test_5.xml'
        partwise.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_6(self):
        def get_chord(node):
            output = fm.get_choral_midis(range_factor=1)
            transposition = node.midi_value - output[3]
            output = [midi + transposition for midi in output]
            return output

        fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
                          quarter_duration=30, tempo=72)
        fm.midi_generator.midi_range = (62, 62 + 11)
        fm.midi_generator.microtone = 4
        fm.add_layer()
        fm.quantize_children(grid_size=1)

        def make_breathe(nodes, proportions, breakpoints):
            breath_quarter_duration = sum([node.quarter_duration for node in nodes])
            breathe = Breathe(proportions=proportions, breakpoints=breakpoints,
                              quarter_duration=breath_quarter_duration,
                              quantize=1)

            parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
            for i in range(len(nodes)):
                node = selected_nodes[i]
                start_chord = get_chord(node)
                next_node = node.next_sibling
                if next_node:
                    end_chord = get_chord(next_node)
                else:
                    end_chord = start_chord

                chord_field = ChordField(
                    quarter_duration=node.quarter_duration,
                    midi_generator=ValueGenerator(RandomInterpolation(start=start_chord, end=end_chord, seed=10)),
                    long_ending_mode='self_extend',
                    short_ending_mode='self_shrink')
                parent_chord_field.add_child(chord_field)

            return parent_chord_field

        selected_nodes = fm.get_children()[2:5]
        # print(sum([node.quarter_duration for node in selected_nodes]))
        proportions = (1, 10, 1, 7, 1)
        breakpoints = (1, Fraction(1, 7), 1)
        breathe = make_breathe(nodes=selected_nodes, proportions=proportions,
                               breakpoints=breakpoints)
        # print(breathe.quarter_duration)
        fm.merge_children(2, 3, 2)
        # print(fm.get_children()[1].quarter_duration)
        fm.get_children()[1].simple_format = breathe.simple_format
        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        score.max_division = 7
        score.finish()
        partwise = score.to_partwise()
        xml_path = path + '_test_6.xml'
        partwise.write(xml_path)
        self.assertCompareFiles(xml_path)