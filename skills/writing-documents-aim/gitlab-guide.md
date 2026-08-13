# GitLab 작성 가이드

> 가독성 공통 규칙(인라인 열거 분리, 한 단락 한 개념, blockquote 강조, 구조적 데이터→표/list, 빈 줄 호흡)은 `markdown-guide.md`의 "가독성 핵심 원칙"을 참조한다. 아래는 GitLab 특수 규칙만 다룬다.

## MR Description

MR description은 **finishing-a-development-branch-aim** 스킬이 담당한다.

핵심 규칙 요약 (`.gitlab/merge_request_templates/default.md` 기반):

### 섹션별 상세 (default.md 원문 기준)

**`## 내용`**
- 어떤 요구사항으로 변경하는지 (버그/신기능)
- 왜 변경하는지
- 왜 이렇게 변경하는지

**`## 수정 사항`**
- 수정된 부분의 요약
- 수정 후 변경되는 결과

**`## Test`**

추가:
- `- [ ] 테스트가 추가 되었는가?`
- 해당 테스트만 `--gtest_filter`로 실행한 결과 코드 블록

기존:
- `- [ ] 기존 unit test는 성공했는가?`
- `== Global Coverage (ALL) ==` 블록 복사 (SCOPE 표 헤더/구분선/`ALL(src)` 행/`GLOBAL_COVERAGE_RESULT` 라인 모두 포함)
- `<details><summary>상세보기</summary>` 안에는 `dx make gtest` stdout을 **있는 그대로 verbatim 붙여넣는다**. 요약/필터링/재구성 금지. 반드시 아래 섹션이 **모두** 포함되어야 한다:
  - `== GoogleTest Summary ==` — `BIN_DIR`, `REPORT_DIR`, `XML_DIR`, `LOG_DIR`, `AIM_ROOT`, `MODULELIST_FILE` 경로 라인 포함 + **`BINARY` 전체 표** (개별 바이너리 수십 행, 0개 테스트 행도 그대로) + `RESULT`/`TOTAL_TESTS`/`TOTAL_FAIL`/`TOTAL_ERROR`/`FAILED_BINARIES` 요약
  - `== Module Summary (official modules only) ==` — **ModuleList 전체 모듈** (테스트 0개 `N/A` 행도 그대로 유지, 삭제 금지) + `COVERAGE_RESULT` + `MIN_LINE` 라인
  - `== Unmatched module aliases (need hardcoding) ==` — 이 섹션이 출력되면 통째로 포함 (나중에 모듈 별칭 hardcoding 대상 추적용, 절대 생략 금지)
  - `== Global Coverage (ALL) ==` — `GLOBAL_COV_FILTER` 경로 포함

> 적신호 체크는 문서 하단 `## Self-review checklist (적신호)` 섹션 기준 — PUT/갱신 직전 필수.

