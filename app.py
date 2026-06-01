"""Farm Fresh Egg App - customer pre-order flow."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from egg_app import (
    EGGS_PER_DOZEN,
    EGGS_PER_TRAY,
    PRICE_DOZEN,
    PRICE_TRAY,
    order_totals,
    pickup_location,
    pickup_time,
)
from egg_app import dates, storage, styles

TRAY_IMG = Path(__file__).parent / "img" / "tray_eggs_image.png"

PICKUP_LOCATION = pickup_location()
PICKUP_TIME = pickup_time()

st.set_page_config(page_title="Farm Fresh Eggs", page_icon="🥚", layout="centered")
styles.inject()

styles.badge()
styles.title("Abbotsford Farm Fresh Eggs")
styles.subtitle("Free-range · Veggie fed · Pre-order now")


def _fmt_date(d) -> str:
    return d.strftime("%A, %B %-d, %Y")


pickup_options = dates.upcoming_pickup_dates()

if st.session_state.get("order_confirmed"):
    o = st.session_state["last_order"]
    styles.section("You're all set! 🎉")
    if o.get("product") == "tray" and TRAY_IMG.exists():
        st.image(str(TRAY_IMG), use_container_width=True)
    st.markdown(
        f"""
<div class="egg-card">
<b>Order #{o['order_id']}</b><br>
{o['summary']}<br>
<span class="egg-price">${o['total_price']} · {o['total_eggs']} eggs</span><br><br>
📍 Pickup: <b>{PICKUP_LOCATION}</b> at <b>{PICKUP_TIME}</b><br>
🗓️ {o['pickup_date']}<br>
💵 <b>Cash preferred</b> at pickup<br><br>
Your order is saved. See you at pickup, {o['name']}! 🥚
</div>
""",
        unsafe_allow_html=True,
    )
    if o.get("returning"):
        st.info(f"Welcome back! This is order #{o['count']} for your number. 🥚")
    if st.button("Place another order"):
        st.session_state.pop("order_confirmed", None)
        st.session_state.pop("last_order", None)
        st.session_state.pop("product", None)
        st.rerun()
    st.stop()


styles.section("Choose your eggs")

product = st.session_state.get("product")


def _option(col, key: str, emoji: str, name: str, eggs: int, price: int, best: bool):
    selected = product == key
    check = "✓ " if selected else ""
    best_line = "\n\n⭐ BEST VALUE" if best else ""
    label = f"{emoji}\n\n{check}**{name}**\n\n{eggs} eggs · \\${price}{best_line}"
    with col:
        if st.button(label, key=f"pick_{key}", use_container_width=True):
            st.session_state["product"] = key
            st.rerun()


c1, c2 = st.columns(2)
_option(c1, "tray", "🥚", "Tray", EGGS_PER_TRAY, PRICE_TRAY, best=True)
_option(c2, "dozen", "🥚", "Dozen", EGGS_PER_DOZEN, PRICE_DOZEN, best=False)
styles.option_state(product)

if not product:
    st.caption("👆 Tap an option to continue.")
    st.stop()

is_tray = product == "tray"
unit_label = "Tray" if is_tray else "Dozen"
unit_eggs = EGGS_PER_TRAY if is_tray else EGGS_PER_DOZEN

if not pickup_options:
    st.warning("No pickup dates are available right now — please check back soon! 🥚")
    st.stop()

styles.section("Your details")

with st.form("order_form"):
    qty = st.number_input(
        f"How many {unit_label.lower()}s?", min_value=1, max_value=50, value=1, step=1
    )
    name = st.text_input("Your name")
    phone = st.text_input("Mobile number", placeholder="(555) 123-4567")

    pickup = st.selectbox("Pickup date", options=pickup_options, format_func=_fmt_date)
    st.caption(f"All pickups: {PICKUP_LOCATION} at {PICKUP_TIME}. 💵 Cash preferred.")

    submitted = st.form_submit_button("🥚 Confirm order")

if st.button("← Change selection"):
    st.session_state.pop("product", None)
    st.rerun()

if submitted:
    norm_phone = storage.normalize_phone(phone)
    errors = []
    if not name.strip():
        errors.append("Please enter your name.")
    if not norm_phone:
        errors.append("Please enter a valid mobile number.")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    trays = int(qty) if is_tray else 0
    dozens = int(qty) if not is_tray else 0
    total_eggs, total_price = order_totals(trays, dozens)
    pickup_str = _fmt_date(pickup)
    summary = f"{int(qty)} {unit_label.lower()}{'s' if qty != 1 else ''} ({unit_eggs * int(qty)} eggs)"

    try:
        storage.upsert_customer(norm_phone, name.strip())
        order_id = storage.add_order(
            phone=norm_phone,
            name=name.strip(),
            trays=trays,
            dozens=dozens,
            total_eggs=total_eggs,
            total_price=total_price,
            pickup_date=pickup_str,
        )
        count = storage.order_count(norm_phone)
    except Exception as exc:  # noqa: BLE001
        st.error(
            "Sorry, we couldn't save your order. Please try again in a moment."
        )
        st.caption(f"Details: {exc}")
        st.stop()

    st.session_state["order_confirmed"] = True
    st.session_state["last_order"] = {
        "order_id": order_id,
        "name": name.strip(),
        "phone": norm_phone,
        "product": product,
        "summary": summary,
        "total_eggs": total_eggs,
        "total_price": total_price,
        "pickup_date": pickup_str,
        "count": count,
        "returning": count > 1,
    }
    st.rerun()
