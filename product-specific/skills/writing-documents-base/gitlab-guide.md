# GitLab 작성 가이드

## MR Description

MR description은 **finishing-a-development-branch-base** 스킬이 담당한다.

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

**적신호:**
- `<details>` 안이 `ALL(src)` 한 줄만 있거나, BINARY 표 없이 요약만 있음 → **요약본을 붙여넣은 것**. stdout 원문으로 교체
- `N/A` 행을 제거하여 "실제 실행된 모듈만" 남긴 경우 → 복원
- `Unmatched module aliases` 섹션이 출력됐는데 빠진 경우 → 추가
- `BIN_DIR=` 같은 경로 헤더가 없음 → stdout 맨 윗부분을 자른 것. 다시 전체 복사

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

### MR Title

- 형식: `<type> Korean description` (콜론 없음)
- 예: `<fix> ACS 호환 프로시저 ASSIGN 해석 skip 로직 수정`

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

상세는 finishing-a-development-branch-base SKILL.md를 참조할 것.

## MR 코멘트

MR 코멘트 등록은 **code-reviewer-base** 스킬 (Phase F)이 담당한다.

### 직접 코멘트 작성 시 규칙

- **톤**: 격식체
- **구조**: 문제 → 이유 → 수정 제안
- **코드 블록**: 허용 (개발자 대상)
- **심각도 표시**: Critical/Major/Minor 구분

### API

```bash
# 일반 노트
curl -s --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"body": "코멘트 내용"}' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<IID>/notes"
```

## 참고 MR (작성 예시)

- !578: 대규모 기능 추가 (상세 예시)
- !556: 간단 버그 수정 (최소 예시)
- !583: 판정 로직 수정 + 리팩토링 (중간 규모)
