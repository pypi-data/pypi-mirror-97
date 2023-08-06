"""Auction related objects."""
import datetime
import uuid
from math import floor
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel


class Bids(BaseModel):
    """Bid models.

    Args:
        auction_id (uuid.UUID): Id of auction.
        bidder (uuid.UUID): Id of bidder.
        profile_id (uuid.UUID): Profile_id of seller.
        amount (str): Amount bidded.
        timestamp (datetime.datetime): Timestamp of bid placed.
    """

    auction_id: uuid.UUID
    bidder: uuid.UUID
    profile_id: uuid.UUID
    amount: int
    timestamp: datetime.datetime


class AuctionItem(BaseModel):
    """Auction model.

    Args:
        uuid (uuid.UUID): Id of auction.
        auctioneer (uuid.UUID): Id of seller.
        profile_id (uuid.UUID): Profile_id of seller.
        coop (str): Amount bidded.
        start (datetime.datetime): Start time of auction.
        end (datetime.datetime): End time of auction.
        item_name (str): Name of auction item.
        item_lore (str): Lore of item.
        extra (str): extra.
        category (str): Item category
        tier (str): Tier of item.
        starting_bid (int): Starting Auction bid.
        item_bytes (str): Bytes of item.
        claimed (bool): Wehther the auction has been won.
        claimed_bidders (Optional[List[uuid.UUID]]): Amount bidded.
        highest_bid_amount (int): Highest amount bidded.
        bids (List[Bids]): List of bids on auction.
        id (str): Id of auction.
        bin (bool): Whether the auction is BIN (Buy instantly)

    """

    uuid: uuid.UUID  # type: ignore[name-defined]
    auctioneer: uuid.UUID  # type: ignore[name-defined]
    profile_id: uuid.UUID  # type: ignore[name-defined]
    coop: List[uuid.UUID]  # type: ignore[name-defined]
    start: datetime.datetime
    end: datetime.datetime
    item_name: str
    item_lore: str
    extra: str
    category: str
    tier: str
    starting_bid: int
    item_bytes: Union[str, Dict[str, Union[int, str]]]
    claimed: bool
    claimed_bidders: List[uuid.UUID]  # type: ignore[name-defined]
    highest_bid_amount: int
    bids: List[Bids]
    id: Optional[str] = None
    bin: bool

    def active(self) -> bool:
        """Return if auction is active - you can bid on it."""
        return not self.claimed and datetime.datetime.now(tz=self.end.tzinfo) < self.end

    def lowest_possible_bid(self) -> int:
        """Returns next lowest possible bid."""
        current_price = max(self.starting_bid, self.highest_bid_amount)

        if 1 <= current_price <= 3:
            return floor(current_price) + 1

        return floor(current_price * 1.15)


class Auction(BaseModel):
    """Main auction object.

    Args:
        page (int): Page of auction data.
        total_pages (int): Total pages of auctions.
        total_auctions (int): Total number of auctions.
        last_updated (datetime.datetime): Time last updated.
        auctions (List[AuctionItem]): List of auctions.
    """

    page: int
    total_pages: int
    total_auctions: int
    last_updated: datetime.datetime
    auctions: List[AuctionItem]
