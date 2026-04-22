---
name: harness-support-assets
description: Use when a selected template pack contains support assets next to source skills and those assets need to be carried into a generated product harness as runtime-adjacent bundled files without collapsing them into shared root skills
---

# Harness Support Assets

## Overview

Carry template-side support assets into a generated product harness without bloating `harness-initiator`.

**Core principle:** support assets from source packs are productized first, not generalized first.
This skill is not only a copier. It is responsible for bundling support assets and porting obvious source-runtime assumptions to the target product runtime.

Default behavior is simple:

- if a template skill has adjacent support assets
- and the generated product harness carries that skill
- bundle the support assets next to the generated `SKILL.md`
- unless the adapter already gives that source asset an explicit `generation_assets` treatment such as:
  - `absorb`
  - `absorb_partial`
  - `defer`
  - `stay_in_templates`

Only introduce exceptions after a real generation pass shows a concrete problem.
Do not pre-classify ordinary support guides or prompts as exclusions just because they originated in AIM.

## When to Use

- a source pack such as `templates/aim/` contains prompts, guides, scripts, or helper docs next to `SKILL.md`
- `harness-initiator` has already identified which source skills should appear in the generated runtime
- the remaining task is to materialize support assets in the generated runtime with minimal transformation
- the remaining task is to materialize support assets in the generated runtime with target-product-safe wording, paths, and commands

Do not use for:

- selecting template scope
- drafting adapters
- deciding first-pass runtime layout
- polishing generated skill wording after generation
- promoting a product-specific support asset into root shared `skills/`

Use `harness-initiator` when the question is still "what should be generated?"
Use `harness-refinement` when the generated harness already exists and the question is "how should this generated runtime be improved?"

If repeated low-diff validations show that a support asset no longer needs meaningful productization, treat that as a promotion signal for root shared `skills/`, not as a reason to bloat this skill's porting rules.

## Inputs

- selected source pack under `templates/<pack>/`
- generated target directory such as `generated/<product>-harness/`
- generated skill layout from `harness-initiator`
- adapter context only when it is needed to choose path names or obvious exclusions

## Default Rule

Support assets are bundled by default.

- source location:
  - next to `templates/<pack>/skills/<skill>/SKILL.md`
  - or next to `templates/<pack>/review/<skill>/SKILL.md`
- generated location:
  - next to the generated `SKILL.md`

Examples:

- `templates/aim/skills/brainstorming/spec-document-reviewer-prompt.md`
  -> `generated/<product>-harness/skills/core/brainstorming/spec-document-reviewer-prompt.md`
- `templates/aim/review/code-reviewer/measure_diff_cov.sh`
  -> `generated/<product>-harness/skills/review/code-reviewer/measure_diff_cov.sh`

## Workflow

1. Identify which generated skills came from source-pack skills.
2. Read `generation_assets` first and treat explicit source-asset actions as overrides.
   - generation rules for source `SKILL.md` remain authoritative
   - support assets not explicitly mentioned should still be bundled and ported by default
3. For each selected source skill, inspect adjacent support assets that are not already claimed by an explicit `generation_assets` rule.
4. Bundle those remaining assets next to the generated `SKILL.md` by default.
   - always exclude source `SKILL.md` itself from asset copying
5. Port obvious source-runtime assumptions to target-runtime assumptions when repo or adapter evidence is already available.
   - rewrite artifact paths such as `../agent/prompt/<topic>/...` to `agent/<topic>/...`
   - rewrite source-product wording such as `AIM C project` to target-product wording
   - rewrite command examples to target commands when `command_bindings` already confirm them
   - rewrite module and boundary hints when repo facts already confirm them
   - rewrite review vocabulary such as `MR` to the target product review artifact when terminology or bindings already confirm it
   - if a support guide is tied to a disabled target binding, decide whether it should still travel as a dormant reference
   - keep the source asset recognizable, but remove target-incompatible operational assumptions
6. Keep filenames and relative grouping stable unless the generated runtime contract clearly requires renaming.
   - example: a source example centered on `CLAUDE.md` may become `AGENTS_MD_TESTING.md` in a Codex-generated harness
7. Do not rewrite the asset body just to make it look generic.
   - port concrete assumptions
   - do not erase useful support behavior
8. If a support asset is deeply vendor-locked or editorially large, do the smallest honest port first and record the limit.
   - acceptable first-pass outcome:
     - bundled in generated runtime
     - obvious runtime assumptions removed or annotated
     - explicit note that deeper rewrite belongs to `harness-refinement` or later shared-skill promotion
9. If a concrete problem appears during validation, report it back as:
   - keep bundled
   - move to refinement
   - mark as true exclusion candidate

Current validation interpretation:

- first prove that default bundling works on a real product harness
- only after that introduce exception handling for specific assets
- the first validation target for this skill is `generated/ofgw-harness/`

## Validated Common Patterns

The current `ofgw` and `osd` validation passes show that some support-asset transformations recur without new schema.

Validated common patterns:

- adjacent reviewer prompt markdown can be bundled next to generated skills and ported with existing adapter facts
- planning/review prompt artifacts can be rewritten from source-relative prompt paths to `agent/<topic>/...`
- source-product wording can be rewritten to target-product wording without erasing the support role of the asset
- review vocabulary can be normalized to the target review artifact when terminology already confirms it
- module and boundary hints can be ported from source assumptions to confirmed target repo surfaces
- command examples can be rewritten to confirmed target commands when `command_bindings` already provide them
- authoring support assets can be introduced through a shared root `writing-skills/SKILL.md` baseline plus source-pack support-asset porting under `skills/authoring/`

Validated examples from `ofgw` and `osd`:

- `brainstorming/spec-document-reviewer-prompt.md`
- `writing-plans/plan-document-reviewer-prompt.md`
- `subagent-driven-development/*.md`
- `review/code-reviewer/{code-reviewer-prompt,review-synthesizer-prompt,test-reviewer-prompt}.md`
- `writing-documents/{markdown-guide,jira-guide,gitlab-guide}.md`

Observed product-bound variation:

- a disabled target binding does not automatically force guide exclusion
- a guide may still be bundled as a dormant reference when support-asset completeness is the current validation priority
- example: `confluence-guide.md` can stay bundled in `ofgw` even while `docs_targets.confluence.enabled` remains false

Current non-goal:

- adding a new support-asset schema before these common patterns stop being expressible with existing adapter truth

## Boundaries

This skill may:

- copy support assets into generated runtime-adjacent locations
- keep source-relative grouping
- normalize obviously broken paths when needed for runtime consistency
- respect adapter `generation_assets` overrides instead of bundling every adjacent file blindly
- rewrite support assets using already confirmed adapter and repo facts

This skill should not:

- overwrite generated `SKILL.md` with source-pack `SKILL.md`
- re-bundle assets that the adapter already marked as `absorb`, `absorb_partial`, `defer`, or `stay_in_templates`
- redefine root shared skills
- invent support assets that are not in the source pack
- decide broad product workflow semantics
- pre-emptively exclude assets before a real generation pass shows a concrete problem
- leave obvious source-product wording untouched when the target-product replacement is already known

## Outputs

- bundled support assets under `generated/<product>-harness/skills/...`
- ported support assets whose wording now matches target runtime facts
- short note of any asset that caused a real validation problem
- explicit handoff back to:
  - `harness-initiator` if the issue is structural
  - `harness-refinement` if the issue is generated-runtime wording or ergonomics
