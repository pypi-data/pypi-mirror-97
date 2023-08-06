from musurgia.agpdf.drawobject import DrawObject
from musurgia.agpdf.labeled import Labeled
from musurgia.agpdf.line import Line
from musurgia.agpdf.named import Named


class SegmentedLine(DrawObject, Labeled, Named):
    def __init__(self, lengths, factor=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lines = []
        self._factor = None
        self.factor = factor
        self._lengths = None
        self.lengths = lengths

    @DrawObject.relative_y.setter
    def relative_y(self, val):
        self._relative_y = val
        try:
            for line in self.lines:
                line.relative_y = val
        except AttributeError:
            pass

    @DrawObject.relative_x.setter
    def relative_x(self, val):
        self._relative_x = val
        try:
            self.lines[-1].relative_x = val
        except AttributeError:
            pass

    @property
    def lengths(self):
        return self._lengths

    @lengths.setter
    def lengths(self, val):
        if not isinstance(val, list):
            raise TypeError('lengths.value must be of type list not{}'.format(type(val)))
        self._lengths = val
        self._generate_lines()

    @property
    def lines(self):
        return self._lines

    def _generate_lines(self):
        self._lines = []
        for length in self.lengths:
            line = Line(length=length, relative_y=self.relative_y, factor=self.factor)
            if not self._lines:
                line.relative_x = self.relative_x
            else:
                line.relative_x = 0

            self._lines.append(line)
        self._lines[-1].end_mark_line.show = True

    def get_relative_x2(self):
        raise Exception('SegementedLine does not have a x2 value')

    def get_relative_y2(self):
        return self.lines[0].relative_y

    def draw(self, pdf):
        for text_label in self._text_labels:
            text_label.draw(pdf)

        for line in self.lines:
            if line == self.lines[0]:
                line.name = self.name

            line.draw_with_break(pdf)
            new_x = pdf.x

            if line._line_break and self.name:
                line.name = self.name
                pdf.x = new_x - line.actual_length
                line.name.draw(pdf)
                pdf.x = new_x
