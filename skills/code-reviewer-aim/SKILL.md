---
name: code-reviewer-aim
description: "Use when reviewing someone else's AIM merge request or when triggered by requesting-code-review-aim for self-review. Requires MR number and topic name."
---

# Code Reviewer AIM — AIM 코드 리뷰 자동화 파이프라인

IMS/Jira/GitLab 정보 수집부터 코드/테스트/커버리지 리뷰, 종합 보고서, GitLab MR 코멘트 등록까지 에이전트 팀이 자동 수행한다.

## 경로 규칙

본 스킬의 모든 경로에서 `../agent/`는 **aim 프로젝트 루트 기준 상대 경로**이다.
- 프로젝트 루트: aim repo 루트 (`git rev-parse --show-toplevel`). 절대 경로는 머신마다 다르므로 하드코딩하지 않는다
- `../agent/` → aim repo 의 형제 `agent` 디렉터리
- 예: `../agent/prompt/<topic>/02_code_review.md`

파일 Read/Write 시 반드시 aim 루트를 working directory로 사용한다.

## 에이전트 구성 (스킬 동봉 prompt 5개)

base role name과 prompt 파일 매핑. **스폰 시 이름을 주지 않는다** — 재호출은 스폰이 발급한 `agentId`로 한다(아래 "에이전트 식별 규칙" 참조).

| base role | prompt 파일 | 역할 | Phase |
|-----------|------------|------|-------|
| `aim-info-collector` | `./info-collector-prompt.md` | IMS/Jira/GitLab/git 정보 수집 | B |
| `aim-code-reviewer` | `./code-reviewer-prompt.md` | C 코드 리뷰 (스타일+보안+성능+아키텍처 통합) | D |
| `aim-test-reviewer` | `./test-reviewer-prompt.md` | GoogleTest 리뷰 | D |
| `aim-coverage-analyst` | `./coverage-analyst-prompt.md` | gcov 커버리지 측정 | D |
| `aim-review-synthesizer` | `./review-synthesizer-prompt.md` | 종합/문서화/GitLab 코멘트 초안 | E |

에이전트 스폰 시 해당 prompt 파일을 Read하여 내용을 Agent 도구의 prompt에 포함한다. 스폰 결과의 `agentId`는 즉시 plan 파일 에이전트 표에 기록한다.

## 입력 파싱

사용자 입력에서 아래 정보를 추출한다:
- **topic** (필수): 예 `acsapi_aix_351005_6293`
- **Jira key** (필수): 예 `OFV7-6293`
- **MR 번호** (필수): 예 `!577`
- **IMS 번호** (선택): topic에서 자동 추출 가능 (예: `351005`)
- **branch명** (선택): 사용자가 지정하면 사용, 미지정 시 MR API `source_branch`에서 자동 추출
- **`--auto`** (선택): 중간 확인 없이 완전 자동 실행
- **추가 컨텍스트** (선택)

topic에서 IMS 번호를 자동 추출: `<keyword>_<IMS번호>_<Jira번호>` 패턴에서 두 번째 숫자 그룹.

## 에이전트 식별 규칙 (agentId 기반, 필수)

> **이름으로 부르지 않는다.** 스폰이 발급한 `agentId`로만 재호출한다.

**왜 이름을 쓰면 안 되는가**: `SendMessage`의 `to`는 **전역 네임스페이스**를 탐색한다 — 먼저 in-process subagent 이름을 찾고, 없으면 **다른 세션(peer session) 목록에서 검색**한다. 그런데 현재 `Agent` 도구에는 **`name`/`team_name` 파라미터가 없어** 스폰한 subagent에 이름을 붙일 수 없다. 따라서 이름으로 SendMessage하면 **in-process 매칭이 100% 실패하고 곧장 peer session 검색으로 넘어가, 우연히 이름이 겹치는 다른 세션에 메시지가 배달된다.** 세션에 topic명을 붙이는 습관이 있으면 확률이 더 올라간다(`ListAgents`로 실제 peer session 목록을 볼 수 있다).

**agentId는 세션-로컬 고유값**이라 이 문제가 원리적으로 없다. 다른 세션은 내 subagent를 `ListAgents`에서 볼 수도, 호출할 수도 없다.

**규칙**:
1. `Agent` 스폰 결과에 포함된 `agentId`(형식 `a...`)를 **즉시 plan 파일의 에이전트 표에 기록**한다.
2. Phase D·E·F·H의 모든 재호출은 `SendMessage(to: "<agentId>", ...)`로 한다. **이름·역할명을 `to`에 넣지 않는다.**
3. `Agent` 도구의 `description`은 사람이 읽는 라벨일 뿐 라우팅에 쓰이지 않는다. 짧게 역할을 적는다(예: `MR657 gtest 링크 검증`).
4. 같은 역할의 팀원이 이미 있으면 **`Agent` 재스폰 금지** — 기록해 둔 agentId로 `SendMessage` 재활용한다(재스폰 시 Phase D 컨텍스트가 사라진다).

**plan 파일에 유지할 표** (Phase A에서 만들고 스폰할 때마다 갱신):

```markdown
## 에이전트 (agentId — SendMessage 타겟)

| 역할 | agentId | 스폰 Phase | 산출물 |
|------|---------|-----------|--------|
| info-collector     | `a...` | B | `01_info_collection.md` |
| code-reviewer      | `a...` | D | `02_code_review.md` |
| test-reviewer      | `a...` | D | `03_test_review.md` |
| coverage-analyst   | `a...` | D | `04_coverage.md` |
| review-synthesizer | `a...` | E | `05_review_summary.md` |
```

**에이전트 간 통신**: subagent는 서로의 agentId를 모르므로 **직접 통신을 전제하지 않는다.** 역할 간 정보 전달이 필요하면 (a) 오케스트레이터가 산출물 파일을 읽어 다음 스폰 prompt에 넣거나, (b) 각 prompt에 필요한 사실을 미리 주입한다. prompt 파일에 등장하는 peer 호명(예: "테스트 리뷰어에게 전달")은 **오케스트레이터 경유**로 해석한다.