**`## MR Check List`** — [양식 링크](https://tmaxsoft.atlassian.net/l/cp/oRSZFaP2)

> REVIEW BLOCKER: 아래 MR Check List가 모두 체크되지 않으면 리뷰 불가능

- `- [ ] coding convention은 확인 했는가?`
- `- [ ] merge 대상 브랜치가 올바른가?`
- `- [ ] deadline은 알맞게 정했는가?`
- `- [ ] 그 외 MR 양식에 맞게 작성했는가?`
- `- [ ] 테스트가 추가 되었는가?`

**`## Reviewers`**
- Reviewer는 MR Check List를 모두 확인 후 리뷰 진행
- 리뷰 완료 후 Approve 또는 Request Changes 선택
- Approve시 댓글로 LGTM 남기기

**`> #OFV7-XXXX, #Deadline: YYYY-MM-DD`**

**`## Squash Commit Message`**
```
IMS#X:<X> X

    - 

    * module: X
    * version: X

 #OFV7-XXXX
```

**복수 모듈인 경우** — `* module` / `* version` 블록을 모듈 개수만큼 분리하여 반복한다 (한 줄에 쉼표로 나열 금지):
```
IMS#352569:<feat> ACS 호환 프로시저 DCPRES 매크로 PF키 AID 정의 기능 개발

    - assign.c ACS 차단 제거 후 DCPRES 엔트리 기반 AID 해석 추가
    - ...

    * module: libaimais
    * version: 7.3.0()

    * module: aimdcms
    * version: 7.3.0()

 #OFV7-6158
```
❌ 잘못된 예: `* module: libaimais, aimdcms`

### Module 결정 규칙 — 대상(무엇을 넣나)

`* module` 목록은 "내가 고친 파일이 속한 모듈"이 아니라 **이 패치로 나가는 산출물 전부**다. 소스를 건드리지 않은 모듈도 바이너리가 바뀌면 포함한다.

- **공개 헤더(`include/*.h`)를 고치면 그 헤더를 include 하는 모든 모듈이 대상**이 될 수 있다. 헤더가 심볼·구조를 바꾸면 재빌드 산출물이 달라지기 때문이다.
- 판정은 **추론이 아니라 바이너리 체크섬**으로 한다. "실행 동작이 안 바뀐다"와 "바이너리가 안 바뀐다"는 다른 명제다 — 전자가 참이어도 후자는 거짓일 수 있다.

```bash
# 수정 전/후 각각 클린빌드하여 체크섬 비교 (같은 워크트리·같은 경로에서)
dx bash -c 'cd <aim> && git checkout origin/rb_73 -- include/<changed>.h && make clean && make -j16'
#   → 산출물 md5 기록 (BEFORE)
#   → 동일 소스로 한 번 더 빌드해 md5 가 같은지 확인 (재현성 — 이게 같아야 차이를 변경 탓으로 귀속 가능)
dx bash -c 'cd <aim> && git checkout HEAD -- include/<changed>.h && make clean && make -j16'
#   → 산출물 md5 기록 (AFTER). BEFORE 와 다르면 그 모듈은 bump·module 목록 대상.
```

> 실측 사례: `include/aimsmr.h` 의 `typedef` 누락만 정정했는데(실행 동작 불변) 미사용 전역 심볼이 사라지며 소비 모듈 3개(`libaimsmr`·`aimidcm`·`aimsmradm`) 바이너리가 모두 변경됐다. 처음엔 1개만 기재해 리뷰에서 지적받았다.

**함정 2가지**
- `-fno-common` 이 켜진 워크트리에서는 수정 전(BEFORE) 빌드가 아예 실패할 수 있다(tentative-def 다중정의). 비교하려면 `make/cflags.local` 을 `-fcommon` 으로 임시 조정 후 **원복**한다.
- **`lib` 타입은 patch 번호가 파일명에 들어간다**(`libaimsmr.so.64.7_3_0_7`). bump 후 이전 파일명으로 확인하면 "반영 안 됨"으로 오판한다. `svr`/`tool`/`util` 은 파일명 고정이라 내부 문자열만 바뀐다.

### Version 기재 규칙 — 언제 값을 넣나

`* version` 은 **bump 후 값**(이 패치로 배포될 값)이다. 작성 시점의 현재값이 아니다.

- version bump 는 governance 상 **approve 후 merge 직전**에 하므로, Squash 메시지를 MR 생성 시 쓰면 **값이 비거나(`7.3.0()`) 옛 값이 남는 시차**가 생긴다.
- 따라서 **bump 커밋을 넣은 직후 Squash 메시지의 `* version` 을 갱신**한다. 선행 MR 이 같은 모듈을 먼저 올렸으면 그 번호를 이어받는다(예: `aimdcms` 65→66 머지 후 다음 MR 은 66→67).

### Module 이름 형식 규칙

`* module`의 표기는 Makefile의 `MODULE` 변수가 아니라 **설치되는 산출물 이름**을 사용한다.

| Makefile TYPE | 산출물 이름 규칙 | 예시 |
|---|---|---|
| `lib` | `lib<MODULE>` | `MODULE=aimap` → `libaimap` |
| `svr` | `<MODULE>` | `MODULE=aimdcms` → `aimdcms` |
| `tool` | `<MODULE>` | `MODULE=aiminit` → `aiminit` |
| `util` | `<MODULE>` | `MODULE=aimver` → `aimver` |

실제 산출물 이름은 `src/<zone>/<module>/Makefile`의 `TYPE` 변수 + 설치 경로에서 확인 가능:
- `$(OPENFRAME_HOME)/lib/lib<X>.so.64.*` (library)
- `$(OPENFRAME_HOME)/core/appbin/<X>` (server)
- `$(OPENFRAME_HOME)/bin/<X>` (tool)
- `$(OPENFRAME_HOME)/util/<X>` (util)

상세: `src/<zone>/AGENTS.override.md` (TYPE별 governance).

### MR Title = Squash 헤더 = commit 형식 (하나의 형식)

**MR title 은 Squash Commit Message 헤더와 동일한 형식으로 쓴다.** 둘 다 결국 git commit 제목이 되므로, `.gitmessage` + AGENTS.md 의 commit 형식 하나만 따른다. 콜론 위치는 IMS/Jira 번호 유무로 갈린다.

| 상황 | 형식 (MR title·Squash 헤더 공통) | 예 |
|------|------|-----|
| IMS 연결 | `IMS#<번호>:<type> 설명` — 콜론은 **번호와 type 사이** | `IMS#348560:<fix> structure size 변경으로 인한 연관 모듈 패치` |
| **IMS 없이 Jira만** | `OFV7-<번호>:<type> 설명` — 콜론은 **번호와 type 사이** | `OFV7-7297:<refactor> aimdcms usermain 메시지 처리 본문 추출` |
| 둘 다 미연결 | `<type>: 설명` — 콜론은 **type 뒤** | `<chore>: 커버리지 리포트 생성 엔진 소스 제외` |

- `<type>` 의 꺾쇠 `< >` 는 리터럴이다. type 명은 영어(`feat`/`fix`/`test`/`docs`/`refactor`/`style`/`chore`), 설명은 한글.
- **콜론 없는 `<type> 설명` 은 형식 위반**이다 (실제 MR !647 에서 리뷰어가 지적).
- docs-only governance MR 도 동일 — 면제 아님.

### 독자

- 리뷰어 (같은 팀 개발자) + QA + PM
- `## 내용` 섹션: 동작/기능 관점 (코드 상세는 `## 수정 사항`에)
- `## 수정 사항` 섹션: 파일 경로 + 변경 내용 (개발자 수준)

### API

```bash
# Mac curl (not dx)
curl -s --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{ "source_branch": "...", "target_branch": "rb_73", "title": "...", "description": "..." }' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests"
```

상세는 finishing-a-development-branch-aim SKILL.md를 참조할 것.

## docs-only governance MR

**조건**: product source(`.c`/`.h`/`.cpp`) 변경 및 unit test 영향이 전혀 없는 governance·문서·dev 도구 전용 MR (`git diff rb_73..HEAD --name-only` 결과가 `AGENTS.md` / `*/AGENTS.override.md` / `.gitmessage` / `.gitlab/*` / `script/*` / `test/**/AGENTS.override.md` 등만 포함, production 소스 없음). IMS/Jira 미연결인 경우가 많다.

**면제/대체 항목**:

- `## Test ### 추가/### 기존`: 체크박스를 `[x]`로 두고 `N/A — 코드/테스트 영향 없음 (governance·문서·도구 변경)` 명시 + 코드 블록에 `N/A: product source 변경 없음. gtest 추가/실행 대상 없음.` 1줄. `dx make gtest` 실행 불요.
- `<details>` 안 verbatim stdout: 면제. `N/A: 본 MR은 governance·문서·도구 변경뿐이라 dx make gtest 실행 대상이 아니다.` 1줄로 대체.
- `## Squash Commit Message`: 설치 산출물이 없으면 `* module` / `* version` 라인 생략 가능. IMS/Jira 미연결이면 `IMS#`·`#OFV7-` 를 생략하되, **헤더(및 MR title)는 `<type>: <한글 설명>` (콜론 포함)** 을 유지한다 — 콜론 없는 약식은 형식 위반이다 (상세: "MR Title = Squash 헤더 = commit 형식").
- `manual-check` marker (finishing-branch에서 삽입): IMS/Jira 둘 다 없으면 키 없이 `<!-- aim-harness:manual-check status=done checked=YYYY-MM-DD reason=governance-docs-only -->`. product source 미변경이라 매뉴얼 판단은 자명히 "불필요" → `status=done` 고정 (상세 형식은 `manual-guide.md` "Marker 형식").
- MR Check List: `coding convention 확인` / `테스트 추가` 등 코드 전제 항목은 `[x] — N/A(코드 변경 없음)` 부기. 5개 모두 체크해 리뷰 가능 상태 유지. 체크박스 표기 예: `- [x] 테스트가 추가 되었는가? — N/A(코드 변경 없음)` (한 줄에 부기).
- `## 내용` / `## 수정 사항`: generic 규칙대로 작성 (변경 파일 경로·이유·결과 요약).
- `> #OFV7-XXXX, #Deadline:` trailer: IMS/Jira 없으면 `> #Deadline: -` (마감 있으면 날짜만 기재).

**Self-review checklist 적용**: `<details>` verbatim/`BIN_DIR=` 시작 라인/`== Module Summary ==` N/A 행/`== Unmatched module aliases ==`/`* module` 산출물 이름 — 이 stdout·산출물 강제 항목들은 docs-only governance MR에서 **자동 N/A**로 간주한다. `[Check Fail]`이 아니라 N/A로 보고한다 (DONE_WITH_CONCERNS에 `[Check Fail]` 기재 불요).

## MR 코멘트

MR 코멘트 등록은 **code-reviewer-aim** 스킬 (Phase F)이 담당한다.

### 직접 코멘트 작성 시 규칙

- **톤**: 격식체
- **구조**: 문제 → 이유 → 수정 제안
- **코드 블록**: 허용 (개발자 대상)
- **심각도 표시**: Critical/Major/Minor 구분

### API

actionable 리뷰 지적(라인별)은 `/discussions`(resolvable thread)로 등록한다. MR 본문 일반 코멘트나 diff 범위 밖 지적은 `/notes`(resolve 불가)로 등록한다.

```bash
# 일반 노트 (MR 본문, resolve 불가)
curl -s --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"body": "코멘트 내용"}' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<IID>/notes"
```

#### 인라인 코멘트 (라인별, resolvable)

diff 범위 내 라인에만 가능하다. 다음 두 가지를 반드시 지킨다.

**1. Content-Type 필수**: `position`은 nested dict이므로 `Content-Type: application/json` + JSON body로 보낸다. form-urlencoded는 nested dict가 flatten되지 않아 `400 position[base_sha] is missing` 류로 실패한다.

**2. 라인 키 선택 (`new_line` vs `old_line`)** — diff 라인 종류에 따라 다르다:

| diff 라인 종류 | position 키 |
|---|---|
| 추가된 라인 (`+`) | `new_line`만 |
| 삭제된 라인 (`-`) | `old_line`만 — `new_line`을 쓰면 `400 Bad - line code must be valid` |
| context 라인 (변경 없음) | `new_line` + `old_line` 둘 다 |

삭제 라인(본 PR이 제거한 코드: fallback 제거 등)에 `new_line`을 쓰는 게 대표 실수다 — 코드가 변경 후 파일에 없어 가리킬 수 없다. diff 범위 밖 라인은 inline 불가 → `/notes`로 fallback하고 본문에 `파일:라인`을 명시한다.

`diff_refs`(`base_sha`/`head_sha`/`start_sha`)는 `GET .../merge_requests/<IID>` 응답에서 확보한다.

```bash
# 인라인 (라인별, JSON 필수). 삭제 라인이면 new_line 대신 old_line.
curl -s --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "body": "**[🔴 High]** 문제: ...",
    "position": {
      "base_sha": "<diff_refs.base_sha>",
      "head_sha": "<diff_refs.head_sha>",
      "start_sha": "<diff_refs.start_sha>",
      "position_type": "text",
      "new_path": "src/lib/ap/ap.c",
      "new_line": 84
    }
  }' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<IID>/discussions"
```

> thread resolve는 작성자/maintainer만 가능하다(MR 작성자도 리뷰어가 연 thread는 resolve 불가, 답글만 가능). 등록 라우팅 상세는 code-reviewer-aim Phase F.

## 참고 MR (작성 예시)

- !578: 대규모 기능 추가 (상세 예시)
- !556: 간단 버그 수정 (최소 예시)
- !583: 판정 로직 수정 + 리팩토링 (중간 규모)

## Self-review checklist (적신호)

MR description 작성/갱신 PUT **직전** 아래 항목을 확인한다. 위반 시 재작성 후 재PUT. (docs-only governance MR은 `## docs-only governance MR` 섹션의 면제 항목을 먼저 적용 — stdout·산출물 강제 항목은 N/A로 처리, `[Check Fail]` 아님.)

- [ ] `## Test ### 추가`가 `### 기존`보다 위에 있는가?
- [ ] `<details>` 안이 요약본이 아닌 `dx make gtest` stdout **verbatim 전체**인가? (`BIN_DIR=` 시작 라인 존재)
- [ ] stdout 4개 섹션 모두 존재 — `== GoogleTest Summary ==` / `== Module Summary ==` / `== Unmatched module aliases ==`(출력 시) / `== Global Coverage (ALL) ==` *(자동: `grep -c '^==' <description.md>`)*
- [ ] `== Module Summary ==`의 `N/A` 행을 삭제하지 않았는가?
- [ ] `== Unmatched module aliases ==` 섹션이 stdout에 출력됐는데 빠지지 않았는가?
- [ ] `BIN_DIR=` 등 경로 헤더 라인 존재 (stdout 맨 윗부분을 자르지 않음)
- [ ] Squash commit `* module`이 산출물 이름(`lib<MODULE>` / `<MODULE>`)인가? (상기 Module 이름 형식 규칙 참조)
- [ ] Squash commit 복수 모듈인 경우 `* module` / `* version` 블록이 분리되어 있는가? (한 줄 쉼표 나열 금지)
- [ ] **`* module` 목록이 완전한가** — 바이너리가 바뀌는 산출물을 **전부** 담았는가? 공개 헤더를 고쳤다면 소비 모듈까지 체크섬으로 확인했는가? (상기 Module 결정 규칙 참조)
- [ ] **`* version` 이 bump 후 값인가** — `7.3.0()` 공란이나 bump 전 값이 남아 있지 않은가? bump 커밋을 넣었다면 Squash 메시지도 갱신했는가?
- [ ] MR description 본문에 **작성 시점 이후 바뀐 사실**(bump 생략 판단, 계획, 버전 등)이 낡은 채 남아 있지 않은가? — 여러 섹션에 같은 사실이 나오면 교차 확인
- [ ] **MR title 과 Squash commit 헤더가 같은 commit 형식**인가? — IMS/Jira 연결 시 `IMS#<번호>:<type> 설명`, 미연결 시 `<type>: 설명`. 콜론 없는 `<type> 설명` 을 쓰지 않았는가? (docs-only MR 도 동일 — 면제 아님)
- [ ] MR Check List 5개 모두 체크됐는가? (리뷰 가능 조건)

**위반 항목이 있으면**:
1. 재작성 후 재PUT, 또는
2. 부득이한 경우 DONE_WITH_CONCERNS에 `[Check Fail] <항목>: <상황>` 기재

체크리스트 자체의 누락·오류(여기 없는데 사용자가 지적한 패턴)는 `[Skill Gap] writing-documents-aim/gitlab-guide: <내용>`으로 별도 보고.
