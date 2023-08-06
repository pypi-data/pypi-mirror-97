from unittest.mock import MagicMock, Mock

import automock
from geopy.location import Location


def geocode_mock(failed_lookup: bool = False) -> Mock:
    m = Mock()
    if failed_lookup:
        m.return_value.geocode.return_value = None
    else:
        m.return_value.geocode.return_value = Location(
            "nyc", (0, 1), {"address": "nyc", "longitude": 0, "latitude": 0}
        )
    return m


def cron_mock(previous_jobs: bool = False) -> MagicMock:
    m = MagicMock()
    if not previous_jobs:
        m.return_value.__enter__.return_value.find_comment.return_value = []
    else:
        m.return_value.__enter__.return_value.find_comment.return_value = [
            0,
            1,
            2,
            3,
            4,
        ]
    import crontab

    def new_job(command: str, comment: str) -> crontab.CronItem:
        job = crontab.CronItem(
            command=command,
            comment=comment,
            user=None,
            cron=None,
            pre_comment=False,
        )
        return job

    m.return_value.__enter__.return_value.new.side_effect = new_job
    return m


def pwd_mock(valid: bool = True) -> Mock:
    m = Mock()
    if valid:
        m.getpwnam.return_value.pw_uid = 1000
    else:
        m.getpwnam.side_effect = KeyError
    return m


automock.register("adhan_pi.utils.Nominatim", geocode_mock)
automock.register("adhan_pi.cli.CronTab", cron_mock)
automock.register("adhan_pi.cli.AudioSegment")
automock.register("adhan_pi.cli.play")
automock.register("adhan_pi.cli.pwd", pwd_mock)
