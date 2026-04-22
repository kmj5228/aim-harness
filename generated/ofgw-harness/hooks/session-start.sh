#!/usr/bin/env bash
# SessionStart hook for the generated ofgw-harness.

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
session_context="You are in the generated ofgw-harness.\n\nThis startup contract applies on startup, resume, clear, and compact events.\nRead and follow the full AGENTS.md below before improvising workflow.\n\n${agents_escaped}"

printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$session_context"
