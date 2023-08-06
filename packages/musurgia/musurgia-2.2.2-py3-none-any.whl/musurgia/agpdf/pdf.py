import os

from musurgia.agpdf.textlabel import Text
from fpdf import FPDF


class PageText(Text):
    def __init__(self, text, v_position=None, h_position=None, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        self.v_position = v_position
        self.h_position = h_position

    def get_text_physical_length(self):
        return (len(self.text)) * self.font_size / 6

    def draw(self, pdf):
        old_x, old_y = pdf.x, pdf.y
        if self.v_position == 'center':
            pdf.x = (pdf.w / 2) - self.get_text_physical_length() / 2
        elif self.v_position == 'left':
            pdf.x = pdf.l_margin
        elif self.v_position == 'right':
            pdf.x = pdf.w - pdf.r_margin - self.get_text_physical_length()
        else:
            pass

        if self.h_position == 'top':
            pdf.y = pdf.t_margin
        elif self.h_position == 'bottom':
            pdf.y = pdf.h - pdf.b_margin
        else:
            pass
        super().draw(pdf)
        pdf.x, pdf.y = old_x, old_y


class PageNumber(PageText):
    def __init__(self, text='none', v_position='center', h_position='bottom', *args, **kwargs):
        super().__init__(text=text, v_position=v_position, h_position=h_position, *args, **kwargs)

    def __call__(self, val):
        self.text = val
        self.page = val


class Pdf(FPDF):

    def __init__(self, default_line_distance=10, r_margin=10, t_margin=10, l_margin=10, b_margin=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_number = PageNumber('')
        self.r_margin = r_margin
        self.t_margin = t_margin
        self.l_margin = l_margin
        self.b_margin = b_margin
        self.add_page()

        self.default_line_distance = default_line_distance
        self.set_font("Arial", "", 10)

    def add_page(self):
        super().add_page(orientation=self.cur_orientation)

    def draw_page_number(self):
        for page in self.pages:
            self.page = page
            self.page_number(page)
            self.page_number.draw(self)

    def add_space(self, val):
        self.y += val

    def write(self, path):
        self.draw_page_number()
        self.output(path, 'F')

    def show(self, path):
        self.write(path)
        os.system('open ' + path)
