---
name: writing-documents
description: Use when writing osd-facing markdown documents, issue responses, PR text, or manual follow-up drafts
---

# OSD Writing Documents

## Overview

Write for the target audience first, then choose the bound destination.

This generated skill keeps the reusable document-writing skeleton but applies `osd` bindings:

- generated default wording uses `issue`, `PR`, and `markdown document`
- repo markdown outputs go to `agent/`
- manual workspace goes to `generated/manual/`
- PR review target is browser-based

<HARD-GATE>
Do not publish, submit, send, or save content in the same turn as drafting. Show the draft first, then wait for explicit user approval.
</HARD-GATE>

## Verb Split

Treat these as different actions:

- `write`, `draft`, `compose`
  - input content only
  - stop and show the result
- `save`, `submit`, `publish`, `send`
  - execute the stored action only after explicit approval

Do not collapse drafting and publishing into one step.

## Destinations

### Repo Markdown

- default mode: `workspace_file`
- location: `agent/`
- use for internal markdown documents such as reports, plans, and structured notes

### PR

- default mode: `browser`
- location: `http://192.168.51.106/openframe/openframe7/osd`

### Manual Workspace

- default mode: `workspace_file`
- location: `generated/manual/`
- use `manual-workflow` when the task needs a dedicated manual follow-up decision and draft
- external publish/sync behavior is still excluded from this generated scope

## Repo-Aware Guidance

When a document refers to code changes or verification results, keep the actual `osd` change surface explicit:

- `src/lib`
  - shared library logic
- `src/server`
  - server-side runtime logic
- `src/tool`
  - tooling binaries and related code paths
- `src/util`
  - utility programs
- `dist/` or other operational scripts
  - release, packaging, or operational flow
  - do not blur these with normal runtime verification

When drafting issue responses, PR text, or internal markdown:

- state which module changed
- state which module was only inspected
- avoid broad phrases like "OSD was changed" when only one area was touched

Evidence guidance:

- prefer safe evidence from `make`, `make -C test`, and `test/run_coverage.sh`
- do not describe `dist/patch_osd.sh` or `dist/dist_osd.sh` as normal verification evidence unless packaging was intentionally part of the task
- packaging scripts are operational workflows, so do not casually present them as ordinary compile/test proof

## Writing Flow

1. Identify the audience.
2. Decide tone and abstraction level.
3. Identify the real scope of change:
   - library/runtime core (`src/lib`)
   - server surface (`src/server`)
   - tool surface (`src/tool`)
   - util surface (`src/util`)
   - operational or packaging scripts (`dist/` and related paths)
4. Choose the bound destination:
   - `agent/` for markdown document outputs
   - PR browser target for review text
   - `generated/manual/` only when the completion path calls for manual follow-up
5. Draft the content.
6. Stop for review before any publish/send action.

## Output Conventions

- topic-specific markdown artifacts may live under `agent/<topic>/`
- shared markdown outputs default to `agent/`
- reserved manual artifacts default to `generated/manual/`
- when relevant, include an explicit `Scope` or `Affected Areas` section so the document does not blur runtime code and operational scripts

## Markdown Conventions

- write section conclusions first
- prefer diagrams or tight structure before long flow prose
- keep runtime markdown outputs under `agent/`
- keep manual-specific drafts under `generated/manual/`
- keep canonical artifact filenames:
  - `analysis_report.md`
  - `design_spec.md`
  - `plan_tasks.md`

## Terminology

Canonical terms:

- `issue`
- `PR`
- `markdown document`

Accepted aliases:

- `ticket`, `jira`, `ims`
- `pull request`, `review request`
- `doc`, `note`, `report`

## Limits Of This First Pass

- No generated `manual-guide` body yet
- No generated external manual publish workflow yet
- No generated `completing-patch` workflow yet
- No auto-trigger implementation yet
- No generated platform-specific publish/save adapter yet

Use this skill as the generated binding layer, not as proof that the full AIM document workflow has already been productized.
