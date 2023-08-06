from pathlib import Path

from musurgia.pdf.line import VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestVerticalLineSegment(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.vls = VerticalLineSegment(length=10)

    def test_get_relative_x2(self):
        actual = self.vls.get_relative_x2()
        expected = self.vls.get_width()
        self.assertEqual(expected, actual)

    def test_start_mark_line_relative_x(self):
        actual = self.vls.start_mark_line.relative_x
        expected = -1.5
        self.assertEqual(expected, actual)

    def test_start_mark_line_relative_y(self):
        actual = self.vls.start_mark_line.relative_y
        expected = self.vls.relative_y
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_y(self):
        actual = self.vls.end_mark_line.relative_y
        expected = self.vls.relative_y + self.vls.length
        self.assertEqual(expected, actual)

    def test_end_mark_line_relative_x(self):
        actual = self.vls.end_mark_line.relative_x
        expected = -1.5
        self.assertEqual(expected, actual)

    def test_start_mark_line_top_margin(self):
        actual = self.vls.start_mark_line.top_margin
        expected = 0
        self.assertEqual(expected, actual)

    def test_get_width(self):
        actual = self.vls.get_width()
        expected = 3
        self.assertEqual(expected, actual)

    def test_draw(self):
        with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            self.vls.end_mark_line.show = True
            self.vls.draw(self.pdf)
            self.pdf.write(pdf_path)
