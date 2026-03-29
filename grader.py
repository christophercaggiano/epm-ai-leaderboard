from __future__ import annotations

import html
import json
import os
import re
from anthropic import Anthropic


def _strip_html(text: str) -> str:
    """Safety net: strip any residual HTML that slipped past the UI cleaner."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

GRADING_PROMPT = """You are an SOP quality analyst. Grade the following SOP on these 5 dimensions, each scored 1-10:

1. **Clarity** - Is the language precise and unambiguous? Could a new team member follow it without asking questions?
2. **Completeness** - Does it cover prerequisites, step-by-step instructions, edge cases, and troubleshooting?
3. **Reproducibility** - Could someone execute this independently and get the same result every time?
4. **Automation Potential** - How much of this workflow is (or could be) automated vs. manual?
5. **Documentation Quality** - Is it well-structured with headers, examples, and formatting that aids scanning?

Also provide:
- A 2-3 sentence **summary** of what this SOP does
- A **time_before_minutes** estimate: how long (in minutes) the manual version of this task takes per occurrence
- A **time_after_minutes** estimate: how long it takes with the SOP's automation in place
- A **frequency_per_week** estimate: how often this task occurs per person per week
- 3 specific **improvement suggestions** to raise the lowest scores

Respond ONLY with valid JSON in this exact format:
{
  "summary": "...",
  "scores": {
    "clarity": 8,
    "completeness": 9,
    "reproducibility": 7,
    "automation_potential": 8,
    "documentation_quality": 8
  },
  "time_before_minutes": 60,
  "time_after_minutes": 10,
  "frequency_per_week": 1,
  "improvements": [
    "...",
    "...",
    "..."
  ]
}

SOP TO GRADE:
"""


def grade_sop(sop_text: str, api_key: str | None = None) -> dict:
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("No API key provided. Set ANTHROPIC_API_KEY or pass api_key.")

    cleaned = _strip_html(sop_text)

    client = Anthropic(api_key=key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": GRADING_PROMPT + cleaned}],
    )

    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


def grade_sop_manual(scores: dict, meta: dict) -> dict:
    return {
        "summary": meta.get("summary", ""),
        "scores": scores,
        "time_before_minutes": meta.get("time_before_minutes", 0),
        "time_after_minutes": meta.get("time_after_minutes", 0),
        "frequency_per_week": meta.get("frequency_per_week", 0),
        "improvements": meta.get("improvements", []),
    }
