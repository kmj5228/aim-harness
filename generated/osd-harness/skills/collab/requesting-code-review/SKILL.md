---
name: requesting-code-review
description: Use when your own implementation is ready for a self-review pass before handoff, merge preparation, or completion claims
---

# Requesting Code Review

Run a structured self-review before handing work to other reviewers or calling it complete.

**Core principle:** Review your own patch while you still have time to fix it cheaply.

## When to Request

**Recommended:**
- Before asking others to review the change
- Before merge or completion preparation
- After a major feature or risky refactor
- After fixing a subtle bug

**Especially valuable when:**
- The change touched multiple files
- The fix involved control-flow or fallback logic
- The patch was built incrementally over several steps

## The Review Loop

### 1. Define Review Scope

Collect the actual change set you want reviewed:
- Commits in scope
- Files changed
- Key behavior changes
- Known risks or open questions

### 2. Invoke the Review Path

Use the repository's review mechanism for self-review.

That may be:
- A dedicated review skill
- A review prompt
- A structured checklist
- A patch review command

The goal is the same: get a fresh, critical pass over your own work before external review.

### 3. Triage Findings

| Priority | Action |
|----------|--------|
| Critical | Fix immediately |
| Important | Fix before handoff unless you have a strong documented reason |
| Minor | Fix now or document why not |

Push back only with technical evidence.

### 4. Re-verify After Fixes

If review findings lead to code changes:
- Re-run the necessary verification
- Re-run review if the patch changed materially

## What Good Self-Review Catches

- Requirement drift
- Missing tests
- Incorrect control flow
- Weak fallback behavior
- Unclear naming
- Unintended file changes
- Compatibility or integration risks

## Red Flags

- Skipping self-review because the change feels simple
- Ignoring serious findings without evidence
- Treating self-review as a formality
- Asking for external review before your own patch is coherent

## Integration

**Called by:**
- **finishing-a-development-branch** — before review or merge preparation

**Uses:**
- **code-reviewer** — when a structured review workflow is available

**Feeds into:**
- **receiving-code-review** — if findings need systematic follow-up
