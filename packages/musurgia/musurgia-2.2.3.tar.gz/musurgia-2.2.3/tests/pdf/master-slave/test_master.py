from musurgia.pdf.masterslave import Master, PositionMaster, MarginMaster
from musurgia.unittest import TestCase


class DummyMaster(Master):

    def get_slave_position(self, slave, position):
        pass

    def get_slave_margin(self, slave, margin):
        pass


class DummyPositionMaster(PositionMaster):
    def get_slave_position(self, slave, position):
        pass


class DummyMarginMaster(MarginMaster):
    def get_slave_margin(self, slave, margin):
        pass


class TestMaster(TestCase):
    def test_init(self):
        m = DummyMaster()
        self.assertTrue(isinstance(m, Master))

    def test_init_margin(self):
        m = DummyMarginMaster()
        self.assertTrue(isinstance(m, MarginMaster))

    def test_init_position(self):
        m = DummyPositionMaster()
        self.assertTrue(isinstance(m, PositionMaster))
