import unittest

from sentile.s1.tile import Tile

class TileTests(unittest.TestCase):
    def test_parsed_parameters(self):
        tile = Tile('S1A_IW_GRDH_1SDV_20210216T165218_20210216T165243_036618_044D49_302A.zip')
        self.assertEqual(tile.start.year, 2021)
        self.assertEqual(tile.start.month, 2)
        self.assertEqual(tile.start.day, 16)
        self.assertEqual(tile.polarization, 'DV')
        self.assertEqual(tile.product, 'GRD')
        self.assertEqual(tile.mode, 'IW')


