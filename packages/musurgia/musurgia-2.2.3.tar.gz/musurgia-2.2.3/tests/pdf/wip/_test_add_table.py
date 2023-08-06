import os
from unittest import TestCase

from musurgia.pdf.pdf import Pdf
from musurgia.pdf.table import Table

path = os.path.abspath(__file__).split('.')[0]


# todo
class Test(TestCase):
    def test_1(self):
        pass
        # pdf_path = path + '_test_1.pdf'
        # pdf = Pdf()
        # table = Table(number_of_rows=20, relative_x=70)
        # table.draw(pdf=pdf)
        # pdf.write(pdf_path)
