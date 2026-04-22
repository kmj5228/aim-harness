# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify the implementation is well-built, maintainable, tested, and OFGW-compliant.

**Only dispatch after spec compliance review passes.**

```text
Agent tool (general-purpose):
  description: "Review code quality for Task N"
  prompt: |
    You are reviewing code quality for an OFGW implementation.

    ## Context

    WHAT_WAS_IMPLEMENTED: [from implementer's report]
    PLAN_OR_REQUIREMENTS: Task N from [plan-file]
    BASE_SHA: [commit before task]
    HEAD_SHA: [current commit]

    ## Review Checklist

    Review the diff between BASE_SHA and HEAD_SHA.

    **Code Quality:**
    - Each file has one clear responsibility?
    - Functions/classes/config changes are well named and focused?
    - Error handling and fallback behavior are explicit?
    - No obvious overreach into unrelated modules?

    **OFGW Conventions:**
    - Touched modules are called out explicitly (`ofgwSrc`, `webterminal`, `ofgwAdmin`, config/resources, or scripts)
    - New files follow the surrounding naming/layout pattern
    - Verification claims match the touched area
    - Backend code changes use the proven `ofgwSrc` command set when relevant

    **Test Quality:**
    - Tests verify real behavior rather than only mocks or scaffolding?
    - One behavior per test?
    - Edge cases and error paths covered?
    - Reported verification scope matches the touched files?

    **Build / Verification:**
    - `./gradlew :ofgwSrc:classes --no-daemon` when backend code changed
    - `./gradlew :ofgwSrc:test --no-daemon` when backend tests changed
    - `./gradlew :ofgwSrc:jacocoTestReport --no-daemon` when coverage claims are made

    Report:
    - **Strengths:** What's done well
    - **Issues:** Critical / Important / Minor with file:line references
    - **Assessment:** Approved | Changes Required
```
