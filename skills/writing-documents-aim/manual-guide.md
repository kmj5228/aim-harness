# Manual Guide (AIM 매뉴얼 작성)

> writing-documents-aim 서브가이드. AIM 제품 매뉴얼(Antora/AsciiDoc, 한글, 7.3) 작성 전용.

## Overview

- **대상 저장소**: `/Users/mjkang/company/MANUAL/openFrame_aim`
- **브랜치**: `7.3_main` (직접 commit + push, feature branch/MR 없음)
- **포맷**: Antora/AsciiDoc, 한글, `~한다` 체
- **트리거**:
  - **사용자 명시 요청**: "매뉴얼 작성해줘", "매뉴얼 작성 여부 알려줘", "매뉴얼 검토해줘" 등 매뉴얼 관련 요청 (특정 IMS/Jira/MR 전달 포함)
  - **개발 완료 자동 트리거** (구현 예정): MR 생성 또는 승인 시점에 aim-harness 워크플로우가 이 스킬을 호출
  - **어느 경로든 Step 1(필요성 판단)이 선행**. 바로 작성으로 진입 금지
- **5원칙** (memory `feedback_manual_writing_principles`): 정확성·일관성·명확성·완성도·검토

**매뉴얼은 고객/QA가 직접 보는 외부 문서**다. 추측성 기술은 제품 신뢰도 문제로 직결된다. 경험적 검증 없이 작성 금지.

## Iron Rule: 경험적 검증 (가장 중요)

### 1. "manual's exact text == verified text"

매뉴얼에 들어가는 **모든 실행 예시·출력 텍스트는 실제 실행 결과와 글자 단위로 일치**해야 한다. 예시를 가독성 목적으로 수정하면 **수정본을 다시 돌려서 재검증**한다.

```
작성 → 검증 → 편집 → 재검증 → 편집 → 재검증 → ...
```

편집 후 재검증을 건너뛰면 매뉴얼과 실제 출력이 괴리된다. 305201에서 실제 발생: `ap_tail.inc` + `EXCLUSIVE UNIT`으로 검증했는데 매뉴얼엔 `ap_common.inc` + 간결화본을 적음 → 사용자 지적으로 발견.

### 2. print_usage == 사용자 계약

CLI 툴 매뉴얼은 **`print_usage()`가 single source of truth**다. 내부 `process_args`/switch에 옵션이 있더라도 `print_usage`에 노출되지 않은 것은 **비공개 계약**이다.

- print_usage에 있음 + 내부 처리 있음 → 문서화
- print_usage에 있음 + 내부 처리 없음 → **사용자 질의** (버그 의심)
- print_usage에 없음 + 내부 처리 있음 → **문서화 금지**. 필요하면 사용자 질의

**사례**: jxdddms `print_usage()`는 `DCMS`를 ADL type 목록에 의도적으로 제외(주석 처리)했으나 내부 dump 테이블엔 DCMS 존재. 매뉴얼은 `print_usage` 기준으로 작성한다.

### 3. 후속 커밋 전수 확인

```bash
dx git log --all --grep=<IMS번호>
dx git log --all --grep=<OFV7-Jira번호>
```

**결과 전체를 본다**. 첫 커밋만 보고 매뉴얼 작성 금지. 347742의 경우 본기능 `948c42bd` 이후 `54abeb02`가 **출력 char-set을 박스 드로잉 → ASCII로 변경**. Jira description은 구버전 상태로 남아 있었다.

### 4. Jira description은 보조 자료

Jira description은 **구현자가 작성**한 것이고 최종 코드와 다를 수 있다. 코드가 최종 권위.

- Jira description의 샘플 출력 → **복붙 금지**. 실제 `dx make` + 실행으로 캡처
- Jira description의 옵션명/에러 메시지 → 코드로 재확인
- 구현자가 테스트 로그를 붙여뒀다면 참고 자료로만 사용

