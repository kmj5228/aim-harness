---
name: writing-skills
description: Use when creating a new skill, revising an existing skill, or validating whether a skill teaches the intended workflow clearly and reliably
---

# Writing Skills

Writing skills is test-driven development applied to process documentation.

The point is not to write a clever document. The point is to produce a skill that reliably changes agent behavior in the intended situation.

**Core principle:** If you did not observe failure without the skill, you do not yet know what the skill needs to teach.

**Required background:** `test-driven-development` explains the RED-GREEN-REFACTOR loop this skill adapts for documentation.

**Reference:** `anthropic-best-practices.md` contains additional vendor guidance for skill authoring. Use it as supporting material, not as a substitute for testing.

## What a Skill Is

A skill is a reusable guide for a proven technique, workflow, or reference pattern that future agents should be able to discover and apply.

Skills are:
- reusable techniques
- repeatable workflows
- focused references
- prompts or helpers that support those workflows

Skills are not:
- one-off narratives
- raw project history
- repository policy dumps better suited for `AGENTS.md` or `CLAUDE.md`
- rules that could be enforced more safely with automation

## When to Create One

Create a skill when:
- the technique is not obvious without explicit guidance
- the same workflow will recur
- the guidance should be discoverable across tasks or repositories
- failure is likely if the workflow is left implicit

Do not create a skill for:
- one-time cleanup steps
- repository-only rules that belong in always-loaded docs
- generic knowledge already covered well elsewhere
- purely mechanical validation that automation can enforce

## Skill Types

### Technique

A concrete method with steps to follow.

Examples:
- debugging workflow
- review orchestration
- verification gate

### Pattern

A decision model or operating style.

Examples:
- subagent usage pattern
- plan execution pattern

### Reference

Focused lookup material needed during execution.

Examples:
- API notes
- format rules
- prompt templates

## Structure

Preferred layout:

```text
skills/
  skill-name/
    SKILL.md
    supporting-file.*
```

Follow the repository's local naming convention if one already exists. In transitional repositories, the directory name may still carry legacy suffixes even when the body has been generalized.

Keep in `SKILL.md`:
- principles
- workflow
- short examples
- decision rules

Split into support files only for:
- long reference material
- reusable scripts or templates
- subagent prompt templates

## SKILL.md Rules

Frontmatter:
- required: `name`, `description`
- `name`: letters, numbers, hyphens
- `description`: third-person trigger description only
- start with `Use when...`
- describe when the skill should be loaded, not how the workflow works

Recommended sections:

```markdown
---
name: skill-name
description: Use when [specific triggers or symptoms]
---

# Skill Name

## Overview

## When to Use

## Workflow / Checklist

## Common Mistakes

## Integration
```

Add more sections only when they materially improve usability.

## Discovery Rules

Skills must be easy for future agents to find.

### Description Quality

Good descriptions:
- mention triggering situations
- mention symptoms or failure modes
- avoid workflow summaries

Bad descriptions:
- summarize the whole process
- duplicate the body
- mention broad labels with no trigger information

```yaml
# Bad
description: Use when doing code review in multiple phases

# Good
description: Use when reviewing a large change set that needs separate context gathering, analysis, and synthesis
```

### Keyword Coverage

Include words an agent would search for:
- symptoms
- failure modes
- workflow names
- relevant tool or artifact names when they matter

Use repository-neutral product-specific unless the skill is intentionally product-specific.

### Naming

Prefer descriptive active names:
- `systematic-debugging`
- `verification-before-completion`
- `dispatching-parallel-agents`

In a transitional repository, keep legacy filenames until the rename plan is ready, but write new guidance as if the skill were generic.

## Token Discipline

Frequently loaded skills must stay small.

Guidelines:
- keep the body concise
- avoid repeating repository policy already loaded elsewhere
- cross-reference related skills instead of duplicating them
- prefer one strong example over many weak ones

```markdown
# Bad
Repeat the full TDD loop in every skill.

# Good
Testing follows `test-driven-development`. Reference that skill for the full loop.
```

## The Iron Law

```text
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to both:
- creating a new skill
- editing an existing skill

If you changed the skill before establishing the baseline failure, your evidence is weak. Recreate the baseline.

## TDD for Skills

### RED

Run a scenario without the skill.

Capture:
- what the agent did
- what it missed
- which rationalizations it used
- which pressures caused failure

### GREEN

Write the smallest skill that addresses those failures.

Re-run the same scenario with the skill present.

### REFACTOR

Look for new loopholes.

If the agent finds a workaround:
- update the skill
- test again
- keep tightening until the workflow is robust

`testing-skills-with-subagents.md` contains the detailed testing method.

## Testing by Skill Type

### Discipline Skills

Use pressure scenarios:
- time pressure
- sunk-cost pressure
- ambiguity
- fatigue or impatience

Goal: the agent still follows the rule.

### Technique Skills

Use application scenarios:
- normal case
- edge case
- incomplete information case

Goal: the agent can apply the method correctly.

### Reference Skills

Use retrieval and application scenarios:
- can the agent find the right part
- can it apply the reference correctly

Goal: the reference is discoverable and usable.

## Rationalization Control

Skills that enforce discipline need explicit anti-loophole language.

### Capture Rationalizations

Build a table from real failures:

```markdown
| Excuse | Reality |
|--------|---------|
| "This is too small to need the workflow" | Small changes still fail when assumptions go untested. |
| "I'll verify after I finish" | Late verification misses whether the workflow changed behavior. |
```

### Add Red Flags

Make recovery conditions obvious:

```markdown
## Red Flags

- skipped the baseline test
- assumed the workflow was obvious
- summarized the process only in the description
```

## Quality Checklist

### RED

- [ ] Wrote or selected realistic failure scenarios
- [ ] Observed baseline behavior without the skill
- [ ] Captured concrete failures or rationalizations

### GREEN

- [ ] Added frontmatter with `name` and `description`
- [ ] Description starts with `Use when...`
- [ ] Description explains trigger conditions only
- [ ] Skill addresses real failures from baseline testing
- [ ] Added search-friendly terms where relevant
- [ ] Cross-referenced related skills instead of duplicating them
- [ ] Verified the agent behaves better with the skill

### REFACTOR

- [ ] Closed newly observed loopholes
- [ ] Added rationalization counters if needed
- [ ] Removed unnecessary words and duplication
- [ ] Re-tested after refinement

## Common Mistakes

### Narrative History Instead of Guidance

Bad:
- session diary
- project anecdote
- one-off debug story

Fix:
- extract the reusable pattern

### Workflow Summary in Description

Bad:
- description tells the agent the whole process in one sentence

Fix:
- put the process in the body
- keep the description focused on triggers

### Too Many Weak Examples

Bad:
- multiple shallow language examples
- filler templates

Fix:
- one focused example or none

### Untested Edits

Bad:
- changing a skill because it "seems clearer"

Fix:
- recreate the failing scenario and validate the revision

## Deployment Discipline

After editing a skill:
- verify it works
- document what changed
- do not batch multiple untested skill edits together unless each one was validated independently

## Bottom Line

Skill authoring is workflow design plus behavioral verification.

The standard loop stays the same:
- RED: observe failure
- GREEN: write the smallest useful guidance
- REFACTOR: close loopholes and retest
