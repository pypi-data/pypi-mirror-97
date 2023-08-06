class AGRandom(object):
    import random
    current_random = random

    def __init__(self, pool=None, periodicity=None, forbidden_list=None, seed=None):
        self._pool = None
        self._periodicity = None
        self._forbidden_list = None
        self._seed = None
        self._counter = 0
        self._result = None

        self.pool = pool
        self.periodicity = periodicity
        self.forbidden_list = forbidden_list
        self.seed = seed

    # periodicity None will sets the periodicity always to len(pool)-2
    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, values):
        if values is not None:
            try:
                self._pool = list(dict.fromkeys(values))
            except TypeError:
                self._pool = [values]

    @property
    def periodicity(self):
        return self._periodicity

    @periodicity.setter
    def periodicity(self, value):
        if value is not None:
            if isinstance(value, int) and value >= 0:
                self._periodicity = value
            else:
                raise ValueError()

    @property
    def forbidden_list(self):
        if not self._forbidden_list:
            self._forbidden_list = []
        return self._forbidden_list

    @forbidden_list.setter
    def forbidden_list(self, values):
        self._forbidden_list = values

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        self.current_random.seed(value)

    @property
    def counter(self):
        return self._counter

    @property
    def result(self):
        if self._result is None:
            self._result = []
        return self._result

    @property
    def iterator(self):

        if not self.pool:
            raise AttributeError('set pool')

        while True:
            periodicity = self.periodicity
            if self.periodicity is None:
                periodicity = len(self.pool) - 2

            elif self.periodicity >= len(self.pool):
                periodicity = len(self.pool) - 1

            if periodicity < 0: periodicity = 0

            def check(x):

                def forbid_element(x):
                    if len(self.forbidden_list) >= periodicity:
                        self.forbidden_list.pop(0)
                    self.forbidden_list.append(x)

                if periodicity != 0:
                    if x in self.forbidden_list:
                        return False
                    else:
                        forbid_element(x)
                        return True
                else:
                    return True

            if len(self.forbidden_list) > periodicity:
                # print "self.periodicity", self.periodicity
                self.forbidden_list = self.forbidden_list[(-1 * periodicity):]

            random_element = self.pool[self.current_random.randrange(len(self.pool))]
            while check(random_element) is False:
                random_element = self.pool[self.current_random.randrange(len(self.pool))]

            yield random_element

    def __next__(self):
        next_el = self.iterator.__next__()
        self._counter += 1
        # self._sum+=next_el
        self.result.append(next_el)

        return next_el

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(pool=self.pool, periodicity=self.periodicity, forbidden_list=self.forbidden_list,
                                seed=self.seed)
        return copied
