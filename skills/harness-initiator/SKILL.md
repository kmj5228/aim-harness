---
name: harness-initiator
description: Use when adapting product-bound source assets into a new product harness by analyzing template candidates, drafting adapter files, confirming unresolved operational gaps, and generating a first harness draft
---

# Harness Initiator

## Overview

Turn product-bound source assets into a first product harness draft without rewriting everything by hand.

**Core principle:** Separate inferred facts, unresolved operational gaps, and generated output. Do not let guesses become adapter truth.

This skill is the first-class deliverable. Generated product harnesses are downstream validation targets, not the primary artifact of this round.

## When to Use

- A new product harness such as `ofgw-harness` needs to be derived from existing product-bound assets
- Existing source assets contain reusable workflow plus product-specific bindings that need to be split
- You need adapter drafts before generating a product harness
- You want to validate whether the current template boundary is sufficient for a first generated harness

Do not use for:

- ordinary feature development inside one repository
- direct cleanup of all product-specific assets at once
- manual-guide / patch-completion style workflows that are still ops-locked

## First-Run Scope

Current first-pass template scope:

- `issue-analysis`
- `writing-documents`
- `markdown-guide`

Interpretation:

- `issue-analysis` and `writing-documents` are the main template candidates.
- `markdown-guide` behaves more like a shared support reference than a full workflow template.
- Mixed-stack repositories such as `ofgw` may inform adapter facts, but they must not force the template body to become JavaScript-, Gradle-, or JVM-specific. Many target products may still be C-based.

Current excluded scope:

- `completing-patch`
- `manual-guide`
- coverage-specific prompt/script assets

## Required Inputs

- selected template source pack or template candidates
- target repository to inspect
- target product name
- current artifact workspace for notes and drafts

Optional but useful:

- known issue or review system
- known access mode such as `mcp`, `browser`, `api`, `workspace_file`
- known access location such as repo path or URL
- known release/manual workflow policy

## Workflow

### Phase 1: Analyze

Goal:
- inspect the selected template candidates and the target repository
- identify reusable workflow, binding candidates, and obvious exclusion areas

Produce:
- analysis summary
- inferred repository facts
- template applicability notes
- red flags

Stop if:
- the target repository cannot be inspected
- the selected source assets are too ambiguous to classify

### Phase 2: Draft Adapter

Goal:
- translate inferred repository facts into adapter drafts
- keep inferred values separate from unresolved values

Produce:
- `adapters/<product>/product-profile.yaml` draft
- `adapters/<product>/mappings.yaml` draft
- inferred-vs-unresolved field list

Rules:
- fill only codebase-derived facts directly
- leave unresolved operational fields as explicit gaps
- do not invent policy values

### Phase 3: Confirm Gaps

Goal:
- present unresolved operational questions for human confirmation

Typical grouped questions:
- issue access
- review access
- docs access
- notebook or manual access

Produce:
- confirmation checklist or unresolved-items report
- accepted assumptions
- user-confirmed values

Hard gate:
- do not generate a harness before this phase is resolved

Preferred report shape:

- `Inferred Facts`
- `Needs Confirmation`
- `Red Flags`
- `Proposed Next Step`

Group unresolved questions by:

- access bindings
- release/manual policy
- terminology

Track each unresolved item as one of:

- `confirmed`
- `deferred`
- `unknown`

Do not proceed to generation while any required item remains `unknown`.

### Phase 4: Generate Harness

Goal:
- apply the confirmed adapter to the selected templates and generate a first harness draft

Produce:
- `generated/<product>-harness/`
- generation summary
- excluded-items list

Report explicitly:
- what was generated
- what was skipped
- what remains ops-locked or unresolved

For the first validation pass, keep the generated skeleton minimal:

- root metadata such as `AGENTS.md`, `README.md`, and `GENERATION_SUMMARY.md`
- generated drafts for `skills/product/issue-analysis/` and `skills/docs/writing-documents/`
- `references/markdown-guide.md` as carried support reference

Do not treat missing `hooks/`, `profiles/`, `skills/core/`, or `skills/collab/` as first-pass failure.

## Output Contract

Expected core outputs:

- analysis summary
- `product-profile.yaml` draft
- `mappings.yaml` draft
- confirmation report
- generated harness draft

Core skills should refer to logical artifacts such as:

- `analysis_report`
- `design_spec`
- `implementation_plan`

Do not assume a fixed root path unless the active runtime defines one.

## First Validation Target

For the first validation pass, success means the skill preserves the full contract:

- analyze selected templates and report exclusions explicitly
- draft `product-profile.yaml` and `mappings.yaml`
- produce a grouped confirmation packet
- after confirmation, generate only a minimal harness draft for the selected template scope

For the current `ofgw` validation target, the selected scope is:

- `issue-analysis`
- `writing-documents`
- `markdown-guide` as support reference only

Do not treat first-pass success as:

- a full `ofgw-harness` rollout
- proof that mixed-stack `ofgw` facts should rewrite the template body
- permission to silently include excluded assets such as `completing-patch`

## First Build Readiness

At the current design stage:

- `analyze`, `draft-adapter`, and `confirm-gaps` are ready to execute
- `generate-harness` is blocked until the first adapter draft is reviewed and required unresolved values are no longer `unknown`

Treat the next run as a real draft attempt, not as another abstract design pass.

## Common Mistakes

- Trying to convert every product-bound asset in one pass
- Treating codebase guesses as confirmed operational policy
- Letting a mixed-stack validation target overfit the template body to one stack
- Generating the harness before user confirmation
- Hiding excluded assets instead of reporting them
- Letting source-pack cleanup and harness generation become one uncontrolled refactor

## Integration

Pairs with:

- `writing-skills-base` — if the initiator workflow itself needs revision
- `brainstorming-base` — when the generation approach or boundary still needs design work
- `writing-plans-base` — when the initiator implementation itself needs a task breakdown

Produces drafts for:

- `adapters/<product>/product-profile.yaml`
- `adapters/<product>/mappings.yaml`
- `generated/<product>-harness/`

## Adapter Draft Contract

Start with exactly two adapter files:

- `product-profile.yaml`
- `mappings.yaml`

`product-profile.yaml` should capture:

- product name
- inferred repository facts
- inferred commands
- human-confirmed workflow defaults
- a `confirm` list for unresolved values

`mappings.yaml` should capture:

- source pack name
- target product name
- terminology mapping
- command bindings
- provider-style access and integration bindings
- a `confirm` list for unresolved mappings

Do not expand the schema early unless repeated generation attempts show a stable need.
