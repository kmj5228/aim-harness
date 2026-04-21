---
name: coverage-review
description: Use when checking AIM diff coverage signals with the bound gcov workflow before completion or during review follow-up
---

# Coverage Review

Review coverage evidence for `aim` using the bound diff-coverage workflow.

This generated skill is the explicit AIM coverage helper extracted from the original review system. Unlike the `aim` JaCoCo path, AIM already has a concrete diff-based coverage rule and helper script.

## When to Use

- when a review needs explicit coverage evidence
- when new production logic changed
- when self-review or external review asks for coverage proof
- before completion when the AIM policy gate matters

## Bound Commands

- test:
  - `dx tmdown -y && dx make gtest`
- coverage:
  - `dx bash -c "cd /root/ofsrc/aim && bash skills/review/code-reviewer/scripts/measure_diff_cov.sh"`

## Policy

- required threshold:
  - added-code line coverage `>= 80%`
- measurement basis:
  - diff-added production code under the current branch versus base branch

## Workflow

1. Run full gtest once to generate coverage data.
2. Run the bound `measure_diff_cov.sh` helper.
3. Compare the coverage result against the current diff scope.
4. Record:
   - total percentage
   - weak or uncovered areas
   - whether the result meets the 80% policy
5. Write `agent/<topic>/coverage_review.md`

## Output Contract

Write:

- `agent/<topic>/coverage_review.md`

Suggested sections:

- `Command`
- `Policy`
- `Measured Result`
- `Changed Files In Scope`
- `Weak Or Uncovered Areas`
- `Conclusion`

## Rules

- Separate measured output from reviewer inference.
- Do not claim coverage success without running the helper script.
- Do not replace diff coverage with hand-wavy test count claims.
- If the script fails, report the blocker explicitly.

## Integration

**Called by:**
- **code-reviewer**
- **verification-before-completion**

**Feeds into:**
- review summaries
- completion verification notes
