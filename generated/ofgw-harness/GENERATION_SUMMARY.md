# Generation Summary: ofgw-harness

## Result

The current reconstruction pass rebuilt `ofgw-harness` from the accepted initiator contract:

- template-derived outputs follow `adapters/ofgw/mappings.yaml` `generation_assets`
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
  - `skills/meta/using-ofgw-harness/SKILL.md`
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
- authoring skills:
  - `skills/authoring/writing-skills/SKILL.md`
- review skill:
  - `skills/review/code-reviewer/SKILL.md`
  - `skills/review/review-context-collector/SKILL.md`
  - `skills/review/coverage-review/SKILL.md`
- bundled support assets:
  - `skills/core/brainstorming/spec-document-reviewer-prompt.md`
  - `skills/core/writing-plans/plan-document-reviewer-prompt.md`
  - `skills/collab/subagent-driven-development/*.md`
  - `skills/core/systematic-debugging/*`
  - `skills/core/test-driven-development/testing-anti-patterns.md`
  - `skills/review/code-reviewer/code-reviewer-prompt.md`
  - `skills/review/code-reviewer/review-synthesizer-prompt.md`
  - `skills/review/code-reviewer/test-reviewer-prompt.md`
  - `skills/docs/writing-documents/markdown-guide.md`
  - `skills/docs/writing-documents/jira-guide.md`
  - `skills/docs/writing-documents/gitlab-guide.md`
  - `skills/docs/writing-documents/ims-guide.md`
  - `skills/docs/writing-documents/mail-guide.md`
  - `skills/docs/writing-documents/confluence-guide.md`
  - `skills/authoring/writing-skills/best-practices.md`
  - `skills/authoring/writing-skills/persuasion-principles.md`
  - `skills/authoring/writing-skills/testing-skills-with-subagents.md`
  - `skills/authoring/writing-skills/graphviz-conventions.dot`
  - `skills/authoring/writing-skills/render-graphs.js`
  - `skills/authoring/writing-skills/examples/AGENTS_MD_TESTING.md`
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
- the legacy coverage helper role is now also represented as an experimental repo-native script under `skills/review/code-reviewer/scripts/measure_diff_cov.sh`
- manual follow-up now has a local draft workflow under `skills/docs/manual-workflow/`
- `writing-documents` keeps generated markdown rules in the main skill while also bundling selected docs guides for runtime reference
- `writing-skills` is now carried as a shared authoring family under `skills/authoring/`
- both the main `SKILL.md` and its shared support assets come from root `skills/writing-skills/`
- generated runtime now includes a product-local startup meta skill:
  - `skills/meta/using-ofgw-harness/SKILL.md`
  - this is intentionally product-local and is not promoted into root shared `skills/`
- a later rebuild reproducibility check confirmed that the current OFGW runtime can be re-materialized from the current three-skill contract
- the only initial live drift was three `writing-skills` shared-family files that were still one step behind the whole-family carry-over policy; they have since been resynced to the shared baseline
- later support-asset/refinement passes tightened `testing-anti-patterns.md` into a JUnit 5 / Mockito / Kotlin-Java service guide after first-pass porting still underfit the actual `ofgw` stack
- after the first OFGW pass, the old vendor-heavy `anthropic-best-practices.md` reference was replaced with shared `best-practices.md`
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
  - `review/code-reviewer/scripts/measure_diff_cov.sh`
  - `writing-documents/markdown-guide.md`
  - `writing-documents/jira-guide.md`
  - `writing-documents/gitlab-guide.md`
  - `writing-documents/ims-guide.md`
  - `writing-documents/mail-guide.md`
  - `writing-skills/testing-skills-with-subagents.md`
  - `writing-skills/examples/AGENTS_MD_TESTING.md`
  using `ofgw` module boundaries, artifact paths, and confirmed Gradle commands
  - `review/code-reviewer/scripts/measure_diff_cov.sh`
  as an experimental helper rewritten around `git diff` plus JaCoCo XML rather than the original AIM `gcov` workflow
  - `confluence-guide.md`
  while keeping `docs_targets.confluence.enabled: false`; disabled target bindings no longer force guide exclusion when support-asset completeness is the current validation priority
  - `best-practices.md`
  after promoting the large vendor-heavy reference into a shared runtime-neutral authoring guide; future changes here should happen in shared `skills/writing-skills/` rather than by product-local carry-over
- a second fit-check pass also tightened the generated review prompts so they speak more directly in OFGW's Kotlin/JPA/QueryDSL/JUnit/JaCoCo terms and keep `ofgwSrc` as the default verified boundary

## Remaining Exclusions

- external manual publish workflow
- `completing-patch`
- diff-aware coverage gating beyond the current JaCoCo-based review skill

## Review Focus

- Confirm that the rebuilt tree is reproducible from current source inputs and policies.
- Confirm that default support-asset bundling is operationally tolerable before inventing exception rules.
- Confirm that carried-over base skills are normalized to standalone runtime naming.
- Keep refinement scope separate from initiator validation.
