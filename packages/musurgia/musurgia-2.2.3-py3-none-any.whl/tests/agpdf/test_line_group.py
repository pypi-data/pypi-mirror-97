import os
from unittest import TestCase

from musurgia.agpdf.line import Line
from musurgia.agpdf.linegroup import LineGroup
from musurgia.agpdf.pdf import Pdf

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_1(self):
        pdf = self.pdf
        pdf_path = path + '_test_1.pdf'
        lg = LineGroup(inner_distance=7)
        lg.add_line(Line(length=10))
        lg.add_line(Line(length=10))
        lg.add_line(Line(length=10))

        lg.draw(pdf)
        pdf.write(pdf_path)

    def test_2(self):
        def make_line_group():
            lg = LineGroup(inner_distance=7, bottom_distance=30)
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            return lg

        pdf = self.pdf
        pdf_path = path + '_test_2.pdf'

        lg = make_line_group()
        lg.draw(pdf)
        pdf.write(pdf_path)

    def test_3(self):
        def make_line_group():
            lg = LineGroup(inner_distance=7, bottom_distance=30)
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            return lg

        pdf = self.pdf
        pdf_path = path + '_test_3.pdf'
        lg = make_line_group()
        lg.draw(pdf)

        lg = make_line_group()
        lg.draw(pdf)
        pdf.write(pdf_path)

    def test_4(self):
        def make_line_group():
            lg = LineGroup(inner_distance=7, bottom_distance=30)
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            return lg

        pdf = self.pdf
        pdf_path = path + '_test_4.pdf'
        lg = make_line_group()
        lg.draw(pdf)

        lg = make_line_group()
        lg.relative_x = 50
        lg.relative_y = 50
        lg.draw(pdf)
        pdf.write(pdf_path)

    def test_5a(self):
        pdf = self.pdf
        pdf_path = path + '_test_5a.pdf'
        line = Line(length=10)
        line.draw_with_break(pdf)

        line = Line(length=10)
        line.relative_x = 300
        line.draw_with_break(pdf)
        pdf.write(pdf_path)

    def test_5(self):
        def make_line_group():
            lg = LineGroup(inner_distance=7, bottom_distance=30)
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            return lg

        pdf = self.pdf
        pdf_path = path + '_test_5.pdf'
        lg = make_line_group()
        lg.draw_with_break(pdf)

        lg = make_line_group()
        lg.relative_x = 300
        lg.draw_with_break(pdf)
        pdf.write(pdf_path)

    def test_6(self):
        def make_line_group():
            lg = LineGroup(inner_distance=7, bottom_distance=30)
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            lg.add_line(Line(length=10))
            return lg

        pdf = self.pdf
        pdf_path = path + '_test_6.pdf'
        lg = make_line_group()
        lg.draw_with_break(pdf)

        lg = make_line_group()
        lg.relative_x = 300
        lg.relative_y = 240
        lg.draw_with_break(pdf)
        pdf.write(pdf_path)
