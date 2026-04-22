#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "usage: $0 <generated-harness-dir> <target-repo-dir>" >&2
    exit 1
fi

SOURCE_DIR="$(cd "$1" && pwd)"
TARGET_REPO="$(cd "$2" && pwd)"
PRODUCT_NAME="$(basename "$SOURCE_DIR")"
PRODUCT_NAME="${PRODUCT_NAME%-harness}"

if [ ! -d "${SOURCE_DIR}/skills" ]; then
    echo "missing generated skills directory: ${SOURCE_DIR}/skills" >&2
    exit 1
fi

TARGET_SKILLS_DIR="${TARGET_REPO}/.agents/skills"
TARGET_CODEX_DIR="${TARGET_REPO}/.codex"
TARGET_PRODUCT_CODEX_DIR="${TARGET_CODEX_DIR}/${PRODUCT_NAME}-harness"
TARGET_HOOKS_DIR="${TARGET_CODEX_DIR}/hooks"
ROOT_AGENTS_PATH="${TARGET_REPO}/AGENTS.md"

mkdir -p "${TARGET_SKILLS_DIR}" "${TARGET_PRODUCT_CODEX_DIR}" "${TARGET_HOOKS_DIR}" "${TARGET_REPO}/agent" "${TARGET_REPO}/generated/manual"

while IFS= read -r SKILL_DIR; do
    SKILL_NAME="$(basename "$SKILL_DIR")"
    TARGET_SKILL_DIR="${TARGET_SKILLS_DIR}/${SKILL_NAME}"
    if [ -e "${TARGET_SKILL_DIR}" ]; then
        echo "install collision: ${TARGET_SKILL_DIR} already exists" >&2
        exit 1
    fi
    cp -R "${SKILL_DIR}" "${TARGET_SKILL_DIR}"
done < <(find "${SOURCE_DIR}/skills" -mindepth 2 -maxdepth 2 -type d | sort)

STARTUP_CONTRACT_PATH=""
if [ -e "${ROOT_AGENTS_PATH}" ]; then
    cp "${SOURCE_DIR}/AGENTS.md" "${TARGET_PRODUCT_CODEX_DIR}/AGENTS.md"
    STARTUP_CONTRACT_PATH="${TARGET_PRODUCT_CODEX_DIR}/AGENTS.md"
    echo "AGENTS collision: keeping existing ${ROOT_AGENTS_PATH} and installing harness contract to ${STARTUP_CONTRACT_PATH}"
else
    cp "${SOURCE_DIR}/AGENTS.md" "${ROOT_AGENTS_PATH}"
    STARTUP_CONTRACT_PATH="${ROOT_AGENTS_PATH}"
fi

cp "${SOURCE_DIR}/hooks/config.toml" "${TARGET_CODEX_DIR}/config.toml"
cp "${SOURCE_DIR}/hooks/hooks.json" "${TARGET_HOOKS_DIR}/hooks.json"
cp "${SOURCE_DIR}/hooks/session-start.sh" "${TARGET_HOOKS_DIR}/session-start.sh"

cp "${SOURCE_DIR}/agent/README.md" "${TARGET_REPO}/agent/README.md"
cp "${SOURCE_DIR}/generated/manual/README.md" "${TARGET_REPO}/generated/manual/README.md"

sed -i "s|\$(git rev-parse --show-toplevel)/hooks/session-start.sh|\$(git rev-parse --show-toplevel)/.codex/hooks/session-start.sh|g" "${TARGET_HOOKS_DIR}/hooks.json"
sed -i "s|ROOT_DIR|CODEX_DIR|g" "${TARGET_HOOKS_DIR}/session-start.sh"
sed -i "s|generated ${PRODUCT_NAME}-harness|installed ${PRODUCT_NAME}-harness|g" "${TARGET_HOOKS_DIR}/session-start.sh"
sed -i "s|generated AGENTS.md|installed ${PRODUCT_NAME}-harness AGENTS.md|g" "${TARGET_HOOKS_DIR}/session-start.sh"

if [ "${STARTUP_CONTRACT_PATH}" = "${ROOT_AGENTS_PATH}" ]; then
    sed -i '/^agents_content=/i REPO_DIR="$(cd "${CODEX_DIR}/.." && pwd)"' "${TARGET_HOOKS_DIR}/session-start.sh"
    sed -i 's|cat "${CODEX_DIR}/AGENTS.md"|cat "${REPO_DIR}/AGENTS.md"|g' "${TARGET_HOOKS_DIR}/session-start.sh"
else
    sed -i "s|\\\${CODEX_DIR}/AGENTS.md|\\\${CODEX_DIR}/${PRODUCT_NAME}-harness/AGENTS.md|g" "${TARGET_HOOKS_DIR}/session-start.sh"
fi

echo "Installed ${PRODUCT_NAME}-harness into ${TARGET_REPO}"
echo "Skills: ${TARGET_SKILLS_DIR}"
echo "Startup contract: ${STARTUP_CONTRACT_PATH}"
echo "Hooks: ${TARGET_HOOKS_DIR}"
