from pathlib import Path

from musurgia.pdf.line import HorizontalLine, SegmentedHorizontalLine
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.scene import Scene
from musurgia.pdf.segmentedline import SegmentedLine, LineSegment
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        pdf_path = create_test_path(path, 'draw.pdf')
        scene = Scene(relative_x=10, relative_y=10)
        scene.add_draw_object(SegmentedHorizontalLine(name='I', lengths=[3, 10, 5, 15]))
        scene.add_draw_object(SegmentedHorizontalLine(name='II', lengths=[3, 10, 5, 15, 20]))
        scene.draw(self.pdf)
        self.pdf.write(pdf_path)
        # self.assertCompareFiles(pdf_path)

    def test_draw_with_margins(self):
        self.assertFalse(True)

    def test_get_height(self):
        scene = Scene()
        do1 = scene.add_draw_object(HorizontalLine(relative_x=10, length=20, top_margin=10, bottom_margin=10))
        do2 = scene.add_draw_object(HorizontalLine(length=10, relative_x=10))
        expected = sum([do.get_height() + do.top_margin + do.bottom_margin + do.relative_y for do in [do1, do2]])
        actual = scene.get_height()
        self.assertEqual(expected, actual)

    def test_get_width(self):
        self.assertFalse(True)

    def test_get_relative_y2(self):
        self.assertFalse(True)

    def test_frame(self):
        self.assertFalse(True)

