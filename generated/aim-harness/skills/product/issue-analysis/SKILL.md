---
name: issue-analysis
description: Use when an aim issue, Jira ticket, or IMS report needs triage before deciding whether to explain, configure, or fix
---

# AIM Issue Analysis

## Overview

Analyze first, act second. Determine a verdict before entering implementation work.

This generated skill keeps the reusable issue-analysis skeleton but applies `aim` bindings:

- issue wording defaults to `issue`
- Jira uses `mcp` first, then REST API fallback
- IMS uses browser access
- NotebookLM remains the default spec source
- analysis artifacts live under `agent/<topic>/analysis_report.md`

## When to Use

- Jira issue investigation
- IMS report triage
- customer symptom analysis
- pre-fix verdict determination

## Access Bindings

### Jira

- default mode: `mcp`
- location: `atlassian-rovo`
- fallback: REST API

### IMS

- default mode: `browser`
- location pattern: `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`

### Spec

- NotebookLM is the default spec source.
- Default mode is `mcp`, with `browser` fallback.
- Current target notebook: `https://notebooklm.google.com/notebook/158fe966-8a78-4a7e-a6c9-40747330edc5`
- Preferred provider source: `https://github.com/jacob-bd/notebooklm-mcp-cli`

## Workflow

1. Gather issue context from Jira and/or IMS.
2. Capture symptom, environment, and reproduction information.
3. Trace the relevant code path in `aim`.
4. Call out the main impacted surface:
   - `src/lib`, `src/common`, or `src/ulib`
   - `src/server`
   - `src/tool` or `src/util`
   - `errcode` or `msgcode`
   - `config` or `resource`
   - `test/unit/gtest` or `test/ivp`
5. Check specification or reference material through NotebookLM when applicable.
6. Determine one verdict:
   - Bug
   - Expected behavior
   - Configuration error
   - Unsupported feature
7. Save `analysis_report.md` under `agent/<topic>/`.
8. Hand off based on the verdict.

## Output Contract

Write:

- `agent/<topic>/analysis_report.md`

## Setup Notes

- If NotebookLM MCP is unavailable, use the browser fallback against the configured notebook target.
- Keep spec lookup as an explicit step; do not silently skip it just because the issue looks obvious.

Use canonical wording in generated drafts:

- issue item: `issue`
- review artifact: `MR`
- docs artifact: `markdown document`

## Verdict Handoff

- Bug:
  - hand off to base runtime design/planning skills such as `brainstorming` and `writing-plans`
- Expected behavior:
  - draft a customer-facing explanation with the generated `writing-documents` skill
- Configuration error:
  - draft a configuration or operating guide with the generated `writing-documents` skill
- Unsupported feature:
  - draft a scope clarification or request document

## Notes

- Keep `aim` repo facts in evidence and examples, not in the verdict model itself.
- Do not hardcode C/Makefile-specific reasoning into the reusable verdict structure.
