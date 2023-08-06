from pathlib import Path

from musurgia.pdf.line import HorizontalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestHorizontalSegmentedLine(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()
        self.hsl = HorizontalSegmentedLine(lengths=[10, 15, 20, 25])

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            with self.file_path(parent_path=path, name='draw', extension='pdf') as pdf_path:
                self.pdf.translate_page_margins()
                self.pdf.draw_ruler('h')
                self.pdf.draw_ruler('v')
                self.pdf.translate(10, 10)
                self.hsl.draw(self.pdf)
                self.pdf.write(pdf_path)

    def test_get_height(self):
        self.hsl.segments[1].start_mark_line.length = 5
        actual = self.hsl.get_height()
        expected = 5
        self.assertEqual(expected, actual)

    def test_add_label_left(self):
        self.hsl.add_label('first left label', placement='left')
        self.hsl.add_label('second left label', placement='left')
        self.hsl.add_label('third left label', placement='left')
        self.hsl.add_label('fourth left label', placement='left')
        self.hsl.segments[0].start_mark_line.length = 10
        self.pdf.translate_page_margins()
        self.pdf.draw_ruler('h')
        self.pdf.draw_ruler('v')
        self.pdf.translate(20, 20)
        self.hsl.draw(self.pdf)
        # print(self.hsl.get_relative_position())
        # print(self.hsl.text_labels[0].get_relative_position())
        # print(self.hsl.get_relative_y2())
        # print(self.hsl.get_height())
        with self.file_path(path, 'add_label_left', 'pdf') as pdf_path:
            self.pdf.write(pdf_path)
