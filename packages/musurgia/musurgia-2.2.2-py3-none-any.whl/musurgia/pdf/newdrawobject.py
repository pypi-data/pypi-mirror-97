from abc import ABC, abstractmethod
from math import ceil

from musurgia.pdf.margined import Margined
from musurgia.pdf.positioned import Positioned


class DrawObject(ABC, Positioned, Margined):
    def __init__(self, *args, **kwargs):
        self._show = True
        self._clipping_area = ClippingArea(pdf=None, draw_object=self)
        super().__init__(*args, **kwargs)

    @property
    def clipping_area(self):
        return self._clipping_area

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError(f"show.value must be of type bool not{type(val)}")
        self._show = val

    @abstractmethod
    def get_relative_x2(self):
        raise NotImplementedError()

    @abstractmethod
    def get_relative_y2(self):
        raise NotImplementedError()

    def get_height(self):
        return self.top_margin + self.get_relative_y2() - self.relative_y + self.bottom_margin

    def get_width(self):
        return self.left_margin + self.get_relative_x2() - self.relative_x + self.right_margin

    @abstractmethod
    def draw(self, pdf):
        raise NotImplementedError()

    def clipped_draw(self, pdf):
        self.clipping_area.pdf = pdf
        self.clipping_area.draw()

    def get_relative_position(self):
        return {'relative_x': self.relative_x, 'relative_y': self.relative_y}

    def get_margins(self):
        return {'left_margin': self.left_margin, 'top_margin': self.top_margin, 'right_margin': self.right_margin,
                'bottom_margin': self.bottom_margin}


class ClippingArea:
    def __init__(self, pdf, draw_object, left_margin=10, right_margin=0, top_margin=10):
        self.pdf = pdf
        self.draw_object = draw_object
        self.left_margin = left_margin
        self.right_margin = right_margin
        self.top_margin = top_margin

    @property
    def row_width(self):
        if not self.pdf:
            raise AttributeError('set pdf first!')
        return self.pdf.w - self.pdf.l_margin - self.pdf.r_margin - self.left_margin - self.right_margin

    def row_height(self):
        if not self.pdf:
            raise AttributeError('set pdf first!')
        return self.draw_object.get_height()

    def _prepare_page(self):
        self.pdf.translate_page_margins()
        self.pdf.translate(self.left_margin, self.top_margin)

    def _add_page(self):
        self.pdf.add_page()
        self._prepare_page()

    def _draw_with_clip(self, index):
        with self.pdf.saved_state():
            self.pdf.clip_rect(-1, -5, self.row_width + 1.14, self.row_height())
            self.pdf.translate(index * -self.row_width, 0)
            self.draw_object.draw(self.pdf)

    def get_number_of_rows(self):
        return int(ceil(self.draw_object.get_width() / self.row_width))

    def draw(self):
        self.pdf.translate(self.left_margin, self.top_margin)
        for index in range(self.get_number_of_rows()):
            if index != 0:
                self.pdf.translate(0, self.draw_object.get_height())
            if self.pdf.absolute_y > self.pdf.h - self.pdf.b_margin:
                self._add_page()
            self._draw_with_clip(index)
