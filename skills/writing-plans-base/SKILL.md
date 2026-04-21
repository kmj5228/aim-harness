---
name: writing-plans-base
description: Use when you have an approved design or clear requirements for a multi-step implementation task and need a task-by-task execution plan before coding
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has near-zero context for the current codebase. Document what changes, where it changes, how to verify it, and how to execute it as small tasks. DRY. YAGNI. TDD. Frequent checkpoints.

Assume the implementer is technically strong but unfamiliar with the repository's local structure and conventions.

**Save plans to:** the `implementation_plan` artifact in the current topic artifact workspace. The current runtime may map this to `plan_tasks.md`.

## Scope Check

If the spec covers multiple independent subsystems, suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified:

- Check naming and layout patterns in the target directory before proposing new files.
- Prefer existing local conventions over abstract global rules when they conflict.
- Each file should have one clear responsibility
- In existing code areas, follow established patterns
- Note related contracts, schemas, config, errors, or docs that must change with the code

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" — step
- "Run the targeted test to verify it fails" — step
- "Implement the minimal code to pass" — step
- "Run the targeted test to verify it passes" — step
- "Run the project verification command" — step
- "Checkpoint or commit" — step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Use subagent-driven-development-base (recommended) or executing-plans-base to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences about approach]

**Affected Components:** [modules/services/apis/ui/schema/etc.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `src/<component>/new-file.<ext>`
- Modify: `src/<component>/existing-file.<ext>`
- Modify: `src/<shared-contract>/public-api.<ext>`
- Test: `tests/<component>/new-file-test.<ext>`

- [ ] **Step 1: Write the failing test**

```text
TEST "returns a normalized result for valid input"
  EXPECT build_result("valid-input") == { ok: true, value: "valid-input" }
END
```

- [ ] **Step 2: Run the targeted test and verify it fails**

Run: `<targeted_test_command_for_this_repository>`
Expected: FAIL — `build_result` is missing or incomplete

- [ ] **Step 3: Write minimal implementation**

```text
FUNCTION build_result(input)
  IF input is empty
    RETURN { ok: false, reason: "empty-input" }
  END
  RETURN { ok: true, value: input }
END
```

- [ ] **Step 4: Run the targeted test and verify it passes**

Run: `<targeted_test_command_for_this_repository>`
Expected: PASS

- [ ] **Step 5: Run the broader verification command**

Run: `<broader_verification_command_for_this_repository>`
Expected: Tests pass, build succeeds

- [ ] **Step 6: Commit**

```bash
git add src/<component>/new-file.<ext> src/<shared-contract>/public-api.<ext> tests/<component>/new-file-test.<ext>
git commit -m "<repository-appropriate commit message>"
```
````

The example above is intentionally stack-neutral. Real plans must replace placeholder paths, commands, and commit style with exact repository-specific values after inspecting the codebase.

## Plan Code는 "스케치"다 — Implementer가 실제 코드 기준으로 교정한다

Plan에 적는 함수 시그니처, 데이터 구조, 에러 이름, 파일명은 **의도를 전달하는 스케치**다. 정확한 값을 planning 단계에서 모두 확정하려고 하면 비용이 과도해진다.

**원칙:**
- Implementer(subagent 또는 inline executor)는 plan 코드와 실제 소스가 충돌하면 **실제 소스를 기준으로 교정할 의무**가 있다.
- 교정 대상 예: 함수 시그니처, 타입 이름, 데이터 구조, 에러 이름, import/include 의존성, 테스트 헬퍼 사용 방식.
- Plan 작성자는 의도(어떤 동작을 구현할 것인가)를 명확히 하는 것에 집중한다.

**단, 경로와 스크립트는 정확해야 한다:**
- 파일 경로, 명령, 스크립트 경로, 테스트 타깃 이름은 plan 작성 시 **실제 존재하는지 확인**하고 기재한다.
- 추측으로 쓰지 말 것. 찾기 어려우면 먼저 저장소에서 확인한다.

## No Placeholders

Every step must contain actual content. These are **plan failures**:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" (without actual code)
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code)
- Steps without code blocks for code steps
- References to functions not defined in any task

## Remember
- Exact file paths always (project-root relative)
- Complete code in every step
- Exact commands for the current repository
- DRY, YAGNI, TDD, frequent commits
- **구현과 테스트를 별도 Task로 분리 금지** — 각 Task 내에서 RED(테스트 실패) → GREEN(구현) → REFACTOR. "Task N: 구현, Task M: 테스트"는 TDD 위반
- Commit/checkpoint style should match the current repository workflow

## Self-Review

After writing the plan:

1. **Spec coverage:** Skim each requirement in the `design_spec` artifact. Can you point to a task? List gaps.
2. **Placeholder scan:** Search for "TBD", "TODO", vague instructions. Fix them.
3. **Type consistency:** Do function names, signatures match across tasks?
4. **Build/test gates:** Does every task end with the right targeted verification and the right broader verification?

Fix issues inline. If a spec requirement has no task, add the task.

## Execution Handoff

After saving the plan:

> "The `implementation_plan` artifact is written in the current topic workspace. Execution options:
>
> **1. Subagent-Driven (recommended)** — fresh subagent per task, review between tasks
>
> **2. Inline Execution** — execute tasks in this session with checkpoints
>
> Which approach?"

**Subagent-Driven:** Use subagent-driven-development-base
**Inline:** Use executing-plans-base

## Integration

**Called by:**
- **brainstorming-base** — after design approval

**Feeds into (user selects):**
- **subagent-driven-development-base** (recommended) — fresh subagent per task
- **executing-plans-base** — inline execution
