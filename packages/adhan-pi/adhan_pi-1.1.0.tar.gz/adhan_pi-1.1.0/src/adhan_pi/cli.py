import datetime as dt
import os
import pickle
import pwd
from abc import ABC, abstractmethod
from argparse import ArgumentParser

from .config import ADHAN_MP3_PATH, FAJR_ADHAN_MP3_PATH
from .dataclasses import PrayerTimes
from .utils import get_location_from_query, get_prayer_times_for_month

try:
    from crontab import CronTab
    from pydub import AudioSegment
    from pydub.playback import play

    CRON_SCRIPTS_IMPORTED = True
except ImportError:
    CRON_SCRIPTS_IMPORTED = False


def schedule_prayer_cron_runner() -> None:
    parser = ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    schedule_prayer_cron(args.user, args.query)


def schedule_prayer_cron(user: str, query: str) -> None:
    if not CRON_SCRIPTS_IMPORTED:
        raise ImportError

    user_id = pwd.getpwnam(user).pw_uid

    prayer_times = _get_prayer_times_for_today(query)

    with CronTab(user=user) as cron:
        for old_job in cron.find_comment("adhan_pi"):
            cron.remove(old_job)

        for prayer in prayer_times:
            job = cron.new(
                command="XDG_RUNTIME_DIR=/run/user/{user_id} /opt/adhan-pi/env/bin/alert_adhan --prayer {prayer} > /dev/null 2>&1".format(
                    user_id=user_id, prayer=prayer.name
                ),
                comment="adhan_pi",
            )
            job.day.every(1)
            job.hour.on(prayer.time.hour)
            job.minute.on(prayer.time.minute)


def _get_prayer_times_for_today(query: str) -> PrayerTimes:
    today = dt.date.today()

    cache_folder = os.environ.get(
        "CACHE_FOLDER",
        os.path.expanduser(f"~/.cache/prayertimes/{today.year}/"),
    )
    os.makedirs(cache_folder, exist_ok=True)

    cache_file = os.path.join(
        cache_folder, f"{today.strftime('%B').lower()}.pickle"
    )
    try:
        with open(cache_file, "rb") as f:
            prayer_times_all = pickle.load(f)
        if prayer_times_all[today.day - 1].date != today:
            raise KeyError
    except (FileNotFoundError, IndexError, AttributeError, KeyError):
        prayer_times_all = get_prayer_times_for_month(
            get_location_from_query(query), today.year, today.month
        )
        with open(cache_file, "wb") as f:
            pickle.dump(prayer_times_all, f)
    return prayer_times_all[today.day - 1]


class AdhanAlert(ABC):
    def __init__(self, prayer: str):
        self.prayer = prayer

    @abstractmethod
    def alert(self) -> None:
        pass


class AdhanAlertFFMPEG(AdhanAlert):
    """
    play adhan sound
    """

    def alert(self) -> None:
        if not CRON_SCRIPTS_IMPORTED:
            raise ImportError

        if self.prayer == "fajr":
            adhan = AudioSegment.from_mp3(FAJR_ADHAN_MP3_PATH)
        else:
            adhan = AudioSegment.from_mp3(ADHAN_MP3_PATH)
        play(adhan)


def alert_factory(prayer: str) -> AdhanAlert:
    return AdhanAlertFFMPEG(prayer)


def alert_adhan() -> None:
    parser = ArgumentParser()
    parser.add_argument("--prayer", required=True)
    args = parser.parse_args()
    alert_cls = alert_factory(args.prayer)
    alert_cls.alert()
