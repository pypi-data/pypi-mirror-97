import copy
from itertools import chain

from quicktions import Fraction

from musurgia.arithmeticprogression import ArithmeticProgression, DAndSError
from musurgia.basic_functions import dToX


class ValueGeneratorException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class GeneratorHasNoNextError(ValueGeneratorException):
    def __init__(self, generator, *args):
        msg = 'generator {} has no __next__'.format(generator)
        super().__init__(msg, *args)


class GeneratorNotIterableError(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class XOutOfRange(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class NoDurationError(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ArithmeticConflictError(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class PositionError(ValueGeneratorException):
    def __init__(self, position, duration, *args):
        msg = 'position {} must be smaller than duration {}'.format(position, duration)
        super().__init__(msg, *args)


class CallConflict(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ChildrenValueModeConflict(ValueGeneratorException):
    def __init__(self, children_value_modes, *args):
        msg = 'children have more than one value_mode: {}'.format(children_value_modes)
        super().__init__(msg, *args)


class ValueGeneratorTypeConflict(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ValueGenerator(object):
    def __init__(self, generator=None, value_mode=None, duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._generator = None
        self._duration = None
        self._position = 0
        self._children = None
        self._children_iterator = None

        self.generator = generator
        self.value_mode = value_mode
        self.duration = duration

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, val):
        if val and not callable(val) and not hasattr(val, '__next__'):
            raise TypeError('generator {} must have  __call__ or __next__ attribute'.format(val))
        self._generator = val

    def _set_generator_duration(self):
        if isinstance(self.generator, ArithmeticProgression) and self.value_mode in ['duration']:
            try:
                self.generator.s = self.duration
            except DAndSError:
                if self.generator.s != self.duration:
                    raise ArithmeticConflictError()
        elif hasattr(self.generator, 'quarter_duration'):
            self.generator.quarter_duration = self.duration
        elif hasattr(self.generator, 'duration'):
            self.generator.duration = self.duration
        else:
            pass

    @property
    def value_mode(self):
        if self.children:
            if self._value_mode is None:
                children_value_modes = list(
                    dict.fromkeys([child.value_mode for child in self.children if child.value_mode is not None])
                )
                if not children_value_modes:
                    return None
                elif len(children_value_modes) > 1:
                    raise ChildrenValueModeConflict(children_value_modes)
                else:
                    return children_value_modes[0]
            else:
                for child in self.children:
                    child.value_mode = self._value_mode

        return self._value_mode

    @value_mode.setter
    def value_mode(self, val):
        permitted = [None, 'duration', 'midi', 'chord']
        if val not in permitted:
            raise ValueError('value_mode.value {} must be in {}'.format(val, permitted))
        self._value_mode = val

    @property
    def duration(self):
        if self.children:
            children_durations = [child.duration for child in self.children]
            if None in children_durations:
                return None
            else:
                return sum(children_durations)
        return self._duration

    @duration.setter
    def duration(self, val):
        if val is not None:
            if self.children:
                raise ValueGeneratorException('parent\'s duration cannot be set')
                # children_duration = [fractal_tree.duration for fractal_tree in self.children]
                # if None in children_duration:
                #     raise ValueGeneratorException(
                #         'ValueGenerator: parent\'s duration cannot be set if not all children have a duration.')
                # unit = Fraction(val, sum(children_duration))
                # for fractal_tree in self.children:
                #     fractal_tree.duration *= unit
        self._duration = val
        self._set_generator_duration()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        if val < 0:
            raise ValueError(float(val))
        self._position = val

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        if not isinstance(child, ValueGenerator):
            raise TypeError('fractal_tree must be of type ValueGenerator not{}'.format(type(child)))
        if self._children is None:
            self._children = []
        if self._children_iterator is None:
            self._children_iterator = iter([])
        child.parent_group = self
        self._children.append(child)
        self._children_iterator = chain(self._children_iterator, child)

    def _check_position(self):
        if not self.duration:
            raise NoDurationError()
        if not self.position < self.duration:
            raise PositionError(self.position, self.duration)

    def _change_position_in_duration(self, value):
        if self.value_mode == 'duration':
            self.position += value
        elif self.value_mode == 'chord':
            self.position += value.quarter_duration

    def __next__(self):
        try:
            return self.__call__(self.position)
        except (ValueError, PositionError):
            raise StopIteration()

    def __call__(self, x):
        self.position = x
        self._check_position()
        output = None
        if self.children:
            durations = [vg.duration for vg in self.children]
            duration_limits = dToX(durations)
            for i in range(len(duration_limits) - 1):
                if duration_limits[i] <= x < duration_limits[i + 1]:
                    output = self.children[i](x - duration_limits[i])
                    break
        elif callable(self.generator):
            output = self.generator.__call__(x)
        else:
            # if isinstance(self.generator, ArithmeticProgression):
            #     raise CallConflict('Calling Arithmetic Progression is not allowed.')
            output = self.generator.__next__()
        self._change_position_in_duration(output)
        return output

    def __iter__(self):
        return self

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(value_mode=self.value_mode,
                                duration=self.duration)
        if self.generator is not None:
            copied.generator = copy.deepcopy(self.generator)
        if self.children is not None:
            for child in self.children:
                copied.add_child(child.__deepcopy__())
        return copied

# class ValueGeneratorGroup(object):
#     def __init__(self, *value_generators, **kwargs):
#         super().__init__(**kwargs)
#         self._value_generators = None
#         self._value_generators_iterator = None
#         self._child_type = None
#         self._current_value_generator = None
#         self.value_generators = value_generators
#
#     @property
#     def value_generators(self):
#         return self._value_generators
#
#     @value_generators.setter
#     def value_generators(self, values):
#         try:
#             values = list(values)
#         except TypeError:
#             values = [values]
#
#         for value in values:
#             self.add_value_generator(value)
#
#     @property
#     def duration(self):
#         try:
#             return sum([vg.duration for vg in self.value_generators])
#         except AttributeError:
#             return 0
#
#     def add_value_generator(self, value_generator):
#         if not isinstance(value_generator, ValueGenerator):
#             raise TypeError('value_generators must be of type ValueGenerator not{}'.format(type(value_generator)))
#         if self._value_generators is None:
#             self._value_generators = []
#         if self._value_generators_iterator is None:
#             self._value_generators_iterator = iter([])
#         value_generator.parent_group = self
#         self._value_generators.append(value_generator)
#         self._value_generators_iterator = chain(self._value_generators_iterator, value_generator)
#
#     def __next__(self):
#         return self._value_generators_iterator.__next__()
#
#     def __iter__(self):
#         return self
#
#     def __call__(self, x):
#         durations = [vg.duration for vg in self.value_generators]
#         duration_limits = dToX(durations)
#         for i in range(len(duration_limits) - 1):
#             if duration_limits[i] <= x < duration_limits[i + 1]:
#                 return self.value_generators[i](x - duration_limits[i])
