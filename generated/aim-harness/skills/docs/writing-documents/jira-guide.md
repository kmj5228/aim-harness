# Jira 작성 가이드

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
- 다이어그램은 **이미지로 첨부**: mermaid.live에서 렌더링 → PNG 다운로드 → Jira 첨부
- description에서 참조: `!filename.png|thumbnail!`

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
- **분량 초과 시**: 방대한 내용은 Confluence 페이지에 작성하고, Jira에서 링크

## Jira API 접근

**Jira는 REST API로 접근한다. Chrome 브라우저 자동화를 사용하지 않는다.** (IMS만 Chrome 사용)

```bash
# Mac curl (not dx) — Jira API
curl -s -u "$(JIRA_EMAIL):$(JIRA_TOKEN)" \
  "https://tmaxsoft.atlassian.net/rest/api/2/issue/OFV7-XXXX"
```

- 인증: Basic Auth (email + API Token)
- 인증 정보: `agent/info/access.md` 참조
- Base URL: `https://tmaxsoft.atlassian.net`
- Mac에서 직접 실행 (dx 경유 불필요)

### 주요 API

| 용도 | 메서드 | 경로 |
|------|--------|------|
| 이슈 조회 | GET | `/rest/api/2/issue/OFV7-XXXX` |
| description 수정 | PUT | `/rest/api/2/issue/OFV7-XXXX` + `{"fields":{"description":"..."}}` |
| 댓글 추가 | POST | `/rest/api/2/issue/OFV7-XXXX/comment` + `{"body":"..."}` |
| 파일 첨부 | POST | `/rest/api/2/issue/OFV7-XXXX/attachments` + `-F "file=@path"` + `-H "X-Atlassian-Token: no-check"` |

## 댓글 작성

- 인사 없이 본문부터 시작
- 격식체
- 특정 사용자 호출 시 `@멘션` 사용
- 상태 변경 시 사유를 댓글로 함께 작성

## 상태/핸들러 변경

- 상태 변경 사유를 댓글에 기록
- 핸들러 변경 시 `@멘션`으로 호출 + 인수인계 내용 포함
