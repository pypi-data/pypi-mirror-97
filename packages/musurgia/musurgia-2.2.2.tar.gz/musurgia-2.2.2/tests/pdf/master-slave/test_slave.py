from musurgia.pdf.masterslave import Master, PositionMaster, MarginMaster, Slave, PositionSlave, MarginSlave
from musurgia.pdf.newdrawobject import DrawObject
from musurgia.unittest import TestCase


class DummyMaster(Master):

    def get_slave_position(self, slave, position):
        pass

    def get_slave_margin(self, slave, margin):
        if margin in ['t', 'top']:
            return 10


class DummyPositionMaster(PositionMaster):
    def get_slave_position(self, slave, position):
        pass


class DummyMarginMaster(MarginMaster):
    def get_slave_margin(self, slave, margin):
        if margin in ['t', 'top']:
            return 20


class DummyMarginSlave(DrawObject, MarginSlave):
    def get_relative_y2(self):
        return 'dummy'

    def get_relative_x2(self):
        return 'dummy'

    def draw(self, pdf):
        return 'dummy'


class TestSlave(TestCase):
    def test_slave_init(self):
        s = Slave(name='test_slave', master=DummyMaster())
        self.assertTrue(isinstance(s, Slave))

    def test_position_slave_init(self):
        s = PositionSlave(name='test_position_slave', master=DummyPositionMaster())
        self.assertTrue(isinstance(s, PositionSlave))

    def test_margin_slave_init(self):
        s = MarginSlave(name='test_margin_slave', master=DummyMarginMaster())
        self.assertTrue(isinstance(s, MarginSlave))

    def test_margin_slave_top(self):
        m = DummyMarginMaster()
        s = MarginSlave(name='test_margin_slave', master=m)

        actual = s.top_margin
        expected = m.get_slave_margin(s, 't')
        self.assertTrue(expected, actual)

    def test_margin_slave_position(self):
        m = DummyMarginMaster()
        s = DummyMarginSlave(name='test_margin_slave', master=m)
        s.relative_x = 10
