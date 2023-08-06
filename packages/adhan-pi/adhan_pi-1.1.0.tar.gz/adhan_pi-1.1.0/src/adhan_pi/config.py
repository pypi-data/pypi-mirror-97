import os

FAJR_ADHAN_MP3_PATH = os.getenv(
    "FAJR_ADHAN_MP3_PATH", "/opt/adhan-pi/static/azan-fajr.mp3"
)
ADHAN_MP3_PATH = os.getenv("ADHAN_MP3_PATH", "/opt/adhan-pi/static/azan2.mp3")
AUTOMOCK_REGISTRATION_IMPORTS = ("adhan_pi.test_mocks",)
