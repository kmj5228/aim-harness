# Review Generated Harness: aim-harness

## Purpose

Validate whether `generated/aim-harness/` is a usable regenerated draft under the current initiator/refinement model.

This review checks structure, active skill placement, runtime consistency, and whether the generated result stays meaningfully comparable to the original `aim-harness`.

## Checklist

### 1. Target Layout Conformity

Status: pass

- expected runtime shape exists:
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

### 2. Source Separation

Status: mixed

- pass:
  - root runtime tree is separate from original `aim-harness`
  - adapter inputs live under `adapters/aim/`
- caution:
  - some source-style guide assets remain copied into generated skill directories for comparison fidelity
  - this is acceptable for the validation draft, but not ideal for a final minimal standalone runtime

### 3. Runtime Entry Consistency

Status: pass with expected difference

- generated runtime uses:
  - `AGENTS.md`
  - `hooks/`
  - `agent/<topic>/`
- original runtime used:
  - `CLAUDE.md`
  - `settings.json`
  - `using-aim-harness` injection

This is an expected model difference, not a generation defect.

### 4. Review Layer Materialization

Status: pass

- `review-context-collector` now exists explicitly
- `coverage-review` now exists explicitly
- `code-reviewer` keeps prompt/script assets nearby

### 5. Manual And Completion Scope

Status: partial

- `manual-workflow` exists as an active generated skill
- upstream MANUAL repo publication is not active in the generated runtime
- `completing-patch` is still excluded

This is the main remaining contract-level gap.

### 6. Hook Consistency

Status: pass after root-doc rewrite

- generated `hooks/session-start.sh` reads generated `AGENTS.md`
- generated hook files stay inside the regenerated tree

## Decision

- Structural regeneration: acceptable
- Semantic fidelity: meaningful but incomplete
- Main blocker to stronger equivalence:
  - missing first-class support for post-merge patch/manual workflow
  - no first-class schema for external manual repo truth
  - remaining Claude-era orchestration wording inside several copied skills
