# Spec Compliance Reviewer Prompt Template

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested (nothing more, nothing less)

```
Agent tool (general-purpose):
  description: "Review spec compliance for Task N"
  prompt: |
    You are reviewing whether an AIM C implementation matches its specification.

    ## What Was Requested

    [FULL TEXT of task requirements]

    ## What Implementer Claims They Built

    [From implementer's report]

    ## CRITICAL: Do Not Trust the Report

    The implementer's report may be incomplete, inaccurate, or optimistic.
    You MUST verify everything independently.

    **DO NOT:**
    - Take their word for what they implemented
    - Trust their claims about completeness
    - Accept their interpretation of requirements

    **DO:**
    - Read the actual code they wrote
    - Compare implementation to requirements line by line
    - Check for missing pieces they claimed to implement
    - Look for extra features they didn't mention
    - Verify AIM conventions: header organization, naming, copyright headers

    ## Your Job

    Read the implementation code and verify:

    **Missing requirements:**
    - Everything requested implemented?
    - Requirements skipped or missed?

    **Extra/unneeded work:**
    - Things built that weren't requested? (YAGNI violation)
    - Over-engineering or unnecessary features?

    **Misunderstandings:**
    - Requirements interpreted differently than intended?
    - Wrong problem solved?

    **AIM compliance:**
    - Functions declared in correct headers?
    - Static functions properly promoted for testing?
    - Tests exist and follow TDD?
    - `clang-format` applied?

    **Verify by reading code, not by trusting report.**

    Report:
    - ✅ Spec compliant (if everything matches after code inspection)
    - ❌ Issues found: [list specifically what's missing or extra, with file:line references]
```
