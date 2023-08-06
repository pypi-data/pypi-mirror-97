import os

from fpdf import FPDF

from musurgia.agpdf.pdf import Pdf, PageText
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_0_1(self):
        pdf = self.pdf
        pdf_path = path + '_test_0_1.pdf'
        pdf.y = 100
        t = PageText('bold_test', font_weight='bold')
        t.draw(pdf)
        pdf.y = 200
        t = PageText('normal_test')
        t.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_0_2(self):
        pdf = self.pdf
        pdf_path = path + '_test_0_2.pdf'
        pdf.y = 100
        t = PageText('large_test', font_size=15)
        t.draw(pdf)
        pdf.y = 200
        t = PageText('normal_test')
        t.draw(pdf)
        pdf.write(pdf_path)
        # TestCompareFiles().assertExpected(file_path=pdf_path)

    def test_1(self):
        pdf = self.pdf
        pdf_path = path + '_test_1.pdf'
        pdf.y = 100
        t = PageText('hallo world!', font_weight='bold')
        t.draw(pdf)
        pdf.add_page()
        t.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_2(self):
        pdf = self.pdf
        pdf.add_page()

        pdf_path = path + '_test_2.pdf'
        pdf.page = 1
        pdf.y = 100
        t = PageText('hallo world!', font_weight='bold')

        t.draw(pdf)
        # t = PageText('hallo new world!', font_weight='bold')
        pdf.page = 2
        # print(pdf.font_style)
        pdf.y = 100
        t.draw(pdf)
        # print(pdf.font_style)

        pdf.page = 1
        pdf.y = 150
        t.draw(pdf)
        pdf.page = 2
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_3(self):
        pdf = self.pdf
        pdf.add_page()

        pdf_path = path + '_test_3.pdf'
        pdf.page = 1
        pdf.y = 100
        t = PageText('hallo world!')

        t.draw(pdf)
        t.font_weight = 'bold'
        # t = PageText('hallo new world!', font_weight='bold')
        pdf.page = 2

        pdf.y = 100
        t.draw(pdf)
        # print(pdf.font_style)

        pdf.page = 1
        pdf.y = 150
        t.draw(pdf)
        pdf.page = 2
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_4(self):
        pdf = FPDF()
        pdf.font_family = 'Arial'
        pdf.add_page()
        pdf.add_page()

        pdf_path = path + '_test_4.pdf'
        pdf.page = 1
        pdf.text(10, 100, 'hello world!')

        pdf.page = 2
        pdf.set_font(family=pdf.font_family, style='B')
        pdf.text(10, 100, 'hello new world!')

        pdf.page = 1
        # print(pdf.font_style)
        # pdf.set_font(family=pdf.font_family, style='BI')
        pdf.set_font(family=pdf.font_family, style='')
        pdf.set_font(family=pdf.font_family, style='B')
        pdf.text(10, 150, 'hello old world!')
        pdf.page = 2
        pdf.output(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
