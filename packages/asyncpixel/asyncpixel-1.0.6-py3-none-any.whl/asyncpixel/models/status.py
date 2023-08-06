"""Status data class."""
from typing import Optional

from pydantic import BaseModel

from .game_type import gametype


class Status(BaseModel):
    """Status data object.

    Args:
        online (bool): Wether player is online.
        game_type (Optional[str]): Current game player is playing. Defaults to None.
        mode (Optional[str]): Mode of current game. Defaults to None.
        map (Optional[str]): Map of current game. Defaults to None.
    """

    online: bool
    game_type: Optional[gametype] = None
    mode: Optional[str] = None
    map: Optional[str] = None
