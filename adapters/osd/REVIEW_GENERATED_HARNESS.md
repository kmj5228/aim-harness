# Review Generated Harness: osd-harness

## Purpose

This document is the output of the `review-generated-harness` phase.

It checks whether the generated `osd-harness` is usable as a standalone product harness draft rather than only as a generation experiment.

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
  - `skills/docs/`
  - `skills/review/`
  - `skills/product/`
  - `generated/manual/`

### 2. Active Skill and Deferred Scope Classification

Status: pass

- active reusable workflow is under `skills/*`
- the AIM info-collector pattern is now productized as `skills/review/review-context-collector/`
- `osd` coverage review is now productized as `skills/review/coverage-review/`
- template/source-only carry-over is no longer copied into the generated harness
- current split is acceptable for this pass

Follow-up:

- keep diff-aware coverage gating deferred until `osd` has a trustworthy repository-supported method
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

- the generated review layer now has an explicit orchestration path through `code-reviewer`
- `review-context-collector` and `coverage-review` are no longer isolated companion skills
- this improves first-draft usability without adding `osd`-specific adapter complexity

### 8. Interface Cost

Status: pass

- the two-skill split is clearer than pushing refinement back into `harness-initiator`
- refinement schema growth is still contained inside one block in `adapters/osd/mappings.yaml`
- no second refinement-only adapter file was introduced

### 9. Portability

Status: pass

- the main improvement found in this evaluation was a shared review-orchestration rule
- the fix belongs in the shared carried-over `code-reviewer` skill, not in `osd`-only schema growth
- no extra `osd`-specific refinement field was needed to close this gap

### 10. Support-Asset Carry-Over

Status: pass after first validation

- default support-asset bundling materially enriches the generated runtime without introducing a new adapter schema
- adjacent support assets are useful for:
  - brainstorming
  - writing-plans
  - systematic-debugging
  - subagent-driven-development
  - selected review helpers
  - writing-documents guides
- support prompts and guides can be ported with existing repo and adapter facts
- `make`, `make -C test`, and `test/run_coverage.sh` are enough to rewrite many OSD-specific support assets without extra schema
- `dist/` operational flow can be kept explicit without turning packaging semantics into default runtime verification
- a second narrow pass also ports:
  - `condition-based-waiting.md`
  - `defense-in-depth.md`
  - `testing-anti-patterns.md`

## Findings Summary

- The rebuilt generated draft is structurally valid as a standalone-target harness draft.
- The main defects found in this review were naming/path hygiene issues, not contract-level design failures.
- standalone behavior now lives under `skills/*` and runtime directories only
- source/template materials are no longer copied into the generated harness
- this is a cleaner target for a true standalone runtime bundle
- the current generated draft is structurally usable without reintroducing template/source leakage
- the main maturity gap found in this review was review-layer coherence, and that gap has now been closed through the shared `code-reviewer` workflow rather than product-local schema growth
- the same three-skill support-asset model validated on `ofgw` also works on `osd`

## Decision

- Mark this pass as reviewed, not final.
- Treat `osd-harness` as a usable first draft.
- Prefer shared skill evolution over `osd`-specific adapter growth when the issue is layer-wide.
