#!/bin/bash
# measure_diff_cov.sh — diff 기반 추가 코드 커버리지 측정
# 위치: .claude/skills/code-reviewer/scripts/measure_diff_cov.sh
# 용도: code-reviewer 스킬의 aim-coverage-analyst 에이전트가 사용
#
# 사용법:
#   bash measure_diff_cov.sh [BASE_BRANCH]
#   - BASE_BRANCH: 비교 기준 브랜치 (기본: rb_73)
#
# 전제 조건:
#   1. make gtest 실행 완료 (gcda 생성)
#   2. 필요 시 mock 바이너리 실행 완료 (gcda 합산)
#   3. /root/ofsrc/aim 에서 실행

cd /root/ofsrc/aim

BASE_BRANCH="${1:-rb_73}"

# 변경된 .c 파일 목록 자동 감지 (src/ 하위만)
FILES=$(git diff "${BASE_BRANCH}...HEAD" --diff-filter=AM --name-only -- 'src/**/*.c')

if [ -z "$FILES" ]; then
    echo "No changed .c files found in src/ (diff: ${BASE_BRANCH}...HEAD)"
    exit 0
fi

# gcov 파일 재생성
for f in $FILES; do
    dir=$(dirname "$f")
    base=$(basename "$f")
    if [ -d "$dir" ] && [ -f "$dir/${base%.c}.gcda" ]; then
        (cd "$dir" && gcov -b "$base" > /dev/null 2>&1)
    fi
done

TOTAL_COV=0
TOTAL_UNCOV=0

for f in $FILES; do
    dir=$(dirname "$f")
    base=$(basename "$f")
    gcov_file="$dir/${base}.gcov"

    [ ! -f "$gcov_file" ] && continue

    # diff에서 추가된 라인 번호 추출
    mapfile -t lines < <(git diff "${BASE_BRANCH}...HEAD" -U0 -- "$f" | awk '/^@@ .* \+[0-9]/ { match($3, /\+([0-9]+)(,([0-9]+))?/, a); s=a[1]+0; c=(a[3]!="")?a[3]+0:1; for(i=s;i<s+c;i++) print i }')

    cov=0
    uncov=0

    for lno in "${lines[@]}"; do
        # gcov 라인 매칭: 정확 매칭 필수 (부분 매칭 금지)
        match=$(awk -v n="$lno" 'BEGIN{found=0} $2 == n":" && $1 ~ /^[0-9]+:$/ {found=1; exit} $2 == n":" && $1 == "#####:" {found=2; exit} END{print found}' "$gcov_file")
        if [ "$match" = "1" ]; then
            cov=$((cov + 1))
        elif [ "$match" = "2" ]; then
            uncov=$((uncov + 1))
        fi
    done

    total=$((cov + uncov))
    if [ $total -gt 0 ]; then
        pct=$((cov * 100 / total))
        echo "$f: $cov/$total ($pct%)"
        TOTAL_COV=$((TOTAL_COV + cov))
        TOTAL_UNCOV=$((TOTAL_UNCOV + uncov))
    fi
done

TOTAL_ADD=$((TOTAL_COV + TOTAL_UNCOV))
if [ $TOTAL_ADD -gt 0 ]; then
    PCT=$((TOTAL_COV * 100 / TOTAL_ADD))
    echo ""
    echo "=== TOTAL (added code only) ==="
    echo "  Line: $TOTAL_COV/$TOTAL_ADD ($PCT%)"
    if [ $PCT -lt 80 ]; then
        echo "  WARNING: Coverage below 80% policy threshold"
    else
        echo "  OK: Coverage meets 80% policy threshold"
    fi
fi
