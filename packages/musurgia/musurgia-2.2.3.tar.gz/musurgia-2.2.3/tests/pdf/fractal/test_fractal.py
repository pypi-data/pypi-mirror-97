from pathlib import Path

from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.pdf.line import HorizontalLineSegment
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.rowcolumn import DrawObjectColumn, DrawObjectRow
from musurgia.unittest import TestCase

path = Path(__file__)


def fill_tree_with_columns(fractal_tree, factor=1):
    max_large_ml = 6
    min_large_ml = 3
    for node in fractal_tree.traverse():
        node.manual_graphic = DrawObjectColumn()
        segment = node.manual_graphic.add_draw_object(HorizontalLineSegment(length=node.value * factor))
        ml_length = (max_large_ml - (
                node.get_distance() * (max_large_ml - min_large_ml) / fractal_tree.number_of_layers)) / 2
        segment.start_mark_line.length = ml_length
        segment.end_mark_line.length = ml_length
        if node.get_children():
            node.children_manual_graphics_row = node.manual_graphic.add_draw_object(DrawObjectRow(top_margin=3))
        if node.up:
            node.up.children_manual_graphics_row.add_draw_object(node.manual_graphic)
        if not node.up or node.up.get_children().index(node) == len(node.up.get_children()) - 1:
            node.manual_graphic.draw_objects[0].end_mark_line.show = True
            node.manual_graphic.draw_objects[0].end_mark_line.length *= 2
        if not node.up or node.up.get_children().index(node) == 0:
            node.manual_graphic.draw_objects[0].start_mark_line.length *= 2


class TestFractal(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf(orientation='l')
        self.ft = FractalTree(value=20)
        self.ft.add_layer()
        self.factor = 2
        fill_tree_with_columns(self.ft, self.factor)

    def test_draw(self):
        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            self.ft.manual_graphic.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_with_text(self):
        leaf = self.ft.get_leaves()[1]
        leaf_start_mark_line = leaf.manual_graphic.draw_objects[0].start_mark_line
        leaf_start_mark_line.add_label('bla')
        leaf_start_mark_line.add_label('blue')
        row = self.ft.manual_graphic.draw_objects[1]
        row.top_margin = max(
            [do.draw_objects[0].start_mark_line.get_above_text_labels_height() for do in row.draw_objects])
        print(row.top_margin)
        with self.file_path(path, 'draw_with_text', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            self.ft.manual_graphic.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_filled_tree(self):
        ft = FractalTree(value=20)
        ft.add_layer()
        ft.get_children()[1].add_layer()
        fill_tree_with_columns(ft, 2)

        with self.file_path(path, 'draw_filled_tree', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            ft.manual_graphic.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_unpruned_tree_with_some_text(self):
        ft = FractalTree(value=20)
        ft.add_layer()
        ft.get_children()[0].add_layer()
        ft.get_children()[-1].add_layer()
        fill_tree_with_columns(ft, 2)
        selected_node = ft.select_index([1])
        child_1 = selected_node.get_children()[1]
        child_2 = selected_node.get_children()[2]
        lb1 = child_1.manual_graphic.draw_objects[0].start_mark_line.add_label(1, font_size=8, bottom_margin=1)
        lb2 = child_1.manual_graphic.draw_objects[0].start_mark_line.add_label(2, font_size=8, bottom_margin=1)
        lb3 = child_2.manual_graphic.draw_objects[0].start_mark_line.add_label(3, font_size=8, bottom_margin=1)

        for child in ft.get_children():
            try:
                child.manual_graphic.draw_objects[1].top_margin += 2
            except IndexError:
                pass

        with self.file_path(path, 'draw_unpruned_tree_with_some_text', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')
            self.pdf.translate(10, 10)
            ft.manual_graphic.draw(self.pdf)
            self.pdf.write(pdf_path)

    