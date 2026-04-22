---
name: writing-documents
description: Use when writing aim-facing markdown documents, issue responses, MR text, or manual follow-up drafts
---

# AIM Writing Documents

## Overview

Write for the target audience first, then choose the bound destination.

This generated skill keeps the reusable document-writing skeleton but applies `aim` bindings:

- generated default wording uses `issue`, `MR`, and `markdown document`
- repo markdown outputs go to `agent/`
- manual workspace goes to `generated/manual/`
- MR review target is browser-based

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

### MR

- default mode: `browser`
- location: `http://192.168.51.106/openframe/openframe7/aim`

### Manual Workspace

- default mode: `workspace_file`
- location: `generated/manual/`
- use `manual-workflow` when the task needs a dedicated manual follow-up decision and draft
- external publish and sync behavior are still excluded from this generated scope

## Repo-Aware Guidance

When a document refers to code changes or verification results, keep the actual `aim` change surface explicit:

- `src/lib`, `src/common`, `src/ulib`
  - shared library or common runtime logic
- `src/server`
  - server-side runtime logic
- `src/tool`, `src/util`
  - CLI tools and utility binaries
- `errcode`, `msgcode`
  - generated code and message data flows
- `config`, `resource`
  - configuration or runtime resource assets
- `test/unit/gtest`, `test/ivp`
  - test-only or verification-only surfaces
- `script/`
  - release, packaging, or operational flow
  - do not blur these with normal runtime verification

When drafting issue responses, MR text, or internal markdown:

- state which surface changed
- state which surface was only inspected
- avoid broad phrases like "AIM was changed" when only one area was touched

Evidence guidance:

- prefer safe evidence from `make`, `make gtest`, `make gtest-build`, and `make gtest-run`
- if coverage is mentioned, state whether the evidence came from:
  - the default GoogleTest summary under `test/unit/gtest/report/`
  - module `make html` output
  - the legacy `script/lcov-*.sh` workflow
- do not describe `script/dist/*.sh` or `script/ofrelease.sh` as normal verification evidence unless packaging was intentionally part of the task

## Writing Flow

1. Identify the audience.
2. Decide tone and abstraction level.
3. Identify the real scope of change:
   - runtime libraries or shared code
   - server surface
   - tool or utility surface
   - generated code and message data
   - config or resource assets
   - tests only
   - operational or packaging scripts
4. Choose the bound destination:
   - `agent/` for markdown document outputs
   - MR browser target for review text
   - `generated/manual/` only when the completion path calls for manual follow-up
5. Draft the content.
6. Stop for review before any publish/send action.

## Output Conventions

- topic-specific markdown artifacts may live under `agent/<topic>/`
- shared markdown outputs default to `agent/`
- reserved manual artifacts default to `generated/manual/`
- when relevant, include an explicit `Scope` or `Affected Areas` section so the document does not blur runtime code, generated data, and operational scripts

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
- `MR`
- `markdown document`

Accepted aliases:

- `ticket`, `jira`, `ims`
- `merge request`, `pull request`, `review request`
- `doc`, `note`, `report`

## Limits Of This First Pass

- No generated `manual-guide` body yet
- No generated external manual publish workflow yet
- No generated `completing-patch` workflow yet
- No auto-trigger implementation yet
- No generated platform-specific publish/save adapter yet

Use this skill as the generated binding layer, not as proof that the full AIM document workflow has already been productized.
