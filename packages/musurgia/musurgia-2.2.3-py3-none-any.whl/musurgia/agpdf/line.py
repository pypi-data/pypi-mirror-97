from musurgia.agpdf.drawobject import DrawObject
from musurgia.agpdf.labeled import Labeled
from musurgia.agpdf.markline import MarkLine
from musurgia.agpdf.named import Named


class Line(DrawObject, Labeled, Named):
    def __init__(self, length, factor=1, line_distance=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._length = None

        self._line_distance = None
        self.line_distance = line_distance
        self._factor = None
        self.length = length
        self.factor = factor
        self._start_mark_line = MarkLine()
        self._end_mark_line = MarkLine(show=False)
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._page = None

    @property
    def x1(self):
        return self._x1

    @property
    def x2(self):
        return self._x2

    @property
    def y1(self):
        return self._y1

    @property
    def y2(self):
        return self._y2

    @property
    def page(self):
        return self._page

    @property
    def factor(self):
        if self._factor is None:
            self._factor = 1
        return self._factor

    @factor.setter
    def factor(self, val):
        self._factor = val

    @property
    def line_distance(self):
        return self._line_distance

    @line_distance.setter
    def line_distance(self, val):
        self._line_distance = val

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        self._length = val

    @property
    def actual_length(self):
        return self.length * self.factor

    @property
    def start_mark_line(self):
        self._start_mark_line.relative_x = self.relative_x
        self._start_mark_line.relative_y = self.relative_y
        return self._start_mark_line

    @property
    def end_mark_line(self):
        self._end_mark_line.relative_x = self.relative_x + self.length * self.factor
        self._end_mark_line.relative_y = self.relative_y
        return self._end_mark_line

    def get_relative_x2(self):
        return self.relative_x + self.actual_length

    def get_relative_y2(self):
        return max([self.start_mark_line.get_relative_y2(), self.end_mark_line.get_relative_y2(), self.line_distance])

    def draw(self, pdf):
        x1 = pdf.x + self.relative_x
        x2 = pdf.x + self.relative_x + self.actual_length
        y1 = pdf.y + self.relative_y
        y2 = y1

        self._x1, self._x2, self._y1, self._y2 = x1, x2, y1, y2
        self._page = pdf.page
        if self.name:
            self.name.draw(pdf)

        if self.show:
            self.start_mark_line.draw(pdf)
            self.end_mark_line.draw(pdf)
            pdf.line(x1=x1, y1=y1, x2=x2, y2=y2)
            for text_label in self._text_labels:
                text_label.draw(pdf)

        pdf.x = x2