> **왜 topic-slug 규칙이 사라졌나**: 구 규칙은 `~/.claude/teams/<team>/inboxes/` 디렉토리 충돌을 막기 위한 것이었다. 현재 `Agent` 도구는 그 인프라를 쓰지 않고 in-process subagent를 만들며, 격리는 agentId가 구조적으로 보장한다. 이름 규칙을 정교화하는 방향은 오히려 **peer session 오배송 경로를 여는** 역효과다.

## 워크플로우

**절대 규칙: Phase는 반드시 A → B → C → D → E → F → G → H → I 순서로 실행한다. 어떤 Phase도 건너뛰거나 병합하지 않는다. 각 Phase의 gate 조건을 충족해야만 다음 Phase로 진행한다.**

---

### Phase A: 준비 (오케스트레이터 직접)

**최소 필수 입력: MR 번호**만 있으면 나머지는 자동 추출 가능.

입력 우선순위:
1. 사용자가 명시적으로 제공한 값을 최우선 사용
2. 미제공 필드는 MR API에서 자동 추출:
   - **branch**: MR `source_branch`
   - **topic**: MR `source_branch` (branch명을 topic으로 사용)
   - **Jira key**: MR description에서 `OFV7-XXXX` 패턴 추출
   - **IMS 번호**: MR description 또는 커밋 메시지에서 `IMS#XXXXXX` 패턴 추출
3. 자동 추출 실패 시 사용자에게 텍스트로 요청

MR 번호조차 없으면 사용자에게 "MR 번호를 알려주세요"라고 요청한다.

**실행 모드**는 `AskUserQuestion`으로 선택:
```
AskUserQuestion(questions: [
  {
    question: "실행 모드를 선택해주세요",
    header: "모드",
    options: [
      { label: "풀 리뷰 (Recommended)", description: "코드+테스트+커버리지 전체 리뷰" },
      { label: "코드만", description: "코드 리뷰만 수행" },
      { label: "테스트만", description: "테스트 리뷰만 수행" },
      { label: "커버리지만", description: "커버리지 측정만 수행" }
    ],
    multiSelect: false
  }
])
```

수행:
1. `../agent/prompt/<topic>/` 디렉토리 생성
2. 입력 정리하여 `../agent/prompt/<topic>/00_input.md` 저장
3. 워크스페이스 결정 (아래 "워크스페이스 결정" 참조)
4. plan 파일에 **에이전트 표**(빈 상태) 생성 — 위 "에이전트 식별 규칙" 참조. 이후 스폰할 때마다 `agentId`를 채운다. **이 표가 없으면 Phase H에서 팀원을 재활용할 수 없다**(재스폰하면 Phase D 컨텍스트가 사라진다)

#### 워크스페이스 결정 (오케스트레이터 직접)

리뷰는 사용자의 main aim 작업 흐름을 보호하기 위해 **worktree 격리**를 default로 한다.

판단 분기:
- main aim이 이미 리뷰 대상 branch + clean(`dx git status --short` 빈 출력) → main 사용 허용
- 그 외 → worktree 사용

```bash
# 자동 판단:
dx bash -c "cd /root/ofsrc/aim && [ \"\$(git branch --show-current)\" = \"<대상_branch>\" ] && [ -z \"\$(git status --short)\" ] && echo 'main_ok' || echo 'use_worktree'"
```

worktree 사용 시:
- 명명: `review_<MR번호>` (work용 `<keyword>_<IMS>_<Jira>`와 구분, 충돌 회피)
- **fetch 선행 (필수)**: 타인 MR의 리뷰 대상 branch는 거의 항상 원격(origin) 전용이라 로컬 ref가 없다. worktree_add.sh는 base를 로컬 ref로 요구하므로, fetch 없이 실행하면 `fatal: not a valid object name: '<대상_branch>'`로 실패한다. 생성 전에 대상 branch를 로컬로 fetch한다:
```bash
# 1. 리뷰 대상 branch를 로컬로 fetch (원격 전용 대비)
dx bash -c "cd /root/ofsrc/aim && git fetch origin <대상_branch>:<대상_branch>"
# 2. worktree 생성
dx bash -c "cd /root/ofsrc/aim && ./script/worktree_add.sh review_<MR번호> review_<topic>_<MR번호> <대상_branch>"
```
- **실패 시 cleanup**: worktree_add.sh가 중간 실패하면 `aim_worktrees/review_<MR번호>/` 빈 디렉토리가 잔존하여 재시도가 `Worktree directory already exists`로 다시 실패한다. 빈 잔여 디렉토리는 `worktree_remove.sh`가 처리하지 못하므로 `rmdir <empty_dir>` 후 재시도한다(내용이 있으면 `rmdir`가 거부하므로 안전).
- 본 worktree는 throwaway 용도로, Phase G/I 종료 시 정리한다.

이후 **본 스킬이 사용하는 작업 경로(WORKSPACE_AIM)** 가 결정된다:
- main 사용 시: aim repo 루트 (`git rev-parse --show-toplevel`)
- worktree 사용 시: `<ofsrc>/aim_worktrees/review_<MR번호>/aim/` (`worktree_add.sh` 산출 위치, `<ofsrc>` = aim repo 의 부모)

오케스트레이터는 Phase B~F의 모든 spawn prompt에 `WORKSPACE_AIM` 경로를 명시한다 (예: "작업 경로: <WORKSPACE_AIM>"). 커버리지 분석가를 포함한 5명 모두 같은 `WORKSPACE_AIM`에서 동작한다 (aim repo MR !597 머지로 워크트리 측정이 main과 동등하게 가능).

운영 규칙(install/서버기동 금지 등)과 셋업 절차 상세는 SSoT 참조:
- 운영 규칙: `aim/AGENTS.md` "Worktree Operations" 섹션
- 셋업 절차: **using-feature-branches-aim** 스킬