**Destructive 명령 예외**: `delete` 같은 파괴적 명령의 성공 메시지는 `fprintf(stdout, "[%s] delete success.\n", ...)` 에서 결정적이다. 실행 없이 **코드 기반 유추 허용**하되, "어느 파일 어느 라인에서 유추했는지" 주석으로 명시한다.

## 8-Step Workflow

### Step 1: 매뉴얼 필요성 판단 (GATE)

트리거 시점에 이 건이 실제로 매뉴얼 추가가 필요한지 먼저 판단한다. **이 단계를 건너뛰고 작성 단계로 진입 금지**.

**사전 체크 (필수)**: 판단 전에 **MANUAL repo에서 기존 작성 여부부터 확인**한다.

```bash
cd /Users/mjkang/company/MANUAL/openFrame_aim
git log --all --grep=<IMS번호> --oneline
git log --all --grep=<OFV7-num> --oneline
```

둘 중 하나라도 hit하면 **이미 반영된 케이스**. 트리거가 재진입일 수 있다.

**추가 필요 기준** (사용자 노출 변화가 있는 경우):
- CLI 툴의 사용법/옵션 신규·변경
- 유틸 바이너리의 사용법 변경
- ofconfig 키 신규·기본값 변경·범위 변경
- ADL 문법/디렉티브 신규
- 사용자 노출 에러 메시지 신규 또는 메시지 문구 변경
- 서버 구성/운영 절차 변경
- 기존 동작의 사용자 관찰 가능한 변화 (출력 포맷, 성공/실패 조건 등)

**추가 불필요 기준** (문서화 제외):
- 내부 리팩토링 (사용자 관찰 변화 없음)
- 버그 수정 중 사용자 동작이 "원래 의도"로 돌아간 경우
- 성능 개선 (출력/명령 변화 없음)
- 테스트 코드 변경
- 빌드 시스템 변경
- 내부 모듈 간 인터페이스 변경

**판단 결과 4가지**:
- **추가 필요** → Step 2~8 진행
- **추가 불필요** → 사용자에게 근거 보고 후 종료. 예: "이 MR은 내부 리팩토링으로 사용자 노출 변화가 없어 매뉴얼 추가 불필요"
- **이미 반영됨** → 사전 체크에서 MANUAL repo에 기존 commit 발견. 사용자에게 commit SHA + 반영 내용 요약 보고 후 **재작성/보완 필요 여부 질의**. 임의로 재작성 진입 금지. 사용자가 "보완 필요"라고 하면 Step 2~8 진행 시 기존 내용과의 delta만 추가
- **애매** → 사용자 질의. 판단 근거가 부족하면 "그대로 진행"이 아니라 **질의**

### Step 2: Jira 키 조회

IMS에 연결된 Jira 키(`OFV7-XXXX`)가 있으면 API로 description/댓글/테스트 로그 확인.

```bash
curl -u <user>:<token> "http://tmaxsoft.atlassian.net/rest/api/2/issue/OFV7-<num>"
```

**토큰 없음은 이유가 아니다**. access.md에서 찾아 사용한다.

### Step 3: aim repo 커밋 + MR 조회

두 가지 방법을 **모두** 사용한다. 한 쪽에만 의존 금지.

**방법 1: git log (IMS 번호 + Jira 키 둘 다 필수)**
```bash
dx git log --all --grep=<IMS번호> --oneline
dx git log --all --grep=<OFV7-num> --oneline
```

**두 grep을 모두 실행하고 합집합을 본다**. 한쪽만 돌리고 0건이면 포기 금지. aim repo commit 관례가 혼재되어 있다:
- IMS 번호만 기록: `IMS#347742, ...` (MANUAL repo 관례에 가까움)
- Jira 키만 기록: `fa468669 [#OFV7-1596] INC기능 지원` (305201 실제 사례)
- 둘 다 기록: `3cb581f2 IMS#310719:<feat> 7.1 to 7.3` + 본문에 Jira 키

한쪽 grep이 0건이어도 반대쪽에 본기능이 있을 수 있다. **본기능 커밋 + 후속 수정 커밋을 전수 확인**.

