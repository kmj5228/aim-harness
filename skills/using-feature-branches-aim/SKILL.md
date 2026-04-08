---
name: using-feature-branches-aim
description: Use when starting feature work that needs a new branch, before executing implementation plans, or when on rb_73 and about to commit
---

# Using Feature Branches

## Overview

All AIM development happens on feature branches. Never commit to `rb_73` directly.

**Core principle:** `rb_73` is the release branch. Feature branches isolate work until it's reviewed and ready.

## When to Use

- Starting new feature, fix, or refactoring
- About to commit but currently on `rb_73`
- Need to isolate experimental work
- Before executing any implementation plan

## The Rule

```
NEVER COMMIT TO rb_73
```

If you're on `rb_73`, create a feature branch BEFORE any commit.

**No exceptions:**
- Not for "just a small fix"
- Not for "I'll merge right away"
- Not for "it's already tested"

## Branch Creation

### Step 0: Verify Current Branch

```bash
dx git branch --show-current
```

If NOT `rb_73`, you already have a feature branch — proceed with work.

If `rb_73`, continue to Step 1.

### Step 1: Create Branch

**Naming convention:** `<keyword>_<IMS>_<Jira>`

```bash
# Examples:
dx git checkout -b msgrcv_335342_6293
dx git checkout -b acsapi_351005_6293
dx git checkout -b smqn_recovery_335342
```

Components:
- `keyword`: Short description of the work (module name or feature)
- `IMS`: IMS issue number (if applicable)
- `Jira`: Jira ticket number (if applicable)
- Omit IMS/Jira if not applicable, but include at least keyword

### Step 2: Verify

```bash
dx git branch --show-current
# Should show your new branch, NOT rb_73
```

### Step 3: Work

Now safe to commit:

```bash
dx git add <specific-files>
# 한글 커밋: 파일(-F)로 전달 (dx가 한글을 이중 이스케이프하여 깨뜨림)
cat > /tmp/commit_msg.txt << 'EOF'
<feat> 기능 설명

    - 변경사항

 #OFV7-XXXX
EOF
dx bash -c "git commit -F /tmp/commit_msg.txt"
```

**Remember:** `git add .` / `git add -A` prohibited. Always specify files.

## Commit Message Format

**일반 commit** (feature branch 작업 중):
```
<type> 한글 설명

    - 변경사항 1
    - 변경사항 2

 #OFV7-XXXX
```

**merge commit** (MR squash 시, `.gitmessage` 전체 포맷):
```
IMS#XXXXXX:<type> summary

    - described

    * module: module_name
    * version: 7.3.0()

 #OFV7-XXXX
```

- type: `<>` 괄호로 감싸며, 콜론 없음
- 영문 type: `feat`, `fix`, `test`, `docs`, `refactor`, `style`, `chore`
- 설명은 한글
- Jira 티켓: `#OFV7-XXXX` (브랜치명의 Jira 번호 참조)

```bash
# 예시 (한글은 파일로 전달):
cat > /tmp/commit_msg.txt << 'EOF'
<fix> SMQN recovery 판정 로직 수정

    - mqn recovery 테이블 검사 누락 수정
    - smqn만 확인하던 로직에 mqn 추가

 #OFV7-6293
EOF
dx bash -c "git commit -F /tmp/commit_msg.txt"
```

## Push

```bash
dx git push -u origin <branch-name>
```

If `could not read Username` error (Docker has no interactive terminal):
```bash
dx bash -c "git push http://oauth2:<TOKEN>@192.168.51.106/openframe/openframe7/aim.git HEAD:<branch-name>"
```
Token: see `../agent/info/access.md`

## Quick Reference

| Situation | Action |
|-----------|--------|
| On `rb_73`, about to commit | Create feature branch first |
| Already on feature branch | Proceed with work |
| Need branch name, have IMS/Jira | `<keyword>_<IMS>_<Jira>` |
| Need branch name, no ticket | `<keyword>_<brief_desc>` |
| Ready to push | `dx git push -u origin <branch>` |
| Need MR | See finishing-a-development-branch-aim |

## Common Mistakes

### Committing to rb_73

- **Problem:** Direct commits to release branch bypass review
- **Fix:** Always check `dx git branch --show-current` before committing

### Vague branch names

- **Problem:** `fix_bug` tells nothing about the work
- **Fix:** Include module name and ticket numbers: `msgrcv_335342_6293`

### Using `git add .`

- **Problem:** Stages unintended files (local configs, build artifacts)
- **Fix:** Always `dx git add <specific-files>`

## Red Flags

- About to `git commit` on `rb_73` — STOP, create branch
- Branch name with no keyword — add descriptive prefix
- Using `git add .` or `git add -A` — specify files explicitly
- Pushing to `rb_73` — STOP, you should be on a feature branch

## Integration

**Called by:**
- **brainstorming-aim** — after design approved, before implementation
- **executing-plans-aim** — before executing any tasks
- **subagent-driven-development-aim** — before dispatching implementers

**Pairs with:**
- **finishing-a-development-branch-aim** — push, MR, cleanup after work complete
