class FontError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Font(object):
    _FAMILY = ['Arial']
    _WEIGHT = ['bold', 'regular']
    _STYLE = ['italic', 'regular']

    def __init__(self, family='Arial', weight='regular', style='regular', size=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._family = None
        self._weight = None
        self._style = None
        self._size = None

        self.family = family
        self.weight = weight
        self.style = style
        self.size = size

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, val):
        if val not in self._FAMILY:
            raise FontError('{} not a valid value: {}'.format(val, self._FAMILY))
        self._family = val

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, val):
        if val not in self._WEIGHT:
            raise FontError('{} not a valid value: {}'.format(val, self._WEIGHT))
        self._weight = val

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val):
        if val not in self._STYLE:
            raise FontError('{} not a valid value: {}'.format(val, self._STYLE))
        self._style = val

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val
