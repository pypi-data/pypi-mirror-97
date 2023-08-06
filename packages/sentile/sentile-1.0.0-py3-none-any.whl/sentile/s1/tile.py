import re
import datetime
from pathlib import Path
from enum import Enum


Polarization = Enum("Polarization", "VV VH")


class Tile:
    def __init__(self, path):
        self.path = Path(path)

        pattern = (
                r"^S1[AB]_"
                r"(?P<mode>(IW|EW|WV|IM))_"
                r"(?P<product>(SLC|GRD|OCN))"
                r"(?P<resolution>(F|H|M|_))_"
                r"(?P<level>(1|2))"
                r"(S|A)"
                r"(?P<polarization>(SH|SV|DH|DV|HH|HV|VV|VH))_"
                r"(?P<start>\d{8}T(\d{6}))_"
                r"(?P<stop>\d{8}T(\d{6}))_"
                r"(?P<orbit>(\d{6}))_"
                r"(?P<mission>[A-Z0-9]{6})_"
                r"(?P<pid>[A-Z0-9]{4})"
            )

        match = re.match(pattern, self.path.name, re.IGNORECASE)

        if not match:
            raise RuntimeError("unable to parse tile name")

        self.props = match.groupdict()

    @property
    def mode(self):
        return self.props["mode"]

    @property
    def product(self):
        return self.props["product"]

    @property
    def polarization(self):
        return self.props["polarization"]

    @property
    def start(self):
        return datetime.datetime.strptime(self.props["start"], "%Y%m%dT%H%M%S")

    @property
    def stop(self):
        return datetime.datetime.strptime(self.props["stop"], "%Y%m%dT%H%M%S")

