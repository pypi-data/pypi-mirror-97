from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        ft = FractalTree(value=10, reading_direction='vertical')
        ft.add_layer()
        ft.add_layer()
        self.ft = ft.get_children()[1]
        self.deep_copied = self.ft.__deepcopy__()

    def test(self, exp=None, act=None):
        if not exp:
            exp = self.ft

        if not act:
            act = self.deep_copied

        self.assertEqual(exp.value, act.value)
        self.assertEqual(exp.proportions, act.proportions)
        self.assertEqual(exp.value, act.value)
        self.assertEqual(exp.proportions, act.proportions)
        self.assertEqual(exp.tree_permutation_order, act.tree_permutation_order)
        self.assertEqual(exp.fractal_order, act.fractal_order)
        self.assertEqual(exp.reading_direction, act.reading_direction)
        self.assertEqual(exp._name, act._name)

    def test_1(self):
        self.assertIsNone(self.deep_copied.up)
