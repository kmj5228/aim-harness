# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent.

```
Agent tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name] in the AIM C project.

    ## AIM Rules (MUST follow)
    - All shell commands via `dx` (dev_exec.sh): `dx make gtest`, `dx make`, `dx git ...`
    - Docker 내 검색: `grep` → `rg`, `find` → `fd`
    - TDD: RED (failing gtest) -> GREEN (minimal code) -> REFACTOR
    - Headers: `include/{MODULE}.h` (external), `{MODULE}_inner.h` (internal), `{SOURCE}.h` (source-local)
    - `include/{MODULE}.h`: `extern "C"` guard 필수 (`#ifdef __cplusplus extern "C" { #endif`)
    - Static functions needing tests: promote to `{SOURCE}.h` with underscore prefix
    - 함수 파라미터는 줄바꿈 없이 한 줄로 작성 (ColumnLimit: 0이 기존 줄바꿈을 제거하지 않음)
    - `clang-format -i` on changed files before commit
    - Never commit to `rb_73` — feature branch only
    - Commit message: `<type> <Korean description>` (콜론 없음) via file (-F) for encoding safety
    - **새 파일 생성 시 copyright 헤더 필수** (push hook이 거부함):
      `.c`/`.h`: `/* Copyright (c) 2026 TmaxSoft Co., Ltd. ... */`
      `.cpp`: `// Copyright (c) 2026 TmaxSoft Co., Ltd. ...`

    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context

    [Scene-setting: where this fits, dependencies, previous task results if relevant]

    ## Before You Begin

    If you have questions about requirements, approach, dependencies, or anything unclear:
    **Ask them now.** Raise concerns before starting work.

    ## Your Job

    Once clear on requirements:
    1. Follow TDD: write failing gtest first, then minimal C code to pass
    2. Verify: `dx make gtest` (all pass) + `dx make` (clean build)
    3. `clang-format -i` on changed files
    4. Commit your work
    5. Self-review (see below)
    6. Report back

    Work from: /root/ofsrc/aim (via dx)

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
    **Discipline:** YAGNI? Only what was requested? Followed AIM patterns?
    **Testing:** Tests verify real behavior? TDD followed? Coverage adequate?

    Fix issues before reporting.

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented
    - Test results (`dx make gtest` output)
    - Build result (`dx make` output)
    - Files changed
    - Self-review findings
    - Issues or concerns
```
