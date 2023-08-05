"""
:author: Alex Robinson <girotobial@gmail.com>
:copyright: Copyright (c) Alex Robinson, 2021-2021.
:license: MIT
"""

import math
import re
from typing import Optional

from .constant import DIAMETER_RE, METRIC_RE, WHEEL_DIAMETER_RE, WIDTH_RE
from .enums import Unit
from .util import circle_area, convert_length


class Tire:
    """A rubber pneumatic tire.

    Attributes
    ----------
    size : str
        Size code as would be displayed on the sidewall.
        E.g 'H45.5x16.5-21', '30x10.75-16', '615x225-10'
    diameter : float
        Outer diameter in metres
    width : float
        width in metres
    wheel_diameter : float
        inner diameter in metres
    """

    def __init__(self, size: str):
        """A rubber pneumatic tire.

        Parameters
        ----------
        size : str
            Size code as would be displayed on the sidewall.
            E.g 'H45.5x16.5-21', '30x10.75-16', '615x225-10'
        """
        self.size = size
        self.unit = Unit.MILLIMETRE if re.match(METRIC_RE, self.size) else Unit.INCH

    @property
    def diameter(self) -> Optional[float]:
        """Tire diameter in metres"""

        match = re.search(DIAMETER_RE, self.size)

        if match is None:
            return match

        diameter = float(match.group(0))
        return convert_length(diameter, self.unit, Unit.METRE)

    @property
    def width(self) -> Optional[float]:
        """Tire width in metres"""

        match = re.search(WIDTH_RE, self.size)
        if match is None:
            return match

        width = float(match.group(0))
        return convert_length(width, self.unit, Unit.METRE)

    @property
    def wheel_diameter(self) -> Optional[float]:
        """Wheel diameter in metres"""

        match = re.search(WHEEL_DIAMETER_RE, self.size)
        if match is None:
            return match

        wheel_diameter = float(match.group(0))
        return convert_length(wheel_diameter, Unit.INCH, Unit.METRE)

    def volume(self, geometry: str = "cuboid") -> Optional[float]:
        """The exterior volume of the tire.

        Parameters
        ----------
        geometry : str, default 'cuboid'
            The shape assumed during the calculation of the volume.
            allowed values are ['cuboid', 'cylinder', 'square_toroid', 'circular_toroid']

        Returns
        -------
        float
            Volume in m^2
        """

        geometry_map = {
            "cuboid": self.__cuboid_volume,
            "cylinder": self.__cylinder_volume,
            "square_toroid": self.__square_toroid_volume,
            "circular_toroid": self.__circular_toroid_volume,
        }

        if geometry not in geometry_map.keys():
            raise ValueError(f"{geometry} is not a valid geometry")

        function = geometry_map.get(geometry)
        if function is None:
            return None

        return function()

    def __cuboid_volume(self) -> Optional[float]:
        if self.diameter is None or self.width is None:
            return None

        return self.diameter * self.width

    def __cylinder_volume(self) -> Optional[float]:
        if self.diameter is None or self.width is None:
            return None

        radius = self.diameter / 2
        return circle_area(radius) * self.width

    def __square_toroid_volume(self) -> Optional[float]:
        if self.diameter is None or self.width is None or self.wheel_diameter is None:
            return None

        inner_radius = self.wheel_diameter / 2
        wheel_volume = circle_area(inner_radius) * self.width
        cylinder_volume = self.__cylinder_volume()
        assert cylinder_volume is not None
        return cylinder_volume - wheel_volume

    def __circular_toroid_volume(self) -> Optional[float]:
        if self.diameter is None or self.width is None or self.wheel_diameter is None:
            return None

        tyre_radius = self.diameter / 2
        wheel_radius = self.wheel_diameter / 2

        cross_section_radius = 0.5 * (tyre_radius - wheel_radius)
        cross_section_area = circle_area(cross_section_radius)
        toroid_radius = tyre_radius - cross_section_radius

        return 2 * math.pi * cross_section_area * toroid_radius
