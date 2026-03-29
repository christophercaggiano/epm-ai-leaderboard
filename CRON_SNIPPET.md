# Auto-Log to Team Tracker

Add this to the end of any Claude Code automation script (before the final `exit`) to automatically log usage to the team dashboard.

Replace `YOUR_NAME` with your name exactly as it appears in the Google Form dropdown.

```bash
# ── Auto-log to EPM AI Usage Tracker ──
FORM_URL="https://docs.google.com/forms/d/e/1FAIpQLScd6SMZOD-UPYY3qHtv-5KJOSooPQsstpJnuxMacv6DAxymqA/formResponse"
MY_NAME="YOUR_NAME"           # e.g., "Tucker Moody"
SOP_NAME="YOUR_SOP_NAME"     # e.g., "Automated Merchant Context File Refresh"
MINUTES_SAVED=40              # How many minutes of manual work this replaces

curl -s -o /dev/null "$FORM_URL" \
  --data-urlencode "entry.323d6310=${MY_NAME}" \
  --data-urlencode "entry.6f613e48=${SOP_NAME}" \
  --data-urlencode "entry.769328a6=${MINUTES_SAVED}" \
  --data-urlencode "entry.071dfaee=Auto-logged from cron $(date '+%Y-%m-%d %H:%M')" \
  && echo "Logged to team tracker"
```

## How it works

- The `curl` command submits a response to the shared Google Form
- No authentication needed -- the form is open
- Responses automatically appear in the Google Sheet and the team dashboard
- Each cron run = one form submission = one tracked data point

## Form field IDs (for reference)

| Field | Entry ID |
|---|---|
| Your Name | entry.323d6310 |
| SOP Name | entry.6f613e48 |
| Minutes Saved | entry.769328a6 |
| Notes | entry.071dfaee |

## SOP name options (must match exactly)

- Automated Merchant Context File Refresh
- Mission Control Weekly Reporting
- Meeting Prep Brief Generator
- Weekly QBR Prep
- Merchant Performance Recap Email
- Escalation Summary
- Contract Review Prep
- Other
