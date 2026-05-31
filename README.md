# 🥚 Farm Fresh Egg App

A simple Streamlit pre-order app for farm-fresh eggs. Customers enter their
name, phone, and quantity; pickup details are confirmed in-app and via a
(stubbed) SMS. Pickup is the **last Saturday of each month, 7:00 PM @ Science
World**.

## Products


| Option | Eggs | Price |
| ------ | ---- | ----- |
| Tray   | 30   | $20   |
| Dozen  | 12   | $10   |


## Setup

1. **Install dependencies**
  ```bash
   pip install -r requirements.txt
  ```
2. **Set the admin password.** Copy the example and edit it:
  ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
  ```
   `secrets.toml` is gitignored — never commit it.
3. **Run**
  ```bash
   streamlit run app.py
  ```

That's it — no external accounts or services needed.

## Data

Orders, customers, and messages are stored as plain CSV files in a local
`data/` folder, created automatically on first order:

- `data/customers.csv`
- `data/orders.csv`
- `data/messages.csv` (stubbed SMS log)

`data/` is gitignored so customer info isn't committed.

## Admin

The admin page is hidden from the customer navigation. Reach it directly by
adding `/admin` to the app URL (e.g. `http://localhost:8501/admin`), then enter
your `admin_password`. From there you can view, **edit, and delete** orders in
a table, filter by pickup date, download CSV, and see per-pickup rollups
(trays, dozens, total eggs, revenue).

## SMS

SMS is currently **stubbed** — messages are logged to `data/messages.csv`
instead of being sent. The `send_sms(to, body)` interface in `egg_app/sms.py`
matches what a Twilio client needs, so wiring in real SMS later is a
one-function change.

## Project structure

```text
egg_app/
├── app.py                  # customer order flow
├── pages/admin.py          # password-gated admin view (served at /admin)
├── egg_app/
│   ├── __init__.py         # constants + pricing helpers
│   ├── storage.py          # local CSV data layer
│   ├── dates.py            # last-Saturday-of-month logic
│   ├── sms.py              # stubbed SMS (Twilio-ready signature)
│   └── styles.py           # poster-inspired theme/CSS
├── .streamlit/
│   ├── config.toml         # base theme
│   └── secrets.toml        # admin password (gitignored)
└── requirements.txt
```

> Referral tracking is intentionally deferred; the schema leaves room to add a
> `referred_by` column and a referral network graph later.

