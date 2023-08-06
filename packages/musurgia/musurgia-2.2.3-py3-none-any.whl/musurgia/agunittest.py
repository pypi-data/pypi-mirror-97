from unittest import TestCase
import os

from diff_pdf_visually import pdfdiff


class AGTestCase(TestCase):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compare_pdfs(self, actual_file_path, expected_file_path, verbosity):
        self.assertTrue(pdfdiff(actual_file_path, expected_file_path, verbosity=verbosity))

    def _compare_contents(self, actual_file_path, expected_file_path):
        with open(actual_file_path, 'r') as myfile:
            result = myfile.read()

        with open(expected_file_path, 'r') as myfile:
            expected = myfile.read()

        self.assertEqual(expected, result)

    def assertCompareFiles(self, actual_file_path, expected_file_path=None, verbosity=0):
        file_name, extension = os.path.splitext(actual_file_path)
        if not expected_file_path:
            if not extension:
                raise ValueError('actual_file_path has no file extension')
            expected_file_path = file_name + '_expected' + extension

        if extension == '.pdf':
            self._compare_pdfs(actual_file_path, expected_file_path, verbosity=verbosity)
        else:
            self._compare_contents(actual_file_path, expected_file_path)
