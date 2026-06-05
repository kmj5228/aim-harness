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

#### 3-A. 세션 작업 디렉토리 DONE 이동
이번 세션의 작업 디렉토리(`prompt/<topic>/`)가 완료되었으면 `prompt/DONE/<topic>/`으로 이동했는지 점검.
- 위치: `agent/prompt/DONE/`
- 패턴: `agent/prompt/<topic>/` → `agent/prompt/DONE/<topic>/`
- 적용 대상: 코드 리뷰 산출물, 디버깅 보고서, 매뉴얼 작업물 등 완료된 모든 topic 디렉토리
- 미이동 시 → `prompt/` 직접 ls 시 진행 중 topic과 시각 분리 안 됨 → 다음 세션 컨텍스트 회복 비용 증가
- **자동 이동 금지**. 발견 시 noti + `git mv prompt/<topic> prompt/DONE/<topic>` 확인 후 진행

#### 3-B. TODO 항목 DONE 이동
본 세션이 *발견 → 처리*한 skill gap/후속 보강 항목이 `prompt/TODO/`에 있다면 `prompt/TODO/DONE/`으로 이동했는지 점검.
- 위치: `agent/prompt/TODO/DONE/` (3-A와 다른 위치 — `TODO` 폴더 *내부*의 DONE)
- 패턴: `agent/prompt/TODO/<item>.md` → `agent/prompt/TODO/DONE/<item>.md`
- 적용 대상: 이전 세션이 등록한 skill gap 중 본 세션이 PR/메모리 등으로 완료한 항목
- 미이동 시 → 다음 세션이 이미 처리된 TODO를 중복 작업 위험

#### 3-C. Repo 변경사항 점검
- 변경된 파일이 각 repo에 commit/push 됐는지 (`git status --short`로 stale 잔여 점검)
- **모든 관련 repo 검사**: `aim`, `agent`, `aim-harness`, 그 외 본 세션이 건드린 모든 git repo

#### 3-D. 임시 파일 알림
- `tmp/` 안 commit_msg/payload 등 임시 파일 (강제 아님)

미반영 발견 시 → noti + 진행 여부 확인.

#### 3-E. 다른 세션 격리 점검 (agent repo commit/push 직전 필수 게이트)

여러 세션이 동시에 `agent/` repo의 다른 디렉토리에서 작업할 수 있다(예: 본 세션=A, 다른 세션=B/C). `git add .`/`git add -A` 금지로 부분 방어되지만, **path 지정 add를 하더라도 이미 다른 세션이 staged해 둔 항목이 본 세션 commit에 함께 빨려 들어가는** 사고는 막지 못한다. agent repo commit 직전 다음을 수행한다.

1. `git status --short` 전체 출력 점검.
2. staged 항목(`R/M/D/A` 좌측 컬럼) 각각이 *본 세션의 작업 디렉토리* 또는 *본 세션이 손댄 공유 파일*에서 나왔는지 분류.
   - 본 세션 식별 기준: 현재 세션의 topic prefix(예: `prompt/<topic>/`, `prompt/<ims_keyword_jira>/`) + 본 세션이 명시적으로 만진 공유 파일(`prompt/TODO/<this_session_artifact>.md`, memory 등).
3. 다른 세션 흔적 **짝짓기 휴리스틱**(자동 식별은 어려우나 플래그 후보):
   - **짝짓기 패턴**: `D prompt/TODO/<topic>.md` + `?? prompt/DONE/<topic_dir>/` + `?? prompt/TODO/<topic>_followups.md` → 다른 세션이 closing 진행 중. 분리 필수.
   - **working tree only(`?M`)가 본 세션 작업 디렉토리 밖**이면 다른 세션 소유 → commit 대상 아님.
   - **untracked 디렉토리**가 본 세션 외 topic이면 무시.
4. 다른 세션 항목이 staged이거나 working tree에 섞여 있으면 본 세션 commit에서 분리한다. **(권장) pathspec commit**을 우선한다:
   - **(권장) pathspec commit** — `git commit -- <본 세션 경로들>`로 지정 경로만 커밋한다. index에 남아 있는 다른 세션 staged 항목은 **건드리지 않고 그대로 보존**되므로, 그 세션이 자기 의도대로 이어서 commit할 수 있다. rename은 old·new 경로를 둘 다 pathspec에 명시한다(`git commit -- prompt/TODO/x.md prompt/TODO/DONE/x.md`).
   - **(대안) `git restore --staged <path>`** — 다른 세션 staged 항목을 unstage한 뒤 본 세션분만 commit. 단 이는 *그 세션의 staged 상태를 변경(간섭)*하므로, pathspec으로 분리 가능하면 restore 대신 pathspec을 쓴다.
5. commit 전 staged/대상 명단을 한 줄씩 시각 확인(restore 방식은 `git diff --cached --name-status`, pathspec 방식은 commit할 경로 목록) — 본 세션 의도와 일치하는지 사용자에게 보고 후 commit. **commit 후** 다른 세션 staged/untracked 항목이 보존됐는지 `git status --short`로 재확인한다.

> ⚠️ **사고 사례 (2026-06-04 세미나 세션 종료)**: closing 중 `git status --short` 전수 점검에서 다른 세션(DCMS gtest 통합)이 staged해 둔 `D prompt/TODO/dcms_test_binary_unification.md`를 발견. 그대로 commit했다면 DCMS 세션이 *짝지어 add하려던* `?? prompt/DONE/dcms_gtest_unify_6751/`·`?? prompt/TODO/dcms_gtest_followups.md`와 분리되어 어색한 중간 상태로 push될 뻔했다. `git restore --staged`로 unstage 후 본 세션분만 commit하여 가로챔을 방지.

> ✅ **검증 (2026-06-05 governance/skill 배치 세션)**: 동일 구도 재현 — agent repo에 DCMS(`D dcms_test_binary_unification.md` staged)와 NDB 세션의 미commit 작업이 다수 공존. 이번엔 `git restore --staged`(타 세션 간섭) 대신 `git commit -- <본 세션 9개 경로 + plan>`으로 **pathspec commit**하여 DCMS staged·NDB untracked를 무손상 보존했다. commit 후 `git status`로 `D dcms_test_binary_unification.md`가 그대로 staged임을 재확인. → pathspec commit이 restore보다 우월(타 세션 staged를 unstage하지 않음)함이 실증됨.

> ⚠️ **사고 사례 (2026-05-14 ld_write_354377_6919 세션)**: 본 Step 3가 "TODO 작업 산출물이 `DONE/`으로 이동됐는지" 한 줄로만 명시되어 (3-A)/(3-B) 두 layer를 묶어 표현. 작업자가 (3-B) TODO/DONE만 인지하고 (3-A) 작업 디렉토리 DONE을 떠올리지 못해 새 TODO를 잘못 등록하는 재 retro 발생. 사용자 지적으로 (3-A) 누락 발견. 본 보강은 그 사고 후속.

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
| 3 | (3-A) `ls prompt/` 진행 중 topic + (3-B) `ls prompt/TODO/` 처리 항목 + (3-C) `git status --short` (모든 관련 repo) + (3-D) 임시 파일 + (3-E) 다른 세션 격리 점검 (`git diff --cached --name-status`로 staged 명단 확인) | noti + confirm |
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
