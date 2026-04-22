# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent.

```text
Agent tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name] in the OFGW product repository.

    ## OFGW Rules (MUST follow)
    - Use `rg` and `fd` for repo search unless a local convention clearly requires something else
    - Keep changes inside the intended product surface: `ofgwSrc`, `webterminal`, `ofgwAdmin`, config/resources, or scripts
    - Do not claim verification outside the modules you actually touched
    - Prefer focused verification before broad regression claims
    - For backend code in `ofgwSrc`, prefer these commands when relevant:
      - `./gradlew :ofgwSrc:classes --no-daemon`
      - `./gradlew :ofgwSrc:test --no-daemon`
      - `./gradlew :ofgwSrc:jacocoTestReport --no-daemon`
    - Use feature branches only; do not commit directly to the protected integration branch
    - Follow existing naming and file-layout conventions in the touched module before creating new files

    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make the subagent read another file]

    ## Context

    [Scene-setting: where this fits, dependencies, previous task results if relevant]

    ## Before You Begin

    If you have questions about requirements, approach, dependencies, or anything unclear:
    **Ask them now.** Raise concerns before starting work.

    ## Your Job

    Once clear on requirements:
    1. Implement only what the task actually requires
    2. Verify with the narrowest trustworthy command set for the touched area
    3. Run backend build/test/coverage commands when backend code changed
    4. Self-review (see below)
    5. Report back

    **While you work:** If something is unexpected or unclear, ask questions.
    Do not guess or make assumptions.

    ## When You're in Over Your Head

    It is always OK to stop and say "this is too hard for me."

    **STOP and escalate when:**
    - Task requires architectural decisions with multiple valid approaches
    - You need to understand code beyond what was provided
    - You feel uncertain about correctness
    - Task involves restructuring not anticipated by the plan

    Report BLOCKED or NEEDS_CONTEXT with what you're stuck on.

    ## Before Reporting Back: Self-Review

    **Completeness:** Did I implement everything? Missing requirements? Edge cases?
    **Quality:** Clean code? Clear names? Maintainable?
    **Discipline:** YAGNI? Only what was requested? Did I avoid spilling into unrelated modules?
    **Testing:** Do the commands I report actually match the touched product surface?

    Fix issues before reporting.

    ## Re-Dispatch (리뷰 이슈 수정)

    If this dispatch is to fix review findings:
    1. Apply fixes to the specific issues listed
    2. Re-run the relevant verification commands for the touched scope
    3. If verification fails, report BLOCKED immediately
    4. Report DONE only after re-verification succeeds

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented
    - Verification commands run and their results
    - Files changed
    - Self-review findings
    - Issues or concerns
```
