#!/usr/bin/env bash
# Append a row to the shared EPM AI Usage Tracker after each cron run.
# Add this to the end of refresh-merchants.sh (before the final exit).
#
# Requirements: gsheet CLI or curl + Google Sheets API.
# Simplest approach: use the Streamlit app's team logger via a POST,
# or paste the snippet below into refresh-merchants.sh.
#
# ── SNIPPET TO ADD TO ~/scripts/refresh-merchants.sh ──
# (paste just before the final "exit $EXIT_CODE" line)
#
# --- START SNIPPET ---
#
# # Auto-log to team tracker
# PERSON="$(whoami)"
# SOP_NAME="Merchant Context Refresh"
# MINUTES_SAVED=40
# TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"
#
# # Count merchants from the log
# MERCHANTS_PROCESSED=$(grep -c '###' "$LOG_FILE" 2>/dev/null || echo 0)
# MERCHANTS_UPDATED=$(grep -c 'updates\? made\|New additions' "$LOG_FILE" 2>/dev/null || echo 0)
#
# # Calculate duration
# if [ -n "$START_TIME" ] && [ -n "$END_TIME" ]; then
#   DURATION=$(( (END_TIME - START_TIME) / 60 ))
# else
#   DURATION="?"
# fi
#
# STATUS="Success"
# [ "$EXIT_CODE" -ne 0 ] && STATUS="Failed"
#
# # Append to the shared JSON tracker (works if dashboard is accessible)
# cd ~/sop-value-tracker && source venv/bin/activate 2>/dev/null
# python3 -c "
# from team import log_usage
# log_usage(
#     person='${PERSON}',
#     sop_name='${SOP_NAME}',
#     minutes_saved=${MINUTES_SAVED},
#     notes='${MERCHANTS_PROCESSED} merchants, ${MERCHANTS_UPDATED} updated, ${DURATION}m runtime'
# )
# print('Logged to team tracker')
# " 2>&1 | tee -a "$LOG_FILE"
#
# --- END SNIPPET ---

echo "This file contains the snippet to add to refresh-merchants.sh."
echo "See the comments above for instructions."
