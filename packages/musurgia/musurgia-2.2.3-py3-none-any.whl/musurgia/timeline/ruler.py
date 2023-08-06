from musurgia.pdf.text import TextLabel
from musurgia.timeline.abstractvoice import AbstractVoice
from musurgia.timing import Timing


class Ruler(AbstractVoice):
    def __init__(self, show_interval=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._show_interval = None
        self.show_interval = show_interval

    @property
    def show_interval(self):
        return self._show_interval

    @show_interval.setter
    def show_interval(self, val):
        if not isinstance(val, int):
            raise TypeError('show_interval.value must be of type int not{}'.format(type(val)))
        self._show_interval = val
        self.update_show_intervals()

    def update_show_intervals(self):
        for index, line_segment in enumerate(self.line_segments):
            seconds = index
            line_segment.start_mark_line.remove_text_labels()
            if seconds % self.show_interval == 0:
                line_segment.start_mark_line.add_text_label(
                    TextLabel(text=Timing.get_clock(seconds, mode='ms'), relative_y=-3, font_size=9))
                line_segment.start_mark_line.thickness = 4
