"""Data object for player friends."""
import datetime
import uuid

from pydantic import BaseModel


class Friend(BaseModel):
    """Friend object.

    Args:
        id (bool): Id of friend.
        uuid_sender (uuid.UUID): UUID of player sending friend request.
        uuid_receiver (uuid.UUID): UUID of player receiving friend request.
        started (datetime.datetime): Time players started being friends.
    """

    id: str
    uuid_sender: uuid.UUID
    uuid_receiver: uuid.UUID
    started: datetime.datetime
