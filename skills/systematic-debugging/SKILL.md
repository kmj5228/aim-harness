---
name: systematic-debugging
description: Use when encountering a bug, test failure, build failure, or unexpected behavior and you need to find root cause before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create secondary bugs. Fast guesses feel efficient but usually extend the failure.

**Core principle:** Find root cause before proposing or implementing a fix.

## The Iron Law

```text
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you have not completed root-cause investigation, you are not ready to fix the issue.

## When to Use

Use for any technical issue:
- Failing tests
- Build or compile failures
- Runtime errors
- Unexpected behavior
- Integration breakage
- Regressions after a change

Use especially when:
- You are under time pressure
- A quick fix looks obvious
- Multiple fixes have already failed
- You do not fully understand the system behavior

## The Four Phases

Complete each phase before moving on.

### Phase 1: Root Cause Investigation

Before attempting any fix:

1. **Read the evidence carefully**
   - Error messages
   - Stack traces
   - Logs
   - File paths
   - Line numbers
   - Inputs and outputs

2. **Reproduce consistently**
   - Use the smallest reliable command or action that reproduces the issue
   - Confirm whether the failure is deterministic, flaky, or environment-dependent

3. **Check recent change context**
   - Recent commits
   - Local diff
   - Dependency or config changes
   - Environment drift

4. **Trace data flow backward**
   - Where does the bad value or bad state first appear?
   - What called this code?
   - What earlier decision made the failure inevitable?
   - Keep tracing until you reach the source, not just the crash point

5. **Use the right tools**
   - Search tools for code paths and callers
   - Debuggers for state inspection
   - Profilers or memory tools when relevant
   - Logs, tracing, or temporary instrumentation when needed

### Phase 2: Pattern Analysis

1. Find a similar working path
2. Compare working and broken behavior
3. Identify meaningful differences:
   - Inputs
   - Control flow
   - State transitions
   - Dependencies
   - Configuration
   - Timing

### Phase 3: Hypothesis and Testing

1. Form one hypothesis at a time
   - "I think X is the root cause because Y"
2. Test the hypothesis with the smallest possible experiment
3. Evaluate the result
   - Confirmed -> move to Phase 4
   - Rejected -> form a new hypothesis

Do not mix multiple fixes into one experiment.

### Phase 4: Fix and Verification

1. Reproduce the bug with a failing test when practical
2. Implement one fix that addresses the root cause
3. Run targeted verification
4. Run broader verification appropriate to the repository
5. If 3+ fix attempts fail, stop and question the architecture or assumptions

**Required:** Use test-driven-development when the issue should be protected by a regression test.

## Red Flags - Stop and Reset

- "Quick fix for now, investigate later"
- "Let me just try changing this"
- "It is probably X"
- "I do not fully understand it, but this might work"
- Proposing a fix before tracing the failure source
- Making a second or third change without learning from the previous one

All of these mean: stop and return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The issue is simple" | Simple failures still have root causes. |
| "There is no time" | Systematic debugging is faster than repeated guessing. |
| "I already see the bug" | Seeing a symptom is not the same as understanding cause. |
| "One more fix attempt" | Repeated failed fixes usually mean the model is wrong. |
| "I can patch the symptom safely" | Symptom fixes often move the bug instead of removing it. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| Root Cause | Read evidence, reproduce, trace backward | You know what failed and why |
| Pattern | Compare with working behavior | You know what is meaningfully different |
| Hypothesis | Test one theory at a time | The cause is confirmed or disproven |
| Fix | Add protection, fix source, verify | The issue is resolved and guarded |

## Supporting Techniques

Available in this directory:
- `root-cause-tracing.md` — trace bugs backward through call paths
- `defense-in-depth.md` — add validation at multiple layers
- `condition-based-waiting.md` — replace arbitrary sleeps and timing guesses

## Tool Guidance

- Prefer fast search tools over manual browsing when tracing callers and data flow
- Prefer targeted instrumentation over broad noisy logging
- Prefer minimal experiments over broad speculative rewrites
- Prefer repository-native verification commands over guessed commands

## Integration

**Called by:**
- **executing-plans** — when task execution fails
- **subagent-driven-development** — when implementer work hits unexpected failures
- **dispatching-parallel-agents** — when independent investigations are needed

**Uses:**
- **test-driven-development** — regression test before fix
- **verification-before-completion** — final verification before claiming success