#### cross-module 의존 인지 (오케스트레이터 직접)

AIM MR이 **미머지 base MR의 신규 심볼**(매크로/타입/함수)에 의존하면, base 미머지 상태에서 AIM 단독 빌드·커버리지 측정이 불가능하다 → CI red는 코드 결함이 아니라 **구조적 의존**이다. 다음을 점검한다.

1. AIM MR description에 base cross-link이 있으면 그 base MR을 사용한다.
2. 링크가 없으면 OFV7 Jira description "Design > BASE" + 작성자 comment에서 base MR을 식별한다.
3. 식별한 base MR의 head SHA를 `base_mr_sha`로 확보한다 (`GET .../merge_requests/<base_iid>` 응답 `diff_refs.head_sha`, 또는 base repo `git rev-parse <base_branch>`).

cross-module 의존이 식별되면 Phase D에서 coverage-analyst에 `base_mr_sha`를 함께 주입한다(측정 전 base swap 필요). 측정 mechanics는 coverage-analyst-prompt.md "cross-module 의존 측정" 참조.

**Phase A gate**: `00_input.md` 파일이 존재하고 워크스페이스가 결정되어야 Phase B 진행.

---

### Phase B: 정보 수집 (info-collector 에이전트)

**반드시 Agent 도구로 info-collector를 스폰한다. 오케스트레이터가 직접 수행하지 않는다.**

```
Agent(
  subagent_type: "general-purpose",
  prompt: "<info-collector-prompt.md의 내용> + <00_input.md의 내용>"
)
```

스폰 결과의 `agentId`를 plan 파일 에이전트 표에 기록한다(Phase H 재활용에 필요).

에이전트 완료를 기다린 후 산출물을 확인한다.

**Phase B gate**: `01_info_collection.md` 파일이 존재하고, "변경 내용 초안" 섹션이 포함되어야 Phase C 진행.

---

### Phase C: Plan 생성 (오케스트레이터 직접)

**반드시 `01_info_collection.md`를 읽고 plan 파일을 생성한다. 이 Phase를 건너뛰지 않는다.**

1. `01_info_collection.md` 기반으로 `../agent/prompt/<topic>/<topic>_review.plan.md` 생성
   - 기존 plan 구조 준수: 주제/목표/작업전제/Jira-MR요약/변경내용초안/Phase Plan
2. `--auto`가 아닌 경우: `AskUserQuestion`으로 plan 확인
   ```
   옵션: "실행" / "수정 후 실행" / "중단"
   ```
3. "중단" 선택 시 워크플로우 종료
4. "수정 후 실행" 선택 시 사용자 피드백 반영 후 plan 업데이트

**Phase C gate**: `../agent/prompt/<topic>/<topic>_review.plan.md` 파일이 존재하고, 사용자가 승인(또는 --auto)해야 Phase D 진행.

---

### Phase D: 리뷰 실행 (3개 에이전트 병렬)

**반드시 Agent 도구로 3개 리뷰어를 동시에 스폰한다. 오케스트레이터가 직접 리뷰하지 않는다.**

```
Agent(description: "<topic> 코드 리뷰",     subagent_type: "general-purpose", prompt: ...)
Agent(description: "<topic> 테스트 리뷰",   subagent_type: "general-purpose", prompt: ...)
Agent(description: "<topic> 커버리지 측정", subagent_type: "general-purpose", prompt: ...)

→ 반환된 agentId 3개를 plan 파일 에이전트 표에 기록한다.
```

각 에이전트의 prompt에 `01_info_collection.md`의 내용과 해당 에이전트 prompt 파일 내용을 포함한다.

**작업 경로 주입(필수)**: 각 spawn prompt에 Phase A에서 결정된 `WORKSPACE_AIM` 경로를 명시한다 (예: "작업 경로: <WORKSPACE_AIM>"). coverage-analyst를 포함한 모든 에이전트가 같은 워크스페이스에서 동작한다. (aim repo MR !597의 `measure_diff_cov.sh` PWD 인지 + `env.sh` LD prepend로 워크트리 측정이 main과 동등.)

**cross-module 의존 주입(해당 시)**: Phase A에서 base MR 의존이 식별됐으면 coverage-analyst prompt에 `base_mr_sha`와 base 변경 파일 목록도 명시한다. coverage-analyst가 측정 전 base 파일을 swap하고 측정 후 즉시 복원한다(절차는 coverage-analyst-prompt.md "cross-module 의존 측정" 참조).

역할 간 정보 전달 (subagent는 서로의 agentId를 모르므로 **오케스트레이터 경유**):
- 코드 리뷰어 → 테스트 리뷰어: 복잡 함수 목록, 보안 관련 사항
- 테스트 리뷰어 → 커버리지 분석가: 테스트 실행 경로/필터

| 역할 | 산출물 |
|------|--------|
| 코드 리뷰어 | `../agent/prompt/<topic>/02_code_review.md` |
| 테스트 리뷰어 | `../agent/prompt/<topic>/03_test_review.md` |
| 커버리지 분석가 | `../agent/prompt/<topic>/04_coverage.md` |

**3개 에이전트 모두 완료될 때까지 대기한다.**

**🔴 Critical 격상 시 measurement-first cross-check (필수)**

리뷰어가 finding을 🔴 Critical로 격상하기 전에는 **filesystem 존재(파일/디렉토리/Makefile/코드가 git에 있다는 사실)로부터 build graph 활성을 추론하지 말고 측정으로 검증**한다. 추론 채널과 측정 채널이 독립이어야 false-positive cycle을 깰 수 있다.

| 추론 (file presence) | 측정 (independent channel) |
|---------------------|---------------------------|
| `grep MODULE=` 결과 두 디렉토리 같음 | `grep -rn <dir>` 으로 SRC_DIRS 진입 경로 확인 |
| 디렉토리/소스 파일 존재 | 빌드 산출물 (`.gcno` / `.o` / `bin/`) 존재 확인 |
| Makefile 정의 됨 | build log에서 진입 흔적 확인 |
| 함수 정의 존재 | 호출 경로 (rg/lsp/실행 로그) 확인 |
| 테스트 파일 존재 | `report/xml/<suite>.xml` 또는 `report/log/` 결과 확인 |

