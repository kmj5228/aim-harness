# Base Harness Agents

## Purpose

`base-harness`의 기본 런타임은 Codex다.

- 루트 `AGENTS.md`는 Codex가 바로 따르는 실제 하네스 규칙이다.
- `skills/`는 기본 base runtime skill set이다.
- `templates/`는 generation source pack 영역이다.
- `adapters/`는 제품별 adaptation draft 영역이다.
- `generated/`는 생성된 제품 하네스 초안 영역이다.
- `hooks/`는 Codex hook source-of-truth다.
- `claude/`는 선택형 Claude runtime pack이다.

루트에는 활성화된 Codex 런타임 파일을 직접 두지 않는다.
Codex 기본 진입점은 이 문서와 `skills/`다.

## Core Runtime Boundary

- 기본 런타임 규칙: `AGENTS.md`
- 기본 스킬 세트: `skills/`
- generation source packs: `templates/`
- product adaptation drafts: `adapters/`
- generated product harnesses: `generated/`
- Codex hook source: `hooks/`
- 선택형 Claude 자산: `claude/`
- 마이그레이션 기록: `MIGRATION.md`

`templates/` 아래의 문서는 기본 스킬 라우팅에 자동 포함되지 않는다.
명시적으로 generation source를 읽을 때만 사용한다.

## Skill Rule

관련 스킬이 있으면 행동 전에 먼저 사용한다.

우선순위:

1. 프로세스 스킬
2. 실행 스킬
3. 협업 스킬
4. template source pack

우선 확인 대상:

- `brainstorming`
- `writing-plans`
- `executing-plans`
- `subagent-driven-development`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`
- `receiving-code-review`
- `code-reviewer`
- `harness-initiator`
- `writing-skills`

## Skill Routing

| Situation | Skill |
|------|------|
| 새 기능/수정/리팩토링 설계 | `brainstorming` |
| 설계 후 태스크 분해 | `writing-plans` |
| 계획을 순차 실행 | `executing-plans` |
| 계획을 서브에이전트로 실행 | `subagent-driven-development` |
| 독립 작업 병렬 처리 | `dispatching-parallel-agents` |
| 구현/버그 수정 | `test-driven-development` |
| 실패 분석/원인 추적 | `systematic-debugging` |
| 완료 주장 전 검증 | `verification-before-completion` |
| feature branch/workspace 분리 | `using-feature-branches` |
| 브랜치 정리/리뷰 준비 | `finishing-a-development-branch` |
| 셀프 리뷰 요청 | `requesting-code-review` |
| 리뷰 피드백 처리 | `receiving-code-review` |
| 타인 변경 리뷰 | `code-reviewer` |
| 제품 하네스 생성/적응 | `harness-initiator` |
| 스킬 작성/수정 | `writing-skills` |

## Default Workflow

```text
brainstorming
  -> writing-plans
  -> executing-plans / subagent-driven-development
     -> test-driven-development
     -> systematic-debugging (when needed)
     -> verification-before-completion
  -> finishing-a-development-branch
     -> requesting-code-review
     -> receiving-code-review
```

독립 스킬:

- `dispatching-parallel-agents`
- `code-reviewer`
- `using-feature-branches`
- `writing-skills`

## Template Pack Rule

아래 경로는 기본 런타임 스킬이 아니다.

- `templates/aim/skills/issue-analysis`
- `templates/aim/skills/completing-patch`
- `templates/aim/skills/writing-documents`
- `templates/aim/review/code-reviewer/*`

사용 조건:

- `harness-initiator`로 source template를 읽을 때
- 제품별 generation input을 분석할 때
- base runtime 밖의 product-bound workflow를 분해할 때

## Execution And Verification

- 비자명한 작업은 설계 후 실행한다.
- 실행 중에는 태스크 단위 검증과 최종 검증을 분리한다.
- 검증 없이 완료를 주장하지 않는다.
- 완료 보고에는 실제 실행한 검증 또는 검증하지 못한 이유를 포함한다.

## Skill Gap Reporting

스킬이 오래됐거나 실제 저장소 상태와 어긋나면 사용자에게 보고한다.

형식:

```text
[Skill Gap] <skill-name>
Finding: <what is wrong>
Evidence: <file, command, or observed behavior>
Proposal: <specific improvement>
```

## Document Ownership

- `AGENTS.md`: Codex 기본 런타임 규칙
- `README.md`: 구조와 사용법
- `MIGRATION.md`: 마이그레이션 이력과 판단 로그
- `HARNESS_INITIATOR.md`: initiator 방향, 검증 기준, flow I/O, refinement 경계
- `templates/`: source template packs
- `hooks/`: Codex hook source-of-truth
- `claude/`: Claude 사용자용 선택형 runtime pack

새 runtime-specific 자산은 루트에 바로 두지 않는다.
필요하면 별도 디렉토리 아래에 모은다.
