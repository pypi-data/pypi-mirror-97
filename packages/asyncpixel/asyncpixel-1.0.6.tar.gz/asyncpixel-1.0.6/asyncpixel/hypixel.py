"""A Python HypixelAPI wrapper."""
#  Copyright (C) 2020 Leon Bowie
# This program is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License a
# long with this program. If not, see <https://www.gnu.org/licenses/>.
import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import aiohttp

from .exceptions import ApiNoSuccess
from .exceptions import InvalidApiKey
from .exceptions import RateLimitError
from .models import Auction
from .models import AuctionItem
from .models import Banner
from .models import Bazaar
from .models import BazaarItem
from .models import BazaarQuickStatus
from .models import BazaarSummary
from .models import Booster
from .models import Boosters
from .models import Friend
from .models import Game
from .models import GameCounts
from .models import GameCountsGame
from .models import gametype
from .models import Guild
from .models import GuildMembers
from .models import InvArmor
from .models import Item
from .models import Key
from .models import Leaderboards
from .models import Members
from .models import News
from .models import Objective
from .models import Pattern
from .models import Player
from .models import Profile
from .models import Quests
from .models import Status
from .models import WatchDog

__all__ = ["Hypixel"]

BASE_URL = "https://api.hypixel.net/"

GAMETYPES = (
    gametype("QUAKECRAFT", "Quake", "Quake", 2),
    gametype("WALLS", "Walls", "Walls", 3),
    gametype("PAINTBALL", "Paintball", "Paintball", 4),
    gametype("SURVIVAL_GAMES", "HungerGames", "Blitz Survival Games", 5),
    gametype("TNTGAMES", "TNTGames", "TNT Games", 6),
    gametype("VAMPIREZ", "VampireZ", "VampireZ", 7),
    gametype("WALLS3", "Walls3", "Mega Walls", 13),
    gametype("ARCADE", "Arcade", "Arcade", 14),
    gametype("ARENA", "Arena", "Arena", 17),
    gametype("UHC", "UHC", "UHC Champions", 20),
    gametype("MCGO", "MCGO", "Cops and Crims", 21),
    gametype("BATTLEGROUND", "Battleground", "Warlords", 23),
    gametype("SUPER_SMASH", "SuperSmash", "Smash Heroes", 24),
    gametype("GINGERBREAD", "GingerBread", "Turbo Kart Racers", 25),
    gametype("HOUSING", "Housing", "Housing", 26),
    gametype("SKYWARS", "SkyWars", "SkyWars", 51),
    gametype("TRUE_COMBAT", "TrueCombat", "Crazy Walls", 52),
    gametype("SPEED_UHC", "SpeedUHC", "Speed UHC", 54),
    gametype("SKYCLASH", "SkyClash", "SkyClash", 55),
    gametype("LEGACY", "Legacy", "Classic Games", 56),
    gametype("PROTOTYPE", "Prototype", "Prototype", 57),
    gametype("BEDWARS", "Bedwars", "Bed Wars", 58),
    gametype("MURDER_MYSTERY", "Quake", "Quake", 59),
    gametype("QUAKECRAFT", "MurderMystery", "Murder Mystery", 60),
    gametype("BUILD_BATTLE", "BuildBattle", "Build Battle", 61),
    gametype("DUELS", "Duels", "Duels", 62),
    gametype("SKYBLOCK", "SkyBlock", "SkyBlock", 63),
    gametype("PIT", "Pit", "Pit", 64),
)


