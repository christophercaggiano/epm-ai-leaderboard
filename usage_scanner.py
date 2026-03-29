"""Scan Claude Code logs and other signals to measure actual automation usage."""
from __future__ import annotations

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def scan_claude_code_logs(
    log_dir: str = os.path.expanduser("~/logs"),
    pattern: str = "merchant-refresh-*.log",
) -> list[dict]:
    """Parse Claude Code log files and extract run metadata."""
    log_path = Path(log_dir)
    if not log_path.exists():
        return []

    runs = []
    for f in sorted(log_path.glob(pattern)):
        text = f.read_text()
        run = _parse_log(f.name, text)
        if run:
            runs.append(run)

    return runs


def _parse_log(filename: str, text: str) -> Optional[dict]:
    started = None
    finished = None
    exit_code = None
    merchants_updated = 0
    merchants_no_change = 0
    merchant_names = []

    for line in text.splitlines():
        if line.startswith("Started:"):
            started = _parse_timestamp(line.replace("Started:", "").strip())
        elif line.startswith("Finished:"):
            finished = _parse_timestamp(line.replace("Finished:", "").strip())
        elif line.startswith("Exit code:"):
            try:
                exit_code = int(line.split(":")[1].strip())
            except ValueError:
                exit_code = -1

    merchant_blocks = re.findall(r"###\s+(.+?)[\s(]", text)
    for name in merchant_blocks:
        clean = name.strip("`").strip()
        if clean and clean not in ("Refresh", "Summary"):
            merchant_names.append(clean)

    updates_found = re.findall(r"(\d+)\s+updates?\s+made", text)
    merchants_updated = len(updates_found)
    no_change_hits = re.findall(r"No significant new context found", text)
    merchants_no_change = len(no_change_hits)

    if merchants_updated == 0 and "New additions" in text:
        merchants_updated = len(re.findall(r"New additions", text))

    duration_minutes = None
    if started and finished:
        delta = finished - started
        duration_minutes = round(delta.total_seconds() / 60, 1)

    return {
        "filename": filename,
        "started": started.isoformat() if started else None,
        "finished": finished.isoformat() if finished else None,
        "duration_minutes": duration_minutes,
        "exit_code": exit_code,
        "success": exit_code == 0,
        "merchants_processed": len(merchant_names),
        "merchants_updated": merchants_updated,
        "merchants_no_change": merchants_no_change,
        "merchant_names": merchant_names,
    }


def _parse_timestamp(ts: str) -> Optional[datetime]:
    formats = [
        "%a %b %d %H:%M:%S %Z %Y",
        "%a %b %d %H:%M:%S %Y",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue

    cleaned = re.sub(r"\s[A-Z]{3,4}\s", " ", ts)
    for fmt in ["%a %b %d %H:%M:%S %Y"]:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue

    return None


def compute_actuals(
    runs: list[dict],
    time_saved_per_run_minutes: float = 40.0,
) -> dict:
    """Roll up log scan results into actual usage metrics."""
    if not runs:
        return {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_merchants_updated": 0,
            "avg_duration_minutes": 0,
            "total_actual_time_saved_hrs": 0,
            "runs_this_week": 0,
            "runs_this_month": 0,
            "first_run": None,
            "last_run": None,
            "runs": [],
        }

    successful = [r for r in runs if r["success"]]
    failed = [r for r in runs if not r["success"]]

    durations = [r["duration_minutes"] for r in runs if r["duration_minutes"]]
    avg_dur = sum(durations) / len(durations) if durations else 0

    total_saved = len(successful) * (time_saved_per_run_minutes / 60)

    now = datetime.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    runs_this_week = 0
    runs_this_month = 0
    for r in runs:
        if r["started"]:
            try:
                dt = datetime.fromisoformat(r["started"])
                if dt >= week_ago:
                    runs_this_week += 1
                if dt >= month_ago:
                    runs_this_month += 1
            except (ValueError, TypeError):
                pass

    total_merchants = sum(r["merchants_updated"] for r in successful)

    dates = []
    for r in runs:
        if r["started"]:
            try:
                dates.append(datetime.fromisoformat(r["started"]))
            except (ValueError, TypeError):
                pass

    return {
        "total_runs": len(runs),
        "successful_runs": len(successful),
        "failed_runs": len(failed),
        "total_merchants_updated": total_merchants,
        "avg_duration_minutes": round(avg_dur, 1),
        "total_actual_time_saved_hrs": round(total_saved, 1),
        "runs_this_week": runs_this_week,
        "runs_this_month": runs_this_month,
        "first_run": min(dates).isoformat() if dates else None,
        "last_run": max(dates).isoformat() if dates else None,
        "runs": runs,
    }
