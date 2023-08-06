from sentile.s1 import Tile, Polarization


def main(args):
    tile = Tile(args.tile)

    print("product", tile.product)
    print("mode", tile.mode)
    print("start", tile.start)

    print(tile.get_band(Polarization.VV))
    print(tile.get_band(Polarization.VH))
