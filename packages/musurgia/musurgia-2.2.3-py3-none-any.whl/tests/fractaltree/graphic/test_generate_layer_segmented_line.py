from pathlib import Path

from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import PageText
from musurgia.unittest import TestCase

path = Path(__file__)


def make_ft():
    ft = FractalTree(value=20)
    ft.add_layer()
    ft.get_children()[0].add_layer()
    ft.get_children()[-1].add_layer()
    return ft


class TestGenerateLayerSegmentedLine(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')

    def test_draw(self):
        def change_ft_graphic():
            ft.graphic.unit = unit
            ft.graphic.add_labels(lambda node: round(float(node.value), 2), placement='above', font_size=6,
                                  bottom_margin=2, left_margin=0.5)
            ft.graphic.add_labels(lambda node: node.fractal_order, placement='below', font_size=6, top_margin=1,
                                  left_margin=0.5)

            ft.graphic.change_segment_attributes(bottom_margin=5)

        def change_layer_graphic(layer_graphic):
            for segment in layer_graphic.segments:
                segment.straight_line.add_label(round(float(segment.node.value), 2), font_size=6, bottom_margin=3)

        unit = 20
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            ft = make_ft()
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h', first_label=-1, unit=unit)
            self.pdf.draw_ruler('v')
            self.pdf.translate(15, 10)
            pt = PageText('Some Title', v_position='center', font_weight='bold', font_size=12)
            pt.draw(self.pdf)
            self.pdf.translate(0, 10)
            change_ft_graphic()
            ft.graphic.draw(self.pdf)
            self.pdf.translate(0, ft.graphic.get_height() + 10)
            segmented_line = ft.generate_layer_segmented_line(layer_number=2, unit=unit)
            change_layer_graphic(segmented_line)
            segmented_line.segments[0].start_mark_line.add_text_label('blabla', placement='left', right_margin=1)
            segmented_line.draw(self.pdf)
            self.pdf.write(pdf_path)
