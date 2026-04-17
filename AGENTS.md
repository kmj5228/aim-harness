# Base Harness Agents

## Purpose

`base-harness`의 기본 런타임은 Codex다.

- 루트 `AGENTS.md`는 Codex가 바로 따르는 실제 하네스 규칙이다.
- `skills/`는 기본 base runtime skill set이다.
- `product-specific/`는 기본 런타임에 포함하지 않는 product pack 번들이다.
- `hooks/`는 Codex hook source-of-truth다.
- `claude/`는 선택형 Claude runtime pack이다.

루트에는 활성화된 Codex 런타임 파일을 직접 두지 않는다.
Codex 기본 진입점은 이 문서와 `skills/`다.

## Core Runtime Boundary

- 기본 런타임 규칙: `AGENTS.md`
- 기본 스킬 세트: `skills/`
- 선택형 제품 확장: `product-specific/`
- Codex hook source: `hooks/`
- 선택형 Claude 자산: `claude/`
- 마이그레이션 기록: `MIGRATION.md`

`product-specific/` 아래의 문서는 기본 스킬 라우팅에 자동 포함되지 않는다.
명시적으로 제품 전용 워크플로우가 필요할 때만 사용한다.

## Skill Rule

관련 스킬이 있으면 행동 전에 먼저 사용한다.

우선순위:

1. 프로세스 스킬
2. 실행 스킬
3. 협업 스킬
4. product-specific pack

우선 확인 대상:

- `brainstorming-base`
- `writing-plans-base`
- `executing-plans-base`
- `subagent-driven-development-base`
- `test-driven-development-base`
- `systematic-debugging-base`
- `verification-before-completion-base`
- `requesting-code-review-base`
- `receiving-code-review-base`
- `code-reviewer-base`
- `writing-skills-base`

## Skill Routing

| Situation | Skill |
|------|------|
| 새 기능/수정/리팩토링 설계 | `brainstorming-base` |
| 설계 후 태스크 분해 | `writing-plans-base` |
| 계획을 순차 실행 | `executing-plans-base` |
| 계획을 서브에이전트로 실행 | `subagent-driven-development-base` |
| 독립 작업 병렬 처리 | `dispatching-parallel-agents-base` |
| 구현/버그 수정 | `test-driven-development-base` |
| 실패 분석/원인 추적 | `systematic-debugging-base` |
| 완료 주장 전 검증 | `verification-before-completion-base` |
| feature branch/workspace 분리 | `using-feature-branches-base` |
| 브랜치 정리/리뷰 준비 | `finishing-a-development-branch-base` |
| 셀프 리뷰 요청 | `requesting-code-review-base` |
| 리뷰 피드백 처리 | `receiving-code-review-base` |
| 타인 변경 리뷰 | `code-reviewer-base` |
| 스킬 작성/수정 | `writing-skills-base` |

## Default Workflow

```text
brainstorming-base
  -> writing-plans-base
  -> executing-plans-base / subagent-driven-development-base
     -> test-driven-development-base
     -> systematic-debugging-base (when needed)
     -> verification-before-completion-base
  -> finishing-a-development-branch-base
     -> requesting-code-review-base
     -> receiving-code-review-base
```

독립 스킬:

- `dispatching-parallel-agents-base`
- `code-reviewer-base`
- `using-feature-branches-base`
- `writing-skills-base`

## Product Pack Rule

아래 경로는 기본 런타임 스킬이 아니다.

- `product-specific/skills/issue-analysis-base`
- `product-specific/skills/completing-patch-base`
- `product-specific/skills/writing-documents-base`
- `product-specific/code-reviewer-base/*`

사용 조건:

- 특정 제품 절차가 명시적으로 필요할 때
- 기본 `skills/`만으로는 작업 문맥이 부족할 때
- 제품별 issue/document/review workflow를 복원해야 할 때

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
- `hooks/`: Codex hook source-of-truth
- `claude/`: Claude 사용자용 선택형 runtime pack

새 runtime-specific 자산은 루트에 바로 두지 않는다.
필요하면 별도 디렉토리 아래에 모은다.
