import argparse
from pathlib import Path

import sentile.scripts.s1
import sentile.scripts.s2


def main():
    parser = argparse.ArgumentParser(prog="sentile")

    subcmd = parser.add_subparsers(dest="command")
    subcmd.required = True

    Formatter = argparse.ArgumentDefaultsHelpFormatter

    s1 = subcmd.add_parser("s1", help="Sentinel-1 related sub-commands", formatter_class=Formatter)
    s1.add_argument("tile", type=Path, help="path to Sentinel-1 .SAFE directory")
    s1.set_defaults(main=sentile.scripts.s1.main)

    s2 = subcmd.add_parser("s2", help="Sentinel-2 related sub-commands", formatter_class=Formatter)
    s2.add_argument("tile", type=Path, help="path to Sentinel-2 .SAFE directory")
    s2.set_defaults(main=sentile.scripts.s2.main)

    args = parser.parse_args()
    args.main(args)


if __name__ == "__main__":
    main()
