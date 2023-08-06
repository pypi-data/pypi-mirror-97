from pathlib import Path

import matplotlib as mpl
from matplotlib.afm import AFM


class FontError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _make_afm_path_dictionary():
    def check_entry():
        old_afm = output.get((family, weight, style))
        if old_afm is not None:
            old_header = old_afm._header
            new_header = afm._header
            diff = set(old_header) ^ set(new_header)
            if diff == {b'CapHeight'}:
                if new_header.get(b'CapHeight'):
                    return True
                #
                # print('old:', old_header.get(b'CapHeight'))
                # print('new:', new_header.get(b'CapHeight'))
            elif diff == set():
                return False
            else:
                raise AttributeError(
                    f'{family},  {weight}, {style} already in dict: {old_afm} differnce: {diff}')
        else:
            return True

    output = {}
    directory = Path(mpl.get_data_path(), 'fonts', 'afm')
    for file in directory.iterdir():
        afm_path = file
        with afm_path.open('rb') as fh:
            afm = AFM(fh)
        family = afm.get_familyname()
        weight = afm.get_weight().lower()
        if afm.get_angle() < 0:
            style = 'italic'
        else:
            style = 'regular'
        if check_entry():
            output[family, weight, style] = afm

    return output


class Font:
    __AFM_PATH_DICTIONARY = _make_afm_path_dictionary()

    _FAMILY = ['Helvetica', 'Courier', 'Times']
    _WEIGHT = ['bold', 'medium']
    _STYLE = ['italic', 'regular']

    def __init__(self, family='Helvetica', weight='medium', style='regular', size=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._family = None
        self._weight = None
        self._style = None
        self._size = None
        self._afm = None

        self.family = family
        self.weight = weight
        self.style = style
        self.size = size

    def _set_afm(self):
        if self.family and self.weight and self.style:
            self._afm = self.__AFM_PATH_DICTIONARY[self.family, self.weight, self.style]

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, val):
        if val not in self._FAMILY:
            raise FontError(f'{val} not a valid value: current valid families are: {self._FAMILY}')
        self._family = val
        self._set_afm()

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, val):
        if val not in self._WEIGHT:
            raise FontError('{} not a valid value: {}'.format(val, self._WEIGHT))
        self._weight = val
        self._set_afm()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val):
        if val not in self._STYLE:
            raise FontError('{} not a valid value: {}'.format(val, self._STYLE))
        self._style = val
        self._set_afm()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    def get_text_pixel_width(self, val):
        return (self._afm.string_width_height(val)[0] / 1000) * self.size

    def get_text_pixel_height(self, val):
        return (self._afm.string_width_height(val)[1] / 1000) * self.size
