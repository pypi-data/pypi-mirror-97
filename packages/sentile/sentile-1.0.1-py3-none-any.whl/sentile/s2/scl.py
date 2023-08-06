import enum

# Sentinel-2 imagery comes with pixel-wise scene slassification e.g. clouds, water, etc.
#
# See:
#   https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm


class SCL(enum.IntEnum):
    NO_DATA = 0
    SATURATED_OR_DEFECTIVE = 1
    DARK_AREA = 2
    CLOUD_SHADOWS = 3
    VEGETATION = 4
    NOT_VEGETATED = 5
    WATER = 6
    UNCLASSIFIED = 7
    CLOUD_MEDIUM_PROBABILITY = 8
    CLOUD_HIGH_PROBABILITY = 9
    THIN_CIRRUS = 10
    SNOW = 11
