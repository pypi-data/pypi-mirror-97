"""Profile objects."""
import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class Quests(BaseModel):
    """Armor.

    Args:
        status (str): Status of quest.
        activated_at (datetime.datetime): Time activated.
        activated_at_sb (datetime.datetime): Time activated.
        completed_at (datetime.datetime): Time Completed.
        completed_at_sb (datetime.datetime): Time Completed.
    """

    status: str
    activated_at: datetime.datetime
    activated_at_sb: datetime.datetime
    completed_at: datetime.datetime
    completed_at_sb: datetime.datetime


class Objective(BaseModel):
    """Armor.

    Args:
        status (str): Status of objective.
        progress (int): Progress through objective.
        completed_at (Optional[datetime.datetime]): Time compelted at. Defaults to None.
    """

    status: str
    progress: int
    completed_at: Optional[datetime.datetime] = None


class InvArmor(BaseModel):
    """Armor.

    Args:
        type (int): Type of armor.
        data (str): Data of armor.
    """

    type: int
    data: str


class Members(BaseModel):
    """Member.

    Args:
        last_save (datetime.datetime):Time last saved.
        inv_armor (InvArmor): Armor.
        first_join (datetime.datetime): Time first joined.
        first_join_hub (datetime.datetime): first joined hub.
        stats (Dict[str, int]): Member stats.
        objectives (Dict[str, Objective]): Objectives.
        tutorial (List[str]): Tutorial.
        quests (Dict[str, Quests]): Quests done.
        coin_purse (int): Amount of coins in purse.
        last_death (datetime.datetime): Time last died.
        crafted_generators (List[str]): Crafted generators.
        visited_zones (List[str]): Visited zones.
        fairy_souls_collected (int): Souls collected.
        fairy_souls (Optional[int]): Fairy souls.
        death_count (type): death count.
        slayer_bosses (Dict[str, Dict[str, Any]]): Slayer bosses.
        pets (List[Any]): Pets.
    """

    last_save: datetime.datetime
    inv_armor: InvArmor
    first_join: datetime.datetime
    first_join_hub: int
    stats: Dict[str, float]
    objectives: Dict[str, Objective]
    tutorial: List[str]
    quests: Dict[str, Quests]
    coin_purse: float
    last_death: int
    crafted_generators: Optional[List[str]]
    visited_zones: List[str]
    fairy_souls_collected: int
    fairy_souls: Optional[int]
    death_count: int
    slayer_bosses: Dict[str, Dict[str, Any]]
    pets: List[Any]


class Profile(BaseModel):
    """Profile.

    Args:
        profile_id (str): Id of profile
        cute_name (Optional[str]): Cute name of profile
        members (Dict[str, Members]): Dict of all members in profile.
        raw (Dict[str, Any]): Raw response.
    """

    profile_id: uuid.UUID
    cute_name: Optional[str]
    members: Dict[str, Members]
    raw: Dict[str, Any]
