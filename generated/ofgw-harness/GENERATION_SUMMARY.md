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
- manual follow-up now has a local draft workflow under `skills/docs/manual-workflow/`
- `writing-documents` keeps generated markdown rules in the main skill while also bundling selected docs guides for runtime reference
- `writing-skills` is now carried as a shared authoring baseline under `skills/authoring/`, while its source-pack support assets are ported into the product runtime
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
  - `writing-documents/markdown-guide.md`
  - `writing-documents/jira-guide.md`
  - `writing-documents/gitlab-guide.md`
  - `writing-documents/ims-guide.md`
  - `writing-documents/mail-guide.md`
  - `writing-skills/testing-skills-with-subagents.md`
  - `writing-skills/examples/AGENTS_MD_TESTING.md`
  using `ofgw` module boundaries, artifact paths, and confirmed Gradle commands
  - `confluence-guide.md`
  while keeping `docs_targets.confluence.enabled: false`; disabled target bindings no longer force guide exclusion when support-asset completeness is the current validation priority
  - `best-practices.md`
  after promoting the large vendor-heavy reference into a shared runtime-neutral authoring guide; future changes here should happen in shared `skills/writing-skills/` rather than by product-local carry-over

## Remaining Exclusions

- external manual publish workflow
- `completing-patch`
- diff-aware coverage gating beyond the current JaCoCo-based review skill

## Review Focus

- Confirm that the rebuilt tree is reproducible from current source inputs and policies.
- Confirm that default support-asset bundling is operationally tolerable before inventing exception rules.
- Confirm that carried-over base skills are normalized to standalone runtime naming.
- Keep refinement scope separate from initiator validation.
