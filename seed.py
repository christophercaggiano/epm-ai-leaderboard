"""Seed the tracker with sample SOPs for demo purposes."""
from store import add_sop, load_sops, save_sops

SEED_SOPS = [
    {
        "name": "Automated Merchant Context File Refresh",
        "team_size": 40,
        "sop_text": "Automated weekly refresh of merchant context files using Claude Code CLI...",
        "grading_result": {
            "summary": "Automates weekly merchant context file updates by scheduling Claude Code to search Glean and Slack for new information and append findings to local context.md files — replacing a manual research-and-update process.",
            "scores": {
                "clarity": 9,
                "completeness": 9,
                "reproducibility": 8,
                "automation_potential": 9,
                "documentation_quality": 9,
            },
            "time_before_minutes": 45,
            "time_after_minutes": 5,
            "frequency_per_week": 1,
            "improvements": [
                "Add a validation step that checks context.md files for formatting consistency after each refresh",
                "Include a rollback procedure in case Claude introduces incorrect information",
                "Add a summary notification (Slack or email) after each run with a diff of what changed",
            ],
        },
    },
    {
        "name": "Mission Control Weekly Reporting",
        "team_size": 40,
        "sop_text": "Weekly merchant performance reporting via Mission Control dashboard...",
        "grading_result": {
            "summary": "Generates weekly merchant performance reports by pulling data from multiple dashboards, synthesizing into narrative format, and distributing to stakeholders — currently a highly manual copy/paste/write workflow.",
            "scores": {
                "clarity": 7,
                "completeness": 6,
                "reproducibility": 6,
                "automation_potential": 8,
                "documentation_quality": 6,
            },
            "time_before_minutes": 150,
            "time_after_minutes": 20,
            "frequency_per_week": 1,
            "improvements": [
                "Document the exact data sources and dashboard URLs for each metric to improve reproducibility",
                "Add a standard output template so all EPMs produce consistent reports",
                "Include screenshots or screen recordings of the current manual workflow for training purposes",
            ],
        },
    },
    {
        "name": "Meeting Prep Brief Generator",
        "team_size": 40,
        "sop_text": "Automated meeting prep using Cursor with Calendar, Slack, and Glean MCPs...",
        "grading_result": {
            "summary": "Uses Cursor + MCPs to pull calendar context, recent Slack threads, and Glean docs to auto-generate a 1-page meeting prep brief for upcoming merchant meetings.",
            "scores": {
                "clarity": 8,
                "completeness": 7,
                "reproducibility": 8,
                "automation_potential": 9,
                "documentation_quality": 7,
            },
            "time_before_minutes": 30,
            "time_after_minutes": 5,
            "frequency_per_week": 4,
            "improvements": [
                "Add merchant-specific prompt templates for different meeting types (QBR, escalation, onboarding)",
                "Include a section on how to handle meetings with no prior Slack/Glean context",
                "Document expected output format with a real before/after example",
            ],
        },
    },
]


def seed():
    existing = load_sops()
    existing_names = {s["name"] for s in existing}

    added = 0
    for sop in SEED_SOPS:
        if sop["name"] not in existing_names:
            add_sop(sop["name"], sop["team_size"], sop["grading_result"], sop["sop_text"])
            added += 1
            print(f"  Added: {sop['name']}")

    if added == 0:
        print("  Seed data already present, no changes.")
    else:
        print(f"  Seeded {added} SOPs.")


if __name__ == "__main__":
    seed()
