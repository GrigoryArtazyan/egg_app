"""Pickup date logic: the last Saturday of each month."""

from __future__ import annotations

import calendar
from datetime import date


def last_saturday(year: int, month: int) -> date:
    """Return the date of the last Saturday in the given month."""
    last_day = calendar.monthrange(year, month)[1]
    d = date(year, month, last_day)
    # weekday(): Monday=0 ... Saturday=5
    offset = (d.weekday() - 5) % 7
    return date(year, month, last_day - offset)


def upcoming_pickup_dates(count: int = 4, today: date | None = None) -> list[date]:
    """Return the next `count` last-Saturday pickup dates, including this
    month's if it has not passed yet."""
    today = today or date.today()
    results: list[date] = []
    year, month = today.year, today.month
    while len(results) < count:
        candidate = last_saturday(year, month)
        if candidate >= today:
            results.append(candidate)
        month += 1
        if month > 12:
            month = 1
            year += 1
    return results
