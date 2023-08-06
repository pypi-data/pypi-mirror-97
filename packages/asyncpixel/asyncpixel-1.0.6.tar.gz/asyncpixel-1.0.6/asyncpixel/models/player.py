"""Player objects."""
import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel

from .game_type import gametype


class Player(BaseModel):
    """Player object.

    Args:
        id (str): ID of the player.
        uuid (UUID): UUID of the player.
        first_login (datetime): Datetime of the players first login.
        playername (str): The players name.
        last_login (datetime): Datetime of the players last login.
        displayname (str): Display name of the player.
        known_aliases (List[str]): List of the players known aliases.
        known_aliases_lower (List[str]): List of the players known
            aliases in lower case.
        achievements_one_time (List[str]): Players achievements.
        mc_version_rp (str): Minecraft version of the player.
        network_exp (float): Experience points on the network.
        karma (int): Total karama.
        last_adsense_generate_time (datetime): Datetime of the last
            daily claimed reward.
        last_claimed_reward (int): Last claimed reward.
        total_rewards (int): Total amount of rewards the player has.
        total_daily_rewards (int): Total amount of dialy rewards the player has.
        reward_streak (int): Streak of how long a player has opened daily rewards for.
        reward_score (int): Current score of the players daily reward.
        reward_high_score (int): Highest score of the players daily reward.
        last_logout (datetime): Datetime of the last time the player logged out.
        friend_requests_uuid (List[UUID]): UUID list of the players friend requests.
        achievement_tracking (List[str]): List of the players tracked achievements.
        achievement_points (Int): Points the player achieved from doing achievements.
        current_gadget (str): The players currently selected gadget.
        channel (str): The players channel.
        most_recent_game_type (gametype): The players most recently played game.
        level (float): Current level on hypixel.
        raw (Dict[str, Any]): Raw response.
    """

    id: str
    uuid: uuid.UUID
    first_login: datetime.datetime
    playername: str
    last_login: datetime.datetime
    displayname: str
    known_aliases: List[str]
    known_aliases_lower: List[str]
    achievements_one_time: List[str]
    mc_version_rp: str
    network_exp: float
    karma: int
    last_adsense_generate_time: datetime.datetime
    last_claimed_reward: int
    total_rewards: int
    total_daily_rewards: int
    reward_streak: int
    reward_score: int
    reward_high_score: int
    last_logout: datetime.datetime
    friend_requests_uuid: List[uuid.UUID]  # type: ignore[name-defined]
    achievement_tracking: List[str]
    achievement_points: int
    current_gadget: str
    channel: str
    most_recent_game_type: gametype
    level: float
    raw: Dict[str, Any]
