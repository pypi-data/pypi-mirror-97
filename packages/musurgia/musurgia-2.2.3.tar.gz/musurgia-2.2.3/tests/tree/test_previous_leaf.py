from unittest import TestCase

from musurgia.tree import Tree


class Test(TestCase):
    def test_1(self):
        t = Tree()
        self.assertIsNone(t.previous_leaf)

    def test_2(self):
        t = Tree()
        t.add_child(Tree())
        t.add_child(Tree())
        self.assertIsNone(t.get_children()[0].previous_leaf)

    def test_3(self):
        t = Tree()
        t.add_child(Tree())
        t.add_child(Tree())
        self.assertEqual(t.get_children()[1].previous_leaf, t.get_children()[0])

    def test_4(self):
        t = Tree()
        t.add_child(Tree())
        t.add_child(Tree())
        t.get_children()[0].add_child(Tree())
        self.assertEqual(t.get_children()[1].previous_leaf, t.get_children()[0].get_children()[0])
