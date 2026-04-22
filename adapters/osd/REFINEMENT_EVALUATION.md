# Refinement Evaluation: osd-harness

## Purpose

This document evaluates whether `osd-harness` needs additional refinement, whether `harness-initiator` applied cleanly, and whether the current refinement boundary is appropriate.

The goal is not to maximize `osd-harness` completeness. The goal is to check whether the current three-skill model is behaving correctly:

1. `harness-initiator` should produce a usable first draft
2. `harness-support-assets` should port adjacent source assets without needing a new schema
3. `harness-refinement` should remain narrow
4. shared problems should move into shared skills before adapter/schema growth is considered

It is a validation artifact only. It is not a runtime skill or generation input.

## Initiator Application Review

Current judgment: good

What the current initiator pass already did well:

- produced the standalone target tree
- kept runtime naming normalized
- materialized `agent/`, `generated/manual/`, and `hooks/`
- generated `skills/docs/`, `skills/review/`, and `skills/product/` with `osd` bindings
- avoided template/source leakage inside active runtime skills

What the pass did not do strongly enough at first:

- the carried-over `code-reviewer` workflow did not yet acknowledge the generated companion review skills

This is important because `review-context-collector` and `coverage-review` existed, but the top-level review workflow still behaved like they were optional side notes rather than connected runtime helpers.

## Observed Gap

Gap type: shared review-layer coherence

Observed issue:

- `skills/review/review-context-collector/` existed
- `skills/review/coverage-review/` existed
- `skills/review/code-reviewer/` did not explicitly orchestrate them

Why this matters:

- the generated harness looked complete structurally
- but the review layer was less operationally coherent than it appeared
- users could miss the intended review flow even though the right generated assets were present

## Correction Applied

Instead of growing `osd`-specific adapter fields, the fix was applied to the shared carried-over skill:

- updated shared `skills/code-reviewer/SKILL.md`
- synchronized generated `skills/review/code-reviewer/SKILL.md` in:
  - `generated/osd-harness/`
  - `generated/ofgw-harness/`

New shared behavior:

- if a harness provides `review-context-collector`, `code-reviewer` now treats it as the preferred context phase
- if a harness provides `coverage-review`, `code-reviewer` now treats it as the explicit coverage-evidence companion when needed

## Evaluation

### Maturity Gain

Result: meaningful

- `osd-harness` remains a first draft, but the review layer is now internally coherent
- the improvement is practical: users now have a clearer top-level review path

### Interface Cost

Result: low

- no new `osd`-specific adapter file was introduced
- no new refinement-only schema field was needed
- the fix stayed in shared skill text and review criteria

### Portability

Result: high

- this correction is not `osd`-specific
- any generated harness that includes companion review skills benefits from the same change
- this is the clearest current example of a shared skill evolution triggered by cross-product validation

## Support-Asset Productization Note

The current `osd` pass also validated the third narrow step:

- `harness-support-assets`

Confirmed on `osd`:

- `brainstorming/spec-document-reviewer-prompt.md`
- `writing-plans/plan-document-reviewer-prompt.md`
- `systematic-debugging/root-cause-tracing.md`
- `systematic-debugging/condition-based-waiting.md`
- `systematic-debugging/defense-in-depth.md`
- `subagent-driven-development/*.md`
- `review/code-reviewer/*.md`
- `test-driven-development/testing-anti-patterns.md`
- `writing-documents/markdown-guide.md`
- `writing-documents/jira-guide.md`
- `writing-documents/gitlab-guide.md`

These were improved with:

- `agent/<topic>/...` runtime paths
- `src/lib` / `src/server` / `src/tool` / `src/util` / `dist` boundary wording
- confirmed `make`, `make -C test`, and `test/run_coverage.sh` examples

Current judgment:

- this is still small enough to live inside `harness-support-assets`
- no extra schema is justified yet
- the same support-asset model used on `ofgw` carries over to `osd` with different stack facts

## Judgment

`osd-harness` is a usable first draft.

Additional `osd`-specific refinement is not mandatory before treating the current initiator pass as successful.

The main improvement found in this evaluation was not "make `osd` more custom." It was "make the shared review orchestrator actually use generated companion review skills."

That means the current three-skill boundary is still correct:

- generation and structural validation stay with `harness-initiator`
- adjacent support-asset bundle + port stays with `harness-support-assets`
- narrow generated-harness improvement stays with `harness-refinement`
- shared recurring gaps should still be fixed in shared skills before adapter/schema complexity grows

## Decision

- keep the current three-skill model
- keep the refinement schema small
- treat the current `code-reviewer` orchestration fix as a shared improvement, not an `osd`-local refinement rule
- only expand `osd`-specific refinement later if real repo usage shows a product-local gap that shared skill evolution cannot close
