import itertools

from quicktions import Fraction

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.basic_functions import flatten
from musurgia.pdf.line import HorizontalLineSegment, HorizontalSegmentedLine
from musurgia.pdf.newdrawobject import DrawObject
from musurgia.pdf.rowcolumn import DrawObjectColumn, DrawObjectRow
from musurgia.permutation import LimitedPermutation, permute
from musurgia.tree import Tree


class FractalTreeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ValueCannotBeChanged(FractalTreeException):
    def __init__(self, *args):
        super().__init__(*args)


class SetValueFirst(FractalTreeException):
    def __init__(self, *args):
        super().__init__('FractalTree().value must be set before add_layer()', *args)


class _Graphic(DrawObject):
    def __init__(self, fractal_tree, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._draw_object_column = None
        self._fractal_tree = fractal_tree
        self._unit = 1
        self._large_mark_line_max_length = 6
        self._large_mark_line_min_length = 3

    def update_draw_object_columns(self):
        unit = self.unit
        max_large_ml = self.large_mark_line_max_length
        min_large_ml = self.large_mark_line_min_length

        def _make_segment():
            segment = HorizontalLineSegment(length=node.value * unit)
            ml_length = (max_large_ml - (
                    node.get_distance() * (max_large_ml - min_large_ml) / self._fractal_tree.number_of_layers)) / 2
            segment.start_mark_line.length = ml_length
            segment.end_mark_line.length = ml_length
            return segment

        for node in self._fractal_tree.traverse():
            node.graphic._draw_object_column = DrawObjectColumn()
            node.graphic._draw_object_column.add_draw_object(_make_segment())

            if node.get_children():
                node.graphic._draw_object_column.add_draw_object(DrawObjectRow(top_margin=3))
            if node.up:
                node.up.graphic._draw_object_column.draw_objects[1].add_draw_object(node.graphic)
            if not node.up or node.up.get_children().index(node) == len(node.up.get_children()) - 1:
                node.graphic._draw_object_column.draw_objects[0].end_mark_line.show = True
                node.graphic._draw_object_column.draw_objects[0].end_mark_line.length *= 2
            if not node.up or node.up.get_children().index(node) == 0:
                node.graphic._draw_object_column.draw_objects[0].start_mark_line.length *= 2

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, val):
        self._unit = val

    @property
    def large_mark_line_max_length(self):
        return self._large_mark_line_max_length

    @large_mark_line_max_length.setter
    def large_mark_line_max_length(self, val):
        self._large_mark_line_max_length = val

    @property
    def large_mark_line_min_length(self):
        return self._large_mark_line_min_length

    @large_mark_line_min_length.setter
    def large_mark_line_min_length(self, val):
        self._large_mark_line_min_length = val

    @property
    def draw_object_column(self):
        if self._draw_object_column is None:
            self.update_draw_object_columns()
        return self._draw_object_column

    def add_labels(self, function, **kwargs):
        for node in self._fractal_tree.traverse():
            node.graphic.get_straight_line().add_label(function(node), **kwargs)

    def get_start_mark_line(self):
        return self.draw_object_column.draw_objects[0].start_mark_line

    def get_end_mark_line(self):
        return self.draw_object_column.draw_objects[0].end_mark_line

    def get_straight_line(self):
        return self.draw_object_column.draw_objects[0].straight_line

    def get_relative_x2(self):
        return self.draw_object_column.get_relative_x2()

    def get_relative_y2(self):
        return self.draw_object_column.get_relative_y2()

    def get_line_segment(self):
        return self.draw_object_column.draw_objects[0]

    def get_children_draw_object_row(self):
        return self.draw_object_column.draw_objects[1]

    def change_segment_attributes(self, **kwargs):
        for node in self._fractal_tree.traverse():
            for key in kwargs:
                setattr(node.graphic.get_line_segment(), key, kwargs[key])

    def draw(self, pdf):
        self.draw_object_column.draw(pdf)


