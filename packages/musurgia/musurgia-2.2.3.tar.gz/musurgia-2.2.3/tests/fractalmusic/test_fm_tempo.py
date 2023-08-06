from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic, TempoIsAlreadySet, ChildTempoIsAlreadySet


class Test(TestCase):
    def test_1(self):
        fm = FractalMusic(duration=100)
        fm.tempo = 72
        fm.add_layer()
        with self.assertRaises(TempoIsAlreadySet):
            fm.get_children()[0].tempo = 60

    def test_2(self):
        fm = FractalMusic(duration=100)
        fm.add_layer()
        fm.get_children()[0].tempo = 72
        with self.assertRaises(ChildTempoIsAlreadySet):
            fm.tempo = 60

    def test_3(self):
        fm = FractalMusic(duration=100)
        fm.add_layer()
        try:
            fm.tempo = 60
        except (ChildTempoIsAlreadySet, TempoIsAlreadySet) as err:
            self.fail(err + "was raised!")

    def test_4(self):
        fm = FractalMusic(duration=100)
        fm.add_layer()
        fm.get_children()[0].tempo = 72
        fm.set_none_tempi(90)
        self.assertEqual([child.tempo for child in fm.get_children()], [72, 90., 90])

    def test_5(self):
        fm = FractalMusic(duration=100)
        fm.add_layer()
        fm.tempo = 72
        self.assertEqual([child.tempo for child in fm.get_children()], [72, 72, 72])

    def test_6(self):
        fm = FractalMusic(duration=100)
        fm.add_layer()

        fm.get_children()[1].tempo = 80
        fm.add_layer()
        fm.get_children()[2].get_children()[2].tempo = 72
        fm.add_layer()

        self.assertEqual(fm.get_layer(2, key='tempo'), [[None, None, None], [80, 80, 80], [None, None, 72]])

    def test_7(self):
        fm = FractalMusic(duration=100)
        fm.add_layer()

        fm.get_children()[1].tempo = 80
        fm.add_layer()
        fm.get_children()[2].get_children()[2].tempo = 72
        fm.add_layer()
        fm.set_none_tempi(60)

        self.assertEqual(fm.get_layer(2, key='tempo'), [[60, 60, 60], [80, 80, 80], [60, 60, 72]])

    def test_8(self):
        fm = FractalMusic(duration=100)
        fm.tempo = 72
        fm.add_layer()
        fm.add_layer()
        fm.add_layer()
        fm.set_none_tempi(60)

        self.assertEqual(fm.get_layer(2, key='tempo'), [[72, 72, 72], [72, 72, 72], [72, 72, 72]])
