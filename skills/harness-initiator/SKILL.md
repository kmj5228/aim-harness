---
name: harness-initiator
description: Use when adapting product-bound source assets into a new product harness by analyzing template candidates, drafting adapter files, confirming unresolved operational gaps, and generating a first harness draft
---

# Harness Initiator

## Overview

Turn template source assets into a first product harness draft without rewriting everything by hand.

**Core principle:** Separate inferred facts, unresolved operational gaps, and generated output. Do not let guesses become adapter truth.

This skill is the first-class deliverable. Generated product harnesses are downstream validation targets, but the long-term target is still a standalone product harness rather than a thin overlay.

## Layer Model

Treat skill sources as three different layers, not as duplicate files.

- root `skills/`
  - shared normalized runtime skills
  - stack-neutral carry-over source for generated `skills/core/`, `skills/collab/`, and shared review runtime
- `templates/<pack>/skills/`
  - source-fidelity product/template skills
  - used when initiator needs source workflow wording, startup semantics, or skill-adjacent support asset
- `generated/<product>-harness/skills/`
  - product runtime v1
  - the generated result after carry-over, productization, and path/name normalization

Do not delete `templates/<pack>/skills/<skill>/SKILL.md` just because root `skills/<skill>/SKILL.md` also exists.
The template-side `SKILL.md` is the anchor for interpreting adjacent support assets and source workflow semantics.

## When to Use

- A new product harness such as `ofgw-harness` needs to be derived from existing template source assets
- Existing source assets contain reusable workflow plus product-bound bindings that need to be split
- You need adapter drafts before generating a product harness
- You want to validate whether the current template boundary is sufficient for a first generated harness

## Responsibility Boundary

`harness-initiator` is responsible for:

- selecting template scope
- extracting binding candidates
- drafting adapters
- confirming unresolved gaps
- generating the first product harness draft
- reviewing the generated harness for structural correctness
- defining explicit generation rules for template-derived assets

`harness-initiator` is not the long-term owner of:

- polishing full product-specific skill bodies
- evolving review/manual/coverage workflow semantics after the first viable generated draft exists
- ongoing authoring work inside an already generated standalone harness

Treat those as generated harness refinement work, not as core initiator responsibility.

Do not use for:

- ordinary feature development inside one repository
- direct cleanup of every template pack at once
- manual-guide / patch-completion style workflows that are still ops-locked
- ongoing product-skill refinement after the generated harness already has a usable first draft

## First-Run Scope

Current first-pass template scope:

- `AGENTS.template.md`
- `issue-analysis`
- `writing-documents`
- `markdown-guide`

Interpretation:

- `AGENTS.template.md` is the source of generated runtime entry and top-level harness rule text when a source pack carries a strong startup contract.
- `issue-analysis` and `writing-documents` are the main template candidates.
- `markdown-guide` behaves more like a shared support reference than a full workflow template.
- source packs may include skill-adjacent support assets next to `SKILL.md`; initiator should treat them as source material, not as accidental clutter.
- Mixed-stack repositories such as `ofgw` may inform adapter facts, but they must not force the template body to become JavaScript-, Gradle-, or JVM-specific. Many target products may still be C-based.

Current excluded scope:

- `completing-patch`
- `manual-guide`
- coverage-specific prompt/script assets

Interpretation:

- the full source body for `manual-guide` remains excluded while external publish behavior is still unbound
- a reduced local `manual-workflow` may still be generated when only reusable gate and draft-first semantics are absorbed
- diff-aware or policy-heavy coverage automation remains excluded until a product-bound coverage workflow exists

## Runtime Entry Contract

When adapter truth includes `runtime_entry`, treat it as a standard initiator contract rather than an ad hoc product note.

Minimum supported fields:

