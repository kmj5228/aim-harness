---
name: using-base-harness
description: Use when starting any conversation in this repository to establish how to discover and apply base-harness skills before responding or acting
---

<SUBAGENT-STOP>
If you were dispatched as a subagent for a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a small chance a skill applies, invoke the skill before acting.

If a relevant skill exists, use it.
</EXTREMELY-IMPORTANT>

## Instruction Priority

1. **User instructions** — highest priority
2. **Repository rules** (`AGENTS.md`, `CLAUDE.md`) — next
3. **base-harness skills** — workflow guidance
4. **Default system behavior** — lowest priority

## How To Access Skills

Use the `Skill` tool. Do not read skill files directly when the skill system is available.

## The Rule

Invoke relevant or requested skills before responding or acting.

Typical flow:

1. Read the user request
2. Ask: "Does any skill likely apply?"
3. If yes, invoke the skill
4. Follow the skill
5. Respond or act

## Skill Routing Table

| Trigger | Skill |
|---------|-------|
| New feature, fix, refactor — design first | **brainstorming-base** |
| Approved design, need task breakdown | **writing-plans-base** |
| Plan exists, executing inline | **executing-plans-base** |
| Plan exists, executing with fresh subagents | **subagent-driven-development-base** |
| Multiple independent tasks can run in parallel | **dispatching-parallel-agents-base** |
| Implementing behavior with tests first | **test-driven-development-base** |
| Test failure, bug, or unexpected behavior | **systematic-debugging-base** |
| About to claim work complete | **verification-before-completion-base** |
| Need isolated branch/workspace before implementation | **using-feature-branches-base** |
| Implementation finished, need branch/review handoff | **finishing-a-development-branch-base** |
| Need structured self-review | **requesting-code-review-base** |
| Need to process review feedback | **receiving-code-review-base** |
| Need a structured review workflow | **code-reviewer-base** |
| Creating or editing skills | **writing-skills-base** |

## Workflow Chain

```text
brainstorming-base
  -> writing-plans-base
  -> executing-plans-base / subagent-driven-development-base
     -> test-driven-development-base
     -> systematic-debugging-base (when needed)
     -> verification-before-completion-base
  -> finishing-a-development-branch-base
     -> requesting-code-review-base
     -> receiving-code-review-base

Independent / specialized:
  dispatching-parallel-agents-base
  code-reviewer-base
  using-feature-branches-base
  writing-skills-base

Product-specific product packs:
  product-specific/skills/issue-analysis-base
  product-specific/skills/completing-patch-base
  product-specific/skills/writing-documents-base
```

## Skill Gap Reporting

When a skill is outdated, incomplete, misleading, or inconsistent with the actual repository state, report it.

Format:

```text
[Skill Gap] <skill-name>
Finding: <what is wrong>
Evidence: <file, command, or observed behavior>
Proposal: <specific improvement>
```

Report the gap. Do not silently rewrite the skill without approval.

## Product-Specific Product Packs

Some product-bound workflows are no longer part of the default `skills/` routing set.

- location: `product-specific/skills/`
- purpose: preserve product-specific product packs without mixing them into the base runtime skill set
- current packs: issue analysis, patch completion, documentation workflow

## Skill Priority

When multiple skills might apply:

1. **Process skills first** — e.g. `brainstorming-base`, `systematic-debugging-base`
2. **Execution skills second** — e.g. `test-driven-development-base`, `executing-plans-base`

## Common Red Flags

- "This is simple, I can skip skills"
- "I need more context first"
- "I'll just inspect files quickly"
- "I remember the skill already"
- "This one action doesn't need a workflow"

These are usually signals to check the relevant skill first.
