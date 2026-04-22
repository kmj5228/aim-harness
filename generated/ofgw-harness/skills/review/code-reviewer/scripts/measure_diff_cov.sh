#!/usr/bin/env bash
#
# measure_diff_cov.sh
# OFGW repo-native diff-coverage helper
#
# Purpose:
#   - approximate added-line coverage for `ofgwSrc` using git diff + JaCoCo XML
#   - provide an extra review signal for changed backend code
#   - avoid reusing the AIM gcov workflow directly
#
# Important limits:
#   - this is an experimental helper, not the primary coverage contract
#   - the primary verified coverage path is still `:ofgwSrc:jacocoTestReport`
#   - this helper only reasons about `ofgwSrc/src/main/java` and `ofgwSrc/src/main/kotlin`
#   - this helper must not be used to claim coverage for `webterminal` or `ofgwAdmin`

set -euo pipefail

BASE_REF="${1:-}"
MODULE_ROOT="${2:-ofgwSrc}"
REPORT_XML="${3:-$MODULE_ROOT/build/reports/jacoco/test/jacocoTestReport.xml}"

if [[ -z "$BASE_REF" ]]; then
  echo "Usage: $0 <BASE_REF> [MODULE_ROOT] [REPORT_XML]" >&2
  echo "Example: $0 origin/7.3.21 ofgwSrc ofgwSrc/build/reports/jacoco/test/jacocoTestReport.xml" >&2
  exit 2
fi

if [[ ! -d "$MODULE_ROOT" ]]; then
  echo "Missing module root: $MODULE_ROOT" >&2
  exit 2
fi

if [[ ! -f "$REPORT_XML" ]]; then
  echo "Missing JaCoCo XML report: $REPORT_XML" >&2
  echo "Run the bound coverage command first:" >&2
  echo "  JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:jacocoTestReport --no-daemon" >&2
  exit 2
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This helper must run inside a git work tree." >&2
  exit 2
fi

TMP_JSON="$(mktemp)"
cleanup() {
  rm -f "$TMP_JSON"
}
trap cleanup EXIT

python3 - "$REPORT_XML" <<'PY' > "$TMP_JSON"
import json
import sys
import xml.etree.ElementTree as ET

report_xml = sys.argv[1]
tree = ET.parse(report_xml)
root = tree.getroot()

result = {}
for package in root.findall("package"):
    pkg_name = package.get("name", "").strip("/")
    for sourcefile in package.findall("sourcefile"):
        name = sourcefile.get("name")
        if not name:
            continue
        key = f"{pkg_name}/{name}" if pkg_name else name
        line_map = {}
        for line in sourcefile.findall("line"):
            nr = line.get("nr")
            mi = int(line.get("mi", "0"))
            ci = int(line.get("ci", "0"))
            if nr is None:
                continue
            line_map[int(nr)] = {"mi": mi, "ci": ci}
        result[key] = line_map

json.dump(result, sys.stdout)
PY

map_changed_lines() {
  local path="$1"
  git diff "${BASE_REF}...HEAD" -U0 -- "$path" \
    | awk '
      /^@@ / {
        split($3, plus, ",")
        sub(/^\+/, "", plus[1])
        start = plus[1] + 0
        count = 1
        if (plus[2] != "") count = plus[2] + 0
        for (i = 0; i < count; i++) print start + i
      }
    '
}

to_source_key() {
  local path="$1"
  path="${path#${MODULE_ROOT}/src/main/java/}"
  path="${path#${MODULE_ROOT}/src/main/kotlin/}"
  printf '%s\n' "$path"
}

FILES="$(git diff "${BASE_REF}...HEAD" --diff-filter=AM --name-only -- \
  "$MODULE_ROOT/src/main/java/**/*.java" \
  "$MODULE_ROOT/src/main/kotlin/**/*.kt" || true)"

if [[ -z "$FILES" ]]; then
  echo "No changed Java/Kotlin files found under $MODULE_ROOT/src/main (diff: ${BASE_REF}...HEAD)"
  exit 0
fi

TOTAL_COVERED=0
TOTAL_UNCOVERED=0

while IFS= read -r file; do
  [[ -z "$file" ]] && continue

  SOURCE_KEY="$(to_source_key "$file")"
  if [[ "$SOURCE_KEY" == "$file" ]]; then
    continue
  fi

  mapfile -t CHANGED_LINES < <(map_changed_lines "$file")
  [[ "${#CHANGED_LINES[@]}" -eq 0 ]] && continue

  RESULT="$(
    python3 - "$TMP_JSON" "$SOURCE_KEY" "${CHANGED_LINES[@]}" <<'PY'
import json
import sys

db_path = sys.argv[1]
source_key = sys.argv[2]
changed = [int(x) for x in sys.argv[3:]]

with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

entry = db.get(source_key)
if not entry:
    print("0 0 missing")
    sys.exit(0)

covered = 0
uncovered = 0
for line in changed:
    line_data = entry.get(str(line))
    if not line_data:
      continue
    ci = int(line_data.get("ci", 0))
    mi = int(line_data.get("mi", 0))
    if ci > 0:
        covered += 1
    elif mi > 0:
        uncovered += 1

print(f"{covered} {uncovered} ok")
PY
  )"

  COVERED="$(awk '{print $1}' <<<"$RESULT")"
  UNCOVERED="$(awk '{print $2}' <<<"$RESULT")"
  STATUS="$(awk '{print $3}' <<<"$RESULT")"

  if [[ "$STATUS" == "missing" ]]; then
    echo "$file: no matching sourcefile entry in JaCoCo XML"
    continue
  fi

  TOTAL=$((COVERED + UNCOVERED))
  if [[ "$TOTAL" -eq 0 ]]; then
    echo "$file: no executable added lines matched in JaCoCo XML"
    continue
  fi

  PCT=$((COVERED * 100 / TOTAL))
  echo "$file: $COVERED/$TOTAL ($PCT%)"
  TOTAL_COVERED=$((TOTAL_COVERED + COVERED))
  TOTAL_UNCOVERED=$((TOTAL_UNCOVERED + UNCOVERED))
done <<< "$FILES"

TOTAL_ADDED=$((TOTAL_COVERED + TOTAL_UNCOVERED))
if [[ "$TOTAL_ADDED" -eq 0 ]]; then
  echo ""
  echo "No executable added lines matched in JaCoCo XML for diff ${BASE_REF}...HEAD"
  exit 0
fi

TOTAL_PCT=$((TOTAL_COVERED * 100 / TOTAL_ADDED))
echo ""
echo "=== TOTAL (added executable lines in $MODULE_ROOT) ==="
echo "  Line: $TOTAL_COVERED/$TOTAL_ADDED ($TOTAL_PCT%)"
echo ""
echo "Interpretation:"
echo "- treat this as a review helper signal, not as the primary OFGW coverage contract"
echo "- primary coverage evidence still comes from :ofgwSrc:jacocoTestReport"
