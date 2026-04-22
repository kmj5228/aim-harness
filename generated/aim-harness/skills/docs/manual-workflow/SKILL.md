---
name: manual-workflow
description: Use when aim work may require manual follow-up and a draft must be prepared under the generated manual workspace
---

# Manual Workflow

Run the `aim` manual follow-up flow as a local drafting workflow.

This generated skill keeps the useful gate and safety semantics from the AIM manual process, but does not carry over the AIM-specific repo, branch, Antora, or publish procedure.

## Core Policy

- manual follow-up is part of the default completion path
- writable workspace: `generated/manual/`
- this skill drafts local manual artifacts only
- prefer a topic-scoped manual draft directory when the topic is known
- external publish, sync, or release integration is still out of scope

<HARD-GATE>
Do not publish, sync, submit, or treat the manual as complete in the same turn as drafting. Draft first, show it, then wait for explicit approval.
</HARD-GATE>

## Step 1: Decide Whether Manual Follow-Up Is Needed

Check for user-visible change such as:

- command usage or option changes
- config key changes
- output or message changes
- operating procedure changes
- setup or runtime behavior that users must learn

Usually not needed for:

- internal refactors
- test-only changes
- invisible cleanup
- implementation details with no user-facing effect

If manual follow-up is not needed, say so with the reason and stop.

## Step 2: Collect Existing Context

Reuse what already exists:

- `agent/<topic>/analysis_report.md`
- `agent/<topic>/design_spec.md`
- `agent/<topic>/review_context.md`
- `agent/<topic>/plan_tasks.md`
- user-provided notes or issue context

Do not restate details you cannot verify.

## Step 3: Draft Manual Content

Write the draft under:

- preferred: `generated/manual/<topic>/manual_draft.md`
- fallback when no stable topic exists yet: `generated/manual/manual_draft.md`

Suggested shape:

```markdown
# Manual Draft

Status: Draft
Approval: Pending

## Audience

## Affected Surface

## Change Summary

## Before

## After

## Procedure or Usage

## Verification Notes

## Open Questions
```

Use plain markdown unless a later pass defines a richer target format.

## Step 4: Review Before Any Publish Action

- show the draft to the user
- call out assumptions
- call out which parts are verified versus still provisional
- wait for approval before any save/send/publish step beyond the local workspace

## Rules

- Keep the draft user-facing and operational.
- Prefer exact verified wording for commands, options, and outputs.
- Separate verified facts from provisional wording.
- Keep the draft status explicit until the user approves a next step.
- If the product has multiple runtime surfaces, state which surface changed and which remain out of scope.
- Do not invent an external manual repo workflow that has not been generated yet.

## Current Limits

- no generated external manual repo sync
- no generated format conversion to Antora/AsciiDoc
- no generated release marker automation
- no auto-trigger implementation

## Integration

**Called by:**
- **writing-documents** — when completion includes manual follow-up
- Completion review — when user-facing behavior changed

**Feeds into:**
- local manual draft review under `generated/manual/`
