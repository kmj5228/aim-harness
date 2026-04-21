# Claude Runtime Pack

이 문서는 `base-harness`의 선택형 Claude 런타임 가이드다.
기본 규칙의 source of truth는 루트 [AGENTS.md](/home/smj/harness/base-harness/AGENTS.md:1)다.

Claude에서 사용할 때는 아래 원칙으로 읽는다.

- 루트 `AGENTS.md`의 기본 규칙을 우선 적용한다.
- 이 문서는 Claude에서 스킬 라우팅을 빠르게 잡기 위한 보조 가이드다.
- 자동 주입이 필요하면 `claude/settings.json`과 `claude/hooks/session-start.sh`를 함께 사용한다.

## 스킬 사용 규칙

작업 시작 전 해당 스킬이 있는지 **반드시** 확인한다.
1%라도 해당 스킬이 있을 수 있으면 반드시 Skill 도구로 invoke한다.

**스킬 우선순위:**
1. 프로세스 스킬 (brainstorming, systematic-debugging)
2. 실행 스킬 (test-driven-development, executing-plans)

## 스킬 라우팅

| 상황 | 스킬 |
|------|------|
| 새 기능/수정/리팩토링 — 설계 | brainstorming |
| 설계 완료, 태스크 분해 | writing-plans |
| 계획 실행 (순차) | executing-plans |
| 계획 실행 (서브에이전트) | subagent-driven-development |
| 독립 작업 병렬 처리 | dispatching-parallel-agents |
| 함수 구현 / 버그 수정 | test-driven-development |
| 테스트 실패, 런타임 에러 | systematic-debugging |
| 작업 완료 주장 전 | verification-before-completion |
| 테스트 통과, 브랜치 정리/리뷰 준비 | finishing-a-development-branch |
| feature branch 필요 | using-feature-branches |
| 내 코드 셀프 리뷰 | requesting-code-review |
| 리뷰 피드백 수신 | receiving-code-review |
| 타인 변경 리뷰 | code-reviewer |
| 스킬 작성/수정 | writing-skills |

## 공통 워크플로우

```text
brainstorming → writing-plans
  → executing-plans / subagent-driven-development
    → test-driven-development
      → systematic-debugging
    → verification-before-completion
  → finishing-a-development-branch
    ├→ requesting-code-review
    ├→ receiving-code-review
    └→ 제품별 review / merge workflow
```

독립 스킬:

- `code-reviewer`
- `dispatching-parallel-agents`
- `using-feature-branches`
- `writing-skills`

## Template Packs

생성 입력 번들은 기본 스킬 라우팅에서 분리했다.

- 위치: `templates/aim/skills/`
- 현재 source template: `issue-analysis`, `writing-documents`, `completing-patch`