**방법 2: GitLab MR 조회**
```bash
# IMS/Jira 키로 MR 검색 (project 211 = aim)
curl -s --header "PRIVATE-TOKEN: <PAT>" \
  "http://192.168.51.106/api/v4/projects/211/merge_requests?search=<IMS번호>&state=merged"

# MR description 조회 (IID 확보 후)
curl -s --header "PRIVATE-TOKEN: <PAT>" \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<IID>"
```
MR description에는 commit보다 풍부한 정보가 있는 경우가 많다:
- 구현 의도 / 변경 범위 / 테스트 결과
- 스펙 결정 배경 (논의/리뷰 내역)
- 영향 범위 평가

**두 방법 병행**: git log에서 commit SHA → MR 브랜치/IID → MR description 조회. 반대로 MR에서 시작해 commit으로 역추적도 가능. PAT은 `../agent/info/access.md` 참조.

### Step 4: 커밋 상세 + 소스 확인

```bash
dx git show <commit>
```

변경 파일·모듈 버전·작업 범위 확인 후 실제 소스 열람:

- **CLI 툴**: `src/tool/<name>/<name>_main.c`의 `print_usage()` + `process_args()`
- **설정 키**: `config/openframe_aim.conf` + ofconfig 소비 코드
- **ADL 문법**: lex/yacc 파일 + 파서 호출부
- **서버 동작**: `src/server/<name>/...`

### Step 5: 경험적 검증 (`dx make` + 실행)

**이 단계는 선택 아니다**. 매뉴얼 작성 전에 실제 빌드 + 실행으로 출력을 캡처한다.

```bash
cd /Users/mjkang/company/dev_sshfs/aim
dx make                    # 또는 dx make <target>
dx bash -c "<실제 명령>"   # 실제 실행으로 출력 캡처
```

생략 가능 조건:
- Destructive 명령 (delete 등): 코드 기반 유추 허용. 단 주석 명시
- 사용자가 **명시적으로** 생략을 지시한 경우: "경험적 검증 생략해도 됨". 단 초안에 경고 블록 삽입

### Step 6: MANUAL repo 대상 파일 탐색 + 스타일 조사

```bash
cd /Users/mjkang/company/MANUAL/openFrame_aim
find docs -iname '*<keyword>*'
find docs/modules/<guide> -name 'sect-*.adoc' | head
```

**기존 파일 스타일을 먼저 본다**:
- 같은 guide 내 유사 파일을 `head -200`으로 훑기
- 헤더 레벨 (`==`, `===`, `=====`) 관례
- 표 cols 비율 (command 옵션 `16%,84%`, 출력 필드 `22%,78%`)
- 경고 블록 스타일 (`[NOTE] ==== ... ====`)
- 앵커 명명 (`sect_aim_<area>_<key>`)

### Step 7: 작성 (스타일 미러링)

- 유사 옵션은 유사 표 구조 (예: `delete -t` ← `load -t`, `dump` 표 ← `store` 표)
- 사용예제 관용 문구:
  - "다음은 … 하는 예이다." + 코드 블록
  - "다음은 명령을 수행한 결과이다." + 출력 블록
- 강한 경고는 `[NOTE] ==== ... ====` 어드모니션

### Step 8: 셀프 검토 + commit/push

**5원칙 체크리스트**:
1. 정확성: 코드/스펙/실행 결과와 일치?
2. 일관성: 기존 파일 스타일 미러링?
3. 명확성: 간결, 모호한 표현 없음?
4. 완성도: 배경·파라미터·예시·에러·제약 모두 포함?
5. 검토: 오타·문법·사실관계 재확인?

**<HARD-GATE>**: 초안을 사용자에게 보여주고 승인 받기 전에 push 금지. `7.3_main` 직접 push는 사실상 "발송"이다.

## 문서 배치 결정표

**"어디에 쓸지"와 "어디에 안 쓸지" 양쪽 명시한다**. 305201 사례에서 검증된 패턴.

