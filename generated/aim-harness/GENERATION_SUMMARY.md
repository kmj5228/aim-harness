# Generation Summary: aim-harness

## Result

The current generation pass built `aim-harness` from the accepted initiator contract:

- template-derived outputs follow `adapters/aim/mappings.yaml` `generation_assets`
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
- meta skill:
  - `skills/meta/using-aim-harness/SKILL.md`
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
  - `skills/core/systematic-debugging/find-polluter.sh`
  - `skills/collab/subagent-driven-development/*.md`
  - `skills/core/test-driven-development/testing-anti-patterns.md`
  - `skills/review/code-reviewer/code-reviewer-prompt.md`
  - `skills/review/code-reviewer/review-synthesizer-prompt.md`
  - `skills/review/code-reviewer/test-reviewer-prompt.md`
  - `skills/review/code-reviewer/scripts/measure_diff_cov.sh`
  - `skills/docs/writing-documents/markdown-guide.md`
  - `skills/docs/writing-documents/jira-guide.md`
  - `skills/docs/writing-documents/gitlab-guide.md`
  - `skills/docs/writing-documents/ims-guide.md`
  - `skills/docs/writing-documents/mail-guide.md`
  - `skills/docs/writing-documents/confluence-guide.md`
- product/docs layer:
  - `skills/product/issue-analysis/SKILL.md`
  - `skills/docs/writing-documents/SKILL.md`
  - `skills/docs/manual-workflow/SKILL.md`
- authoring layer:
  - `skills/authoring/writing-skills/`

## Source Inputs

- analysis summary: `adapters/aim/analysis-summary.md`
- product profile: `adapters/aim/product-profile.yaml`
- mappings: `adapters/aim/mappings.yaml`
- confirmation packet: `adapters/aim/confirmation-packet.md`
- base runtime skills: reusable root `skills/`
- AIM/template source assets: `templates/aim/*`

## Applied Decisions

- `aim` repo facts stay in bindings, not template body
- generated default wording uses:
  - `issue`
  - `MR`
  - `markdown document`
- generated runtime now includes a product-local startup meta skill:
  - `skills/meta/using-aim-harness/SKILL.md`
  - this is intentionally product-local and is not promoted into root shared `skills/`
- manual flow stays in the default completion path
- manual writable target is `generated/manual/`
- `core`, `collab`, and reusable `review` skills are included when they are stack-neutral or product-neutral
- the AIM info-collector pattern is productized as `review-context-collector`
- `aim` coverage review is productized around `make gtest`
- manual follow-up now has a local draft workflow under `skills/docs/manual-workflow/`
- `writing-documents` keeps generated markdown rules in the main skill while also bundling selected docs guides for runtime reference
- `writing-skills` is now carried as a shared authoring family under `skills/authoring/`
- both the main `SKILL.md` and its shared support assets come from root `skills/writing-skills/`
- selected support prompts and helper assets are bundled next to generated skills for semantic fidelity where they still help the runtime

## Remaining Exclusions

- external manual publish workflow
- `completing-patch`
- diff-aware coverage gating beyond the current `make gtest` and optional gcovr/lcov review flow
- patch and release automation as active `aim` runtime skills

## Review Focus

- Confirm that the generated tree is reproducible from current source inputs and policies.
- Confirm that carried-over base skills are normalized to standalone runtime naming.
- Keep first-pass generation separate from later refinement work.
