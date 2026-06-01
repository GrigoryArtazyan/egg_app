"""Pickup dates — manually maintained.

To change the available pickup dates, edit the PICKUP_DATES list below.
Use ISO format strings: "YYYY-MM-DD" (e.g. "2026-06-27").
Past dates are hidden automatically, and invalid/typo entries are ignored.
"""

from __future__ import annotations

from datetime import date, datetime

# ---------------------------------------------------------------------------
# EDIT ME: the list of pickup dates customers can choose from.
# Format: "YYYY-MM-DD". Order doesn't matter; duplicates and past dates are
# cleaned up automatically.
# ---------------------------------------------------------------------------
PICKUP_DATES = [
    "2026-06-27",
    "2026-07-25",
]


def _parsed_dates() -> list[date]:
    """Parse PICKUP_DATES into date objects, skipping any invalid entries."""
    out: list[date] = []
    for s in PICKUP_DATES:
        try:
            out.append(datetime.strptime(str(s).strip(), "%Y-%m-%d").date())
        except (ValueError, TypeError):
            continue
    return sorted(set(out))


def upcoming_pickup_dates(
    count: int | None = None, today: date | None = None
) -> list[date]:
    """Return configured pickup dates that haven't passed yet, sorted ascending.

    Pass `count` to cap how many are returned (default: all upcoming).
    """
    today = today or date.today()
    upcoming = [d for d in _parsed_dates() if d >= today]
    return upcoming[:count] if count else upcoming