오케스트레이터는 코드/테스트 리뷰어가 🔴 Critical을 보고하면 **coverage-analyst에게 measurement cross-check를 명시 요청**한다. coverage-analyst가 측정으로 활성을 confirm하기 전까지는 종합 단계에서 Critical을 잠정으로 표기하고 머지 차단 사유로 단정하지 않는다.

> ⚠️ **사고 사례 (2026-05-06 MR !602)**: code-reviewer + test-reviewer가 file presence(`grep MODULE=aimocs` 두 곳, jxalocsi 디렉토리 존재)로 "swap 발현" 추론 → 🔴 Critical 격상. 두 명이 같은 file-based 채널로 verify-each-other하여 false-positive 강화 cycle. coverage-analyst의 `grep -rn jxalocsi` (build graph 측정) + `.gcno` 0개 + `report/xml/gtest_aimocs.xml` 14 PASS 확인으로 stranded code 확정 → DORMANT로 정정. 측정 채널 부재 시 Critical 격상은 false-positive 위험.

**Phase D gate**: `02_code_review.md`, `03_test_review.md`, `04_coverage.md` 3개 파일이 모두 존재해야 Phase E 진행. (모드에 따라 해당 파일만 확인)

---

### Phase E: 종합 (review-synthesizer 에이전트)

**반드시 Agent 도구로 review-synthesizer를 스폰한다. 오케스트레이터가 직접 종합하지 않는다.**

스폰 전에 오케스트레이터가 **반드시** 아래 4개 파일을 Read하여 전체 내용을 확보한다:
1. `../agent/prompt/<topic>/01_info_collection.md`
2. `../agent/prompt/<topic>/02_code_review.md`
3. `../agent/prompt/<topic>/03_test_review.md`
4. `../agent/prompt/<topic>/04_coverage.md`

읽은 내용을 **전부** prompt에 포함하여 synthesizer를 스폰한다:
```
Agent(
  subagent_type: "general-purpose",
  prompt: """
    <review-synthesizer-prompt.md 내용>

    아래는 리뷰 입력 산출물이다. 이 내용을 빠짐없이 종합하라.

    === 01_info_collection.md ===
    <01 파일 전체 내용>

    === 02_code_review.md ===
    <02 파일 전체 내용 — 발견 사항, 수정 제안 포함>

    === 03_test_review.md ===
    <03 파일 전체 내용>

    === 04_coverage.md ===
    <04 파일 전체 내용>

    topic: <topic>
    산출물 경로: ../agent/prompt/<topic>/
  """
)
```

**핵심: 02_code_review.md의 수정 제안(🔴/🟡/🟢 발견 사항)이 05_review_summary.md와 GitLab 코멘트 초안에 빠짐없이 반영되어야 한다.**

**Phase E gate**: `05_review_summary.md` 파일이 존재하고, "최종 판정"과 "GitLab 코멘트 초안" 섹션이 포함되어야 Phase F 진행.

synthesizer 완료 후 **오케스트레이터가** `<topic>_review.plan.md`의 Phase A~E 체크박스를 `[x]`로 업데이트한다. (plan 파일 쓰기는 오케스트레이터 전용)

---


GitLab MR 코멘트의 톤/구조/심각도 표시 규칙은 **writing-documents-aim**의 gitlab-guide.md "MR 코멘트" 섹션을 참조한다.

### Phase F: GitLab 등록 (오케스트레이터 직접)

#### Step 1: 누락 검증
`05_review_summary.md`의 "코멘트 누락 검증" 섹션을 확인한다.
누락이 있으면 synthesizer에게 `SendMessage`로 보완 요청한다.

#### Step 2: 사용자 확인
`--auto`가 아닌 경우:
- 전체 코멘트 텍스트를 사용자에게 보여준다
- 라인별 코멘트 목록 (파일:라인, 심각도, 요약)을 테이블로 보여준다
- `AskUserQuestion`으로 확인: "등록" / "수정 후 등록" / "스킵"

#### Step 3: clang-format 검증
등록 전에 변경된 모든 `.c`/`.cpp`/`.h` 파일의 clang-format 준수 여부를 검증한다:
```bash
dx bash -c "cd /root/ofsrc/aim && for f in <changed files>; do diff <(clang-format \$f) \$f > /dev/null 2>&1 && echo 'OK: '\$f || echo 'DIFF: '\$f; done"
```
위반이 있으면 코멘트에 포함하여 담당자에게 안내한다.

#### Step 4: GitLab API 등록
승인 시 GitLab API로 등록 (Mac에서 직접 `curl`, project ID: 211):
- MR 전체 리뷰 코멘트 1건 (요약/finding목록/커버리지/판정/수정권고안)
- MR 라인별 코멘트 N건 (심각도/문제/수정제안/근거 포함)

> ⚠️ **리뷰 텍스트에 대문자 리터럴 `LGTM` 절대 금지** (전체/라인별 코멘트 본문·설명 문구 모두). CI `mr_lgtm_gate`는 approver allowlist 계정의 노트에서 **토큰 `LGTM`을 substring 스캔**해 승인을 판정하므로, 승인 의도가 없는 설명 문장(예: "판정(LGTM/approve)은 작성자가 직접")에 `LGTM`이 들어가면 **우발적으로 게이트를 통과**시킨다(`✅ LGTM approved by: <you>`). 필요 시 "승인 코멘트", "엘지티엠", "L-G-T-M" 등으로 우회 표기한다. (사고: 2026-07-01 MR !629 — 전체 노트의 설명 문구 `LGTM`이 게이트를 우발 통과 → 노트 PUT으로 토큰 제거 + 해당 pipeline `mr_lgtm_gate` job retry로 복구.)

