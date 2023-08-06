class PdfUnit:
    _DEFAULT_UNIT = 'mm'
    GLOBAL_UNIT = _DEFAULT_UNIT

    @staticmethod
    def get_k():
        k_dict = {'pt': 1, 'mm': 72 / 25.4, 'cm': 72 / 2.54, 'in': 72.}
        k = k_dict.get(PdfUnit.GLOBAL_UNIT)
        if k is None:
            raise AttributeError(f'wrong unit {PdfUnit.GLOBAL_UNIT}')
        return k

    @staticmethod
    def reset():
        PdfUnit.GLOBAL_UNIT = PdfUnit._DEFAULT_UNIT

    @staticmethod
    def change(val):
        PdfUnit.GLOBAL_UNIT = val
#
# def _get_unit(k):
#     unit_dict = {1: 'pt', 72. / 25.4: 'mm', 72. / 2.54: 'cm', 72.: 'in'}
#     unit = unit_dict.get(k)
#     if k is None:
#         raise AttributeError(f'wrong k {k}')
#     return unit
