class MarginedOrbjectError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MarginNotSettableError(MarginedOrbjectError):
    def __init__(self, *args):
        super().__init__(*args)


class Margined:
    def __init__(self, top_margin=None, bottom_margin=None, left_margin=None, right_margin=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._top_margin = None
        self._left_margin = None
        self._bottom_margin = None
        self._right_margin = None

        self.top_margin = top_margin
        self.left_margin = left_margin
        self.bottom_margin = bottom_margin
        self.right_margin = right_margin


    @property
    def top_margin(self):
        if self._top_margin is None:
            return 0
        return self._top_margin

    @top_margin.setter
    def top_margin(self, val):
        self._top_margin = val

    @property
    def left_margin(self):
        if self._left_margin is None:
            return 0
        return self._left_margin

    @left_margin.setter
    def left_margin(self, val):
        self._left_margin = val

    @property
    def bottom_margin(self):
        if self._bottom_margin is None:
            return 0
        return self._bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, val):
        self._bottom_margin = val

    @property
    def right_margin(self):
        if self._right_margin is None:
            return 0
        return self._right_margin

    @right_margin.setter
    def right_margin(self, val):
        self._right_margin = val
