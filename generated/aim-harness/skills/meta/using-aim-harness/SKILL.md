---
name: using-aim-harness
description: Use at session start inside the generated aim-harness runtime to enforce skill-first routing, startup contract reloading, and explicit skill-gap reporting before ad hoc work
---

<SUBAGENT-STOP>
If you were dispatched as a subagent for a narrowly scoped task, skip this startup meta skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a small chance a generated AIM harness skill applies, read that skill before acting.

If the harness lacks a needed skill, report the gap instead of silently bypassing the runtime contract.
</EXTREMELY-IMPORTANT>

## Instruction Priority

1. User instructions
2. This generated runtime contract and the generated `AGENTS.md`
3. Generated AIM harness skills
4. Default model behavior

## Startup Rule

On `startup`, `resume`, `clear`, and `compact`:

1. Re-read `AGENTS.md`
2. Check whether the task routes to an existing generated skill
3. If yes, use that skill before improvising workflow
4. If no, report `[Skill Gap] <skill>: <problem>`

Do not treat "I can probably do this directly" as a reason to skip the harness.

## Skill Routing Summary

Use these generated skills first when relevant:

- `issue-analysis`
- `brainstorming`
- `writing-plans`
- `executing-plans`
- `subagent-driven-development`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `finishing-a-development-branch`
- `requesting-code-review`
- `receiving-code-review`
- `code-reviewer`
- `review-context-collector`
- `coverage-review`
- `writing-documents`
- `manual-workflow`
- `writing-skills`

## Workflow Reminder

Default chain:

`issue-analysis` optional entry
-> `brainstorming`
-> `writing-plans`
-> `executing-plans` or `subagent-driven-development`
-> `test-driven-development`
-> `systematic-debugging` on failure
-> `verification-before-completion`
-> `finishing-a-development-branch`
-> `requesting-code-review` and `receiving-code-review`

Deferred tail:

- `completing-patch`
- external manual publish

Keep those visible as deferred runtime gaps, not as silently completed workflow.

## Skill Gap Reporting

Format:

```text
[Skill Gap] <skill>: <problem>
```

Examples:

- `[Skill Gap] coverage-review: changed area is outside the current proven coverage boundary`
- `[Skill Gap] manual-workflow: current generated runtime stops at local draft and does not cover upstream publish`

## Runtime Boundaries

- This meta skill belongs to the generated AIM runtime only.
- It is not a shared root skill.
- Product-specific startup/access/review wording should stay here or in `AGENTS.md`, not in root `skills/using-base-harness/`.