**라인별 코멘트 (인라인)**: actionable 지적은 `/discussions`(resolvable)로 등록한다. `position`은 JSON content-type 필수이며, 라인 키는 **추가 라인=`new_line`, 삭제 라인=`old_line`, context=둘 다**다 — 본 PR이 삭제한 라인에 `new_line`을 쓰면 `400 Bad - line code must be valid`로 실패한다. diff 범위 밖의 라인(예: 기존 코드의 strcpy)은 inline 불가 → 일반 노트(`/notes`)로 fallback하고 본문에 파일:라인을 명시한다. 전체 규칙·payload 예시는 writing-documents-aim/gitlab-guide.md "MR 코멘트 > 인라인 코멘트" 참조.

#### Step 5: 등록 결과 검증
- notes/discussions 증가 확인
- 등록된 코멘트 수가 예상과 일치하는지 확인
- **`mr_lgtm_gate`/approvals 우발 flip 점검**: 등록한 코멘트 때문에 LGTM 게이트가 의도치 않게 통과되지 않았는지 확인한다(`GET .../merge_requests/<iid>`의 `detailed_merge_status`, 또는 최신 pipeline `mr_lgtm_gate` job status/trace의 `✅ LGTM approved by`). flip됐으면 원인 노트에서 `LGTM` 토큰 제거(PUT `.../notes/<id>`) 후 해당 gate job retry로 원복한다. (Step 4의 `LGTM` 리터럴 금지 경고 참조)

**Phase F gate**: GitLab 코멘트 등록 완료 (또는 사용자가 스킵 선택) 후 Phase G 진행.

---

### Phase G: 작성자 반영 대기 (active monitor 옵션)

Phase F 등록 완료 후 사용자에게 monitor 진입 여부를 묻는다. "예" 시 active monitor + Phase H 자동 트리거를 활성화한다. "아니오" 시 단순 idle 대기(기존 동작).

#### Step 0: 사용자 의향 확인 (필수)

```
AskUserQuestion(questions: [{
  question: "작성자 응답을 active monitor 할까요? (60s polling, 머지/수정/코멘트 자동 감지)",
  header: "Phase G monitor",
  options: [
    { label: "예 (Recommended)", description: "MR head_sha/notes/state 60s polling, 변화 시 Phase H 자동 진입 또는 보고" },
    { label: "아니오", description: "단순 idle 대기. 사용자가 명시적으로 요청할 때만 처리" }
  ],
  multiSelect: false
}])
```

"아니오" 선택 시: 팀원 idle 유지 + 사용자 명시 요청 처리(`SendMessage`로 해당 팀원 호출). Step 1~4 skip하고 Step 5만 적용.

#### Step 1: Monitor 설정 (Bash `run_in_background`, persistent)

GitLab MR API를 60초 간격 polling하여 다음 변화 감지:
- `head_sha` 변화 (새 commit push)
- `user_notes_count` 증가 (새 코멘트)
- `state` opened → merged / closed
- `pipeline_status` 변화 (정보성)

**중요 — auto-trigger 패턴**: `run_in_background` task는 *완료될 때만* 자동으로 turn에 진입한다. 중간 stdout echo는 누적만 되고 사용자가 직접 묻기 전까지 turn 미진입. 따라서 monitor가 NEW_COMMIT/NEW_NOTE를 stdout echo만 하고 sleep을 계속하면 이벤트를 잡았어도 Phase H 자동 진입이 안 된다. **이벤트 감지 시 settle window를 거쳐 `exit 0`** 하여 task 완료 notification으로 다음 phase를 trigger한다.

**Settle window (point-stable polling)**: 첫 이벤트 감지 후 즉시 exit하지 않고 `SETTLE_SECS`(default 60s) 동안 추가 변화를 기다린다. 작성자가 commit + 여러 reply를 순차 등록하는 경우 첫 이벤트로 exit하면 나머지가 누락된 채 Phase H가 시작되는 위험이 있다. 변화가 settle window 동안 멈출 때까지 반복하여 모든 이벤트를 누적한 후 exit. 절대 상한 `SETTLE_MAX`(default 1800s)로 무한 대기 방지.

