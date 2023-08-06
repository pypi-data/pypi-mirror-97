import os

from musurgia.unittest import TestCase


path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def test_1_1(self):
        with self.assertRaises(ValueError):
            wrong_path = path + '_test_1'
            self.assertCompareFiles(wrong_path)

    def test_1_2(self):
        actual_file_path = path + '_test_1.txt'
        self.assertCompareFiles(actual_file_path)

    def test_2_1(self):
        actual_file_path = path + '_test_2.txt'
        with self.assertRaises(AssertionError):
            self.assertCompareFiles(actual_file_path)

    def test_2_2(self):
        actual_file_path = path + '_test_2.txt'
        expected_file_path= path + '_test_1_expected.txt'
        self.assertCompareFiles(actual_file_path=actual_file_path, expected_file_path=expected_file_path)
