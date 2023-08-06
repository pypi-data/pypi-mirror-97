import collections.abc

from geopy.point import Point
from typing import Dict, Union

class Location:
    def __init__(
        self,
        address: str,
        point: Union[Point, str, collections.abc.Sequence[float]],
        raw: Dict[str, Union[str, float]],
    ) -> None: ...
    @property
    def latitude(self) -> float: ...
    @property
    def longitude(self) -> float: ...
