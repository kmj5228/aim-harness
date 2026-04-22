---
name: finishing-a-development-branch
description: Use when implementation is complete and you need to finalize the branch, prepare review handoff, or decide how to wrap up the current development line
---

# Finishing a Development Branch

## Overview

Guide the final handoff of implementation work: verify, clean up, push or sync the branch, and choose the next review/completion step.

**Core principle:** Verify first, then present clear completion options, then execute the chosen path.

## The Process

### Step 1: Verify Completion

**Required:** Use verification-before-completion first.

If required checks fail:
- Stop
- Fix the issues
- Re-run verification before proceeding

### Step 2: Clean Up

Before final handoff:

1. Confirm you are on the correct isolated branch or workspace
2. Review the change set for unintended files
3. Review commit structure if the repository uses meaningful commit history
4. Apply any required format, lint, or policy checks

### Step 3: Sync the Branch

Use the repository's normal push or sync flow for the current branch/workspace.

Before syncing:
- Confirm the destination is correct
- Confirm you are not writing to the shared baseline by mistake
- Confirm credentials or access method are correct for the repository workflow

### Step 4: Present Completion Options

Typical options:

1. Create a new review request
2. Update an existing review request
3. Keep the branch as-is for later
4. Request self-review first

Use the options that match the repository's actual workflow.

### Step 5: Execute the Chosen Path

#### Option 1: Create Review Request

- Create the repository's normal review artifact
  - pull request
  - merge request
  - review branch handoff
  - equivalent team workflow
- Add the required title, summary, and verification notes

#### Option 2: Update Existing Review Request

- Update the existing review artifact
- Refresh summary, verification status, and scope if the patch changed materially

#### Option 3: Keep As-Is

- Report the current branch/workspace status clearly
- State what remains to be done later

#### Option 4: Self-Review First

- Invoke requesting-code-review
- Apply findings before external review if needed

## Quick Reference

| Option | Branch Sync | Review Artifact | Extra Review |
|--------|-------------|-----------------|-------------|
| Create review request | yes | create | optional |
| Update review request | yes | update | optional |
| Keep as-is | optional | skip | skip |
| Self-review first | yes or later | after self-review | self-review |

## Common Mistakes

### Skipping verification

- Problem: handoff happens with stale or missing evidence
- Fix: always run verification-before-completion first

### Wrong branch or workspace

- Problem: code is synced from the wrong context
- Fix: confirm branch/workspace before push or review creation

### Stale review description

- Problem: reviewers see outdated scope or validation info
- Fix: refresh review summary whenever the patch changes materially

### Premature completion

- Problem: work is declared done before the review path is chosen
- Fix: separate "implementation complete" from "handoff complete"

## Red Flags

- Syncing with failing verification
- Creating review without current verification evidence
- Pushing or merging from the wrong branch/workspace
- Force-updating history without explicit need
- Assuming the review artifact still matches the patch after changes

## Integration

**Called by:**
- **subagent-driven-development** — after all tasks complete
- **executing-plans** — after inline execution completes

**Feeds into:**
- **requesting-code-review** — when self-review is chosen first
- Product-specific completion steps — when the repository has extra release, documentation, or patch workflows

**Pairs with:**
- **verification-before-completion** — verify before finishing
