---
name: subagent-driven-development-base
description: Use when executing an implementation plan with mostly independent tasks and you want a fresh subagent to implement each task with review between tasks
---

# Subagent-Driven Development

Execute a plan by dispatching a fresh implementer per task, then reviewing the result before moving to the next task.

**Why subagents:** Fresh context reduces anchoring, stale assumptions, and context pollution. Each implementer gets only the task-relevant context.

**Core principle:** Fresh implementer per task, followed by review before accepting the task.

## When to Use

- You have a written implementation plan
- Tasks are mostly independent or can be serialized cleanly
- You want stronger isolation and review than inline execution

**vs. executing-plans-base:** This skill uses fresh subagents per task. `executing-plans-base` executes inline in the current session.

## The Process

### Step 0: Verify Working Context

Before dispatching any implementer:

1. Confirm the repository is in the correct isolated branch or workspace if isolation is required
2. Confirm the plan file and current task order are correct
3. Raise plan issues before dispatching work

### Step 1: Load Plan

1. Read `../agent/prompt/<topic>/plan_tasks.md`
2. Extract all task text in executable order
3. Review critically and raise concerns before starting

### Step 2: Per Task Execution

For each task:

1. **Dispatch implementer subagent**
   - Provide full task text
   - Provide only the context needed for that task
   - Do not make the implementer reconstruct context from the whole session by default

2. **Handle implementer status**
   - `DONE` -> proceed to review
   - `DONE_WITH_CONCERNS` -> assess concerns, then review
   - `NEEDS_CONTEXT` -> provide missing context, then re-dispatch
   - `BLOCKED` -> escalate, break down the task, or refine the plan

3. **Run acceptance review**
   - Verify the implementation matches the task intent
   - Reject over-building, under-building, and requirement drift

4. **Run code quality review**
   - Check maintainability, test quality, compatibility with surrounding code, and repository conventions

5. **If review fails**
   - Re-dispatch the implementer with exact issues to fix
   - Require fresh verification after the fix
   - Re-review before accepting the task

6. **Mark task complete**

## Re-dispatch Rules

When sending a task back after review:

- Include the exact review findings
- State what must be fixed
- State what verification must be re-run
- Require `BLOCKED` instead of repeated guessing if the fix is unclear

If the required change needs real design judgment, re-dispatch.

If the change is a trivial mechanical correction, the main agent may handle it directly, but only if:
- The scope is clearly tiny
- No new design judgment is required
- Verification is re-run afterward

If in doubt, re-dispatch.

## Review Structure

Recommended review order:

1. **Task acceptance / spec compliance**
   - Did the implementer build the intended change?
   - Did they avoid unrelated work?

2. **Code quality**
   - Is the change understandable?
   - Are tests appropriate?
   - Does it fit repository conventions?

Do not start quality review before basic task acceptance passes.

## Context Curation

You are the filter between the plan and the implementer.

For each implementer:
- Provide the full task text
- Include relevant facts from earlier tasks
- Include renamed APIs, changed contracts, and shared assumptions
- Omit unrelated history

Never assume the subagent should discover everything from scratch if you already know what matters.

## Handling Implementer Status

| Status | Action |
|--------|--------|
| `DONE` | Proceed to review |
| `DONE_WITH_CONCERNS` | Assess concerns, then review |
| `NEEDS_CONTEXT` | Supply missing context, then re-dispatch |
| `BLOCKED` | Escalate, refine, or split the task |

Do not ignore escalation. Change the inputs before retrying.

## Red Flags

- Skipping review
- Proceeding with open review issues
- Dispatching parallel implementers on overlapping write scopes
- Making subagents reconstruct the whole plan from scratch without curated context
- Starting the next task while the current one still has unresolved review issues
- Repeating retries without changing context or task framing

## Integration

**Required:**
- **using-feature-branches-base** — when branch or workspace isolation is needed
- **test-driven-development-base** — implementers should follow TDD
- **verification-before-completion-base** — final verification before accepting completion
- **finishing-a-development-branch-base** — after all tasks complete

**Alternative / Related:**
- **executing-plans-base** — inline execution without subagents
- **dispatching-parallel-agents-base** — for truly independent parallel tasks
