from fpdf import FPDF
from fpdf.php import sprintf

from musurgia.pdf.line import HorizontalRuler, VerticalRuler
from musurgia.pdf.pdfunit import PdfUnit
from musurgia.pdf.text import PageText


class SavedState:
    def __init__(self, pdf):
        self.pdf = pdf

    def __enter__(self):
        self.pdf._push_state()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pdf._pop_state()


class PrepareDrawObject:
    def __init__(self, pdf, draw_object):
        self.pdf = pdf
        self.draw_object = draw_object

    def __enter__(self):
        self.pdf._push_state()
        self.pdf.translate(self.draw_object.relative_x, self.draw_object.relative_y)
        self.pdf.translate(self.draw_object.left_margin, self.draw_object.top_margin)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pdf._pop_state()


class Pdf(FPDF):

    def __init__(self, r_margin=10, t_margin=10, l_margin=10, b_margin=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r_margin = r_margin
        self.t_margin = t_margin
        self.l_margin = l_margin
        self.b_margin = b_margin
        self._absolute_positions = {}
        self.add_page()

        self._state = []

        self.set_font("Helvetica", "", 10)

    def _pop_state(self):
        self._state.pop()
        self._out(sprintf('Q\n'))

    def _push_state(self):
        self._state.append('push')
        self._out(sprintf('q\n'))

    @property
    def absolute_positions(self):
        return self._absolute_positions

    @property
    def absolute_x(self):
        return self._absolute_positions[self.page][0]

    @property
    def absolute_y(self):
        return self._absolute_positions[self.page][1]

    @property
    def k(self):
        return PdfUnit.get_k()

    @k.setter
    def k(self, val):
        pass

    def add_space(self, val):
        self.y += val

    def add_page(self):
        super().add_page(orientation=self.cur_orientation)
        self._absolute_positions[self.page] = [0, 0]

    def prepare_draw_object(self, draw_object):
        pdo = PrepareDrawObject(self, draw_object=draw_object)
        return pdo

    def reset_font(self):
        self._out(sprintf('BT /F%d %.2f Tf ET',
                          self.current_font['i'],
                          self.font_size_pt))

    def reset_position(self):
        self.translate(-self.absolute_x, -self.absolute_y)

    def clip_rect(self, x, y, w, h):
        self._out(sprintf('%.2f %.2f %.2f %.2f re W n',
                          x * self.k, (self.h - y) * self.k,
                          w * self.k, -h * self.k))

    def draw_page_numbers(self, **kwargs):
        for page in self.pages:
            self.page = page
            self.reset_position()
            page_number = PageText(page, **kwargs)
            page_number.draw(self)

    def saved_state(self):
        ss = SavedState(self)
        return ss

    def translate(self, dx, dy):
        if not self._state:
            self._absolute_positions[self.page][0] += dx
            self._absolute_positions[self.page][1] += dy
        dx, dy = dx * self.k, dy * self.k
        self._out(sprintf('1.0 0.0 0.0 1.0 %.2F %.2F cm',
                          dx, -dy))

    def translate_page_margins(self):
        self.translate(self.l_margin, self.t_margin)

    def draw_ruler(self, mode='h', unit=10, first_label=0, show_first_label=False, label_show_interval=1):
        if mode in ['h', 'horizontal']:
            length = self.w - self.l_margin - self.r_margin
            ruler = HorizontalRuler(length=length, unit=unit, first_label=first_label,
                                    show_first_label=show_first_label, label_show_interval=label_show_interval)
        elif mode in ['v', 'vertical']:
            length = self.h - self.t_margin - self.b_margin
            ruler = VerticalRuler(length=length, unit=unit, first_label=first_label,
                                  show_first_label=show_first_label, label_show_interval=label_show_interval)
        else:
            raise AttributeError()
        ruler.draw(self)

    def write(self, path):
        # if self.show_page_number:
        #     self.draw_page_number()
        self.output(path, 'F')
