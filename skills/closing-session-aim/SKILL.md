---
name: closing-session-aim
description: Use when user requests to end or wrap up the current session — examples "세션 종료/마무리/끝내자/마치자", "wrap up", "close session", "오늘 작업 끝내자"
---

# Closing a Session

## Overview

세션 종료는 단순 인사말이 아니라 *현 상태를 정리해 다음 세션이 끊김 없이 진입할 수 있도록 마무리하는 마지막 작업*이다. 7개 체크포인트를 통과한 뒤에만 종료한다.

**Core principle:** 발견 즉시 사용자 noti + 진행 여부 confirm. 자동으로 destructive 작업 실행 금지(브랜치 삭제·commit·push 등).

## When to Use

사용자가 세션 종료/마무리를 요청할 때 즉시 발동. 신호 예:
- "세션 종료하자/마무리하자/끝내자/마치자"
- "wrap up", "close session", "we're done"
- "오늘 작업 끝내자"

다른 작업 요청이 함께 들어오면 그쪽을 먼저 처리한 뒤 본 스킬 재진입.

## The 7-Step Closure

### Step 1 — 세션 진행 요약
이번 세션에서 *실제로 한 일*을 표/리스트로 사실 위주 1줄씩.
- 새 commit/MR/브랜치
- 수정·삭제한 파일
- 외부 시스템 변경 (GitLab MR, Jira/IMS comment, GitHub push 등)

narrative 금지. 짧고 사실만.

### Step 2 — 미처리 작업 검토
사용자 요청 중 *완료되지 못한* 항목 점검:
- TODO 발견했지만 미작성/미반영
- 리뷰 응답 미제출
- merge 후 후속(`completing-patch-aim`) 미실행
- "나중에 한다"로 미뤄둔 항목

발견 시 → 사용자 noti + "이대로 종료 / 지금 처리" 확인.

### Step 3 — 산출물 정리 점검
- TODO 작업 산출물이 `DONE/`으로 이동됐는지
- 변경된 파일이 각 repo에 commit/push 됐는지 (`git status --short`로 stale 잔여 점검)
  - **모든 관련 repo 검사**: `aim`, `agent`, `aim-harness`, 그 외 본 세션이 건드린 모든 git repo
- 임시 파일(`tmp/` 안 commit_msg/payload 등) 알림 (강제 아님)

미반영 발견 시 → noti + 진행 여부 확인.

### Step 4 — 브랜치/워크트리 정리 점검
- merge된 feature branch 로컬 잔존: `git branch --merged rb_73 | grep -v 'rb_73\|^\*'`
- 사용 끝난 워크트리: `git worktree list` (원본 외 검토)

자동 삭제 금지. 발견 시 사용자 confirm 후 `git branch -d` / `worktree_remove.sh`.

### Step 5 — 세션 산출 MR 상태 보고
이번 세션에서 만든/갱신한 MR을 list:

```
| MR  | 제목 | 상태 |
|-----|------|------|
| !N  | ...  | open / merged / 리뷰 대기 / 신규 댓글 X건 |
```

리뷰 대기 중이거나 신규 댓글 발생 시 사용자에게 명시 — 종료 후 놓치지 않도록.

### Step 6 — memory 자가 점검
이번 세션에서 학습한 *사용자 운영 선호*나 *사고 사례* 중 memory 미저장 항목 점검.

저장 후보 신호:
- 사용자 명시 운영 지시 ("매번 X로", "default는 Y", "X는 항상 물어봐")
- 재발 방지 가치 있는 사고 사례 (자가 default 미스, 절차 누락 등)
- 새 외부 시스템 정보 (URL/토큰 위치/스프레드시트 등 → `reference` type)

**SSoT 중복 회피**: governance/CLAUDE.md/AGENTS.md에 이미 있는 사실은 memory 저장 금지.

발견 시 → noti + 저장 여부 확인.

### Step 7 — 자가 회고 / Skill Gap 보고
다음을 1~3줄로 요약:

- **자가 운영 미스**: 잘못된 default 선택, 절차 누락, 사용자가 정정 요청한 항목
- **Skill Gap**: 기존 스킬/governance가 다루지 못한 케이스 (이미 TODO 작성했으면 파일명 언급)
- **`[Check Fail]` / `DONE_WITH_CONCERNS`**: 미해결 채로 진행한 항목

이미 처리·기록된 건 reference만. 새 발견은 *후속 결정* (TODO 작성/스킬 수정 PR/그대로 두기) 사용자 제시.

## Quick Reference

| Step | 도구 | 발견 시 |
|------|------|--------|
| 1 | 세션 message scan | 사실 보고만 |
| 2 | 사용자 요청 vs 처리 결과 비교 | noti + confirm |
| 3 | `git status --short` (모든 관련 repo) | noti + confirm |
| 4 | `git branch --merged` / `git worktree list` | noti + confirm |
| 5 | gh/curl (GitLab MR API) | 상태 + 신규 댓글 명시 |
| 6 | memory dir review | noti + confirm |
| 7 | 세션 message scan (회고) | 새 발견 시 후속 결정 제시 |

## Common Mistakes

- **단순 "수고하셨습니다"로 종료** — 7단계 누락 → 다음 세션 컨텍스트 회복 비용 증가
- **자동 destructive 작업 실행** — 사용자 confirm 없이 브랜치 삭제·commit·push 금지. 항상 noti 후 진행
- **Skill Gap 보고 누락** — 자가 회고 영역. 보고 자체가 시스템 학습 시작점
- **memory와 governance 중복 저장** — SSoT 분기 위험. memory는 governance에 없는 *운영 선호*/*사고 사례*만

## Red Flags

- "별다른 거 없어서 종료" → 그래도 7 step 모두 1줄씩 점검 결과 명시
- "사용자가 명시 지시 안 했으니 skip" → step 5/6/7은 사용자 명시 지시 없이 자발 점검 영역
- "한 곳 commit만 했으니 OK" → step 3은 본 세션이 건드린 *모든 repo* 검사 (aim/agent/aim-harness 등)
