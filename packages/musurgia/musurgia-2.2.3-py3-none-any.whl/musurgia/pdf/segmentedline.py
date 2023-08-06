from musurgia.pdf.newdrawobject import DrawObject
from musurgia.pdf.labeled import Labeled
from musurgia.pdf.named import Named
from musurgia.pdf.positioned import RelativeXNotSettableError, RelativeYNotSettableError


class MarkLine(DrawObject, Labeled):
    def __init__(self, parent, placement='start', height=3, thickness=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_margin, self.top_margin, self.right_margin, self.bottom_margin = 0, 0, 0, 0
        self._parent = None
        self._height = None
        self._placement = None
        self.parent = parent
        self.placement = placement
        self.height = height
        self.position = None
        self.thickness = thickness

    @property
    def relative_x(self):
        if self.placement == 'start':
            return self.parent.relative_x
        else:
            return self.parent.relative_x + self.parent.actual_length

    @relative_x.setter
    def relative_x(self, val):
        if val is not None:
            raise RelativeXNotSettableError()

    @property
    def relative_y(self):
        return self.parent.relative_y

    @relative_y.setter
    def relative_y(self, val):
        if val is not None:
            raise RelativeYNotSettableError()

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, val):
        permitted = ['start', 'end']
        if val not in permitted:
            raise ValueError('placement.value {} must be in {}'.format(val, permitted))
        self._placement = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    def get_relative_x2(self):
        return self.relative_x

    def get_relative_y2(self):
        return self.relative_y + self.height

    def draw(self, pdf):
        x1 = self.relative_x + pdf.x
        x2 = x1
        y1 = self.relative_y + pdf.y - self.height / 2
        y2 = y1 + self.height
        if self.show:
            for i in range(self.thickness):
                grid = 0.1
                pdf.line(x1=x1 + i * grid, y1=y1, x2=x2 + i * grid, y2=y2)
        self.position = (x1, y2)
        for text_label in self.text_labels:
            text_label.draw(pdf)
        # pdf.x = x2
        # pdf.y = y2


class LineSegment(DrawObject, Labeled, Named):
    def __init__(self, length, factor=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._length = None
        self._factor = None
        self._parent = None
        self.length = length
        self.factor = factor
        self._start_mark_line = MarkLine(parent=self, placement='start')
        self._end_mark_line = MarkLine(parent=self, placement='end', show=False)
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
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        self._length = val

    @property
    def actual_length(self):
        return self.length * self.factor

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        if not isinstance(val, SegmentedLine):
            raise TypeError(f"parent.value must be of type SegmentedLine not{type(val)}")
        self._parent = val

    @property
    def start_mark_line(self):
        return self._start_mark_line

    @property
    def end_mark_line(self):
        return self._end_mark_line

    def get_relative_x2(self):
        return self.relative_x + self.actual_length

    def get_relative_y2(self):
        return max([self.start_mark_line.get_relative_y2(), self.end_mark_line.get_relative_y2()])

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
        pdf.y += self.bottom_margin


class SegmentedLine(DrawObject, Labeled, Named):
    def __init__(self, lengths, bottom_margin=10, factor=1, *args, **kwargs):
        super().__init__(bottom_margin=bottom_margin, *args, **kwargs)
        self._line_segments = []
        self._factor = None
        self.factor = factor
        self._lengths = None
        self.lengths = lengths

    @DrawObject.relative_y.setter
    def relative_y(self, val):
        self._relative_y = val
        try:
            for line in self.line_segments:
                line.relative_y = val
        except AttributeError:
            pass

    @DrawObject.relative_x.setter
    def relative_x(self, val):
        self._relative_x = val
        try:
            self.line_segments[-1].relative_x = val
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
        self._generate_line_segments()

    @property
    def line_segments(self):
        return self._line_segments

    def _generate_line_segments(self):
        self._line_segments = []
        for length in self.lengths:
            line_segment = LineSegment(length=length, relative_y=self.relative_y, factor=self.factor)

            if not self._line_segments:
                line_segment.relative_x = self.relative_x
            else:
                line_segment.relative_x = 0
            line_segment.parent = self
            self._line_segments.append(line_segment)
        self._line_segments[-1].end_mark_line.show = True

    def get_relative_x2(self):
        raise Exception('SegementedLine does not have a x2 value')

    def get_relative_y2(self):
        return self.line_segments[0].get_relative_y2()

    def draw_with_break(self, pdf):
        for text_label in self._text_labels:
            text_label.draw(pdf)

        for line_segment in self.line_segments:
            if line_segment == self.line_segments[0]:
                line_segment.name = self.name

            line_segment.draw_with_break(pdf)
            new_x = pdf.x

            if line_segment._line_break:
                # pdf.y += self.bottom_margin
                if self.name:
                    line_segment.name = self.name
                    pdf.x = new_x - line_segment.actual_length
                    line_segment.name.draw(pdf)
                pdf.x = new_x

    def draw(self, pdf):
        for text_label in self._text_labels:
            text_label.draw(pdf)
        pdf.x = pdf.l_margin
        for line_segment in self.line_segments:
            if line_segment == self.line_segments[0]:
                line_segment.name = self.name

            line_segment.draw_with_break(pdf)
            new_x = pdf.x

            if line_segment._line_break:
                # pdf.y += self.bottom_margin
                if self.name:
                    line_segment.name = self.name
                    pdf.x = new_x - line_segment.actual_length
                    line_segment.name.draw(pdf)
                pdf.x = new_x
