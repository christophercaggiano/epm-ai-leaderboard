"""Team roster and usage log for team-wide tracking."""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "team_usage.json"

ROSTER = [
    # NYC
    {"name": "Chris Caggiano", "location": "NYC", "role": "Lead"},
    {"name": "Dan Sheetz", "location": "NYC", "role": "Captain"},
    {"name": "Samuel Bunis", "location": "NYC", "role": "Captain"},
    {"name": "Lee Hofman", "location": "NYC", "role": "Captain"},
    {"name": "Tucker Moody", "location": "NYC", "role": "Captain"},
    {"name": "Alex Kalman", "location": "NYC", "role": "EPM"},
    {"name": "Clara Kennedy", "location": "NYC", "role": "EPM"},
    {"name": "Diana Weisz", "location": "NYC", "role": "EPM"},
    {"name": "Elie Shields", "location": "NYC", "role": "EPM"},
    {"name": "Emily Peck", "location": "NYC", "role": "EPM"},
    {"name": "Holly Santero", "location": "NYC", "role": "EPM"},
    {"name": "Jackson Wikstrom", "location": "NYC", "role": "EPM"},
    {"name": "Jovonnie Gonzales", "location": "NYC", "role": "EPM"},
    {"name": "Julie Kesselhaut", "location": "NYC", "role": "EPM"},
    {"name": "Laura Cohen", "location": "NYC", "role": "EPM"},
    {"name": "Rachel Weinbren", "location": "NYC", "role": "EPM"},
    {"name": "Robert Jablonski", "location": "NYC", "role": "EPM"},
    {"name": "Charles Shoener", "location": "NYC", "role": "EPM"},
    {"name": "Dabney Villasenor", "location": "NYC", "role": "EPM"},
    {"name": "Samantha Berlin", "location": "NYC", "role": "EPM"},
    {"name": "Paige Cammalleri", "location": "NYC", "role": "EPM"},
    # Canada
    {"name": "Luka Raspopovic", "location": "Toronto", "role": "Captain"},
    {"name": "Maria Bou-assi", "location": "Toronto", "role": "EPM"},
    {"name": "Kevin Nguyen", "location": "Toronto", "role": "EPM"},
    {"name": "Jay Sim", "location": "Vancouver (Virtual)", "role": "EPM"},
    {"name": "Vedansh Wadhwa", "location": "Vancouver (Virtual)", "role": "EPM"},
    {"name": "Nathan Linton", "location": "Vancouver (Virtual)", "role": "EPM"},
    # Tex-cago
    {"name": "Brady Wilson", "location": "Tex-cago", "role": "Captain"},
    {"name": "Daksha Potnis", "location": "Tex-cago", "role": "EPM"},
    {"name": "Kolin Smialek", "location": "Tex-cago", "role": "EPM"},
    {"name": "Chase Cochrane", "location": "Tex-cago (Virtual)", "role": "EPM"},
    {"name": "Emily Goldstein", "location": "Tex-cago", "role": "EPM"},
    {"name": "Bridget Carlson", "location": "Tex-cago", "role": "EPM"},
    # Rocky Mountains
    {"name": "Danielle Walworth", "location": "Rocky Mountains", "role": "Captain"},
    {"name": "Gregory Sergakis", "location": "Rocky Mountains", "role": "EPM"},
    {"name": "Anum Qamar", "location": "Rocky Mountains", "role": "EPM"},
    {"name": "Olivia Sammak", "location": "Rocky Mountains", "role": "EPM"},
    {"name": "Erica Morrin", "location": "Rocky Mountains", "role": "EPM"},
    # PST/Remote
    {"name": "Calvin Neumeyer", "location": "SF/PST", "role": "Captain"},
    {"name": "Rene Bright", "location": "PST/Remote", "role": "EPM"},
    {"name": "Connor Christensen", "location": "PST/Remote", "role": "EPM"},
    {"name": "Haley Schlatter", "location": "PST/Remote", "role": "EPM"},
    {"name": "Jordan Pontelandolfo", "location": "PST/Remote", "role": "EPM"},
    {"name": "Elizabeth Simmons", "location": "PST/Remote", "role": "EPM"},
]

TEAM_NAMES = sorted([m["name"] for m in ROSTER])
LOCATIONS = sorted(set(m["location"] for m in ROSTER))


def _ensure():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]")


def load_usage_logs() -> list[dict]:
    _ensure()
    return json.loads(DATA_FILE.read_text())


def save_usage_logs(logs: list[dict]):
    _ensure()
    DATA_FILE.write_text(json.dumps(logs, indent=2, default=str))


def log_usage(
    person: str,
    sop_name: str,
    minutes_saved: float,
    notes: str = "",
) -> dict:
    logs = load_usage_logs()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "person": person,
        "sop_name": sop_name,
        "minutes_saved": minutes_saved,
        "notes": notes,
        "timestamp": datetime.now().isoformat(),
    }
    logs.append(entry)
    save_usage_logs(logs)
    return entry


def delete_usage_log(log_id: str):
    logs = load_usage_logs()
    logs = [l for l in logs if l["id"] != log_id]
    save_usage_logs(logs)


def get_team_metrics(logs: list[dict]) -> dict:
    if not logs:
        return {
            "total_logs": 0,
            "unique_people": 0,
            "total_minutes_saved": 0,
            "total_hours_saved": 0,
            "top_savers": [],
            "top_sops": [],
            "by_person": {},
            "by_sop": {},
            "by_location": {},
        }

    by_person: dict[str, float] = {}
    by_sop: dict[str, float] = {}
    for l in logs:
        by_person[l["person"]] = by_person.get(l["person"], 0) + l["minutes_saved"]
        by_sop[l["sop_name"]] = by_sop.get(l["sop_name"], 0) + l["minutes_saved"]

    by_location: dict[str, float] = {}
    person_to_loc = {m["name"]: m["location"] for m in ROSTER}
    for person, mins in by_person.items():
        loc = person_to_loc.get(person, "Unknown")
        by_location[loc] = by_location.get(loc, 0) + mins

    total_mins = sum(l["minutes_saved"] for l in logs)
    top_savers = sorted(by_person.items(), key=lambda x: x[1], reverse=True)[:10]
    top_sops = sorted(by_sop.items(), key=lambda x: x[1], reverse=True)[:10]

    roster_set = {m["name"] for m in ROSTER}
    active_people = {l["person"] for l in logs if l["person"] in roster_set}

    return {
        "total_logs": len(logs),
        "unique_people": len(active_people),
        "total_roster": len(ROSTER),
        "adoption_pct": round(len(active_people) / len(ROSTER) * 100) if ROSTER else 0,
        "total_minutes_saved": round(total_mins, 1),
        "total_hours_saved": round(total_mins / 60, 1),
        "top_savers": top_savers,
        "top_sops": top_sops,
        "by_person": by_person,
        "by_sop": by_sop,
        "by_location": by_location,
    }
