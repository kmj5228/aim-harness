# OSD Harness

## Purpose

This directory is the current generated `osd-harness` draft.

- Treat it as a standalone product harness target, not just a thin overlay.
- Core, collaboration, docs, review, and product skills are now materialized inside this generated tree.
- Template/source-only carry-over should stay in `templates/`, not inside this standalone harness.

## Active Skill Layout

- `skills/core/`
  - `brainstorming`
  - `writing-plans`
  - `executing-plans`
  - `test-driven-development`
  - `systematic-debugging`
  - `verification-before-completion`
- `skills/collab/`
  - `subagent-driven-development`
  - `dispatching-parallel-agents`
  - `using-feature-branches`
  - `requesting-code-review`
  - `receiving-code-review`
  - `finishing-a-development-branch`
- `skills/review/`
  - `code-reviewer`
  - `review-context-collector`
  - `coverage-review`
- `skills/docs/`
  - `writing-documents`
  - `manual-workflow`
- `skills/product/`
  - `issue-analysis`

## Runtime Conventions

- Topic artifacts live under `agent/<topic>/`
- Shared markdown outputs default to `agent/`
- Manual workspace defaults to `generated/manual/`
- Canonical filenames remain:
  - `analysis_report.md`
  - `design_spec.md`
  - `plan_tasks.md`

## Access Bindings

### Issue Sources

- Jira: `mcp` default, `api` fallback, location `atlassian-rovo`
- IMS: `browser` default, location `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`

### Spec Source

- NotebookLM: `mcp` default, `browser` fallback

### Review Target

- PR: `browser` default, location `http://192.168.51.106/openframe/openframe7/osd`

### Docs Target

- repo markdown: `workspace_file`, location `agent/`

### Manual Target

- manual workspace: `workspace_file`, location `generated/manual/`

## Productization Notes

- `review-context-collector` is the productized counterpart of the AIM info-collector pattern.
- `coverage-review` is the `osd` coverage counterpart built around the confirmed `test/run_coverage.sh` path.
- `manual-workflow` is the active local manual draft workflow.
- template-specific comparison material stays in `templates/`, not here.

## Deferred Scope

- generated external manual publish workflow
- generated `completing-patch`
- diff-aware coverage gating beyond the current script-based review skill