```yaml
runtime_entry:
  hook_event: SessionStart
  matcher: startup|resume|clear|compact
  inject_artifact: AGENTS.md
  startup_contract:
    require_skill_check: true|false
    enforce_skill_routing: true|false
    require_skill_gap_reporting: true|false
    preserve_workflow_chain: true|false
    deferred_tail:
      - <optional workflow item>
```

Interpretation:

- `hook_event`
  - the session lifecycle event the generated harness binds to
- `matcher`
  - the generated hook trigger pattern
- `inject_artifact`
  - the top-level runtime artifact injected on session entry
- `startup_contract.require_skill_check`
  - whether the generated runtime must force an explicit skill-first check before ad hoc work
- `startup_contract.enforce_skill_routing`
  - whether the generated runtime must route common tasks through the declared harness skills
- `startup_contract.require_skill_gap_reporting`
  - whether missing-skill situations must be surfaced explicitly
- `startup_contract.preserve_workflow_chain`
  - whether the generated runtime should keep a default ordered workflow chain visible at startup
- `startup_contract.deferred_tail`
  - workflow items intentionally left outside the generated base runtime

Generation rule:

- if `AGENTS.template.md` exists, generated `AGENTS.md` should derive its runtime contract from that source plus `runtime_entry`
- generated `hooks/hooks.json` and `hooks/session-start.sh` must match the same `runtime_entry` truth
- do not let startup wording, hook matcher, and deferred-tail reporting drift independently

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

Recommended three-skill sequence:

1. `harness-initiator`
   - generate the first standalone skeleton and product-bound runtime v1
2. `harness-support-assets`
   - bundle source-pack support assets next to the generated skills
3. `harness-refinement`
   - improve wording, ergonomics, or product-local usability only after the bundled runtime exists

## Fresh Generation vs Rebuild Validation

Treat fresh generation and rebuild validation as different modes.

- fresh generation
  - a new product or a new product setup pass where adapter truth is not yet fully confirmed
  - existing `adapters/<product>/` content may be read as context, but it must not be silently treated as confirmed input
  - existing `generated/<product>-harness/` content is reference-only for comparison and must not be used as generation input
  - unresolved or draft-default values still require explicit user confirmation before generation
- rebuild validation
  - a reproducibility check for an already accepted adapter truth
  - existing `adapters/<product>/` content may be reused as canonical input when the goal is to verify parity or regeneration quality
  - existing `generated/<product>-harness/` content may be used only as a validation target or diff target, never as the source pack

Generation rule:

- do not silently reuse adapter values just because files already exist under `adapters/`
- do not treat `generated/` as authoritative truth for the next generation pass
- when in doubt, show the user:
  - reused confirmed truth
  - inferred facts
  - needs confirmation
- when reusing existing adapter truth during rebuild validation, make that reuse explicit in the confirmation/report output

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
- combine codebase-derived facts with template-inherited binding candidates
- keep inferred values separate from unresolved values

Produce:
- `adapters/<product>/product-profile.yaml` draft
- `adapters/<product>/mappings.yaml` draft
- inferred-vs-unresolved field list
- a user-facing `fill-now` list of concrete unresolved values

Rules:
- fill only codebase-derived facts directly
- carry template-inherited access patterns as suggested defaults, not as confirmed product truth
- leave unresolved operational fields as explicit gaps
- do not invent policy values
- after the first adapter draft, always show the user the exact values that still need to be filled
- for each unresolved value, include:
  - field path
  - current draft value
  - short meaning
  - expected answer shape
  - recommended value only when repo or org evidence makes one plausible

Extraction checklist:

- scan selected templates for explicit URL patterns, repo paths, notebook targets, API snippets, and mode hints such as `mcp`, `browser`, `api`, `workspace_file`
- map those inline patterns to `access_bindings.*` candidates
- distinguish generated runtime conventions such as artifact paths or workspace placeholders from provider bindings
- keep ops-locked prompts/scripts as excluded assets unless the current pass explicitly absorbs them
- record source-asset handling in `generation_assets` using only:
  - `generate`
  - `absorb`
  - `absorb_partial`
  - `defer`
  - `stay_in_templates`

