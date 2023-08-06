class AdhanPiError(Exception):
    pass


class PrayerAPIError(AdhanPiError):
    pass


class LocationNotFoundError(AdhanPiError):
    def __init__(self, query: str):
        super().__init__("Could not find location for {}".format(query))
