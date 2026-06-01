"""Farm Fresh Egg App package."""


PRICE_TRAY = 20
PRICE_DOZEN = 10
EGGS_PER_TRAY = 30
EGGS_PER_DOZEN = 12

# Pickup details are read from .streamlit/secrets.toml (which is gitignored),
# so the real address never lives in the repo. These are safe fallbacks used
# only when secrets aren't configured.
DEFAULT_PICKUP_LOCATION = "Address shared after you order"
DEFAULT_PICKUP_TIME = "7:00 PM"


def pickup_location() -> str:
    """Pickup address from secrets, falling back to a safe placeholder."""
    try:
        import streamlit as st

        return st.secrets.get("pickup_location") or DEFAULT_PICKUP_LOCATION
    except Exception:
        return DEFAULT_PICKUP_LOCATION


def pickup_time() -> str:
    """Pickup time from secrets, falling back to a safe default."""
    try:
        import streamlit as st

        return st.secrets.get("pickup_time") or DEFAULT_PICKUP_TIME
    except Exception:
        return DEFAULT_PICKUP_TIME


def order_totals(trays: int, dozens: int) -> tuple[int, int]:
    """Return (total_eggs, total_price) for a given number of trays and dozens."""
    total_eggs = trays * EGGS_PER_TRAY + dozens * EGGS_PER_DOZEN
    total_price = trays * PRICE_TRAY + dozens * PRICE_DOZEN
    return total_eggs, total_price
