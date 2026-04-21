---
name: coverage-review
description: Use when checking ofgw test coverage signals with the bound JaCoCo workflow before completion or during review follow-up
---

# Coverage Review

Review coverage evidence for `ofgw` using the bound JaCoCo workflow.

This skill is the `ofgw` productized coverage counterpart. It does not copy the AIM `gcov` and diff-line script workflow. Instead, it uses the confirmed `ofgw` coverage command and reports what the current repository can actually prove.

## When to Use

- When a review needs explicit coverage evidence
- When test changes are substantial and regression protection is uncertain
- When verifying whether follow-up fixes preserved or improved coverage
- Before completion if coverage is a real gate for the change

## Bound Command

- coverage command:
  - `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:jacocoTestReport --no-daemon`

Related commands:

- test command:
  - `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:test --no-daemon`

Command safety note:

- `:ofgwSrc:jacocoTestReport` is the preferred evidence path for this skill
- do not replace it with `:ofgwSrc:jar` or root packaging tasks just to obtain a stronger-sounding result
- do not imply `webterminal` or `ofgwAdmin` verification from this command alone

## Scope

This skill measures repository-supported coverage artifacts for `ofgwSrc`.

Repository-aware boundary:

- current proven coverage scope:
  - `ofgwSrc`
- outside the first review boundary:
  - `webterminal`
  - `ofgwAdmin`

Reason:

- the confirmed bound coverage command only proves JaCoCo coverage for `:ofgwSrc`
- `webterminal` packaging and `ofgwAdmin` frontend build follow separate paths and are not covered by this skill yet

It can reliably report:

- whether the JaCoCo report was generated
- module-level coverage signals
- whether changed areas appear weakly protected based on nearby tests and coverage outputs

It must not claim:

- exact diff-line coverage unless the repository provides a trustworthy diff-aware report
- a policy threshold that is not explicitly confirmed for `ofgw`

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

Run the bound coverage command for `ofgwSrc`.

If coverage artifacts do not exist yet and only test execution is needed first, run the test command before retrying coverage generation.

### Step 3: Inspect Coverage Outputs

Look for generated outputs under the module build directory, typically under:

- `ofgwSrc/build/reports/jacoco/`
- `ofgwSrc/build/reports/tests/`

Prefer repository-generated outputs over hand-written interpretation.

Collect:

- report generation success/failure
- top-level coverage percentages when available
- packages or classes with obviously weak coverage
- whether changed modules appear covered by matching tests

### Step 4: Compare Against Change Scope

Use local git diff and changed files to answer:

- which production files changed
- which tests changed
- whether the test additions map to the changed behavior
- whether the coverage signal is broad, narrow, or missing
- whether the changed files were actually inside `ofgwSrc` or outside the current coverage boundary

Do not overstate precision. If coverage is only module-level, say so explicitly.

If the change is mainly in `webterminal` or `ofgwAdmin`, say that the current coverage workflow does not prove coverage for that area.

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
- Do not pretend JaCoCo module coverage is diff-line coverage.
- Do not invent a required percentage threshold unless the product policy is confirmed.
- If coverage generation fails, report the failure and the likely blocker.
- If the change is outside `ofgwSrc`, report the coverage boundary explicitly instead of forcing a misleading conclusion.

## Integration

**Called by:**
- **code-reviewer** — when coverage evidence is needed as part of review
- **verification-before-completion** — when completion requires stronger regression confidence

**Feeds into:**
- review summaries
- completion verification notes
