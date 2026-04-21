---
name: requesting-code-review
description: Use when completing tasks or before merging to self-review your own AIM code using code-reviewer Phase A~E
---

# Requesting Code Review

Dispatch code-reviewer in `--auto` mode (Phase A~E only) to catch issues in your own code before MR.

**Core principle:** Review early, review often. Self-review catches issues before they reach human reviewers.

## When to Request

**Mandatory:**
- Before creating MR (finishing-a-development-branch Option 4)
- After completing major feature

**Optional but valuable:**
- When stuck (fresh perspective)
- After fixing complex bug
- Before large refactoring

## How to Request

### 1. Get git info

```bash
dx git log --oneline rb_73..HEAD    # commits to review
dx git diff rb_73..HEAD --stat      # files changed
```

### 2. Invoke code-reviewer

Invoke the `code-reviewer` skill with `--auto` flag:

```
/code-reviewer --auto
Topic: <topic>
MR: (none — self-review, use branch diff)
Source branch: <feature-branch>
Target branch: rb_73
```

**`--auto` mode:**
- Runs Phase A~E only (info collect → code review → test review → coverage → synthesis)
- Skips Phase F~I (GitLab registration, standby, verification, final judgment)
- Results saved to `agent/<topic>/review_*` files

### 3. Act on feedback

| Priority | Action |
|----------|--------|
| Critical | Fix immediately |
| Important | Fix before MR |
| Minor | Fix or document rationale for skipping |

Push back with technical reasoning if reviewer is wrong.

## Integration

**Called by:**
- **finishing-a-development-branch** (Option 4) — self-review before MR

**Uses:**
- **code-reviewer** — Phase A~E in `--auto` mode

**Feeds into:**
- **receiving-code-review** — if review findings need systematic processing

## Red Flags

- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback without evidence
