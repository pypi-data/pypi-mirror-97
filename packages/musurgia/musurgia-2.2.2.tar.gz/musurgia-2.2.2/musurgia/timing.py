class Clock(object):
    def __init__(self, duration=None, clock=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._duration = None
        self._clock = None
        self.duration = duration
        self.clock = clock

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, val):
        if val is None:
            val = 0
        self._duration = val
        self._calculate_clock()

    @property
    def clock(self):
        return self._clock

    @clock.setter
    def clock(self, val):
        if val is None:
            val = (0, 0, 0)
        self._clock = val
        self._calculate_duration()

    def _calculate_clock(self):
        h = int(self.duration / 3600.0)
        s = self.duration - h * 3600
        m = int(s / 60.)
        self._clock = (h, m, s)

    def _calculate_duration(self):
        self._duration = self.clock[0] * 3600 + self.clock[1] * 60 + self.clock[2]

    def add(self, clock2):
        output = Clock()
        output.duration = self.duration + clock2.duration
        return output

    def subtract(self, clock2):
        output = Clock()
        output.duration = self.duration - clock2.duration
        return output


class Timing(object):

    @staticmethod
    def get_clock(time, mode='hms'):
        h = int(time / 3600.0)
        s = time - h * 3600
        m = int(s / 60.)
        s = round(s - m * 60, 1)

        if m / 10 == 0 and mode != 'msreduced':
            m = '0' + str(m) + '\''
        else:
            m = str(m) + '\''

        if int(s / 10) == 0 and mode != 'msreduced':
            s = '0' + str(s) + '\"'
        else:
            s = str(s) + '\"'
        h = str(h)

        if not mode or mode == 'hms':
            return h + ':' + m + ':' + s

        elif mode == 'ms':
            return m + ':' + s
        elif mode == 'msreduced':
            if m == '0\'':
                return s
            else:
                return m + ':' + s
        else:
            raise ValueError('mode not known')

    def __init__(self, quarter_duration=None, duration=None, tempo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self._duration = None
        self._tempo = None

        self.tempo = tempo
        self.quarter_duration = quarter_duration
        self.duration = duration

    @property
    def duration(self):
        if self._duration is None:
            return self.quarter_duration * 60. / self.tempo

        return self._duration

    @duration.setter
    def duration(self, value):
        if value:
            if self._quarter_duration is not None and self._tempo is not None:
                raise Exception('quarter_duration and tempo are already set. duration cannot be set anymore.')
            self._duration = value

    @property
    def quarter_duration(self):
        if self._quarter_duration is None:
            return self.duration * self.tempo / 60
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if value:
            if self._tempo and self._duration:
                raise Exception('duration and tempo are already set. quarter_duration cannot be set anymore.')
            self._quarter_duration = value

    @property
    def tempo(self):
        if self._tempo is None:
            return self.quarter_duration * 60. / self.duration
        return self._tempo

    @tempo.setter
    def tempo(self, value):
        if value:
            if self._quarter_duration and self._duration:
                raise Exception('duration and quarter_duration are already set. tempo cannot be set anymore.')
            self._tempo = value

    @property
    def clock(self):
        h = int(self.duration / 3600.0)
        s = self.duration - h * 3600
        m = int(s / 60.)
        s = round(s - m * 60, 1)
        if m / 10 == 0:
            m = '0' + str(m) + '\''
        else:
            m = str(m) + '\''

        if int(s / 10) == 0:
            s = '0' + str(s) + '\"'
        else:
            s = str(s) + '\"'
        h = str(h)
        return h + ':' + m + ':' + s
