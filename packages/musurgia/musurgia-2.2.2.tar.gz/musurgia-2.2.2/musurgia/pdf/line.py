from abc import abstractmethod

from quicktions import Fraction

from musurgia.pdf.labeled import Labeled
from musurgia.pdf.masterslave import Master, Slave
from musurgia.pdf.newdrawobject import DrawObject
from musurgia.pdf.rowcolumn import DrawObjectRow, DrawObjectColumn, DrawObjectContainer
from musurgia.pdf.text import TextLabel


class StraightLine(Slave, DrawObject, Labeled):
    def __init__(self, mode, length, show=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = None
        self._length = None

        self.mode = mode
        self.length = length
        self.show = show

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        permitted = ['h', 'horizontal', 'v', 'vertical']
        if val not in permitted:
            raise ValueError(f'mode.value {val} must be in {permitted}')
        self._mode = val

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        if not isinstance(val, float) and not isinstance(val, int) and not isinstance(val, Fraction):
            raise TypeError(f"length.value must be of type float, int or Fraction  not{type(val)}")
        self._length = val

    @property
    def is_vertical(self):
        if self.mode in ['v', 'vertical']:
            return True
        else:
            return False

    @property
    def is_horizontal(self):
        if self.mode in ['h', 'horizontal']:
            return True
        else:
            return False

    @staticmethod
    def get_opposite_mode(mode):
        if mode == 'h':
            return 'v'
        elif mode == 'v':
            return 'h'
        elif mode == 'horizontal':
            return 'vertical'
        elif mode == 'vertical':
            return 'horizontal'
        else:
            raise AttributeError()

    def get_relative_x2(self):
        if self.mode in ['h', 'horizontal']:
            return self.relative_x + self.length
        else:
            return self.relative_x

    def get_relative_y2(self):
        if self.mode in ['v', 'vertical']:
            return self.relative_y + self.length
        else:
            return self.relative_y

    def draw(self, pdf):
        if self.show:
            with pdf.prepare_draw_object(self):
                self.draw_above_text_labels(pdf)
                self.draw_left_text_labels(pdf)
                x2 = self.get_relative_x2() - self.relative_x
                y2 = self.get_relative_y2() - self.relative_y
                pdf.line(0, 0, x2, y2)
                self.draw_below_text_labels(pdf)


class MarkLine(StraightLine):
    def __init__(self, placement, length=3, *args, **kwargs):
        super().__init__(length=length, *args, **kwargs)
        self._placement = None
        self.placement = placement

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, val):
        permitted = ['start', 'end']
        if val not in permitted:
            raise ValueError(f'placement.value {val} must be in {permitted}')
        self._placement = val

    def get_middle_y(self):
        return self.length / 2


