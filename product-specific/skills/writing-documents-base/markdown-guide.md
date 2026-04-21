# Markdown 작성 가이드

## 공통 규칙

### 두괄식

- 모든 섹션은 **결론부터** 작성: 결론 → 근거 → 상세
- 배경 → 분석 → 결론 순서 금지
- 두괄식이 아닌 문단은 삭제하고 재작성

### 다이어그램 우선

- 흐름/구조를 텍스트로 설명하기 전에 **mermaid로 먼저 그린다**
- ASCII art 금지 — mermaid flowchart, sequence diagram 등 렌더링 가능한 도구 사용
- 큰 그림(아키텍처, 처리 흐름, 모듈 관계)은 **반드시 다이어그램**

### 목차

- heading 5개 이상이면 **목차 필수**

### 톤

- **내부 기술 문서** (analysis, design, plan): 간결체 ("~한다", "~이다") 허용
- **공유/보고 문서** (report, 회의록): 격식체 권장

### 산출물 계약

- 문서는 현재 topic의 artifact workspace에 저장한다.
- core/base skill은 physical path를 직접 가정하지 않는다.
- 현재 runtime이 특정 경로를 제공할 수는 있지만, 그것은 runtime mapping이며 문서 규칙 자체는 아니다.
- logical artifact와 canonical filename은 아래처럼 본다:

| logical artifact | canonical filename | typical producer |
|------------------|--------------------|------------------|
| `analysis_report` | `analysis_report.md` | issue-analysis-base |
| `design_spec` | `design_spec.md` | brainstorming-base |
| `implementation_plan` | `plan_tasks.md` | writing-plans-base |

- 아래 prefix는 문서군을 구분하는 관습으로만 본다:

| prefix | 스킬 |
|--------|------|
| `analysis_` | issue-analysis-base |
| `design_` | brainstorming-base |
| `plan_` | writing-plans-base |
| `exec_` | executing-plans-base |
| `debug_` | systematic-debugging-base |
| `verify_` | verification-before-completion-base |
| `finish_` | finishing-a-development-branch-base |
| `review_` | code-reviewer-base |
| `patch_` | completing-patch-base |

## 문서 유형별 구조

### 분석 보고서 (`analysis_report`)

```markdown
# Issue Analysis: <topic>

## Issue Info
- IMS / Jira / Reporter / Handler

## Verdict: <Bug | Expected Behavior | Configuration Error | Unsupported Feature>
(두괄식: 결론 먼저)

## Symptom
정확한 증상, 환경, 재현 조건

## Root Cause Analysis
코드 추적, 로직 분석. 핵심 코드 블록 포함.

## Spec Reference
XSP 스펙 참조 결과 (해당 시)

## Rationale
판정 근거

## Recommended Action
구체적 다음 단계
```

**독자:** 같은 팀 개발자. 코드 수준 상세 허용.

### 설계 문서 (`design_spec`)

Confluence 기술 설계 문서와 동일 구조 사용:

```markdown
# Design Spec: <topic>

## 목차

## 1. 개요
- 목적 한 문단 + 개발 범위 + 관련 문서 링크

## 2. 전체 Overview
- 아키텍처/흐름도 (mermaid 필수)
- 전체 동작 요약

## 3~N. 모듈별 상세
각 모듈:
- 기능 설명 (결론부터)
- 핵심 코드 (pseudo-code, 함수 시그니처, 구조체)
- 매핑 표
- 그외 고려한 방안 (채택하지 않은 대안 + 이유)

## N+1. DB (해당 시)
- 테이블 정의 + 인덱스 + SQL

## N+2. ERROR CODE (해당 시)

## N+3. TEST
- Target Function → Test Code 매핑 표

## 관련 문서
```

**독자:** 같은 팀 개발자. 코드 블록, 구조체, 테이블 허용.
**분량:** 제한 없음. 길면 목차 필수.

### 실행 계획 (`implementation_plan`)

```markdown
# [Feature] Implementation Plan

> **For agentic workers:** Use executing-plans-base to implement.

**Goal:** [한 문장]
**Architecture:** [2-3 문장]
**Affected Modules:** [모듈 목록]

---

### Task N: [Component Name]
**Files:** Create/Modify/Test 목록
- [ ] Step 1: ...
- [ ] Step 2: ...
```

**독자:** 에이전트 또는 개발자. 정확한 파일 경로, 코드 포함 필수.

### 일반 보고서/메모

```markdown
# 제목

## 결론 (두괄식)
핵심 결과/판단 한 문단

## 상세
번호 매기기 또는 섹션별 구분. 다이어그램 포함.

## 다음 단계
```

**독자:** 문서 목적에 따라 결정.

---

## 코드 블록

- 내부 기술 문서: 코드 블록 허용 (핵심만)
- 공유 문서: 독자에 따라 판단 (SKILL.md 독자별 추상화 표 참조)
