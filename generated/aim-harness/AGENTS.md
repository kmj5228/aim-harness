# AIM Harness

## Runtime Contract

Treat this directory as the standalone `aim-harness` runtime v1.

- This file is the startup contract for this harness.
- On `startup`, `resume`, `clear`, and `compact`, re-load this contract before improvising workflow.
- Use relevant skills before improvising workflow from scratch.
- Process skills decide how to work. Execution skills carry the work out.
- If a skill is missing, stale, or insufficient, report a skill gap instead of silently bypassing it.
- Do not silently self-edit shared or generated harness skills during normal task execution.
- This harness is runtime-facing. Template/source-only material stays in `templates/`.

## Skill Use Rules

Before starting meaningful work, check whether a matching skill exists.

If there is even a plausible matching skill, read it first.

Priority:

1. process and routing skills
   - `using-aim-harness`
   - `issue-analysis`
   - `brainstorming`
   - `systematic-debugging`
   - `verification-before-completion`
2. execution and branch/review skills
   - `writing-plans`
   - `executing-plans`
   - `subagent-driven-development`
   - `test-driven-development`
   - `finishing-a-development-branch`
   - `requesting-code-review`
   - `receiving-code-review`
   - `code-reviewer`
3. docs/manual skills
   - `writing-documents`
   - `manual-workflow`
4. authoring skills
   - `writing-skills`

Skill gap rule:

- If the harness lacks an appropriate skill or the existing skill is clearly stale, report the gap explicitly instead of pretending the harness already covers it.
- Use the form `[Skill Gap] <skill>: <problem>` when the gap is concrete.

## Skill Routing

| Situation | Skill |
|-----------|-------|
| Session start or startup contract re-entry | `using-aim-harness` |
| Jira / IMS issue analysis, bug triage | `issue-analysis` |
| New feature, change, or refactor design | `brainstorming` |
| Design complete, task decomposition needed | `writing-plans` |
| Sequential execution of a plan | `executing-plans` |
| Plan execution with delegated workers | `subagent-driven-development` |
| Independent work that can run in parallel | `dispatching-parallel-agents` |
| Function implementation or bug fix | `test-driven-development` |
| Test failure or runtime investigation | `systematic-debugging` |
| Completion claim before review or handoff | `verification-before-completion` |
| Branch finalization and MR preparation | `finishing-a-development-branch` |
| Feature branch management | `using-feature-branches` |
| Self-review before requesting review | `requesting-code-review` |
| Review feedback intake and follow-up | `receiving-code-review` |
| Review of another MR | `code-reviewer` |
| Review context collection | `review-context-collector` |
| Coverage interpretation for touched modules | `coverage-review` |
| Markdown, Jira, Confluence, IMS, mail, MR-style output | `writing-documents` |
| Local manual drafting under `generated/manual/` | `manual-workflow` |
| Skill authoring or support-asset authoring | `writing-skills` |

## Workflow Chain

Default chain:

`using-aim-harness`
-> `issue-analysis` optional entry
-> `brainstorming`
-> `writing-plans`
-> `executing-plans` or `subagent-driven-development`
-> `test-driven-development` per task
-> `systematic-debugging` on failure
-> `verification-before-completion`
-> `finishing-a-development-branch`
-> `requesting-code-review` and `receiving-code-review`

Subagent review loop:

- when `subagent-driven-development` is used, support prompts under that skill may help with:
  - spec review
  - implementation
  - code quality review
- if delegated work fails a quality gate, rerun the loop instead of treating the first output as final

Review and docs side flows:

- use `code-reviewer` for reviewing another MR
- use `review-context-collector` before deep review when issue, module, or review context is incomplete
- use `coverage-review` when coverage claims depend on the confirmed `dx make gtest` / `measure_diff_cov.sh` flow
- use `writing-documents` for markdown, Jira, Confluence, IMS, GitLab-style, and mail outputs
- use `manual-workflow` when a local manual draft under `generated/manual/` is required
- use `writing-skills` when creating or revising skills, support prompts, or skill authoring references inside this harness

Deferred tail:

- external manual publish stays outside v1
- `completing-patch` stays deferred in the current runtime

## Active Skill Layout

- `skills/meta/`
  - `using-aim-harness`
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
- `skills/authoring/`
  - `writing-skills`
- `skills/product/`
  - `issue-analysis`

Support assets are bundled next to their generated `SKILL.md` by default unless the adapter already gives that source asset an explicit override.

When a bundled support asset exists next to a skill:

- prefer reading it before inventing a new format or prompt shape
- treat it as runtime support, not as template residue
- if it still looks source-biased or product-inaccurate, route the problem through refinement rather than silently ignoring it

## Runtime Conventions

- Topic artifacts live under `agent/<topic>/`
- Shared markdown outputs default to `agent/`
- Manual workspace defaults to `generated/manual/`
- Canonical filenames remain:
  - `analysis_report.md`
  - `design_spec.md`
  - `plan_tasks.md`

## Access Bindings

### Issue Sources

- Jira: `api` default, location `https://tmaxsoft.atlassian.net/rest/api/2/issue/<JIRA_KEY>`
- IMS: `browser` default, location `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`

### Spec Source

- NotebookLM: `mcp` default, `browser` fallback, location `xsp-specification`

### Review Target

- MR: `api` default, browser/git fallback, location `http://192.168.51.106/api/v4/projects/211/merge_requests`

### Docs Target

- repo markdown: `workspace_file`, location `agent/`

### Manual Target

- manual workspace: `workspace_file`, location `generated/manual/`

## Productization Notes

- `review-context-collector` is the productized counterpart of the AIM info-collector pattern.
- `coverage-review` is the `aim` coverage counterpart built around the confirmed `dx make gtest` and diff-coverage helper flow.
- `manual-workflow` is the active local manual draft workflow.
- `writing-skills` is carried as a shared authoring family under `skills/authoring/`.
- startup/runtime rules are intentionally stronger than a thin layout summary and follow the source-derived harness contract model.

## Deferred Scope

- generated external manual publish workflow
- generated `completing-patch`
- marker-driven manual follow-up after merge
