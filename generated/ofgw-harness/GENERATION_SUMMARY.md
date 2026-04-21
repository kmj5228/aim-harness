# Generation Summary: ofgw-harness

## Result

The current reconstruction pass rebuilt `ofgw-harness` from the accepted initiator contract:

- template-derived outputs follow `adapters/ofgw/mappings.yaml` `generation_assets`
- base runtime carry-over follows the default policy in `skills/harness-initiator/SKILL.md`
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
- product/docs layer:
  - `skills/product/issue-analysis/SKILL.md`
  - `skills/docs/writing-documents/SKILL.md`
  - `skills/docs/manual-workflow/SKILL.md`

## Source Inputs

- analysis summary: `adapters/ofgw/analysis-summary.md`
- product profile: `adapters/ofgw/product-profile.yaml`
- mappings: `adapters/ofgw/mappings.yaml`
- confirmation packet: `adapters/ofgw/confirmation-packet.md`
- base runtime skills: reusable root `skills/`
- AIM/template source assets: `templates/aim/*`

## Applied Decisions

- mixed-stack `ofgw` facts stay in bindings, not template body
- generated default wording uses:
  - `issue`
  - `PR`
  - `markdown document`
- manual flow stays in the default completion path
- manual writable target is `generated/manual/`
- `core`, `collab`, and reusable `review` skills are included when they are stack-neutral or product-neutral
- the AIM info-collector pattern is productized as `review-context-collector`
- `ofgw` coverage review is productized as `coverage-review`
- manual follow-up now has a local draft workflow under `skills/docs/manual-workflow/`
- `markdown-guide` rules are absorbed into `writing-documents`
- template/source-only carry-over is not copied into the standalone harness

## Remaining Exclusions

- external manual publish workflow
- `completing-patch`
- diff-aware coverage gating beyond the current JaCoCo-based review skill
- AIM-specific MR/API automation as active `ofgw` review subskills

## Review Focus

- Confirm that the rebuilt tree is reproducible from current source inputs and policies.
- Confirm that carried-over base skills are normalized to standalone runtime naming.
- Keep refinement scope separate from initiator validation.
