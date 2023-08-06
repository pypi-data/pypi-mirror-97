import itertools
import os
from math import ceil, floor

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.elements.note import Notations, Notehead
from musicscore.musicxml.types.complextypes.notations import Slide
from prettytable import PrettyTable
from quicktions import Fraction

from musurgia import basic_functions, scaledvalues
from musurgia.chordfield.chordfield import ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator
from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.fractaltree.midigenerators import RelativeMidi, MidiGenerator
from musurgia.interpolation import Interpolation
from musurgia.pdf.segmentedline import SegmentedLine
from musurgia.permutation import permute
from musurgia.quantize import get_quantized_values
from musurgia.timing import Timing


class FractalMusicException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class SetDurationFirstException(FractalMusicException):
    def __init__(self, *args):
        super().__init__('set duration first!', *args)


class SetTempoFirstException(FractalMusicException):
    def __init__(self, *args):
        super().__init__('set tempo first!', *args)


class TempoIsAlreadySet(FractalMusicException):
    def __init__(self, *args):
        super().__init__('FractalMusic().tempo can only be set once', *args)


class ChildTempoIsAlreadySet(FractalMusicException):
    def __init__(self, *args):
        super().__init__('FractalMusic().tempo of parent can not be set after setting tempo of fractal_tree', *args)


class MergeException(FractalMusicException):
    def __init__(self, *args):
        super().__init__(*args)


class MergeTempoException(MergeException):
    def __init__(self, tempo, *args):
        super().__init__('nodes to merge must have the same tempo {}'.format(tempo), *args)


class ChordFieldConflict(FractalMusicException):
    def __init__(self, *args):
        super().__init__('node.chord and node.chord_field cannot be both set!', *args)


class SimpleFormatConflict(FractalMusicException):
    def __init__(self, *args):
        super().__init__('simple_format and node.chord or node.chord_field cannot be both set!', *args)


class NoneChordException(FractalMusicException):
    def __init__(self, *args):
        super().__init__('node.chord and node.chord_field are both None.', *args)