```bash
SETTLE_SECS=60     # 추가 이벤트 누적 대기 window
SETTLE_MAX=1800    # 절대 상한 (작성자가 무한정 작성하는 극단 케이스 방지)

prev_sha="<HEAD_SHA>"
prev_count=<USER_NOTES_COUNT>
prev_pipe=""

# 한 번의 polling, 결과를 전역 변수에 저장
poll() {
  local resp
  resp=$(curl -s --header "PRIVATE-TOKEN: $TOKEN" "$BASE/merge_requests/<IID>" 2>/dev/null || echo '{}')
  cur_sha=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('sha') or '')" 2>/dev/null)
  cur_count=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('user_notes_count') or 0)" 2>/dev/null)
  state=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('state') or '')" 2>/dev/null)
  pipe=$(echo "$resp" | python3 -c "import json,sys; p=json.load(sys.stdin).get('pipeline') or {}; print(p.get('status') or '')" 2>/dev/null)
}

while true; do
  poll
  ts=$(date '+%Y-%m-%dT%H:%M:%S')
  event=""

  if [ -n "$cur_sha" ] && [ "$cur_sha" != "$prev_sha" ]; then
    echo "[$ts] NEW_COMMIT: $prev_sha -> $cur_sha"
    event="commit"
  fi
  if [ "$cur_count" -gt "$prev_count" ] 2>/dev/null; then
    echo "[$ts] NEW_NOTE: count $prev_count -> $cur_count"
    [ -z "$event" ] && event="note" || event="commit_and_note"
  fi
  if [ -n "$pipe" ] && [ "$pipe" != "$prev_pipe" ]; then
    echo "[$ts] PIPELINE: $prev_pipe -> $pipe"
    prev_pipe="$pipe"
    # pipeline 변화만 발생한 경우는 exit 안 함 (정보성)
  fi
  [ "$state" = "merged" ] && echo "[$ts] MR_MERGED" && exit 0
  [ "$state" = "closed" ] && echo "[$ts] MR_CLOSED" && exit 0

  # 이벤트 감지 시 settle 진입 (point-stable polling)
  if [ -n "$event" ]; then
    settle_elapsed=0
    while [ "$settle_elapsed" -lt "$SETTLE_MAX" ]; do
      baseline_sha="$cur_sha"
      baseline_count="$cur_count"
      ts=$(date '+%Y-%m-%dT%H:%M:%S')
      echo "[$ts] settling ${SETTLE_SECS}s (elapsed=${settle_elapsed}s, baseline_count=$baseline_count, baseline_sha=$baseline_sha)"
      sleep "$SETTLE_SECS"
      settle_elapsed=$((settle_elapsed + SETTLE_SECS))
      poll
      ts=$(date '+%Y-%m-%dT%H:%M:%S')

      [ "$state" = "merged" ] && echo "[$ts] MR_MERGED" && exit 0
      [ "$state" = "closed" ] && echo "[$ts] MR_CLOSED" && exit 0

      # settle window 동안 변화 있으면 누적 echo + event 라벨 갱신 + 재 settle
      change=""
      if [ -n "$cur_sha" ] && [ "$cur_sha" != "$baseline_sha" ]; then
        echo "[$ts] ALSO_NEW_COMMIT: $baseline_sha -> $cur_sha"
        change="commit"
      fi
      if [ "$cur_count" -gt "$baseline_count" ] 2>/dev/null; then
        echo "[$ts] ALSO_NEW_NOTE: $baseline_count -> $cur_count"
        [ -z "$change" ] && change="note" || change="commit_and_note"
      fi
      if [ -z "$change" ]; then
        # settle window 안에 변화 없음 → 안정 → exit
        echo "[$ts] SETTLED (no change in ${SETTLE_SECS}s)"
        echo "[$ts] EXIT_FOR_REVIEW event=$event final_count=$cur_count final_sha=$cur_sha"
        exit 0
      fi
      # 변화 있음 → event 라벨 갱신 후 재 settle
      if [ "$event" = "commit" ] && [ "$change" = "note" ]; then
        event="commit_and_note"
      elif [ "$event" = "note" ] && [ "$change" = "commit" ]; then
        event="commit_and_note"
      elif [ "$change" = "commit_and_note" ]; then
        event="commit_and_note"
      fi
    done
    # SETTLE_MAX 도달 → 강제 exit
    ts=$(date '+%Y-%m-%dT%H:%M:%S')
    echo "[$ts] SETTLE_MAX (${SETTLE_MAX}s) reached, force exit"
    echo "[$ts] EXIT_FOR_REVIEW event=$event final_count=$cur_count final_sha=$cur_sha"
    exit 0
  fi

  sleep 60
done
```

`run_in_background: true`, `timeout: 43200000` (12시간) 또는 horizon에 맞게.

> Step 3 "이벤트별 처리" 표의 분기 판정은 monitor 종료 후 turn 진입 시점에 오케스트레이터가 출력 로그를 보고 결정한다. event 라벨은 settle 누적 결과(`final_count` / `final_sha` 포함)를 사용한다 — settle 중 `ALSO_NEW_COMMIT`/`ALSO_NEW_NOTE` 라인을 확인해 누적 이벤트 전체를 검증 대상으로 삼는다.

#### Step 2: ScheduleWakeup fallback (max 1시간)

Monitor가 죽거나 멈췄을 때 안전망. 작성자 수정은 분~시간 단위이므로 짧은 polling으로 cache 유지를 시도하는 것은 비용 비효율 (cache TTL 5분 vs 작성자 응답 시간 단위).

```
ScheduleWakeup(
  delaySeconds: 3600,
  reason: "Phase G monitor liveness 점검 (작성자 응답 시간 단위 horizon)",
  prompt: "Phase G monitor 상태 점검"
)
```

> ⚠️ **사고 사례 (2026-05-06 MR !602)**: ScheduleWakeup의 `prompt`를 `/loop continue` 같은 슬래시 커맨드로 걸면 fire 시 자동으로 dynamic mode가 부팅되어 자기 강화 루프가 형성된다(의도치 않은 비용 누적·통제 손실). **fallback heartbeat 용도 ScheduleWakeup의 `prompt`는 반드시 평문 사용**.

매 wakeup 도착 시: Monitor 살아있는지 확인 → 죽었으면 재시작 → 다음 fallback ScheduleWakeup 재예약.

#### Step 3: 이벤트별 처리

| 이벤트 (Monitor 알림) | 처리 |
|----------------------|------|
| 새 commit + 새 코멘트 (양쪽 동시) | **Phase H 자동 진입** (반영 검증) |
| 새 commit만 | 사용자 보고 + Phase H 진입 의사 확인 |
| 새 코멘트만 (작성자 reply 등) | 사용자 보고 + Phase H 진입 또는 추가 응답 의사 확인 |
| `state=merged` | Monitor TaskStop + PushNotification + Phase I 진입 또는 사용자 명시 종료 대기 |
| `state=closed` | Monitor TaskStop + 사용자 보고 + 종료 |
| `pipeline_status` 변화만 (예: failed→success는 LGTM gate 자동 통과) | 정보성 보고만, Phase H 진입 안 함 |

#### Step 4: 종료 (monitor 모드)

- merged/closed 감지 시: Monitor TaskStop + PushNotification, 팀원 idle 유지하되 사용자에게 다음 단계(워크트리/팀 정리, Phase I 진행) 결정 요청.

#### Step 5: 정리 (공통 — monitor 여부 무관)

사용자가 명시적으로 종료/정리 요청하면 Monitor TaskStop(있다면) + 팀 shutdown + worktree 정리:

```bash
dx bash -c "cd /root/ofsrc/aim && ./script/worktree_remove.sh review_<MR번호>"
```

정리 절차 상세는 **using-feature-branches-aim** 스킬 참조.

---

