# Skill Authoring Best Practices

Use this reference when writing or revising shared skills and you need practical guardrails for structure, scope, and testability.

This is intentionally a shared guide. It avoids vendor-specific runtime assumptions unless they materially change the advice.

## Core Principles

### 1. Write for the trigger, not for the topic

Good skills are discovered because the trigger is clear.

Focus on:
- when the skill should load
- what failure or pressure makes it necessary
- what the user or agent is likely to do wrong without it

Avoid:
- long conceptual introductions
- broad topic summaries
- repeating obvious background the model already knows

### 2. Keep the main body small

`SKILL.md` should teach the workflow and point to supporting files.

Keep in `SKILL.md`:
- trigger and scope
- core workflow
- decision rules
- short examples

Move out of `SKILL.md`:
- long references
- reusable prompts
- scripts
- worked examples

### 3. Match specificity to fragility

Use high freedom when many approaches are acceptable.

Use low freedom when:
- the workflow is brittle
- validation is easy to skip
- command order matters
- failure is expensive

If the task is risky, exact steps are better than philosophy.

### 4. Prefer progressive disclosure

The main file should help the agent discover what exists, then load only what is needed.

Good pattern:
- `SKILL.md`
- `best-practices.md`
- `examples/...`
- `scripts/...`

Bad pattern:
- every rule and example copied into one giant `SKILL.md`

### 5. Test skills with observed failure first

Do not treat skill writing as pure editorial work.

Before changing a skill:
- run or imagine a realistic scenario without the skill
- capture what would likely fail
- write the smallest change that prevents that failure

If there is no concrete failure mode, the skill usually needs less text, not more.

### 6. Make support assets do real work

A support asset should have a job.

Good support assets:
- pressure-test examples
- prompt templates
- format guides
- rendering scripts
- reference tables

Bad support assets:
- duplicate prose
- decorative examples
- notes with no clear execution value

### 7. Keep references shallow

When a skill needs extra files, prefer one-hop references from `SKILL.md`.

Good:
- `SKILL.md` -> `best-practices.md`
- `SKILL.md` -> `examples/AGENTS_MD_TESTING.md`

Avoid long chains where one reference points to another and the important guidance becomes hard to find.

### 8. Prefer runtime-neutral wording in shared assets

Shared assets should not unnecessarily depend on:
- one vendor name
- one repo layout
- one hook filename
- one proprietary tool

If a reference came from a vendor-specific source, rewrite it around the durable concept:
- discovery
- progressive disclosure
- validation
- workflow structure
- support-script usage

## Metadata Rules

### `name`

- use descriptive hyphenated names
- make the name match the actual behavior

Good:
- `writing-skills`
- `systematic-debugging`
- `verification-before-completion`

### `description`

Descriptions should:
- start with `Use when...`
- describe triggers or symptoms
- help discovery

Good:

```yaml
description: Use when creating a new skill, revising an existing skill, or validating whether a skill teaches the intended workflow clearly and reliably
```

Bad:

```yaml
description: A skill about writing skills and references
```

## Layout Rules

Preferred layout:

```text
skills/
  skill-name/
    SKILL.md
    best-practices.md
    examples/
    scripts/
```

Only add extra files when they reduce confusion or token cost.

## Example Rules

Worked examples should reflect the current runtime contract.

If the runtime uses:
- `AGENTS.md`
- `skills/`
- `agent/<topic>/`

then examples should use those names.

Do not leave stale example paths like:
- `~/.claude/skills/...`
- `CLAUDE.md`

unless the skill is explicitly about migrating from them.

## Script Rules

Scripts are worth bundling when they:
- automate deterministic work
- reduce repeated manual effort
- prevent formatting drift
- support visualization or validation

Scripts should:
- fail clearly
- print actionable error messages
- keep assumptions explicit

## Quality Checklist

Before treating a writing-related asset as shared-ready, check:

- the trigger is clear
- the body is concise
- references are one hop away
- examples use the current runtime contract
- vendor language is removed unless essential
- scripts have a clear operational purpose
- the asset still helps after removing product-specific wording

## Promotion Rule

Promote a support asset into shared `skills/writing-skills/` when:
- it works across multiple products with little or no porting
- its value comes from authoring method rather than product operations
- keeping it product-local would just duplicate the same file repeatedly

Keep an asset product-local when:
- it depends on repo-specific workflow
- it depends on one review/manual/release system
- it still needs heavy runtime-specific rewriting
