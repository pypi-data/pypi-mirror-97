from .base import DEFAULT_SENTINEL, Geocoder
from ..point import Point
from ..location import Location

from typing import Callable, List, Optional, Union

_DEFAULT_NOMINATIM_DOMAIN = "nominatim.openstreetmap.org"

class Nominatim(Geocoder):
    def __init__(
        self,
        *,
        timeout: Union[int, object] = DEFAULT_SENTINEL,
        proxies: Union[int, object] = DEFAULT_SENTINEL,
        domain: str = _DEFAULT_NOMINATIM_DOMAIN,
        scheme: Optional[str] = None,
        user_agent: Optional[str] = None,
        ssl_context: Union[int, object] = DEFAULT_SENTINEL,
    ) -> None: ...
    def geocode(
        self,
        query: str,
        *,
        exactly_one: bool = True,
        timeout: Union[int, object] = DEFAULT_SENTINEL,
        limit: Optional[int] = None,
        addressdetails: bool = False,
        language: Union[bool, str] = False,
        geometry: Optional[str] = None,
        extratags: bool = False,
        country_codes: Optional[Union[str, List[str]]] = None,
        viewbox: Optional[List[Point]] = None,
        bounded: bool = False,
        featuretype: Optional[str] = None,
        namedetails: bool = False,
    ) -> Location: ...
