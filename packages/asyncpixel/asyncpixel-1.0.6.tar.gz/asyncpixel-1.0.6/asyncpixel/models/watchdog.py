"""Watchdog objects."""
from pydantic import BaseModel


class WatchDog(BaseModel):
    """Base class for watchdog.

    Args:
        watchdog_last_minute (int): Watchdog bans in last minute.
        staff_rolling_daily (int): Staff bans in the day.
        watchdog_total (int): Watchdog total bans.
        watchdog_rolling_daily (int): Watchdog bans in the day.
        staff_total (int): Staff total bans.
    """

    watchdog_last_minute: int
    staff_rolling_daily: int
    watchdog_total: int
    watchdog_rolling_daily: int
    staff_total: int
