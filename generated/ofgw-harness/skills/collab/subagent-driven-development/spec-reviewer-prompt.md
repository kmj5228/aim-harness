# Spec Compliance Reviewer Prompt Template

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify the implementer built what was requested for OFGW, nothing more and nothing less.

```text
Agent tool (general-purpose):
  description: "Review spec compliance for Task N"
  prompt: |
    You are reviewing whether an OFGW implementation matches its specification.

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
    - Look for extra features they did not mention
    - Verify OFGW module boundaries and runtime conventions

    ## Your Job

    Read the implementation and verify:

    **Missing requirements:**
    - Everything requested implemented?
    - Any requested behavior skipped or only partially applied?

    **Extra work:**
    - Unrequested changes added?
    - Broader refactor or behavior change than the task required?

    **Misunderstandings:**
    - Was the requirement interpreted differently from the plan?
    - Did the implementation drift into the wrong module or layer?

    **OFGW compliance:**
    - Changes stay within the intended surface (`ofgwSrc`, `webterminal`, `ofgwAdmin`, config/resources, or scripts)?
    - Verification claims match the actual touched files and commands?
    - Backend changes cite `:ofgwSrc:classes`, `:ofgwSrc:test`, or `:ofgwSrc:jacocoTestReport` when relevant?
    - Notes avoid implying untouched modules were validated?

    **Verify by reading code, not by trusting the report.**

    Report:
    - ✅ Spec compliant (if everything matches after code inspection)
    - ❌ Issues found: [list missing, extra, or misleading items with file:line references]
```
