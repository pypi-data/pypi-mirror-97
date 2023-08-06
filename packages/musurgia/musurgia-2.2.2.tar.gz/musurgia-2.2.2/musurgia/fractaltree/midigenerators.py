import itertools

from musicscore import basic_functions
from musicscore.musictree.midi import MidiNote

from musurgia.random import Random
from musurgia.quantize import get_quantized_positions


class MidiGenerator(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node = None

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    def next(self):
        err = str(type(self)) + ' should override next()'
        raise ImportWarning(err)

    def copy(self):
        err = str(type(self)) + ' should override copy()'
        raise ImportWarning(err)


class RelativeMidi(MidiGenerator):
    def __init__(self, midi_range=None, proportions=None, directions=None, microtone=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._midi_range = None
        self._proportions = None
        self._directions = None
        self._microtone = None
        self._iterator = None
        self._direction_iterator = None

        self.midi_range = midi_range
        self.proportions = proportions
        self.directions = directions
        self.microtone = microtone

        self._auto_ranged = False

    @property
    def midi_range(self):
        return self._midi_range

    @midi_range.setter
    def midi_range(self, values):
        def get_midi_note_values():
            output = values
            for index, v in enumerate(values):
                if isinstance(v, MidiNote):
                    output[index] = v.value
            return output

        if values:

            try:
                if not hasattr(values, '__iter__'):
                    values = [values, values]
                if len(values) == 1:
                    value = values[0]
                    values = [value, value]

                if len(values) != 2:
                    raise ValueError('wrong length for midi_range')
            except:
                raise TypeError('wrong type for midi_range')

            values = get_midi_note_values()

            if min(values) < 18:
                raise ValueError('midi cannot be smaller than 18')

            self._midi_range = values
        else:
            self._midi_range = None

    @property
    def proportions(self):
        if not self._proportions:
            try:
                self.proportions = self.node.children_fractal_values
            except Exception as err:
                pass
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values is not None:
            self._proportions = [value / sum(values) * 100 for value in values]
        else:
            self._proportions = None

    @property
    def directions(self):
        return self._directions

    @directions.setter
    def directions(self, values):
        # print('directions {} setting for {} and node {}'.format(values, self, self.node))
        if values:
            for value in values:
                if value not in [-1, 1]:
                    raise ValueError('directions can only be 1 or -1')

            self._directions = values
            self._direction_iterator = itertools.cycle(self._directions)
        else:
            self._directions = None
            self._direction_iterator = None

    def set_directions(self, *values):
        if len(values) != len(self.proportions):
            raise ValueError(
                "values length {} must equal proportions length {}".format(len(values), len(self.proportions)))
        self.directions = list(values)
        if self.node:
            root = self.node.get_root()
            if root.permute_directions:
                permutation_dict = {}
                for index, order in enumerate(root.permutation_order):
                    permutation_dict[order] = self.directions[index]
                keys = sorted(permutation_dict.keys())
                tree_directions = [permutation_dict[key] for key in keys]
                root.tree_directions = tree_directions
            else:
                root.tree_directions = self.directions

    @property
    def direction_iterator(self):
        return self._direction_iterator

    @property
    def microtone(self):
        return self._microtone

    @microtone.setter
    def microtone(self, value):
        if value and value not in [2, 4, 8]:
            raise ValueError('microtone can only be 2,4,8 or None')
        self._microtone = value

    @property
    def iterator(self):

        if self._iterator is None:
            def scale(old_value, old_lower_limit, old_higher_limit, new_lower_limit, new_higher_limit):
                old_range = old_higher_limit - old_lower_limit
                if old_range == 0:
                    new_value = new_lower_limit
                else:
                    new_range = (new_higher_limit - new_lower_limit)
                    new_value = (((old_value - old_lower_limit) * new_range) / old_range) + new_lower_limit
                return new_value

            if not self.directions:
                raise AttributeError('set directions')
            if not self.proportions:
                raise AttributeError('set proportions')
            if not self.midi_range:
                raise AttributeError('set midi_range')
            if not self.microtone:
                raise AttributeError('set microtone')

            intervals = [proportion * self.direction_iterator.__next__() for proportion in self.proportions]
            midis = basic_functions.dToX(intervals)
            midis = [scale(midi, min(midis), max(midis), min(self.midi_range), max(self.midi_range)) for midi in midis]

            grid = 2 / self.microtone
            quantized_positions = get_quantized_positions(midis, grid_size=grid)
            quantized_midis = [float(midi) for midi in quantized_positions]

            self._iterator = iter(quantized_midis)

        return self._iterator

    def next(self):
        return self.iterator.__next__()

    def copy(self):
        return self.__class__(microtone=self.microtone)

    def __deepcopy__(self, memodict={}):
        return self.__class__(midi_range=self.midi_range, proportions=self.proportions, directions=self.directions,
                              microtone=self.microtone)


class RandomMidi(MidiGenerator):
    def __init__(self, pool=None, periodicity=None, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_random = Random()

        self.pool = pool
        self.periodicity = periodicity
        self.seed = seed

    @property
    def my_random(self):
        return self._my_random

    @property
    def seed(self):
        return self.my_random.seed

    @seed.setter
    def seed(self, value):
        self.my_random.seed = value

    @property
    def pool(self):
        return self._my_random.pool

    @pool.setter
    def pool(self, values):
        if values is not None:
            if min(values) < 18:
                raise ValueError('midi cannot be smaller than 18')

            self._my_random.pool = list(set(values))
        else:
            self._my_random.pool = None

    @property
    def periodicity(self):
        return self._my_random.periodicity

    @periodicity.setter
    def periodicity(self, value):
        self._my_random.periodicity = value

    @property
    def iterator(self):
        return self.my_random

    def next(self):
        return self.my_random.__next__()

    def copy(self):
        return self.__class__(pool=self.pool, seed=self.seed, periodicity=self.periodicity)
