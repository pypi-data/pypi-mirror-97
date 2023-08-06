from musurgia.agpdf.textlabel import TextLabel


class Labeled(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text_labels = []

    def add_text_label(self, val, **kwargs):
        if val is not None and not isinstance(val, TextLabel):
            val = TextLabel(val, **kwargs)
        val.parent = self
        self._text_labels.append(val)
        return val

    @property
    def text_labels(self):
        return self._text_labels

    def remove_text_labels(self):
        self._text_labels = []
