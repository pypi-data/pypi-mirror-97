import shutil
from unittest.mock import patch

import pytest
import responses
from automock import get_mock, swap_mock

import adhan_pi.cli as cli


@pytest.fixture
def cache_folder():
    cache_folder = "/tmp/testingadhan"
    d = patch.dict("os.environ", {"CACHE_FOLDER": cache_folder})
    d.start()
    yield
    d.stop()
    shutil.rmtree(cache_folder)


def test_alert_adhan_fajr():
    cli.AdhanAlertFFMPEG("fajr").alert()
    audio_mock = get_mock("adhan_pi.cli.AudioSegment")
    play_mock = get_mock("adhan_pi.cli.play")
    audio_mock.from_mp3.assert_called_with("fajr.mp3")
    play_mock.assert_called_with(audio_mock.from_mp3())


def test_alert_adhan():
    cli.AdhanAlertFFMPEG("dhuhr").alert()
    audio_mock = get_mock("adhan_pi.cli.AudioSegment")
    play_mock = get_mock("adhan_pi.cli.play")
    audio_mock.from_mp3.assert_called_with("adhan.mp3")
    play_mock.assert_called_with(audio_mock.from_mp3())


@responses.activate
@pytest.mark.freeze_time("2021-01-01")
def test_schedule_no_previous_jobs(prayer_api_200_response, cache_folder):
    cli.schedule_prayer_cron("salah", "Los Angeles")
    pwd_mock = get_mock("adhan_pi.cli.pwd")
    pwd_mock.getpwnam.assert_called_with("salah")
    geopy_mock = get_mock("adhan_pi.utils.Nominatim")
    geopy_mock.assert_called_with(user_agent="adhan-pi")
    geopy_mock().geocode.assert_called_with("Los Angeles")
    cron_mock = get_mock("adhan_pi.cli.CronTab")
    cron_mock.assert_called_with(user="salah")
    cron_mock().__enter__().find_comment.assert_called_with("adhan_pi")
    cron_mock().__enter__().remove.assert_not_called()
    for p in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
        cron_mock().__enter__().new.assert_any_call(
            command="XDG_RUNTIME_DIR=/run/user/{user_id} /opt/adhan-pi/env/bin/alert_adhan --prayer {prayer} > /dev/null 2>&1".format(
                user_id=1000, prayer=p,
            ),
            comment="adhan_pi",
        )


@responses.activate
@pytest.mark.freeze_time("2021-01-01")
def test_schedule_previous_jobs(prayer_api_200_response, cache_folder):
    with swap_mock("adhan_pi.cli.CronTab", previous_jobs=True):
        cli.schedule_prayer_cron("salah", "Los Angeles")
        cron_mock = get_mock("adhan_pi.cli.CronTab")
        cron_mock.assert_called_with(user="salah")
        cron_mock().__enter__().find_comment.assert_called_with("adhan_pi")
        for i in [0, 1, 2, 3, 4]:
            cron_mock().__enter__().remove.assert_any_call(i)
        for p in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
            cron_mock().__enter__().new.assert_any_call(
                command="XDG_RUNTIME_DIR=/run/user/{user_id} /opt/adhan-pi/env/bin/alert_adhan --prayer {prayer} > /dev/null 2>&1".format(
                    user_id=1000, prayer=p,
                ),
                comment="adhan_pi",
            )
    pwd_mock = get_mock("adhan_pi.cli.pwd")
    pwd_mock.getpwnam.assert_called_with("salah")
    geopy_mock = get_mock("adhan_pi.utils.Nominatim")
    geopy_mock.assert_called_with(user_agent="adhan-pi")
    geopy_mock().geocode.assert_called_with("Los Angeles")
