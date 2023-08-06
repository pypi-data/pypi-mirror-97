from typing import Callable, Optional
from unittest.mock import Mock

def register(cmd: str, mock: Optional[Callable[..., Mock]] = Mock) -> None: ...
