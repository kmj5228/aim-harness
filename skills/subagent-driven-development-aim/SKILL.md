---
name: subagent-driven-development-aim
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

**vs. executing-plans-aim:** This skill dispatches subagents (fresh context, higher quality). executing-plans-aim executes inline (simpler, no subagent overhead).

## The Process

### Step 0: Verify Branch

Not on `rb_73`. If so, use using-feature-branches-aim first.

### Step 1: Load Plan

1. Read `../agent/prompt/<topic>/plan_tasks.md`
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
   - If issues → implementer fixes → re-review
4. **Code quality review** (./code-quality-reviewer-prompt.md)
   - Only after spec compliance passes
   - Check AIM conventions, test quality, maintainability
   - If issues → implementer fixes → re-review
5. **Mark task complete**

### Step 3: Finish

After all tasks:
1. Dispatch final reviewer for entire implementation
2. Use finishing-a-development-branch-aim

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

## Integration

**Required:**
- **using-feature-branches-aim** — branch before starting
- **test-driven-development-aim** — subagents follow TDD
- **Plan TDD 위반 검사**: 실행 전에 plan을 검토하여 구현과 테스트가 별도 Task로 분리되어 있으면 사용자에게 경고하고 plan 수정을 제안한다. 구현/테스트 분리 plan을 그대로 실행하지 않는다.
- **finishing-a-development-branch-aim** — after all tasks

**Alternative:**
- **executing-plans-aim** — inline execution without subagents
- **dispatching-parallel-agents-aim** — for truly independent parallel tasks
