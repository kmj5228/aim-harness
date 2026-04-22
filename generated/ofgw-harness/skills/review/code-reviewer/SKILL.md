---
name: code-reviewer
description: Use when running a structured multi-step review of someone else's change set or a self-review workflow that needs coordinated information gathering, analysis, synthesis, and follow-up
---

# Code Reviewer

Run a structured review workflow that gathers context, analyzes code and tests, synthesizes findings, and supports follow-up verification.

**Core principle:** Separate context gathering, technical analysis, and synthesis so the review stays evidence-driven.

## When to Use

- Reviewing someone else's change set
- Running a structured self-review before handoff
- Reviewing a large patch that benefits from multiple specialist passes
- Re-checking whether review findings were properly addressed

## Review Structure

Recommended review roles:

| Role | Responsibility |
|------|----------------|
| Context collector | Gather change scope, files, commits, and relevant metadata |
| Code reviewer | Review logic, correctness, maintainability, and risk |
| Test reviewer | Review tests, regression protection, and missing coverage areas |
| Synthesizer | Merge findings into a single coherent report |

If some roles are unnecessary for the repository or change size, reduce the set. Keep the separation of responsibilities.

## Inputs

Collect what is needed to review the patch:

- Topic or review identifier
- Change scope
- Branch or review artifact identifier if applicable
- Files changed
- Relevant requirements, design notes, or linked work items
- Optional mode flags, such as self-review vs external review

## Bound Review Extensions

If the current harness provides companion review skills, treat them as bound helpers rather than disconnected extras.

- `review-context-collector`
  - run this first when issue, PR, or diff context is not already normalized
  - prefer reusing `agent/<topic>/review_context.md` when a fresh context artifact already exists
- `coverage-review`
  - run this when the review mode is full or test-focused, or when the risk profile needs explicit coverage evidence
  - prefer reusing `agent/<topic>/coverage_review.md` when the evidence is still fresh enough for the current patch
  - if an extra diff-focused hint is useful, the helper at `skills/review/code-reviewer/scripts/measure_diff_cov.sh` may be used after the main JaCoCo report exists
  - treat that helper as supplemental evidence, not as the primary coverage contract

If the harness does not provide these helpers, continue with the base workflow directly.

## The Workflow

### Step 1: Preparation

1. Normalize the input
2. Create a review workspace or output location
3. Decide review mode
   - full review
   - code-focused review
   - test-focused review
   - update/verification review

### Step 2: Context Gathering

Prefer the dedicated context helper when available.

- if `review-context-collector` exists in the current harness and no fresh context artifact already exists, run it first
- otherwise collect the same context directly here

Collect:
- changed files
- commit history in scope
- diff summary
- linked requirements or design context
- known risk areas

This stage should describe what changed before judging whether it is good.

### Step 3: Review Plan

Create a short review plan covering:
- what will be reviewed
- which reviewer roles will run
- what outputs are expected
- any areas needing special attention

If the plan reveals missing context, stop and ask before reviewing.

### Step 4: Execute Review

Run the selected review roles.

Recommended pattern:
- Context collector runs first
- Code and test review can run in parallel once context is ready
- `coverage-review` may run as the test-review companion when explicit coverage evidence is needed and the current harness provides it
- Synthesizer runs after reviewer outputs exist

Each reviewer should produce findings with:
- severity or priority
- location
- problem statement
- evidence
- suggested direction

### Step 5: Synthesize Findings

Produce one review summary that includes:
- overall assessment
- grouped findings
- testing concerns
- context gaps or coverage-boundary notes when they materially affect confidence
- unresolved risks
- follow-up recommendation

When present, use the generated `review_context.md` and `coverage_review.md` artifacts as supporting inputs rather than silently recomputing them.

Do not let synthesis hide or water down concrete findings from earlier review steps.

### Step 6: Deliver or Record Review

Depending on the repository workflow:
- present review findings to the user
- write them into review documents
- post them into the repository's review channel
- hold them for self-review use

The delivery mechanism is repository-specific. The finding structure is not.

### Step 7: Follow-Up Verification

If the patch is updated after review:
- compare the new patch against prior findings
- check which items are fixed, partially fixed, or still open
- note any new issues introduced by the follow-up patch

## Review Modes

### Full Review

Use when the patch is large or risky.

Include:
- context gathering
- code review
- test review
- synthesis

### Code-Focused Review

Use when test structure is trivial or unchanged.

### Test-Focused Review

Use when the main risk is weak regression protection or missing tests.

### Verification Review

Use after the author claims to have addressed prior findings.

## Finding Quality Rules

Good findings:
- identify a real risk or defect
- point to evidence
- explain impact
- separate fact from suggestion

Bad findings:
- style-only nitpicks presented as critical
- vague discomfort without evidence
- architecture criticism with no relevance to the patch
- duplicated findings under different wording

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reviewing before understanding scope | Gather context first |
| Mixing evidence and opinion | Separate observation, impact, suggestion |
| Letting synthesis erase detail | Preserve concrete findings |
| Reviewing huge patches with one undifferentiated pass | Split roles or modes |
| Treating follow-up as full re-review without focus | Verify against prior findings first |

## Integration

**Works with:**
- **review-context-collector** — when the current harness provides a dedicated context pass
- **coverage-review** — when the current harness provides explicit coverage evidence workflow

**Called by:**
- **requesting-code-review** — structured self-review
- Direct review requests — someone else's patch

**Feeds into:**
- **receiving-code-review** — when findings need to be processed and fixed
- **verification-before-completion** — after review-driven fixes