Draft default bias:

- when org-level evidence already supports the same integration shape across products, prefer:
  - Jira:
    - `enabled: true`
    - `default_mode: mcp`
    - `fallback_modes: [api]`
    - `location: atlassian-rovo`
  - local manual workspace:
    - `manual_workflow_required: true`
    - `manual_repo.enabled: true`
    - `manual_repo.default_mode: workspace_file`
    - `manual_repo.location: generated/manual/`
- treat these as draft defaults for user-config minimization, not as irreversible truth
- if repo or product evidence conflicts, the adapter may still override or reopen them

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

- `Reused Confirmed Truth`
- `Inferred Facts`
- `Needs Confirmation`
- `Fill Now`
- `Red Flags`
- `Proposed Next Step`

`Reused Confirmed Truth` rule:

- include this block whenever an existing accepted adapter contributes values to the current pass
- list only values that are being treated as canonical reuse
- do not mix reused values into `Inferred Facts`

`Fill Now` rule:

- always present the unresolved values as a short fill-in list immediately after the first adapter draft
- do not hide them only inside prose
- keep the list answerable in one reply
- prefer exact field paths over vague labels

Preferred item shape:

- `<field path>`
  - current draft: `<value>`
  - meaning: `<what this controls>`
  - answer shape: `<true|false|path|url|enum>`
  - recommended: `<value or none>`

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
- handoff note for `harness-support-assets` when the source pack contains adjacent support assets

Report explicitly:
- what was generated
- what was skipped
- what remains ops-locked or unresolved

Entry and support-asset generation rules:

- if the selected source pack includes `AGENTS.template.md`, generated `AGENTS.md` should be derived from it rather than written as a thin summary from scratch
- when adapter truth includes `runtime_entry`, use it as the generation contract for:
  - hook matcher
  - startup injection artifact
  - strength of startup rules in generated `AGENTS.md`
- remove source-runtime-specific wording only when it conflicts with the target runtime contract
  - example: Claude-specific file naming or tool wording
- preserve startup governance, workflow chain, routing rules, and skill-gap reporting when they are still meaningful in the target runtime
- generated `AGENTS.md` should read like a runtime constitution, not a layout memo
- generated `AGENTS.md` should explicitly state:
  - when the harness must check skills
  - how skill routing works
  - what the default workflow chain is
  - what tail workflows remain deferred
- generated `AGENTS.md` minimum checklist:
  - runtime contract
  - startup rule strength
  - skill use rules
  - skill routing
  - default workflow chain
  - active skill layout
  - runtime conventions
  - access-binding summary only when it materially affects runtime behavior
  - deferred scope
- if a template skill contains adjacent support assets, initiator should hand that source scope to `harness-support-assets`
- keep initiator focused on:
  - selecting which source skills participate in generation
  - honoring explicit `generation_assets` overrides
  - emitting a clear handoff note for support-asset materialization
- while this rule was motivated by AIM source-fidelity work, the first validation target for the new bundling and AGENTS-template behavior should still be `ofgw-harness`, not `aim-harness`

Long-term target layout:

- root metadata such as `AGENTS.md` and `README.md`
- `hooks/`
- `skills/meta/`
- `skills/core/`
- `skills/collab/`
- `skills/authoring/`
- `skills/docs/`
- `skills/review/`
- `skills/product/`
- materialized workspace bindings such as `agent/` and `generated/manual/` when confirmed

Second-pass bundling criteria:

