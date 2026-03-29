"""Read team usage data from Google Sheets (form responses + manual tracker).

Data flows:
1. Team fills out the Google Form → responses land in a Google Sheet
2. Cron scripts POST to the same form → auto-logged
3. This module reads the published sheet CSV → feeds the dashboard

No auth required — the sheet just needs to be published to web.
"""
from __future__ import annotations

import csv
import io
import urllib.request
from datetime import datetime

FORM_RESPONSES_SHEET_ID = "1hFuFWt4xxukWyM1-ZiqkbJNNnhDw3HIvABWklIRNExw"
MANUAL_TRACKER_SHEET_ID = "1m-o1j571k60W5lJeUtGhhhZqdtHOCrdQN1csVeRlCK0"


def _published_csv_url(sheet_id: str, gid: int = 0) -> str:
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"


def _fetch_csv(url: str, timeout: int = 10) -> list[dict]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SOPTracker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        return list(reader)
    except Exception:
        return []


def fetch_form_responses() -> list[dict]:
    """Fetch responses from the Google Form response sheet.

    The form response sheet has columns:
    Timestamp, Your Name, Which SOP / automation did you use?, Minutes saved, Notes (optional)
    """
    url = _published_csv_url(FORM_RESPONSES_SHEET_ID)
    rows = _fetch_csv(url)

    entries = []
    for row in rows:
        timestamp = row.get("Timestamp", "")
        person = row.get("Your Name", "")
        sop = row.get("Which SOP / automation did you use?", "")
        minutes_str = row.get("Minutes saved", "0")
        notes = row.get("Notes (optional)", "")

        if not person or not sop:
            continue

        try:
            minutes = float(minutes_str)
        except (ValueError, TypeError):
            minutes = 0

        entries.append({
            "source": "google_form",
            "timestamp": timestamp,
            "person": person,
            "sop_name": sop,
            "minutes_saved": minutes,
            "notes": notes,
        })

    return entries


def fetch_manual_tracker() -> list[dict]:
    """Fetch rows from the manual EPM AI Usage Tracker sheet.

    Columns: Timestamp, Person, SOP Name, Minutes Saved, Merchants Processed,
             Merchants Updated, Duration (min), Status, Notes
    """
    url = _published_csv_url(MANUAL_TRACKER_SHEET_ID)
    rows = _fetch_csv(url)

    entries = []
    for row in rows:
        person = row.get("Person", "")
        sop = row.get("SOP Name", "")
        minutes_str = row.get("Minutes Saved", "0")
        status = row.get("Status", "")
        notes = row.get("Notes", "")
        timestamp = row.get("Timestamp", "")

        if not person or not sop:
            continue

        try:
            minutes = float(minutes_str)
        except (ValueError, TypeError):
            minutes = 0

        entries.append({
            "source": "manual_sheet",
            "timestamp": timestamp,
            "person": person,
            "sop_name": sop,
            "minutes_saved": minutes,
            "notes": f"{status}: {notes}" if status else notes,
        })

    return entries


def fetch_all_remote_usage() -> list[dict]:
    """Combine all remote usage sources into a single list."""
    form = fetch_form_responses()
    manual = fetch_manual_tracker()
    return form + manual
