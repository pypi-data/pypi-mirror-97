from musurgia.pdf.newdrawobject import DrawObject


class Scene(DrawObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._draw_objects = []

    @property
    def draw_objects(self):
        return self._draw_objects

    def add_draw_object(self, draw_object):
        if not isinstance(draw_object, DrawObject):
            raise TypeError()
        self._draw_objects.append(draw_object)
        return draw_object

    def get_relative_x2(self):
        if self.draw_objects:
            return max([do.get_relative_x2() + do.right_margin + do.left_margin for do in self.draw_objects])
        else:
            return None

    def get_relative_y2(self):
        if self.draw_objects:
            return sum([do.get_relative_y2() + do.bottom_margin + do.bottom_margin for do in
                        self.draw_objects]) + self.relative_y
        else:
            return None

    def draw(self, pdf):
        # with pdf.saved_state():
        pdf.translate(self.relative_x, -self.relative_y)
        pdf.translate(self.left_margin, self.top_margin)
        for draw_object in self._draw_objects:
            draw_object.draw(pdf)
        pdf.translate(self.right_margin, self.bottom_margin)
