"""Data objects for boosters."""
import datetime
import uuid
from typing import List
from typing import Union

from pydantic import BaseModel

from .game_type import gametype


class Booster(BaseModel):
    """Main booster class.

    Args:
        id (str): ID
        purchaser_uuid (uuid.UUID): UUID of booster.
        amount (int): Amount of boosters.
        original_length (int): Original length of booster.
        length (int): Length of booster.
        game_type (int): Game type.
        date_activated (datetime.datetime): Date boost activated.
        stacked (Union[List[uuid.UUID], bool]): Wether boosters stacked.
    """

    id: str
    purchaser_uuid: uuid.UUID
    amount: float
    original_length: int
    length: int
    game_type: gametype
    date_activated: datetime.datetime
    stacked: Union[List[uuid.UUID], bool]


class Boosters(BaseModel):
    """Object containing boosters.

    Args:
        booster_state_decrementing (bool): Wether booster state decrementing.
        boosters (List[Booster]): List of boosters online.
    """

    booster_state_decrementing: bool
    boosters: List[Booster]
