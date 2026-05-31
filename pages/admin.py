"""Password-gated admin view: orders + per-pickup rollups (editable).

Reachable at /admin. Hidden from the customer-facing page navigation via
.streamlit/config.toml (client.showSidebarNavigation = false).
"""

from __future__ import annotations

import csv
import io
from collections import defaultdict

import streamlit as st

from egg_app import EGGS_PER_DOZEN, EGGS_PER_TRAY, PRICE_DOZEN, PRICE_TRAY, storage, styles

STATUS_OPTIONS = ["pending", "confirmed", "picked_up", "cancelled"]

st.set_page_config(page_title="Egg App · Admin", page_icon="🥚", layout="wide")
styles.inject()
styles.title("Admin")


def _check_password() -> bool:
    expected = st.secrets.get("admin_password")
    if not expected:
        st.error("No admin_password set in secrets.toml.")
        return False
    if st.session_state.get("admin_ok"):
        return True
    pwd = st.text_input("Admin password", type="password")
    if pwd:
        if pwd == expected:
            st.session_state["admin_ok"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    return False


if not _check_password():
    st.stop()

_, top_r = st.columns([3, 1])
with top_r:
    if st.button("🔄 Refresh"):
        storage.get_records.clear()
        st.rerun()
    if st.button("🚪 Log out"):
        st.session_state.pop("admin_ok", None)
        st.rerun()

orders = storage.get_records("orders")

if not orders:
    st.info("No orders yet.")
    st.stop()


def _ints(rows: list[dict]) -> list[dict]:
    """Coerce numeric columns (CSV stores everything as strings)."""
    out = []
    for r in rows:
        r = dict(r)
        for col in ("trays", "dozens", "total_eggs", "total_price"):
            r[col] = int(r.get(col) or 0)
        out.append(r)
    return out


orders = _ints(orders)

styles.section("Pickup rollups")

rollup: dict[str, dict[str, int]] = defaultdict(
    lambda: {"trays": 0, "dozens": 0, "total_eggs": 0, "total_price": 0, "orders": 0}
)
for o in orders:
    key = str(o.get("pickup_date", "—"))
    r = rollup[key]
    r["trays"] += o["trays"]
    r["dozens"] += o["dozens"]
    r["total_eggs"] += o["total_eggs"]
    r["total_price"] += o["total_price"]
    r["orders"] += 1

rollup_rows = [
    {
        "Pickup date": k,
        "Orders": v["orders"],
        "Trays": v["trays"],
        "Dozens": v["dozens"],
        "Total eggs": v["total_eggs"],
        "Revenue ($)": v["total_price"],
    }
    for k, v in rollup.items()
]
st.dataframe(rollup_rows, use_container_width=True, hide_index=True)

c1, c2, c3 = st.columns(3)
c1.metric("Total orders", len(orders))
c2.metric("Total eggs", sum(o["total_eggs"] for o in orders))
c3.metric("Total revenue", f"${sum(o['total_price'] for o in orders)}")

styles.section("Orders")

pickup_dates = sorted({str(o.get("pickup_date", "—")) for o in orders})
chosen = st.selectbox("Filter by pickup date", ["All dates"] + pickup_dates)
visible = orders if chosen == "All dates" else [
    o for o in orders if str(o.get("pickup_date")) == chosen
]

st.caption(
    "Edit status or quantities inline, tick rows and press ⌫ to delete, then "
    "**Save changes**. Totals recalculate on save."
)

edited = st.data_editor(
    visible,
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    column_config={
        "order_id": st.column_config.TextColumn("order_id", disabled=True),
        "total_eggs": st.column_config.NumberColumn("total_eggs", disabled=True),
        "total_price": st.column_config.NumberColumn("total_price", disabled=True),
        "created_at": st.column_config.TextColumn("created_at", disabled=True),
        "status": st.column_config.SelectboxColumn("status", options=STATUS_OPTIONS),
    },
    key="orders_editor",
)

save_col, dl_col = st.columns(2)

with save_col:
    if st.button("💾 Save changes", type="primary"):
        # Recompute derived totals for the edited (visible) rows.
        for r in edited:
            trays = int(r.get("trays") or 0)
            dozens = int(r.get("dozens") or 0)
            r["trays"] = trays
            r["dozens"] = dozens
            r["total_eggs"] = trays * EGGS_PER_TRAY + dozens * EGGS_PER_DOZEN
            r["total_price"] = trays * PRICE_TRAY + dozens * PRICE_DOZEN
        # Merge edits back: keep rows outside the current filter untouched.
        if chosen == "All dates":
            merged = edited
        else:
            merged = [o for o in orders if str(o.get("pickup_date")) != chosen]
            merged += edited
        storage.save_records("orders", merged)
        st.success("Saved.")
        st.rerun()

with dl_col:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=storage.ORDERS_HEADERS, extrasaction="ignore")
    writer.writeheader()
    for r in visible:
        writer.writerow(r)
    fname = "orders.csv" if chosen == "All dates" else f"orders_{chosen}.csv"
    st.download_button(
        "⬇️ Download CSV", buf.getvalue(), file_name=fname, mime="text/csv"
    )
