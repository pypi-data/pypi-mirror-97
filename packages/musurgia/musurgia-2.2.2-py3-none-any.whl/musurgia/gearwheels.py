from musicscore.basic_functions import lcm, xToD


class Position:
    def __init__(self, value, wheel):
        self._value = None
        self._wheel = None
        self.value = value
        self.wheel = wheel

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def wheel(self):
        return self._wheel

    @wheel.setter
    def wheel(self, val):
        if not isinstance(val, Wheel):
            raise TypeError('wheel.value must be of type Wheel not{}'.format(type(val)))
        self._wheel = val


class Wheel:
    def __init__(self, size, start=0):
        self._size = None
        self._start = None
        self._number_of_cycles = None
        self.size = size
        self.start = start
        self.index = None

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        if not isinstance(val, int):
            raise TypeError(f'size.value must be of type int not{type(val)}')
        self._size = val

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        self._start = val

    def get_positions(self, number_of_cycles=None):
        if not number_of_cycles:
            number_of_cycles = self._number_of_cycles
        if not number_of_cycles or not isinstance(number_of_cycles, int) or number_of_cycles < 0:
            raise AttributeError(f'number_of_cycles must be a positive non zero int not {number_of_cycles}')
        position_values = list(range(self.start, number_of_cycles * self.size + self.start, self.size))
        return [Position(value, self) for value in position_values]

    def get_position_values(self):
        position_values = [p.value for p in self.get_positions()]
        return list(dict.fromkeys(position_values))


class GearWheels:
    def __init__(self, wheels):
        self._wheels = None
        self._positions = None
        self._iterator = None

        self.wheels = wheels

    def _set_positions(self):
        _positions = []
        _lcm = lcm(self.gear_sizes)
        for wheel in self.wheels:
            number_of_cycles = (_lcm // wheel.size) + 1
            wheel._number_of_cycles = number_of_cycles
            _positions.extend(wheel.get_positions())
        self._positions = sorted(_positions, key=lambda p: (p.value, p.wheel.index))

    # public properties

    @property
    def gear_sizes(self):
        return [wheel.size for wheel in self.wheels]

    @property
    def wheels(self):
        return self._wheels

    @wheels.setter
    def wheels(self, vals):
        for val in vals:
            if not isinstance(val, Wheel):
                raise TypeError(f'{val} must be of type Wheel not {type(val)} ')
        self._wheels = []
        for index, wheel in enumerate(vals):
            wheel.index = index
            self._wheels.append(wheel)
        self._set_positions()

    # get
    def get_positions(self):
        return self._positions

    def get_position_values(self):
        position_values = [p.value for p in self.get_positions()]
        return list(dict.fromkeys(position_values))

    def get_rhythm(self):
        return xToD(self.get_position_values())
