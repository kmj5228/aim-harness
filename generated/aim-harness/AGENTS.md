# AIM Harness

## Purpose

This directory is a regenerated `aim-harness` draft built under the current `harness-initiator` and `product-harness-refinement` model.

The target is semantic reconstruction:

- preserve the AIM development loop
- preserve AIM-specific operational truth where current generated layout can hold it
- keep the result auditable as a generated harness, not as an in-place copy of the original repo

## Active Skill Layout

- `skills/core/`
  - `brainstorming`
  - `writing-plans`
  - `executing-plans`
  - `test-driven-development`
  - `systematic-debugging`
  - `verification-before-completion`
- `skills/collab/`
  - `subagent-driven-development`
  - `dispatching-parallel-agents`
  - `using-feature-branches`
  - `requesting-code-review`
  - `receiving-code-review`
  - `finishing-a-development-branch`
- `skills/review/`
  - `code-reviewer`
  - `review-context-collector`
  - `coverage-review`
- `skills/docs/`
  - `writing-documents`
  - `manual-workflow`
- `skills/product/`
  - `issue-analysis`

## Default Workflow

```text
issue-analysis (optional entry)
  -> brainstorming
  -> writing-plans
  -> executing-plans / subagent-driven-development
     -> test-driven-development
     -> systematic-debugging
     -> verification-before-completion
  -> finishing-a-development-branch
     -> requesting-code-review
     -> receiving-code-review
```

Recognized but not yet fully regenerated:

- post-merge `completing-patch`
- full external manual publish path

## AIM Runtime Bindings

- shell/build wrapper:
  - `dx`
- release branch rule:
  - never commit directly to `rb_73`
- issue systems:
  - IMS
  - Jira
- review system:
  - GitLab merge requests
- spec source:
  - NotebookLM `xsp-specification`
- coverage policy:
  - diff-added code coverage `>= 80%`

## Runtime Conventions

- topic artifacts live under `agent/<topic>/`
- shared markdown outputs default to `agent/`
- manual drafts default to `generated/manual/`
- canonical filenames remain:
  - `analysis_report.md`
  - `design_spec.md`
  - `plan_tasks.md`
  - `review_context.md`
  - `coverage_review.md`

## Important Differences From The Original Runtime

- startup entry is `AGENTS.md` plus Codex hook, not `CLAUDE.md` plus `settings.json`
- the original `using-aim-harness` meta skill is not regenerated as a first-class active skill
- `manual-workflow` stops at local drafting under the current contract
- `completing-patch` is still deferred

These are current model differences, not accidental file loss.