- include `skills/core/` when the base skill is stack-neutral and already follows the artifact contract
- include `skills/collab/` when the workflow is product-neutral and does not depend on AIM-only systems
- include `skills/review/` when the review layer can be expressed as reusable review workflow plus product-bound bindings
- promote source review context-collector patterns into active `skills/review/` when provider bindings are confirmed and outputs can be normalized into local artifacts
- promote product-safe coverage workflows into active `skills/review/` when the repository already exposes a trustworthy native coverage path such as JaCoCo
- promote a local `manual-workflow` into `skills/docs/` when the manual target is confirmed as workspace-local and external publish steps remain deferred
- absorb support guidance such as markdown conventions into active skills or root docs instead of carrying a generated `references/` tree
- keep ops-locked review prompts/scripts in `templates/` until adapter inputs can bind them safely

Default base-runtime carry-over policy:

- treat reusable root `skills/` entries as generator-owned defaults, not as product adapter data
- bundle `skills/core/` by default when the corresponding base skills have already been neutralized enough for standalone reuse
- bundle `skills/collab/` by default when the workflow is repository-neutral
- carry over `skills/authoring/writing-skills/` from root shared `skills/writing-skills/` when the generated harness needs local skill-authoring guidance
- bundle the base `code-reviewer` workflow by default as the minimum reusable review orchestrator
- when generated review companions such as `review-context-collector` or `coverage-review` also exist, the carried-over `code-reviewer` must acknowledge them as optional bound helpers rather than leaving the review layer disconnected
- when carrying these defaults into a generated harness, preserve standalone runtime names and do not reintroduce legacy `*-base` naming
- do not require `generation_assets` entries for these carry-over defaults
- use `generation_assets` only for template-derived productization decisions
- if a product needs to opt out of a default carry-over rule later, add an explicit policy hook then; do not pre-emptively expand adapter schema
- once `writing-skills` support assets have been promoted into root shared `skills/writing-skills/`, treat the whole directory as a default carry-over source
- do not hand shared `writing-skills/` support assets to `harness-support-assets`
- reserve `harness-support-assets` for template-side adjacent assets that still require product-local productization

Product-local startup meta-skill rule:

- do not promote `using-<product>-harness` into root shared `skills/`
- treat it as a generated runtime-local meta skill when:
  - the source pack carries a strong startup contract through `AGENTS.template.md`
  - adapter truth includes `runtime_entry`
- generation target:
  - `generated/<product>-harness/skills/meta/using-<product>-harness/SKILL.md`
- purpose:
  - restate the startup contract in skill form
  - give the generated runtime a first-class "entry skill" closer to original AIM `using-aim-harness`
  - keep root shared `using-base-harness` reserved for the generator repository itself

For the first validation pass, allow the generated skeleton to stay minimal:

- root metadata such as `AGENTS.md`, `README.md`, and `GENERATION_SUMMARY.md`
- generated drafts for `skills/product/issue-analysis/` and `skills/docs/writing-documents/`
- materialized workspace bindings such as `agent/` and `generated/manual/` when their locations are already confirmed
- `hooks/hooks.json` and `hooks/session-start.sh` that match the current `runtime_entry` contract when runtime entry is already bound

Interpret missing areas carefully:

- do not treat missing `hooks/`, `skills/core/`, `skills/collab/`, or `skills/review/` as first-pass failure
- do treat them as explicit next-pass generation targets
- do not describe the first-pass skeleton as the final intended harness shape

### Phase 5: Review Generated Harness

Goal:
- inspect the generated harness as a generated product artifact rather than as a source-pack draft
- catch structural regressions before treating the pass as complete

Produce:
- generated-harness review notes
- required follow-up fixes
- confirmed deferred scope

Preferred artifact:
- `adapters/<product>/REVIEW_GENERATED_HARNESS.md`

Interpretation:

- this file is a validation artifact only
- it is not a runtime skill
- it is not adapter truth
- it must not become an input source for later generation passes
- generated harness root should keep runtime-facing docs only:
  - `README.md`
  - `AGENTS.md`
  - `GENERATION_SUMMARY.md`

