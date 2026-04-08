---
name: code-reviewer-aim
description: "Use when reviewing someone else's AIM merge request or when triggered by requesting-code-review-aim for self-review. Requires MR number and topic name."
---

# Code Reviewer AIM — AIM 코드 리뷰 자동화 파이프라인

IMS/Jira/GitLab 정보 수집부터 코드/테스트/커버리지 리뷰, 종합 보고서, GitLab MR 코멘트 등록까지 에이전트 팀이 자동 수행한다.

## 경로 규칙

본 스킬의 모든 경로에서 `../agent/`는 **aim 프로젝트 루트 기준 상대 경로**이다.
- 프로젝트 루트: `/Users/mjkang/company/dev_sshfs/aim/`
- `../agent/` → `/Users/mjkang/company/dev_sshfs/agent/`
- 예: `../agent/prompt/<topic>/02_code_review.md` → `/Users/mjkang/company/dev_sshfs/agent/prompt/<topic>/02_code_review.md`

파일 Read/Write 시 반드시 aim 루트를 working directory로 사용한다.

## 에이전트 구성 (스킬 동봉 prompt 5개)

| 에이전트 | prompt 파일 | 역할 | Phase |
|---------|------------|------|-------|
| aim-info-collector | `./info-collector-prompt.md` | IMS/Jira/GitLab/git 정보 수집 | B |
| aim-code-reviewer | `./code-reviewer-prompt.md` | C 코드 리뷰 (스타일+보안+성능+아키텍처 통합) | D |
| aim-test-reviewer | `./test-reviewer-prompt.md` | GoogleTest 리뷰 | D |
| aim-coverage-analyst | `./coverage-analyst-prompt.md` | gcov 커버리지 측정 | D |
| aim-review-synthesizer | `./review-synthesizer-prompt.md` | 종합/문서화/GitLab 코멘트 초안 | E |

에이전트 스폰 시 해당 prompt 파일을 Read하여 내용을 Agent 도구의 prompt에 포함한다.

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

**Phase A gate**: `00_input.md` 파일이 존재해야 Phase B 진행.

---

### Phase B: 정보 수집 (aim-info-collector 에이전트)

**반드시 Agent 도구로 aim-info-collector를 스폰한다. 오케스트레이터가 직접 수행하지 않는다.**

