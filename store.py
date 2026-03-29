from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "sops.json"


def _ensure_data_dir():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]")


def load_sops() -> list[dict]:
    _ensure_data_dir()
    return json.loads(DATA_FILE.read_text())


def save_sops(sops: list[dict]):
    _ensure_data_dir()
    DATA_FILE.write_text(json.dumps(sops, indent=2, default=str))


def add_sop(name: str, team_size: int, grading_result: dict, sop_text: str = "", built_by: str = "") -> dict:
    sops = load_sops()

    time_saved_per_occ = grading_result["time_before_minutes"] - grading_result["time_after_minutes"]
    freq = grading_result["frequency_per_week"]

    weekly_savings_hrs = (time_saved_per_occ * freq) / 60
    weekly_team_savings_hrs = weekly_savings_hrs * team_size
    annual_team_savings_hrs = weekly_team_savings_hrs * 50

    scores = grading_result["scores"]
    overall_grade = sum(scores.values()) / len(scores)

    entry = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "built_by": built_by,
        "summary": grading_result.get("summary", ""),
        "date_added": datetime.now().isoformat(),
        "scores": scores,
        "overall_grade": round(overall_grade, 1),
        "time_before_minutes": grading_result["time_before_minutes"],
        "time_after_minutes": grading_result["time_after_minutes"],
        "frequency_per_week": freq,
        "team_size": team_size,
        "weekly_savings_per_person_hrs": round(weekly_savings_hrs, 1),
        "weekly_team_savings_hrs": round(weekly_team_savings_hrs, 1),
        "annual_team_savings_hrs": round(annual_team_savings_hrs, 0),
        "improvements": grading_result.get("improvements", []),
        "sop_text": sop_text[:500] + "..." if len(sop_text) > 500 else sop_text,
    }

    sops.append(entry)
    save_sops(sops)
    return entry


def delete_sop(sop_id: str):
    sops = load_sops()
    sops = [s for s in sops if s["id"] != sop_id]
    save_sops(sops)


def get_portfolio_metrics(sops: list[dict]) -> dict:
    if not sops:
        return {
            "total_sops": 0,
            "avg_grade": 0,
            "total_weekly_hrs": 0,
            "total_annual_hrs": 0,
            "total_people_impacted": 0,
            "highest_value_sop": None,
            "lowest_grade_sop": None,
        }

    total_weekly = sum(s["weekly_team_savings_hrs"] for s in sops)
    total_annual = sum(s["annual_team_savings_hrs"] for s in sops)
    avg_grade = sum(s["overall_grade"] for s in sops) / len(sops)
    people = max(s["team_size"] for s in sops)

    highest_value = max(sops, key=lambda s: s["annual_team_savings_hrs"])
    lowest_grade = min(sops, key=lambda s: s["overall_grade"])

    return {
        "total_sops": len(sops),
        "avg_grade": round(avg_grade, 1),
        "total_weekly_hrs": round(total_weekly, 1),
        "total_annual_hrs": round(total_annual, 0),
        "total_people_impacted": people,
        "highest_value_sop": highest_value["name"],
        "lowest_grade_sop": lowest_grade["name"],
    }
