---
name: using-feature-branches-aim
description: Use when starting feature work that needs a new workspace (worktree or branch), before executing implementation plans, or when on rb_73 and about to commit
---

# Setting Up Workspace (Worktree or Branch)

## Overview

All AIM development happens on a feature branch — either inside a **git worktree** (isolated directory, recommended) or as a plain branch checkout in the original `aim` directory. Never commit to `rb_73` directly.

**Core principle:** `rb_73` is the release branch. Feature workspaces isolate work until it's reviewed and ready.

## When to Use

- Starting new feature, fix, or refactoring
- About to commit but currently on `rb_73`
- Need to isolate experimental work
- Before executing any implementation plan

## The Rule

```
NEVER COMMIT TO rb_73
```

If you're on `rb_73`, set up a feature workspace BEFORE any commit.

**No exceptions:**
- Not for "just a small fix"
- Not for "I'll merge right away"
- Not for "it's already tested"

## Workspace Setup

### Step 0: Verify Current Branch

```bash
dx git branch --show-current
```

If NOT `rb_73`, you already have a feature branch (in original tree or worktree) — proceed with work.

If `rb_73`, continue to Step 1.

### Step 1: Choose Workspace — Worktree (recommended) or Branch only

**Naming convention (both options):** `<keyword>_<IMS>_<Jira>`

```
# Examples:
msgrcv_335342_6293
acsapi_351005_6293
smqn_recovery_335342
```

Components:
- `keyword`: Short description of the work (module name or feature)
- `IMS`: IMS issue number (if applicable)
- `Jira`: Jira ticket number (if applicable)
- Omit IMS/Jira if not applicable, but include at least keyword

#### Option A: Worktree (recommended)

병렬 작업, 원본 디렉토리 보호, 독립 빌드 산출물이 필요할 때 권장. `worktree_add.sh`가 새 feature branch를 자동 생성하고 격리된 디렉토리(`<ofsrc>/aim_worktrees/<wt_name>/aim`)를 만든다.

```bash
# Direct SSH dev server 또는 Docker 내부:
cd /root/ofsrc/aim
./script/worktree_add.sh <wt_name> <new_branch> rb_73

# Mac SSHFS+Docker 환경:
# dx bash -c "cd /root/ofsrc/aim && ./script/worktree_add.sh <wt_name> <new_branch> rb_73"
```

진입:
```bash
cd /root/ofsrc/aim_worktrees/<wt_name>/aim
source /root/ofsrc/aim_worktrees/<wt_name>/env.sh   # SOURCE_BASE export
```

운영 규칙(install 금지, 서버 기동 금지, 커버리지 측정 금지 등)과 격리/공유 리소스 구분은 `aim/AGENTS.md`의 **Worktree Operations** 섹션을 참조한다.

**`git worktree add`를 직접 호출하지 말 것** — 필수 symlink(`base/batch/dev/ndb/tacf`)와 seed 파일(`make/config.local`, `make/cflags.local`, `include/build_info_aim.h`)이 누락되어 빌드 실패한다.

#### Option B: Branch only (경량)

단일 작업 흐름이거나 워크트리 인프라가 부담스러울 때. 원본 `<ofsrc>/aim` 디렉토리에서 직접 작업한다.

```bash
dx git checkout -b <new_branch>
```

### Step 2: Verify

```bash
dx git branch --show-current
# Should show your new branch, NOT rb_73
```

워크트리의 경우 `<ofsrc>/aim_worktrees/<wt_name>/aim` 디렉토리 안에서 실행하면 해당 워크트리의 branch가 표시된다.

### Step 3: Work

Now safe to commit:

> **환경별 git 실행 (env-neutral)**: pc(host)에선 git을 **host에서 직접** 실행한다(`git add` / `git commit -F`; dx 불필요 — dx는 빌드/실행 전용, pc dx는 oexec 래핑). Mac-SSHFS 환경은 아래처럼 `dx git`(컨테이너 경유). 한글 커밋 메시지는 양쪽 모두 **repo 내부에 파일로 작성한 뒤 `git commit -F`** 로 참조한다(컨테이너/dx 안 heredoc은 한글을 이중 이스케이프해 깨뜨리므로 메시지 파일은 host/Mac shell에서 작성).

```bash
# 아래는 Mac-SSHFS 예시 — pc는 `dx ` 접두어를 빼고 host에서 git 직접 실행
dx git add <specific-files>
# 한글 커밋: 메시지 파일을 repo 내부에 (host/Mac shell로) 작성한 뒤 `git commit -F` 로 참조한다.
#   - Mac `/tmp` ↔ Docker `/tmp` 는 비공유 → `/tmp/commit_msg.txt` 에 작성하면 dx 가 다른 파일을 보거나 못 찾는다.
#   - `dx bash -c "cat > ... << EOF ...한글... EOF"` 처럼 dx 안에서 heredoc 으로 작성하면 dx 가 한글을 이중 이스케이프하여 깨뜨린다.
#   - 따라서 heredoc 작성은 dx 없이(Mac shell) repo 내부 경로에 하고, dx 는 `git commit -F` 만 맡긴다.
cat > .commit_msg.tmp << 'EOF'
<feat> 기능 설명

    - 변경사항

 #OFV7-XXXX
EOF
dx git commit -F .commit_msg.tmp
rm .commit_msg.tmp
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
# 예시 — 메시지 파일을 repo 내부(SSHFS-공유)에 Mac 측에서 작성한 뒤 dx 로 commit:
#   (Mac `/tmp` 는 Docker 와 비공유, `dx bash -c` 안의 heredoc 은 한글 깨짐 — 둘 다 피한다)
cat > .commit_msg.tmp << 'EOF'
<fix> SMQN recovery 판정 로직 수정

    - mqn recovery 테이블 검사 누락 수정
    - smqn만 확인하던 로직에 mqn 추가

 #OFV7-6293
EOF
dx git commit -F .commit_msg.tmp
rm .commit_msg.tmp
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
| On `rb_73`, about to commit | Set up workspace first (worktree or branch) |
| 병렬 작업 / 원본 격리 필요 | `./script/worktree_add.sh <wt> <branch> rb_73` |
| 단일 작업, 경량 | `dx git checkout -b <branch>` |
| Already on feature branch (or in worktree) | Proceed with work |
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

### `git worktree add` 직접 호출

- **Problem:** 필수 symlink(`base`/`batch`/`dev`/`ndb`/`tacf`)와 seed 파일(`make/config.local`, `make/cflags.local`, `include/build_info_aim.h`) 누락으로 빌드 실패
- **Fix:** 항상 `./script/worktree_add.sh` 경유. 제거도 `./script/worktree_remove.sh` 경유 (메타데이터 정합)

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
