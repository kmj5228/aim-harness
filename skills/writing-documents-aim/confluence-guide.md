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

## 가독성 (공통 + Confluence 특수)

> **가독성 공통 규칙(인라인 열거 분리, 한 단락 한 개념, blockquote 강조, 구조적 데이터→표/list, 빈 줄 호흡, 형제 hr)은 `markdown-guide.md`의 "가독성 핵심 원칙"을 SSoT로 따른다.** 아래는 Confluence 게시 시에만 적용하는 플랫폼 특수 매크로다.

markdown을 그대로 storage로 변환하면 평문에 가까운 렌더가 나온다. 다음 매크로를 변환 후처리로 적용하면 가독성이 크게 향상된다.

### 가독성 강화 매크로

#### 1. TOC 매크로 — 자동 목차

수동 `## 목차 + ol` 대신 자동 클릭형 목차를 사용한다.

```xml
<ac:structured-macro ac:name="toc" ac:schema-version="1">
  <ac:parameter ac:name="maxLevel">3</ac:parameter>
  <ac:parameter ac:name="minLevel">2</ac:parameter>
</ac:structured-macro>
```

#### 2. Panel 매크로 — blockquote 분류 변환

`<blockquote>`는 시각 효과가 약하다. 내용 패턴으로 분류해 색상 panel로 변환한다.

| 본문 내 패턴 | 매크로 | 색 |
|---|---|---|
| 핵심 원칙 / Iron Law / 핵심 주장 / 정의 | `info` | 파랑 |
| 한 줄 요약 / 정리 / `즉 ...` | `note` | 노랑 |
| 참조 / 참고 / tip | `tip` | 초록 |
| ⚠️ / 안티패턴 / 절대 / 금지 / 주의 | `warning` | 주황 |
| 그 외 (일반 인용·예시) | `<blockquote>` 유지 | 회색 |

패턴 미매칭 blockquote는 그대로 둔다 — 모두 panel로 바꾸면 화려해져 *시각적 노이즈*가 된다.

#### 3. mermaid 블록 → PNG 변환

Confluence는 mermaid를 기본 지원하지 않는다. 이미지로 변환 후 첨부한다. 변환 명령은 아래 "다이어그램 이미지 변환" 절을 참조한다.

- 변환 후 첨부 API로 업로드 → 본문에서 `<ac:image><ri:attachment ri:filename="..." /></ac:image>`로 참조.

#### 4. attachments 매크로 — 파일 자동 노출

PDF/이미지 등 첨부를 페이지의 *발표 자료* 섹션에 자동 목록화한다.

```xml
<ac:structured-macro ac:name="attachments" ac:schema-version="1">
  <ac:parameter ac:name="upload">true</ac:parameter>
</ac:structured-macro>
```

### markdown → storage 변환 절차

1. **markdown → HTML** — markdown 라이브러리(표/fenced code/sane lists 확장 포함).
2. **코드 블록** → `<ac:structured-macro ac:name="code">` 매크로 (CDATA + `language` 파라미터).
3. **언어 prefix 처리** — markdown 라이브러리는 `language-X` 형식으로 출력하므로, regex로 prefix를 제거해 `language` 파라미터에 넣는다.
4. **블록 분류** — 본문 패턴 매칭으로 blockquote → panel 변환(위 표 참조).
5. **placeholder 마커** — 변환 전 markdown에 `<!--ATTACHMENT_MACRO-->` / `<!--TOC_MACRO-->` 같은 marker를 두고, 변환 후 매크로로 치환한다.

### 수동 편집 보존 — PUT 갱신 시 머지

게시 후 사용자가 페이지를 수동 편집했을 수 있다. 단순 PUT 덮어쓰기는 그 편집을 날린다.

**안전 흐름:**

1. 갱신 직전 현재 페이지를 fetch한다 (storage 포맷).
2. 로컬 백업(현재 body + meta)을 저장한다.
3. 새 body와 백업을 diff해 사용자 수동 편집 영역을 식별한다.
4. 전체 덮어쓰기 대신 *특정 섹션만* 교체한다.
5. PUT(version +1)으로 갱신한다.

### Confluence 게시 후 검증

생성 후 페이지를 열어 다음을 확인한다.

- TOC 매크로가 정상 렌더(목차 클릭 가능)
- Panel 색상이 의도대로(info=파랑 등)
- mermaid PNG가 깨지지 않음(해상도 확인)
- 형제 sub-section 사이 hr이 보임
- 첨부 파일 macro가 upload 버튼과 함께 노출

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
