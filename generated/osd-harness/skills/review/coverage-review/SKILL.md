---
name: coverage-review
description: Use when checking osd test coverage signals with the bound repository coverage workflow before completion or during review follow-up
---

# Coverage Review

Review coverage evidence for `osd` using the bound repository coverage workflow.

This skill is the `osd` productized coverage counterpart. It does not copy the AIM diff-line helper workflow directly. Instead, it uses the confirmed `osd` coverage entry point and reports what the current repository can actually prove.

## When to Use

- When a review needs explicit coverage evidence
- When test changes are substantial and regression protection is uncertain
- When verifying whether follow-up fixes preserved or improved coverage
- Before completion if coverage is a real gate for the change

## Bound Command

- coverage command:
  - `test/run_coverage.sh`

Related commands:

- test command:
  - `make -C test`

Command safety note:

- `test/run_coverage.sh` is the preferred evidence path for this skill
- do not replace it with `dist/patch_osd.sh`, `dist/dist_osd.sh`, or generic packaging output just to obtain a stronger-sounding result
- do not imply full repository coverage from this command alone

## Scope

This skill measures repository-supported coverage artifacts produced by `test/run_coverage.sh`.

Repository-aware boundary:

- current proven coverage scope:
  - code paths and test targets actually exercised by `test/run_coverage.sh`
- outside the first review boundary:
  - packaging and distribution scripts under `dist/`
  - runtime setup assumptions outside the scripted test/coverage flow

Reason:

- the confirmed bound coverage command is an environment-dependent shell workflow, not a universal repository-wide proof
- the script stages runtime libraries and selectively builds/runs coverage-aware test binaries

It can reliably report:

- whether the coverage script completed
- whether `gcov`, `lcov`, and `genhtml` outputs were produced
- whether changed areas appear weakly protected based on the generated coverage outputs and nearby tests

It must not claim:

- exact diff-line coverage unless the repository provides a trustworthy diff-aware report
- a policy threshold that is not explicitly confirmed for `osd`
- that every changed path in the repo was included in the script's exercised scope

## Workflow

### Step 1: Decide Whether Coverage Review Is Needed

Use it when:

- production logic changed
- tests changed materially
- the reviewer or user asked for coverage evidence
- completion depends on stronger regression confidence

Skip or reduce scope when:

- docs-only changes
- comment-only changes
- metadata-only changes

### Step 2: Run Coverage Generation

Run the bound coverage command for `osd`.

If the coverage script cannot run because required environment values or runtime libraries are missing, report that blocker explicitly before making any coverage claim.

### Step 3: Inspect Coverage Outputs

Look for generated outputs under the script's report locations, typically under:

- `/tmp/osd_coverage_report/`
- `$REPORT_DIR` when overridden
- generated `lcov` or `html` report paths reported by the script

Prefer repository-generated outputs over hand-written interpretation.

Collect:

- report generation success/failure
- top-level coverage percentages when available
- packages or classes with obviously weak coverage
- whether changed areas appear covered by matching tests or reported files

### Step 4: Compare Against Change Scope

Use local git diff and changed files to answer:

- which production files changed
- which tests changed
- whether the test additions map to the changed behavior
- whether the coverage signal is broad, narrow, or missing
- whether the changed files were actually inside the script's exercised coverage scope or outside it

Do not overstate precision. If coverage is only module-level, say so explicitly.

If the change is mainly in packaging scripts, release flow, or repo areas not exercised by the coverage script, say that the current coverage workflow does not prove coverage for that area.

### Step 5: Write Coverage Review

Write the result to:

- `agent/<topic>/coverage_review.md`

Suggested shape:

```markdown
# Coverage Review

## Command
- coverage:

## Report Status
- generated:
- report paths:

## Coverage Signals
- summary:
- weak areas:

## Change-Scope Comparison
- changed production files:
- changed test files:
- mapping assessment:

## Conclusion
- confidence level:
- gaps or follow-up:
```

## Rules

- Separate report facts from reviewer inference.
- Do not pretend script-generated coverage is full repository or diff-line coverage.
- Do not invent a required percentage threshold unless the product policy is confirmed.
- If coverage generation fails, report the failure and the likely blocker.
- If the change is outside the script's exercised scope, report the coverage boundary explicitly instead of forcing a misleading conclusion.

## Integration

**Called by:**
- **code-reviewer** — when coverage evidence is needed as part of review
- **verification-before-completion** — when completion requires stronger regression confidence

**Feeds into:**
- review summaries
- completion verification notes
