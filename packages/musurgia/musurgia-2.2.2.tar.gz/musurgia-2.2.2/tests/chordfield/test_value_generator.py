from itertools import cycle

from musicscore.musicstream.streamvoice import SimpleFormat

from musurgia.unittest import TestCase
from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGenerator, NoDurationError, PositionError
from musurgia.interpolation import RandomInterpolation


class Test(TestCase):
    def test_1(self):
        vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=20, correct_s=True), duration=100)
        expected = 20
        actual = sum(list(vg))
        self.assertEqual(expected, actual)

    def test_2(self):
        with self.assertRaises(NoDurationError):
            vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=10, correct_s=True))
            vg.__next__()

    def test_3(self):
        vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=10, correct_s=True), duration=20,
                            value_mode='duration')
        expected = 20
        actual = sum(list(vg))
        self.assertEqual(expected, actual)

    def test_4(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        vg.position = 20
        with self.assertRaises(StopIteration):
            vg.__next__()

    def test_5(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        expected = 1
        actual = vg(19)
        self.assertEqual(expected, actual)

    def test_6(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        with self.assertRaises(PositionError):
            vg(20)

    def test_7(self):
        vg = ValueGenerator(generator=cycle([1]), duration=20)
        with self.assertRaises(PositionError):
            vg(20)

    # def test_8(self):
    #     vg = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, s=10), duration=20)
    #     with self.assertRaises(CallConflict):
    #         vg(21)

    def test_9(self):
        vg = ValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10),
                            duration=10)
        actual = [vg(x / 2) for x in range(20)]
        expected = [1, 2, 2, 1, 1, 2, 3, 1, 3, 2, 3, 2, 4, 3, 2, 3, 2, 5, 4, 5]
        self.assertEqual(expected, actual)

    # def test_10(self):
    #     vg = ValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10),
    #                         duration=10)
    #     with self.assertRaises(GeneratorHasNoNextError):
    #         vg.__next__()

    # def test_11(self):
    #     vg = ValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10),
    #                         duration=10)
    #     with self.assertRaises(GeneratorHasNoNextError):
    #         list(vg)

    def test_12(self):
        vg = ValueGenerator(generator=RandomInterpolation(start=[1, 1, 2], end=[3, 4, 5], seed=10),
                            value_mode='duration',
                            duration=10)

        expected = [1, 2, 2, 4, 3]
        actual = list(vg)
        self.assertEqual(expected, actual)

    def test_13(self):
        vg = ValueGenerator(generator=iter([1, 2, 3, 2, 1, 2, 1, 2, 2]),
                            value_mode='duration', duration=10)
        expected = [1, 2, 3, 2, 1, 2]
        actual = list(vg)
        self.assertEqual(expected, actual)

    def test_14(self):
        vg = ValueGenerator(generator=iter(SimpleFormat(quarter_durations=[1, 2, 3, 2, 1, 2, 1, 2, 2]).chords),
                            value_mode='chord', duration=10)

        expected = [1, 2, 3, 2, 1, 2]
        actual = [ch.quarter_duration for ch in list(vg)]
        self.assertEqual(expected, actual)

    def test_15(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)
        actual = vgg.__next__()
        expected = 2
        self.assertEqual(expected, actual)

    def test_16(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)
        actual = vgg(6)
        expected = 3
        self.assertEqual(expected, actual)

    def test_17(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), duration=10,
                              value_mode='duration')
        vg_2 = ValueGenerator(generator=ArithmeticProgression(an=0.2, a1=1, correct_s=True), duration=5,
                              value_mode='duration')
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)
        actual = float(vgg(12))
        expected = 1.0416666666666667
        self.assertEqual(expected, actual)

    def test_18(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), duration=10,
                              value_mode='duration')
        vg_2 = ValueGenerator(generator=ArithmeticProgression(an=0.2, a1=1, correct_s=True), duration=5,
                              value_mode='duration')
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)
        vgg(12)
        actual = float(vgg.position)
        expected = 13.041666666666666
        self.assertEqual(expected, actual)

    def test_19(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=ArithmeticProgression(a1=0.2, an=1, correct_s=True), duration=10,
                              value_mode='duration')
        vg_2 = ValueGenerator(generator=ArithmeticProgression(an=0.2, a1=1, correct_s=True), duration=5,
                              value_mode='duration')
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)
        actual = [round(float(x), 3) for x in vgg]
        expected = [0.208, 0.264, 0.319, 0.375, 0.431, 0.486, 0.542, 0.597, 0.653, 0.708, 0.764, 0.819, 0.875, 0.931,
                    0.986, 1.042, 1.042, 0.923, 0.804, 0.685, 0.565, 0.446, 0.327, 0.208]
        self.assertEqual(expected, actual)

    def test_20(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)
        actual = vgg.duration
        expected = 15
        self.assertEqual(expected, actual)

    def test_21(self):
        vgg = ValueGenerator()
        vg_1 = ValueGenerator(generator=cycle([2]), duration=5)
        vg_2 = ValueGenerator(generator=cycle([3]), duration=10)
        vgg.add_child(vg_1)
        vgg.add_child(vg_2)

        copied = vgg.__deepcopy__()
        actual = copied.duration
        expected = 15
        self.assertEqual(expected, actual)
