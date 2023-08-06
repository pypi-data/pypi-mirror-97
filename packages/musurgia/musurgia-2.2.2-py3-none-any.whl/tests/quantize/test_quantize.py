from unittest import TestCase

from quicktions import Fraction

from musurgia.basic_functions import xToD, dToX
from musurgia.quantize import get_quantized_values, find_best_quantized_values


class Test(TestCase):

    def test_1(self):
        input = [0.2, 0.333, 0.6, 0.99, 0.1, 0.5]
        example = get_quantized_values(input, 0.6)
        result = [Fraction(0, 1), Fraction(3, 5), Fraction(3, 5), Fraction(6, 5), Fraction(0, 1), Fraction(0, 1)]
        self.assertEqual(result, example)

    def test_2(self):
        midis = [60, 61.5, 58.5, 56.5, 63]
        intervals = xToD(midis)
        quantized_intervals = get_quantized_values(intervals, 1)
        quantized_midis = [int(x) for x in dToX(quantized_intervals, first_element=midis[0])]
        result = [60, 61, 58, 57, 63]
        self.assertEqual(result, quantized_midis)

    def test_find_best_unit_without_check_sum(self):
        values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        units = [0.5, 0.7, 0.2]
        actual = find_best_quantized_values(values=values, units=units, check_sum=False)
        expected = [Fraction(1, 5), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(3, 5), Fraction(3, 5),
                    Fraction(4, 5)]
        self.assertEqual(expected, actual)

    def test_find_best_unit_with_check_sum(self):
        values = [Fraction(1,7), Fraction(3, 7), Fraction(5, 7)]
        units = [Fraction(1, 2), Fraction(1, 7), Fraction(1, 5)]
        actual = find_best_quantized_values(values=values, units=units, check_sum=True)
        expected = [Fraction(1, 7), Fraction(3, 7), Fraction(5, 7)]

        self.assertEqual(expected, actual)

    def test_find_best_unit_with_check_sum_2(self):
        values = [1, 2, 3, 4, 5]
        units = [Fraction(1, 2), Fraction(1, 7), Fraction(1, 5)]
        actual = find_best_quantized_values(values=values, units=units, check_sum=True)