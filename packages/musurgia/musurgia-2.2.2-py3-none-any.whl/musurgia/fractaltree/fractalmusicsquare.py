import os

from musurgia.table.table import Table
from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.fractaltree.fractaltree import FractalTreeException
from prettytable import PrettyTable
from quicktions import Fraction


class Module(FractalMusic):
    def __init__(self, row_number=None, column_number=None, *args, **kargs):
        super().__init__(*args, **kargs)
        self.row_number = row_number
        self.column_number = column_number
        self._parent_row = None
        self._parent_column = None
        self._name = None

    @property
    def parent_square(self):
        return self.parent_row.parent_square

    @property
    def parent_row(self):
        return self._parent_row

    @property
    def parent_column(self):
        return self._parent_column

    def set_name(self, value):
        self._name = value

    @property
    def name(self):
        if self._name:
            return self._name

        if self.row_number and self.column_number:
            return str(self.row_number) + '_' + str(self.column_number)
        else:
            return super().name

    def write_info(self, text_path, show_quarter_durations=False):
        os.system('touch ' + text_path)
        file = open(text_path, 'w')
        file.write("module_tempo: " + str(self.tempo))
        file.write("\n")
        x = PrettyTable(hrules=1)

        leaf_names = [leaf.name for leaf in self.traverse_leaves()]
        leaf_fractal_orders = [leaf.fractal_order for leaf in self.traverse_leaves()]

        leaf_durations = [leaf.duration for leaf in self.traverse_leaves()]

        rounded_leaf_durations = [round(float(dur), 2) for dur in leaf_durations]

        leaf_quarter_durations = [leaf.quarter_duration for leaf in self.traverse_leaves()]
        rounded_quarter_durations = [round(float(dur), 2) for dur in leaf_quarter_durations]

        x.field_names = ["name", "info", *leaf_names, "sum"]
        x.add_row([self.name, 'frac_ord', *leaf_fractal_orders, " "])
        x.add_row([self.name, 'durations', *rounded_leaf_durations, round(float(sum(leaf_durations)), 2)])
        if show_quarter_durations:
            x.add_row(
                [self.name, 'quarter_dur', *rounded_quarter_durations,
                 round(float(sum(leaf_quarter_durations)), 2)])

        file.write(x.get_string())
        file.close()

    def __deepcopy__(self, memodict={}):
        copied = super().__deepcopy__(memodict)
        copied.row_number = self.row_number
        copied.column_number = self.column_number
        copied._name = self._name

        return copied


