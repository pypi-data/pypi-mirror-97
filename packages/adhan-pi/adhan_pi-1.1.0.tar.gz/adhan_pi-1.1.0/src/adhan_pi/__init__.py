import datetime as dt

from .dataclasses import Coordinates, PrayerTimes
from .exceptions import PrayerAPIError
from .utils import get_prayer_times_for_month


def get_prayer_times(location: Coordinates, date: dt.date) -> PrayerTimes:
    data = get_prayer_times_for_month(location, date.year, date.month)
    try:
        return data[date.day - 1]
    except (IndexError, KeyError):
        raise PrayerAPIError
