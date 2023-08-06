from musurgia.pdf.labeled import Labeled
from musurgia.pdf.newdrawobject import DrawObject
from musurgia.pdf.positioned import RelativeXNotSettableError, RelativeYNotSettableError


class MarkLine(DrawObject, Labeled):
    def __init__(self, parent, placement='start', height=3, thickness=1, show=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show = show
        self.parent = parent
        self._height = None
        self._placement = None

        self.placement = placement
        self.height = height
        self.position = None
        self.thickness = thickness

    @property
    def left_margin(self):
        return 0

    @property
    def right_margin(self):
        return 0

    @property
    def top_margin(self):
        return 0

    @property
    def bottom_margin(self):
        return 0

    @property
    def relative_x(self):
        if self.placement == 'start':
            return 0
        else:
            return self.parent.actual_length

    @relative_x.setter
    def relative_x(self, val):
        if val is not None:
            raise RelativeXNotSettableError()

    @property
    def relative_y(self):
        return self.parent.relative_y - self.height / 2

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
        # pdf.translate(self.relative_x, self.relative_y)
        # no margins
        x1 = self.relative_x
        x2 = x1
        y1 = self.relative_y
        y2 = y1 + self.height
        if self.show:
            for i in range(self.thickness):
                grid = 0.1
                pdf.line(x1=x1 + i * grid, y1=y1, x2=x2 + i * grid, y2=y2)
        for text_label in self.text_labels:
            text_label.draw(pdf)
