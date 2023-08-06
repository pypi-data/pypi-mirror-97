from musurgia.agpdf.positioned import Positioned


class DrawObject(Positioned):
    def __init__(self, show=True, *args, **kwargs):
        self._show = None
        self.show = show
        self._page_break = False
        self._line_break = False
        super().__init__(*args, **kwargs)

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError()
        self._show = val

    def get_relative_x2(self):
        raise NotImplementedError()

    def get_relative_y2(self):
        raise NotImplementedError()

    def draw(self, pdf):
        raise NotImplementedError()

    def _check_line_break(self, pdf):
        next_x2 = pdf.x + self.get_relative_x2()
        printable_range = pdf.w - pdf.r_margin
        diff = next_x2 - printable_range
        if diff > 0:
            self._line_break = True
            self.relative_x -= printable_range
            if self.relative_x < 0:
                self.relative_x = 0
            try:
                pdf.y += self.get_relative_y2() + self.line_distance
            except (AttributeError, TypeError):
                pdf.y += self.get_relative_y2() + pdf.default_line_distance
            pdf.x = pdf.l_margin

    def _check_page_break(self, pdf):
        next_y2 = pdf.y + self.get_relative_y2()
        printable_y_range = pdf.h - pdf.b_margin
        diff = next_y2 - printable_y_range
        if diff > 0:
            self._page_break = True
            # print(
            #     '_check_page_break _check_page_break _check_page_break _check_page_break _check_page_break _check_page_break')
            self.relative_y -= printable_y_range
            if self.relative_y < 0:
                self.relative_y = 0

            margins = pdf.l_margin, pdf.t_margin, pdf.r_margin, pdf.b_margin
            pdf.add_page()
            pdf.l_margin, pdf.t_margin, pdf.r_margin, pdf.b_margin = margins

            pdf.y = pdf.t_margin
            pdf.x = pdf.l_margin

    def draw_with_break(self, pdf):
        self._check_line_break(pdf)
        self._check_page_break(pdf)
        self.draw(pdf)
