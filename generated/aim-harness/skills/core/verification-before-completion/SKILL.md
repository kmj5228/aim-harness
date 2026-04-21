---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing - requires running verification commands and confirming output before making any success claims
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## AIM Verification Commands

| Claim | Command | Evidence Required |
|-------|---------|-------------------|
| Tests pass | `dx tmdown -y && dx make gtest` | Output: 0 failures |
| Build succeeds | `dx make` | Output: exit 0, no errors |
| Coverage meets 80% | `dx bash -c "cd /root/ofsrc/aim && bash skills/review/code-reviewer/scripts/measure_diff_cov.sh"` | Output: >= 80% |
| Code formatted | `clang-format -i <files>` then `dx git diff` | No diff |
| Bug fixed | Failing gtest now passes | RED→GREEN verified |

**전체 `dx make gtest`는 이 스킬에서 1회만 수행한다.** 각 태스크 중간에 반복 실행하지 말 것 — 모듈 전체 재컴파일이 누적되어 전체 소요 시간의 40% 이상을 차지한다. 태스크 중간 검증은 test-driven-development 가이드에 따라 해당 모듈 테스트만 실행한다.

**`dx tmdown -y` 필수:** 실행 중인 서버 바이너리가 `Text file busy` 에러를 유발한다. `tmdown -s <server>` 개별 종료는 의존 서버가 많아 불완전하므로 `-y`(전체)를 사용한다.

**미커버 라인 식별:** `gcov`를 직접 `grep`/`awk`로 파싱하지 말 것 (메타데이터 5줄만 출력되는 재현성 있는 현상). `measure_diff_cov.sh` 출력 + `dx git diff --unified=0 <base>..HEAD` 조합으로 확인한다.

## Common Failures

| Claim | Not Sufficient |
|-------|----------------|
| "Tests pass" | Previous run, "should pass" |
| "Build clean" | Tests passing (tests != build) |
| "Bug fixed" | Code changed, assumed fixed |
| "Coverage OK" | "I added enough tests" without measuring |
| "Ready for MR" | Tests pass but coverage not checked |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Done!", "Perfect!")
- About to commit/push without verification
- Relying on partial verification
- Thinking "just this once"
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence != evidence |
| "Just this once" | No exceptions |
| "Tests passed, build must be fine" | Tests != build. Run both. |
| "I added tests, coverage is fine" | Measure it. Don't guess. |

## Full Verification Sequence

Before claiming ANY work complete (모든 태스크 완료 후 1회):

```bash
# 0. 실행 중인 서버 종료 (Text file busy 방지)
dx tmdown -y

# 1. All tests pass (전체 회귀는 여기서 1회)
dx make gtest

# 2. Production build clean
dx make

# 3. Coverage meets threshold (if new code added)
dx bash -c "cd /root/ofsrc/aim && bash skills/review/code-reviewer/scripts/measure_diff_cov.sh"

# 4. Code formatted
# (verify no unformatted changes)
```

**All 3 (or 4) must pass. Partial is not complete.**

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

## Integration

**Called by:**
- **executing-plans** — 태스크 완료 주장 전
- **subagent-driven-development** — implementer 서브에이전트 내부 완료 전
- **systematic-debugging** — 수정 완료 전
- **finishing-a-development-branch** — 브랜치 완료 전 gate
- **dispatching-parallel-agents** — 에이전트 완료 후 통합 검증
