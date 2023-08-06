# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentile', 'sentile.s1', 'sentile.s2', 'sentile.scripts', 'sentile.tests']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sentile = sentile.scripts.__main__:main']}

setup_kwargs = {
    'name': 'sentile',
    'version': '1.0.1',
    'description': 'Sentinel tile utilities',
    'long_description': '<h1 align=\'center\'>sentile</h1>\n\n<p align=center>\n  Sentinel tile utilities\n  <img src="assets/sentile.png" />\n</p>\n\nThe sentile module provides convenient Sentinel tile utility functions.\n\n\n## Usage\n\nTile name parsing\n\n```python3\n>>> from sentile.s2 import Tile\n>>> tile = Tile("S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE")\n>>> tile.name\n\'T33UVU\'\n>>> tile.orbit\n\'R065\'\n```\n\nScene classification mask enum\n\n```python3\n>>> from sentile.s2 import SCL\n>>> SCL.THIN_CIRRUS\n10\n```\n\nPath lookup based on band name\n\n```python3\n>>> from sentile.s2 import Tile, Band10, Band60\n>>> tile = Tile("S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE")\n>>> tile.get_band(Band10.B04)\nPosixPath(\'S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE/GRANULE/L2A_T33UVU_A026660_20200730T102528/IMG_DATA/R10m/T33UVU_20200730T102031_B04_10m.jp2\')\n>>> tile.get_band(Band60.SCL)\nPosixPath(\'S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE/GRANULE/L2A_T33UVU_A026660_20200730T102528/IMG_DATA/R60m/T33UVU_20200730T102031_SCL_60m.jp2\')\n```\n\n\n## sentile CLI\n\nSentile\'s command line interface, named "sentile", has commands for extracting a Sentinel tile\'s properties.\n\n```bash\n$ sentile --help\n```\n\n\n## Testing\n\nRun\n\n     $ python -m unittest discover\n\nTo add a new test \n\n- file name should match patter test*.py\n- the filename must be a valid identifier (not contain - etc)\n- the directory inn which the test file resides must contain an __init__.py\n\n## See Also\n\nInspired by the [mercantile](https://github.com/mapbox/mercantile) module for Web Mercator tiles ❤️\n\n\n## License\n\nCopyright © 2020 robofarm\n\nDistributed under the MIT License (MIT).\n',
    'author': 'Robofarm',
    'author_email': 'hello@robofarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
