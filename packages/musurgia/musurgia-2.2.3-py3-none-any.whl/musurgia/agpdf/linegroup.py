from musurgia.agpdf.drawobject import DrawObject
from musurgia.agpdf.line import Line


class LineGroup(DrawObject):
    def __init__(self, inner_distance=None, bottom_distance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lines = []
        self._inner_distance = None
        self.inner_distance = inner_distance
        self._bottom_distance = None
        self.bottom_distance = bottom_distance

    def set_distances(self):
        self.set_inner_distance()
        self.set_bottom_distance()

    def set_bottom_distance(self):
        if self.bottom_distance is not None and self.lines:
            self.lines[-1].line_distance = self.bottom_distance

    def set_inner_distance(self):
        if self.inner_distance is not None:
            for index, line in enumerate(self.lines):
                line.relative_y = self.relative_y + (index * self.inner_distance)

    def add_line(self, line):
        if not isinstance(line, Line):
            raise TypeError()
        if self.length:
            if line.length != self.length:
                raise ValueError('line.length {} must be {}'.format(line.length, self.length))
        line.relative_y = self.relative_y
        line.relative_x = self.relative_x
        self._lines.append(line)
        self.set_distances()

    @DrawObject.relative_x.setter
    def relative_x(self, val):
        self._relative_x = val
        try:
            for line in self.lines:
                line.relative_x = self.relative_x
        except AttributeError:
            pass

    @DrawObject.relative_y.setter
    def relative_y(self, val):
        self._relative_y = val
        try:
            for line in self.lines:
                line.relative_y = self.relative_y
            self.set_distances()
        except AttributeError:
            pass

    @property
    def lines(self):
        return self._lines

    @property
    def length(self):
        try:
            return self.lines[0].length
        except IndexError:
            return None

    @property
    def inner_distance(self):
        return self._inner_distance

    @inner_distance.setter
    def inner_distance(self, val):
        self._inner_distance = val
        self.set_inner_distance()

    @property
    def bottom_distance(self):
        return self._bottom_distance

    @bottom_distance.setter
    def bottom_distance(self, val):
        self._bottom_distance = val
        self.set_bottom_distance()

    def get_relative_x2(self):
        try:
            return self.lines[0].get_relative_x2()
        except IndexError:
            return None

    def get_relative_y2(self):
        try:
            return self.lines[-1].get_relative_y2() + self.bottom_distance
        except IndexError:
            return None

    def draw(self, pdf):
        old_pdf_x = pdf.x
        for line in self.lines:
            pdf.x = old_pdf_x
            line.draw(pdf)
