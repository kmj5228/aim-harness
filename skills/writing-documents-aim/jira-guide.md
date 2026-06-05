# Jira 작성 가이드

> 가독성 공통 규칙(인라인 열거 분리, 한 단락 한 개념, blockquote 강조, 구조적 데이터→표/list, 빈 줄 호흡)은 `markdown-guide.md`의 "가독성 핵심 원칙"을 참조한다. 아래는 Jira 특수 규칙만 다룬다.

## Description 작성

### 구조

```
h1. Problem
* 문제 상황 기술

h1. Goal
* 달성 목표

h1. Analysis
* 분석 결과 (원인, 영향 범위)

h1. Design
* 설계 방향, 접근 방식

h1. Development
* 개발 내역, 변경 사항

h1. Test
* 테스트 결과, 검증 항목

h1. Document
* 관련 문서 링크

h1. Reference
* IMS, Confluence, 기타 참조
```

### Jira Wiki Markup (API 작성 시 필수)

Jira API v2는 markdown이 아니라 **wiki markup**을 사용한다. markdown 문법을 그대로 보내면 렌더링이 깨진다.

| 용도 | markdown (사용 금지) | Jira wiki markup (사용) |
|------|---------------------|----------------------|
| heading 1 | `# Problem` | `h1. Problem` |
| heading 2 | `## Design` | `h2. Design` |
| bold | `**bold**` | `*bold*` |
| bullet list | `- item` | `* item` |
| numbered list | `1. item` | `# item` |
| table header | `\|header\|` | `\|\|header\|\|` |
| table cell | `\|cell\|` | `\|cell\|` |
| image (첨부) | `![alt](url)` | `!filename.png\|thumbnail!` |
| code block | ` ```code``` ` | `{code}code{code}` |
| link | `[text](url)` | `[text\|url]` |

### 다이어그램

- Jira는 mermaid를 **기본 지원하지 않음**
- 다이어그램은 **이미지로 변환 후 첨부**:
  ```bash
  # Mac에서 실행 (not dx)
  npx -y @mermaid-js/mermaid-cli@10 -i diagram.mmd -o diagram.png -b black -s 4
  ```
- 배경색: 검은색 (`-b black`)
- 해상도: `-s 4` (4x scale, 3000px+ 출력) — 기본값은 저해상도이므로 반드시 지정
- 변환 후 첨부 API로 업로드 → description에서 참조: `!filename.png|thumbnail!`
- **정량 데이터(분포·시계열·비교)** 도 같은 방식으로 PNG 첨부한다. 차트는 mermaid가 아닌 matplotlib로 렌더한다(차트 종류·gnuplot-style 레시피는 `markdown-guide.md` "그림 우선" 참조).

### 기 작성 내용 규칙

- **Problem, Goal은 보통 이미 작성되어 있음** — 기존 내용을 존중
- 내용 **추가**는 필요 시 가능
- 기존 내용 **삭제/수정**은 반드시 사용자 확인 후 진행
- 빈 섹션(Analysis, Design 등)을 채워나가는 방식으로 작업

### 규칙

- **독자**: 개발자
- **추상화**: 핵심 코드 삽입까지 허용 (함수명, 코드 블록 OK)
- **톤**: description은 간결체/명사형 허용, 댓글은 격식체
- **설계/개발 깊이**: 큰 그림(접근 방식, 영향 모듈, 변경 방향) 필수 작성. 흐름도는 이미지 첨부로 포함. 필요 시 세부 내용까지 기술
- **분량 초과 시**: Jira description은 32,767자 하드 한계 — 아래 "Description 분량 한계 — Confluence 이관" 참조

### Description 분량 한계 — Confluence 이관

Jira description은 **32,767자 하드 한계**가 있다 (초과 PUT은 HTTP 400). 한계에 근접/초과하면 분리한다:

