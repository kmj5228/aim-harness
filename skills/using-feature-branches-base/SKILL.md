---
name: using-feature-branches-base
description: Use when starting implementation work that should be isolated from the main branch, shared branch, or current workspace before coding or committing
---

# Using Feature Branches

## Overview

Implementation work should happen in an isolated branch or workspace when the repository relies on branch-based collaboration.

**Core principle:** Do not commit directly to the branch that other people treat as the shared baseline.

## When to Use

- Starting a new feature, fix, or refactor
- About to commit while still on a shared branch
- Need to isolate experimental work
- Before executing an implementation plan

## The Rule

```text
DO NOT COMMIT DIRECTLY TO THE SHARED BASELINE BRANCH
```

If the repository has a protected branch, release branch, default branch, or team-shared integration branch, create an isolated branch first.

## Branch / Workspace Setup

### Step 0: Verify Current Context

Check:
- Current branch name
- Whether the branch is shared or protected
- Whether the repository uses branch-based isolation or another workspace model

If you are already in an isolated working branch or equivalent workspace, proceed with work.

If you are on the shared baseline branch, continue to Step 1.

### Step 1: Create an Isolated Branch

Use the repository's naming convention.

Good branch names are:
- Descriptive
- Short enough to scan
- Traceable to the work item when the repository uses ticket IDs

Common patterns:
- `<area>/<short-description>`
- `<type>/<ticket-id>-<short-description>`
- `<short-description>`

Examples:
- `feature/auth-timeout-handling`
- `fix/1234-empty-queue-name`
- `refactor/build-pipeline-cleanup`

### Step 2: Verify Isolation

Confirm that:
- The new branch or workspace is active
- You are no longer on the shared baseline branch
- The upcoming commits will land only in the isolated work context

### Step 3: Work Safely

While working:
- Stage only files relevant to the task
- Follow the repository's commit message rules
- Avoid broad staging commands if they are likely to capture unrelated files

## Naming Guidance

If the repository has a documented naming rule, follow it exactly.

If not, prefer:
- A short work descriptor
- Optional ticket or issue ID
- Stable separators such as `/` or `-`

Bad names:
- `fix_bug`
- `temp`
- `work`

Good names:
- `fix/session-timeout`
- `feature/4821-bulk-import`
- `refactor/query-builder-cleanup`

## Push Guidance

Use the repository's normal push flow for isolated branches.

Before pushing:
- Confirm the target branch or upstream is correct
- Confirm you are not pushing to the shared baseline branch
- Confirm only intended commits are included

If the repository uses review branches, merge requests, or pull requests, hand off to the completion/review skill after push preparation.

## Quick Reference

| Situation | Action |
|-----------|--------|
| On shared baseline branch, about to commit | Create isolated branch first |
| Already on isolated branch | Proceed with work |
| Need branch name | Follow repo naming rule or use descriptive short form |
| Ready to push | Push isolated branch, not shared baseline |
| Ready for review | See finishing-a-development-branch-base |

## Common Mistakes

### Committing on the shared branch

- Problem: bypasses isolation and increases integration risk
- Fix: check branch/workspace before the first commit

### Vague branch names

- Problem: branch purpose is unclear in history and review tools
- Fix: include a clear work descriptor and ticket ID if appropriate

### Over-broad staging

- Problem: unintended files get included
- Fix: stage explicit files whenever practical

## Red Flags

- About to commit on the shared baseline branch
- Branch name provides no clue about the work
- Staging unrelated files together with the task
- Pushing directly to the shared baseline branch

Any of these means you should stop and correct the workspace setup first.

## Integration

**Called by:**
- **brainstorming-base** — after design approval, before implementation
- **executing-plans-base** — before inline execution
- **subagent-driven-development-base** — before dispatching implementers

**Pairs with:**
- **finishing-a-development-branch-base** — push, review, merge preparation, cleanup after work completes
