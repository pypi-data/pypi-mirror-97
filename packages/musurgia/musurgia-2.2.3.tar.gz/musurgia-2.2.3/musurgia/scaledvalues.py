class ScaledValues(object):
    def __init__(self, old_min, old_max, new_min, new_max, step=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_min = old_min
        self.old_max = old_max
        self.new_min = new_min
        self.new_max = new_max
        self._step = None
        self.step = step

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, val):
        if val is not None and val <= 0:
            raise TypeError('step.value must positive not {}'.format(type(val)))
        self._step = val

    def __call__(self, x):
        y = self.new_min + (self.new_max - self.new_min) * (x - self.old_min) / (self.old_max - self.old_min)
        if self.step:
            y = round(y / self.step) * self.step
        return y
