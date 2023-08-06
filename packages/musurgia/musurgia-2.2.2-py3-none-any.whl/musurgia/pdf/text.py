from musurgia.pdf.font import Font
from musurgia.pdf.masterslave import PositionSlave
from musurgia.pdf.newdrawobject import DrawObject
from musurgia.pdf.pdfunit import PdfUnit


class Text(DrawObject):
    DEFAULT_FONT_FAMILY = 'Helvetica'
    DEFAULT_FONT_SIZE = 10
    DEFAULT_FONT_WEIGHT = 'medium'
    DEFAULT_FONT_STYLE = 'regular'

    def __init__(self, value, font_family=None, font_weight=None, font_style=None,
                 font_size=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.font = Font()
        self.font_family = font_family
        self.font_weight = font_weight
        self.font_style = font_style
        self.font_size = font_size
        self._value = None
        self.value = value

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
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = str(val)

    def get_text_width(self):
        return self.font.get_text_pixel_width(self.value) / PdfUnit.get_k()

    def get_text_height(self):
        return self.font.get_text_pixel_height(self.value) / PdfUnit.get_k()

    def get_relative_x2(self):
        return self.relative_x + self.get_text_width()

    def get_relative_y2(self):
        return self.relative_y + self.get_text_height()

    def draw(self, pdf):
        if pdf.k != PdfUnit.get_k():
            raise AttributeError('wrong pdf.k!')
        if self.show:
            pdf.reset_font()
            style = ""
            if self.font.style == 'italic':
                style += 'I'
            if self.font.weight == 'bold':
                style += 'B'
            pdf.set_font(self.font.family, style=style, size=self.font_size)
            with pdf.prepare_draw_object(self):
                pdf.text(x=0, y=0, txt=self.value)


class TextLabel(PositionSlave, Text):
    def __init__(self, text, placement='above', *args, **kwargs):
        super().__init__(value=text, *args, **kwargs)
        self._placement = None
        self.placement = placement

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, val):
        permitted = ['above', 'below', 'left']
        if val not in permitted:
            raise ValueError(f'placement.value {val} must be in {permitted}')
        self._placement = val

class PageText(Text):
    def __init__(self, value, v_position=None, h_position=None, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        self.v_position = v_position
        self.h_position = h_position

    def draw(self, pdf):
        if self.v_position == 'center':
            self.relative_x = ((pdf.w - pdf.l_margin - pdf.r_margin) / 2) - self.get_width() / 2
        elif self.v_position == 'left':
            self.relative_x = pdf.l_margin
        elif self.v_position == 'right':
            self.relative_x = pdf.w - pdf.r_margin - self.get_width()
        else:
            pass

        if self.h_position == 'top':
            self.relative_y = 0
        elif self.h_position == 'bottom':
            self.relative_y = pdf.h - pdf.b_margin
        else:
            pass
        super().draw(pdf)