| 변경 종류 | 대상 파일 | 쓰지 않는 기준 |
|----------|---------|---------------|
| CLI 툴 사용법/옵션 | `tool-reference-guide/pages/aim/sect-<tool>.adoc` | 툴 옵션 변화 없고 투명하게 동작하면 제외 |
| 유틸 바이너리 | `utility-reference-guide/pages/aim/sect-<util>.adoc` | 동일 |
| ofconfig 키 | `configuration-guide/pages/aim/sect-aim.adoc` | 기존 카테고리에 속하지 않으면 신규 `=== <CATEGORY>` 필요 |
| ADL 문법/디렉티브 | `resource-guide/pages/chapter-adl.adoc` | 디렉티브가 아니라 엔트리/구면 appendix-adl-reference로 |
| ADL 엔트리/구 지원표 | `resource-guide/pages/appendix-adl-reference.adoc` | **디렉티브(`-INC` 등)는 해당 없음** (305201 실제 판단) |
| 런타임 운영 명령 | `command-reference-guide/pages/chapter-<area>-commands.adoc` | ADL 문법/설정은 해당 없음 |
| 에러 코드/메시지 | `error-reference-guide/...` | 신규 코드 없으면 제외 |
| 서버 구성/운영 | `admin-guide/...` | 설치 절차 변화 없으면 제외 |

### 단일 파일 vs 다중 파일 판단

- **단일 파일**: 기능이 한 툴/한 파일에 집약됐을 때 (347742 jxdddms dump)
- **다중 파일**: 기능이 "설정 + 문법 + 동작"처럼 여러 계층에 걸칠 때 (305201 INC_PATH + `-INC` 디렉티브)

**다중 파일일 때 명시적 제외 판단**: 유사해 보이지만 성격이 다른 파일을 **왜 제외했는지** 초안 옆에 한 줄로 적는다. (예: `appendix-adl-reference는 엔트리/구 지원표 → 전처리 디렉티브는 해당 없음`)

## Antora/AsciiDoc Cheat Sheet

```asciidoc
== <주제>              // h2
=== <소주제>           // h3
===== 사용법            // 관례 레벨 (툴 문서에서 많이 씀)

[source,console]        // 코드 블록 (shell/console 출력)
....
$ jxdddms dump -d 00 -p /tmp/out.adl
....

[subs="specialcharacters,quotes"]    // 사용법 블록에서 __command__ 이탤릭 치환
[source]
----
jxdddms __command__ [options]
----

[cols="16%,84%"]        // command 옵션 표
|===
| 옵션 | 설명
| -d <id> | AIMDIR ID를 지정한다. 생략 시 `00`.
|===

[cols="22%,78%"]        // 출력 필드 표
|===
| 필드 | 설명
|===

[NOTE]                  // 경고/주의 어드모니션
====
`-t ALL`은 전체 삭제다. 복구 불가.
====

[[sect_aim_adl_inc_path]]   // 앵커
==== INC_PATH

xref:configuration-guide:aim/sect-aim.adoc#sect_aim_adl_inc_path[INC_PATH]
```

## Git 정책

```bash
cd /Users/mjkang/company/MANUAL/openFrame_aim
git checkout 7.3_main
git pull

# 작성 후
git add docs/modules/<guide>/pages/<file>.adoc   # 전체 add 금지
git status                                        # 의도한 파일만인지 확인
git commit -m "IMS#<num>, <한글 설명>"

# push (PAT은 access.md)
git push "http://oauth2:<PAT>@192.168.51.106/antora_ko/openframe_aim.git" 7.3_main
```

### 커밋 메시지 패턴

```
IMS#<num>, <한글 또는 영문 설명>
IMS#<num> <설명>                   # 콤마 없는 변형도 history에 존재
IMS#<num1>, IMS#<num2>, <설명>    # 여러 IMS 묶기도 함
```

**참고 커밋**:
- `d32f379 IMS#341217, aimctlcheck의 사용법 추가`
- `08bf993 IMS#347742, jxdddms의 dump 기능 및 delete 타입 옵션 사용법 추가`
- `700a15c IMS#305201, ADL -INC 디렉티브 및 INC_PATH 설정 사용법 추가`

