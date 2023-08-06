"""Bazaar classes."""
import datetime
from typing import List

from pydantic import BaseModel


class BazaarSummary(BaseModel):
    """Bazaar object.

    Args:
        amount (int): Amount available to buy.
        price_per_unit (float): Price per unit.
        orders (int): How many orders.
    """

    amount: int
    price_per_unit: float
    orders: int


class BazaarQuickStatus(BaseModel):
    """Bazaar quick status.

    Args:
        product_id (str): Id of product.
        sell_price (int): Sell price per unit.
        sell_volume (float): Volume of sale.
        sell_moving_week (int): Sell moving week.
        sell_orders (int): How many orders.
        buy_price (int): Buy price.
        buy_volume (float): Volume of purchase.
        buy_moving_week (int): How many orders.
        buy_orders (int): How many orders.
    """

    product_id: str
    sell_price: float
    sell_volume: int
    sell_moving_week: int
    sell_orders: int
    buy_price: float
    buy_volume: int
    buy_moving_week: int
    buy_orders: int


class BazaarItem(BaseModel):
    """Bazaar item.

    Args:
        product_id (str): Product id.
        buy_summary (List[BazaarSellSummary]): List of sell summary.
        buy_summary (List[BazaarBuySummary]): List of buy summary.
        quick_status (BazaarQuickStatus): Quick status.
    """

    product_id: str
    sell_summary: List[BazaarSummary]
    buy_summary: List[BazaarSummary]
    quick_status: BazaarQuickStatus


class Bazaar(BaseModel):
    """Bazaar object.

    Args:
        last_updated (datetime.datetime): Time last updated.
        bazaar_items (List[BazaarItem]): Items in bazaar.
    """

    last_updated: datetime.datetime
    bazaar_items: List[BazaarItem]
