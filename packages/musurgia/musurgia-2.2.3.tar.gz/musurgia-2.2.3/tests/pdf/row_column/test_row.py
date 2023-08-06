from pathlib import Path

from musurgia.pdf.line import VerticalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.rowcolumn import DrawObjectRow
from musurgia.unittest import TestCase

path = Path(__file__)
# class TestRow(TestCase):
#     def setUp(self) -> None:
#         self.pdf = Pdf()
#
#     def test_add_label_lef(self):
#         row = DrawObjectRow()
#         row.add_draw_object(VerticalLineSegment(10))