from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.tree import Tree
from musurgia.unittest import TestCase


class TestFtSplit(TestCase):
    def test_two(self):
        t = FractalTree(value=10)
        t.add_layer()
        child = t.get_children()[0]
        s = child.split(1, 1)
        actual = [x.value for x in s]
        expected = [child.value/2, child.value/2]
        self.assertEqual(expected, actual)

    def test_three(self):
        t = FractalTree(value=10)
        t.add_layer()
        child = t.get_children()[0]
        s = child.split(1, 1, 1)
        actual = [x.value for x in s]
        expected = [child.value/3, child.value/3, child.value/3]
        self.assertEqual(expected, actual)

    def test_child_is_not_leaf(self):
        t = FractalTree(value=10)
        t.add_layer()
        child = t.get_children()[0]
        child.split(1, 1, 1)
        self.assertFalse(child.is_leaf)

    def test_split_is_leaf(self):
        t = FractalTree(value=10)
        t.add_layer()
        child = t.get_children()[0]
        s = child.split(1, 1, 1)
        actual = [x.is_leaf for x in s]
        expected = [True, True, True]
        self.assertEqual(expected, actual)