class FractalMusic(FractalTree):
    def __init__(self,
                 duration=None,
                 midi_generator=None,
                 tempo=None,
                 quarter_duration=None,
                 tree_directions=None,
                 permute_directions=True,
                 *args, **kwargs):

        # super().__init__(value=duration, *args, **kwargs)
        super().__init__(*args, **kwargs)

        self._children_generated_midis = None
        self._chord = None
        self._chord_field = None
        self._midi_generator = None
        self._midi_value = None
        self._permute_directions = True
        self._simple_format = None
        self._tempo = None
        self._tree_directions = None

        self.midi_generator = midi_generator
        if duration:
            self.duration = duration

        self.tempo = tempo
        self.permute_directions = permute_directions
        self.tree_directions = tree_directions

        self.quarter_duration = quarter_duration

    # //private properties
    @property
    def _children_midis(self):
        return [child.midi_value for child in self.get_children()]

    @property
    def _midi_iterator(self):
        mg = self.midi_generator
        return mg.iterator

    @_midi_iterator.setter
    def _midi_iterator(self, value):
        raise AttributeError('_midi_iterator cannot be set directly. Use midi-generator!')

    # //private methods
    def _calculate_durational_position_in_tree(self):
        parent = self.up
        if self.is_root:
            return 0
        else:
            index = parent.get_children().index(self)
            if index == 0:
                return parent.durational_position_in_tree
            else:
                return parent.get_children()[index - 1].durational_position_in_tree + parent.get_children()[
                    index - 1].duration

    def _check_merge_nodes(self, nodes):
        tempo = set([node.tempo for node in nodes])
        if len(tempo) != 1:
            raise MergeTempoException(tempo)

    def _child_has_tempo(self):
        children_tempi = [child.tempo for child in self.get_children() if child.tempo]
        if children_tempi:
            return True
        else:
            return False

    # //public properties

    @property
    def auto_midi_range(self):
        if self.is_root:
            raise AttributeError('root has no auto_midi_range')

        parent_midis = self.up.children_generated_midis
        self_index = self.up.get_children().index(self)
        auto_range = parent_midis[self_index:self_index + 2]
        return auto_range

    @property
    def children_generated_midis(self):
        if self._children_generated_midis is None:
            self._children_generated_midis = []
            self._children_generated_midis = list(self._midi_iterator)

        return [midi for midi in self._children_generated_midis]

    @property
    def chord(self):
        if self.chord_field is None and self._simple_format is None:
            if self._chord is None:
                self._chord = TreeChord(quarter_duration=self.quarter_duration, midis=[self.midi_value])
            else:
                self._chord.quarter_duration = self.quarter_duration
            return self._chord
        else:
            return None

    @property
    def chord_field(self):
        if self._chord_field is not None:
            list(self._chord_field)
        return self._chord_field

    @chord_field.setter
    def chord_field(self, chord_field):
        if chord_field is not None and not isinstance(chord_field, ChordField):
            raise TypeError()
        if chord_field is not None:
            chord_field.quarter_duration = self.quarter_duration
        self._chord_field = chord_field

    @property
    def duration(self):
        return self.value

    @duration.setter
    def duration(self, val):
        self.value = val

    @property
    def durational_position_in_tree(self):
        return self._calculate_durational_position_in_tree()

    @property
    def midi_generator(self):
        if self._midi_generator is None:
            try:
                if not self.duration:
                    raise SetDurationFirstException()
                self._midi_generator = RelativeMidi(midi_range=None, proportions=self.children_fractal_values,
                                                    directions=None)
                self._midi_generator.node = self
            except AttributeError:
                raise Exception('midi_generator is None and cannot be set:')
        else:
            self._midi_generator.node = self

        if isinstance(self._midi_generator, RelativeMidi):

            if not self._midi_generator._directions:
                tree_directions = self.get_root().tree_directions

                if self.permute_directions:
                    directions = permute(tree_directions, self.permutation_order)
                else:
                    directions = tree_directions

                self._midi_generator.directions = directions

            if self._midi_generator.midi_range is None:
                if self.is_root:
                    self._midi_generator.midi_range = [71]
                else:
                    self._midi_generator.midi_range = self.auto_midi_range
                    self._midi_generator._auto_ranged = True

        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, value):
        if value is not None:
            if not (isinstance(value, MidiGenerator)):
                err = 'midi_generator can only be an instance of subclasses of MidiGenerator or None. None=RelativeMidi(midi_range=self.midi_range, proportions=permute(self.fractal_proportions, self.fractal.permutation_order)'
                raise TypeError(err)

        self._midi_generator = value
        if self._midi_generator:
            self._midi_generator.node = self

    @property
    def midi_value(self):
        if self._midi_value is None:
            if self.is_root:
                self._midi_value = 71
            else:
                self._midi_value = self.up.children_generated_midis[self.up.get_children().index(self)]
        return self._midi_value

    @midi_value.setter
    def midi_value(self, value):
        if value is not None:
            if isinstance(value, int) or isinstance(value, float):
                if value >= 18 or value == 0:
                    self._midi_value = value
                else:
                    raise ValueError('midi can be 0 and greater than 18')
            else:
                raise TypeError('midi can only be int, float or None not {}'.format(type(value)))
        else:
            self._midi_value = value

    @property
    def multi(self):
        return super().multi

    @multi.setter
    def multi(self, val):
        FractalTree.multi.fset(self, val)
        # is midi_generator already set?
        try:
            if self._midi_generator:
                if isinstance(self._midi_generator, RelativeMidi):
                    midi_range = self._midi_generator.midi_range
                    _auto_ranged = self._midi_generator._auto_ranged
                    self._midi_generator = self._midi_generator.copy()
                    self._midi_generator.midi_range = midi_range
                    self._midi_generator._auto_ranged = _auto_ranged
                else:
                    self._midi_generator = self._midi_generator.copy()
        except AttributeError:
            pass

    @property
    def permute_directions(self):
        return self._permute_directions

    @permute_directions.setter
    def permute_directions(self, value):
        if not isinstance(value, bool):
            raise TypeError()
        self._permute_directions = value

    @property
    def quarter_duration(self):
        if not self.tempo:
            raise SetTempoFirstException()
        return Fraction(Fraction(self.duration * self.tempo), Fraction(60))

    @quarter_duration.setter
    def quarter_duration(self, val):
        if val is not None:
            if not self.tempo:
                raise SetTempoFirstException()
            self.duration = Fraction(Fraction(val * 60), Fraction(self.tempo))

    @property
    def quarter_position_in_tree(self):
        return self.position_in_tree * self.tempo / 60

    @property
    def simple_format(self):
        raise FractalMusicException('simple_format is not gettable.')

    @simple_format.setter
    def simple_format(self, val):
        if not isinstance(val, SimpleFormat):
            raise TypeError()
        self._simple_format = val

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, val):
        if self._tempo:
            raise TempoIsAlreadySet()
        if self._child_has_tempo():
            raise ChildTempoIsAlreadySet()
        self._tempo = val
        for child in self.get_children():
            child.tempo = val

    @property
    def tree_directions(self):
        return self._tree_directions

    @tree_directions.setter
    def tree_directions(self, val):
        if val is None:
            val = [1, -1]
        length = len(self.permutation_order)
        if len(val) > length:
            val = val[:length]
        elif len(val) < length:
            output = []
            cycled = itertools.cycle(val)
            for i in range(length):
                output.append(cycled.__next__())
            val = output
        self._tree_directions = val
        for node in self.traverse():
            if node._midi_generator:
                try:
                    if self.permute_directions and node._midi_generator.directions:
                        node._midi_generator.directions = permute(self.tree_directions, self.permutation_order)
                    else:
                        node._midi_generator.directions = self.tree_directions
                except AttributeError:
                    pass

    # //public methods
    # add
    def add_gliss(self, unit=1, grid=1, min_quarter_duration=Fraction(1, 8), show_heads=False):
        def get_slides(chord):
            return [slide for notation in chord.get_children_by_type(Notations) for slide in
                    notation.get_children_by_type(Slide)]

        position = self.quarter_position_in_tree
        delta = unit - (position - int(position))
        if delta >= min_quarter_duration:
            duration_generator = ValueGenerator(itertools.chain(iter([delta]), itertools.cycle([unit])))
        else:
            duration_generator = ValueGenerator(itertools.cycle([unit]))

        chord_field = ChordField(duration_generator=duration_generator,
                                 midi_generator=ValueGenerator(
                                     Interpolation(start=self.midi_generator.midi_range[0],
                                                   end=self.midi_generator.midi_range[1], grid=grid)),
                                 long_ending_mode='cut',
                                 short_ending_mode='stretch')

        first_chord = self.chord.__deepcopy__()
        self.chord_field = chord_field
        list(chord_field)
        first_chord.quarter_duration = chord_field.chords[0].quarter_duration
        chord_field.chords[0] = first_chord
        if chord_field.chords[-1].quarter_duration < min_quarter_duration:
            chord_field._chords = chord_field._chords[:-1]

        for chord in chord_field.chords[1:]:
            for midi in chord.midis:
                if show_heads is False:
                    midi.notehead = Notehead('none')
                    alter = midi.get_pitch_rest().alter
                    if alter:
                        midi.transpose(-alter.value)
                    midi.accidental.force_hide = True

        if self.previous_leaf and self.previous_leaf.chord_field:
            list(self.previous_leaf.chord_field)
            previous_slides_types = [slide.type for slide in get_slides(self.previous_leaf.chord_field.chords[0])]
            if 'start' in previous_slides_types:
                try:
                    self.chord.add_slide('stop')
                except AttributeError:
                    self.chord_field.chords[0].add_slide('stop')
        if self.next_leaf is None:
            grace = TreeChord(midis=self.midi_generator.midi_range[1])
            grace.add_slide('stop')
            chord_field.chords[-1].add_grace_chords([grace], mode='post')

        chord_field.chords[0].add_slide('start')

    def add_info(self, *show_attributes, condition=None):
        def write_words(words, placement, relative_y):
            if placement is None:
                placement = 'below'
            if relative_y is None:
                if placement == 'below':
                    relative_y = -15
                else:
                    relative_y = 15
            try:
                self.chord.add_words(words, placement=placement, relative_y=relative_y)
            except AttributeError:
                try:
                    for chord in self.chord_field.chords:
                        chord.add_words(words, placement=placement, relative_y=relative_y)
                except AttributeError:
                    for chord in self._simple_format.chords:
                        chord.add_words(words, placement=placement, relative_y=relative_y)

        def get_words(attr):
            if attr == 'fractal_order':
                text = [node.fractal_order for node in self.get_branch()[1:]]
                words = ('\n'.join([str(x) for x in text]))
            elif isinstance(attr, str):
                words = str(getattr(self, attr))
            elif callable(attr):
                words = str(attr(self))
            else:
                raise AttributeError()
            return words

        for attr in show_attributes:
            placement = None
            relative_y = None
            if isinstance(attr, tuple):
                words = get_words(attr[0])
                placement = attr[1]
                try:
                    relative_y = attr[2]
                except IndexError:
                    pass
            else:
                words = get_words(attr)

            write_words(words, placement, relative_y)

        for child in self.get_children():
            if condition is None or condition(child) is True:
                child.add_info(*show_attributes, condition=condition)

    # get

    def get_choral(self, range_factor=1, direction=None, last=False):
        choral_midis = list(dict.fromkeys(
            self.get_choral_midis(range_factor=range_factor, direction=direction, last=last)
        ))
        return TreeChord(quarter_duration=self.quarter_duration, midis=choral_midis)

    def get_choral_midis(self, range_factor=1, direction=None, last=False):
        range_ = (self.midi_generator.midi_range[1] - self.midi_generator.midi_range[0]) * range_factor
        self_direction = range_ / abs(range_)
        if direction is None or direction == 0:
            pass
        elif direction == 1:
            range_ = abs(range_)
        elif direction == -1:
            range_ = -abs(range_)

        children_midis = self.children_generated_midis
        choral_midis = []

        step = 2 / self.midi_generator.microtone
        if self_direction > 0:
            scale = scaledvalues.ScaledValues(min(children_midis), max(children_midis), self.midi_value,
                                              self.midi_value + range_,
                                              step=step)
        else:
            scale = scaledvalues.ScaledValues(max(children_midis), min(children_midis), self.midi_value,
                                              self.midi_value + range_,
                                              step=step)
        if not last:
            min_midi = min(children_midis)
            max_midi = max(children_midis)
            if self.midi_value == min_midi:
                children_midis.remove(max_midi)
            else:
                children_midis.remove(min_midi)
        for midi in children_midis:
            new_midi = scale(midi)
            choral_midis.append(new_midi)

        return choral_midis

    def get_children_score(self, score=None, show_fractal_orders=False, show_midis=False):
        if not score:
            score = self.get_score_template()

        old_tempo = None
        max_layers = max([child.number_of_layers for child in self.get_children()])
        for child in self.get_children():
            tempo = child.tempo
            if tempo == old_tempo:
                show_metronome = False
            else:
                show_metronome = True
            old_tempo = tempo
            child_score = child.get_score(layer_number=list(range(0, max_layers + 1)),
                                          show_fractal_orders=show_fractal_orders, show_midis=show_midis,
                                          barline='light-light', show_metronome=show_metronome)

            score.extend(child_score)

        score.accidental_mode = 'modern'
        score.get_measure(-1).set_barline_style('light-heavy')
        return score

    def get_root_score(self, score=None, layer_number=None, show_fractal_orders=False, show_midis=False
                       # , show_positions=False
                       ):

        if not score:
            score = self.get_score_template()

        try:
            return self.get_score(score=score, layer_number=layer_number, show_fractal_orders=show_fractal_orders,
                                  show_midis=show_midis)
        except SetTempoFirstException as err:
            if not self.get_children():
                raise err
            else:
                for child in self.get_children():
                    score.extend(
                        child.get_score(layer_number=layer_number, show_fractal_orders=show_fractal_orders,
                                        show_midis=show_midis, barline='light-light'))

        # if set_time_signatures:
        #     if layer_number == 0 or not self.get_children():
        #         score.set_time_signatures(quarter_durations=self.quarter_duration, barline_style='light-light', times=times)
        #     else:
        #         durations = [fractal_tree.quarter_duration for fractal_tree in self.get_children() if fractal_tree.quarter_duration != 0]
        #         score.set_time_signatures(
        #             durations=durations, barline_style='light-light', times=times)
        # else:

        score.accidental_mode = 'modern'

        # if show_positions:
        #     for node in self.get_children()[1:]:
        #         position_in_tree = float(node.position_in_tree)
        #         quarter_position_in_tree = position_in_tree * self.tempo / 60
        #         position_in_score = quarter_position_in_tree * 60 / self.score_tempo
        #         node.chord.add_words(
        #             Timing.get_clock(time=round(position_in_score, 1), mode='msreduced'),
        #             enclosure='rectangle', relative_y=40)
        score.get_measure(-1).set_barline_style('light-heavy')
        return score

    def get_score_template(self):
        score = TreeScoreTimewise()
        score.tuplet_line_width = 2.4
        score.page_style.orientation = 'landscape'
        score.page_style.system_distance = 180
        score.page_style.staff_distance = 150
        score.page_style.top_system_distance = 150
        score.page_style.bottom_margin = 100

        score.add_title('module: {}'.format(self.name))
        rounded_duration = round(float(self.duration), 1)
        if rounded_duration == int(rounded_duration):
            rounded_duration = int(rounded_duration)

        clock = Timing.get_clock(rounded_duration, mode='msreduced')
        score.add_subtitle(
            'duration: {}'.format(clock))
        score.accidental_mode = 'modern'
        return score

    def get_score(self, score=None, layer_number=None, show_fractal_orders=False, show_midis=None,
                  barline='light-heavy',
                  show_metronome=True):
        if not score:
            score = self.get_score_template()
        score.set_time_signatures(quarter_durations=self.quarter_duration)
        if show_fractal_orders:
            for node in self.traverse():
                if node.fractal_order is not None:
                    try:
                        node.chord.add_lyric(node.fractal_order)
                    except AttributeError:
                        try:
                            for chord in node.chord_field.chords:
                                chord.add_lyric(node.fractal_order)
                        except AttributeError:
                            for chord in node._simple_format.chords:
                                chord.add_lyric(node.fractal_order)
        if show_midis:
            for node in self.traverse():
                try:
                    node.chord.add_words(node.chord.midis)
                except AttributeError:
                    try:
                        for chord in node.chord_field.chords:
                            chord.add_words(chord.midis)
                    except AttributeError:
                        for chord in node.simple_format.chords:
                            chord.add_words(chord.midis)

        def layer_to_score(layer_number, part_number):
            try:
                sf = self.get_simple_format(layer_number)
                sf.auto_clef()
                v = sf.to_stream_voice(1)
                v.add_to_score(score, part_number=part_number)
            except ValueError:
                print('module {}: number_of_layers={}: getting layer {} not possible'.format(self.name,
                                                                                             self.number_of_layers,
                                                                                             i))

        if layer_number is None:
            for i, j in zip(range(self.number_of_layers + 1), range(1, self.number_of_layers + 2)):
                layer_to_score(i, j)

        elif hasattr(layer_number, '__iter__'):
            for i, j in zip(layer_number, range(1, len(layer_number) + 1)):
                layer_to_score(i, j)
        else:
            layer_to_score(layer_number, 1)

        if show_metronome:
            score.get_measure(1).get_part(1).add_metronome(per_minute=self.tempo, relative_y=40)
        score.get_measure(-1).set_barline_style(barline)
        return score

    def get_simple_format(self, layer=None):
        if layer is None:
            layer = self.get_farthest_leaf().get_distance()
        self.get_layer(layer=layer)

        simple_format = SimpleFormat()
        for node in basic_functions.flatten(self.get_layer(layer)):
            if node.chord is not None:
                if node.chord_field is not None:
                    raise ChordFieldConflict()
                if node._simple_format is not None:
                    raise SimpleFormatConflict()
                copied_chord = node.chord.__deepcopy__()
                simple_format.add_chord(copied_chord)
            elif node.chord_field is not None:
                if node._simple_format is not None:
                    raise SimpleFormatConflict()
                for chord in node.chord_field.chords:
                    copied_chord = chord.__deepcopy__()
                    simple_format.add_chord(copied_chord)
            elif node._simple_format is not None:
                for chord in node._simple_format.chords:
                    copied_chord = chord.__deepcopy__()
                    simple_format.add_chord(copied_chord)

            else:
                raise NoneChordException()

        return simple_format

    # set
    def set_chord(self, chord):
        self._chord = chord

    def set_none_tempi(self, val=60):
        try:
            self.tempo = val
        except TempoIsAlreadySet:
            pass
        except ChildTempoIsAlreadySet:
            for child in self.get_children():
                child.set_none_tempi(val=val)

    # others
    def change_midis(self):
        if not isinstance(self._midi_generator, RelativeMidi):
            raise TypeError(
                'set_reduced_auto_ranges can only be applied to FractalMusic nodes with RelativeMidi as midi_generator')
        else:

            directions = self.midi_generator.directions
            midi_range = self.midi_generator.midi_range
            microtone = self.midi_generator.microtone
            # print('inside'+ midi_range)
            # children = iter(self.get_children())
            # old_generated_midis = self.children_generated_midis
            # print("old_generated_midis", old_generated_midis)
            # self._children_generated_midis = [node.midi_value for node in self.get_children()]
            # self._children_generated_midis.append(old_generated_midis[-1])
            # print("new_generated_midis", old_generated_midis)

            self.midi_generator = None
            self.midi_generator.proportions = None
            self.midi_generator.midi_range = midi_range
            self.midi_generator.microtone = microtone
            self.midi_generator.directions = directions
            self._children_generated_midis = None

            for child in self.get_children():
                child.midi_value = None
                child._chord = None

            for child in self.get_children():
                if isinstance(child.midi_generator, RelativeMidi):
                    child.midi_generator.midi_range = None
                    child.midi_generator.directions = None
                    child.midi_generator.proportions = None
                    child.midi_generator._iterator = None
                    child._children_generated_midis = None

    def change_quarter_duration(self, new_quarter_duration):
        if new_quarter_duration is not None:
            if not self.tempo:
                raise SetTempoFirstException()
            try:
                self.change_value(Fraction(new_quarter_duration * 60, self.tempo))
            except TypeError:
                self.change_value(Fraction(Fraction(new_quarter_duration * 60), Fraction(self.tempo)))

    def create_segmented_line_group(self, layers=None, *show_attributes):
        # show_attributes: attr / (attr) / (attr, function/kwdict) / (attr, function, kwdict)
        def add_line_text_labels():
            for line, ch in zip(segmented_line.line_segments, self.get_children()):
                for attr_tuple in show_attributes:
                    attr_func = None
                    kwdict = None
                    if isinstance(attr_tuple, tuple):
                        for x in attr_tuple[1:]:
                            if isinstance(x, str):
                                attr_func = lambda y: getattr(ch, x)
                            if callable(x):
                                attr_func = x
                            elif isinstance(x, dict):
                                kwdict = x
                    else:
                        attr_func = lambda child: getattr(child, x)

                    label = line.start_mark_line.add_text_label(str(attr_func(ch)))
                    if kwdict:
                        for key in kwdict.keys():
                            setattr(label, key, kwdict[key])

        segmented_line_group = SegementedLineGroup()
        segmented_line_group.add_segemented_line(SegmentedLine(lengths=[ch.duration for ch in self.get_children()]))
        for segmented_line in segmented_line_group.get_segmented_lines():
            add_line_text_labels()
        return segmented_line_group

    def find_best_tempo_in_range(self, min_tempo=40, max_tempo=144):
        min_quarter_duration = ceil(Timing(duration=self.duration, tempo=min_tempo).quarter_duration)
        max_quarter_duration = floor(Timing(duration=self.duration, tempo=max_tempo).quarter_duration)
        tempi = [Timing(duration=self.duration, quarter_duration=x).tempo for x in
                 range(min_quarter_duration, max_quarter_duration + 1)]
        tempo_deltas = [abs(round(tempo) - tempo) for tempo in tempi]
        min_delta = min(tempo_deltas)
        index = tempo_deltas.index(min_delta)
        best_tempo = int(round(tempi[index]))
        return best_tempo

    def find_best_tempi_in_list(self, tempi):
        quarter_durations = [Timing(duration=self.duration, tempo=tempo).quarter_duration for tempo in tempi]
        quarter_duration_deltas = [abs(round(quarter_duration) - quarter_duration) for quarter_duration in
                                   quarter_durations]
        rounded_duration_deltas = [round(float(delta), 2) for delta in quarter_duration_deltas]

        min_delta = min(rounded_duration_deltas)
        indices = [i for i, quarter_duration_delta in enumerate(rounded_duration_deltas) if
                   quarter_duration_delta == min_delta]
        best_tempi = [tempi[index] for index in indices]
        return best_tempi

    def inverse_tree_directions(self):
        self.tree_directions = [direction * -1 for direction in self.tree_directions]

    def split(self, *proportions):
        if hasattr(proportions[0], '__iter__'):
            proportions = proportions[0]

        proportions = [Fraction(prop) for prop in proportions]

        for prop in proportions:
            duration = self.quarter_duration * prop / sum(proportions)
            new_node = self.copy()
            new_node.multi = self.multi
            new_node.quarter_duration = duration
            new_node._fractal_order = self.fractal_order
            new_node.midi_value = self.midi_value
            new_node.midi_generator.midi_range = self.midi_generator.midi_range
            if self._chord:
                new_node.set_chord(self.chord.__deepcopy__())
            self.add_child(new_node)

        return self.get_children()

    def quantize_leaves(self, grid_size):

        #     quantizing quarter_durations!
        leaves = list(self.traverse_leaves())
        quarter_durations = [leaf.quarter_duration for leaf in leaves]
        quantized_quarter_durations = get_quantized_values(quarter_durations, grid_size)
        for leaf, quantized_duration in zip(leaves, quantized_quarter_durations):
            leaf.change_quarter_duration(quantized_duration)

    def quantize_children(self, grid_size=0.5):
        #     quantizing quarter_durations!
        children = self.get_children()
        quarter_durations = [child.quarter_duration for child in children]
        quantized_quarter_durations = get_quantized_values(quarter_durations, grid_size)
        for child, quantized_duration in zip(children, quantized_quarter_durations):
            child.change_quarter_duration(quantized_duration)

    def recreate_segmented_line(self):
        self._segmented_line = None

    def reduce_children(self, condition):
        super().reduce_children(condition)

        try:
            self.change_midis()
        except TypeError:
            pass

    def reset_midis(self):
        for node in self.traverse():
            node.midi_value = None
            node.midi_generator = None
            node._children_generated_midis = None

    def round_leaves(self):
        #     quantizing quarter_durations!
        leaves = list(self.traverse_leaves())
        rounded_quarter_durations = [round(leaf.quarter_duration) for leaf in leaves]
        for leaf, rounded_quarter_duration in zip(leaves, rounded_quarter_durations):
            leaf.change_quarter_duration(rounded_quarter_duration)

    def round_children(self):
        children = self.get_children()
        rounded_quarter_durations = [round(child.quarter_duration) for child in children]
        for child, rounded_quarter_duration in zip(children, rounded_quarter_durations):
            child.change_quarter_duration(rounded_quarter_duration)

    def write_infos(self, file_name):
        os.system('touch ' + file_name)
        file = open(file_name, 'w')
        x = PrettyTable()

        x.field_names = ["name", "f_o", "quarters", "duration", "midi", "perm_ord", "multi", "directions",
                         "midi_range", "childr_midis"]

        for node in self.traverse():
            x.add_row([node.name, node.fractal_order, round(float(node.quarter_duration), 2),
                       Timing(quarter_duration=float(node.quarter_duration), tempo=self.tempo).clock,
                       node.midi_value,
                       node.permutation_order, node.multi, node.midi_generator.directions,
                       node.midi_generator.midi_range, node.children_generated_midis]
                      )

        if self.is_root:
            file.write('name: root')
        else:
            file.write('name: {} fo: {}'.format(self.name, self.fractal_order))
        file.write('\n')
        file.write(
            'quarter_duration: {}, tempo: {}, duration: {}'.format(round(float(self.quarter_duration), 2),
                                                                   self.tempo,
                                                                   round(float(self.duration), 2)))
        file.write('\n')
        file.write('tree directions: {}'.format(self.tree_directions))
        file.write('\n')
        file.write('\n')
        file.write(x.get_string())
        file.close()

    # //copy
    def copy(self):
        copied_midi_generator = self.midi_generator.copy()

        copied = super().copy()
        copied.tempo = self.tempo
        copied.midi_generator = copied_midi_generator
        copied.tree_directions = self.tree_directions
        copied.permute_directions = self.permute_directions

        if self.fertile is False:
            copied._midi_value = self._midi_value
        return copied

    def __deepcopy__(self, memodict={}):
        copied = super().__deepcopy__()
        copy_attribute_names = ['_chord_field', '_chord', '_midi_value', '_simple_format', '_midi_generator',
                                '_children_generated_midis', '_tree_directions', '_permute_directions', '_tempo']

        self.deepcopy_attributes(copied, copy_attribute_names)

        return copied

    def __copy__(self):
        copied = self.__class__(proportions=self.proportions, tree_permutation_order=self.tree_permutation_order)
        copied.duration = self.duration
        copied.midi_generator = None
        copied._tempo = self.tempo
        copied.quarter_duration = self.quarter_duration
        copied.tree_directions = self.tree_directions
        copied.permute_directions = self.permute_directions
        return copied
