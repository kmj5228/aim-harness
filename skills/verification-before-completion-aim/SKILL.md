---
name: verification-before-completion-aim
description: Use when about to claim work is complete, fixed, or passing - requires running verification commands and confirming output before making any success claims
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## AIM Verification Commands

| Claim | Command | Evidence Required |
|-------|---------|-------------------|
| Tests pass | `dx make gtest` | Output: 0 failures |
| Build succeeds | `dx make` | Output: exit 0, no errors |
| Coverage meets 80% | `dx bash -c "cd /root/ofsrc/aim && ./script/measure_diff_cov.sh"` | Output: >= 80% |
| Code formatted | `clang-format -i <files>` then `dx git diff` | No diff |
| Bug fixed | Failing gtest now passes | RED→GREEN verified |

## Common Failures

| Claim | Not Sufficient |
|-------|----------------|
| "Tests pass" | Previous run, "should pass" |
| "Build clean" | Tests passing (tests != build) |
| "Bug fixed" | Code changed, assumed fixed |
| "Coverage OK" | "I added enough tests" without measuring |
| "Ready for MR" | Tests pass but coverage not checked |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Done!", "Perfect!")
- About to commit/push without verification
- Relying on partial verification
- Thinking "just this once"
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence != evidence |
| "Just this once" | No exceptions |
| "Tests passed, build must be fine" | Tests != build. Run both. |
| "I added tests, coverage is fine" | Measure it. Don't guess. |

## Full Verification Sequence

Before claiming ANY work complete:

```bash
# 1. All tests pass
dx make gtest

# 2. Production build clean
dx make

# 3. Coverage meets threshold (if new code added)
dx bash -c "cd /root/ofsrc/aim && ./script/measure_diff_cov.sh"

# 4. Code formatted
# (verify no unformatted changes)
```

**All 3 (or 4) must pass. Partial is not complete.**

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
