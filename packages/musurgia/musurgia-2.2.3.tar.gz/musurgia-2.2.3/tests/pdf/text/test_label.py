from pathlib import Path

from musurgia.pdf.labeled import Labeled
from musurgia.pdf.line import VerticalSegmentedLine
from musurgia.pdf.masterslave import PositionMaster
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import TextLabel
from musurgia.unittest import TestCase

path = Path(__file__)


class LabeledVerticalLine(VerticalSegmentedLine, Labeled):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, pdf):
        self.draw_above_text_labels(pdf)
        self.draw_left_text_labels(pdf)
        super().draw(pdf)

    # def get_slave_position(self, slave, position):
    #     if isinstance(slave, TextLabel):
    #         return 0
    #     else:
    #         return super().get_slave_position(slave, position)


class DummyPositionMaster(PositionMaster):
    def get_slave_position(self, slave, position):
        if position == 'x':
            return 0
        elif position == 'y':
            return 0


class TestTextLabel(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        t = TextLabel(master=DummyPositionMaster(), name='t1', text='Fox is going to be dead.')

        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            t.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_multiple(self):
        t1 = TextLabel(master=DummyPositionMaster(), name='t1', text='Fox is going to be dead.')
        t1.top_margin = -5
        t2 = TextLabel(master=DummyPositionMaster(), name='t2', text='What should we do??')
        t3 = TextLabel(master=DummyPositionMaster(), name='t3', text='What should we do??')
        with self.file_path(path, 'draw_multiple', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            t1.draw(self.pdf)
            self.pdf.translate(0, t1.get_height())
            t2.draw(self.pdf)
            self.pdf.translate(0, t2.get_height())
            t3.draw(self.pdf)
            self.pdf.translate(0, t3.get_height())
            self.pdf.write(pdf_path)

    def test_left_labels(self):
        unit = 1
        length = 40

        lvl = LabeledVerticalLine(lengths=int(length / unit) * [unit])
        for index, segment in enumerate(lvl.segments):
            if index % 10 == 0:
                segment.start_mark_line.length = 3
            else:
                segment.start_mark_line.length = 1.5

        lvl.add_label('first one one', placement='left', font_size=8)
        lvl.add_label('second two two', placement='left')
        lvl.add_label('third three three', placement='left', font_size=12)
        lvl.add_label('fourth four four', placement='left')
        lvl.add_label('fifth five five', placement='left')
        lvl.add_label('sixth six six', placement='left')
        lvl.add_label('seventh seven seven', placement='left')
        with self.file_path(path, 'left_labels', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(30, 10)
            lvl.draw(self.pdf)
            self.pdf.write(pdf_path)
