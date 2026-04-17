# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable, repository-compliant)

**Only dispatch after spec compliance review passes.**

```
Agent tool (general-purpose):
  description: "Review code quality for Task N"
  prompt: |
    You are reviewing code quality for an implementation.

    ## Context

    WHAT_WAS_IMPLEMENTED: [from implementer's report]
    PLAN_OR_REQUIREMENTS: Task N from [plan-file]
    BASE_SHA: [commit before task]
    HEAD_SHA: [current commit]

    ## Review Checklist

    Review the diff between BASE_SHA and HEAD_SHA:

    ```bash
    git diff BASE_SHA..HEAD_SHA
    ```

    **Code Quality:**
    - Each file has one clear responsibility?
    - Functions well-named and focused?
    - Error handling appropriate for the language and repository?
    - Resource handling safe and consistent?
    - No obvious correctness or maintainability hazards?

    **Repository Conventions:**
    - File naming and layout match nearby patterns?
    - New or changed contracts are placed in the expected files?
    - Required formatting or linting conventions followed?
    - Plan instructions did not override stronger repository conventions?

    **Test Quality:**
    - Tests or reproductions verify real behavior?
    - Cases are scoped and understandable?
    - Edge cases and failure paths are covered where appropriate?
    - Test organization matches local conventions?

    **Build:**
    - Required task-level verification passes?
    - No obvious skipped validation steps?

    Report:
    - **Strengths:** What's done well
    - **Issues:** Critical / Important / Minor with file:line references
    - **Assessment:** Approved | Changes Required
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment
