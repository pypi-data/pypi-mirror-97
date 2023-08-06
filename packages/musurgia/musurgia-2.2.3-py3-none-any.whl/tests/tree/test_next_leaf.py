

from musurgia.tree import Tree
from musurgia.unittest import TestCase


class TestNextLeaf(TestCase):
    def test_of_root(self):
        t = Tree()
        self.assertIsNone(t.next_leaf)

    def test_of_last_leaf(self):
        t = Tree()
        t.add_child(Tree())
        t.add_child(Tree())
        self.assertIsNone(t.get_children()[1].next_leaf)

    def test_3(self):
        t = Tree()
        t.add_child(Tree())
        t.add_child(Tree())
        self.assertEqual(t.get_children()[0].next_leaf, t.get_children()[1])

    def test_4(self):
        t = Tree()
        t.add_child(Tree())
        t.add_child(Tree())
        t.get_children()[1].add_child(Tree())
        self.assertEqual(t.get_children()[0].next_leaf, t.get_children()[1].get_children()[0])
