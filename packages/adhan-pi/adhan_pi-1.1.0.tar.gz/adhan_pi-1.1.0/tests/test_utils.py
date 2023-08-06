import datetime as dt

import pytest
import responses
from automock import get_mock

import adhan_pi
import adhan_pi.utils as utils
from adhan_pi.dataclasses import PrayerTimes


@pytest.fixture(autouse=True)
def prayer_times_cache_restart():
    utils.get_prayer_times_for_month.cache_clear()


def test_get_location():
    location = utils.get_location_from_query("New York, NY")
    assert (0, 1) == tuple(location)
    assert location.latitude == 0
    assert location.longitude == 1
    mock = get_mock("adhan_pi.utils.Nominatim")
    mock.assert_called_with(user_agent="adhan-pi")
    mock().geocode.assert_called_with("New York, NY")


@responses.activate
def test_get_prayer_times(prayer_api_200_response):
    location = utils.get_location_from_query("New York, NY")
    day = dt.date(year=2021, month=1, day=1)
    prayer_times = adhan_pi.get_prayer_times(location, day)
    assert isinstance(prayer_times, PrayerTimes)
    assert prayer_times.fajr.name == "fajr"
    assert prayer_times.fajr.time == dt.time(hour=4, minute=58)
    assert prayer_times.date == day
    assert [
        ("fajr", dt.time(hour=4, minute=58)),
        ("dhuhr", dt.time(hour=12)),
        ("asr", dt.time(hour=14, minute=22)),
        ("maghrib", dt.time(hour=16, minute=40)),
        ("isha", dt.time(hour=18, minute=2)),
    ] == [(p.name, p.time) for p in prayer_times]


@responses.activate
def test_get_prayer_times_200_bad_response(
    prayer_api_200_response_different_version_response,
):
    location = utils.get_location_from_query("New York, NY")
    day = dt.date(year=2021, month=1, day=1)
    with pytest.raises(utils.PrayerAPIError):
        adhan_pi.get_prayer_times(location, day)


@responses.activate
def test_get_prayer_times_400(prayer_api_400_response):
    location = utils.get_location_from_query("New York, NY")
    day = dt.date(year=2021, month=1, day=1)
    with pytest.raises(utils.PrayerAPIError):
        adhan_pi.get_prayer_times(location, day)


@responses.activate
def test_get_prayer_times_correct_day(prayer_api_200_response):
    location = utils.get_location_from_query("New York, NY")
    # day marked as the second of january
    day = dt.date(year=2021, month=1, day=2)
    prayer_times = adhan_pi.get_prayer_times(location, day)
    assert isinstance(prayer_times, PrayerTimes)
    assert prayer_times.fajr.name == "fajr"
    assert prayer_times.fajr.time == dt.time(hour=4, minute=59)
