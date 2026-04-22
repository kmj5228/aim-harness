# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent.

```
Agent tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name].

    ## Repository Rules (MUST follow)
    - Follow the repository's shell/tooling conventions
    - Prefer fast search tools already used by the repository
    - Follow TDD or the task's required verification loop
    - Match local naming, layout, formatting, and commit conventions
    - Before creating new files, inspect nearby files and follow existing patterns
    - If the plan conflicts with repository conventions, follow the repository and report the correction

    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context

    [Scene-setting: where this fits, dependencies, previous task results if relevant]

    ## Before You Begin

    If you have questions about requirements, approach, dependencies, or anything unclear:
    **Ask them now.** Raise concerns before starting work.

    ## Your Job

    Once clear on requirements:
    1. Follow the required implementation loop: failing test or targeted reproduction first, then minimal code to pass
    2. Verify with the smallest useful scope first:
       - Run the targeted verification for the exact task
       - Run the task-level build/test check required by the repository
       - Leave broad full-project regression to the orchestrator unless the task explicitly requires it
    3. Apply the repository's formatter or formatting convention to changed files
    4. Commit your work
    5. Self-review (see below)
    6. Report back

    Work from: [REPOSITORY_ROOT or WORKTREE]

    **While you work:** If something is unexpected or unclear, **ask questions**.
    Don't guess or make assumptions.

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
    **Discipline:** YAGNI? Only what was requested? Followed repository patterns?
    **Testing:** Tests verify real behavior? Required verification loop followed? Coverage or regression risk addressed?

    Fix issues before reporting.

    ## Re-Dispatch (리뷰 이슈 수정)

If this dispatch is to fix review findings (spec or code-quality):
1. Apply fixes to the specific issues listed
2. **반드시 재검증 재실행** (이전 통과 결과 재사용 금지):
   - rerun the targeted verification for the changed area
   - rerun the required task-level build/test check
   - leave broad regression to the orchestrator unless explicitly required
3. 검증 실패 시 즉시 BLOCKED 리포트 (리뷰 재요청 금지)
4. 검증 통과 시에만 DONE 리포트

## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented
    - Targeted verification results
    - Task-level build/test results
    - Files changed
    - Self-review findings
    - Issues or concerns
```
