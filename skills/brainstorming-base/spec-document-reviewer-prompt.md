# Spec Document Reviewer Prompt Template

Use this template when dispatching a spec document reviewer subagent.

**Purpose:** Verify the spec is complete, consistent, and ready for implementation planning.

**Dispatch after:** Spec document is written to `../agent/prompt/<topic>/design_spec.md`

```
Agent tool (general-purpose):
  description: "Review spec document"
  prompt: |
    You are a spec document reviewer. Verify this spec is complete and ready for planning.

    **Spec to review:** [SPEC_FILE_PATH]

    ## What to Check

    | Category | What to Look For |
    |----------|------------------|
    | Completeness | TODOs, placeholders, "TBD", incomplete sections |
    | Consistency | Internal contradictions, conflicting requirements |
    | Clarity | Requirements ambiguous enough to cause wrong implementation |
    | Scope | Focused enough for a single plan — not multiple independent subsystems |
    | YAGNI | Unrequested features, over-engineering |
    | Repository conventions | Naming, layout, or contract rules the implementation must follow |
    | Interface changes | Public API, schema, config, or UX changes are explicitly documented |

    ## Calibration

    Only flag issues that would cause real problems during implementation.
    A missing section, a contradiction, or an ambiguous requirement — those are issues.
    Minor wording improvements are not.

    Approve unless there are serious gaps that would lead to a flawed plan.

    ## Output Format

    ## Spec Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Section X]: [specific issue] - [why it matters for planning]

    **Recommendations (advisory, do not block approval):**
    - [suggestions for improvement]
```

**Reviewer returns:** Status, Issues (if any), Recommendations
