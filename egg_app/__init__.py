"""Farm Fresh Egg App package."""

PICKUP_LOCATION = "Science World"
PICKUP_TIME = "7:00 PM"

PRICE_TRAY = 20
PRICE_DOZEN = 10
EGGS_PER_TRAY = 30
EGGS_PER_DOZEN = 12


def order_totals(trays: int, dozens: int) -> tuple[int, int]:
    """Return (total_eggs, total_price) for a given number of trays and dozens."""
    total_eggs = trays * EGGS_PER_TRAY + dozens * EGGS_PER_DOZEN
    total_price = trays * PRICE_TRAY + dozens * PRICE_DOZEN
    return total_eggs, total_price
