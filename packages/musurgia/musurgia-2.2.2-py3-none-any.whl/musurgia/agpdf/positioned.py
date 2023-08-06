class Positioned(object):
    def __init__(self, relative_x=None, relative_y=None, *args, **kwargs):
        self._relative_x = None
        self._relative_y = None
        self.relative_x = relative_x
        self.relative_y = relative_y
        super().__init__(*args, **kwargs)

    @property
    def relative_x(self):
        if self._relative_x is None:
            return 0
        return self._relative_x

    @relative_x.setter
    def relative_x(self, val):
        self._relative_x = val

    @property
    def relative_y(self):
        if self._relative_y is None:
            return 0
        return self._relative_y

    @relative_y.setter
    def relative_y(self, val):
        self._relative_y = val
