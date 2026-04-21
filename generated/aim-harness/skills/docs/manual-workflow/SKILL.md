---
name: manual-workflow
description: Use when AIM work may require manual follow-up and a local draft must be prepared under the generated manual workspace
---

# Manual Workflow

Run the AIM manual follow-up flow as a local-first drafting workflow.

This generated skill preserves the AIM gate semantics:

- decide whether a manual update is needed
- gather verified context first
- draft before any publish action

But it stops before the original upstream publish path.

## Core Policy

- manual follow-up stays in the default completion path
- writable draft workspace: `generated/manual/`
- prefer a topic-scoped draft directory
- upstream truth still exists:
  - original manual repo: `/Users/mjkang/company/MANUAL/openFrame_aim`
  - original branch: `7.3_main`
- current generated runtime does not automate that publish step

<HARD-GATE>
Do not publish, sync, submit, or treat the manual as complete in the same turn as drafting. Draft first, show it, then wait for explicit approval.
</HARD-GATE>

## Step 1: Decide Whether Manual Follow-Up Is Needed

Check for user-visible change such as:

- command usage or option changes
- config key changes
- output or message changes
- operational procedure changes
- user-facing behavior change

Usually not needed for:

- internal refactors
- test-only changes
- invisible cleanup

If manual follow-up is not needed, say so with the reason and stop.

## Step 2: Collect Existing Context

Reuse what already exists:

- `agent/<topic>/analysis_report.md`
- `agent/<topic>/design_spec.md`
- `agent/<topic>/review_context.md`
- `agent/<topic>/plan_tasks.md`
- user-provided notes or issue context

If the original AIM-style upstream manual workflow matters for the task, consult the carried-over reference:

- `skills/docs/writing-documents/manual-guide.md`

Treat that file as source reference, not as proof that the full publish path is active here.

## Step 3: Draft Manual Content

Write the local draft under:

- preferred: `generated/manual/<topic>/manual_draft.md`
- fallback: `generated/manual/manual_draft.md`

Suggested shape:

```markdown
# Manual Draft

Status: Draft
Approval: Pending

## Audience

## Affected Surface

## Change Summary

## Procedure Or Usage

## Verification Notes

## Upstream Publish Notes

## Open Questions
```

## Step 4: Review Before Any Publish Action

- show the draft to the user
- separate verified text from provisional wording
- call out that upstream MANUAL repo publication is still out of active generated scope

## Current Limits

- no generated external MANUAL repo sync
- no generated Antora/AsciiDoc conversion
- no generated post-merge marker automation
- no active generated `completing-patch`

## Integration

**Called by:**
- **writing-documents**
- completion review when user-facing behavior changed

**Feeds into:**
- local draft review under `generated/manual/`
