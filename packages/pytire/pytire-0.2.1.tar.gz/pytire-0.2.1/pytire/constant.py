"""
Defines constants used elsewhere in the library.

:author: Alex Robinson <girotobial@gmail.com>
:copyright: Copyright (c) Alex Robinson, 2021-2021.
:license: MIT
"""


INCHES_PER_FOOT = 12
FEET_PER_METER = 3.28084

# Regexs
METRIC_RE = r"\d{3}[xX]\d{3}-\d+"  # noqa not an f-string
DIAMETER_RE = r"\d+[(\.\d)]+(?=[xX])"
WIDTH_RE = r"(?<=[xX])\d+[(\.\d)]+(?=-)|\d+[(\.\d)]+(?=-)|(?<=[xX])\d+[(\.\d)]+"
WHEEL_DIAMETER_RE = r"(?<=[-rR])\d+[(\.\d)]+"
