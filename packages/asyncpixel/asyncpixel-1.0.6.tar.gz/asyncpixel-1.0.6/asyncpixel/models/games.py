"""Game related objects."""
import datetime
from typing import Optional

from pydantic import BaseModel

from .game_type import gametype


class Game(BaseModel):
    """Game class.

    Args:
        date (datetime.datetime): Time game started.
        game_type (str): Game Type.
        mode (str): Game mode.
        map (str): Map the game is on.
        ended (Optional[datetime.datetime]): Time game ended. Defaults to None.
    """

    date: datetime.datetime
    game_type: gametype
    mode: str
    map: str
    ended: Optional[datetime.datetime] = None
