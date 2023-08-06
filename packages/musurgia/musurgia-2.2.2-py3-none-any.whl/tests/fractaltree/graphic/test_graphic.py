from pathlib import Path

from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.pdf.line import HorizontalRuler
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


def make_ft():
    ft = FractalTree(value=20)
    ft.add_layer()
    ft.get_children()[0].add_layer()
    ft.get_children()[-1].add_layer()
    return ft


class TestPdfColumn(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            ft = make_ft()
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            ft.graphic.unit = 2
            ft.graphic.draw(self.pdf)

            self.pdf.write(pdf_path)

    def test_add_labels(self):
        def generate_ruler():
            ruler_length = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
            ruler = HorizontalRuler(length=ruler_length, unit=3, show_first_label=True, label_show_interval=5)
            for segment in ruler.segments:
                try:
                    segment.start_mark_line.text_labels[0].font_size = 8
                except IndexError:
                    pass
            return ruler

        with self.file_path(path, 'add_labels', 'pdf') as pdf_path:
            ft = make_ft()
            self.pdf.translate_page_margins()

            ruler = generate_ruler()
            ruler.draw(self.pdf)
            self.pdf.translate(0, 10)
            ft.graphic.unit = 3
            ft.graphic.add_labels(lambda node: node.fractal_order if node.fractal_order is not None else '',
                                  font_size=8, bottom_margin=3)
            ft.graphic.add_labels(lambda node: round(float(node.value), 2), placement='below', font_size=6,
                                  top_margin=2)
            ft.graphic.change_segment_attributes(bottom_margin=5)

            ft.graphic.draw(self.pdf)
            self.pdf.write(pdf_path)
