# Semantic Comparison: original aim-harness vs regenerated aim-harness

## Comparison Baseline

This comparison uses semantic equivalence, not byte-level identity.

Priority order:

1. structure
2. skill responsibility
3. runtime and workflow behavior
4. operator-facing meaning

## Findings

### Regression

1. `completing-patch` is missing from the active generated runtime.
   - original: post-merge IMS patch verification is part of the official end-to-end workflow
   - regenerated: explicitly deferred
   - effect: the regenerated harness does not yet cover the full AIM lifecycle

2. Full external manual publication semantics are not reproduced.
   - original: `/Users/mjkang/company/MANUAL/openFrame_aim`, direct push to `7.3_main`, Antora/AsciiDoc
   - regenerated: local draft workflow under `generated/manual/`
   - effect: manual responsibility is only partially reproduced

3. Several regenerated skill bodies still preserve Claude-era orchestration vocabulary.
   - examples:
     - `Agent(...)`
     - `AskUserQuestion`
   - effect: role and workflow intent are preserved, but current Codex runtime operability is incomplete

### Expected Difference

1. Skill names are normalized and layered.
   - original: flat `*-aim` directories
   - regenerated: `skills/core`, `skills/collab`, `skills/review`, `skills/docs`, `skills/product`

2. Runtime artifact paths are localized.
   - original: `../agent/prompt/<topic>/`
   - regenerated: `agent/<topic>/`

3. Root runtime entry is Codex-shaped.
   - original: `CLAUDE.md`, `settings.json`
   - regenerated: `AGENTS.md`, `hooks/`, `skills/meta/using-aim-harness`

4. Review artifact terminology is normalized in adapter truth.
   - original often says `MR`
   - current generator model expects a shared review layer and explicit bindings

### Improvement

1. Review responsibilities are split more clearly.
   - original: `code-reviewer` contains context-gathering and coverage concepts internally
   - regenerated: `review-context-collector` and `coverage-review` are explicit helper skills

2. Generation inputs are now auditable.
   - `adapters/aim/product-profile.yaml`
   - `adapters/aim/mappings.yaml`
   - this makes AIM-specific truth easier to inspect than the original inline-only binding model

3. Generated runtime boundaries are clearer.
   - source pack, adapter truth, generated runtime are physically separated
   - this is better for future regeneration and maintenance than the original all-in-one layout

4. The original `using-aim-harness` entry model is now reproduced as a first-class generated runtime asset.
   - original: `CLAUDE.md` + `settings.json` + SessionStart hook injects `using-aim-harness`
   - regenerated: `AGENTS.md` + Codex hook + generated `skills/meta/using-aim-harness`
   - effect: startup routing and skill-gap reporting are materially closer to the original AIM contract than before

## Evaluation

### Structural Similarity

High.

- high:
  - comparable root runtime docs and hook presence
  - generated startup meta skill now exists
  - comparable full-skill workflow coverage for design, planning, execution, review, docs
- lower:
  - no active `completing-patch`

### Skill Responsibility Similarity

High for:

- issue analysis
- document writing
- code review
- TDD/debug/verification loop
- branch and MR workflow

Medium for:

- manual flow
- post-merge workflow tail

### Runtime / Hook / Workflow Similarity

Medium-high.

- workflow chain is still recognizable
- issue -> design -> plan -> execute -> verify -> finish -> review survives
- startup enforcement is now materially closer because the generated runtime includes `using-aim-harness`
- post-merge patch/manual tail is only partially preserved

## Summary Judgment

- Reproducibility: meaningful
- Reproducibility of startup/runtime entry: strong
- Reproducibility of full AIM lifecycle: incomplete
- Main missing capability: explicit schema and generation support for:
  - `completing-patch`
  - external manual repo publication
