# Generation Summary: aim-harness

## Result

This reconstruction pass rebuilt `aim-harness` under the current initiator/refinement contract:

- template-derived outputs follow `adapters/aim/mappings.yaml`
- generated layout follows the current layered runtime model
- semantic AIM content was re-materialized where the current model can carry it without touching the original repo

Generated:

- root metadata:
  - `AGENTS.md`
  - `README.md`
  - `GENERATION_SUMMARY.md`
- runtime materialization:
  - `agent/README.md`
  - `generated/manual/README.md`
  - `hooks/README.md`
  - `hooks/config.toml`
  - `hooks/hooks.json`
  - `hooks/session-start.sh`
- core skills:
  - `skills/core/brainstorming/SKILL.md`
  - `skills/core/writing-plans/SKILL.md`
  - `skills/core/executing-plans/SKILL.md`
  - `skills/core/test-driven-development/SKILL.md`
  - `skills/core/systematic-debugging/SKILL.md`
  - `skills/core/verification-before-completion/SKILL.md`
- collab skills:
  - `skills/collab/subagent-driven-development/SKILL.md`
  - `skills/collab/dispatching-parallel-agents/SKILL.md`
  - `skills/collab/using-feature-branches/SKILL.md`
  - `skills/collab/requesting-code-review/SKILL.md`
  - `skills/collab/receiving-code-review/SKILL.md`
  - `skills/collab/finishing-a-development-branch/SKILL.md`
- review layer:
  - `skills/review/code-reviewer/SKILL.md`
  - `skills/review/review-context-collector/SKILL.md`
  - `skills/review/coverage-review/SKILL.md`
- product/docs layer:
  - `skills/product/issue-analysis/SKILL.md`
  - `skills/docs/writing-documents/SKILL.md`
  - `skills/docs/manual-workflow/SKILL.md`

## Source Inputs

- analysis summary: `adapters/aim/analysis-summary.md`
- product profile: `adapters/aim/product-profile.yaml`
- mappings: `adapters/aim/mappings.yaml`
- original runtime evidence:
  - `/home/woosuk_jung/harness/aim-harness/README.md`
  - `/home/woosuk_jung/harness/aim-harness/CLAUDE.md`
  - `/home/woosuk_jung/harness/aim-harness/settings.json`
- AIM/template source assets: `templates/aim/*`

## Applied Decisions

- normalize the runtime into the current generated layered layout
- preserve AIM-specific operational truth in generated skill bodies where possible:
  - `dx`
  - `rb_73`
  - IMS/Jira/GitLab MR
  - NotebookLM
  - diff coverage `>= 80%`
- normalize artifact outputs to `agent/<topic>/`
- keep manual drafting inside `generated/manual/`
- promote the original info-collector and coverage concepts into explicit review helper skills

## Remaining Exclusions

- active generated `completing-patch`
- full external MANUAL repository publish flow
- first-class regeneration of `using-aim-harness`
- complete Codex-native rewrite of Claude-era agent orchestration instructions

## Review Focus

- compare regenerated structure against the original harness role, not byte identity
- separate expected model differences from actual regressions
- identify which missing pieces require schema growth rather than more template copying