Check explicitly:
- target layout conformity
- active skill vs deferred source-asset classification
- source-pack path leakage
- naming normalization
- hook/runtime consistency
- review-layer coherence when companion review skills are generated
- excluded-scope reporting
- `generation_assets` consistency for template-derived outputs
- maturity gain vs initiator-only baseline when available
- interface cost of any attached refinement schema
- portability of the observed refinement outcomes

Reference handling rule:

- standalone product harnesses should not keep a generated `references/` directory
- active runtime behavior should live under `skills/*` or explicit runtime docs such as `README.md`
- support guidance needed at runtime should be absorbed into skills or root docs
- source-derived comparison material should remain in `templates/`, not inside the generated harness
- AIM-locked carry-over assets stay source-side until they are either productized or intentionally dropped

Naming normalization rule:

- generated carry-over skills must use standalone names in the generated tree
- preserve standalone frontmatter `name:` fields during carry-over
- rewrite any lingering legacy `*-base` cross-skill references to standalone runtime names
- do not leak template or source-pack file paths into active generated runtime skills

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
- preserve source hard gates and behavior-critical safety rules unless the generated harness explicitly replaces them with an equivalent rule
- keep the long-term standalone target visible rather than collapsing the contract to a docs/product-only overlay

For the current `ofgw` validation target, the selected scope is:

- `issue-analysis`
- `writing-documents`
- `markdown-guide` rules absorbed into the generated docs layer

Do not treat first-pass success as:

- a full `ofgw-harness` rollout
- proof that the final generated harness should remain docs/product-only
- proof that mixed-stack `ofgw` facts should rewrite the template body
- permission to silently include excluded assets such as `completing-patch`

## First Build Readiness

At the current design stage:

- `analyze`, `draft-adapter`, and `confirm-gaps` are ready to execute
- `generate-harness` is blocked until the first adapter draft is reviewed and required unresolved values are no longer `unknown`
- `review-generated-harness` runs immediately after generation and is required before calling the pass complete

Treat the next run as a real draft attempt, not as another abstract design pass.

## Common Mistakes

- Trying to convert every product-bound asset in one pass
- Treating codebase guesses as confirmed operational policy
- Letting a mixed-stack validation target overfit the template body to one stack
- Generating the harness before user confirmation
- Hiding excluded assets instead of reporting them
- Letting source-pack cleanup and harness generation become one uncontrolled refactor
- Treating every `references/` asset as either permanent runtime behavior or guaranteed future deletion

## Integration

Pairs with:

- `writing-skills` — if the initiator workflow itself needs revision
- `brainstorming` — when the generation approach or boundary still needs design work
- `writing-plans` — when the initiator implementation itself needs a task breakdown

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
- terminology mapping using `canonical` + `aliases`
- command bindings
- provider-style access and integration bindings
- a `confirm` list for unresolved mappings

Binding source rule:

- `repo.*` and most `command_bindings.*` come from the target codebase
- `access_bindings.*` often start from template-inherited patterns such as URL forms, tool modes, and workflow semantics
- repository docs and user confirmation decide whether those inherited patterns are actually enabled for the target product
- therefore initiator does not require a separate `templates/<pack>/bindings/` directory before it can draft adapters

Inline extraction rule:

- treat template body text as a valid source of binding candidates while the source pack is still in mixed inline form
- prefer extracting stable facts from repeated statements such as:
  - access URL patterns
  - tool-mode restrictions
  - notebook/manual workflow semantics
  - MR or issue marker contracts
- do not promote one-off prose examples into binding fields unless they materially affect runtime routing

Terminology rule:

- use `canonical` for generated default wording
- keep `aliases` for input interpretation and synonym coverage

Workflow default rule:

- if `workflow.defaults.*` are directly implied by confirmed provider bindings, treat them as derived defaults rather than a separate generation gate

Generation preservation rule:

- keep source hard gates and behavior-critical safety rules unless the generated harness explicitly replaces them with an equivalent rule

Do not expand the schema early unless repeated generation attempts show a stable need.
