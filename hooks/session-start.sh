#!/usr/bin/env bash
# SessionStart hook source for Codex.
# This file lives under `hooks/` as repository source-of-truth.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${SCRIPT_DIR}/../skills" && pwd)"

skill_content=$(cat "${SKILLS_DIR}/using-base-harness/SKILL.md" 2>&1 || echo "Error reading using-base-harness skill")

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

skill_escaped=$(escape_for_json "$skill_content")
session_context="You have base-harness skills.\n\nBelow is the full content of the 'using-base-harness' meta skill. For all other skills, use the Skill tool.\n\n${skill_escaped}"

printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$session_context"
