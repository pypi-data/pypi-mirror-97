import os

from musurgia.agpdf.line import Line
from musurgia.agpdf.pdf import Pdf
from musurgia.agpdf.textlabel import TextLabel
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def test_1(self):
        pdf_path = path + '_test_1.pdf'
        pdf = Pdf()
        line = Line(length=60, relative_x=70)
        line.end_mark_line.show = True
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_2(self):
        pdf_path = path + '_test_2.pdf'
        pdf = Pdf()
        line_1 = Line(length=10)
        line_2 = Line(length=20, relative_x=10)
        line_2.end_mark_line.show = True
        line_1.draw_with_break(pdf)
        line_2.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_3(self):
        pdf_path = path + '_test_3.pdf'
        pdf = Pdf()
        line_1 = Line(length=10, relative_x=20)
        line_2 = Line(length=20, relative_x=200)
        line_2.end_mark_line.show = True
        line_1.draw_with_break(pdf)
        line_2.draw_with_break(pdf)
        pdf.write(pdf_path)

    def test_4(self):
        pdf_path = path + '_test_4.pdf'
        pdf = Pdf(orientation='landscape')
        line_1 = Line(length=10)
        line_3 = Line(length=20, relative_y=190)
        line_1.draw_with_break(pdf)
        line_3.draw_with_break(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_5(self):
        pdf_path = path + '_test_5.pdf'
        pdf = Pdf()
        line = Line(length=60, relative_x=70)
        line.end_mark_line.show = True
        line.add_text_label(TextLabel('bla', font_size=8))
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_6(self):
        pdf_path = path + '_test_6.pdf'
        pdf = Pdf()
        line = Line(length=60, relative_x=70)
        line.end_mark_line.show = True
        TextLabel.DEFAULT_FONT_SIZE = 8

        line.end_mark_line.add_text_label(TextLabel(3))
        line.end_mark_line.add_text_label(TextLabel(4, relative_y=-4))
        line.end_mark_line.add_text_label(TextLabel(5, relative_y=-6))
        line.add_text_label(TextLabel('bla'))
        line.add_text_label(TextLabel('bla bla', relative_y=-4))
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
        TextLabel.DEFAULT_FONT_SIZE = 10

    def test_7(self):
        pdf_path = path + '_test_7.pdf'
        pdf = Pdf()
        line = Line(length=20, relative_x=0, factor=5)
        line.end_mark_line.show = True
        line.draw(pdf=pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
