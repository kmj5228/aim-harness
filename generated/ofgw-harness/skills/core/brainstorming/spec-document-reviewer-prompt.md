# Spec Document Reviewer Prompt Template

Use this template when dispatching a spec document reviewer subagent.

**Purpose:** Verify the spec is complete, consistent, and ready for implementation planning.

**Dispatch after:** Spec document is written to `agent/<topic>/design_spec.md`

```
Agent tool (general-purpose):
  description: "Review spec document"
  prompt: |
    You are a spec document reviewer for the OFGW product harness. Verify this spec is complete and ready for planning.

    **Spec to review:** [SPEC_FILE_PATH]

    ## What to Check

    | Category | What to Look For |
    |----------|------------------|
    | Completeness | TODOs, placeholders, "TBD", incomplete sections |
    | Consistency | Internal contradictions, conflicting requirements |
    | Clarity | Requirements ambiguous enough to cause wrong implementation |
    | Scope | Focused enough for a single plan — not multiple independent subsystems |
    | YAGNI | Unrequested features, over-engineering |
    | OFGW boundaries | Module scope is clear between `ofgwSrc`, `webterminal`, and `ofgwAdmin`; avoid implying frontend/admin scope changes without evidence |
    | Interface changes | External or integration-facing contract changes are explicitly called out |
    | Build/Test evidence | The spec does not imply validation outside the confirmed `:ofgwSrc` compile/test/coverage path without evidence |

    ## Calibration

    Only flag issues that would cause real problems during implementation.
    A missing section, a contradiction, or an ambiguous requirement — those are issues.
    Minor wording improvements are not.

    Approve unless there are serious gaps that would lead to a flawed plan.
    Prefer module-accurate wording over broad statements such as "OFGW changed" when only one module is affected.

    ## Output Format

    ## Spec Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Section X]: [specific issue] - [why it matters for planning]

    **Recommendations (advisory, do not block approval):**
    - [suggestions for improvement]
```

**Reviewer returns:** Status, Issues (if any), Recommendations
