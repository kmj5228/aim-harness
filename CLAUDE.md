# AIM Development Harness

## 스킬 사용 규칙

작업 시작 전 해당 스킬이 있는지 **반드시** 확인한다.
1%라도 해당 스킬이 있을 수 있으면 반드시 Skill 도구로 invoke한다.

**스킬 우선순위:**
1. 프로세스 스킬 (issue-analysis-aim, brainstorming-aim, systematic-debugging-aim) — HOW를 결정
2. 실행 스킬 (test-driven-development-aim, executing-plans-aim) — 실행을 안내

## 스킬 라우팅

| 상황 | 스킬 |
|------|------|
| IMS/Jira 이슈 분석, 버그 트리아지 | issue-analysis-aim |
| 새 기능/수정/리팩토링 — 설계 | brainstorming-aim |
| 설계 완료, 태스크 분해 | writing-plans-aim |
| 계획 실행 (순차) | executing-plans-aim |
| 계획 실행 (서브에이전트) | subagent-driven-development-aim |
| 독립 작업 병렬 처리 | dispatching-parallel-agents-aim |
| 함수 구현 / 버그 수정 | test-driven-development-aim |
| 테스트 실패, 런타임 에러 | systematic-debugging-aim |
| 작업 완료 주장 전 | verification-before-completion-aim |
| 테스트 통과, push/MR 준비 | finishing-a-development-branch-aim |
| MR merge 후 패치 검증서 | completing-patch-aim |
| feature branch 필요 | using-feature-branches-aim |
| 내 코드 셀프 리뷰 | requesting-code-review-aim |
| 리뷰 피드백 수신 | receiving-code-review-aim |
| 타인 MR 리뷰 | code-reviewer-aim |
| 스킬 작성/수정 | writing-skills-aim |

## 워크플로우 체인

```
issue-analysis-aim → brainstorming-aim → writing-plans-aim
  → executing-plans-aim / subagent-driven-development-aim
    → test-driven-development-aim (각 태스크)
    → verification-before-completion-aim (완료 시)
  → finishing-a-development-branch-aim (push/MR)
    → [MR merged] → completing-patch-aim (패치 검증서)
```
