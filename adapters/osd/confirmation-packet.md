# OSD Confirmation Packet

## Inferred Facts

- repo uses `make` as the primary build entry point
- repository contains C/C++ code plus shell-based operational scripts
- repo-native coverage entry point exists at `test/run_coverage.sh`
- repo-native patch packaging entry point exists at `dist/patch_osd.sh`
- repo markdown workspace can likely use `agent/`
- browser review target is likely `http://192.168.51.106/openframe/openframe7/osd`
- Jira MCP binding can follow the same org-level pattern already used in `ofgw`
- local manual draft workflow can default to enabled under `generated/manual/`

## Needs Confirmation

### Issue Access

- no required unresolved value remains
- current draft:
  - `access_bindings.issue_sources.jira.enabled: true`
  - `default_mode: mcp`
  - `fallback: api`
  - `auth_source: agent/info/access.md`
- interpretation: use the same Jira MCP + API fallback shape as `ofgw`

### Spec Access

- no required unresolved value remains
- current draft:
  - `access_bindings.spec_sources.notebooklm.enabled: true`
  - `default_mode: mcp`
  - `fallback: browser`
  - `location: https://notebooklm.google.com/notebook/158fe966-8a78-4a7e-a6c9-40747330edc5`
- interpretation: use the same NotebookLM setup shape as `ofgw` for the first draft

### Manual Policy

- `workflow.defaults.manual_workflow_required`
  - current draft: `true`
- `access_bindings.manual_targets.manual_repo.enabled`
  - current draft: `true`
- `access_bindings.manual_targets.manual_repo.location`
  - current draft: `generated/manual/`
  - interpretation: local manual draft workflow is enabled by default, using the same generated workspace policy as `ofgw`

## Red Flags

- `test/run_coverage.sh` is useful but environment-dependent
  - it assumes `OPENFRAME_ROOT`
  - it stages runtime libs
  - it writes under `/tmp`
- `dist/patch_osd.sh` and `dist/dist_osd.sh` are strong candidates for later `completing-patch` work
  - but they are too operationally coupled for first-pass generation
- repo facts support a review/coverage layer, but not yet enough to prove exact policy thresholds

## Proposed Next Step

1. keep `completing-patch` deferred for the first `osd` generation pass
2. generate an `osd-harness` first draft with:
   - `issue-analysis`
   - `writing-documents`
   - `review-context-collector`
   - `coverage-review`
   - local `manual-workflow`
