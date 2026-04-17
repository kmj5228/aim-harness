---
name: code-reviewer-base
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
- unresolved risks
- follow-up recommendation

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

**Called by:**
- **requesting-code-review-base** — structured self-review
- Direct review requests — someone else's patch

**Feeds into:**
- **receiving-code-review-base** — when findings need to be processed and fixed
- **verification-before-completion-base** — after review-driven fixes
