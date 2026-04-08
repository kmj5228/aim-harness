# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable, AIM-compliant)

**Only dispatch after spec compliance review passes.**

```
Agent tool (general-purpose):
  description: "Review code quality for Task N"
  prompt: |
    You are reviewing code quality for an AIM C implementation.

    ## Context

    WHAT_WAS_IMPLEMENTED: [from implementer's report]
    PLAN_OR_REQUIREMENTS: Task N from [plan-file]
    BASE_SHA: [commit before task]
    HEAD_SHA: [current commit]

    ## Review Checklist

    Review the diff between BASE_SHA and HEAD_SHA:

    ```bash
    dx git diff BASE_SHA..HEAD_SHA
    ```

    **Code Quality:**
    - Each file has one clear responsibility?
    - Functions well-named and focused?
    - Error handling correct (return codes, not exceptions)?
    - Memory management safe (no leaks, double-free)?
    - No buffer overflows or unsafe string operations?

    **AIM Conventions:**
    - Header organization: include/{MODULE}.h, {MODULE}_inner.h, {SOURCE}.h
    - Static functions promoted correctly for testing?
    - ADT used where appropriate?
    - Copyright header present in new files?
    - `clang-format` applied?

    **Test Quality:**
    - Tests verify real behavior (not stubs)?
    - One behavior per test?
    - Clear descriptive test names?
    - Edge cases and error paths covered?
    - Test file naming: test_{module}_{source}.cpp?

    **Build:**
    - `dx make gtest` passes?
    - `dx make` clean build?

    Report:
    - **Strengths:** What's done well
    - **Issues:** Critical / Important / Minor with file:line references
    - **Assessment:** Approved | Changes Required
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment
