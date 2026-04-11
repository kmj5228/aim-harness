---
name: executing-plans-aim
description: Use when you have a written implementation plan to execute in the current session with build/test gate verification between steps
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks with TDD cycle and phase gates, report when complete.

**Note:** If subagents are available, prefer subagent-driven-development-aim for higher quality (fresh context per task, review between tasks). Use this skill for inline execution when subagents aren't needed or available.

## The Process

### Step 0: Verify Branch

```bash
dx git branch --show-current
```

If on `rb_73`, STOP. Create feature branch first (see using-feature-branches-aim).

### Step 1: Load and Review Plan

1. Read `../agent/prompt/<topic>/plan_tasks.md`
2. Review critically — identify questions or concerns
3. If concerns: Raise with user before starting
4. If no concerns: Proceed

### Step 2: Execute Tasks

For each task:

1. **Mark as in_progress** (TaskUpdate)
2. **Follow TDD cycle exactly:**
   - RED: Write failing gtest → `dx make gtest` (verify fails correctly)
   - GREEN: Write minimal C code → `dx make gtest` (verify passes)
   - REFACTOR: Clean up → `dx make gtest` (still green)
3. **Phase gate:**
   - `dx make gtest` — all tests pass
   - `dx make` — production build clean
4. **Commit:**
   ```bash
   dx git add <specific-files>
   dx git commit -F /tmp/commit_msg.txt
   ```
5. **Mark as completed** (TaskUpdate)

**REQUIRED SUB-SKILL:** Use test-driven-development-aim for the TDD cycle within each task.

### Step 3: Complete Development

After all tasks complete:

1. **Verify everything:**
   ```bash
   dx make gtest    # all tests pass
   dx make          # clean build
   ```
2. **Check coverage:**
   ```bash
   dx bash -c "cd /root/ofsrc/aim && ./script/measure_diff_cov.sh"
   ```
   Must be >= 80% on added code.

3. **Transition:** Use finishing-a-development-branch-aim to push, create MR.

## When to Stop and Ask

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails unexpectedly, instruction unclear)
- Plan has critical gaps
- You don't understand an instruction
- Verification fails after 3 attempts

**Ask for clarification rather than guessing.** Never apply workarounds to make tests pass.

## When to Revisit

**Return to Step 1 when:**
- User updates the plan
- Fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly (TDD: RED → GREEN → REFACTOR)
- **Plan TDD 위반 검사**: 실행 전에 plan을 검토하여 구현과 테스트가 별도 Task로 분리되어 있으면 사용자에게 경고하고 plan 수정을 제안한다. 구현/테스트 분리 plan을 그대로 실행하지 않는다.
- Don't skip phase gates (`dx make gtest` + `dx make`)
- Stop when blocked, don't guess
- Never commit to `rb_73`
- Korean commit messages via file (-F)

## Integration

**Required workflow skills:**
- **using-feature-branches-aim** — create branch before starting
- **test-driven-development-aim** — TDD cycle for each task
- **systematic-debugging-aim** — when tests fail unexpectedly
- **verification-before-completion-aim** — before claiming complete
- **finishing-a-development-branch-aim** — push, MR after all tasks
