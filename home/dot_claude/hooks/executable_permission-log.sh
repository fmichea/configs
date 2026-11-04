#!/bin/bash
# ~/.claude/hooks/permission-log.sh
# PermissionRequest hook. Appends the request to a JSONL log and prints nothing,
# so Claude Code still shows the permission prompt.

LOG_FILE="${CLAUDE_PERMISSION_LOG:-$HOME/.claude/permission-log.jsonl}"

jq --compact-output --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '{ts: $ts} + .' >> "$LOG_FILE" 2>/dev/null
exit 0
