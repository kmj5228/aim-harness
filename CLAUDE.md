# AIM Development Harness

## 스킬 사용 규칙

작업 시작 전 해당 스킬이 있는지 **반드시** 확인한다.
1%라도 해당 스킬이 있을 수 있으면 반드시 Skill 도구로 invoke한다.

**스킬 우선순위:**
1. 프로세스 스킬 (issue-analysis-aim, brainstorming-aim, systematic-debugging-aim) — HOW를 결정
2. 실행 스킬 (test-driven-development-aim, executing-plans-aim) — 실행을 안내

**스킬 자가 진화 의무:** 스킬 사용 중 결함/누락/오래된 정보를 발견하면 `[Skill Gap] <skill>: ...` 형식으로 사용자에게 자발 보고한다. 에이전트가 스스로 스킬을 수정하지 않는다(사용자 권한). 상세: `using-aim-harness` SKILL의 "Skill Gap Reporting" 섹션.

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
| MR merge 후 패치 검증서 + 매뉴얼 후속 | completing-patch-aim |
| feature branch 필요 | using-feature-branches-aim |
| 내 코드 셀프 리뷰 | requesting-code-review-aim |
| 리뷰 피드백 수신 | receiving-code-review-aim |
| 타인 MR 리뷰 | code-reviewer-aim |
| 문서 작성 (Jira/Confluence/IMS/GitLab/메일/md/**manual**) | writing-documents-aim |
| 매뉴얼 작성 (AIM 제품 매뉴얼, Antora/AsciiDoc) | writing-documents-aim → manual-guide |
| 스킬 작성/수정 | writing-skills-aim |

## 워크플로우 체인

```
issue-analysis-aim (optional entry) → brainstorming-aim → writing-plans-aim
  → executing-plans-aim / subagent-driven-development-aim
    → test-driven-development-aim (각 태스크)
      → systematic-debugging-aim (실패 시)
    → verification-before-completion-aim (태스크 완료 시)
    → [subagent-driven만: spec-reviewer → code-quality-reviewer, FAIL→implementer 재스폰]
  → finishing-a-development-branch-aim (push/MR)
    ├→ [MR create/update] → manual-guide Step 1 필요성 판단 (자동)
    │     ├→ 필요 + now   → Step 2~8 즉시 실행 + marker=done
    │     ├→ 필요 + later → marker=pending-merge (→ completing-patch Step 6)
    │     └→ 불필요/skip  → marker=done
    ├→ requesting-code-review-aim (셀프 리뷰)
    ├→ receiving-code-review-aim (피드백 수신)
    └→ [MR merged] → completing-patch-aim
          ├→ Step 0: marker 확인 (IMS 단위)
          ├→ Step 1~5: 패치 검증서 (IMS)
          └→ Step 6: marker 상태별 매뉴얼 후속
                ├→ marker 없음      → manual-guide Step 1부터 실행
                ├→ pending-merge   → manual-guide Step 2~8 직행
                └→ done            → skip

독립 스킬 (직접 호출):
  issue-analysis-aim (체인 진입점 겸 독립)
  code-reviewer-aim (타인 MR 리뷰, Phase A~I)
  dispatching-parallel-agents-aim (독립 문제 병렬 디버깅/조사)
  using-feature-branches-aim (브랜치 관리)
  writing-documents-aim (문서 작성, 7개 서브가이드: jira/confluence/ims/gitlab/mail/markdown/manual)
  writing-skills-aim (스킬 작성)
```