### Phase H: 리뷰 반영 검증 (오케스트레이터 + 기존 에이전트 재활용)

담당자가 GitLab 코멘트를 확인하고 코드를 수정한 뒤, 반영 결과를 검토하는 단계.

**진입 조건 (둘 중 하나)**:
1. 사용자가 "담당자가 반영했다", "추가 리뷰", "반영 확인" 등을 요청한 경우.
2. **Phase G monitor가 새 commit + 새 코멘트를 동시에 감지하여 자동 진입한 경우** (사용자 입력 없이도 진입 가능).

**기존 에이전트를 검증 모드로 재활용한다.** Phase D에서 각 에이전트가 축적한 컨텍스트(본인이 지적한 finding, 제안한 수정 방향)를 활용하여 본인의 영역을 재검증한다.

#### Step 1: 오케스트레이터 사전 준비 (직접)

1. 새 커밋 확인:
```bash
dx git fetch origin <branch> && dx git log <이전 HEAD>..<새 HEAD> --oneline
dx git diff <이전 HEAD>..<새 HEAD>
```
2. GitLab discussion reply 수집: `GET /api/v4/projects/211/merge_requests/<iid>/discussions`
3. clang-format 검증:
```bash
dx bash -c "cd /root/ofsrc/aim && for f in <changed files>; do diff <(clang-format \$f) \$f > /dev/null 2>&1 && echo 'OK: '\$f || echo 'DIFF: '\$f; done"
```
4. 위 결과를 정리하여 에이전트에게 전달할 검증 컨텍스트를 구성한다.

#### Step 2: 에이전트 병렬 스폰 (검증 모드)

Phase D와 동일한 3명을 **검증 모드**로 재활용한다. `Agent` 재스폰 금지(Phase D 컨텍스트가 사라진다) — plan 파일 에이전트 표의 **agentId**로 `SendMessage` 한다.

각 메시지에 다음을 포함한다:
- **검증 모드** 명시: "Phase D에서 작성한 리뷰의 반영 여부를 검증하라"
- 이전 산출물 (02/03/04): 본인이 작성한 finding 목록
- 새 커밋 diff: 담당자의 수정 내용
- GitLab reply: 담당자의 답변/근거
- 05_review_summary.md: 통합 finding 상태

```
SendMessage(to: "<code-reviewer agentId>",    message: "검증 모드 ... 이전 02 + diff + reply")
SendMessage(to: "<test-reviewer agentId>",    message: "검증 모드 ... 이전 03 + diff + reply")
SendMessage(to: "<coverage-analyst agentId>", message: "검증 모드 ... make gtest + 재측정")
```

각 팀원의 검증 산출물:
| 역할 | 산출물 | 내용 |
|---------------------|--------|------|
| 코드 리뷰어 | `02_code_review.md` 업데이트 | 🔴/🟡 항목별: ✅반영 / ⚠️부분반영 / ❌미반영 / 🆕추가발견 |
| 테스트 리뷰어 | `03_test_review.md` 업데이트 | 테스트 수정 검증, Mock 구조 확인, 추가 발견 |
| 커버리지 분석가 | `04_coverage.md` 업데이트 | 커버리지 재측정 결과, 정책 충족 여부 |

#### Step 3: 종합 (review-synthesizer 재활용)

`SendMessage(to: "<review-synthesizer agentId>", ...)`로 종합을 지시한다 (재스폰 금지).
3개 검증 결과를 종합하여 `05_review_summary.md`를 업데이트한다.
- finding 상태 업데이트 (✅ 해결 / ⚠️ 부분 해결 / 🆕 추가 발견)
- 커버리지 재측정 결과 반영
- 추가 발견이 있으면 GitLab 코멘트 초안 포함

#### Step 4: 오케스트레이터 후처리 (직접)

1. 검증 보고서를 사용자에게 보여주고 확인
2. **미반영 항목**: 담당자의 미반영 근거가 타당한지 사용자와 판단
3. **추가 발견**: GitLab 추가 코멘트 등록 여부 사용자 확인
4. 반영 확인된 스레드 resolve: `PUT discussions/<id>?resolved=true`
5. plan 파일 Phase H 체크리스트 업데이트
6. 추가 발견이 있으면 담당자 수정 후 Step 1부터 반복

**Phase H gate**: 모든 🔴 항목 반영 확인 + 커버리지 정책 충족 (또는 미충족 근거 합의) 후 Phase I 진행.

---

### Phase I: 최종 판정 (오케스트레이터 직접)

#### 판정 기준
- **Approve**: 모든 🔴 해결, 커버리지 정책 충족, 추가 발견 없음
- **추가 수정 요청**: Phase H에서 미해결 항목이 남아있는 경우 → Phase H 반복

#### 진입 경로별 분기

Phase I의 수행 절차는 진입 경로에 따라 달라진다.

##### 경로 A — Phase H 완료 후 정식 진입 (reviewer 머지 전 Approve)
1. GitLab에 LGTM 코멘트 등록 (판정 요약 포함, Phase F에서 미등록 시)
2. MR Approve API 호출: `POST /api/v4/projects/211/merge_requests/<iid>/approve`
3. plan 파일 Phase I 완료 체크
4. `../agent/` git push (산출물 보존)
5. (Phase A에서 worktree를 사용한 경우) 워크트리 정리:
```bash
dx bash -c "cd /root/ofsrc/aim && ./script/worktree_remove.sh review_<MR번호>"
```

##### 경로 B — Phase G monitor가 `state=merged` 자동 감지 후 진입 (작성자 자체 머지)
이미 merged 상태이므로 Approve API와 LGTM 추가 등록은 무의미. 정리 작업만 수행.

1. ~~LGTM 코멘트 등록~~: skip (Phase F에서 이미 등록됐고 mr_lgtm_gate가 자동 인식하여 머지가 된 상태)
2. ~~MR Approve API 호출~~: skip (이미 merged)
3. plan 파일 Phase I 완료 체크
4. `../agent/` git push (산출물 보존)
5. 워크트리 정리 (위와 동일)
6. 팀 shutdown (사용자 명시 시)

