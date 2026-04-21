---
name: executing-plans-base
description: Use when you have a written implementation plan to execute in the current session with build/test gate verification between steps
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks with TDD cycle and phase gates, report when complete.

**Note:** If subagents are available, prefer subagent-driven-development-base for higher quality (fresh context per task, review between tasks). Use this skill for inline execution when subagents aren't needed or available.

## The Process

### Step 0: Verify Working Context

1. Check the current branch or workspace state if the repository uses branch-based workflow
2. Confirm the plan file and target files are the ones you intend to change
3. If branch setup or workspace isolation is required, use using-feature-branches-base before starting

### Step 1: Load and Review Plan

1. Read the `implementation_plan` artifact from the current topic artifact workspace
2. Review critically — identify questions or concerns
3. If concerns: Raise with user before starting
4. If no concerns: Proceed

### Step 2: Execute Tasks

For each task:

1. **Mark as in_progress** (TaskUpdate)
2. **Follow TDD cycle exactly**:
   - RED: Write or enable a failing test that proves the behavior gap
   - GREEN: Write the minimal implementation to pass
   - REFACTOR: Clean up while keeping tests green
3. **Phase gate (태스크 단위):**
   - Run targeted verification for the files or component changed in the task
   - Run the broader verification command required by the repository for task-level confidence
4. **Checkpoint or commit:**
   - Stage only the files relevant to the task
   - Use the repository's commit/checkpoint style
5. **Mark as completed** (TaskUpdate)

**REQUIRED SUB-SKILL:** Use test-driven-development-base for the TDD cycle within each task.

### Step 3: Complete Development

After all tasks complete:

1. **Run final verification** using verification-before-completion-base
2. **Review repository state** and confirm only intended files changed
3. **Transition:** Use finishing-a-development-branch-base for branch cleanup, push, review, or merge preparation as appropriate

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
- Don't skip phase gates
- Stop when blocked, don't guess
- Use repository-specific branch and commit rules, not assumptions

## Integration

**Required workflow skills:**
- **using-feature-branches-base** — when branch setup or isolated workspace is needed
- **test-driven-development-base** — TDD cycle for each task
- **systematic-debugging-base** — when tests fail unexpectedly
- **verification-before-completion-base** — before claiming complete
- **finishing-a-development-branch-base** — finalize branch/review workflow after all tasks
