---
name: writing-documents
description: Use when writing ofgw-facing markdown documents, issue responses, PR text, or manual follow-up drafts
---

# OFGW Writing Documents

## Overview

Write for the target audience first, then choose the bound destination.

This generated skill keeps the reusable document-writing skeleton but applies `ofgw` bindings:

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
- location: `http://192.168.51.106/openframe/openframe7/ofgw`

### Manual Workspace

- default mode: `workspace_file`
- location: `generated/manual/`
- use `manual-workflow` when the task needs a dedicated manual follow-up decision and draft
- external publish/sync behavior is still excluded from this generated scope

## Repo-Aware Guidance

When a document refers to code changes or verification results, keep the actual `ofgw` module split explicit:

- `ofgwSrc`
  - main backend/runtime module
  - default assumption for backend issue analysis, fix explanation, and test evidence
- `webterminal`
  - separate packaged module
  - do not imply it changed unless you verified it actually changed
- `ofgwAdmin`
  - separate `pnpm`-based admin frontend
  - do not imply admin UI impact unless the task or evidence explicitly includes it

When drafting issue responses, PR text, or internal markdown:

- state which module changed
- state which module was only inspected
- avoid broad phrases like "OFGW was changed" when only one module was touched

Evidence guidance:

- prefer safe compile/test/coverage evidence from `:ofgwSrc:classes`, `:ofgwSrc:test`, and `:ofgwSrc:jacocoTestReport`
- do not describe `jar` or `war` packaging as completed evidence unless those tasks were intentionally run
- packaging tasks can mutate version files or create commits, so do not casually describe release packaging as part of normal verification

## Writing Flow

1. Identify the audience.
2. Decide tone and abstraction level.
3. Identify the real scope of change:
   - backend/runtime (`ofgwSrc`)
   - packaged terminal module (`webterminal`)
   - admin frontend (`ofgwAdmin`)
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
- when relevant, include an explicit `Scope` or `Affected Modules` section so the document does not blur `ofgwSrc`, `webterminal`, and `ofgwAdmin`

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