```
Agent(
  name: "aim-info-collector",
  subagent_type: "general-purpose",
  team_name: "aim-code-review",
  prompt: "<aim-info-collector.md의 내용> + <00_input.md의 내용>"
)
```

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
Agent(name: "aim-code-reviewer",    subagent_type: "general-purpose", team_name: "aim-code-review", ...)
Agent(name: "aim-test-reviewer",    subagent_type: "general-purpose", team_name: "aim-code-review", ...)
Agent(name: "aim-coverage-analyst", subagent_type: "general-purpose", team_name: "aim-code-review", ...)
```

각 에이전트의 prompt에 `01_info_collection.md`의 내용과 해당 에이전트 정의(`.claude/agents/aim-*.md`)를 포함한다.

에이전트 간 통신 (필요 시 `SendMessage`):
- aim-code-reviewer → aim-test-reviewer: 복잡 함수 목록, 보안 관련 사항
- aim-test-reviewer → aim-coverage-analyst: 테스트 실행 경로/필터

| 에이전트 | 산출물 |
|---------|--------|
| aim-code-reviewer | `../agent/prompt/<topic>/02_code_review.md` |
| aim-test-reviewer | `../agent/prompt/<topic>/03_test_review.md` |
| aim-coverage-analyst | `../agent/prompt/<topic>/04_coverage.md` |

**3개 에이전트 모두 완료될 때까지 대기한다.**

**Phase D gate**: `02_code_review.md`, `03_test_review.md`, `04_coverage.md` 3개 파일이 모두 존재해야 Phase E 진행. (모드에 따라 해당 파일만 확인)

---

### Phase E: 종합 (aim-review-synthesizer 에이전트)

**반드시 Agent 도구로 aim-review-synthesizer를 스폰한다. 오케스트레이터가 직접 종합하지 않는다.**

스폰 전에 오케스트레이터가 **반드시** 아래 4개 파일을 Read하여 전체 내용을 확보한다:
1. `../agent/prompt/<topic>/01_info_collection.md`
2. `../agent/prompt/<topic>/02_code_review.md`
3. `../agent/prompt/<topic>/03_test_review.md`
4. `../agent/prompt/<topic>/04_coverage.md`

읽은 내용을 **전부** prompt에 포함하여 synthesizer를 스폰한다:
```
Agent(
  name: "aim-review-synthesizer",
  subagent_type: "general-purpose",
  team_name: "aim-code-review",
  prompt: """
    <aim-review-synthesizer.md 에이전트 정의>

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

**라인별 코멘트 라인 번호 제약**: GitLab API는 MR diff 범위 내의 라인에만 inline comment를 달 수 있다. diff 범위 밖의 라인(예: 기존 코드의 strcpy)에 대한 코멘트는 일반 노트(note)로 fallback하고, 본문에 파일:라인을 명시한다.

#### Step 5: 등록 결과 검증
- notes/discussions 증가 확인
- 등록된 코멘트 수가 예상과 일치하는지 확인

**Phase F gate**: GitLab 코멘트 등록 완료 (또는 사용자가 스킵 선택) 후 Phase G 진행.

---

### Phase G: 대기 (오케스트레이터)

1. 모든 Phase 완료 후에도 팀원 에이전트를 **종료하지 않고 대기**
2. 사용자가 추가 질문/분석 요청 시 해당 팀원에게 `SendMessage`로 전달
   - 예: "보안 쪽 더 자세히" → aim-code-reviewer에게 전달
   - 예: "이 테스트 추가해줘" → aim-test-reviewer에게 전달
3. 사용자가 명시적으로 종료 요청할 때만 팀 shutdown 수행

---

### Phase H: 리뷰 반영 검증 (오케스트레이터 + 기존 에이전트 재활용)

담당자가 GitLab 코멘트를 확인하고 코드를 수정한 뒤, 반영 결과를 검토하는 단계.
사용자가 "담당자가 반영했다", "추가 리뷰", "반영 확인" 등을 요청하면 이 Phase를 수행한다.

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

Phase D와 동일한 3개 에이전트를 **검증 모드**로 스폰한다.
각 에이전트의 prompt에 다음을 포함한다:
- **검증 모드** 명시: "Phase D에서 작성한 리뷰의 반영 여부를 검증하라"
- 이전 산출물 (02/03/04): 본인이 작성한 finding 목록
- 새 커밋 diff: 담당자의 수정 내용
- GitLab reply: 담당자의 답변/근거
- 05_review_summary.md: 통합 finding 상태

```
Agent(name: "aim-code-reviewer",    검증 모드, prompt: 이전 02 + diff + reply)
Agent(name: "aim-test-reviewer",    검증 모드, prompt: 이전 03 + diff + reply)
Agent(name: "aim-coverage-analyst", 검증 모드, prompt: make gtest + 재측정)
```

각 에이전트의 검증 산출물:
| 에이전트 | 산출물 | 내용 |
|---------|--------|------|
| aim-code-reviewer | `02_code_review.md` 업데이트 | 🔴/🟡 항목별: ✅반영 / ⚠️부분반영 / ❌미반영 / 🆕추가발견 |
| aim-test-reviewer | `03_test_review.md` 업데이트 | 테스트 수정 검증, Mock 구조 확인, 추가 발견 |
| aim-coverage-analyst | `04_coverage.md` 업데이트 | 커버리지 재측정 결과, 정책 충족 여부 |

#### Step 3: 종합 (aim-review-synthesizer)

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

#### 수행
1. GitLab에 LGTM 코멘트 등록 (판정 요약 포함)
2. MR Approve: `POST /api/v4/projects/211/merge_requests/<iid>/approve`
3. plan 파일 Phase I 완료 체크
4. `../agent/` git push

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

## 에러 핸들링

| 에러 유형 | 전략 |
|----------|------|
| IMS 접근 불가 | Chrome 브라우저 미연결 시 IMS 스킵, Jira/MR만으로 진행 |
| Jira/GitLab API 실패 | 토큰/네트워크 확인 요청 후 재시도 1회 |
| 에이전트 실패 | 1회 재시도 → 실패 시 해당 영역 없이 진행, 종합 보고서에 누락 명시 |
| 커버리지 스크립트 실패 | gcda 존재 여부 확인, make gtest 재실행 안내 |
| 대용량 diff | 변경 파일 또는 핵심 파일에 집중, 범위를 보고서에 명시 |

## 환경 전제

- 빌드/실행: `dx` (dev_exec.sh) 경유 Docker 컨테이너
- 파일 편집/읽기: Mac SSHFS 마운트 경로 (`/Users/mjkang/company/dev_sshfs/aim/`)
- GitLab/Jira API: Mac에서 직접 curl
- IMS: Chrome 브라우저 자동화 (mcp__claude-in-chrome)
- 커버리지 스크립트: `.claude/skills/code-reviewer-aim/scripts/measure_diff_cov.sh`
