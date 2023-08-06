from quicktions import Fraction

from musurgia.random import Random


class Interpolation(object):
    def __init__(self, start, end, duration=None, key=None, grid=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = None
        self._end = None
        self._duration = None
        self._grid = None

        self.start = start
        self.end = end
        self.duration = duration
        self.key = key
        self.grid = grid

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        self._start = val

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, val):
        self._end = val

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, val):
        if val and not isinstance(val, Fraction):
            val = Fraction(val)
        self._duration = val

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, val):
        self._grid = val

    def _check_grid(self, val):
        if self.grid:
            return round(val / self.grid) * self.grid
        else:
            return val

    def __call__(self, x):
        self._check_x(x)
        output = Fraction(Fraction(x * (self.end - self.start)), self.duration) + self.start
        output = self._check_grid(output)
        if self.key:
            return self.key(output)
        return output

    def _check_x(self, x):
        if x < 0 or x > self.duration:
            raise ValueError()


class InterpolationGroup(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interpolations = []

    def add_interpolation(self, interpolation):
        if not isinstance(interpolation, Interpolation):
            raise TypeError
        self._interpolations.append(interpolation)

    def add_section(self, start, end, duration):
        interpolation = Interpolation(start, end, duration)
        self.add_interpolation(interpolation)

    def __call__(self, x):
        temp_x = x
        for interpolation in self._interpolations:
            try:
                return interpolation.__call__(temp_x)
            except ValueError:
                temp_x -= interpolation.duration

        raise ValueError(x)


class RandomInterpolation(Interpolation):
    def __init__(self, periodicity=None, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._random = Random(periodicity=periodicity, seed=seed)

    @Interpolation.start.setter
    def start(self, val):
        if not hasattr(val, '__iter__'):
            val = [val]

        self._start = val
        self._check_pool_length()

    @Interpolation.end.setter
    def end(self, val):
        if not hasattr(val, '__iter__'):
            val = [val]
        self._end = val
        self._check_pool_length()

    def _check_pool_length(self):
        if self.start and self.end:
            if len(self.start) != len(self.end):
                return ValueError('start and end must be of the same length.')

    def _get_pool(self, x):
        pools = self.start + self.end
        pool_size = len(self.start)
        first_index = int(round(Interpolation(start=0, end=pool_size, duration=self.duration)(x)))
        pool = pools[first_index:first_index + pool_size]

        return pool

    def __call__(self, x):
        self._check_x(x)
        self._random.pool = self._get_pool(x)
        output = self._random.__next__()
        if self.key:
            return self.key(output)
        return output

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(start=self.start, end=self.end, duration=self.duration, key=self.key)
        copied._random = self._random.__deepcopy__()
        return copied
