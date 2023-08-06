"""Guild objects."""
import datetime
import uuid
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class Pattern(BaseModel):
    """Pattern."""

    color: int
    pattern: str


class Banner(BaseModel):
    """Banner for the guild.

    Args:
        Base (int): Base Colour.
        Patterns (List[Dict[str, Union[int, str]]]): Object with colour
            details of banner.
    """

    base: int
    patterns: List[Pattern]


class GuildMembers(BaseModel):
    """Members in a guild.

    Args:
        uuid (uuid.UUID): UUID of player.
        rank (str): Rank of player.
        joined (datetime.datetime): Time player joined guild.
        exp_history (Dict[str, int]): Exp history of player.
        quest_participation (int): How many quests the player has participated in.
        muted_till (Optional[datetime.datetime]): Time player unmuted. Defaults to None.
    """

    uuid: uuid.UUID
    rank: str
    joined: datetime.datetime
    exp_history: Dict[str, int]
    quest_participation: int
    muted_till: Optional[datetime.datetime] = None


class Rank(BaseModel):
    """Rank.

    Args:
        name (str): Name of rank.
        default (bool): wether its the default.
        created (int): Created.
        priority (int): Priority of role.
        tag (str): Tag of role.
    """

    name: str
    default: bool
    created: int
    priority: int
    tag: str


class Guild(BaseModel):
    """Guild object.

    Args:
        id (str): Guild ID.
        created (datetime.datetime): Timestamp this guild was created at.
        name (str): Name of guild.
        name_lower (str: Priority of role.
        description (str): Description of this guild that appears in the
            guild list and /g info.
        tag (str): Tag of guild.
        exp (int): Exp or guild.
        members (List[Guild_Members]): Array of guild members.
        achievements (Dict[str, int]): Guild achievements earned and
            the current progress.
        ranks (List[Rank]): Array of guild ranks.
        joinable (bool): Whether this guild can be joined using /g join.
        legacy_ranking (int): Ranking in the number of guild coins owned in
            the legacy guild system (0-indexed).
        publicly_listed (bool): Whether this guild is listed in the Guild Finder.
        hide_gm_tag (bool): Whether guild master tag is hidden in guild chat.
        preferred_games (List[str]): This guild's set preferred games.
        chat_mute (datetime.datetime): Timestamp guild chat will be unmuted at,
            or 0 if guild chat is not muted.
        guild_exp_by_game_type (Dict[str, str]): Amount of EXP earned for this guild
            by which game it was earned in.
        banner (Banner):This guild's Minecraft banner - Displayed on the H
            ypixel forums page. See https://minecraft.gamepedia.com/Banner/Patterns
            for pattern IDs.
        tag_color (Optional[str]): Color of this guild's tag, if set. Defaults to None.
    """

    id: str
    created: datetime.datetime
    name: str
    name_lower: str
    description: str
    tag: str
    exp: int
    members: List[GuildMembers]
    achievements: Dict[str, int]
    ranks: List[Rank]
    joinable: bool
    legacy_ranking: int
    publicly_listed: bool
    hide_gm_tag: bool
    preferred_games: List[str]
    chat_mute: datetime.datetime
    guild_exp_by_game_type: Dict[str, int]
    banner: Banner
    tag_color: Optional[str] = None
