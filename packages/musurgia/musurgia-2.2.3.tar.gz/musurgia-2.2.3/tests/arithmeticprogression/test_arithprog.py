from unittest import TestCase

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.quantize import get_quantized_values


class Test(TestCase):
    def setUp(self) -> None:
        self.arith_prog = ArithmeticProgression()

    def test_1(self):
        result = {'a1': None, 'an': None, 'n': None, 'd': None, 's': None}
        self.assertEqual(result, self.arith_prog._parameters_dict)

    def test_2(self):
        self.arith_prog.n = 15
        self.arith_prog.a1 = 1
        self.arith_prog.d = 2
        result = {'a1': 1, 'an': 29, 'n': 15, 'd': 2, 's': 225.0}
        self.assertEqual(result, self.arith_prog.parameters_dict)

    def test_3(self):
        self.arith_prog.n = 15
        self.arith_prog.a1 = 1
        self.arith_prog.d = 2
        result = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
        self.assertEqual(result, list(self.arith_prog))

    def test_4(self):
        self.arith_prog.a1 = 36
        self.arith_prog.an = 25
        self.arith_prog.s = 230
        # print(self.arith_prog.parameters_dict)
        values = list(self.arith_prog)
        # print(values)
        quantized = get_quantized_values(values, 1)
        # print(quantized)
        # print(sum(quantized))
        result = [36, 34, 32, 31, 29, 26, 25]
        self.assertEqual(result, quantized)

    def test_5(self):
        self.arith_prog.a1 = 0.2
        self.arith_prog.an = 1.5
        self.arith_prog.s = 20

        self.arith_prog.correct_s = True
        test_case = sum(list(self.arith_prog))
        expected = self.arith_prog.s
        self.assertEqual(expected, test_case)

    def test_6(self):
        self.arith_prog.n = 15
        self.arith_prog.a1 = 1
        self.arith_prog.d = 2
        copy = self.arith_prog.__deepcopy__()
        actual = {'a1': 1, 'an': 29, 'n': 15, 'd': 2, 's': 225.0}
        expected = copy.parameters_dict
        self.assertEqual(expected, actual)

    def test_7(self):
        self.arith_prog.n = 5
        self.arith_prog.a1 = 1
        self.arith_prog.s = 15
        expected = 1
        actual = self.arith_prog.d
        self.assertEqual(expected, actual)

    def test_8(self):
        self.arith_prog.n = 5
        self.arith_prog.a1 = 1
        self.arith_prog.s = 15
        self.arith_prog.d
        expected = 5
        actual = self.arith_prog.an
        self.assertEqual(expected, actual)
