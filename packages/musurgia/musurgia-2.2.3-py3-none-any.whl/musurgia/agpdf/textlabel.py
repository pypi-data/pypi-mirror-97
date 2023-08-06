from musurgia.agpdf.drawobject import DrawObject
from musurgia.agpdf.font import Font
import copy

from musurgia.agpdf.positioned import Positioned


class Text(DrawObject):
    DEFAULT_FONT_FAMILY = 'Arial'
    DEFAULT_FONT_SIZE = 10
    DEFAULT_FONT_WEIGHT = 'regular'
    DEFAULT_FONT_STYLE = 'regular'

    def __init__(self, text, font_family=None, font_weight=None, font_style=None, font_size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = Font()
        self.font_family = font_family
        self.font_weight = font_weight
        self.font_style = font_style
        self.font_size = font_size
        self._text = None
        self.text = text

    @property
    def font_family(self):
        return self.font.family

    @font_family.setter
    def font_family(self, val):
        if val is None:
            val = self.DEFAULT_FONT_FAMILY
        self.font.family = val

    @property
    def font_size(self):

        return self.font.size

    @font_size.setter
    def font_size(self, val):
        if val is None:
            val = self.DEFAULT_FONT_SIZE
        self.font.size = val

    @property
    def font_weight(self):
        return self.font.weight

    @font_weight.setter
    def font_weight(self, val):
        if val is None:
            val = self.DEFAULT_FONT_WEIGHT
        self.font.weight = val

    @property
    def font_style(self):
        return self.font.style

    @font_style.setter
    def font_style(self, val):
        if val is None:
            val = self.DEFAULT_FONT_STYLE
        self.font.style = val

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = str(val)

    def get_relative_x2(self):
        return self.relative_x + len(self.text) * 1000.0 / self.font.size

    def get_relative_y2(self):
        return self.relative_y

    def draw(self, pdf):
        if self.show:
            style = ""
            pdf.set_font(self.font.family, style=style, size=0)
            if self.font.style == 'italic':
                style += 'I'
            if self.font.weight == 'bold':
                style += 'B'
            pdf.set_font(self.font.family, style=style, size=self.font_size)
            pdf.text(x=pdf.x + self.relative_x, y=pdf.y + self.relative_y, txt=self.text)

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(text=self.text)
        for var in vars(self):
            copied_var = copy.deepcopy(vars(self)[var])
            copied.__setattr__(var, copied_var)
        return copied


class TextLabel(Text):
    def __init__(self, text, parent=None, relative_y=-2, *args, **kwargs):
        super().__init__(text=text, relative_y=relative_y, *args, **kwargs)
        self._parent = None
        self.parent = parent
        # self.x_offset = x_offset
        # self.y_offset = y_offset

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        if val is not None and not isinstance(val, Positioned):
            raise TypeError('parent.value must be of type Positioned not{}'.format(type(val)))
        self._parent = val

    def draw(self, pdf):
        if not self.parent:
            raise Exception('set parent first')
        self.relative_x += self.parent.relative_x
        self.relative_y += self.parent.relative_y
        super().draw(pdf)

    # @DrawObject.relative_x.getter
    # def relative_x(self):
    #     if not self.parent:
    #         raise Exception('set parent first')
    #     return self.parent.relative_x + self.x_offset
    #
    # @DrawObject.relative_y.getter
    # def relative_y(self):
    #     if not self.parent:
    #         raise Exception('set parent first')
    #     return self.parent.relative_y + self.y_offset
