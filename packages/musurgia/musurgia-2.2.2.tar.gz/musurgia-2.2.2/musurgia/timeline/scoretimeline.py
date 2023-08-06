import os

from musurgia.pdf.text import PageText
from musurgia.pdf.positioned import Positioned
from prettytable import PrettyTable
from quicktions import Fraction

from musurgia.fractaltree.fractalmusicsquare import Module
from musurgia.timeline.timeline import TimeLine

path = os.path.abspath(__file__).split('.')[0]


class ModuleTimeLine(object):
    def __init__(self, start_time, module, instruments, text=None, number=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start_time = None
        self.start_time = start_time
        self._instruments = None
        self.instruments = instruments
        self._module = None
        self.module = module
        self.text = text
        self.number = number

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, val):
        if self._module:
            raise Exception()
        if not isinstance(val, Module):
            raise TypeError('module.value must be of type Module not{}'.format(type(val)))
        self._module = val

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, val):
        if self._start_time:
            raise Exception()
        self._start_time = val

    @property
    def instruments(self):
        return self._instruments

    @instruments.setter
    def instruments(self, val):
        if self._instruments:
            raise Exception()
        self._instruments = val

    def get_end_time(self):
        return int(round(self.start_time + round(self.module.duration)))


class Vertical(Positioned):
    def __init__(self, parent, position, number=None, line_type='dashed', thickness=1, mode='start', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position
        self.parent = parent
        self.mode = mode
        self.number = number
        self._line_type = None
        self.line_type = line_type
        self.thickness = thickness

    @property
    def line_type(self):
        return self._line_type

    @line_type.setter
    def line_type(self, val):
        permitted = ['dashed', 'normal']
        if val not in permitted:
            raise ValueError('line_type.value {} must be in {}'.format(val, permitted))
        self._line_type = val

    def draw(self, pdf):
        if self.mode == 'start':
            line = self.parent.ruler.line_segments[self.position]
            x = line.x1
        elif self.mode == 'end':
            line = self.parent.ruler.line_segments[self.position - 1]
            x = line.x2
        else:
            raise ValueError()

        y = line.y1
        p = line.page
        pdf.x = x
        pdf.y = y
        pdf.page = p

        page_text = PageText(self.number, relative_y=-7, font_size=10, font_weight='bold')
        page_text.draw(pdf)

        for i in range(self.thickness):
            grid = 0.1
            y1 = y + self.relative_y
            y2 = y

            if self.line_type == 'dashed':
                pdf.dashed_line(x1=x + i * grid, x2=x + i * grid, y1=y1, y2=y2 + self.parent.get_height() - 7,
                                space_length=3)
            else:
                pdf.line(x1=x + i * grid, x2=x + i * grid, y1=y1, y2=y2 + self.parent.get_height() - 7)


class ScoreTimeLine(TimeLine):
    def __init__(self, instruments, units_per_line=30, show_interval=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instruments = None
        self.instruments = instruments
        self._module_time_lines = []
        self.units_per_line = units_per_line
        self._verticals = []
        self.show_interval = show_interval

    @property
    def instruments(self):
        return self._instruments

    @instruments.setter
    def instruments(self, val):
        self._instruments = val

    @property
    def module_time_lines(self):
        return self._module_time_lines

    def add_module_time_line(self, module_time_line):
        if not isinstance(module_time_line, ModuleTimeLine):
            raise TypeError()
        for instrument in module_time_line.instruments:
            if instrument not in self.instruments:
                raise ValueError('instrument {} not in {}'.format(instrument, self.instruments))
        # module_time_line.number = len(self._module_time_lines) + 1
        self._module_time_lines.append(module_time_line)

    def get_duration(self):
        return int(max([mtl.get_end_time() for mtl in self.module_time_lines]))

    def add_vertical(self, position, mode='start'):
        v = Vertical(parent=self, position=position, number=len(self._verticals) + 1, mode=mode)
        self._verticals.append(v)
        return v

    def apply_module_time_lines(self):
        self.length = self.get_duration()
        for instrument in self.instruments:
            voice = self.add_voice(name=instrument.abbreviation)
            voice.instrument = instrument
        for module_time_line in self.module_time_lines:
            voices = [v for v in self.voices if v.instrument in module_time_line.instruments]
            for voice in voices:
                module = module_time_line.module
                segment = voice.add_voice_segment(module_time_line.start_time, module_time_line.get_end_time())
                segment.lines[0].add_text_label(module.name, font_size=8, font_weight='bold', relative_x=1)
                try:
                    segment.lines[2].add_text_label('t=' + str(module.tempo), font_size=8)
                except IndexError:
                    segment.lines[0].add_text_label('t=' + str(module.tempo), font_size=4, y_offset=-4.5,
                                                            x_offset=4)
                try:
                    segment.lines[4].add_text_label('d=' + str(round(module.duration)) + '"', font_size=8)
                except IndexError:
                    segment.lines[0].add_text_label('d=' + str(round(module.duration)) + '"', font_size=4,
                                                            x_offset=8, y_offset=-4.5)
                if module_time_line.text:
                    segment.lines[0].add_text_label(module_time_line.text, font_size=4, y_offset=-4.5, x_offset=1)
            self.add_vertical(position=module_time_line.start_time)
            self.add_vertical(position=module_time_line.get_end_time(), mode='end')

    def apply_verticals(self, pdf):
        self._verticals.sort(key=lambda v: v.position)
        number = 1
        position = None
        for vertical in self._verticals:
            if vertical.position != position:
                if vertical == self._verticals[-1]:
                    vertical.thickness = 4
                    vertical.relative_y = -3
                    vertical.line_type = 'normal'

                vertical.number = number
                vertical.draw(pdf)
                position = vertical.position
                number += 1

    def draw(self, pdf):
        self.apply_module_time_lines()
        self.ruler.show_interval = self.show_interval
        printable = (pdf.w - pdf.r_margin - pdf.l_margin)
        self.unit = Fraction(Fraction(printable), Fraction(self.units_per_line))
        super().draw(pdf)
        self.apply_verticals(pdf)

    def draw_square(self, square_path, square):
        os.system('touch ' + square_path)
        file = open(square_path, 'w')
        x = PrettyTable(hrules=1)
        x.set_style(11)
        column_numbers = [str(number) for number in range(1, square.side_size + 1)]
        x.field_names = ["instrument", 'row', *column_numbers]
        for instrument in self.instruments:
            mtls = [mtl for mtl in self.module_time_lines if instrument in mtl.instruments]
            for row_number in range(1, square.side_size + 1):
                row_mtls = [mtl for mtl in mtls if mtl.module.row_number == row_number]
                dict_modules = {}
                for mtl in row_mtls:
                    module = mtl.module
                    try:
                        column_number = module.new_column_number
                    except AttributeError:
                        column_number = module.column_number
                    try:
                        dict_modules[column_number].append(mtl.number)
                    except KeyError:
                        dict_modules[column_number] = [mtl.number]

                row_infos = square.side_size * ['']
                for key in dict_modules.keys():
                    row_infos[key - 1] = str(dict_modules[key]).strip('[]')

                x.add_row([instrument.abbreviation, row_number, *row_infos])

        file.write(x.get_string())
        file.close()
