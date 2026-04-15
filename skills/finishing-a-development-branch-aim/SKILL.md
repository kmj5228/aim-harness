---
name: finishing-a-development-branch-aim
description: Use when implementation is complete, all tests pass, and you need to push and create a GitLab MR or finalize the branch
---

# Finishing a Development Branch

## Overview

Guide completion of development work: verify → clean up → push → create MR.

**Core principle:** Verify everything → Present options → Execute choice.

## The Process

### Step 1: Verify Everything

**REQUIRED:** Use verification-before-completion-aim first.

```bash
# All tests pass
dx make gtest

# Production build clean
dx make

# Coverage meets 80%
dx bash -c "cd /root/ofsrc/aim && ./script/measure_diff_cov.sh"
```

**If any fails:** Stop. Fix before proceeding.

### Step 2: Clean Up

1. **Verify branch** — not on `rb_73`
   ```bash
   dx git branch --show-current
   ```

2. **Apply formatting**
   ```bash
   # clang-format on all changed files
   dx bash -c "clang-format -i <changed-files>"
   ```

3. **Review commits** — clean, logical units
   ```bash
   dx git log --oneline rb_73..HEAD
   ```
   
   If needed, squash/reword commits. Commit message format: `<type> <Korean description>`

4. **Verify copyright headers** on new files (push hook will check)

### Step 3: Push

```bash
dx git push -u origin <branch-name>
```

If credential issue, use GitLab token URL.

### Step 4: Present Options

```
Implementation complete and pushed. What would you like to do?

1. Create GitLab MR
2. Update existing MR
3. Keep branch as-is (handle later)
4. Request self-review first (code-reviewer-aim Phase A~E)

Which option?
```

### Step 5: Execute Choice

#### Option 1: Create GitLab MR

```bash
# Mac curl (not dx) — GitLab API, base URL: http://192.168.51.106
curl -s --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "source_branch": "<feature-branch>",
    "target_branch": "rb_73",
    "title": "<type> Korean description",
    "description": "<MR description per default.md template>"
  }' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests"
```

Token: see `../agent/info/access.md`


MR description 작성 규칙 상세는 **writing-documents-aim**의 gitlab-guide.md를 참조한다.

**MR 생성 직후 — 매뉴얼 필요성 자동 판단 (필수)**:

MR 생성 후 `writing-documents-aim/manual-guide.md`의 Step 1 (필요성 판단 GATE)을 자동 호출한다. 이 단계를 건너뛰지 않는다.

1. `Read` manual-guide.md Step 1 섹션
2. 현재 MR의 변경 범위(`dx git diff rb_73..HEAD --stat` + commit 메시지 + MR 제목/본문)로 판단 기준 적용
3. **사전 체크**: `cd /Users/mjkang/company/MANUAL/openFrame_aim && git log --all --grep=<IMS번호>` + `--grep=<OFV7-num>` 양쪽으로 기존 반영 여부 확인 (manual-guide Step 1 Pre-check)
4. 판단 결과 4가지 중 하나 도출 + 사용자 선택 분기:

| 판단 | 후속 액션 | Marker 값 |
|------|---------|----------|
| **이미 반영됨** (MANUAL repo commit 존재) | commit SHA 보고 후 사용자 질의 ("재작성/보완 필요?" → 필요 시 `pending-merge`, 아니면 `done`) | 선택에 따라 |
| **추가 필요** | 사용자에게 3가지 선택: (A) 지금 작성 / (B) MR merge 후 completing-patch에서 진행 / (C) skip | A → 즉시 manual-guide Step 2~8 후 `done`, B → `pending-merge`, C → `done` |
| **추가 불필요** (내부 리팩토링 등) | 근거 보고 후 종료 | `done` |
| **애매** | 사용자 질의 후 위 중 하나로 수렴 | 선택에 따라 |

5. **Marker 삽입**: MR description 맨 아래에 HTML 주석 marker를 추가한다. 이는 `completing-patch-aim`이 merge 시점에 상태를 읽기 위함.

```
<!-- aim-harness:manual-check status=pending-merge checked=2026-04-15 -->
```

또는

```
<!-- aim-harness:manual-check status=done checked=2026-04-15 reason=not-needed -->
```

Marker 값:
- `pending-merge`: 매뉴얼 추가 필요 + MR merge 후 진행 (completing-patch에서 작성 실행)
- `done`: 이 MR에 대한 매뉴얼 판단 종료 (불필요/이미반영/지금작성완료/사용자skip). completing-patch에서 추가 판단 불필요.

