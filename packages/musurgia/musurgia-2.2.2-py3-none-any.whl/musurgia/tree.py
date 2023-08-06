from musurgia.basic_functions import flatten


class TreeError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


class NotLeafError(TreeError):
    def __init__(self, *args):
        msg = '{} is not a leaf.'.format(self)
        super().__init__(msg, *args)


class Tree(object):
    """
    A simple Tree class
    """

    def __init__(self, label=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = []
        self._up = None
        self._leaves = []
        self._label = None
        self.label = label

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, val):
        self._label = val

    @property
    def up(self):
        return self._up

    @property
    def is_root(self):
        if self._up is None:
            return True
        else:
            return False

    @property
    def index(self):
        if self.is_root:
            _index = [0]
        elif self.get_distance() == 1:
            _index = [self.up.get_children().index(self) + 1]
        else:
            _index = self.up.index
            _index.append(self.up.get_children().index(self) + 1)
        return _index

    def get_root(self):
        if self.is_root:
            return self

        root = self.up
        while not root.is_root:
            root = root.get_root()
        return root

    def get_children(self):
        return self._children

    def add_child(self, child):
        if not isinstance(child, Tree):
            raise TypeError('fractal_tree must be of type Tree and not {}'.format(type(child)))
        self._children.append(child)
        child._up = self
        return child

    def remove_child(self, child):
        try:
            self._children.remove(child)
        except ValueError:
            pass

    def remove(self):
        if self.is_root:
            raise Exception()

        parent = self.up
        insert_index = self.up._children.index(self)
        self.up._children.remove(self)

        for child in self.get_children().__reversed__():
            parent.add_child(child)
            new_child = parent._children.pop(-1)
            parent._children.insert(insert_index, new_child)

    def clear_children(self):
        self._children.clear()

    def get_branch(self):
        output = [self]
        node = self
        while node.up is not None:
            output.append(node.up)
            node = node.up
        output.reverse()
        return output

    def get_common_ancestor(self, *other_nodes):
        for other_node in other_nodes:
            if self.get_root() != other_node.get_root():
                raise Exception('{} has not the same root'.format(other_node))

        me_branch = self.get_branch()[:]
        other_branches = [other_node.get_branch()[:] for other_node in other_nodes]

        for node in reversed(me_branch):
            node_in_all_branches = True
            for branch in other_branches:
                if node not in branch:
                    node_in_all_branches = False
                    break
            if node_in_all_branches:
                return node

        # intersection = list(set(a) - (set(a) - set(b)))
        # print(a)
        # print(b)
        # print(intersection)

    @property
    def is_leaf(self):
        if len(self.get_children()) == 0:
            return True
        else:
            return False

    def get_leaves(self, key=None):
        output = []
        for child in self.get_children():
            if not child.is_leaf:
                output.append(child.get_leaves(key=key))
            else:
                if key is not None:
                    output.append(key(child))
                else:
                    output.append(child)
        if not output:
            if key is not None:
                return [key(self)]
            else:
                return [self]
        return output

    def traverse(self):
        yield self
        for child in self.get_children():
            for grand_child in child.traverse():
                yield grand_child

    def dump(self):
        output = []
        for node in self.traverse():
            output.append(node)
        return output

    def get_distance(self, reference=None):
        if reference is None:
            reference = self.get_root()

        if self.is_root:
            return 0
        parent = self.up
        count = 1
        while parent is not reference:
            parent = parent.up
            count += 1
            if parent.is_root and parent is not reference:
                return None
        return count

    def get_farthest_leaf(self):
        leaves = list(self.traverse_leaves())
        if not leaves:
            leaves = [self]
        return max(leaves, key=lambda leaf: leaf.get_distance())

    def get_layer(self, layer, key=None):
        if layer == 0:
            output = [self]
        elif layer == 1:
            output = self.get_children()
        else:
            output = []
            for child in self.get_layer(layer - 1):
                if child.is_leaf:
                    output.append(child)
                else:
                    output.extend(child.get_children())
        if key is None:
            return output
        else:
            return [key(child) for child in output]

    def get_siblings(self):
        if self.is_root:
            return []
        output = []
        for child in self.up.get_children():
            if child != self:
                output.append(child)
        return output

    def detach(self):
        self.up._children.remove(self)
        self._up = None

    def goto(self, index):

        if index == [0]:
            return self

        if len(index) == 1:
            return self.get_children()[index[0] - 1]

        return self.goto(index[:1]).goto(index[1:])

    def select_index(self, index):
        return self.goto(index)

    def replace_node(self, new_node):
        if self.is_root:
            raise Exception('root cannot be replaced')
        else:
            index = self.up.get_children().index(self)
            new_node._up = self._up
            self.up.get_children()[index] = new_node
            self._up = None

    def traverse_leaves(self):
        # for node in self.traverse():
        #     if node.is_leaf:
        #         yield node
        for leaf in flatten(self.get_leaves()):
            yield leaf
        # for leaf in self.get_flatten_leaves():
        #     yield leaf

    def find_leaf(self, condition):
        for leaf in self.traverse_leaves():
            if condition(leaf) is True:
                return leaf
        return False

    @property
    def __next__(self):
        if not self.is_leaf:
            raise Exception('__next__ is only possible for leaves')

        leave_iterator = self.get_root().traverse_leaves()

        def forward_leaves(leave_iterator):
            leaf = leave_iterator.__next__()
            if leaf != self:
                forward_leaves(leave_iterator)

        forward_leaves(leave_iterator)
        return leave_iterator.__next__()

    @property
    def previous_sibling(self):
        try:
            siblings = self.up.get_children()
            index = siblings.index(self)
            if index != 0:
                return siblings[index - 1]
            else:
                return None
        except (IndexError, AttributeError):
            return None

    @property
    def next_sibling(self):
        try:
            siblings = self.up.get_children()
            index = siblings.index(self)
            if index != len(siblings) - 1:
                return siblings[index + 1]
            else:
                return None
        except (IndexError, AttributeError):
            return None

    @property
    def previous_leaf(self):
        if not self.is_leaf:
            raise NotLeafError()
        try:
            leaves = flatten(self.get_root().get_leaves())
            index = leaves.index(self)
            if index != 0:
                return leaves[index - 1]
            else:
                return None
        except (IndexError, AttributeError):
            return None

    @property
    def next_leaf(self):
        if not self.is_leaf:
            raise NotLeafError()
        try:
            leaves = flatten(self.get_root().get_leaves())
            index = leaves.index(self)
            if index != len(leaves) - 1:
                return leaves[index + 1]
            else:
                return None
        except (IndexError, AttributeError):
            return None

    def deepcopy_attributes(self, copied, copy_attribute_names):
        def deepcopy_attribute(attribute):
            try:
                copied_attribute = attribute.__deepcopy__()
            except AttributeError:
                if not isinstance(attribute, str) and hasattr(attribute, '__iter__'):
                    if isinstance(attribute, list):
                        copied_attribute = []
                        for x in attribute:
                            copied_attribute.append(deepcopy_attribute(x))
                    else:
                        raise NotImplementedError(type(attribute))
                else:
                    copied_attribute = attribute
            return copied_attribute

        for attribute_name in copy_attribute_names:
            attribute = getattr(self, attribute_name)
            copied_attribute = deepcopy_attribute(attribute)
            setattr(copied, attribute_name, copied_attribute)


class TreeNode(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
