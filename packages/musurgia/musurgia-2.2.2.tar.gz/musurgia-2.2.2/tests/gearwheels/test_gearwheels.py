import os

from musicscore.basic_functions import xToD
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.unittest import TestCase
from musurgia.gearwheels import GearWheels, Wheel

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def test_1(self):
        wh = Wheel(size=4, start=60)
        expected = [60, 64, 68, 72, 76]
        actual = [position.value for position in wh.get_positions(number_of_cycles=5)]
        self.assertEqual(expected, actual)

    def test_2(self):
        gw = GearWheels(wheels=[Wheel(3), Wheel(4), Wheel(5)])
        expected = [3, 1, 1, 1, 2, 1, 1, 2, 3, 1, 2, 2, 1, 3, 1, 2, 1, 2, 2, 1, 2, 1, 3, 1, 2, 2, 1, 3, 2, 1, 1, 2, 1,
                    1, 1, 3]
        actual = gw.get_rhythm()
        self.assertEqual(actual, expected)

    def test_3(self):
        xml_path = path + '_test_3.xml'
        score = TreeScoreTimewise()
        gw = GearWheels(wheels=[Wheel(3), Wheel(4), Wheel(5)])
        sfs = []
        for index, wheel in enumerate(gw.wheels):
            quarter_durations = xToD(wheel.get_position_values())
            midis = len(quarter_durations) * [60 + index]
            sf = SimpleFormat(quarter_durations=quarter_durations, midis=midis)
            sfs.append(sf)
            sf.to_stream_voice().add_to_score(score, part_number=index + 1)
        sf = SimpleFormat.sum(*sfs)
        sf.to_stream_voice().add_to_score(score, part_number=len(gw.wheels) + 1)
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
