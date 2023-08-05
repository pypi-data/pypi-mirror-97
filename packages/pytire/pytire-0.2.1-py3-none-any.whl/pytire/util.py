"""
Utility functions

:author: Alex Robinson <girotobial@gmail.com>
:copyright: Copyright (c) Alex Robinson, 2021-2021.
:license: MIT
"""

import math

from .constant import FEET_PER_METER, INCHES_PER_FOOT
from .enums import Unit


def convert_length(length: float, from_unit: Unit, to_unit: Unit) -> float:
    """Changes length measurements between units

    Parameters
    ----------
    length : float
        measurement to convert
    from_unit : Unit
        [description]
    to_unit : Unit
        [description]

    Returns
    -------
    float
        converted length in to_unit
    """

    if from_unit == to_unit:
        return length

    factors = {
        (Unit.INCH, Unit.METRE): 1.0 / (INCHES_PER_FOOT * FEET_PER_METER),
        (Unit.MILLIMETRE, Unit.METRE): 1 / 1000,
        (Unit.METRE, Unit.MILLIMETRE): 1000,
        (Unit.METRE, Unit.INCH): INCHES_PER_FOOT * FEET_PER_METER,
    }

    factor = factors.get((from_unit, to_unit))
    if factor is None:
        raise ValueError(
            f"Unable to provide conversion between {from_unit.name} and {to_unit.name}"
        )

    return length * factor


def circle_area(radius: float) -> float:
    """calculates the area of a circle

    Parameters
    ----------
    radius : float
        the radius of the circle

    Returns
    -------
    float
        the area of the circle
    """
    return radius ** 2 * math.pi
