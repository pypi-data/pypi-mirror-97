import math

from quicktions import Fraction


class ArithmeticProgressionError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


class DAndSError(ArithmeticProgressionError):
    def __init__(self, *args):
        msg = 'you cannot set both d an s!'
        super().__init__(msg, *args)


class ArithmeticProgression(object):
    def __init__(self, a1=None, an=None, n=None, d=None, s=None, correct_s=False):
        self._a1 = None
        self._an = None
        self._n = None
        self._d = None
        self._s = None
        self._current = None
        self._index = None
        self._correction_factor = None
        self._correct_s = None

        self.a1 = a1
        self.an = an
        self.n = n
        self.d = d
        self.s = s
        self.correct_s = correct_s

    def _to_fraction(self, value):
        if not isinstance(value, Fraction):
            value = Fraction(value)
        return value

    def _check_args(self, arg=None):
        if arg is None:
            err = 'Not enough attributes are set. Three are needed!'
            if len([v for v in self._parameters_dict.values() if v is not None]) < 3:
                raise AttributeError(err)
        else:
            if self._parameters_dict[arg] is None and len(
                    [v for v in self._parameters_dict.values() if v is not None]) > 2:
                err = 'attribute cannot be set. Three parameters are already set. ArithmeticProgression is already ' \
                      'created!'
                raise AttributeError(err)

    def _calculate_a1(self):
        if self._d is None:
            # self._a1 = (2. * self.s / self.n) - self.an
            self._a1 = Fraction(2 * self.s, self.n) - self.an
        else:
            self._a1 = self.an - ((self.n - 1) * self.d)

    def _calculate_an(self):
        if self._s is None:
            self._an = self.a1 + (self.n - 1) * self.d
        else:
            self._an = Fraction(2 * self.s, self.n) - self.a1
            # self._an = (2. * self.s / self.n) - self.a1

    def _calculate_n(self):
        if self._s is None:
            self._n = Fraction((self.an - self.a1), self.d) + 1
        else:
            self._n = 2 * Fraction(self.s, (self.a1 + self.an))
        self._n = Fraction(int(float(self._n)))

    def _calculate_d(self):
        if self.n == 1:
            self._d = 0
        elif self._a1 is None:
            self._calculate_a1()
            # self._d = Fraction(Fraction(self.an - self.a1), Fraction(self.n - 1))
            self._d = Fraction((self.an - self.a1), (self.n - 1))
            # self._d = (self.an - self.a1) / (self.n - 1)
        elif self._an is None:
            # self._d = Fraction(Fraction((self.s - (self.n * self.a1)) * 2), Fraction((self.n - 1) * self.n))
            self._d = Fraction(((self.s - (self.n * self.a1)) * 2), ((self.n - 1) * self.n))
            # self._d = ((self.s - (self.n * self.a1)) * 2) / ((self.n - 1) * self.n)
        elif self._n is None:
            self._calculate_n()
            # self._d = Fraction(Fraction(self.an - self.a1), Fraction(self.n - 1))
            self._d = Fraction((self.an - self.a1), (self.n - 1))
            # self._d = (self.an - self.a1) / (self.n - 1)
        else:
            self._d = Fraction((self.an - self.a1), (self.n - 1))
            # self._d = (self.an - self.a1) / (self.n - 1)

    def _calculate_s(self):
        if self._a1 is None:
            self._calculate_a1()
            self._s = (self.a1 + self.an) * Fraction(self.n, 2)
        elif self._an is None:
            self._s = self.n * self.a1 + ((self.n - 1) * Fraction(self.n, 2)) * self.d
        elif self._n is None:
            self._calculate_n()
            self._s = (self.a1 + self.an) * Fraction(self.n, 2)
        else:
            self._s = (self.a1 + self.an) * Fraction(self.n, 2)

    @property
    def _parameters_dict(self):
        return {'a1': self._a1, 'an': self._an, 'n': self._n, 'd': self._d, 's': self._s}

    @property
    def parameters_dict(self):
        return {'a1': self.a1, 'an': self.an, 'n': self.n, 'd': self.d, 's': self.s}

    @property
    def a1(self):
        if self._a1 is None:
            self._calculate_a1()
        return self._a1

    @a1.setter
    def a1(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('a1')
        self._a1 = value

    @property
    def an(self):
        if self._an is None:
            self._calculate_an()
        return self._an

    @an.setter
    def an(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('an')
        self._an = value

    @property
    def n(self):
        if self._n is None:
            self._calculate_n()
        return self._n

    @n.setter
    def n(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise AttributeError('n {} must be int'.format(value))
            self._check_args('n')
        self._n = value

    @property
    def s(self):
        if self._s is None:
            self._calculate_s()
        return self._s

    @s.setter
    def s(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('s')
            if self._d is not None:
                raise DAndSError()
        self._s = value

    @property
    def d(self):
        if self._d is None:
            self._calculate_d()
        return self._d

    @d.setter
    def d(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('d')
            if self._s is not None:
                raise DAndSError()
        self._d = value

    @property
    def correct_s(self):
        return self._correct_s

    @correct_s.setter
    def correct_s(self, val):
        if not isinstance(val, bool):
            raise TypeError('correct_s.value must be of type bool not{}'.format(type(val)))
        self._correct_s = val

    @property
    def correction_factor(self):
        def _calculate_correction_factor():
            if self.correct_s:
                actual_s = self.n * Fraction((self.a1 + self.an), 2)
                factor = Fraction(self.s, actual_s)
                return factor
            else:
                return 1

        if self._correction_factor is None:
            self._correction_factor = _calculate_correction_factor()
        return self._correction_factor

    def __iter__(self):
        return self

    def __next__(self):
        if self._current is None:
            self._check_args()
        parameters = [self.a1, self.an, self.n, self.s, self.d]

        if len([v for v in parameters if v is not None]) < 5:
            err = 'Not enough parameter set to create an arithmetic progression. 3 parameters should be set first (s ' \
                  'and d cannot be set together) '
            raise Exception(err)

        if self._current is None:
            self._current = self.a1
            self._index = 0
        else:
            self._index += 1
            self._current += self.d

        if self._index < self.n:
            return self._current * self.correction_factor
        else:
            raise StopIteration()

    @property
    def index(self):
        return self._index

    # def rest(self):
    #     self._current = None

    def __deepcopy__(self, memodict={}):
        copy = self.__class__(correct_s=self.correct_s)
        copy._a1 = self._a1
        copy._an = self._an
        copy._n = self._n
        copy._d = self._d
        copy._s = self._s
        return copy
