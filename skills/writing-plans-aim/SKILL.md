---
name: writing-plans-aim
description: Use when you have a spec or requirements for a multi-step AIM task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the AIM codebase. Document everything: which files to touch, code, test steps, how to verify. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled C developer, but know almost nothing about AIM modules or the OpenFrame environment.

**Save plans to:** `../agent/prompt/<topic>/plan_tasks.md`

## Scope Check

If the spec covers multiple independent subsystems, suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified:

- Follow AIM header conventions: `include/{MODULE}.h` (external), `{MODULE}_inner.h` (internal), `{basename}.h` (source-local, 확장자 `.c` 제외)
- **신규 파일 네이밍은 동일 디렉터리의 기존 파일 패턴을 먼저 확인한다** (`ls <target_dir>`). 규칙과 기존 관행이 충돌하면 기존 관행을 우선. 예: `src/server/dcms/`는 `{basename}.h` 형식 (`ld.h`, `msgq.h`) → 신규 `assign.c`의 헤더는 `assign.h` (❌ `assign.c.h`).
- Each file should have one clear responsibility
- In existing AIM modules, follow established patterns
- Note errcode/msgcode files that need updates

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing gtest" — step
- "Run `dx make gtest` to verify it fails" — step
- "Implement the minimal C code to pass" — step
- "Run `dx make gtest` to verify it passes" — step
- "Run `dx make` to verify production build" — step
- "Commit" — step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use subagent-driven-development-aim (recommended) or executing-plans-aim to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences about approach]

**Affected Modules:** [lib/svr/tool/util modules]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `src/lib/module/new_file.c`
- Create: `src/lib/module/new_file.h`
- Modify: `src/lib/module/existing.c:123-145`
- Modify: `include/module.h` (add new API)
- Test: `test/unit/gtest/test_module_new_file.cpp`

- [ ] **Step 1: Write the failing gtest**

```cpp
TEST(ModuleNew, HandlesValidInput) {
    int rc = aim_module_new_func("valid_input");
    EXPECT_EQ(rc, AIM_OK);
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `dx make gtest`
Expected: FAIL — `aim_module_new_func` not defined

- [ ] **Step 3: Write minimal implementation**

```c
int aim_module_new_func(const char *input) {
    if (input == NULL) return AIM_ERR_INVALID_PARAM;
    return AIM_OK;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `dx make gtest`
Expected: PASS

- [ ] **Step 5: Verify production build**

Run: `dx make`
Expected: Build complete, no warnings

- [ ] **Step 6: Commit**

```bash
dx git add src/lib/module/new_file.c src/lib/module/new_file.h test/unit/gtest/test_module_new_file.cpp
dx git commit -F /tmp/commit_msg.txt
# commit_msg.txt: "<feat> module new_func 추가\n\n    - 변경사항\n\n #OFV7-XXXX"
```
````

## Plan Code는 "스케치"다 — Implementer가 실제 코드 기준으로 교정한다

Plan에 적는 함수 시그니처, 에러 상수, 헤더 가드는 **의도를 전달하는 스케치**다. 정확한 값을 brainstorming 단계에서 모두 확인하려면 시간이 폭증한다.

**원칙:**
- Implementer(subagent 또는 inline executor)는 plan 코드와 실제 소스가 충돌하면 **실제 소스를 기준으로 교정할 의무**가 있다.
- 교정 대상 예: 함수 시그니처 (`int` vs `uint32_t(*)(...)`), 에러 상수 (`-1` vs `AIMCOM_ERR_NOTFND`), `extern "C"` 가드 누락, `#include` 의존성.
- Plan 작성자는 의도(어떤 동작을 구현할 것인가)를 명확히 하는 것에 집중한다.

**단, 경로와 스크립트는 정확해야 한다:**
- 파일 경로, 스크립트 경로, 바이너리 이름은 plan 작성 시 **실제 존재하는지 확인**하고 기재한다.
- 예: 커버리지 스크립트는 `./script/measure_diff_cov.sh`가 아니라 `.claude/skills/code-reviewer-aim/scripts/measure_diff_cov.sh`이다.
- 추측으로 쓰지 말 것. 찾기 어려우면 메모리의 `reference_*`를 확인한다.

**gtest 스케치의 예외:**

함수 구현 코드 스케치는 implementer가 실제 소스 기준 교정 가능. 그러나 **gtest 스케치는 canonical 형식을 Plan 단계에서 유지한다**.

- HP_/E_ prefix, 섹션 마커, Suite comment, TEST body 구조 주석을 Plan 스케치에도 포함
- Plan의 non-canonical 스케치를 implementer가 답습하거나 기존 레거시 파일 스타일을 따라가는 경향 발견 (IMS#353696)
- **Plan 작성 시 Read 필수**: `aim/test/unit/gtest/AGENTS.override.md` (gtest 태스크 포함 시)

## No Placeholders

Every step must contain actual content. These are **plan failures**:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" (without actual code)
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code)
- Steps without code blocks for code steps
- References to functions not defined in any task

## Remember
- Exact file paths always (AIM root-relative)
- Complete code in every step
- Exact commands: `dx make gtest`, `dx make`, `dx git ...`
- DRY, YAGNI, TDD, frequent commits
- **구현과 테스트를 별도 Task로 분리 금지** — 각 Task 내에서 RED(테스트 실패) → GREEN(구현) → REFACTOR. "Task N: 구현, Task M: 테스트"는 TDD 위반
- Korean commit messages via file (-F) to avoid encoding issues

## Self-Review

After writing the plan:

1. **Spec coverage:** Skim each requirement in design_spec.md. Can you point to a task? List gaps.
2. **Placeholder scan:** Search for "TBD", "TODO", vague instructions. Fix them.
3. **Type consistency:** Do function names, signatures match across tasks?
4. **Build/test gates:** Does every task end with `dx make gtest` + `dx make`?

Fix issues inline. If a spec requirement has no task, add the task.

## Execution Handoff

After saving the plan, present two independent choices to the user (둘 다 default 강제 없이 사용자가 명시적으로 선택):

> "Plan saved to `../agent/prompt/<topic>/plan_tasks.md`.
>
> ### Workspace
> **1. Worktree** — 격리 디렉토리(`<ofsrc>/aim_worktrees/<wt>/aim`), 병렬 작업 안전, 빌드 산출물 분리
> **2. Branch only** — 원본 트리에서 `git checkout -b`, 경량 셋업
>
> ### Execution approach
> **1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks
> **2. Inline Execution** — execute tasks in this session with checkpoints
>
> Which workspace? Which approach?"

두 답변을 받은 뒤:

**Workspace setup:** Use using-feature-branches-aim
- 사용자가 Worktree 선택 → Option A 흐름(`./script/worktree_add.sh`)
- 사용자가 Branch only 선택 → Option B 흐름(`dx git checkout -b`)

**Execution:**
- **Subagent-Driven:** Use subagent-driven-development-aim
- **Inline:** Use executing-plans-aim

워크스페이스 결정은 사용자 답변 그대로 다음 실행 스킬의 Step 0에 전달한다(plan 본문에 박지 않음 — plan은 워크스페이스 중립으로 유지).

## Integration

**Called by:**
- **brainstorming-aim** — 설계 승인 후

**Feeds into (user selects):**
- **using-feature-branches-aim** — Workspace 옵션(Worktree / Branch only) 셋업
- **subagent-driven-development-aim** (recommended) — fresh subagent per task
- **executing-plans-aim** — inline execution