6. **MR description 업데이트**:
```bash
curl -s --request PUT \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"description": "<기존 description + marker>"}' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<MR_IID>"
```

**Marker가 없는 MR**은 `completing-patch-aim`이 "판단 생략됨"으로 간주하고 merge 시점에 매뉴얼 판단을 실행한다. 따라서 Option 3(Keep as-is) 같은 경로로 MR을 만들지 않은 상태에서는 marker가 존재하지 않고, 그 경우 completing-patch에서 처리된다.

MR description follows `.gitlab/merge_request_templates/default.md`:
1. `## 내용` — 요구사항, 왜 변경하는지, 왜 이렇게 변경하는지
2. `## 수정 사항` — 변경 파일별 요약 (파일 경로 + 변경 내용)
3. `## Test` — 추가 테스트 결과(gtest) + 기존 테스트 결과(Global Coverage + 상세보기)
4. `## MR Check List` — coding convention, merge 대상, deadline, 양식, 테스트
5. `## Squash Commit Message` — `.gitmessage` 전체 포맷 (IMS#, module, version)
6. `> #OFV7-XXXX, #Deadline: YYYY-MM-DD` — Jira 티켓 + 마감일

**Test 섹션 데이터:**
- `기존`: `dx make gtest-run` 출력의 `== Global Coverage (ALL) ==` 블록 + `<details>` 전체
- `추가`: 해당 테스트만 `--gtest_filter`로 실행한 결과

#### Option 2: Update Existing MR

```bash
curl -s --request PUT \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"description": "<updated description>"}' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<MR_IID>"
```

**Update 시 매뉴얼 재판단**: MR 변경 범위가 달라졌을 수 있으므로 기존 `<!-- aim-harness:manual-check ... -->` marker 확인 후 필요시 재판단한다.
- 기존 marker가 `done`인데 변경 범위에 사용자 노출 요소가 추가되면 `pending-merge` 또는 즉시 작성으로 갱신
- 기존 marker가 `pending-merge`이고 변경이 매뉴얼 결정에 영향 없으면 그대로 유지
- 기존 marker가 없으면 Option 1과 동일하게 새로 판단

#### Option 3: Keep As-Is

Report: "Branch `<name>` pushed. Handle when ready."

#### Option 4: Self-Review

Invoke requesting-code-review-aim → code-reviewer-aim Phase A~E with `--auto`.

## Quick Reference

| Option | Push | MR | Review |
|--------|------|-----|--------|
| 1. Create MR | done | create | optional |
| 2. Update MR | done | update | optional |
| 3. Keep as-is | done | skip | skip |
| 4. Self-review | done | after review | code-reviewer-aim |

## Common Mistakes

**Skipping verification**
- Fix: Always run verification-before-completion-aim first

**Pushing to rb_73**
- Fix: Always verify branch name before push

**Missing clang-format**
- Fix: Format all changed files before final commit

**Missing copyright headers**
- Fix: Check new files have copyright in top 10 lines

## Red Flags

**Never:**
- Push with failing tests
- Create MR without verification
- Push to `rb_73`
- Skip clang-format
- Force-push without explicit request

## Integration

**Called by:**
- **subagent-driven-development-aim** — after all tasks complete
- **executing-plans-aim** — after all tasks complete

**Feeds into:**
- **completing-patch-aim** — MR merge 후 IMS 패치 검증서 작성 + 매뉴얼 marker 확인 후 후속 진행
- **writing-documents-aim / manual-guide.md** — Option 1/2 MR 생성·갱신 직후 Step 1 필요성 판단 자동 호출

**Pairs with:**
- **verification-before-completion-aim** — verify before finishing
- **requesting-code-review-aim** — optional self-review (Option 4)

## 매뉴얼 필요성 판단 Marker (상태 기반 이중 진입)

매뉴얼 작업은 다음 두 진입점을 갖는다. 상태는 MR description의 HTML 주석 marker로 유지한다.

```
<!-- aim-harness:manual-check status=<pending-merge|done> checked=<YYYY-MM-DD> [reason=<text>] -->
```

| 진입점 | 조건 | 동작 |
|--------|------|------|
| finishing-branch Step 5 Option 1/2 | MR 생성/갱신 직후 | manual-guide Step 1 실행 → marker 삽입 |
| completing-patch-aim 진입 시 | marker 없음 | 매뉴얼 판단이 생략된 상태 → 지금 판단 |
| completing-patch-aim 진입 시 | `status=pending-merge` | 이미 "필요 + merge 후 진행" 결정됨 → 바로 manual-guide Step 2~8 진행 |
| completing-patch-aim 진입 시 | `status=done` | 이미 처리 완료 → skip |
