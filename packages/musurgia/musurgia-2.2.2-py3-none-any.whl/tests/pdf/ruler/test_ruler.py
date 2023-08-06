from pathlib import Path

from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class TestRuler(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_h_ruler(self):
        r = HorizontalRuler(length=50)
        with self.file_path(path, 'h_ruler', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            r.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_h_ruler_A4(self):
        with self.file_path(path, 'h_ruler_A4', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler(mode='h')
            self.pdf.write(pdf_path)

    def test_both_rulers_A4(self):
        with self.file_path(path, 'both_rulers_A4', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler(mode='h')
            self.pdf.draw_ruler(mode='v')
            self.pdf.write(pdf_path)
