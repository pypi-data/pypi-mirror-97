"""Game Count related objects."""
import uuid
from typing import List
from typing import Tuple

from pydantic import BaseModel


class Leaderboards(BaseModel):
    """Game count game.

    Args:
        path (int): Path.
        prefix (str): Prefix.
        title (str): Title of leaderboard.
        location (Tuple[int, int, int]): Location of leaderboard in lobby.
        count (int): Count of leaderboards.
        leaders (List[uuid.UUID]): List of leaders on the leaderboard.
    """

    path: str
    prefix: str
    title: str
    location: Tuple[int, int, int]
    count: int
    leaders: List[uuid.UUID]
