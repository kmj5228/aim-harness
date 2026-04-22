# OFGW Harness

## Runtime Contract

Treat this directory as the standalone `ofgw-harness` runtime v1.

- Use relevant skills before improvising workflow from scratch.
- Process skills decide how to work. Execution skills carry the work out.
- If a skill is missing, stale, or insufficient, report a skill gap instead of silently bypassing it.
- This harness is runtime-facing. Template/source-only material stays in `templates/`.

## Skill Use Rules

Before starting meaningful work, check whether a matching skill exists.

Priority:

1. process and routing skills
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

## Workflow Chain

Default chain:

`issue-analysis` optional entry
-> `brainstorming`
-> `writing-plans`
-> `executing-plans` or `subagent-driven-development`
-> `test-driven-development` per task
-> `systematic-debugging` on failure
-> `verification-before-completion`
-> `finishing-a-development-branch`
-> `requesting-code-review` and `receiving-code-review`

Review and docs side flows:

- use `code-reviewer` for reviewing another PR
- use `writing-documents` for markdown/Jira/IMS/Git-style outputs
- use `manual-workflow` when a local manual draft under `generated/manual/` is required
- use `writing-skills` when creating or revising skills, support prompts, or skill authoring references inside this harness

Deferred tail:

- external manual publish stays outside v1
- `completing-patch` stays deferred in the current runtime

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
- `skills/authoring/`
  - `writing-skills`
- `skills/product/`
  - `issue-analysis`

Support assets are bundled next to their generated `SKILL.md` by default unless the adapter already gives that source asset an explicit override.

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

- Jira: `mcp` default, `api` fallback, location `atlassian-rovo`
- IMS: `browser` default, location `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`

### Spec Source

- NotebookLM: `mcp` default, `browser` fallback

### Review Target

- PR: `browser` default, location `http://192.168.51.106/openframe/openframe7/ofgw`

### Docs Target

- repo markdown: `workspace_file`, location `agent/`

### Manual Target

- manual workspace: `workspace_file`, location `generated/manual/`

## Productization Notes

- `review-context-collector` is the productized counterpart of the AIM info-collector pattern.
- `coverage-review` is the `ofgw` coverage counterpart built around JaCoCo and the confirmed Gradle coverage command.
- `manual-workflow` is the active local manual draft workflow.
- startup/runtime rules are intentionally stronger than a thin layout summary and follow the source-derived harness contract model.

## Deferred Scope

- generated external manual publish workflow
- generated `completing-patch`
- support-asset exception handling
- diff-aware coverage gating beyond the current JaCoCo-based review skill
