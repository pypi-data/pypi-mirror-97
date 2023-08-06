import os

from musicscore.musictree.treeinstruments import Violin, Viola, Cello, Percussion, Accordion

from musurgia.agpdf.pdf import Pdf, PageText
from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusicsquare import Square
from musurgia.timeline.scoretimeline import ScoreTimeLine, ModuleTimeLine

path = str(os.path.abspath(__file__).split('.')[0])

square = Square(duration=100, tree_permutation_order=[3, 1, 2], proportions=[1, 2, 3])

square.change_module_duration(1, 1, 4)
square.get_row(1).set_tempo(50)
square.get_row(2).set_tempo(80)
square.get_row(3).set_tempo(100)

for module in square.modules.values():
    module.quarter_duration = round(module.quarter_duration)

# square.get_row(1).set_score_tempo(50)
# square.get_row(1).set_module_tempo(72)
# square.get_row(2).set_score_tempo(80)
# square.get_row(2).set_module_tempo(72)
# square.get_row(3).set_score_tempo(100)
# square.get_row(3).set_module_tempo(72)


VIOLIN = Violin()
VIOLA = Viola()
CELLO = Cello()
PERCUSSION = Percussion()
ACCORDION = Accordion()


class Test(AGTestCase):

    def test_1(self):
        pdf = Pdf(orientation='landscape', t_margin=25, l_margin=20)
        title = PageText(text='t e s t', v_position='center', h_position='top', relative_y=-14, font_size=18,
                         font_weight='bold')
        composer = PageText(text='A. G. 2019', v_position='right', h_position='top', relative_y=-14)

        pdf_path = path + '_test_1.pdf'
        stl = ScoreTimeLine(instruments=[VIOLIN, VIOLA, CELLO, PERCUSSION, ACCORDION], units_per_line=60)
        stl.add_module_time_line(
            ModuleTimeLine(start_time=0, module=square.get_module(1, 2), instruments=[VIOLIN, VIOLA, CELLO]))
        stl.add_module_time_line(
            ModuleTimeLine(start_time=16, module=square.get_module(2, 3), instruments=[PERCUSSION]))
        stl.add_module_time_line(
            ModuleTimeLine(start_time=20, module=square.get_module(3, 1), instruments=[ACCORDION]))
        stl.add_module_time_line(
            ModuleTimeLine(start_time=60, module=square.get_module(3, 3),
                           instruments=[VIOLIN, VIOLA, CELLO, PERCUSSION, ACCORDION]))

        stl.add_module_time_line(
            ModuleTimeLine(start_time=120, module=square.get_module(1, 3),
                           instruments=[VIOLIN, VIOLA, CELLO]))

        stl.add_module_time_line(
            ModuleTimeLine(start_time=135, module=square.get_module(3, 3),
                           instruments=[ACCORDION, PERCUSSION]))

        stl.add_module_time_line(
            ModuleTimeLine(start_time=160, module=square.get_module(3, 3),
                           instruments=[ACCORDION, PERCUSSION]))

        stl.draw(pdf)
        for page in pdf.pages:
            pdf.page = page
            title.draw(pdf)
            composer.draw(pdf)
        pdf.write(pdf_path)
        self.assertCompareFiles(actual_file_path=pdf_path)
