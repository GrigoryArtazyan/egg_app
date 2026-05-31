"""Farm Fresh Egg App - customer pre-order flow."""

from __future__ import annotations

import streamlit as st

from egg_app import (
    EGGS_PER_DOZEN,
    EGGS_PER_TRAY,
    PICKUP_LOCATION,
    PICKUP_TIME,
    PRICE_DOZEN,
    PRICE_TRAY,
    order_totals,
)
from egg_app import dates, sms, storage, styles

st.set_page_config(page_title="Farm Fresh Eggs", page_icon="🥚", layout="centered")
styles.inject()

styles.badge()
styles.title("Abbotsford Farm Fresh Eggs")
styles.subtitle("Free-range · Veggie fed · Pre-order now")


def _fmt_date(d) -> str:
    return d.strftime("%A, %B %-d, %Y")


pickup_options = dates.upcoming_pickup_dates(count=4)

if st.session_state.get("order_confirmed"):
    o = st.session_state["last_order"]
    styles.section("You're all set! 🎉")
    st.markdown(
        f"""
<div class="egg-card">
<b>Order #{o['order_id']}</b><br>
{o['summary']}<br>
<span class="egg-price">${o['total_price']} · {o['total_eggs']} eggs</span><br><br>
📍 Pickup: <b>{PICKUP_LOCATION}</b> at <b>{PICKUP_TIME}</b><br>
🗓️ {o['pickup_date']}<br>
💵 <b>Cash preferred</b> at pickup<br><br>
We'll text <b>{o['phone']}</b> with the details. Thanks, {o['name']}!
</div>
""",
        unsafe_allow_html=True,
    )
    if o.get("returning"):
        st.info(f"Welcome back! This is order #{o['count']} for your number. 🥚")
    if st.button("Place another order"):
        st.session_state.pop("order_confirmed", None)
        st.session_state.pop("last_order", None)
        st.rerun()
    st.stop()


styles.section("Choose your eggs")
st.markdown(
    f"""
<div class="egg-card">
🥚 <b>Tray</b> — {EGGS_PER_TRAY} eggs · <span class="egg-price">${PRICE_TRAY}</span>
&nbsp;&nbsp;<i>(best value)</i><br>
🥚 <b>Dozen</b> — {EGGS_PER_DOZEN} eggs · <span class="egg-price">${PRICE_DOZEN}</span>
</div>
""",
    unsafe_allow_html=True,
)

with st.form("order_form"):
    name = st.text_input("Your name")
    phone = st.text_input("Mobile number", placeholder="(555) 123-4567")

    c1, c2 = st.columns(2)
    with c1:
        trays = st.number_input(
            "Trays (30 eggs)", min_value=0, max_value=50, value=0, step=1
        )
    with c2:
        dozens = st.number_input(
            "Dozens (12 eggs)", min_value=0, max_value=50, value=0, step=1
        )

    pickup = st.selectbox(
        "Pickup date", options=pickup_options, format_func=_fmt_date
    )
    st.caption(f"All pickups: {PICKUP_LOCATION} at {PICKUP_TIME}. 💵 Cash preferred.")

    submitted = st.form_submit_button("🥚 Pre-order now")

if submitted:
    norm_phone = storage.normalize_phone(phone)
    errors = []
    if not name.strip():
        errors.append("Please enter your name.")
    if not norm_phone:
        errors.append("Please enter a valid mobile number.")
    if int(trays) == 0 and int(dozens) == 0:
        errors.append("Add at least one tray or dozen.")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    total_eggs, total_price = order_totals(int(trays), int(dozens))
    pickup_str = _fmt_date(pickup)
    summary_parts = []
    if int(trays):
        summary_parts.append(f"{int(trays)} tray{'s' if trays != 1 else ''}")
    if int(dozens):
        summary_parts.append(f"{int(dozens)} dozen")
    summary = " + ".join(summary_parts)

    try:
        storage.upsert_customer(norm_phone, name.strip())
        order_id = storage.add_order(
            phone=norm_phone,
            name=name.strip(),
            trays=int(trays),
            dozens=int(dozens),
            total_eggs=total_eggs,
            total_price=total_price,
            pickup_date=pickup_str,
        )
        count = storage.order_count(norm_phone)
        sms.send_sms(
            norm_phone,
            f"Hi {name.strip()}! Order #{order_id} confirmed: {summary} "
            f"(${total_price}). Pickup {pickup_str} at {PICKUP_TIME}, "
            f"{PICKUP_LOCATION}. See you there! 🥚",
        )
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
        "summary": summary,
        "total_eggs": total_eggs,
        "total_price": total_price,
        "pickup_date": pickup_str,
        "count": count,
        "returning": count > 1,
    }
    st.rerun()
