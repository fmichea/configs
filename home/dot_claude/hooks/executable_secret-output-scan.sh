#!/bin/bash
# ~/.claude/hooks/secret-output-scan.sh
# PostToolUse hook for Bash. Reads JSON on stdin, emits JSON on stdout.

INPUT=$(cat)
OUTPUT=$(printf '%s' "$INPUT" \
  | jq -r '[.tool_response.stdout // "", .tool_response.stderr // "", .tool_response.output // "", .tool_response.content // ""] | join("\n")' \
  | head -c 1048576)

[ -z "$OUTPUT" ] && exit 0

PATTERNS=(
  'sk-ant-[a-zA-Z0-9_-]{20,}'
  'sk-[a-zA-Z0-9]{40,}'
  'sk_live_[a-zA-Z0-9]{20,}'
  'ghp_[a-zA-Z0-9]{30,}'
  'gho_[a-zA-Z0-9]{30,}'
  'github_pat_[a-zA-Z0-9_]{60,}'
  'AKIA[0-9A-Z]{16}'
  'ASIA[0-9A-Z]{16}'
  'xox[bpors]-[a-zA-Z0-9-]{20,}'
  'SG\.[a-zA-Z0-9_.-]{60,}'
  'eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
)

HITS=""
for pattern in "${PATTERNS[@]}"; do
  if printf '%s' "$OUTPUT" | grep -qE -e "$pattern"; then
    HITS="${HITS}- ${pattern}"$'\n'
  fi
done

if [ -n "$HITS" ]; then
  REASON=$(printf "Possible secret(s) detected in tool output:\n%b\nClaude already saw this. Rotate immediately if real." "$HITS")
  printf '%s' "$REASON" | jq -Rs '{systemMessage:.}'
fi
exit 0
