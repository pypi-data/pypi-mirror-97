import unittest

from sentile.s2.tile import Tile

class TileTests(unittest.TestCase):
    def test_MGRS_parts(self):
        tile = Tile('S2A_MSIL2A_20210126T102311_N0214_R065_T33UVU_20210126T120030.zip')
        self.assertEqual(tile.get_MGRS_GDZ(), '33U')
        self.assertEqual(tile.get_MGRS_square_ID(), 'VU')
        self.assertEqual(tile.get_MGRS_UTM_zone(), 33)
        self.assertEqual(tile.get_MGRS_latitude_band(), 'U')
        self.assertEqual(tile.get_MGRS_square_column(), 'V')
        self.assertEqual(tile.get_MGRS_square_row(), 'U')
        tile = Tile('S2A_MSIL2A_20210126T102311_N0214_R065_T01UVA_20210126T120030.SAVE')
        self.assertEqual(tile.get_MGRS_GDZ(), '01U')
        self.assertEqual(tile.get_MGRS_square_ID(), 'VA')
        self.assertEqual(tile.get_MGRS_UTM_zone(), 1)
        self.assertEqual(tile.get_MGRS_latitude_band(), 'U')
        self.assertEqual(tile.get_MGRS_square_column(), 'V')
        self.assertEqual(tile.get_MGRS_square_row(), 'A')
