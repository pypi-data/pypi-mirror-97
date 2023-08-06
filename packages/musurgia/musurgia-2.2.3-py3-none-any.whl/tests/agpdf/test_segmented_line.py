import os

from musurgia.agpdf.pdf import Pdf
from musurgia.agpdf.segmentedline import SegmentedLine
from musurgia.agpdf.textlabel import TextLabel
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def test_1(self):
        pdf_path = path + '_test_1.pdf'
        sl = SegmentedLine(lengths=[1, 3, 2, 5], factor=5)
        pdf = Pdf('portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_2(self):
        pdf_path = path + '_test_2.pdf'
        sl = SegmentedLine(lengths=30 * [20])
        pdf = Pdf('portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_3(self):
        pdf_path = path + '_test_3.pdf'
        sl = SegmentedLine(lengths=200 * [20])
        pdf = Pdf('portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_4(self):
        pdf_path = path + '_test_4.pdf'
        sl = SegmentedLine(lengths=30 * [10])
        sl.add_text_label(TextLabel('bla is bla'))
        pdf = Pdf('portrait')
        sl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_5(self):
        pdf_path = path + '_test_5.pdf'
        sl = SegmentedLine(lengths=30 * [10], name='vla')
        pdf = Pdf('portrait')
        sl.draw(pdf)
        # pdf.add_draw_object(sl)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