## Scope 결정 (결함 수리)

매뉴얼 작성 중 기존 매뉴얼의 오류/불일치를 발견할 수 있다.

**Rule**: **결함 수리는 사용자 명시 지시가 있을 때만 scope-in**. 단 **발견 자체는 반드시 사용자에게 보고**한다. "그대로 둠"을 스킬이 임의로 결정 금지.

| 발견 종류 | 기본 처리 |
|----------|---------|
| IMS 범위 기능의 설명 오류 | scope-in (당연) |
| IMS 무관한 복붙 오타 (예: `load/delete -d` "등록할") | **발견 보고 + 사용자 질의**. 사용자 지시 있으면 scope-in, 없으면 scope-out (일관성 유지) |
| 섹션 순서 혼란 (alphabetical vs categorical) | 발견 보고 + 사용자 질의 |
| 유사 기능의 과거 누락 | 발견 보고 + 사용자 질의 |
| 문법/스타일 불일치 (cols 다름, 헤더 레벨 등) | 발견 보고 + 사용자 질의 |

**보고 형식**:
```
[Existing Defect] <파일>:<라인> — <결함 요약>
조치: [scope-in 제안 / scope-out 제안 / 판단 요청]
```

305201에서 사용자가 명시적으로 "ofconfig list는 알파벳 순으로 정렬"을 지시 → scope-in. 347742에서 `-d` 옵션 복붙 오타는 **발견 후 보고 누락** → 스킬 개정 대상. 발견 시 반드시 보고해야 사용자가 scope 판단 가능.

## Common Rationalizations (RED verbatim 차단)

| 변명 | 현실 |
|------|------|
| "매뉴얼 초안은 소스 정적 분석으로 충분" | 후속 커밋의 출력 변경을 놓친다. 347742 char-set 사례 — 본기능 후 3일 뒤 `54abeb02`가 출력을 바꿨다 |
| "내부 스위치에도 이 타입이 있으니 문서화해야" | `print_usage()`가 사용자에게 노출된 계약. 내부는 비공개. 괴리 발견 시 사용자 질의 |
| "Jira API 토큰이 없으니 생략" | `access.md`에 PAT이 있다. 토큰 찾기 = 정보 수집의 일부이지 생략 사유 아님 |
| "기존 파일 참고 금지라 제약 준수" (과잉 적용) | "해당 IMS 반영본 참고 금지"는 "유사 파일 스타일 조사 금지"가 아니다 |
| "빨리 하라니 조사 최소화" | 압박은 조사 생략 허가가 아니다. 빠른 쓰레기보다 느린 사실이 낫다 |
| "destructive라 실행 못 해서 창작" | `fprintf` 문자열은 코드에서 결정적. 코드 기반 유추는 OK, 단 "어느 파일 어느 라인" 주석 명시 |
| "예시를 가독성 목적으로 간결화했으니 OK" | 편집본은 **다시 돌린다**. 편집 후 재검증 안 하면 "manual's exact text == verified text" 위반 (305201 실제 발생) |
| "Jira description에 샘플 있으니 복붙" | Jira는 구현자 작성이고 구버전일 수 있다. 실제 빌드 + 실행 캡처 필수 |
| "첫 커밋만 보면 충분" | `git log --all --grep` 결과 **전체**를 본다. 후속 커밋이 출력/옵션을 바꿨을 수 있다 |
| "appendix는 모든 디렉티브 레퍼런스니까 추가" | appendix-adl-reference는 **엔트리/구 지원표**다. 전처리 디렉티브는 해당 없음 (305201 S2 RED 실제 오판 사례) |
| "초안은 스켈레톤이고 나중에 채우면 돼" | TODO 플레이스홀더로 남긴 초안은 초안이 아니라 "조사 회피". 사실 없이는 구조도 틀린다 |

## Red Flags — STOP

