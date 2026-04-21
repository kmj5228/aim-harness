# Refinement Evaluation: ofgw-harness

## Purpose

This document evaluates the two-skill rebuild flow:

1. rebuild `generated/ofgw-harness/` from the current `harness-initiator` contract
2. apply `product-harness-refinement` on top of that initiator-only baseline

The goal is not to maximize `ofgw-harness` completeness. The goal is to check whether the second skill makes the harness more mature without making shared interfaces or adapters unnecessarily heavy.

It is a validation artifact only. It is not a runtime skill or generation input.

## Rebuild Procedure

1. backup the current refined `generated/ofgw-harness/`
2. restore the earlier initiator-only baseline
3. re-apply the refinement layer using the current `product-harness-refinement` skill and `adapters/ofgw/mappings.yaml`
4. compare the refined result against the initiator-only baseline

## Initiator-Only Baseline

The initiator-only baseline already provided:

- standalone target tree
- normalized runtime naming
- usable core/collab/review/docs/product layout
- bound destinations such as `agent/` and `generated/manual/`
- first viable docs/review/manual skills

What it did not yet do well enough:

- separate `ofgwSrc`, `webterminal`, and `ofgwAdmin` clearly in docs-facing output guidance
- keep coverage conclusions tightly bounded to the proven `:ofgwSrc` JaCoCo workflow
- make the local manual draft contract explicit enough for repeatable operator use

## Refinement Deltas

### 1. `skills/docs/writing-documents/SKILL.md`

Maturity gain:

- now forces module-aware writing
- avoids broad wording such as implying all of OFGW changed
- prefers safer compile/test/coverage evidence over packaging-based claims

Assessment:

- meaningful usability improvement
- clearly `product_local`

### 2. `skills/review/coverage-review/SKILL.md`

Maturity gain:

- now states the command safety rule more explicitly
- now marks `ofgwSrc` as the current proven coverage boundary
- now blocks misleading extension of coverage claims to `webterminal` and `ofgwAdmin`

Assessment:

- meaningful review-safety improvement
- clearly `product_local`

### 3. `skills/docs/manual-workflow/SKILL.md`

Maturity gain:

- now uses a clearer local draft output contract
- topic-scoped manual draft path is explicit
- draft status and approval status are explicit
- verified facts and open questions are separated more clearly

Assessment:

- meaningful operator ergonomics improvement
- strongest `shared_candidate` from this pass

## Interface Cost Review

### Skill Boundary

Result: improved

- keeping `harness-initiator` and `product-harness-refinement` separate made the workflow easier to reason about
- the initiator still owns generation and structure
- refinement now owns generated-harness quality upgrades

This is clearer than pushing all improvements back into `harness-initiator`.

### Adapter Complexity

Result: slightly increased, still acceptable

New refinement schema fields now in use:

- `refinement_goal`
- `refinement_targets`
- `priority`
- `portability`
- `depends_on`
- `status`
- `result_note`

Why this is still acceptable:

- the fields live in one block under `mappings.yaml`
- each field answers a real coordination question
- no second refinement-only adapter file was introduced

Current risk:

- if more coordination fields are added too early, `mappings.yaml` will become harder to scan than the generated files it controls

Current judgment:

- not too complex yet
- but the schema should stay close to the current size until `osd` proves another field is truly necessary

## Overall Judgment

The two-skill rebuild produced a more mature harness than the initiator-only baseline.

Why:

- the generated tree is still stable and understandable
- the refined docs/review/manual skills are safer and more explicit
- the shared workflow boundary is cleaner than before

At the same time, the interface cost stayed controlled.

- `harness-initiator` did not become larger
- refinement concerns moved into a dedicated skill
- adapter complexity increased only by one small refinement schema block

## Decision

- keep the two-skill model
- keep the current refinement schema small
- treat `manual-workflow` output-contract refinement as the strongest current shared candidate
- keep `writing-documents` and `coverage-review` refinement results product-local until another product repeats the same need
