from pathlib import Path

from musurgia.pdf.line import StraightLine
from musurgia.pdf.masterslave import Master
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class DummyMaster(Master):
    def get_slave_margin(self, slave, margin):
        return 10

    def get_slave_position(self, slave, position):
        return 20


class TestStraightLine(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.master = DummyMaster()
        self.sl = StraightLine(mode='h', length=20, name='straight_test', master=self.master)

    def test_relative_x(self):
        actual = self.sl.relative_x
        expected = self.master.get_slave_position(self.sl, 'x')
        self.assertEqual(expected, actual)

    def test_get_relative_x(self):
        actual = self.sl.get_relative_x2()
        expected = self.sl.relative_x + self.sl.length
        self.assertEqual(expected, actual)

    def test_get_width(self):
        actual = self.sl.get_width()
        expected = self.sl.left_margin + self.sl.length + self.sl.right_margin
        self.assertEqual(expected, actual)

    def test_get_height(self):
        actual = self.sl.get_height()
        expected = self.sl.top_margin + self.sl.bottom_margin
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.sl.draw(self.pdf)
            self.pdf.write(pdf_path)
