---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing and you need fresh verification evidence before making that claim
---

# Verification Before Completion

## Overview

Claiming success without fresh verification is not efficiency. It is an unsupported assertion.

**Core principle:** Evidence before claims.

## The Iron Law

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you did not run the verification now, you cannot honestly claim success now.

## The Gate Function

Before claiming any status:

1. Identify what evidence proves the claim
2. Run the required verification commands
3. Read the full output and exit status
4. Compare the actual result to the claim
5. Only then report status

Skip any step and the claim is unverified.

## Verification Categories

| Claim | Evidence Needed |
|-------|-----------------|
| Tests pass | Relevant test command completed successfully |
| Build succeeds | Build/compile command completed successfully |
| Bug is fixed | Reproduction no longer fails and regression protection exists |
| Formatting is correct | Formatter or diff check confirms expected state |
| Ready for review/merge | Required repository-level checks all passed |

## What To Run

Use the current repository's real verification commands, not guessed ones.

Typical categories:
- Targeted test verification for the changed area
- Broader regression verification required by the repository
- Build or compile verification
- Lint/format/type-check verification when relevant
- Coverage or policy gates only if the repository actually requires them

## Full Verification Sequence

Before claiming work complete:

1. Run targeted verification for the changed behavior
2. Run broader verification appropriate to the change scope
3. Run build/compile verification if the repository has one
4. Run policy gates required by the repository
5. Confirm only intended files changed

All required checks must pass. Partial verification is not completion.

## Common Failures

| Claim | Not Sufficient |
|-------|----------------|
| "Tests pass" | A previous run or a guess |
| "Build is clean" | Tests passing without a build check |
| "Bug is fixed" | Code changed without re-running reproduction |
| "Ready for review" | Some checks passed but required gates were skipped |
| "Coverage is fine" | Assuming enough tests were added without measuring |

## Red Flags - Stop

- Using words like "should", "probably", "seems"
- Celebrating completion before verification
- Relying on partial checks
- Reusing stale command output
- Skipping a required repository gate

Any of these means the work is not yet verified.

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It should work now" | Run the verification. |
| "I am confident" | Confidence is not evidence. |
| "Just this once" | Verification is not optional. |
| "Targeted tests passed, that is enough" | Only if the repository requires nothing broader. |
| "I added more tests, coverage must be fine" | Measure it if coverage is a real gate. |

## Reporting Rule

When reporting results:

- State the command or category of verification run
- State whether it passed or failed
- State the important evidence
- If it failed, report actual status instead of the desired status

Good:

```text
Verification
- Targeted tests: passed
- Build: passed
- Regression suite: failed in auth/session timeout scenario
```

Bad:

```text
Done, everything looks good.
```

## Bottom Line

Run the command. Read the output. Then make the claim.

No shortcuts.

## Integration

**Called by:**
- **executing-plans** — before claiming task or plan completion
- **subagent-driven-development** — before implementer completion
- **systematic-debugging** — after a fix
- **finishing-a-development-branch** — before review/merge preparation
- **dispatching-parallel-agents** — after integrating parallel work
