from pathlib import Path

import matplotlib as mpl
from matplotlib.afm import AFM

from musurgia.unittest import TestCase

afm_path = Path(mpl.get_data_path(), 'fonts', 'afm', 'ptmr8a.afm')


def make_afm_path_dictionary():
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


class Test(TestCase):
    def test_afm_dict(self):
        actual = sorted(list(make_afm_path_dictionary().keys()))
        expected = [
            ('Computer Modern', 'medium', 'italic'),
            ('Computer Modern', 'medium', 'regular'),
            ('Courier', 'bold', 'italic'),
            ('Courier', 'bold', 'regular'),
            ('Courier', 'medium', 'italic'),
            ('Courier', 'medium', 'regular'),
            ('Helvetica', 'bold', 'italic'),
            ('Helvetica', 'bold', 'regular'),
            ('Helvetica', 'light', 'italic'),
            ('Helvetica', 'light', 'regular'),
            ('Helvetica', 'medium', 'italic'),
            ('Helvetica', 'medium', 'regular'),
            ('ITC Avant Garde Gothic', 'book', 'italic'),
            ('ITC Avant Garde Gothic', 'book', 'regular'),
            ('ITC Avant Garde Gothic', 'demi', 'italic'),
            ('ITC Avant Garde Gothic', 'demi', 'regular'),
            ('ITC Bookman', 'demi', 'italic'),
            ('ITC Bookman', 'demi', 'regular'),
            ('ITC Bookman', 'light', 'italic'),
            ('ITC Bookman', 'light', 'regular'),
            ('ITC Zapf Chancery', 'medium', 'italic'),
            ('ITC Zapf Dingbats', 'medium', 'regular'),
            ('New Century Schoolbook', 'bold', 'italic'),
            ('New Century Schoolbook', 'bold', 'regular'),
            ('New Century Schoolbook', 'medium', 'italic'),
            ('New Century Schoolbook', 'roman', 'regular'),
            ('Palatino', 'bold', 'italic'),
            ('Palatino', 'bold', 'regular'),
            ('Palatino', 'medium', 'italic'),
            ('Palatino', 'roman', 'regular'),
            ('Symbol', 'medium', 'regular'),
            ('Times', 'bold', 'italic'),
            ('Times', 'bold', 'regular'),
            ('Times', 'medium', 'italic'),
            ('Times', 'roman', 'regular'),
            ('Utopia', 'bold', 'italic'),
            ('Utopia', 'bold', 'regular'),
            ('Utopia', 'regular', 'italic'),
            ('Utopia', 'regular', 'regular')]
        self.assertEqual(expected, actual)

    def test_afm_dict_families(self):
        actual = list(dict.fromkeys([key[0] for key in make_afm_path_dictionary().keys()]))
        expected = ['New Century Schoolbook',
                    'Times',
                    'ITC Bookman',
                    'Helvetica',
                    'ITC Avant Garde Gothic',
                    'Palatino',
                    'Computer Modern',
                    'Symbol',
                    'ITC Zapf Dingbats',
                    'Utopia',
                    'Courier',
                    'ITC Zapf Chancery']
        self.assertEqual(expected, actual)

    def test_load_afm(self):
        afm = make_afm_path_dictionary()['Times', 'medium', 'italic']
        actual = afm.get_familyname()
        expected = 'Times'
        self.assertEqual(expected, actual)

    def test_width_height(self):
        afm = make_afm_path_dictionary()['Helvetica', 'bold', 'italic']
        actual = afm.string_width_height('What the heck?')
        expected = (7370.0, 741)
        self.assertEqual(expected, actual)