| 구분 | 대상 |
|------|------|
| Jira 잔류 | `h1. Problem` + `h1. Goal` (티켓 본질) + `h1. 상세 문서` (Confluence 링크) |
| Confluence 이관 | `h1. Analysis` 이하 전체 (Design/Development/Test/Document/Reference + 보존본) |

> **Problem/Goal은 "이관"이 아니라 "복제"한다.** Confluence 페이지에는 Problem/Goal을 *맥락으로 복제*(개요/Abstract 두괄식 요건 충족)하고 Analysis 이하를 *이관 본체*로 둔다. Jira에는 Problem/Goal이 잔류한다. "이관(Jira에서 빼기)"과 "복제(Confluence에 맥락 추가)"는 다른 동작이므로 양쪽 존재는 모순이 아니다.

**Confluence 위치**: AIM IMS 문서는 "AIM IMS" 페이지(space `OFV7`, pageId `6783134`) 하위에 생성한다. 제목은 `[IMS#<번호>] <요약>`.

**절차**: ① `POST /wiki/rest/api/content` (`ancestors`에 `6783134`)로 페이지 생성 ② Jira wiki → storage 변환은 `POST /wiki/rest/api/contentbody/convert/storage` (`representation: wiki`) — 변환기가 `{X}`/`[X]`를 매크로·링크로 오해석하므로 **매크로 토큰·링크 보호**가 필요(상세는 `confluence-guide.md` "wiki → storage 이관 노하우") ③ Confluence 페이지 게시·검증 **후에만** Jira description을 Problem/Goal + 링크로 PUT 축소(양쪽 동시 손상 방지).

**이관은 복사가 아니라 보강·정정**: 부실한 Design/Development는 산출물로 보강하고, 1차 commit 기준 stale 내용은 최종 구현으로 갱신("설계 당시 X → 구현 중 Y 확정" drift bullet로 경위 명시), 검토 과정의 대안(AoS vs SoA 등)은 보존한다.

## Jira API 접근

**Jira는 REST API로 접근한다. Chrome 브라우저 자동화를 사용하지 않는다.** (IMS만 Chrome 사용)

```bash
# Mac curl (not dx) — Jira API
curl -s -u "$(JIRA_EMAIL):$(JIRA_TOKEN)" \
  "https://tmaxsoft.atlassian.net/rest/api/2/issue/OFV7-XXXX"
```

- 인증: Basic Auth (email + API Token)
- 인증 정보: `../agent/info/access.md` 참조
- Base URL: `https://tmaxsoft.atlassian.net`
- Mac에서 직접 실행 (dx 경유 불필요)

### 주요 API

| 용도 | 메서드 | 경로 |
|------|--------|------|
| 이슈 조회 | GET | `/rest/api/2/issue/OFV7-XXXX` |
| description 수정 | PUT | `/rest/api/2/issue/OFV7-XXXX` + `{"fields":{"description":"..."}}` |
| 댓글 추가 | POST | `/rest/api/2/issue/OFV7-XXXX/comment` + `{"body":"..."}` |
| 파일 첨부 | POST | `/rest/api/2/issue/OFV7-XXXX/attachments` + `-F "file=@path"` + `-H "X-Atlassian-Token: no-check"` |

### API 버전 선택: v2 + wiki markup (권장)

Jira REST API는 v2와 v3가 공존한다. **v2 + wiki markup** 조합을 사용한다.

| 측면 | v2 + wiki markup (권장) | v3 + ADF |
|------|-----------------------|---------|
| body 포맷 | 문자열 (wiki markup 그대로) | ADF JSON (구조화된 tree) |
| 작성 난이도 | 낮음 (string 그대로 전송) | 높음 (ADF node 타입마다 JSON 구조 다름) |
| 표/heading | `h3.` / `\|\|헤더\|\|` 문자열 | `{"type": "heading", ...}` 중첩 |
| 디버깅 | 문자열 비교 용이 | 구조 비교 어려움 |

