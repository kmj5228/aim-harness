---
name: review-context-collector
description: Use when gathering AIM issue, MR, git, and design context before running a structured code review
---

# Review Context Collector

Collect the review context before judging the patch.

This generated skill is the explicit AIM productization of the original info-collector pattern. It makes the hidden Phase B responsibility visible as its own active runtime skill.

## When to Use

- before a full AIM review
- before a self-review handoff
- when review needs IMS, Jira, MR, and git context in one place
- when a previous review needs a refreshed context snapshot

## Bound Sources

### Issue Sources

- Jira:
  - default mode: `api`
  - location: `https://tmaxsoft.atlassian.net/rest/api/2/issue/<JIRA_KEY>`
- IMS:
  - default mode: `browser`
  - location: `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`

### Review Target

- MR:
  - default mode: `api`
  - fallback: `browser`, `git`
  - location: `http://192.168.51.106/api/v4/projects/211/merge_requests`

### Repo Context

- local `dx git log`
- local `dx git diff`
- existing topic artifacts under `agent/<topic>/`

## Workflow

1. Normalize identifiers:
   - topic
   - IMS
   - Jira
   - MR IID
   - branch/base branch
2. Gather issue context from Jira and IMS when available.
3. Gather MR metadata:
   - source and target branch
   - description summary
   - discussions or open review concerns
4. Gather git context with `dx`:
   - commits in scope
   - changed files
   - production vs test split
5. Reuse any existing local artifacts:
   - `analysis_report.md`
   - `design_spec.md`
   - prior review notes
6. Write `agent/<topic>/review_context.md`

## Output Contract

Write:

- `agent/<topic>/review_context.md`

Suggested sections:

- `Review Target`
- `Issue Context`
- `Change Scope`
- `Existing Design Context`
- `Missing Context`

## Rules

- Gather context before evaluation.
- Keep provider facts and local-git facts separate.
- Do not require both IMS and Jira when only one exists.
- Prefer concise normalized context over raw dumps.
- Keep AIM-specific truths explicit:
  - project ID `211`
  - merge-request review flow
  - `dx` git usage

## Integration

**Called by:**
- **code-reviewer**
- direct review requests

**Feeds into:**
- `agent/<topic>/review_context.md`
- downstream review, coverage, and synthesis steps
