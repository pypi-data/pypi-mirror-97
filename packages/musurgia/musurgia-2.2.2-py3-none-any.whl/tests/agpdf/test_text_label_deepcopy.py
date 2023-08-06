import os

from musurgia.agpdf.pdf import Pdf
from musurgia.agpdf.textlabel import Text
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_1(self):
        pdf_path = path + '_test_1.pdf'
        tl = Text('test_1')
        tl.relative_x = 30
        copied = tl.__deepcopy__()
        copied.draw(self.pdf)
        self.pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
