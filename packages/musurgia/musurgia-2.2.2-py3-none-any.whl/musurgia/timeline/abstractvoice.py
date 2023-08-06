from musurgia.pdf.segmentedline import SegmentedLine
from musurgia.tree import Tree


class AbstractVoice(SegmentedLine):
    def __init__(self, length, unit=10, *args, **kwargs):
        self._length = None
        self.length = length
        self._unit = None
        self.unit = unit
        super().__init__(lengths=self.length * [self.unit], *args, **kwargs)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        if not isinstance(val, int):
            raise TypeError('length {} must be of type int not {}'.format(val, type(val)))
        if val < 1:
            raise ValueError('length {} must be a positive non zero integer'.format(val))
        self._length = val

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, val):
        if val < 0:
            raise ValueError('unit {} must be a positive number'.format(val))
        self._unit = val

    def update_unit(self, unit):
        if self.unit == unit:
            pass
        else:
            self.unit = unit
            for line in self.line_segments:
                line.length = unit
