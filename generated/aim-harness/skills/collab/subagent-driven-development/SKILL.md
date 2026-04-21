---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session, dispatching fresh subagent per task with review between tasks
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Why subagents:** Fresh context per task prevents context pollution (false assumptions, anchoring bias, context window saturation). You construct exactly what each subagent needs — they never inherit session history.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

- Have implementation plan (`plan_tasks.md`)
- Tasks are mostly independent
- Want review between each task

**vs. executing-plans:** This skill dispatches subagents (fresh context, higher quality). executing-plans executes inline (simpler, no subagent overhead).

## The Process

### Step 0: Verify Branch

Not on `rb_73`. If so, use using-feature-branches first.

### Step 1: Load Plan

1. Read `agent/<topic>/plan_tasks.md`
2. Extract all tasks with full text
3. Review critically — raise concerns with user before starting

### Step 2: Per Task

For each task:

1. **Dispatch implementer subagent** (./implementer-prompt.md)
   - Provide full task text + context (don't make subagent read files)
   - Include AIM rules: `dx` commands, header conventions, TDD cycle
2. **Handle status:**
   - DONE → proceed to review
   - DONE_WITH_CONCERNS → assess concerns, then review
   - NEEDS_CONTEXT → provide info, re-dispatch
   - BLOCKED → escalate (more context, capable model, or break down task)
3. **Spec compliance review** (./spec-reviewer-prompt.md)
   - Verify implementer built what was specified (nothing more, nothing less)
   - If issues → re-dispatch implementer (fix + **반드시 `dx make gtest` + `dx make` 재실행**) → re-review
4. **Code quality review** (./code-quality-reviewer-prompt.md)
   - Only after spec compliance passes
   - Check AIM conventions, test quality, maintainability
   - If issues → re-dispatch implementer (fix + **반드시 `dx make gtest` + `dx make` 재실행**) → re-review
5. **Mark task complete**

**재스폰 시 프롬프트 필수 항목** (리뷰 이슈 수정 시):
- 수정해야 할 이슈 목록 (리뷰어 리포트 발췌)
- "수정 후 반드시 **해당 모듈 테스트 + `dx make`** 재실행하여 검증 gate 통과 확인" (전체 `dx make gtest`는 Step 3 최종 gate에서만 수행)
- 검증 실패 시 BLOCKED 리포트 → 재리뷰 금지

**빌드 스코프 원칙 (시간 절약):**
- 태스크 중간(implementer 내부): 해당 모듈 테스트 바이너리만 빌드/실행
- 전체 `dx make gtest`(전 모듈 회귀)는 Step 3 최종 gate에서 **1회만** 수행
- 실측: 태스크당 빌드 4회(RED/GREEN/make/전체 gtest)가 누적되면 단일 태스크가 20분 이상 소요됨

**메인 에이전트 직접 수정 금지 (Trivial Fix 예외 있음):**
- 리뷰 FAIL 시 **원칙적으로 implementer 재스폰**. 메인이 직접 수정하면 re-dispatch 강제 규칙을 우회하게 된다.
- **Trivial Fix 예외**: 1~2줄 상수/에러코드 교체 같은 순수 기계적 수정은 메인이 처리 가능. 단 수정 후 반드시 `dx make` + 해당 모듈 테스트 재실행.
- 판단 기준: "수정에 판단이 필요한가?" → YES면 재스폰. "기계적 치환인가?" → OK.
- 애매하면 재스폰 쪽으로.

### Step 3: Finish

After all tasks:
1. Dispatch final reviewer for entire implementation
2. Use finishing-a-development-branch

## Context Curation

**You are the "intelligent filter."** For each subagent:

- Provide full task text from plan (never just "see plan file")
- Include relevant context from previous tasks (renames, API changes, globals)
- Record Phase-spanning facts in plan.md for future reference
- Strip unnecessary history — subagent needs only what's relevant to their task

## Handling Implementer Status

| Status | Action |
|--------|--------|
| DONE | Proceed to spec review |
| DONE_WITH_CONCERNS | Assess concerns, then review |
| NEEDS_CONTEXT | Provide missing info, re-dispatch |
| BLOCKED | Escalate: more context, better model, or break task down |

**Never** ignore escalation or retry without changes.

## Prompt Templates

- `./implementer-prompt.md` — implementer subagent
- `./spec-reviewer-prompt.md` — spec compliance reviewer
- `./code-quality-reviewer-prompt.md` — code quality reviewer

## Red Flags

**Never:**
- Commit to `rb_73`
- Skip reviews (spec OR quality)
- Proceed with unfixed issues
- Dispatch parallel implementers (conflicts)
- Make subagent read plan file (provide full text)
- Skip context curation (subagent needs AIM rules)
- Ignore subagent questions
- Start code quality review before spec compliance passes
- Move to next task with open review issues
- **리뷰 FAIL → 메인이 직접 수정** (원칙: implementer 재스폰. 예외는 trivial fix 1~2줄 기계적 치환)
- **태스크 중간에 전체 `dx make gtest` 실행** (해당 모듈 테스트만. 전체는 최종 1회)

## Integration

**Required:**
- **using-feature-branches** — branch before starting
- **test-driven-development** — subagents follow TDD
- **Plan TDD 위반 검사**: 실행 전에 plan을 검토하여 구현과 테스트가 별도 Task로 분리되어 있으면 사용자에게 경고하고 plan 수정을 제안한다. 구현/테스트 분리 plan을 그대로 실행하지 않는다.
- **finishing-a-development-branch** — after all tasks

**Alternative:**
- **executing-plans** — inline execution without subagents
- **dispatching-parallel-agents** — for truly independent parallel tasks
