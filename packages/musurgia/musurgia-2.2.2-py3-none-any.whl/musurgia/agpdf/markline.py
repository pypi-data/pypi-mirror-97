from musurgia.agpdf.drawobject import DrawObject
from musurgia.agpdf.labeled import Labeled


class MarkLine(DrawObject, Labeled):
    def __init__(self, height=3, thickness=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._height = None
        self.height = height
        self.position = None
        self.thickness = thickness

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
