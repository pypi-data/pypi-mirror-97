from musurgia.agpdf.drawobject import DrawObject
from musurgia.agpdf.labeled import Labeled
from musurgia.agpdf.line import Line
from musurgia.agpdf.markline import MarkLine
from musurgia.agpdf.named import Named


class Cell(DrawObject):
    def __init__(self, width=10, height=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._width = None
        self._height = None
        self.width = width
        self.height = height
        self._lines = None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val
        self.generate_lines()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val
        self.generate_lines()

    @DrawObject.relative_y.setter
    def relative_y(self, val):
        super().relative_y = val
        self.generate_lines()

    @DrawObject.relative_x.setter
    def relative_x(self, val):
        super().relative_x = val
        self.generate_lines()

    def generate_lines(self):
        if self.width and self.height:
            # todo: Line must have an angel property
            line_1 = Line(relative_y=self.relative_y, relative_x=self.relative_x)


class Table(DrawObject):
    def __init__(self, number_of_rows=10, number_of_columns=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._number_of_rows = None
        self._number_of_columns = None

        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns

        self._page = None

    @property
    def number_of_rows(self):
        return self._number_of_rows

    @number_of_rows.setter
    def number_of_rows(self, val):
        self._number_of_rows = val

    @property
    def number_of_columns(self):
        return self._number_of_columns

    @number_of_columns.setter
    def number_of_columns(self, val):
        self._number_of_columns = val

    def get_row(self, row_number):
        pass

    def get_column(self, column_number):
        pass

    def get_cell(self, row_number, column_number):
        pass

    def draw(self, pdf):
        pass
        # x1 = pdf.x + self.relative_x
        # x2 = pdf.x + self.relative_x + self.actual_length
        # y1 = pdf.y + self.relative_y
        # y2 = y1
        #
        # self._x1, self._x2, self._y1, self._y2 = x1, x2, y1, y2
        # self._page = pdf.page
        # if self.name:
        #     self.name.draw(pdf)
        #
        # if self.show:
        #     self.start_mark_line.draw(pdf)
        #     self.end_mark_line.draw(pdf)
        #     pdf.line(x1=x1, y1=y1, x2=x2, y2=y2)
        #     for text_label in self._text_labels:
        #         text_label.draw(pdf)
        #
        # pdf.x = x2
