# Plan Document Reviewer Prompt Template

Use this template when dispatching a plan document reviewer subagent.

**Purpose:** Verify the plan is complete, matches the spec, and has proper task decomposition.

**Dispatch after:** The complete plan is written to `../agent/prompt/<topic>/plan_tasks.md`

```
Agent tool (general-purpose):
  description: "Review plan document"
  prompt: |
    You are a plan document reviewer. Verify this plan is ready for implementation.

    **Plan to review:** [PLAN_FILE_PATH]
    **Spec for reference:** [SPEC_FILE_PATH]

    ## What to Check

    | Category | What to Look For |
    |----------|------------------|
    | Completeness | TODOs, placeholders, incomplete tasks, missing steps |
    | Spec Alignment | Plan covers spec requirements, no major scope creep |
    | Task Decomposition | Tasks have clear boundaries, steps are actionable |
    | Buildability | Could an engineer follow this without getting stuck? |
    | Repository conventions | Commands, file paths, naming, and project workflow match the repository |
    | Verification loop | Tasks include targeted verification, broader verification, and checkpointing where appropriate |

    ## Calibration

    Only flag issues that would cause real problems during implementation.
    Approve unless there are serious gaps — missing requirements, contradictory steps,
    placeholder content, or tasks so vague they can't be acted on.

    ## Output Format

    ## Plan Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Task X, Step Y]: [specific issue] - [why it matters]

    **Recommendations (advisory, do not block approval):**
    - [suggestions]
```

**Reviewer returns:** Status, Issues (if any), Recommendations
