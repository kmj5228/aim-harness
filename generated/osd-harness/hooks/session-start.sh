#!/usr/bin/env bash
# SessionStart hook for the generated osd-harness.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

agents_content=$(cat "${ROOT_DIR}/AGENTS.md" 2>&1 || echo "Error reading generated AGENTS.md")

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

agents_escaped=$(escape_for_json "$agents_content")
session_context="You are in the generated osd-harness.\n\nBelow is the full content of AGENTS.md for this harness.\n\n${agents_escaped}"

printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$session_context"
