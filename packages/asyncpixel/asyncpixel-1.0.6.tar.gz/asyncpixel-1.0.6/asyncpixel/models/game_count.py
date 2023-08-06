"""Game Count related objects."""
from typing import Dict

from pydantic import BaseModel


class GameCountsGame(BaseModel):
    """Game count game.

    Args:
        players (int): Number of players in a game.
        uuid_sender (Dict[str, int]): Dict of game modes and people in them.
    """

    players: int
    modes: Dict[str, int]


class GameCounts(BaseModel):
    """Game Count class.

    Args:
        games (Dict[str, GameCountsGame]): dict of all game and their game counts.
        player_count (int): total number of players online.
    """

    games: Dict[str, GameCountsGame]
    player_count: int
