from sentile.s2 import Tile


def main(args):
    tile = Tile(args.tile)

    print("name", tile.name)
    print("orbit", tile.orbit)
    print("start", tile.start)