- `dx make <target>` 없이 초안 완성 → 실행 캡처 재수행
- `git log --all --grep=<IMS>` 결과 일부만 보고 작성 → 전체 조회
- `print_usage`에 없는 옵션을 문서화 중 → 사용자 질의
- Jira description 샘플을 복붙 → 실제 실행으로 대체
- 예시 편집 후 재검증 생략 → **동일 입력으로 다시 실행**
- "다른 파일 참고 금지"로 해석해서 스타일 미러링 생략 → 유사 파일 `head`로 조사
- 다중 파일 케이스에서 "쓸 파일"만 적고 "안 쓸 파일" 생략 → 제외 근거 추가
- `7.3_main`에 push 전에 사용자 승인 없이 진행 → HARD-GATE 위반. 승인 대기
- `appendix-adl-reference`에 엔트리/구가 아닌 것을 추가 → 배치 재검토
- 초안에 `TODO(...)` 블록이 남아 있음 → 조사 회피, 해당 정보 수집 재수행
- 기존 매뉴얼에서 결함(오타/복붙/스타일 불일치)을 발견했는데 **사용자에게 보고하지 않고** 그대로 둠 → 반드시 보고. scope 판단은 사용자 권한
- Step 1 (필요성 판단) 생략하고 바로 Step 2로 진입 → 모든 진입 경로에서 필요성 판단 선행

## Integration

**호출 패턴**:
- **사용자 명시 요청**: "매뉴얼 작성해줘", "매뉴얼 작성 여부 알려줘", "매뉴얼 검토해줘" 등. 특정 IMS/Jira/MR을 함께 전달하는 경우 포함
- **finishing-a-development-branch-aim Step 5 Option 1/2 직후** (자동): MR 생성·갱신 직후 Step 1 필요성 판단 자동 호출. 판단 결과를 MR description marker로 저장 (`<!-- aim-harness:manual-check status=pending-merge|done -->`).
- **completing-patch-aim Step 0/6** (자동, 상태 기반): MR merge 후 completing-patch 진입 시 marker 확인:
  - marker 없음 → Step 1부터 실행 (지금 판단)
  - `status=pending-merge` → Step 2~8 직행 (판단 건너뛰고 작성)
  - `status=done` → skip
- **writing-documents-aim 본체**: 독자 식별(고객/QA), 톤(격식체, `~한다` 체), HARD-GATE(push 전 승인), 동사 분리(작성 ≠ push)

**진입 시 기대 입력**:
- 사용자 요청 + 식별자 (IMS 번호, Jira 키, MR IID 중 하나 이상)
- 또는 MR 컨텍스트 (자동 트리거 시 MR description + diff)

### Marker 형식 (상태 기반 이중 진입)

MR description 맨 아래에 HTML 주석으로 삽입. finishing-branch가 쓰고, completing-patch가 읽는다.

```html
<!-- aim-harness:manual-check status=pending-merge checked=2026-04-15 -->
<!-- aim-harness:manual-check status=done checked=2026-04-15 reason=not-needed -->
```

| 필드 | 값 | 설명 |
|------|------|------|
| status | `pending-merge` | 매뉴얼 추가 필요 + merge 후 작성 (completing-patch Step 6에서 실행) |
| status | `done` | 이 MR에 대한 매뉴얼 판단 종료 (불필요/이미반영/지금작성완료/사용자skip) |
| checked | ISO date | 판단 수행일 |
| reason | 선택 | `done` 상태일 때 구체 사유 (`not-needed`, `already-reflected`, `written-now`, `user-skip`) |

**marker 없음**: 판단 자체 생략된 상태. completing-patch가 진입 시 지금 판단.

### Step 1 결과 → marker 매핑

| Step 1 결과 | 사용자 선택 | Marker |
|------------|----------|--------|
| 추가 필요 | A. 지금 작성 | `done reason=written-now` (작성 완료 후) |
| 추가 필요 | B. MR merge 후 | `pending-merge` |
| 추가 필요 | C. skip | `done reason=user-skip` |
| 추가 불필요 | — | `done reason=not-needed` |
| 이미 반영됨 | 재작성 안 함 | `done reason=already-reflected` |
| 이미 반영됨 | 보완 필요 | `pending-merge` |
| 애매 | 사용자 질의 후 | 수렴된 결과에 따라 |

