musurgia is a library of different (personal) tools for computer aided music composition.

python 3.8.2

**DEPENDENCIES:**  
see requirements.txt (or frozenrequirements.txt)

**VERSIONS**

### v1.0.1

\__init\__.py added

### v1.1.0

reading_direction (vertical) added to:  
permutation  
LimitedPermutation  
FractalTree

### v1.1.1

reading_direction (vertical) added to:  
Square()
pdf function deleted in Square() and Module()

### v1.2.1 (1.2.0 was corrupt)

FractalTree()
value can only be changed for the root without children FractalMusic()
delete module_tempo, score_tempo add tempo quarter_duration only changes duration children can have different tempi
tempo can only be set once set_non_tempi()
FractalTree() and FractalMusic()
changes needed in merge, reduce, quantize, round Square() and TimeLine()
minor changes needed

### v1.2.2

Square()
write_infos() module duration decimal changed to 1

### v1.2.3

FractalMusic().quarter_duration: bug fix

### v1.2.4

FractalMusic().quarter_duration: bug fix

### v1.3.0

Module().change_duration(): deleted  
Module().change_quarter_duration(): deleted  
Square().change_module_duration(): attribute mode (module_duration or score_duration) deleted  
Row().change_duration(): added  
Row().change_quarter_duration(): added

### v1.4.0

FractalMusic().quarter_duration: bug fix (float instead of fraction)  
FractalMusic().find_best_tempo(): function added  
FractalMusic().duration: bug fix (no type change to fraction)  
FractalTree().round_leaves() : deleted  
FractalMusic().round_leaves() : added

### v1.4.1

FractalTree().\__deepcopy\__(): optimize FractalMusic().\__deepcopy\__(): optimize

### v1.4.2

FractalTree().size: added

### v1.5.0

testcomparefiles: renamed to agtestunit TestCompareFiles(): renames to TestCase  
TestCompareFiles().assertTemplate(file_path=pdf_path): changed to: self.assertCompareFiles(actual_file_path=pdf_path)  
file_path: renamed tp actual_path  
template_path: renamed to expected_path  
Tests: if comparing files is needed use Test(TestCase)  
_template.* renamed to _expected.*

### v1.5.1

setup.py: install_requires: added diff-pdf-visually == 1.4.1

### v1.6.0

Tree().get_leaves(): modified to return \[self\] if no children exist  
FractalTree().generate_children(): added

### v1.6.1

FractalTree()._reduce(): bug fix (/ instead of Fraction)

### v1.7.0

FractalTree().change_value()
FractalMusic().quarter_duration: modified to Fraction  
FractalMusic().change_quarter_duration(): added  
FractalMusic().quantize_children(): added  
FractalMusic().quantize_leaves(): optimised  
FractalMusic().round_leaves(): optimised  
FractalMusic().get_root_score(): deleted   
FractalMusic().get_children_score(): added

### v1.7.1

FractalTree().val: Fraction  
FractalTree().change_value(): bug fix (children duration)  
FractalMusic().get_children_score(): bug fix: gets score of each child with max layers of all children

### v1.8.0

setup.py install_requires: musicscore 1.0.1  
FractalMusic().get_score_template(): subtitle changed to have one decimal place for seconds  
FractalMusic().find_best_tempo(): renamed to: find_best_tempo_in_range()  
FractalMusic().find_best_tempi_in_list(): added  
FractalTree().generate_children(): added argument mode in ['reduce','merge'] and argument merge_index

### v1.8.1:

Module().write_square_infos(): renamed to write_info  
Square().write_infos(): renamed to write_info

### v1.8.2:

FractalTree().multi: bug fix: if multi = (size, x>size) --> LimitedPermutation().multi  
FractalTree()._calculate_children_fractal_values(): deleted: if value == 0: value = 0.01

### v1.8.3:

Square().\__name__: added Square().\__deepcopy__(): added

### v1.8.4:

Square().\__deepcopy__(): bug fixed   
agtable.Table(): added  
SquareGroup(): added  
Square().write_to_table: added Square().write_info: optimised

### v1.8.5:

Square().\__deepcopy__(): bug fixed: row.\__name__ will be copied

### v1.8.6

LimitedPermutation().multi: bug fixed (if m_1 == 0)  
FractalTree().multi: optimised like LimitedPermutation().multi

### v1.8.7: VERSION deleted

### v1.8.8:

Module().parent_square: bug fixed  
RowColumn().square: changed to .parent_square

### v1.8.9:

permutation.invert_matrix(): added  
permutation.permute_matrix_rowwise(): added  
permutation.permute_matrix_columnwise():added  
permutation.permute_matrix(): added

### v1.8.10:

