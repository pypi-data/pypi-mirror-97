from musurgia.agpdf.textlabel import TextLabel


class NameLabel(TextLabel):
    def __init__(self, text, relative_x=-10, relative_y=0, *args, **kwargs):
        super().__init__(text=text, relative_x=relative_x, relative_y=relative_y, *args, **kwargs)


class Named(object):
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if val is not None and not isinstance(val, NameLabel):
            val = NameLabel(val)
        self._name = val
        if self.name:
            self.name.parent = self
            self.name.relative_y += self.relative_y

    def __deepcopy__(self, memodict={}):
        return self.__class__(name=self.name.__deepcopy__())