class FractalTree(Tree):
    def __init__(self, value=None, proportions=None, tree_permutation_order=None, multi=None, fertile=True,
                 reading_direction='horizontal', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self._proportions = None
        self._tree_permutation_order = None
        self._multi = None
        self._permutation_order = None
        self._fertile = None
        self._reading_direction = None
        self._fractal_order = None
        self._children_fractal_values = None
        self._name = None
        self._graphic = _Graphic(self)

        self.proportions = proportions
        self.tree_permutation_order = tree_permutation_order
        self.value = value
        self.multi = multi
        self.fertile = fertile
        self.reading_direction = reading_direction

    # // private methods

    def _calculate_children_fractal_orders(self):
        if self.value and self.proportions:
            children_fractal_orders = range(1, self.size + 1)
            permutation_order = self.permutation_order
            if permutation_order:
                children_fractal_orders = permute(children_fractal_orders, permutation_order)
            return children_fractal_orders

    def _calculate_children_fractal_values(self):
        value = self.value
        if value and self.proportions:
            children_fractal_values = [value * prop for prop in self.proportions]
            if self.permutation_order:
                try:
                    children_fractal_values = permute(children_fractal_values, self.permutation_order)
                except ValueError:
                    raise ValueError('proportions and tree_permutation_order should have the same length')
            return children_fractal_values

    def _calculate_position_in_tree(self):
        parent = self.up
        if self.is_root:
            return 0
        else:
            index = parent.get_children().index(self)
            if index == 0:
                return parent.position_in_tree
            else:
                return parent.get_children()[index - 1].position_in_tree + parent.get_children()[index - 1].value

    def _change_children_value(self, factor):
        for child in self.get_children():
            child._value *= factor
            child._change_children_value(factor)

    def _check_merge_nodes(self, nodes):
        return True

    def _child_multi(self, parent, index):
        number_of_children = self.size
        multi_first = sum(parent.multi) % number_of_children
        if multi_first == 0:
            multi_first = number_of_children
        ch_multi = (multi_first, index + 1)
        return ch_multi

    def _get_merge_lengths(self, number_of_children, merge_index):
        if 0 > merge_index > self.size - 1:
            raise ValueError('generate_children.merge_index {} not valid'.format(merge_index))
        if number_of_children > self.size or number_of_children < 0:
            raise ValueError(
                'generate_children.number_of_children {} must be a positive int'.format(number_of_children))
        if number_of_children == 1:
            return [self.size]

        lengths = self.size * [1]
        pointer = merge_index
        sliced_lengths = [lengths[:pointer], lengths[pointer:]]

        if not sliced_lengths[0]:
            sliced_lengths = sliced_lengths[1:]

        while len(sliced_lengths) < number_of_children and len(sliced_lengths[0]) > 1:
            temp = sliced_lengths[0]
            sliced_lengths[0] = temp[:-1]
            sliced_lengths.insert(1, temp[-1:])

        while len(sliced_lengths) < number_of_children and len(sliced_lengths[pointer]) > 1:
            temp = sliced_lengths[pointer]
            sliced_lengths[pointer] = temp[:-1]
            sliced_lengths.insert(pointer + 1, temp[-1:])

        sliced_lengths = [len(x) for x in sliced_lengths]

        return sliced_lengths

    # // properties
    @property
    def children_fractal_values(self):
        if not self._children_fractal_values:
            self._children_fractal_values = self._calculate_children_fractal_values()
        return self._children_fractal_values

    @property
    def children_fractal_orders(self):
        return self._calculate_children_fractal_orders()

    @property
    def fertile(self):
        return self._fertile

    @fertile.setter
    def fertile(self, val):
        if not isinstance(val, bool):
            raise TypeError('fertile.value must be of type bool not{}'.format(type(val)))
        self._fertile = val

    @property
    def fractal_order(self):
        return self._fractal_order

    @property
    def layers(self):
        return [self.get_layer(i) for i in range(self.number_of_layers + 1)]

    @property
    def multi(self):
        return self._multi

    @multi.setter
    def multi(self, vals):
        if vals is None:
            vals = (1, 1)

        elif not isinstance(vals, tuple) or len(vals) != 2:
            raise TypeError('multi has to be a tuple with a length of 2')

        m_1 = vals[0]
        m_2 = vals[1]
        m_1, m_2 = (((m_1 - 1) % self.size) + 1 + ((m_2 - 1) // self.size)) % self.size, (
                (m_2 - 1) % self.size) + 1
        if m_1 == 0:
            m_1 = self.size
        self._multi = (m_1, m_2)

        self._permutation_order = None
        self._children_fractal_values = None

    @property
    def name(self):
        if self._name is None:
            if self.is_root:
                self._name = '0'
            elif self.up.is_root:
                self._name = str(self.up.get_children().index(self) + 1)
            else:
                self._name = self.up.name + '.' + str(self.up.get_children().index(self) + 1)
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def next(self):
        if not self.is_leaf():
            raise Exception('FractalTree().next property can only be used for leaves')
        else:
            try:

                parent = self.up
                while parent is not None:
                    parent_leaves = list(parent.traverse_leaves())
                    index = parent_leaves.index(self)
                    try:
                        return parent_leaves[index + 1]
                    except IndexError:
                        parent = parent.up
                raise IndexError()
            except IndexError:
                return None

    @property
    def number_of_layers(self):
        if self.get_leaves() == [self]:
            return 0
        else:
            return self.get_farthest_leaf().get_distance(self)

    @property
    def graphic(self):
        return self._graphic

    @property
    def permutation_order(self):
        def _calculate_permutation_order():
            if self.tree_permutation_order:
                permutation = LimitedPermutation(input_list=list(range(1, self.size + 1)),
                                                 main_permutation_order=self.tree_permutation_order, multi=self.multi,
                                                 reading_direction=self.reading_direction)

                return permutation.permutation_order
            else:
                raise FractalTreeException('tree_permutation_order must be set')

        if self._permutation_order is None:
            self._permutation_order = _calculate_permutation_order()
        return self._permutation_order

    @property
    def position(self):
        if self.is_root:
            # return self.first_position
            return 0
        else:
            siblings = self.up.get_children()
            index = siblings.index(self)
            previous_siblings = siblings[:index]
            position_in_parent = 0
            for child in previous_siblings: position_in_parent += child.value
            return position_in_parent + self.up.position

    @property
    def position_in_tree(self):
        return self._calculate_position_in_tree()

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values is None:
            values = [1, 2, 3]
        self._proportions = [Fraction(Fraction(value) / Fraction(sum(values))) for value in values]

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
    def size(self):
        return len(self.proportions)

    @property
    def tree_permutation_order(self):
        return self._tree_permutation_order

    @tree_permutation_order.setter
    def tree_permutation_order(self, values):
        if values is None:
            values = [3, 1, 2]
        self._tree_permutation_order = values
        self._permutation_order = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val:
            val = Fraction(val)
        if self._value:
            if self.is_root and not self.get_children():
                self._value = val
            else:
                raise ValueCannotBeChanged(
                    'FractalTree().value can only be changed for the root with no children. Use change_value() for other cases.'
                )
        else:
            self._value = val

        if self._value == 0:
            self.fertile = False

    # //public methods
    # add
    def add_layer(self, *conditions):
        if self.value is None:
            raise SetValueFirst()

        leaves = list(self.traverse_leaves())
        if not leaves:
            leaves = [self]

        if conditions:
            for leaf in leaves:
                for condition in conditions:
                    if not condition(leaf):
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(leaf.size):
                    new_node = leaf.copy()
                    new_node.value = leaf.children_fractal_values[i]
                    new_node.multi = self._child_multi(leaf, i)
                    leaf.add_child(new_node)
                    new_node._fractal_order = leaf.children_fractal_orders[i]

            else:
                pass

    def add_self(self):
        leaves = self.get_leaves()
        for leaf in leaves:
            new_node = self.copy()
            new_node._up = self
            new_node._fractal_order = self.fractal_order
            leaf.add_child(new_node)

    # get
    def get_layer(self, layer, key=None):
        if layer <= self.get_root().number_of_layers:
            branch_distances = []
            for child in self.get_children():
                branch_distances.append(child.get_farthest_leaf().get_distance())
            if layer == 0:
                if key:
                    if isinstance(key, str):
                        return [getattr(self, key)]
                    elif callable(key):
                        return [key(self)]
                    else:
                        raise TypeError(f'key: {key} must be either string or a callable object')
                else:
                    return [self]

            if layer >= 1:
                output = []
                if not branch_distances:
                    output.extend(self.get_layer(layer=layer - 1, key=key))
                for i in range(len(self.get_children())):
                    child = self.get_children()[i]
                    if branch_distances[i] == 1:
                        if key:
                            if isinstance(key, str):
                                output.append(getattr(child, key))
                            elif callable(key):
                                output.append(key(child))
                            else:
                                raise TypeError(f'key: {key} must be either string or a callable object')
                        else:
                            output.append(child)
                    else:
                        if layer == 1:
                            output.extend(child.get_layer(layer - 1, key))
                        else:
                            output.append(child.get_layer(layer - 1, key))

                return output
        else:
            err = 'max layer number=' + str(self.number_of_layers)
            raise ValueError(err)

    def get_next_sibling(self):
        try:
            siblings = self.up.get_children()
            index = siblings.index(self)
            return siblings[index + 1]
        except (IndexError, AttributeError):
            return None

    def get_previous_leaf(self):
        if not self.is_leaf():
            raise Exception('FractalTree().get_previous_leaf  can only be applied to leaves')
        try:
            parent = self.up
            while parent is not None:
                parent_leaves = list(parent.traverse_leaves())
                index = parent_leaves.index(self)
                try:
                    return parent_leaves[index - 1]
                except IndexError:
                    parent = parent.up
            raise IndexError()
        except IndexError:
            return None

    def get_previous_sibling(self):
        try:
            siblings = self.up.get_children()
            index = siblings.index(self)
            if index == 0:
                return None
            return siblings[index - 1]
        except AttributeError:
            return None

    # other

    def change_value(self, new_value):
        if not new_value:
            new_value = Fraction(new_value)
        if not self.value:
            self.value = new_value
        else:
            factor = Fraction(new_value, self.value)
            self._value = new_value
            for node in reversed(self.get_branch()[:-1]):
                node._value = sum([child.value for child in node.get_children()])

            self._change_children_value(factor)

    def generate_children(self, number_of_children, mode='reduce', merge_index=0):

        permitted_modes = ['reduce', 'reduce_backwards', 'reduce_forwards', 'reduce_sieve', 'merge']
        if mode not in permitted_modes:
            raise ValueError('generate_children.mode {} must be in{}'.format(mode, permitted_modes))
        if isinstance(number_of_children, int):
            if number_of_children > self.size:
                raise ValueError(
                    'generate_children.number_of_children {} can not be a greater than size {}'.format(
                        number_of_children, self.size))
            if number_of_children < 0:
                raise ValueError(
                    'generate_children.number_of_children {} must be a positive int'.format(number_of_children))
            elif number_of_children == 0:
                pass
            else:
                self.add_layer()
                if mode in ['reduce', 'reduce_backwards']:
                    self.reduce_children(
                        lambda child: child.fractal_order < self.size - number_of_children + 1)
                elif mode == 'reduce_forwards':
                    self.reduce_children(
                        lambda child: child.fractal_order > number_of_children)
                elif mode == 'reduce_sieve':
                    if number_of_children == 1:
                        self.reduce_children(condition=lambda child: child.fractal_order not in [1])
                    else:
                        ap = ArithmeticProgression(a1=1, an=self.size, n=number_of_children)
                        selection = [int(round(x)) for x in ap]
                        self.reduce_children(condition=lambda child: child.fractal_order not in selection)
                else:
                    merge_lengths = self._get_merge_lengths(number_of_children, merge_index)
                    self.merge_children(*merge_lengths)

        elif isinstance(number_of_children, tuple):
            self.generate_children(len(number_of_children), mode=mode, merge_index=merge_index)

            for index, child in enumerate(self.get_children()):
                if mode == 'reduce':
                    number_of_grand_children = number_of_children[
                        child.fractal_order - child.size + len(number_of_children) - 1]
                else:
                    number_of_grand_children = number_of_children[index]
                child.generate_children(number_of_grand_children, mode=mode, merge_index=merge_index)

        else:
            raise TypeError()

    def generate_layer_segmented_line(self, layer_number, unit, max_mark_line=6, shrink_factor=0.7):
        def get_segmented_line(layer_number):
            if layer_number > self.number_of_layers:
                layer_number = self.number_of_layers
            layer_nodes = flatten(self.get_layer(layer_number))
            lengths = [node.value * unit for node in layer_nodes]
            hsl = HorizontalSegmentedLine(lengths)
            for segment, node in zip(hsl.segments, layer_nodes):
                segment.node = node
                segment.start_mark_line.length = get_ml_length(node)
            return hsl

        def get_ml_length(node):
            if not node.up:
                return max_mark_line
            else:
                if node.up.get_children().index(node) == 0:
                    return get_ml_length(node.up)
                else:
                    return max_mark_line * shrink_factor / node.get_distance()

        def set_last_mark_line_length(row):
            last_mark_line = row.draw_objects[-1].end_mark_line
            last_mark_line.length = max_mark_line
            last_mark_line.show = True

        hls = get_segmented_line(layer_number)
        set_last_mark_line_length(hls)
        return hls

    def merge_children(self, *lengths):
        children = self.get_children()
        if not children:
            raise Exception('there are no children to be merged')
        if sum(lengths) != len(children):
            raise ValueError(
                'sum of lengths {} must be the same as length of children {}'.format(sum(lengths), len(children)))

        def _merge(nodes):
            self._check_merge_nodes(nodes)

            node_values = [node.value for node in nodes]

            nodes[0]._value = sum(node_values)
            for node in nodes[1:]:
                self.remove_child(node)

        iter_children = iter(children)
        chunks = [list(itertools.islice(iter_children, l)) for l in lengths]

        for chunk in chunks:
            _merge(chunk)

    def reduce_children(self, condition):
        if not self.get_children():
            raise ValueError(f'{self} has no children to be reduced')
        # for child in self.get_children():
        #     if condition(child):
        #         child._reduce()
        to_be_detached = [child for child in self.get_children() if condition(child)]
        for child in to_be_detached:
            child.detach()
        reduced_value = sum([child.value for child in self.get_children()])
        factor = self.value / reduced_value
        for child in self.get_children():
            new_value = child.value * factor
            child.change_value(new_value)

        self._children_fractal_values = [child.value for child in self.get_children()]

    # def split(self, *proportions):
    #
    #     for prop in proportions:
    #         self.add_self()
    #         new_value = self.value * prop / sum(proportions)
    #         self.get_children()[-1].change_value(new_value)

    def split(self, *proportions):
        if hasattr(proportions[0], '__iter__'):
            proportions = proportions[0]

        proportions = [Fraction(prop) for prop in proportions]

        for prop in proportions:
            value = self.value * prop / sum(proportions)
            new_node = self.copy()
            new_node.multi = self.multi
            new_node.change_value(value)
            new_node._fractal_order = self.fractal_order
            self.add_child(new_node)

        return self.get_children()

    # // copy

    def copy(self):
        return self.__class__(value=self.value, proportions=self.proportions,
                              tree_permutation_order=self.tree_permutation_order, multi=self.multi,
                              reading_direction=self.reading_direction, fertile=self.fertile)

    # def copy_without_children(self):

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(value=self.value, proportions=self.proportions,
                                tree_permutation_order=self.tree_permutation_order, multi=self.multi,
                                reading_direction=self.reading_direction, fertile=self.fertile)
        copied._fractal_order = self.fractal_order
        copied._name = self._name
        for child in self.get_children():
            copied.add_child(child.__deepcopy__())
        return copied
