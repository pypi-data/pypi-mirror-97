import os

from quicktions import Fraction

from musurgia.agpdf.pdf import Pdf
from musurgia.agunittest import AGTestCase
from musurgia.timeline.timeline import TimeLine

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def test_1(self):
        pdf_path = path + '_test_1.pdf'
        pdf = Pdf(orientation='portrait')
        tl = TimeLine(length=50)
        printable = (pdf.w - pdf.r_margin - pdf.l_margin)
        tl.unit = Fraction(Fraction(printable), Fraction(20))
        tl.show_interval = 10
        tl.ruler.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_2(self):
        pdf_path = path + '_test_2.pdf'
        pdf = Pdf(orientation='portrait')
        tl = TimeLine(length=300)
        printable = (pdf.w - pdf.r_margin - pdf.l_margin)
        tl.unit = Fraction(Fraction(printable), Fraction(20))
        tl.show_interval = 10
        tl.ruler.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
