from abc import ABC, abstractmethod

from musurgia.pdf.margined import MarginNotSettableError
from musurgia.pdf.positioned import RelativePositionNotSettableError


class _GetSlavePositionMixIn(ABC):
    @abstractmethod
    def get_slave_position(self, slave, position):
        pass


class _GetSlaveMarginMixIn(ABC):
    @abstractmethod
    def get_slave_margin(self, slave, margin):
        pass


class _SetSlavePositionMixIn:
    @property
    def relative_x(self):
        return self.master.get_slave_position(slave=self, position='x')

    @relative_x.setter
    def relative_x(self, val):
        if val is not None:
            raise RelativePositionNotSettableError()

    @property
    def relative_y(self):
        return self.master.get_slave_position(slave=self, position='y')

    @relative_y.setter
    def relative_y(self, val):
        if val is not None:
            raise RelativePositionNotSettableError()


class _SetSlaveMarginMixIn:
    @property
    def left_margin(self):
        return self.master.get_slave_margin(slave=self, margin='left')

    @left_margin.setter
    def left_margin(self, val):
        if val is not None:
            raise MarginNotSettableError()

    @property
    def top_margin(self):
        return self.master.get_slave_margin(slave=self, margin='top')

    @top_margin.setter
    def top_margin(self, val):
        if val is not None:
            raise MarginNotSettableError()

    @property
    def right_margin(self):
        return self.master.get_slave_margin(slave=self, margin='right')

    @right_margin.setter
    def right_margin(self, val):
        if val is not None:
            raise MarginNotSettableError()

    @property
    def bottom_margin(self):
        return self.master.get_slave_margin(slave=self, margin='bottom')

    @bottom_margin.setter
    def bottom_margin(self, val):
        if val is not None:
            raise MarginNotSettableError()


class _Named:
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if val and not isinstance(val, str):
            raise TypeError(f"name.value must be of type str not{type(val)}")
        self._name = val


class PositionMaster(_GetSlavePositionMixIn):
    pass


class MarginMaster(_GetSlaveMarginMixIn):
    pass


class Master(_GetSlavePositionMixIn, _GetSlaveMarginMixIn):
    pass


class PositionSlave(_Named, _SetSlavePositionMixIn):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master = None
        self.master = master

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, val):
        if val and not isinstance(val, PositionMaster):
            raise TypeError(f"master.value must be of type {PositionMaster} not {type(val)}")
        self._master = val


class MarginSlave(_Named, _SetSlaveMarginMixIn):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master = None
        self.master = master

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, val):
        if val and not isinstance(val, MarginMaster):
            raise TypeError(f"master.value must be of type {MarginMaster} not {type(val)}")
        self._master = val


class Slave(_Named, _SetSlavePositionMixIn, _SetSlaveMarginMixIn):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master = None
        self.master = master

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, val):
        if val and not isinstance(val, Master):
            raise TypeError(f"master.value must be of type {Master} not {type(val)}")
        self._master = val
