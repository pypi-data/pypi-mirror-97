import pytest
import responses

from adhan_pi.utils import get_location_from_query


@pytest.fixture(scope="session")
def prayer_api_url():
    return "https://api.aladhan.com/v1/calendar"


@pytest.fixture(autouse=True)
def clear_cache():
    get_location_from_query.cache_clear()


@pytest.fixture()
def prayer_api_200_response(prayer_api_url):
    response = {
        "code": 200,
        "status": "OK",
        "data": [
            {
                "timings": {
                    "Fajr": "04:58 (EST)",
                    "Sunrise": "07:20 (EST)",
                    "Dhuhr": "12:00 (EST)",
                    "Asr": "14:22 (EST)",
                    "Sunset": "16:40 (EST)",
                    "Maghrib": "16:40 (EST)",
                    "Isha": "18:02 (EST)",
                    "Imsak": "05:48 (EST)",
                    "Midnight": "00:00 (EST)",
                },
                "date": {
                    "readable": "01 Jan 2021",
                    "timestamp": "1609509661",
                    "gregorian": {
                        "date": "01-01-2021",
                        "format": "DD-MM-YYYY",
                        "day": "01",
                        "weekday": {"en": "Friday"},
                        "month": {"number": 1, "en": "January"},
                        "year": "2021",
                        "designation": {
                            "abbreviated": "AD",
                            "expanded": "Anno Domini",
                        },
                    },
                },
            },
            {
                "timings": {
                    "Fajr": "04:59 (EST)",
                    "Sunrise": "07:21 (EST)",
                    "Dhuhr": "12:01 (EST)",
                    "Asr": "14:23 (EST)",
                    "Sunset": "16:41 (EST)",
                    "Maghrib": "16:41 (EST)",
                    "Isha": "18:03 (EST)",
                    "Imsak": "05:49 (EST)",
                    "Midnight": "00:00 (EST)",
                },
                "date": {
                    "readable": "02 Jan 2021",
                    "timestamp": "1609509661",
                    "gregorian": {
                        "date": "02-01-2021",
                        "format": "DD-MM-YYYY",
                        "day": "02",
                        "weekday": {"en": "Saturday"},
                        "month": {"number": 1, "en": "January"},
                        "year": "2021",
                        "designation": {
                            "abbreviated": "AD",
                            "expanded": "Anno Domini",
                        },
                    },
                },
            },
        ],
    }
    responses.add(
        responses.GET,
        prayer_api_url,
        json=response,
        status=200,
        match_querystring=False,
    )
    return response


@pytest.fixture()
def prayer_api_200_response_different_version_response(prayer_api_url):
    response = {
        "code": 200,
        "status": "OK",
        "data": [
            {
                "timings": {
                    "The Fajr": "04:58 (EST)",
                    "The Sunrise": "07:20 (EST)",
                    "The Dhuhr": "12:00 (EST)",
                    "The Asr": "14:22 (EST)",
                    "The Sunset": "16:40 (EST)",
                    "The Maghrib": "16:40 (EST)",
                    "The Isha": "18:02 (EST)",
                    "The Imsak": "05:48 (EST)",
                    "The Midnight": "00:00 (EST)",
                },
                "date": {
                    "readable": "01 Jan 2021",
                    "timestamp": "1609509661",
                    "gregorian": {
                        "date": "01-01-2021",
                        "format": "DD-MM-YYYY",
                        "day": "01",
                        "weekday": {"en": "Friday"},
                        "month": {"number": 1, "en": "January"},
                        "year": "2021",
                        "designation": {
                            "abbreviated": "AD",
                            "expanded": "Anno Domini",
                        },
                    },
                },
            },
        ],
    }
    responses.add(
        responses.GET,
        prayer_api_url,
        json=response,
        status=200,
        match_querystring=False,
    )
    return response


@pytest.fixture()
def prayer_api_400_response(prayer_api_url):
    response = {
        "code": 400,
        "status": "BAD",
    }
    responses.add(
        responses.GET,
        prayer_api_url,
        json=response,
        status=400,
        match_querystring=False,
    )