class Hypixel:
    """Client class for hypixel wrapper."""

    def __init__(
        self,
        api_key: Optional[Union[str, uuid.UUID]] = None,
    ) -> None:
        """Initialise client object.

        Args:
            api_key (Optional[str], optional): hypixel api key. Defaults to None.
        """
        if isinstance(api_key, str) and api_key is not None:
            api_key = uuid.UUID(api_key)
        self.api_key = api_key
        self._session = aiohttp.ClientSession()
        self.requests_remaining: int = -1
        self.total_requests: int = 0
        self._ratelimit_reset: datetime.datetime = datetime.datetime(1998, 1, 1)
        self.retry_after: datetime.datetime = datetime.datetime(1998, 1, 1)

    async def close(self) -> None:
        """Used for safe client cleanup and stuff."""
        await self._session.close()

    async def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        key_required: Optional[bool] = True,
    ) -> Dict[str, Any]:
        """Base function to get raw data from hypixel.

        Args:
            path (str):
                path that you wish to request from.
            params (Dict, optional):
                parameters to pass into request defaults to empty dictionary.
            key_required (bool, optional): Wether key is needed

        Raises:
            RateLimitError: error if ratelimit has been reached.
            InvalidApiKey: error if api key is invalid.
            ApiNoSuccess: error if api throughs an error.

        Returns:
            dict: returns a dictionary of the json response.
        """
        if (
            self.requests_remaining != -1
            and (
                self.requests_remaining == 0
                and self._ratelimit_reset > datetime.datetime.now()
            )
            or self.retry_after
            and (self.retry_after > datetime.datetime.now())
        ):
            raise RateLimitError(self.retry_after)

        if params is None:
            params = {}
        if key_required:
            params["key"] = str(self.api_key)

        response: aiohttp.ClientResponse = await self._session.get(
            f"{BASE_URL}{path}", params=params
        )

        if response.status == 429:
            self.requests_remaining = 0
            self.retry_after = datetime.datetime.now() + datetime.timedelta(
                seconds=int(response.headers["Retry-After"])
            )
            raise RateLimitError(
                datetime.datetime.now()
                + datetime.timedelta(seconds=int(response.headers["Retry-After"]))
            )

        elif response.status == 400:
            raise InvalidApiKey()

        elif response.status != 200:
            raise ApiNoSuccess(path)

        elif key_required:
            if "RateLimit-Limit" in response.headers:
                if self.total_requests == 0:
                    self.total_requests = int(response.headers["RateLimit-Limit"])
                self.requests_remaining = int(response.headers["RateLimit-Remaining"])
                self._ratelimit_reset = datetime.datetime.now() + datetime.timedelta(
                    seconds=int(response.headers["RateLimit-Reset"])
                )

        data: Dict[str, Any] = await response.json()

        return data

    async def watchdog_stats(self) -> WatchDog:
        """Get current watchdog stats.

        Returns:
            WatchDog: WatchDog stats object.
        """
        data = await self._get("watchdogstats")

        return WatchDog(
            watchdog_last_minute=data["watchdog_lastMinute"],
            staff_rolling_daily=data["staff_rollingDaily"],
            watchdog_total=data["watchdog_total"],
            watchdog_rolling_daily=data["watchdog_rollingDaily"],
            staff_total=data["staff_total"],
        )

    async def key_data(self, key: Optional[str] = None) -> Key:
        """Get information about an api key.

        Args:
            key (str, optional): api key. Defaults token provided in class.

        Raises:
            InvalidApiKey: No api key available.

        Returns:
            Key: Key object.
        """
        if not key:
            key = str(self.api_key)

        if key == "None":
            raise InvalidApiKey()

        params = {"key": key}

        data = await self._get("key", params=params, key_required=False)

        return Key(
            key=data["record"]["key"],
            owner=data["record"]["owner"],
            limit=data["record"]["limit"],
            queries_in_past_min=data["record"]["queriesInPastMin"],
            total_queries=data["record"]["totalQueries"],
        )

    async def boosters(self) -> Boosters:
        """Get the current online boosters.

        Returns:
            Boosters: object containing boosters.
        """
        data = await self._get("boosters")
        boosterlist = []

        for boost in data["boosters"]:
            boosterlist.append(
                Booster(
                    id=boost["_id"],
                    purchaser_uuid=boost["purchaserUuid"],
                    amount=boost["amount"],
                    original_length=boost["originalLength"],
                    length=boost["length"],
                    game_type=[
                        game for game in GAMETYPES if game.id == boost["gameType"]
                    ][0],
                    date_activated=boost["dateActivated"],
                    stacked=boost.get("stacked", None),
                )
            )
        return Boosters(
            booster_state_decrementing=data["boosterState"]["decrementing"],
            boosters=boosterlist,
        )

    async def player_count(self) -> int:
        """Get the current amount of players online.

        Returns:
            int: number of online players.
        """
        data = await self._get("playerCount")

        return int(data["playerCount"])

    async def news(self) -> List[News]:
        """Get current skyblock news.

        Returns:
            List[News]: List of news objects.
        """
        data = await self._get("skyblock/news")
        news_list = []
        for item in data["items"]:
            if "data" in item["item"]:
                _item = Item(
                    material=item["item"]["material"], data=item["item"]["data"]
                )
            else:
                _item = Item(material=item["item"]["material"])
            news_list.append(
                News(
                    item=_item,
                    link=item["link"],
                    text=item["text"],
                    title=item["title"],
                )
            )

        return news_list

    async def player_status(self, uuid: Union[uuid.UUID, str]) -> Status:
        """Get current online status about a player.

        Args:
            uuid (str): uuid of player.

        Returns:
            Status: Status object of player.
        """
        data = await self._get("status", params={"uuid": str(uuid)})
        if data["session"]["online"]:
            return Status(
                online=True,
                game_type=[
                    game
                    for game in GAMETYPES
                    if game.TypeName == data["session"]["gameType"]
                ][0],
                mode=data["session"]["mode"],
                map=data["session"]["map"],
            )
        return Status(online=False)

    async def player_friends(self, uuid: Union[uuid.UUID, str]) -> List[Friend]:
        """Get a list of a players friends.

        Args:
            uuid (str): the uuid of the player you wish to get friends from.

        Returns:
            List[Friend]: returns a list of friend elements.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("friends", params=params)

        friend_list = []
        for friend in data["records"]:
            friend_list.append(
                Friend(
                    id=friend["_id"],
                    uuid_sender=friend["uuidSender"],
                    uuid_receiver=friend["uuidReceiver"],
                    started=friend["started"],
                )
            )

        return friend_list

    async def bazaar(self) -> Bazaar:
        """Get info of the items in the bazaar.

        Returns:
            Bazaar: object for bazzar.
        """
        data = await self._get("skyblock/bazaar")

        bazaar_items = []

        for name in data["products"]:
            elements = data["products"][name]
            sell_summary = []
            buy_summary = []
            for sell in elements["sell_summary"]:
                sell_summary.append(
                    BazaarSummary(
                        amount=sell["amount"],
                        price_per_unit=sell["pricePerUnit"],
                        orders=sell["orders"],
                    )
                )
            for buy in elements["buy_summary"]:
                buy_summary.append(
                    BazaarSummary(
                        amount=buy["amount"],
                        price_per_unit=buy["pricePerUnit"],
                        orders=buy["orders"],
                    )
                )
            quick = elements["quick_status"]
            bazaar_quick_status = BazaarQuickStatus(
                product_id=quick["productId"],
                sell_price=quick["sellPrice"],
                sell_volume=quick["sellVolume"],
                sell_moving_week=quick["sellMovingWeek"],
                sell_orders=quick["sellOrders"],
                buy_price=quick["buyPrice"],
                buy_volume=quick["buyVolume"],
                buy_moving_week=quick["buyMovingWeek"],
                buy_orders=quick["buyOrders"],
            )
            bazaar_items.append(
                BazaarItem(
                    name=name,
                    product_id=elements["product_id"],
                    sell_summary=sell_summary,
                    buy_summary=buy_summary,
                    quick_status=bazaar_quick_status,
                )
            )

        return Bazaar(
            last_updated=1590854517479,
            bazaar_items=bazaar_items,
        )

    async def auctions(self, page: Optional[int] = 0) -> Auction:
        """Get the auctions available.

        Args:
            page (int, optional): Page of auction list you want. Defaults to 0.

        Returns:
            Auction: Auction object.
        """
        params = {"page": page}
        data = await self._get("skyblock/auctions", params=params)
        auction_list = []
        for auc in data["auctions"]:
            auction_list.append(
                AuctionItem(
                    uuid=auc["uuid"],
                    auctioneer=auc["auctioneer"],
                    profile_id=auc["profile_id"],
                    coop=auc["coop"],
                    start=auc["start"],
                    end=auc["end"],
                    item_name=auc["item_name"],
                    item_lore=auc["item_lore"],
                    extra=auc["extra"],
                    category=auc["category"],
                    tier=auc["tier"],
                    starting_bid=auc["starting_bid"],
                    item_bytes=auc["item_bytes"],
                    claimed=auc["claimed"],
                    claimed_bidders=auc["claimed_bidders"],
                    highest_bid_amount=auc["highest_bid_amount"],
                    bids=auc["bids"],
                    bin=auc.get("bin", False),
                )
            )
        return Auction(
            page=data["page"],
            total_pages=data["totalPages"],
            total_auctions=data["totalAuctions"],
            last_updated=data["lastUpdated"],
            auctions=auction_list,
        )

    async def recent_games(self, uuid: Union[uuid.UUID, str]) -> List[Game]:
        """Get recent games of a player.

        Args:
            uuid (str): uuid of player.

        Returns:
            List[Game]: list of recent games.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("recentGames", params=params)

        games_list = []
        for game in data["games"]:
            if "ended" in game:
                games_list.append(
                    Game(
                        date=game["date"],
                        game_type=[
                            _game
                            for _game in GAMETYPES
                            if _game.TypeName == game["gameType"]
                        ][0],
                        mode=game["mode"],
                        map=game["map"],
                        ended=game["ended"],
                    )
                )
            else:
                games_list.append(
                    Game(
                        date=game["date"],
                        game_type=[
                            _game
                            for _game in GAMETYPES
                            if _game.TypeName == game["gameType"]
                        ][0],
                        mode=game["mode"],
                        map=game["map"],
                    )
                )

        return games_list

    async def player(self, uuid: Union[uuid.UUID, str]) -> Player:
        """Get information about a player from their uuid.

        Args:
            uuid (uuid.UUID): uuid of player.

        Returns:
            Player: player object.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("player", params=params)

        return Player(
            id=data["player"]["_id"],
            uuid=data["player"]["uuid"],
            first_login=data["player"]["firstLogin"],
            playername=data["player"]["playername"],
            last_login=data["player"]["lastLogin"],
            displayname=data["player"]["displayname"],
            known_aliases=data["player"]["knownAliases"],
            known_aliases_lower=data["player"]["knownAliasesLower"],
            achievements_one_time=data["player"]["achievementsOneTime"],
            mc_version_rp=data["player"]["mcVersionRp"],
            network_exp=data["player"]["networkExp"],
            karma=data["player"]["karma"],
            last_adsense_generate_time=data["player"]["lastAdsenseGenerateTime"],
            last_claimed_reward=data["player"]["lastClaimedReward"],
            total_rewards=data["player"]["totalRewards"],
            total_daily_rewards=data["player"]["totalDailyRewards"],
            reward_streak=data["player"]["rewardStreak"],
            reward_score=data["player"]["rewardScore"],
            reward_high_score=data["player"]["rewardHighScore"],
            last_logout=data["player"]["lastLogout"],
            friend_requests_uuid=data["player"]["friendRequestsUuid"],
            achievement_tracking=data["player"]["achievementTracking"],
            achievement_points=data["player"]["achievementPoints"],
            current_gadget=data["player"]["currentGadget"],
            channel=data["player"]["channel"],
            most_recent_game_type=[
                game
                for game in GAMETYPES
                if game.TypeName == data["player"]["mostRecentGameType"]
            ][0],
            level=self._calc_player_level(data["player"]["networkExp"]),
            raw=data,
        )

    @staticmethod
    def _calc_player_level(xp: Union[float, int]) -> float:
        """Calculate player level from xp.

        Args:
            xp (int): amount of xp a player has.

        Returns:
            float: current level of player.
        """
        return 1 + (-8750.0 + (8750 ** 2 + 5000 * xp) ** 0.5) / 2500

    async def guild_by_name(self, guild_name: str) -> Guild:
        """Get guild by name.

        Args:
            guild_name (str): name of guild.

        Returns:
            Guild: guild object.
        """
        params = {"name": guild_name}
        data = await self._get("guild", params=params)
        guild_object = self._create_guild_object(data)
        return guild_object

    async def guild_by_id(self, guild_id: str) -> Guild:
        """Get guild by id.

        Args:
            guild_id (str): id of guild.

        Returns:
            Guild: guild object.
        """
        params = {"id": guild_id}
        data = await self._get("guild", params=params)
        guild_object = self._create_guild_object(data)
        return guild_object

    async def guild_by_player(self, player_uuid: Union[uuid.UUID, str]) -> Guild:
        """Get guild by player.

        Args:
            player_uuid (str): uuid of a player in the guild.

        Returns:
            Guild: guild object.
        """
        params = {"player": str(player_uuid)}
        data = await self._get("guild", params=params)
        guild_object = self._create_guild_object(data)
        return guild_object

    @staticmethod
    def _create_guild_object(data: Dict[str, Any]) -> Guild:
        """Create guild object from json.

        Args:
            data (dict): json.

        Returns:
            Guild: guild object.
        """
        guild = data["guild"]
        members = []
        for member in data["guild"]["members"]:
            members.append(
                GuildMembers(
                    uuid=member["uuid"],
                    rank=member["rank"],
                    joined=member["joined"],
                    exp_history=member["expHistory"],
                    quest_participation=member["questParticipation"],
                    muted_till=member["mutedTill"],
                )
            )
        patterns = []
        for pattern in guild["banner"]["Patterns"]:
            patterns.append(Pattern(color=pattern["Color"], pattern=pattern["Pattern"]))
        banner = Banner(base=guild["banner"]["Base"], patterns=patterns)
        return Guild(
            id=guild["_id"],
            created=guild["created"],
            name=guild["name"],
            name_lower=guild["name_lower"],
            description=guild["description"],
            tag=guild["tag"],
            tag_color=guild["tagColor"],
            exp=guild["exp"],
            members=members,
            achievements=guild["achievements"],
            ranks=guild["ranks"],
            joinable=guild["joinable"],
            legacy_ranking=guild["legacyRanking"],
            publicly_listed=guild["publiclyListed"],
            hide_gm_tag=guild["hideGmTag"],
            preferred_games=guild["preferredGames"],
            chat_mute=guild["chatMute"],
            guild_exp_by_game_type=guild["guildExpByGameType"],
            banner=banner,
        )

    async def auction_from_uuid(self, uuid: Union[uuid.UUID, str]) -> List[AuctionItem]:
        """Get auction from uuid.

        Args:
            uuid (str): minecraft uuid.

        Returns:
            List[AuctionItem]: list of auctions.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("skyblock/auction", params=params)
        auction_items = self._create_auction_object(data)
        return auction_items

    async def auction_from_player(self, player: str) -> List[AuctionItem]:
        """Get auction data from player.

        Args:
            player (str): player.

        Returns:
            List[AuctionItem]: list of auction items.
        """
        params = {"player": player}
        data = await self._get("skyblock/auction", params=params)
        auction_items = self._create_auction_object(data)
        return auction_items

    async def auction_from_profile(self, profile_id: str) -> List[AuctionItem]:
        """Get auction data from profile.

        Args:
            profile_id (str): profile id.

        Returns:
            List[AuctionItem]: list of auction items.
        """
        params = {"profile": profile_id}
        data = await self._get("skyblock/auction", params=params)
        auction_items = self._create_auction_object(data)
        return auction_items

    @staticmethod
    def _create_auction_object(data: Dict[str, Any]) -> List[AuctionItem]:
        """Create auction object.

        Args:
            data (Dict): json input.

        Returns:
            List[AuctionItem]: auction object list.
        """
        auction_list = []
        for auc in data["auctions"]:
            auction_list.append(
                AuctionItem(
                    id=auc["_id"],
                    uuid=auc["uuid"],
                    auctioneer=auc["auctioneer"],
                    profile_id=auc["profile_id"],
                    coop=auc["coop"],
                    start=auc["start"],
                    end=auc["end"],
                    item_name=auc["item_name"],
                    item_lore=auc["item_lore"],
                    extra=auc["extra"],
                    category=auc["category"],
                    tier=auc["tier"],
                    starting_bid=auc["starting_bid"],
                    item_bytes=auc["item_bytes"],
                    claimed=auc["claimed"],
                    claimed_bidders=auc["claimed_bidders"],
                    highest_bid_amount=auc["highest_bid_amount"],
                    bids=auc["bids"],
                    bin=auc.get("bin", False),
                )
            )
        return auction_list

    async def game_count(self) -> GameCounts:
        """Gets number of players per game.

        Returns:
            GameCounts: game counts.
        """
        data = await self._get("gameCounts")
        games = {}
        for key in data["games"]:
            games[key] = GameCountsGame(
                players=data["games"][key]["players"], modes=data["games"][key]["modes"]
            )
        return GameCounts(games=games, player_count=data["playerCount"])

    async def leaderboards(self) -> Dict[str, List[Leaderboards]]:
        """Get the current leaderboards.

        Returns:
            Dict[str, Leaderboards]: raw json response.
        """
        data = await self._get("leaderboards")
        leaderboard = {}
        leaderboards = data["leaderboards"]
        for key in leaderboards.keys():
            leaderboards_list = []
            for element in leaderboards[key]:
                location: Tuple[int, int, int] = (
                    int(element["location"].split(",")[0]),
                    int(element["location"].split(",")[1]),
                    int(element["location"].split(",")[2]),
                )
                leaderboards_list.append(
                    Leaderboards(
                        path=element["path"],
                        prefix=element["prefix"],
                        title=element["title"],
                        location=location,
                        count=element["count"],
                        leaders=element["leaders"],
                    )
                )
            leaderboard[key] = leaderboards_list

        return leaderboard

    async def resources_achievements(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/achievements", key_required=False)
        return data

    async def resources_challenges(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/challenges", key_required=False)
        return data

    async def resources_quests(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/quests", key_required=False)
        return data

    async def resources_guilds_achievements(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/guilds/achievements", key_required=False)
        return data

    async def resources_guilds_permissions(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/guilds/permissions", key_required=False)
        return data

    async def resources_skyblock_collections(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/skyblock/collections", key_required=False)
        return data

    async def resources_skyblock_skills(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/skyblock/skills", key_required=False)
        return data

    @staticmethod
    def _fill_profile(data: Dict[str, Any]) -> Profile:
        """Generate profile.

        Args:
            data (Dict[str, Any]): profile dict.

        Returns:
            Profile: profile class.
        """
        member_dict = {}
        for member in data["members"]:
            member_data = data["members"][member]
            quests_dict = {}
            for quest in member_data["quests"]:
                quests_dict[quest] = Quests(
                    status=member_data["quests"][quest]["status"],
                    activated_at=member_data["quests"][quest]["activated_at"],
                    activated_at_sb=member_data["quests"][quest]["activated_at_sb"],
                    completed_at=member_data["quests"][quest]["completed_at"],
                    completed_at_sb=member_data["quests"][quest]["completed_at_sb"],
                )
            objective_dict = {}
            for objective in member_data["objectives"]:
                objective_dict[objective] = Objective(
                    status=member_data["objectives"][objective]["status"],
                    progress=member_data["objectives"][objective]["progress"],
                    completed_at=member_data["objectives"][objective]["completed_at"],
                )
            invarmor = InvArmor(
                type=member_data["inv_armor"]["type"],
                data=member_data["inv_armor"]["data"],
            )
            members = Members(
                last_save=member_data["last_save"],
                inv_armor=invarmor,
                first_join=member_data["first_join"],
                first_join_hub=member_data["first_join_hub"],
                stats=member_data["stats"],
                objectives=objective_dict,
                tutorial=member_data["tutorial"],
                quests=quests_dict,
                coin_purse=member_data["coin_purse"],
                last_death=member_data["last_death"],
                crafted_generators=member_data["crafted_generators"]
                if "crafted_generators" in member_data
                else None,
                visited_zones=member_data["visited_zones"],
                fairy_souls_collected=member_data["fairy_souls_collected"],
                fairy_souls=member_data.get("fairy_souls", None),
                death_count=member_data["death_count"],
                slayer_bosses=member_data["slayer_bosses"],
                pets=member_data["pets"],
            )
            member_dict[member] = members

        return Profile(
            profile_id=data["profile_id"],
            cute_name=data.get("cute_name", None),
            members=member_dict,
            raw=data,
        )

    async def profile(self, profile: str) -> Profile:
        """Get profile info of a skyblock player.

        Args:
            profile (str): profile id of player can be gotten from
                            running profiles.

        Returns:
            Profile: Profile.
        """
        params = {"profile": profile}
        data = await self._get("skyblock/profile", params=params)
        profiles: Profile = self._fill_profile(data["profile"])
        return profiles

    async def profiles(self, uuid: Union[uuid.UUID, str]) -> Dict[str, Profile]:
        """Get info on a profile.

        Args:
            uuid (str): uuid of player.

        Returns:
            Dict[str, Profile]: json response.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("skyblock/profiles", params=params)
        profiles = data["profiles"]
        profile_dict = {}
        for profile in profiles:
            _id = profile["profile_id"]
            profile_dict[_id] = self._fill_profile(profile)

        return profile_dict