FractalTree().multi: bug fix: _children_fractal_values set to None

### v1.8.11:

midi_generator.RelativeMidi(): copy() (used in add_layer) changed to: self.__class__(microtone=self.microtone)  
FractalTree().multi: bug fix: midi_generator

### v1.8.12:

FractalTree().generate_children: modi added: reduce_backwards (=reduce), reduce_forwards and reduce_sieve'

### v1.9.0:

InterpolationSection: changed to Interpolation  
Interpolation: changed to InterpolationGroup  
Interpolation/InterpolationGroup: get_value changed to \__call__  
Interpolation: key added musurgia.chordfield: New sublibrary added

### v1.9.1:

FractalMusic().add_chord_field(): new method added   
RandomInterpolation: new Interpolation class musurgia.chordfield: further developments (Breathe etc.)  
ArithmeticProgression().correct_s: attribute added and other minor optimisations

### v1.9.2:

issue #2' Random(): bug fix

### v1.10.0

NEW: valuegenerator big changes: ChordField, Breathe  
ChordFieldGroup: omitted

### v1.10.1

Breathe: bug fix conflicted builds for chordfield fixed

### v1.10.2

ArithmeticProgression().\__deepcopy__()  
ChordField().\__deepcopy__()  
ValueGenerator.\__deepcopy__()  
Breathe.quantize added Fractal_Music.get_choral_midis(): repetitions not eliminated  
FractalMusic(): bug fixed issue #6

### v1.10.3

FractalMusic().simple_format: added (as alternative to ChordField)

### v1.10.4

ChordField problems: issues #6 and #7 fixed minor changes in ArithmeticProgression (using more fractions)

### v1.10.5

Breathe: checks fields for wrong parameters  
issue #11 bug fix FractalTree().generate_children(): optimise ValueError for number_of_children > ft.size  
issue #12 bug fix FractalMusic().chord_field midi_generator generates rests (midi_value 0)  
issue #9 FractalMusic().\__deepcopy__ tempo

### v1.10.6

Tree().next_leaf: new property  
Tree().previous_leaf: new property  
Interpolation().grid: new attribute  
FractalMusic().add_gliss(): new method  
musicscore 1.2.15

### v1.10.7

issue #14 bug fix FractalMusic().add_gliss(): position_in_tree changed to quarter_position_in_tree  
FractalMusic()
.add_gliss(): attribute min_quarter_duration added musicscore 1.2.16  
FractalMusic().add_gliss(): if show_heads is False: midi.accidental.force_hide = True

### v1.10.8

ChordField() issue #17: calling property chords will now call list(self) first  
ChordField() raises Error if you try to add_child to a ChordField with a given quarter_duration  
ChordField() add_child: return child ChordFiled()  
issue #15: parent.chords = child_1.chords + child_2.chords etc.

### v1.10.9

ArithmeticProgression:  
issue #20: bug fixed for d ArithmeticProgression  
issue #21: bug fixed for an (and a1)  
FractalMusic().add_info(): new method added issue #10

### v1.10.10

SquareGroup().add_square(): method added  
Square().parent_square_group: property added  
Square().\__name__: changed to name (to avoid overwriting module.\__name__ attribute)  
SquareGroup().name: property added issue #23 fixed:  
Tree().deepcopy_attributes(copied, attribute_names): method added  
FractalMusic().\__deepcopy__(): uses Tree().deepcopy_attributes()

### v1.10.11

FractalMusic().inverse_tree_directions(): method added  
FractalMusic(): changing tree_directions changes directions in midi_generators  
musicscore 1.3.2 installed and needed changes applied to tests  
FractalMusic().add_info(): argument condition added  
gearwheels: new module with new structure (Wheel, Position, etc.)

### v2.0.beta

restructuring pdf. time_line does not work yet.

### v2.0.1beta

pdf left text labels position corrected  
pdf DrawObjectContainer inherits from Labeled

### v2.0.2beta

pdf label position corrected

### v2.1.0beta

pdf SegmentedLines as Containers  
pdf Ruler  
pdf DrawObject.clipped_draw  
pdf.absolute_positions  
pdf.reset_position()  
pdf.draw_page_numbers()

### v2.2.0beta

quantize.get_best_quantized_values(values, units): added  
unit_test.file_path: bug fix to use different file extensions  
classes ProportionalChordField and Wave() added to chord_field

### v2.2.1beta

FractalMusic:
bug fix if FM.midi_generator is None reset_midis() added

### v2.2.2

versions added in setup   
BIG CHANGE:: reduce_children >> algorithm changed, remaining children's grows with factor parent.value/sum of
remaing children
if no children reduce_children raises ValueError  

### v2.2.3
FractalTree.get_layer() >> key can be callable