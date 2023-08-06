import os

from prettytable import PrettyTable


class AGTable(PrettyTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def writ_to_path(self, table_path, title=None):
        os.system('touch ' + table_path)
        file = open(table_path, 'w')
        if title:
            file.write(title + '\n')

        file.write(self.get_string())
        file.close()

    def extend(self, other_table):
        if not isinstance(other_table, AGTable):
            raise TypeError()
        for row in other_table._rows:
            self.add_row(row)

    def get_row(self, index):
        return self._rows[index]

    @property
    def rows(self):
        return self._rows
