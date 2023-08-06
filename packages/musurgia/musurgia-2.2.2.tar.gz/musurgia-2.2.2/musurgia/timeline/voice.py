from musurgia.pdf.named import Named
from musurgia.timeline.abstractvoice import AbstractVoice


class VoiceError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VoiceSegment(object):
    def __init__(self, start, stop, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = None
        self._stop = None
        self.start = start
        self.stop = stop
        self._parent = None
        self.parent = parent
        self._lines = None

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, val):
        if not isinstance(val, int):
            raise TypeError('start.value must be of type int not{}'.format(type(val)))
        self._start = val

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, val):
        if not isinstance(val, int):
            raise TypeError('stop.value must be of type int not{}'.format(type(val)))
        self._stop = val

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        if val is not None and not isinstance(val, Voice):
            raise TypeError('parent.value must be of type Voice not{}'.format(type(val)))
        self._parent = val

    @property
    def lines(self):
        if not self._lines:
            self._lines = self.parent.line_segments[self.start:self.stop]
        return self._lines

    def apply_to_parent(self):
        for line in self.lines:
            line.show = True
            if line != self.lines[0]:
                line.start_mark_line.show = False
            if line == self.lines[-1]:
                line.end_mark_line.show = True


class Voice(AbstractVoice, Named):
    def __init__(self, segments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._segments = []
        self.segments = segments
        self.hide_all()

    def hide_all(self):
        for line_segment in self.line_segments:
            line_segment.show = False

    @property
    def segments(self):
        return self._segments

    @segments.setter
    def segments(self, val):
        if val is None:
            self._segments = []
        else:
            if not isinstance(val, list):
                raise TypeError('segments.value must be of type list not{}'.format(type(val)))
            self._segments = []
            for v in val:
                self.add_voice_segment(*v)

    def add_voice_segment(self, start, end):
        vs = VoiceSegment(start, end, parent=self)
        self._segments.append(vs)
        vs.apply_to_parent()
        return vs
