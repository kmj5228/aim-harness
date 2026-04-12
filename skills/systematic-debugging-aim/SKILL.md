---
name: systematic-debugging-aim
description: Use when encountering any bug, test failure, or unexpected behavior in AIM, before proposing fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures (`dx make gtest` failures)
- Bugs in production
- Unexpected behavior
- Build failures (`dx make` errors)
- Segfaults, memory corruption
- Integration issues

**Use ESPECIALLY when:**
- Under time pressure
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- You don't fully understand the issue

## The Four Phases

Complete each phase before proceeding.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes
   - Check AIM errcode definitions if error code appears

2. **Reproduce Consistently**
   ```bash
   dx make gtest    # reproduce test failure
   dx make          # reproduce build failure
   dx bash -c "gdb /root/ofsrc/aim/bin/program core"  # analyze core dump
   ```

3. **Check Recent Changes**
   ```bash
   dx git log --oneline -10
   dx git diff HEAD~3
   ```

4. **Trace Data Flow**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

   ```bash
   dx bash -c "rg 'function_name' /root/ofsrc/aim/src/"   # content search (not grep)
   dx bash -c "fd 'filename' /root/ofsrc/aim/src/"         # file search (not find)
   dx bash -c "gdb -batch -ex 'bt' -ex 'quit' /path/to/binary core"
   ```

5. **Use Debugging Tools**
   ```bash
   dx bash -c "gdb /root/ofsrc/aim/bin/program"    # interactive debugger
   dx bash -c "valgrind --leak-check=full ./program"  # memory issues
   ```

   **Docker 내 검색:** `grep` → `rg`, `find` → `fd` (빠르고 이미 설치됨)

### Phase 2: Pattern Analysis

1. **Find Working Examples** — similar working code in AIM codebase
2. **Compare** — what's different between working and broken?
3. **Understand Dependencies** — other modules, config, environment

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** — "I think X is the root cause because Y"
2. **Test Minimally** — smallest possible change, one variable at a time
3. **Verify** — did it work? Yes → Phase 4. No → new hypothesis.

### Phase 4: Implementation

1. **Create Failing Test Case**
   ```bash
   # Write gtest reproducing the bug
   dx make gtest    # verify it fails
   ```
   **REQUIRED:** Use test-driven-development-aim for the failing test.

2. **Implement Single Fix** — address root cause, ONE change at a time

3. **Verify Fix**
   ```bash
   dx make gtest    # test passes now
   dx make          # build still clean
   ```

4. **If 3+ Fixes Failed: Question Architecture**
   - Each fix reveals new problems in different places → architectural issue
   - STOP and discuss with user before attempting more fixes

## Red Flags - STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too |
| "Emergency, no time" | Systematic is FASTER than thrashing |
| "Just try this first" | First fix sets the pattern. Do it right. |
| "I see the problem" | Seeing symptoms != understanding root cause |
| "One more fix attempt" | 3+ failures = architectural problem |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create failing gtest, fix, verify | Bug resolved, tests pass |

## Supporting Techniques

Available in this directory:
- **`root-cause-tracing.md`** — trace bugs backward through call stack
- **`defense-in-depth.md`** — add validation at multiple layers
- **`condition-based-waiting.md`** — replace arbitrary timeouts

**Related skills:**
- **test-driven-development-aim** — for creating failing test case (Phase 4)
- **verification-before-completion-aim** — verify fix before claiming success

## Integration

**Called by:**
- **executing-plans-aim** — 테스트 실패 시
- **subagent-driven-development-aim** — implementer 서브에이전트 내부 실패 시
- **dispatching-parallel-agents-aim** — 독립 문제 조사 시

**Uses:**
- **test-driven-development-aim** Phase 4 — 수정 검증 테스트 작성
- **verification-before-completion-aim** — 수정 완료 전 검증
