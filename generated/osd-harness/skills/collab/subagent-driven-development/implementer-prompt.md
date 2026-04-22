# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent.

```text
Agent tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name] in the OSD product repository.

    ## OSD Rules (MUST follow)
    - Use `rg` and `fd` for repo search unless a local convention clearly requires something else
    - Keep changes inside the intended product surface: `src/lib`, `src/server`, `src/tool`, `src/util`, code tables, config/resources, or `dist/`
    - Do not claim verification outside the modules you actually touched
    - Prefer focused verification before broad regression claims
    - For normal runtime code changes, prefer:
      - `make`
      - `make -C test`
      - `test/run_coverage.sh`
    - Treat `dist/patch_osd.sh` and `dist/dist_osd.sh` as operational workflows, not default proof of runtime correctness
    - Use feature branches only; do not commit directly to the protected integration branch
    - Follow existing naming and file-layout conventions in the touched module before creating new files

    ## Task Description

    [FULL TEXT of task from plan]

    ## Your Job

    1. Implement only what the task actually requires
    2. Verify with the narrowest trustworthy command set for the touched area
    3. Run coverage only when the task actually needs coverage evidence
    4. Self-review
    5. Report back

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented
    - Verification commands run and their results
    - Files changed
    - Self-review findings
    - Issues or concerns
```
