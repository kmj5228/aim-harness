---
name: review-context-collector
description: Use when gathering issue, PR, diff, and design context before running a structured osd code review
---

# Review Context Collector

Collect the review context before judging the patch.

This skill is the `osd`-safe productized counterpart of the AIM info-collector pattern. It keeps the reusable context-gathering role, but removes AIM-only project IDs, fixed topic naming, and legacy output assumptions.

## When to Use

- Before a full review of an `osd` change
- Before a self-review handoff
- When a review needs issue context plus repo diff context
- When a prior review needs a refreshed context snapshot

## Bound Sources

### Issue Sources

- Jira
  - default mode: `mcp`
  - fallback: `api`
  - location: `atlassian-rovo`
- IMS
  - default mode: `browser`
  - location pattern: `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`

### Review Target

- PR
  - default mode: `browser`
  - fallback: `git`
  - location: `http://192.168.51.106/openframe/openframe7/osd`

### Repo Context

- local git history and diff
- local design notes if they exist under `agent/<topic>/`

## Inputs

Collect whatever is available:

- topic or review identifier
- PR URL or branch name
- base branch if known
- Jira key if known
- IMS number if known
- optional design note or issue summary already prepared in `agent/<topic>/`

Do not block on every input. Continue with partial context and mark what is missing.

## Workflow

### Step 1: Normalize Inputs

- identify the review artifact
- identify the comparison base if known
- normalize issue identifiers

### Step 2: Gather Issue Context

Try in this order:

1. Jira via MCP
2. Jira via API fallback if configured
3. IMS via browser when an IMS number exists

Collect only review-relevant context:

- summary
- status
- description or problem statement
- reproduction or environment notes when visible
- known user-facing impact

If one provider is unavailable, continue and record the gap.

### Step 3: Gather Review Target Context

Collect:

- PR or branch identifier
- source and target branch if available
- description summary
- changed files
- notable discussions or open concerns if visible

If the browser target is unavailable, fall back to local git context.

### Step 4: Gather Repo Diff Context

Use git to capture:

- commit list in scope
- diff summary
- changed file groups
- obvious risk-heavy files or modules

For `osd`, call out whether the change is mainly in:

- `src/lib`
- `src/server`
- `src/tool`
- `src/util`
- operational scripts under `dist/` or other non-runtime support paths

Prefer concise facts over long raw output dumps.

### Step 5: Reuse Existing Local Context

If the topic workspace already contains:

- `analysis_report.md`
- `design_spec.md`
- prior review notes

reuse them instead of re-deriving the same context.

### Step 6: Write Review Context

Write the collected result to:

- `agent/<topic>/review_context.md`

Suggested shape:

```markdown
# Review Context

## Review Target
- artifact:
- branch or diff base:

## Issue Context
- Jira:
- IMS:

## Change Scope
- commits:
- changed files:
- high-risk areas:

## Existing Design Context
- linked docs:

## Missing Context
- unresolved identifiers:
- unavailable providers:
```

## Rules

- Gather context before evaluation.
- Keep evidence and inference separate.
- Do not claim issue details that you could not verify.
- Do not require both Jira and IMS; use what exists.
- Do not assume AIM-style topic naming.

## Error Handling

| Case | Action |
|------|--------|
| Jira unavailable | continue with repo context and mark missing Jira details |
| IMS unavailable | continue and mark IMS as not reviewed |
| PR page unavailable | fall back to branch + git diff context |
| missing topic workspace | create only the review context artifact path you need |

## Integration

**Called by:**
- **code-reviewer** — when the review needs a dedicated context pass first
- Direct review requests — when issue and diff context must be gathered before analysis

**Feeds into:**
- **code-reviewer** — as the prepared context layer for review execution
