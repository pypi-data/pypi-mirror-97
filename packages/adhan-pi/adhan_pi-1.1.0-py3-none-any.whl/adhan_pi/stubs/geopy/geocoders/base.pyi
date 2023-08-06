from typing import Callable, Optional, Union

DEFAULT_SENTINEL = type(
    "object", (object,), {"__repr__": lambda self: "DEFAULT_SENTINEL"}
)()

class Geocoder:
    def __init__(
        self,
        *,
        scheme: Optional[str] = None,
        timeout: Union[int, object] = DEFAULT_SENTINEL,
        proxies: Union[int, object] = DEFAULT_SENTINEL,
        user_agent: Optional[str] = None,
        ssl_context: Union[int, object] = DEFAULT_SENTINEL,
    ) -> None: ...