## 작업 규모별 모드

| 사용자 요청 패턴 | 실행 모드 | 투입 에이전트 |
|----------------|----------|-------------|
| "코드 리뷰해줘", "전체 리뷰" | **풀 리뷰** | 5명 전원 |
| "코드만 봐줘" | **코드 모드** | info + code-reviewer + synthesizer |
| "테스트만 봐줘" | **테스트 모드** | info + test-reviewer + synthesizer |
| "커버리지만 측정" | **커버리지 모드** | info + coverage-analyst + synthesizer |

## 산출물 디렉토리

모든 산출물은 `../agent/prompt/<topic>/` 하위에 저장한다.

```
../agent/prompt/<topic>/
├── 00_input.md                    — 사용자 입력 정리
├── 01_info_collection.md          — IMS/Jira/GitLab/git 정보
├── 02_code_review.md              — 코드 리뷰 (스타일+보안+성능+아키텍처)
├── 03_test_review.md              — 테스트 리뷰
├── 04_coverage.md                 — 커버리지 측정
├── 05_review_summary.md           — 종합 보고서
└── <topic>_review.plan.md         — 리뷰 실행 계획 + Phase별 산출물
```

**파일 경로 표기 규칙**: plan 파일이나 사용자에게 산출물 경로를 안내할 때, 반드시 aim 루트 기준 전체 경로를 사용한다.
- 올바른 예: `../agent/prompt/acsapi_aix_351005_6293/02_code_review.md`
- 잘못된 예: `02_code_review.md`, `review_workspace/acsapi_aix_351005_6293/02_code_review.md`

## 오프라인 리뷰 반영 후 산출물 업데이트

Phase F 등록 전 또는 후에 오프라인 리뷰가 진행되어 담당자가 코드를 수정한 경우:

1. **새 커밋 diff 확인**: `dx git diff <이전 HEAD>..<새 HEAD>` 로 변경 사항 파악
2. **기존 finding과 대조**: 해결된 🔴/🟡 항목을 식별
3. **산출물 업데이트**:
   - `05_review_summary.md`: 해결된 항목에 ~~취소선~~ + ✅ 표시, finding 수 업데이트
   - `03_test_review.md`: 테스트 구조 변경 시 Makefile/fixture 영향 업데이트
   - `<topic>_review.plan.md`: Phase 상태 업데이트
4. **GitLab 코멘트 조정**: 이미 해결된 항목은 등록에서 제외하거나 해결 표시
5. **`../agent/` git push**: 산출물 업데이트 후 push

## Integration

**Called by:**
- **requesting-code-review-aim** — 셀프 리뷰 (--auto, Phase A~E만)
- 직접 호출 — 타인 MR 리뷰 (Phase A~I 전체)

**Feeds into:**
- **receiving-code-review-aim** — 리뷰 피드백 처리

## 에러 핸들링

| 에러 유형 | 전략 |
|----------|------|
| IMS 접근 불가 | Chrome 브라우저 미연결 시 IMS 스킵, Jira/MR만으로 진행 |
| Jira/GitLab API 실패 | 토큰/네트워크 확인 요청 후 재시도 1회 |
| 에이전트 실패 | 1회 재시도 → 실패 시 해당 영역 없이 진행, 종합 보고서에 누락 명시 |
| 커버리지 스크립트 실패 | gcda 존재 여부 확인, make gtest 재실행 안내 |
| 커버리지 스크립트 출력이 비어 있음 (특히 .l/.y 변경 PR) | .l/.y가 측정 후보에 포함됐는지, 대상 모듈이 mock-separated(.gcda 생성 대상)인지 확인. "환경 전제"의 lex/yacc 커버리지 항목 참조 |
| 대용량 diff | 변경 파일 또는 핵심 파일에 집중, 범위를 보고서에 명시 |

## 환경 전제

- 빌드/실행: `dx` (dev_exec.sh) 경유 Docker 컨테이너
- 파일 편집/읽기: `WORKSPACE_AIM` 경로 (Phase A "워크스페이스 결정"에서 결정 — main 또는 worktree)
- GitLab/Jira API: Mac에서 직접 curl
- IMS: Chrome 브라우저 자동화 (mcp__claude-in-chrome)
- 커버리지 스크립트: `aim/script/measure_diff_cov.sh`
- 커버리지 측정은 worktree에서도 사용 가능 (aim repo MR !597 머지로 `measure_diff_cov.sh` PWD 인지 + `env.sh` LD prepend가 자동 처리). 측정 영역은 main과 동등하다 — `aim/AGENTS.md` "Worktree Operations" 참조. `make`/`make gtest`는 install 안 하므로 `tmdown` 선행 불필요. 별도 `make install` 시에만 `dx tmdown -y` 선행.
- 미커버 라인 식별은 `measure_diff_cov.sh` 출력 + `dx git diff --unified=0 <base>..HEAD`로 확인. `gcov`를 직접 `grep`/`awk`로 파싱하면 메타데이터 5줄만 출력되는 재현성 있는 현상이 있으므로 금지.
- lex/yacc 변경 PR(`*.l`/`*.y`)의 커버리지: gcov가 `#line` 디렉티브를 따라 원본 `.l`/`.y` 라인 기준으로 `foo.l.gcov`/`foo.y.gcov`를 생성하므로 측정 단위는 `.l`/`.y`다(자동 재생성 `foo.c`는 측정 대상 아님 — `measure_diff_cov.sh`가 `.l`/`.y`를 후보에 포함하고 컴파일 단위 `foo.c`로 gcov 호출). lex 정규식이 입력 형식을 이미 보장한 뒤 도달하는 sscanf 실패 분기 같은 unreachable defensive guard 라인은 미커버를 정당화할 수 있으니 Critical/Major로 격상하지 말 것 — 상세는 `aim/test/unit/gtest/AGENTS.override.md` "커버리지 측정" 참조.
