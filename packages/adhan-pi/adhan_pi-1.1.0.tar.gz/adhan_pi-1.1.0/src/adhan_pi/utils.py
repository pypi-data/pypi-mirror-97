import datetime as dt
import functools
from typing import List

import requests
from geopy.geocoders import Nominatim

from .dataclasses import Coordinates, Prayer, PrayerTimes
from .exceptions import LocationNotFoundError, PrayerAPIError

_http_client = requests.Session()
_http_client.mount("https://", requests.adapters.HTTPAdapter(max_retries=4))


@functools.lru_cache(maxsize=None)
def get_location_from_query(query: str) -> Coordinates:
    geolocator = Nominatim(user_agent="adhan-pi")
    location = geolocator.geocode(query)
    if location is None:
        raise LocationNotFoundError(query)
    return Coordinates(
        latitude=location.latitude, longitude=location.longitude
    )


@functools.lru_cache(maxsize=None)
def get_prayer_times_for_month(
    location: Coordinates, year: int, month: int,
) -> List[PrayerTimes]:
    API_URL = "https://api.aladhan.com/v1/calendar"
    response = _http_client.get(
        API_URL,
        params=dict(
            latitude=location.latitude,
            longitude=location.longitude,
            method="02",
            month=month,
            year=year,
        ),
        timeout=(0.5, 0.5),
    )
    if response.status_code != 200:
        raise PrayerAPIError
    data = response.json()
    try:
        return [
            PrayerTimes(
                date=dt.datetime.strptime(
                    d["date"]["gregorian"]["date"], "%d-%m-%Y"
                ).date(),
                fajr=Prayer(name="fajr", time=d["timings"]["Fajr"]),
                dhuhr=Prayer(name="dhuhr", time=d["timings"]["Dhuhr"]),
                asr=Prayer(name="asr", time=d["timings"]["Asr"]),
                maghrib=Prayer(name="maghrib", time=d["timings"]["Maghrib"]),
                isha=Prayer(name="isha", time=d["timings"]["Isha"]),
            )
            for d in data["data"]
        ]
    except (IndexError, KeyError):
        raise PrayerAPIError