class LineSegment(Master, DrawObject):
    def __init__(self, mode, length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._straight_line = StraightLine(name='straight_line', mode=mode, length=length, master=self)
        marker_mode = StraightLine.get_opposite_mode(self.mode)
        self._start_mark_line = MarkLine(name='start_mark_line', mode=marker_mode, master=self, placement='start')
        self._end_mark_line = MarkLine(name='end_mark_line', mode=marker_mode, master=self, placement='end', show=False)

    @property
    def straight_line(self):
        return self._straight_line

    @property
    def start_mark_line(self):
        return self._start_mark_line

    @property
    def end_mark_line(self):
        return self._end_mark_line

    @property
    def mode(self):
        return self.straight_line.mode

    @property
    def length(self):
        return self.straight_line.length

    def _get_straight_line_margin(self, margin):
        if margin in ['l', 'left']:
            return 0
        elif margin in ['r', 'right']:
            return 0
        elif margin in ['t', 'top']:
            return 0
        elif margin in ['b', 'bottom']:
            return 0
        else:
            raise AttributeError(margin)

    def _get_mark_line_margin(self, margin):
        if margin in ['l', 'left']:
            return 0
        elif margin in ['r', 'right']:
            return 0
        elif margin in ['t', 'top']:
            return 0
        elif margin in ['b', 'bottom']:
            return 0
        else:
            raise AttributeError(margin)

    def _get_straight_line_position(self, position):
        if position not in ['x', 'y']:
            raise AttributeError(position)

        if self.mode in ['h', 'horizontal']:
            if position == 'x':
                return 0
            elif position == 'y':
                return 0
                # return max([ml.get_middle_y() for ml in [self.start_mark_line, self.end_mark_line]])
        else:
            if position == 'x':
                return 0
                # return max([ml.get_middle_y() for ml in [self.start_mark_line, self.end_mark_line]])
            elif position == 'y':
                return 0

    def _get_mark_line_position(self, position, mark_line):
        if position not in ['x', 'y']:
            raise AttributeError(position)

        if mark_line.mode in ['h', 'horizontal']:
            if position == 'x':
                # return 0
                return -mark_line.length / 2
            else:
                if mark_line.placement == 'start':
                    return 0
                else:
                    return self.length
        else:
            if position == 'y':
                # return 0
                return -mark_line.length / 2
            else:
                if mark_line.placement == 'start':
                    return 0
                else:
                    return self.length

    def get_slave_margin(self, slave, margin):
        if slave.name == 'straight_line':
            return self._get_straight_line_margin(margin)
        elif slave.name == 'start_mark_line':
            return self._get_mark_line_margin(margin)
        elif slave.name == 'end_mark_line':
            return self._get_mark_line_margin(margin)
        else:
            raise AttributeError(slave)

    def get_slave_position(self, slave, position):
        if slave.name == 'straight_line':
            return self._get_straight_line_position(position)
        elif slave.name == 'start_mark_line':
            return self._get_mark_line_position(position, slave)
        elif slave.name == 'end_mark_line':
            return self._get_mark_line_position(position, slave)
        else:
            raise AttributeError(slave)


class HorizontalLineSegment(LineSegment):
    def __init__(self, length, *args, **kwargs):
        super().__init__(mode='horizontal', length=length, *args, **kwargs)

    def get_relative_x2(self):
        return self.relative_x + self.length

    def get_relative_y2(self):
        return self.relative_y + max([ml.get_height() for ml in [self.start_mark_line, self.end_mark_line]])

    def draw(self, pdf):
        with pdf.prepare_draw_object(self):
            self.start_mark_line.draw(pdf)
            self.straight_line.draw(pdf)
            self.end_mark_line.draw(pdf)


class VerticalLineSegment(LineSegment):
    def __init__(self, length, *args, **kwargs):
        super().__init__(mode='vertical', length=length, *args, **kwargs)

    def get_relative_x2(self):
        return self.relative_x + max([ml.get_width() for ml in [self.start_mark_line, self.end_mark_line]])

    def get_relative_y2(self):
        return self.relative_y + self.length

    def draw(self, pdf):
        with pdf.prepare_draw_object(self):
            self.start_mark_line.draw(pdf)
            self.straight_line.draw(pdf)
            self.end_mark_line.draw(pdf)


class AbstractSegmentedLine(DrawObjectContainer):
    def __init__(self, lengths, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._make_segments(lengths)

    @property
    def lengths(self):
        return [segment.length for segment in self.segments]

    @property
    def segments(self):
        return self.draw_objects

    @abstractmethod
    def _make_segments(self, lengths):
        pass


class HorizontalSegmentedLine(AbstractSegmentedLine, DrawObjectRow):

    def _make_segments(self, lengths):
        if not lengths:
            raise AttributeError('lengths must be set.')
        for length in lengths:
            self.add_draw_object(HorizontalLineSegment(length))
        self.segments[-1].end_mark_line.show = True


class VerticalSegmentedLine(AbstractSegmentedLine, DrawObjectColumn):

    def _make_segments(self, lengths):
        if not lengths:
            raise AttributeError('lengths must be set.')
        for length in lengths:
            self.add_draw_object(VerticalLineSegment(length))
        self.segments[-1].end_mark_line.show = True


class AbstractRuler(AbstractSegmentedLine):
    def __init__(self, length, unit=10.0, first_label=0, label_show_interval=1, show_first_label=True, *args, **kwargs):
        number_of_units = length / unit
        partial_segment_length = number_of_units - int(number_of_units)
        lengths = int(number_of_units) * [unit]
        if partial_segment_length:
            lengths += [partial_segment_length * unit]
        super().__init__(lengths=lengths, *args, **kwargs)
        if partial_segment_length:
            self.draw_objects[-1].end_mark_line.show = False
        self.unit = unit
        self.first_label = first_label
        self.label_show_interval = label_show_interval
        self.show_first_label = show_first_label
        self._set_labels()

    @property
    def length(self):
        return sum([s.length for s in self.segments])

    def _set_labels(self):
        def _add_label(mark_line, txt):
            tl = TextLabel(txt)
            if isinstance(self, VerticalSegmentedLine):
                tl.placement = 'left'
                tl.right_margin = 1
                tl.top_margin = 0
            else:
                tl.bottom_margin = 1
            mark_line.add_text_label(tl)

        for index, segment in enumerate(self.segments):
            if not self.show_first_label and index == 0:
                pass
            else:
                if index % self.label_show_interval == 0:
                    mark_line = segment.start_mark_line
                    _add_label(mark_line, index + self.first_label)

        last_segment_end_mark_line = self.segments[-1].end_mark_line
        if last_segment_end_mark_line.show and (len(self.segments)) % self.label_show_interval == 0:
            _add_label(last_segment_end_mark_line, len(self.segments) + self.first_label)


class HorizontalRuler(AbstractRuler, HorizontalSegmentedLine):
    pass


class VerticalRuler(AbstractRuler, VerticalSegmentedLine):
    pass