**참고 메모리**:
- `reference_aim_manual_repo` — MANUAL 저장소 위치/버전/언어
- `feedback_manual_writing_principles` — 5원칙 (정확성·일관성·명확성·완성도·검토)

**관련 스킬**:
- writing-documents-aim (본체)
- finishing-a-development-branch-aim (Step 5 Option 1/2 직후 Step 1 자동 호출 + marker 작성)
- completing-patch-aim (Step 0 marker 확인 + Step 6 후속 작업)

## Sources (근거 사례)

이 가이드의 규칙은 다음 실전 사례를 **근거로** 작성됐다. 새 사례가 누적되면 이 목록에 append하고, 새 합리화/함정이 발견되면 Common Rationalizations 표에 verbatim으로 추가한다.

| 날짜 | IMS / Jira / MR | 종류 | 핵심 교훈 |
|------|---------------|------|----------|
| 2026-04 | IMS 347742 / OFV7-1641 | 단일파일 (tool-reference) | 후속 커밋(`54abeb02`)의 char-set 변경을 놓칠 뻔. 경험적 검증 + `git log --all --grep` 전수 확인의 근거. `print_usage`에서 DCMS 의도적 제외 — 사용자 계약 = print_usage |
| 2026-04 | IMS 305201 / OFV7-1596 | 다중파일 (configuration + resource) | "쓰지 않을 파일" 명시 판단의 근거. 가독성 편집 후 재검증 누락 → "manual's exact text == verified text" 불변식 |
| 2026-04-15 | 자가 진화 첫 실증 | meta | Skill Gap Reporting 메커니즘(using-aim-harness) 도입 직후, GREEN 검증 에이전트가 manual-guide 자체에서 2건 gap 자발 보고 → 반영: Step 1 "이미 반영됨" 4번째 분기 + 사전 체크, Step 3 IMS/Jira 이중 grep 합집합 규칙 |

**누적 반영 방법**:
1. 실전 케이스마다 위 표에 1줄 append
2. 새 verbatim 합리화는 Common Rationalizations 표에 추가
3. 새 Red Flag 패턴은 Red Flags 섹션에 추가
4. 기존 규칙이 실제와 불일치하면 즉시 수정 + Sources 표에 수정 근거 기록

## Known Gaps (미검증 시나리오)

현재까지 실전 검증이 안 된 영역. 해당 케이스 처리 시 사용자에게 "스킬 미검증 영역"임을 고지하고 진행.

- **`command-reference-guide` 런타임 명령 추가** — 미경험. 실제 `chapter-<area>-commands.adoc` 구조 조사 필요
- **`error-reference-guide` 에러 코드 추가** — 미경험. msgcode/errcode 생성 파이프라인과의 관계 확인 필요
- **`utility-reference-guide` 유틸 바이너리** — 미경험. `sect-<util>.adoc` 스타일이 tool-reference와 같은지 확인 필요
- **`admin-guide` 운영 절차 변경** — 미경험
- **여러 IMS를 한 commit/MR로 묶은 경우** — 347742/305201 모두 단일 IMS. 복수 IMS 동시 작성 시 커밋 메시지 패턴(`IMS#A, IMS#B, ...`) 외의 분기 규칙 미정의
- **후속 커밋이 여러 건(3+)인 경우** — 347742는 2건(본기능 + char-set), 3건 이상일 때 전수 검증 부담이 어떻게 되는지 미검증
- **MR 시점 자동 트리거 실구현** — 아직 워크플로우에 연결되지 않음. `finishing-a-development-branch-aim` 또는 별도 trigger point 설계 필요

이 목록에 해당하는 케이스를 만나면 스킬 개정 기회다. 사용자와 협의 후 Sources에 append.
