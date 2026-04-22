# Generation Summary: osd-harness

## Result

The current generation pass built `osd-harness` from the accepted initiator contract:

- template-derived outputs follow `adapters/osd/mappings.yaml` `generation_assets`
- base runtime carry-over follows the default policy in `skills/harness-initiator/SKILL.md`
- adjacent support assets are bundled by default through `skills/harness-support-assets/SKILL.md`
- wording and runtime contract strengthening are applied through `skills/harness-refinement/SKILL.md`
- the generated tree keeps standalone runtime naming and does not reintroduce legacy `*-base` names

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
- meta skill:
  - `skills/meta/using-osd-harness/SKILL.md`
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
- review skill:
  - `skills/review/code-reviewer/SKILL.md`
  - `skills/review/review-context-collector/SKILL.md`
  - `skills/review/coverage-review/SKILL.md`
- bundled support assets:
  - `skills/core/brainstorming/spec-document-reviewer-prompt.md`
  - `skills/core/writing-plans/plan-document-reviewer-prompt.md`
  - `skills/core/systematic-debugging/root-cause-tracing.md`
  - `skills/core/systematic-debugging/condition-based-waiting.md`
  - `skills/core/systematic-debugging/defense-in-depth.md`
  - `skills/collab/subagent-driven-development/*.md`
  - `skills/core/test-driven-development/testing-anti-patterns.md`
  - `skills/review/code-reviewer/code-reviewer-prompt.md`
  - `skills/review/code-reviewer/review-synthesizer-prompt.md`
  - `skills/review/code-reviewer/test-reviewer-prompt.md`
  - `skills/docs/writing-documents/markdown-guide.md`
  - `skills/docs/writing-documents/jira-guide.md`
  - `skills/docs/writing-documents/gitlab-guide.md`
- product/docs layer:
  - `skills/product/issue-analysis/SKILL.md`
  - `skills/docs/writing-documents/SKILL.md`
  - `skills/docs/manual-workflow/SKILL.md`
- authoring layer:
  - `skills/authoring/writing-skills/`

## Source Inputs

- analysis summary: `adapters/osd/analysis-summary.md`
- product profile: `adapters/osd/product-profile.yaml`
- mappings: `adapters/osd/mappings.yaml`
- confirmation packet: `adapters/osd/confirmation-packet.md`
- base runtime skills: reusable root `skills/`
- AIM/template source assets: `templates/aim/*`

## Applied Decisions

- `osd` repo facts stay in bindings, not template body
- generated default wording uses:
  - `issue`
  - `PR`
  - `markdown document`
- generated runtime now includes a product-local startup meta skill:
  - `skills/meta/using-osd-harness/SKILL.md`
  - this is intentionally product-local and is not promoted into root shared `skills/`
- manual flow stays in the default completion path
- manual writable target is `generated/manual/`
- `core`, `collab`, and reusable `review` skills are included when they are stack-neutral or product-neutral
- the AIM info-collector pattern is productized as `review-context-collector`
- `osd` coverage review is productized around `test/run_coverage.sh`
- manual follow-up now has a local draft workflow under `skills/docs/manual-workflow/`
- `writing-documents` keeps generated markdown rules in the main skill while also bundling selected docs guides for runtime reference
- `writing-skills` is now carried as a shared authoring family under `skills/authoring/`
- both the main `SKILL.md` and its shared support assets come from root `skills/writing-skills/`
- support assets are copied into the standalone harness next to their generated skills by default
- adapter-explicit `generation_assets` exceptions override default support-asset bundling
- a first narrow porting pass was applied to selected support assets:
  - `brainstorming/spec-document-reviewer-prompt.md`
  - `writing-plans/plan-document-reviewer-prompt.md`
  - `systematic-debugging/root-cause-tracing.md`
  - `subagent-driven-development/spec-reviewer-prompt.md`
  - `subagent-driven-development/implementer-prompt.md`
  - `subagent-driven-development/code-quality-reviewer-prompt.md`
  - `review/code-reviewer/*.md`
  - `writing-documents/markdown-guide.md`
  - `writing-documents/jira-guide.md`
  - `writing-documents/gitlab-guide.md`
  - `systematic-debugging/condition-based-waiting.md`
  - `systematic-debugging/defense-in-depth.md`
  - `test-driven-development/testing-anti-patterns.md`
  using OSD module boundaries, artifact paths, and confirmed `make` / `make -C test` / `test/run_coverage.sh` commands

## Remaining Exclusions

- external manual publish workflow
- `completing-patch`
- diff-aware coverage gating beyond the current script-based coverage review
- operational patch/distribution automation as active `osd` runtime skills

## Review Focus

- Confirm that the generated tree is reproducible from current source inputs and policies.
- Confirm that default support-asset bundling is operationally tolerable before inventing exception rules.
- Confirm that carried-over base skills are normalized to standalone runtime naming.
- Keep first-pass generation separate from later refinement work.

## Rebuild Validation

- a later cross-product rebuild check confirmed that the current OSD runtime can be re-materialized from the current three-skill contract
- the rebuilt tree and the live `generated/osd-harness/` matched exactly after adding:
  - `runtime_entry`
  - stronger generated `AGENTS.md`
  - `skills/meta/using-osd-harness/SKILL.md`
  - shared `skills/writing-skills/` whole-family carry-over under `skills/authoring/`
