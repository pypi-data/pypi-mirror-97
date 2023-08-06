from musurgia.random import Random


class ReadAList(object):
    ##mode in forwards, backwards, zickzack, random
    def __init__(self, pool=None, mode='random', seed=None):
        self._pool = None
        self._mode = None
        self._random = None
        self._index = None
        self._direction = 1
        self._next_index = None

        self.pool = pool
        self.mode = mode
        self.seed = seed

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, values):
        if values is not None:
            try:
                self._pool = list(values)
            except:
                self._pool = [values]
        self.random.pool = self.pool

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in ['forwards', 'backwards', 'zickzack', 'random']:
            err = 'mode can only be forwards, backwards, zickzack or random'
            raise ValueError(err)
        self._mode = value

    @property
    def random(self):
        if self._random is None:
            self._random = Random()
        return self._random

    @property
    def seed(self):
        return self.random.seed

    @seed.setter
    def seed(self, value):
        self.random.seed = value

    @property
    def next_index(self):
        err = 'next_index can only be set'
        raise AttributeError(err)

    @next_index.setter
    def next_index(self, value):
        self._next_index = value

    def _set_next_index(self):

        if self.mode == 'forwards':
            self._direction = 1

        elif self.mode == 'backwards':
            self._direction = -1

        elif self.mode == 'zickzack':
            pass

        self._index += self._direction

    def _check_index(self):
        if self.mode == 'forwards':
            if self._index >= len(self.pool):
                self._index = 0

        elif self.mode == 'backwards':
            if self._index >= len(self.pool):
                self._index = len(self.pool) - 1
            elif self._index < 0:
                self._index = len(self.pool) - 1

        elif self.mode == 'zickzack':
            if self._index == len(self.pool) - 1:
                self._direction = -1

            elif self._index > len(self.pool) - 1:
                self._index = len(self.pool) - 1
                self._direction = -1

            elif self._index == 0:
                self._direction = 1

            elif self._index < 0:
                self._index = 1
                self._direction = 1

    def next(self):
        if self.pool is None:
            err = 'pool can not be None'
            raise AttributeError(err)

        if self.mode != 'random':
            # print 'read_a_list.next(): self.mode=',self.mode
            # print 'read_a_list.next(): self._next_index=',self._next_index

            if self._next_index is None and self._index is None:
                if self.mode == 'backwards':
                    self._next_index = len(self.pool) - 1
                else:
                    self._next_index = 0

            if self._next_index is None:
                self._set_next_index()
            else:
                self._index = self._next_index
                self._next_index = None

            self._check_index()
            # print 'read_a_list.next(): self._index after check=',self._index
            # print 'read_a_list.next(): self.pool', self.pool
            return self.pool[self._index]

        else:
            return self.random.next()
