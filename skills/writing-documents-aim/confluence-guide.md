# Confluence 작성 가이드

## 독자

- **주 독자**: 개발자 (같은 팀 + 다른 팀)
- 코드 포함 허용 (핵심만)
- 분량 제한 없음. 단, **길면 목차 필수**

## 페이지 구조

### 기술 설계/사양/개발 문서 (주력)

```
# 제목

작성자: @이름
이력:
- YYYY-MM-DD: 내용 추가/수정 사항

---

## 목차
(heading이 많으면 Confluence 자동 목차 매크로 사용)

## 1. 개요 (Abstract)
- 본 문서의 목적 한 문단
- 개발 범위 bullet list
- 관련 문서 링크 (스펙, IMS, Jira)

## 2. 전체 Overview
- 아키텍처 figure / 흐름도
- 전체 동작 요약

## 3~N. 모듈별 상세
(영향 모듈별로 섹션 분리)

각 모듈 섹션 내 구성:
- 기능 설명
- 핵심 코드 (pseudo-code, 함수 시그니처, 구조체)
- 표 (상태, 설정값, 매핑 등)
- 그외 고려한 방안 (채택하지 않은 대안 + 이유)

## N+1. DB (해당 시)
- 테이블 정의 (CREATE TABLE)
- 인덱스 설계
- 주요 SQL

## N+2. ERROR CODE (해당 시)
- Error Code 표: 코드명 | 코드값 | 설명

## N+3. TEST
- Target Function → Test Code 매핑 표

## N+4. 관련 Jira
- Jira issue filter 매크로 또는 표

## 관련 문서
- 스펙, 분석 문서, IMS 링크
```

### 프로토콜/인터페이스 문서

```
# 제목

## 개요
본 문서의 대상 프로토콜 한 문단.

## Protocol 전체 구조
- 구조 figure
- 전체 포맷 요약 (크기, 필드 관계)

## 각 구조체/메시지 상세
- C 구조체 정의
- 필드별 설명 표

## 관련 문서
```

### 회의록

```
# [날짜] 회의 제목

- 일시: YYYY-MM-DD HH:MM
- 참석자: @이름1, @이름2
- 주제: 한 줄 요약

## 논의 사항
1. 항목별 번호 매기기
   - 논의 내용
   - 결정 사항 (있으면)

## Action Items
| 담당자 | 항목 | 기한 |
|--------|------|------|

## 다음 회의
- 일시 / 주제 (있으면)
```

## 작성 규칙

### 목차

- heading 5개 이상이면 **목차 필수** (Confluence 목차 매크로 또는 numbered heading)
- heading은 번호 매기기: `1. 개요`, `2. Overview`, `3. DCMS`, ...

### 이력

- 페이지 상단에 작성자 + 수정 이력 기록
- 형식: `YYYY-MM-DD: 변경 내용 요약`

### 코드

- **핵심 코드만** 포함: pseudo-code, 함수 시그니처, 구조체, SQL
- 전체 함수를 복사하지 않음
- Confluence 코드 매크로 사용 (언어 지정)

### Figure / 다이어그램

- 아키텍처, 흐름도는 **mermaid** (flowchart, sequence diagram 등) 또는 draw.io로 작성
- ASCII art 금지 — 렌더링 가능한 도구 사용
- figure에 캡션/번호 부여: `[figure1. overview]`
- **글보다 그림 우선:** 흐름/구조를 텍스트로 설명하기 전에 다이어그램으로 표현할 수 있는지 먼저 검토

### 대안 검토

- 채택하지 않은 방안도 **"그외 고려한 방안"** 섹션에 기록
- 왜 채택하지 않았는지 이유 포함
- 이후 동일 질문에 대한 답변이 됨

### 관련 문서 연결

- 스펙 문서, 분석 문서, IMS, Jira를 **링크로 연결**
- Jira는 가능하면 Jira issue filter 매크로 사용

### 두괄식

- 모든 섹션은 **결론부터** 작성: 결론 → 근거 → 상세
- 배경 → 분석 → 결론 순서 금지
- 두괄식이 아닌 문단은 삭제하고 재작성

### 톤

- 기술 문서: 간결체 ("~한다", "~이다") 허용
- 격식체도 가능 — 일관성만 유지
- **인사: "안녕하십니까"** (댓글 등)

## Confluence REST API 접근

**Confluence는 REST API로 접근한다. Chrome 브라우저 자동화를 사용하지 않는다.**

```bash
# Mac curl (not dx) — Confluence API
curl -s -u "$(JIRA_EMAIL):$(JIRA_TOKEN)" \
  "https://tmaxsoft.atlassian.net/wiki/rest/api/content/PAGE_ID"
```

- 인증: Basic Auth (Jira와 동일한 email + API Token)
- 인증 정보: `../agent/info/access.md` 참조
- Base URL: `https://tmaxsoft.atlassian.net/wiki`
- Mac에서 직접 실행 (dx 경유 불필요)
- 개인 스페이스 key: `~62afbb6842d926a01e50ae29`

### 주요 API

| 용도 | 메서드 | 경로 |
|------|--------|------|
| 현재 사용자 조회 | GET | `/rest/api/user/current` |
| 스페이스 목록 | GET | `/rest/api/space?type=personal&limit=50` |
| 페이지 조회 | GET | `/rest/api/content/PAGE_ID` |
| 페이지 생성 | POST | `/rest/api/content` + `{"type":"page","title":"...","space":{"key":"..."},"body":{"storage":{"value":"...","representation":"storage"}}}` |
| 페이지 수정 | PUT | `/rest/api/content/PAGE_ID` + body에 version.number 증가 필수 |
| 파일 첨부 | POST | `/rest/api/content/PAGE_ID/child/attachment` + `-F "file=@path"` + `-H "X-Atlassian-Token: nocheck"` |
| 접근 제한 설정 | PUT | `/rest/api/content/PAGE_ID/restriction` + read/update restrictions JSON 배열 |

### 본문 포맷 (Confluence Storage Format)

Confluence API는 **Storage Format (XHTML 기반)**을 사용한다. markdown이 아니다.

| 용도 | Storage Format |
|------|----------------|
| heading | `<h2>제목</h2>` |
| bold | `<strong>bold</strong>` |
| bullet list | `<ul><li>item</li></ul>` |
| table | `<table><tbody><tr><th>header</th></tr><tr><td>cell</td></tr></tbody></table>` |
| code block | `<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">c</ac:parameter><ac:plain-text-body><![CDATA[code]]></ac:plain-text-body></ac:structured-macro>` |
| 이미지 (첨부) | `<ac:image ac:width="800"><ri:attachment ri:filename="file.png"/></ac:image>` |
| 목차 매크로 | `<ac:structured-macro ac:name="toc"><ac:parameter ac:name="printable">true</ac:parameter></ac:structured-macro>` |
| info 패널 | `<ac:structured-macro ac:name="info"><ac:rich-text-body><p>내용</p></ac:rich-text-body></ac:structured-macro>` |

### 다이어그램 이미지 변환

Confluence는 mermaid를 기본 지원하지 않는다. 이미지로 변환 후 첨부한다.

```bash
# Mac에서 실행 (not dx)
npx -y @mermaid-js/mermaid-cli@10 -i diagram.mmd -o diagram.png -b white -s 4
```

- 배경색: 흰색 (`-b white`)
- 해상도: `-s 4` (4x scale, 3000px+ 출력) — 기본값은 저해상도이므로 반드시 지정
- 변환 후 첨부 API로 업로드 → Storage Format `<ac:image>`로 참조
