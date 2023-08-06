from musurgia.pdf.drawobjectgroup import DrawObjectGroup
from musurgia.timeline.ruler import Ruler
from musurgia.timeline.voice import Voice


class TimeLineError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TimeLine(DrawObjectGroup):
    def __init__(self, length=None, unit=10, inner_distance=10, bottom_margin=20, *args, **kwargs):
        super().__init__(inner_distance=inner_distance, bottom_margin=bottom_margin, *args, **kwargs)
        self._unit = None
        self.unit = unit
        self._length = None
        self.length = length

    @property
    def ruler(self):
        try:
            return self.draw_objects[0]
        except IndexError:
            return None

    @property
    def voices(self):
        try:
            return self.draw_objects[1:]
        except IndexError:
            return []

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        if val is not None:
            if self._length:
                raise TimeLineError('length can only be set by instantiation')
            self._add_draw_object(Ruler(length=val, unit=self.unit))
            self._length = val

    @property
    def unit(self):
        return self._unit

    def update_units(self):
        for voice in self.draw_objects:
            voice.update_unit(self.unit)

    @unit.setter
    def unit(self, val):
        self._unit = val
        self.update_units()

    def add_voice(self, name):
        voice = Voice(length=self.length, unit=self.unit, name=name)
        return self._add_draw_object(voice)

    def add_draw_object(self, draw_object):
        raise TimeLineError('use add_voice instead')

    # @property
    # def line_groups(self):
    #     if self._line_groups is None:
    #         output = []
    #         for index, line_ in enumerate(self.ruler.lines):
    #             gl = DrawObjectGroup(inner_distance=self.inner_distance, bottom_distance=self.bottom_margin)
    #             gl.add_line(line)
    #             for voice in self.voices:
    #                 gl.add_line(voice.line_segments[index])
    #             output.append(gl)
    #         self._line_groups = output
    #     return self._line_groups

    # def get_relative_x2(self):
    #     raise Exception('timeline has no x2 value')
    #
    # def get_relative_y2(self):
    #     return self._segmented_line_group.get_relative_y2()

    # def get_height(self):
    #     return self.get_relative_y2() - self.relative_y
    #
    # def draw(self, pdf):
    #     for voice in self._segmented_line_group:
    #         voice.
    #         if line_group == self.line_groups[0]:
    #             for fractal_tree, line in zip(self.get_children()[1:], line_group.lines[1:]):
    #                 line.name = fractal_tree.name
    #                 if line.name:
    #                     line.name.relative_y = line.relative_y
    #
    #         line_group.draw_with_break(pdf)
    #         new_x = pdf.x
    #
    #         if line_group._line_break:
    #             for fractal_tree, line in zip(self.get_children(), line_group.lines):
    #                 pdf.x = new_x - line_group.length
    #                 line.name = fractal_tree.name
    #
    #                 if line.name:
    #                     line.name.draw(pdf)
    #             pdf.x = new_x
