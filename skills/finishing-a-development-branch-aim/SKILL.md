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
   
   If needed, squash/reword commits. Commit message format: `<type>: <Korean description>`

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

**Pairs with:**
- **verification-before-completion-aim** — verify before finishing
- **requesting-code-review-aim** — optional self-review (Option 4)
