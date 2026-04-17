# Base Harness

## 스킬 사용 규칙

작업 시작 전 해당 스킬이 있는지 **반드시** 확인한다.
1%라도 해당 스킬이 있을 수 있으면 반드시 Skill 도구로 invoke한다.

**스킬 우선순위:**
1. 프로세스 스킬 (brainstorming-base, systematic-debugging-base) — HOW를 결정
2. 실행 스킬 (test-driven-development-base, executing-plans-base) — 실행을 안내

**과도기 원칙:** 현재 스킬 이름과 내용에 `aim` 전용 요소가 남아 있다. 기본 해석은 "공통 루프 우선, 제품 전용 절차는 product pack 후보"다.

**스킬 자가 진화 의무:** 스킬 사용 중 결함/누락/오래된 정보를 발견하면 `[Skill Gap] <skill>: ...` 형식으로 사용자에게 자발 보고한다. 에이전트가 스스로 스킬을 수정하지 않는다(사용자 권한). 상세: `using-base-harness` SKILL의 "Skill Gap Reporting" 섹션을 따른다.

## 스킬 라우팅

| 상황 | 스킬 |
|------|------|
| 새 기능/수정/리팩토링 — 설계 | brainstorming-base |
| 설계 완료, 태스크 분해 | writing-plans-base |
| 계획 실행 (순차) | executing-plans-base |
| 계획 실행 (서브에이전트) | subagent-driven-development-base |
| 독립 작업 병렬 처리 | dispatching-parallel-agents-base |
| 함수 구현 / 버그 수정 | test-driven-development-base |
| 테스트 실패, 런타임 에러 | systematic-debugging-base |
| 작업 완료 주장 전 | verification-before-completion-base |
| 테스트 통과, 브랜치 정리/리뷰 준비 | finishing-a-development-branch-base |
| feature branch 필요 | using-feature-branches-base |
| 내 코드 셀프 리뷰 | requesting-code-review-base |
| 리뷰 피드백 수신 | receiving-code-review-base |
| 타인 변경 리뷰 | code-reviewer-base |
| 스킬 작성/수정 | writing-skills-base |

## 공통 워크플로우

```
brainstorming-base → writing-plans-base
  → executing-plans-base / subagent-driven-development-base
    → test-driven-development-base (각 태스크)
      → systematic-debugging-base (실패 시)
    → verification-before-completion-base (태스크 완료 시)
    → [subagent-driven만: spec-reviewer → code-quality-reviewer, FAIL→implementer 재스폰]
  → finishing-a-development-branch-base (브랜치 정리/리뷰 준비)
    ├→ requesting-code-review-base (셀프 리뷰)
    ├→ receiving-code-review-base (피드백 수신)
    └→ 제품별 review / merge workflow

독립 스킬:
  code-reviewer-base (타인 변경 리뷰, 다단계 리뷰 오케스트레이션)
  dispatching-parallel-agents-base (독립 문제 병렬 디버깅/조사)
  using-feature-branches-base (브랜치 관리)
  writing-skills-base (스킬 작성)
```

제품 전용 번들은 기본 스킬 라우팅에서 분리했다.

- 위치: `product-specific/skills/`
- 현재 product pack: `issue-analysis-base`, `writing-documents-base`, `completing-patch-base`
