import unittest

from sentile.s1.filename import FileName

class TileTests(unittest.TestCase):
    def test_parsed_parameters(self):
        tile = FileName('s1b-iw-grd-vv-20210301t164333-20210301t164358-025824-031465-001.tiff')
        self.assertEqual(tile.start.year, 2021)
        self.assertEqual(tile.start.month, 3)
        self.assertEqual(tile.start.day, 1)
        self.assertEqual(tile.polarization, 'vv')
        self.assertEqual(tile.product, 'grd')
        self.assertEqual(tile.mode, 'iw')


