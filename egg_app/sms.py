"""Stubbed SMS sending.

The signature matches what a real Twilio client will need (`to`, `body`),
so swapping in Twilio later is a one-function change. For now, messages are
logged to the `messages` worksheet and returned for display.
"""

from __future__ import annotations

from datetime import datetime

from . import storage


def send_sms(to: str, body: str) -> dict:
    """Pretend to send an SMS. Logs the message and returns the record."""
    record = {
        "to": to,
        "body": body,
        "sent_at": datetime.now().isoformat(timespec="seconds"),
    }
    try:
        storage.append_message(record)
    except Exception:
        # Never let logging failures break the order flow.
        pass
    return record