class RowColumn(object):
    def __init__(self, parent_square, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_square = None
        self.parent_square = parent_square
        self._number = None
        self.number = number
        self._modules = []

    @property
    def parent_square(self):
        return self._parent_square

    @parent_square.setter
    def parent_square(self, value):
        if not isinstance(value, Square):
            raise TypeError('parent_square.value must be of type Square not {}'.format(type(value)))
        self._parent_square = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('number.value must be of type int not {}'.format(type(value)))
        if not 0 < value <= self.parent_square.side_size:
            raise ValueError('number.value must be of between 0 and {}'.format(self.parent_square.side_size))
        self._number = value

    @property
    def modules(self):
        return self._modules

    def get_module(self, number):
        return self.modules[number - 1]

    @property
    def quarter_duration(self):
        return sum([module.quarter_duration for module in self.modules])


class Row(RowColumn):
    def __init__(self, square, number, *args, **kwargs):
        super().__init__(square, number, *args, **kwargs)
        self._name = str(self.number)

    def _add_module(self, module):
        module._parent_row = self
        self._modules.append(module)

    def set_tempo(self, tempo):
        for module in self.modules:
            module.tempo = tempo

    def set_name(self, val):
        self._name = val

    @property
    def name(self):
        return self._name

    def change_module_quarter_duration(self, module_number, new_quarter_duration):
        factor = Fraction(Fraction(new_quarter_duration),
                          Fraction(self.modules[module_number - 1].quarter_duration))

        for index, module in enumerate(self.modules):
            module.duration = self.modules[index].duration * factor

    def change_module_duration(self, module_number, new_duration):
        factor = Fraction(
            Fraction(new_duration),
            Fraction(self.modules[module_number - 1].duration)
        )

        for index, module in enumerate(self.modules):
            module.duration = self.modules[index].duration * factor


class Column(RowColumn):
    def __init__(self, square, number, *args, **kwargs):
        super().__init__(square, number, *args, **kwargs)

    def _add_module(self, module):
        module._parent_column = self
        self._modules.append(module)


class Square(object):
    def __init__(self, duration, proportions, tree_permutation_order, first_multi=(1, 1),
                 reading_direction='horizontal', name=None):

        self._duration = None
        self._proportions = None
        self._modules = {}
        self._tree_permutation_order = None
        self._first_multi = (1, 1)
        self._reading_direction = None
        self._side_size = None
        self._name = None
        self._parent_square_group = None

        self.duration = duration
        self.proportions = proportions
        self.reading_direction = reading_direction
        self.tree_permutation_order = tree_permutation_order
        self.first_multi = first_multi
        self._rows = None
        self._columns = None
        self.name = name

    # //private methods
    def _calculate_module_values(self):
        if self.duration is not None and self.proportions is not None and self.tree_permutation_order is not None:
            row_durations = [self.duration * prop / float(sum(self.proportions)) for prop in self.proportions]
            for (row, column) in [(i + 1, j + 1) for i in range(self.side_size) for j in range(self.side_size)]:
                module_durations = [row_durations[row - 1] * prop / float(sum(self.proportions)) for prop in
                                    self.proportions]
                multi = self.index_to_r_c(
                    self.r_c_to_index(row, column) + self.r_c_to_index(self.first_multi[0], self.first_multi[1]))
                module = Module(duration=module_durations[column - 1],
                                tree_permutation_order=self.tree_permutation_order, proportions=self.proportions,
                                multi=multi, reading_direction=self.reading_direction)
                (module.row_number, module.column_number) = (row, column)
                self._modules[(row, column)] = module
                module._parent_square = self

    # //public properties
    @property
    def columns(self):
        if self._columns is None:
            self._columns = []
            for column_number in range(1, self.side_size + 1):
                column = Column(square=self, number=column_number)
                for row_number in range(1, self.side_size + 1):
                    module = self.get_module(row_number, column_number)
                    column._add_module(module)

                self._columns.append(column)
        return self._columns

    @property
    def duration(self):
        if self.modules != {}:
            durations = map(lambda module: module.duration, self.modules.values())
            self._duration = sum(durations)
        return self._duration

    @duration.setter
    def duration(self, value):
        if value is None:
            raise ValueError('duration cannot be None')
        self._duration = value
        self._calculate_module_values()

    @property
    def first_multi(self):
        return self._first_multi

    @first_multi.setter
    def first_multi(self, value):
        self._first_multi = value
        if self._modules != {}:
            for key in self._modules.keys():
                module = self._modules[key]
                module.multi = self.index_to_r_c(
                    self.r_c_to_index(module.row_number, module.column_number) + self.r_c_to_index(self.first_multi[0],
                                                                                                   self.first_multi[1]))

    @property
    def index_in_group(self):
        if self.parent_square_group:
            return self.parent_square_group.squares.index(self)
        else:
            return None

    @property
    def modules(self):
        return self._modules

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def parent_square_group(self):
        return self._parent_square_group

    @parent_square_group.setter
    def parent_square_group(self, val):
        if not isinstance(val, SquareGroup):
            raise TypeError('parent_square_group.value must be of type SquareGroup  not{}'.format(type(val)))
        self._parent_square_group = val

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values is None:
            raise ValueError('proportions cannot be None')
        if self.side_size is not None:
            if len(values) != self.side_size:
                raise ValueError('wrong proportions length')
        else:
            self._side_size = len(values)
        self._proportions = values
        self._calculate_module_values()

    @property
    def reading_direction(self):
        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, val):
        if self._reading_direction:
            raise FractalTreeException('reading_direction can only be set during initialisation')
        permitted = ['horizontal', 'vertical']
        if val not in permitted:
            raise ValueError('reading_direction.value {} must be in {}'.format(val, permitted))
        self._reading_direction = val

    @property
    def rows(self):
        if self._rows is None:
            self._rows = []
            for row_number in range(1, self.side_size + 1):
                row = Row(square=self, number=row_number)
                for column_number in range(1, self.side_size + 1):
                    module = self.get_module(row_number, column_number)
                    row._add_module(module)

                self._rows.append(row)
        return self._rows

    @property
    def side_size(self):
        return self._side_size

    @property
    def tree_permutation_order(self):
        return self._tree_permutation_order

    @tree_permutation_order.setter
    def tree_permutation_order(self, values):
        if values is None:
            raise ValueError('tree_permutation_order cannot be None')
        if self.side_size is not None:
            if len(values) != self.side_size:
                raise ValueError('wrong tree_permutation_order length')
        else:
            self._side_size = len(values)
        self._tree_permutation_order = values
        self._calculate_module_values()

    # //public methods

    # get
    def get_all_modules(self):
        return self.modules.values()

    def get_column(self, column_number):
        return self.columns[column_number - 1]

    def get_module(self, *args):
        args = tuple(args)
        return self.modules[args]

    def get_row(self, row_number):
        return self.rows[row_number - 1]

    # other
    def change_module_quarter_duration(self, row_number, column_number, new_quarter_duration):
        factor = Fraction(Fraction(new_quarter_duration),
                          Fraction(self.get_module(row_number, column_number).quarter_duration))

        for key in self.modules:
            self.modules[key].duration = self.modules[key].duration * factor

    def change_module_duration(self, row_number, column_number, new_duration):
        factor = Fraction(
            Fraction(new_duration),
            Fraction(self.get_module(row_number, column_number).duration)
        )

        for key in self.modules:
            self.modules[key].duration = self.modules[key].duration * factor

    def index_to_r_c(self, index):
        row = int(index / self.side_size) % self.side_size + 1
        column = index % self.side_size + 1
        return row, column

    def round_quarter_durations(self):
        for module in self.modules.values():
            module.quarter_duration = round(module.quarter_duration)

    def r_c_to_index(self, row, column):
        index = ((row - 1) * self.side_size) + (column - 1)
        return index

    def write_to_table(self, table=None, show_attributes=None):
        if not show_attributes:
            show_attributes = []

        if not table:
            table = Table(hrules=1)
            column_numbers = [str(number) for number in range(1, self.side_size + 1)]
            table.field_names = ['row', "column:", *column_numbers]
        elif not isinstance(table, Table):
            raise TypeError('table must be of type Table not {}'.format(type(table)))

        for row_number in range(1, self.side_size + 1):
            row = self.get_row(row_number)

            def _round(duration):
                output = round(duration, 1)
                if output != int(output):
                    output = float(output)
                return output

            row_name = row.name
            for attr in show_attributes:
                if attr == 'quarter_duration':
                    tempi = [module.tempo for module in row.modules]
                    if None in tempi:
                        raise Exception('set tempi first')
                    quarter_durations = [round(float(module.quarter_duration), 2) for module in row.modules]
                    table.add_row([row_name, 'quarter_dur', *quarter_durations])
                elif attr == 'duration':
                    durations = [_round(module.duration) for module in row.modules]
                    table.add_row([row_name, 'duration', *durations])
                else:
                    if isinstance(attr, str):
                        module_attributes = [getattr(module, attr) for module in row.modules]
                        table.add_row([row_name, attr, *module_attributes])
                    elif isinstance(attr, tuple) and len(attr) == 2 and isinstance(attr[0], str) and callable(
                            attr[1]):
                        module_attributes = [attr[1](module) for module in row.modules]
                        table.add_row([row_name, attr[0], *module_attributes])
                    else:
                        raise ValueError('attribute {} can not be written to table'.format(attr))
                row_name = ''
        return table

    def write_info(self, text_path, show_attributes=None, title=None):
        if not show_attributes:
            show_attributes = []

        os.system('touch ' + text_path)
        file = open(text_path, 'w')
        if title:
            file.write(title + '\n')
        table = self.write_to_table(show_attributes=show_attributes)

        file.write(table.get_string())
        file.close()

    # //copy
    def __deepcopy__(self, memodict={}):
        copied = self.__class__(duration=self.duration, proportions=self.proportions,
                                tree_permutation_order=self.tree_permutation_order, first_multi=self.first_multi,
                                reading_direction=self.reading_direction, name=self.name)

        for key in self.modules.keys():
            copied.modules[key] = self.modules[key].__deepcopy__()

        for row, copied_row in zip(self.rows, copied.rows):
            if row.name:
                copied_row.set_name(row.name)

        return copied


class SquareGroup(object):
    def __init__(self, *squares, name=None):
        super().__init__()
        self._name = None
        self._squares = []
        for square in squares:
            self.add_square(square)

        self.name = name

    @property
    def squares(self):
        return self._squares

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    def add_square(self, val):
        if not isinstance(val, Square):
            raise TypeError()
        self._squares.append(val)
        val.parent_square_group = self

    def get_all_rows(self):
        return [row for square in self.squares for row in square.rows]

    def write_to_table(self, table=None, show_attributes=None):
        first_square = self.squares[0]
        if not table:
            table = first_square.write_to_table(table=None, show_attributes=show_attributes)
        for square in self.squares[1:]:
            table.extend(square.write_to_table(table=None, show_attributes=show_attributes))
        return table

    def write_info(self, text_path, show_attributes=None, title=None):

        os.system('touch ' + text_path)
        file = open(text_path, 'w')
        if title:
            file.write(title + '\n')
        table = self.write_to_table(show_attributes=show_attributes)

        file.write(table.get_string())
        file.close()

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(*[square.__deepcopy__() for square in self.squares])
        return copied
