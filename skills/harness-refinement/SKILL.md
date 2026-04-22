---
name: harness-refinement
description: Use when a generated product harness already exists and needs targeted refinement of skill bodies, wording, runtime ergonomics, or product-specific workflow details without changing the core initiator flow
---

# Harness Refinement

## Overview

Refine an already generated product harness without collapsing that work back into `harness-initiator`.

**Core principle:** `harness-initiator` generates and validates the first usable draft. This skill improves the generated harness after that point.

If the current goal is to validate refinement workflow or refinement schema, state that explicitly and avoid broadening the generated harness scope just to make the draft feel more complete.

## When to Use

- a generated harness such as `generated/ofgw-harness/` already exists
- the remaining work is inside the generated harness rather than in template selection or adapter drafting
- a skill body needs product-specific semantics, stronger wording, or better runtime ergonomics
- review findings are no longer about generation correctness, but about harness usability or operational detail
- bundled support assets need a second-pass check for product fit after initial bundle + port

Do not use for:

- initial template selection
- adapter generation
- unresolved product binding confirmation
- first-pass harness generation
- structural generated-tree validation that belongs to `review-generated-harness`

Use `harness-initiator` instead when the question is still "what should be generated?" rather than "how should the generated harness be improved?"

## Inputs

- generated harness directory such as `generated/<product>-harness/`
- current adapter inputs when they still matter for product truth
- explicit refinement schema such as `refinement_goal` or `refinement_targets` when available
- review findings or observed usage gaps
- explicit product workflow requirements that were intentionally deferred from initiator scope

## Workflow

1. Identify whether the requested change belongs to refinement or initiator scope.
2. Read only the generated skill or runtime doc that needs improvement.
3. Check whether the requested behavior is already implied by adapters, refinement schema, or generated review findings.
4. Assume `harness-initiator` and `harness-support-assets` have already materialized the baseline runtime.
5. Improve the generated harness asset directly.
6. When bundled support assets exist, check whether they still fit the target product's:
   - technology stack
   - module or service boundaries
   - terminology
   - review or docs workflow
   - current runtime contract
7. Prefer small corrections that make the bundled asset honestly usable in the target product runtime.
   - if the asset only needs path, command, wording, or example cleanup, keep that work in refinement
   - if the asset reveals that first-pass stack-aware porting should have handled it already, route that defect back to `harness-support-assets`
   - if the asset reveals a missing generation rule, route that defect back to `harness-initiator` or `harness-support-assets`
8. Keep template/source history out of the generated runtime unless it is still required for traceability in a root doc.
9. Re-check the changed generated files for naming, path, and runtime consistency.
10. Compare the refined result against the initiator-only baseline when that baseline is available.
11. Record what was refined versus what should move back to initiator or adapter work.

## Typical Refinement Targets

- generated `skills/docs/*` wording, audience fit, or output conventions
- generated `skills/review/*` usability and product-safe review semantics
- generated `skills/product/*` handoff wording or output shape
- bundled support assets whose first-pass port is present but still too source-biased for the target product
- root docs such as generated `README.md` or `AGENTS.md`
- runtime ergonomics around `agent/`, `generated/manual/`, or hook expectations

## Boundaries

This skill may:

- refine generated skill bodies
- tighten output contracts inside the generated harness
- improve wording and operator ergonomics
- turn already-generated rough product skills into better usable drafts
- verify that bundled support assets still make sense for the target product's stack and workflow

This skill should not:

- redefine the base generator contract casually
- move deferred template assets into generation scope without updating initiator rules
- invent new product truth that belongs in adapters
- treat validation artifacts as runtime assets

If refinement reveals a generator defect, report it and route that change back to `harness-initiator`.
If refinement reveals that a bundled support asset should actually have been shared carry-over or excluded from first-pass productization, report that boundary issue explicitly.
If refinement finds a stack mismatch that was already strongly knowable from adapter and repo facts, treat that as a `harness-support-assets` miss first, not as a permanent refinement burden.

## Outputs

- refined generated harness files
- explicit note of what changed in refinement scope
- explicit note of any issue that should move back to initiator or adapter work
- a short evaluation of:
  - whether the harness became materially more usable than the initiator-only baseline
  - whether the adapter/schema became harder to understand
  - whether the refinement result should stay product-local or suggests a reusable pattern

## Cross-Product Discipline

Keep this skill reusable across products such as `ofgw`, `osd`, and future harness targets.

- keep the refinement skill and refinement schema generic
- keep product-specific facts in:
  - generated runtime assets
  - `refinement_targets[].source_inputs`
  - product adapters
- do not turn one product's module names, build commands, or org terms into shared refinement rules casually
- only promote a refinement pattern back into shared skill/schema behavior when it is clearly binding-neutral or has repeated across more than one product
- when in doubt, prefer a product-local refinement result over a shared rule change

## Evaluation Lens

When refinement is being validated as a workflow, do not stop at "the generated skill is better now." Also check:

- maturity gain
  - did the refined harness become more operationally usable than the initiator-only baseline?
- interface cost
  - did the adapter or schema become harder to read or maintain?
- portability
  - is the refinement outcome a product-local correction or a likely shared pattern?

Prefer a small number of clearly justified fields over a large refinement schema that tries to predict every future need.

## Suggested Refinement Schema

When refinement needs to be repeatable across products, prefer a small product-bound schema such as:

```yaml
refinement_goal:
  purpose: <why this refinement pass exists>
  current_generated_target: generated/<product>-harness/
  success_criteria:
    - <criterion>

refinement_targets:
  - target: skills/<layer>/<skill>/SKILL.md
    priority: high|medium|low
    portability: product_local|shared_candidate
    depends_on:
      - <optional earlier refinement target>
    objective: <what should improve>
    source_inputs:
      - <adapter or repo path>
    constraints:
      - <must not expand scope>
    status: queued|refined|deferred
    result_note: <optional short outcome>
```

Use it to keep refinement focused on generated runtime assets instead of reopening initiator scope accidentally.

Suggested interpretation:

- `priority`
  - tells you which refinement target to run first
- `depends_on`
  - prevents refining a later target before an earlier target has stabilized
- `status`
  - shows whether the target is still queued, already refined, or intentionally deferred
- `result_note`
  - gives a short auditable outcome without turning the schema into a changelog
- `portability`
  - marks whether the result should stay product-local or may become a reusable shared candidate later

## Decision Test

- "Need to generate, classify, bind, or validate structure" -> `harness-initiator`
- "Need to improve the generated harness that already exists" -> `harness-refinement`
