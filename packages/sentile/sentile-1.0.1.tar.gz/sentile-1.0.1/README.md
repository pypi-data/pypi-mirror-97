<h1 align='center'>sentile</h1>

<p align=center>
  Sentinel tile utilities
  <img src="assets/sentile.png" />
</p>

The sentile module provides convenient Sentinel tile utility functions.


## Usage

Tile name parsing

```python3
>>> from sentile.s2 import Tile
>>> tile = Tile("S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE")
>>> tile.name
'T33UVU'
>>> tile.orbit
'R065'
```

Scene classification mask enum

```python3
>>> from sentile.s2 import SCL
>>> SCL.THIN_CIRRUS
10
```

Path lookup based on band name

```python3
>>> from sentile.s2 import Tile, Band10, Band60
>>> tile = Tile("S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE")
>>> tile.get_band(Band10.B04)
PosixPath('S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE/GRANULE/L2A_T33UVU_A026660_20200730T102528/IMG_DATA/R10m/T33UVU_20200730T102031_B04_10m.jp2')
>>> tile.get_band(Band60.SCL)
PosixPath('S2A_MSIL2A_20200730T102031_N0214_R065_T33UVU_20200730T110107.SAFE/GRANULE/L2A_T33UVU_A026660_20200730T102528/IMG_DATA/R60m/T33UVU_20200730T102031_SCL_60m.jp2')
```


## sentile CLI

Sentile's command line interface, named "sentile", has commands for extracting a Sentinel tile's properties.

```bash
$ sentile --help
```


## Testing

Run

     $ python -m unittest discover

To add a new test 

- file name should match patter test*.py
- the filename must be a valid identifier (not contain - etc)
- the directory inn which the test file resides must contain an __init__.py

## See Also

Inspired by the [mercantile](https://github.com/mapbox/mercantile) module for Web Mercator tiles ❤️


## License

Copyright © 2020 robofarm

Distributed under the MIT License (MIT).