v3는 Atlassian이 새 포맷으로 밀지만 실무 비용이 커서 v2 우선. markdown 혼용 금지(위 wiki markup 표 참조).

### POST 실용 패턴 (댓글 등록 예)

JSON body는 **파일로 분리**하여 기호 이스케이프 문제를 피한다. HTTP status 확인을 위해 `-w` 옵션 사용.

```bash
# 1) Body 파일 생성 (wiki markup 본문)
cat > /tmp/jira_comment.json <<'EOF'
{"body": "h3. 제목\n\n||헤더1||헤더2||\n|값1|값2|\n\n*강조*"}
EOF

# 2) POST (Mac curl, not dx)
curl -s -w "\nHTTP_STATUS:%{http_code}\n" \
    -u "$JIRA_EMAIL:$JIRA_TOKEN" \
    -X POST -H 'Content-Type: application/json' \
    -d @/tmp/jira_comment.json \
    'https://tmaxsoft.atlassian.net/rest/api/2/issue/OFV7-XXXX/comment'
# → 201 Created + comment ID JSON
```

**검증**:
- `HTTP_STATUS:201` 확인 (404/403이면 권한/키 확인, 400이면 body 구조 확인)
- 리턴 JSON의 `id` / `self` 필드로 생성된 댓글 URL 확인
- 실패 시 body 파일을 그대로 남겨두고 재시도

**인증 정보**: `/Users/mjkang/company/dev_sshfs/agent/info/access.md` (API Token은 하드코딩 금지 — 환경변수 또는 access.md 참조 인라인).

## 댓글 작성

- 인사 없이 본문부터 시작
- 격식체
- 특정 사용자 호출 시 `@멘션` 사용
- 상태 변경 시 사유를 댓글로 함께 작성

## 상태/핸들러 변경

- 상태 변경 사유를 댓글에 기록
- 핸들러 변경 시 `@멘션`으로 호출 + 인수인계 내용 포함

## Self-review checklist (적신호)

description PUT / 댓글 등록 직전 다음을 점검한다. 하나라도 위반 시 PUT 보류 → 수정 → 재점검.

### 형식 (Wiki markup)

- [ ] markdown 잔존 없음: `#`/`**`/`-`/`1.`/`` ``` ``의 모든 markdown이 `h1.`/`*`/`*`/`#`/`{code}`로 변환됐는지 (v2는 wiki markup, markdown 그대로면 렌더 깨짐)
- [ ] 표 헤더는 `||header||` (`|header|`는 헤더 행 아님)
- [ ] 링크는 `[text|url]` (`[text](url)` 금지)
- [ ] mention은 `[~accountid:<id>]` (Cloud v2). `[~user]`·plain `@name`은 알림 안 감

### 내용

- [ ] description PUT 시 기 작성 Problem/Goal 보존됨 (임의 수정 시 사용자 confirm 필수)
- [ ] description 32,767자 한계 미초과 (초과 시 Confluence 이관 + Jira엔 링크만 잔류)
- [ ] 다이어그램은 mermaid 원본이 아니라 이미지 변환본 (`-b black -s 4` 고해상도 PNG, `!filename.png|thumbnail!` 참조)
- [ ] API 토큰 하드코딩 없음 (환경변수/`access.md` 참조 — memory `feedback_api_token_env_var`)

### 댓글 (description과 다른 규칙)

- [ ] 인사말 없이 본문부터 시작
- [ ] 격식체 (`~합니다`/`~드립니다`)
- [ ] 특정 사용자 호출 시 `[~accountid:<id>]` 멘션 포함

### 상태/핸들러 변경

- [ ] 상태 변경 사유를 댓글에 함께 기록
- [ ] 핸들러 변경 시 인수인계 내용 + mention 포함

### POST/PUT 검증

- [ ] HTTP_STATUS 201/200 확인 (`-w '\nHTTP_STATUS:%{http_code}\n'`)
- [ ] 리턴 JSON `id`/`self`로 생성된 댓글·페이지 URL 재확인
