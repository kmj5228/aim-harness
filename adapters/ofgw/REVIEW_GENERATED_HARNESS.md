# Review Generated Harness: ofgw-harness

## Purpose

This document is the output of the `review-generated-harness` phase.

It checks whether the generated `ofgw-harness` is usable as a standalone product harness draft rather than only as a generation experiment.

It is a validation artifact only. It is not a runtime skill, adapter input, or future generation source.

## Checklist

### 1. Target Layout Conformity

Status: pass

- expected top-level runtime shape exists:
  - `AGENTS.md`
  - `README.md`
  - `GENERATION_SUMMARY.md`
  - `hooks/`
  - `skills/core/`
  - `skills/collab/`
  - `skills/authoring/`
  - `skills/docs/`
  - `skills/review/`
  - `skills/product/`
  - `generated/manual/`

### 2. Active Skill and Deferred Scope Classification

Status: pass

- active reusable workflow is under `skills/*`
- the AIM info-collector pattern is now productized as `skills/review/review-context-collector/`
- `ofgw` coverage review is now productized as `skills/review/coverage-review/`
- template/source-only carry-over is no longer copied into the generated harness
- current split is acceptable for this pass

Follow-up:

- keep diff-aware coverage gating deferred until `ofgw` has a trustworthy repository-supported method
- keep external manual publish behavior deferred while local drafting stays under `skills/docs/manual-workflow/`

### 3. Source-Pack Path Leakage

Status: pass after reconstruction fix

Fixed in this review:

- `skills/core/brainstorming/SKILL.md` no longer points to a template source path

Allowed provenance notes:

- `README.md` and `GENERATION_SUMMARY.md` may mention source inputs for traceability
- source asset details should stay in `templates/`, not in a generated `references/` tree

### 4. Naming Normalization

Status: pass after reconstruction fix

Fixed in this review:

- generated carry-over skills now use standalone `name:` fields and contain no legacy `*-base` naming
- generated cross-skill references now point to standalone runtime names

Confirmed:

- generated runtime paths use `agent/` and `generated/manual/` consistently

### 5. Hook and Runtime Consistency

Status: pass

Confirmed:

- `hooks/hooks.json` contains only the generated hook definition
- `hooks/session-start.sh` reads the generated harness `AGENTS.md`

### 6. Excluded Scope Reporting

Status: pass

- `GENERATION_SUMMARY.md` still reports deferred scope explicitly
- review/manual carry-over remains visible rather than hidden

### 7. Maturity Gain

Status: pass

- compared with the initiator-only baseline, the generated harness is more explicit in docs, coverage, and manual draft behavior
- the refined manual draft contract is easier to operate without inventing publish behavior
- the refined review/docs skills reduce overstatement risk around `ofgw` module boundaries

### 8. Interface Cost

Status: pass

- the two-skill split is clearer than pushing refinement back into `harness-initiator`
- refinement schema growth is still contained inside one block in `adapters/ofgw/mappings.yaml`
- no second refinement-only adapter file was introduced

### 9. Portability

Status: pass

- `writing-documents` and `coverage-review` remain product-local refinements
- `manual-workflow` output-contract refinement is the strongest current shared candidate
- no `ofgw`-specific module facts were promoted into shared initiator/refinement rules

### 10. Support-Asset Carry-Over

Status: pass after first validation fix

Confirmed:

- default support-asset bundling materially enriches the generated runtime without introducing a new adapter schema
- adjacent support assets are useful for:
  - brainstorming
  - writing-plans
  - subagent-driven-development
  - systematic-debugging
  - test-driven-development
  - writing-skills
  - selected review helpers
  - writing-documents guides

Fixed in this review:

- source `SKILL.md` must never be copied during support-asset bundling
- adapter `generation_assets` overrides must win over default support-asset bundling
- selected support assets can and should be ported using existing repo/adapter facts rather than copied verbatim when obvious product/runtime assumptions are known
- later `ofgw` validation also showed that support prompts and guides can be ported for:
  - subagent dispatch
  - review synthesis
  - Jira / PR writing
  without adding a new schema block
- platform-bound docs guides can also use existing adapter truth:
  - `ims-guide.md`
  - `mail-guide.md`
- disabled target bindings do not have to block bundling:
  - `confluence-guide.md` is now carried as a dormant support reference even though `docs_targets.confluence.enabled` remains false
- authoring assets expose a useful shared-promotion path:
  - `writing-skills` can be carried as a shared baseline plus productized support assets
  - highly reusable authoring assets can graduate into shared root `skills/writing-skills/` after low-diff validation across products
  - the first concrete graduation was replacing the vendor-heavy `anthropic-best-practices.md` carry-over with shared `best-practices.md`

## Findings Summary

- The rebuilt generated draft is structurally valid as a standalone-target harness draft.
- The main defects found in this review were naming/path hygiene issues, not contract-level design failures.
- standalone behavior now lives under `skills/*` and runtime directories only
- source/template materials are no longer copied into the generated harness
- this is a cleaner target for a true standalone runtime bundle
- the current refined draft is measurably more usable than the initiator-only baseline without a large adapter/schema cost

## Decision

- Mark this pass as reviewed, not final.
- Use the next pass to keep initiator validation and later refinement work clearly separated.
