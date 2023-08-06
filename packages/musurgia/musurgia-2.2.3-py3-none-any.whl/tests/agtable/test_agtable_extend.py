import os

from musurgia.agtable.agtable import AGTable
from musurgia.agunittest import AGTestCase

path = str(os.path.abspath(__file__).split('.')[0])


class Test(AGTestCase):
    def test_1(self):
        main_table = AGTable(hrules=1)
        main_table.field_names = [1, 2, 3]
        main_table.add_row(['a', 'b', 'c'])
        side_table = AGTable()
        side_table.add_row(['aa', 'bb', 'cc'])
        main_table.extend(side_table)
        table_path = path + '_test_1.txt'

        main_table.writ_to_path(table_path=table_path, title='test extend')
        self.assertCompareFiles(table_path)
