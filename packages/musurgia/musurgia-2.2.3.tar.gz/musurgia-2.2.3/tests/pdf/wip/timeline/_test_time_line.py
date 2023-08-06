from pathlib import Path

from quicktions import Fraction

from musurgia.pdf.pdf import Pdf
from musurgia.timeline.timeline import TimeLine
from musurgia.unittest import TestCase, create_test_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    # def test_ruler_bottom_margin(self):
    #     tl = TimeLine(length=30, bottom_margin=40)
    #     tl.add_voice('v1')
    #     print(tl.bottom_margin)
    #     print(tl.ruler.bottom_margin)
    #     print(tl.get_height())

    def test_draw_ruler(self):
        pdf_path = create_test_path(path, 'draw_ruler.pdf')
        pdf = Pdf(orientation='p')
        tl = TimeLine(length=50, bottom_margin=40)
        printable = (pdf.w - pdf.r_margin - pdf.l_margin)
        tl.unit = Fraction(Fraction(printable), Fraction(20))
        tl.show_interval = 10
        tl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_draw_ruler_with_break(self):
        pdf_path = create_test_path(path, 'draw_ruler_with_break.pdf')
        pdf = Pdf(orientation='p')
        tl = TimeLine(length=300)
        printable = (pdf.w - pdf.r_margin - pdf.l_margin)
        tl.unit = Fraction(Fraction(printable), Fraction(20))
        tl.show_interval = 10
        tl.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)

    def test_time_line_with_voices(self):
        pdf_path = create_test_path(path, 'time_line_with_voices.pdf')
        tl = TimeLine(length=200, inner_distance=20, bottom_margin=30)
        # voice = tl.add_voice(name='v1')
        # voice.name.relative_x = -5
        # for segment in voice.segments[5:15]:
        #     segment.show = True

        tl.draw(self.pdf)
        self.pdf.write(pdf_path)
