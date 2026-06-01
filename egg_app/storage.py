"""Local CSV data layer. No external services required.

Two CSV files live in a `data/` folder next to the app: customers and orders.
Phone number is the dedupe key for customers.
"""

from __future__ import annotations

import csv
import re
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CUSTOMERS_HEADERS = ["phone", "name", "first_seen"]
ORDERS_HEADERS = [
    "order_id",
    "phone",
    "name",
    "trays",
    "dozens",
    "total_eggs",
    "total_price",
    "pickup_date",
    "created_at",
    "status",
]
_FILES = {
    "customers": CUSTOMERS_HEADERS,
    "orders": ORDERS_HEADERS,
}


def normalize_phone(raw: str, default_country: str = "1") -> str | None:
    """Normalize a phone number to a simple E.164-ish form (+<digits>).

    Returns None if it doesn't look like a valid number.
    """
    if not raw:
        return None
    digits = re.sub(r"[^\d+]", "", raw.strip())
    if digits.startswith("+"):
        digits = "+" + re.sub(r"\D", "", digits[1:])
        return digits if len(digits) >= 11 else None
    digits = re.sub(r"\D", "", digits)
    if len(digits) == 10:
        return f"+{default_country}{digits}"
    if len(digits) == 11 and digits.startswith(default_country):
        return f"+{digits}"
    return None


def _path(name: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(_FILES[name])
    return path


def _append_row(name: str, row: list) -> None:
    with _path(name).open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)


def save_records(name: str, rows: list[dict]) -> None:
    """Overwrite a CSV file with the given rows (header order preserved)."""
    headers = _FILES[name]
    with _path(name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})
    _clear_cache()


@st.cache_data(ttl=30, show_spinner=False)
def get_records(name: str) -> list[dict]:
    """Return all rows of a CSV file as a list of dicts (header-keyed)."""
    with _path(name).open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _clear_cache() -> None:
    get_records.clear()


def get_customer(phone: str) -> dict | None:
    for row in get_records("customers"):
        if str(row.get("phone")) == phone:
            return row
    return None


def upsert_customer(phone: str, name: str) -> None:
    """Insert the customer if new (dedupe on phone)."""
    if get_customer(phone):
        return
    _append_row(
        "customers", [phone, name, datetime.now().isoformat(timespec="seconds")]
    )
    _clear_cache()


def order_count(phone: str) -> int:
    return sum(1 for row in get_records("orders") if str(row.get("phone")) == phone)


def add_order(
    *,
    phone: str,
    name: str,
    trays: int,
    dozens: int,
    total_eggs: int,
    total_price: int,
    pickup_date: str,
) -> str:
    """Append an order row and return its order_id."""
    order_id = uuid.uuid4().hex[:8]
    _append_row(
        "orders",
        [
            order_id,
            phone,
            name,
            trays,
            dozens,
            total_eggs,
            total_price,
            pickup_date,
            datetime.now().isoformat(timespec="seconds"),
            "pending",
        ],
    )
    _clear_cache()
    return order_id
