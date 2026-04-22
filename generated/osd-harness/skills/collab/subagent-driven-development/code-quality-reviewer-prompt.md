# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify the implementation is well-built, maintainable, tested, and OSD-compliant.

**Only dispatch after spec compliance review passes.**

```text
Agent tool (general-purpose):
  description: "Review code quality for Task N"
  prompt: |
    You are reviewing code quality for an OSD implementation.

    ## Review Checklist

    **Code Quality:**
    - Each file has one clear responsibility?
    - Error handling and fallback behavior are explicit?
    - No obvious spill into unrelated modules?

    **OSD Conventions:**
    - Touched areas are called out explicitly (`src/lib`, `src/server`, `src/tool`, `src/util`, code tables, or `dist/`)
    - New files follow the surrounding naming/layout pattern
    - Verification claims match the touched area

    **Build / Verification:**
    - `make` when runtime code changed
    - `make -C test` when test code changed
    - `test/run_coverage.sh` when coverage claims are made

    Report:
    - **Strengths**
    - **Issues:** Critical / Important / Minor with file:line references
    - **Assessment:** Approved | Changes Required
```
