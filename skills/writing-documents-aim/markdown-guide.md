# Markdown 작성 가이드

## 공통 규칙

### 두괄식

- 모든 섹션은 **결론부터** 작성: 결론 → 근거 → 상세
- 배경 → 분석 → 결론 순서 금지
- 두괄식이 아닌 문단은 삭제하고 재작성

### 그림 우선 (다이어그램 + 데이터 차트)

그림은 두 종류로 나누며 역할이 다르다. 둘 다 PNG로 렌더해 첨부한다.

- **정성(관계·흐름·구조)** → mermaid (flowchart, sequence, ERD)
- **정량(분포·시계열·비교·상관)** → matplotlib (히스토그램, box plot, bar, 시계열)

규칙:

- 흐름/구조를 텍스트로 설명하기 전에 **mermaid로 먼저 그린다**.
- ASCII art / ASCII 차트 금지 — 렌더링 가능한 도구 사용.
- 큰 그림(아키텍처, 처리 흐름, 모듈 관계)은 **반드시 다이어그램**.
- 정량 데이터는 mermaid로 그릴 수 없다(xychart 한계). mermaid로 억지로 그리거나 표만으로 끝내지 말고 **matplotlib 차트**로 그린다.

#### 데이터 차트 종류 → 용도 매핑

| 목적 | 차트 | matplotlib |
|---|---|---|
| 분포(편향·꼬리) | 히스토그램(+백분위 수직선, 그룹별 stacked) | `ax.hist(arrs, stacked=True)` + `axvline` |
| 그룹별 산포·이상값 | box plot + 개별 점(strip) | `ax.boxplot(...)` + `ax.scatter(jitter)` |
| 구성 분해(A vs B 누적) | stacked bar | `ax.bar(a)` + `ax.bar(b, bottom=a)` |
| 두 지표 시계열 동시 | 이중축(막대 + 선) | `ax.bar` + `ax.twinx().plot` |
| 조건 비교(배율 큼) | grouped bar(log scale) | `ax.bar(x-w/2)`, `ax.bar(x+w/2)`, `set_yscale("log")` |

#### 통계 요소 권장

평균만 쓰지 않는다. 분포가 비대칭이면 **중앙값·표준편차·변동계수(CV)·왜도(skew)·백분위(p50/p95/p99)** 를 함께 제시한다. 간헐적 경합은 *중앙값/평균 괴리*로만 드러나는 경우가 많다(평균이 꼬리값에 끌려감). box plot에 개별 점을 얹으면 이상값 유무 오해도 방지된다.

#### gnuplot-style matplotlib 레시피

matplotlib의 풍부한 주석(값 라벨·배율·설명 박스)을 유지하면서 gnuplot의 클래식 룩을 입힌다. 3요소: ① 안쪽 틱 + 4면 박스, ② 점선 가로 그리드, ③ 얇은 선/작은 점.

```python
import matplotlib.pyplot as plt, matplotlib.font_manager as fm

# 한글 폰트: 환경에 설치된 폰트 중 첫 번째 사용 (특정 OS 폰트명 하드코딩 금지)
KF = next((f.name for c in ["Noto Sans CJK KR", "NanumGothic", "Malgun Gothic"]
           for f in fm.fontManager.ttflist if f.name == c), None)
plt.rcParams.update({
    "font.family": KF, "axes.unicode_minus": False, "font.size": 11,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "black", "axes.linewidth": 0.9,
    "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,   # 가로 그리드만
    "grid.color": "#9aa0a6", "grid.linestyle": ":", "grid.linewidth": 0.6,
    "xtick.direction": "in", "ytick.direction": "in",                  # 틱 안쪽
    "xtick.top": True, "ytick.right": True,                            # 4면 틱
    "xtick.major.size": 5, "ytick.major.size": 5,
    "xtick.major.width": 0.9, "ytick.major.width": 0.9,
    "legend.frameon": True, "legend.edgecolor": "black",
    "legend.fancybox": False, "legend.framealpha": 1.0,                # 각진 범례 박스
    "axes.titlesize": 13, "axes.titleweight": "bold",
})
EDGE = dict(edgecolor="black", linewidth=0.6)   # 막대 얇은 테두리: ax.bar(..., **EDGE)
# box plot 개별 점: ax.scatter(x, y, s=6, linewidths=0, alpha=0.75)
# 각진 설명 박스: bbox=dict(boxstyle="square,pad=0.5", fc="white", ec="black", lw=0.7)
```

- 이중축(twinx)에선 `ytick.right` 강제 대신 축별 `tick_params(direction="in")`를 개별 적용한다.
- 주석은 **데이터가 비어 있는 영역**에 배치한다. 고정 모서리(예: 0.02/0.95)에 두면 막대·선과 겹친다.

### 목차

- heading 5개 이상이면 **목차 필수**

### 가독성 핵심 원칙 (모든 markdown 문서 공통)

> 이 원칙은 모든 문서 플랫폼의 공통 기준(SSoT)이다. 플랫폼 가이드(confluence/jira 등)는 이 절을 참조하고 자기 플랫폼 특수 규칙만 추가한다.

1. **인라인 열거(`A + B + C`, `①②③`) 금지 — 항상 list로**
   2개 이상의 개념이 한 문장에 `+` 또는 `·/·/·`로 묶이면 분리한다. 4개 이상은 무조건 bullet list.

2. **한 단락 = 한 개념 (약 2~3문장 또는 ~250자 이내)**
   기계적 임계는 250자지만 본질은 *내부에 묻힌 개념 수*다. 4개 이상 개념이 한 단락에 섞이면 길이와 무관하게 쪼갠다.

3. **핵심 원칙·정의는 `>` blockquote로 분리**
   본문 문장 안에 핵심 주장이 묻히지 않도록 시각적으로 강조한다. Core principle / Iron Law / 정의 인용에 적용.

4. **구조적 데이터는 nested list 또는 표로**
   "5섹션 — A·B·C·D·E"처럼 구조가 있는 데이터를 평문으로 나열하지 않는다. nested list나 표로 구조를 시각화한다.

5. **빈 줄로 호흡 — 문단 사이, 리스트 항목 사이**
   markdown은 빈 줄이 곧 문단 경계다. 빈 줄 없이 이어진 텍스트는 벽처럼 느껴진다.

6. **형제 sub-section 사이에 hr(`---`) 삽입**
   같은 부모 아래의 형제 h3·h4 사이에 `---`를 넣어 시각 구분과 길이 호흡을 준다.

#### Before / After 예시

**패턴 1 — 인라인 열거 → list**

Before:
> 원인이 4층으로 분해됐다 — 메인 에이전트 누락 + 가이드 부재 + Step 0 약한 권고 + AGENTS.md 톤.

After:
> 원인은 4층으로 분해됐다:
>
> - 메인 에이전트 누락
> - 가이드 부재
> - Step 0 약한 권고
> - AGENTS.md 톤

**패턴 2 — 구조적 데이터 → nested list**

Before:
> 검증서를 5섹션으로 작성 — (Rnd) 변경 사유·변경 내용 / (Verification) 변경 이력·검증 항목·영향.

After:
> 패치 검증서 5섹션:
>
> - (Rnd) 변경 사유 · 변경 내용
> - (Verification) 변경 이력 · 검증 항목 · 영향

**패턴 3 — 핵심 원칙 → blockquote**

Before:
> 핵심 원칙은 "분석 먼저, 행동은 나중"이다. IMS 이슈를 받으면 곧바로 고치지 않고...

After:
> > **핵심 원칙: 분석 먼저, 행동은 나중.**
>
> IMS 이슈를 받으면 곧바로 고치지 않고...

#### 검증 방법

- **라인 길이 필터**: 250자 초과 라인을 후보로 추출(요약/표 행/blockquote 인용문은 제외).
- **인라인 열거 필터**: 한 라인에 ` + ` 또는 `·` 구분이 3개 이상 등장하는 패턴을 후보로 검출.
- **형제 hr 누락 점검**: 같은 부모 아래 sibling h3/h4 사이에 `---`가 없는 곳 점검.
- **Cold-read**: 기계 필터 후 전체 cold-read로 한 단락에 4개 이상 개념이 묻혔는지 최종 확인.

### 톤

- **내부 기술 문서** (analysis, design, plan): 간결체 ("~한다", "~이다") 허용
- **공유/보고 문서** (report, 회의록): 격식체 권장

### 산출물 경로

- 모든 산출물: `../agent/prompt/<topic>/`
- prefix로 출처 구분:

| prefix | 스킬 |
|--------|------|
| `analysis_` | issue-analysis-aim |
| `design_` | brainstorming-aim |
| `plan_` | writing-plans-aim |
| `exec_` | executing-plans-aim |
| `debug_` | systematic-debugging-aim |
| `verify_` | verification-before-completion-aim |
| `finish_` | finishing-a-development-branch-aim |
| `review_` | code-reviewer-aim |
| `patch_` | completing-patch-aim |

---

## 문서 유형별 구조

### 분석 보고서 (analysis_report.md)

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

### 설계 문서 (design_spec.md)

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

### 실행 계획 (plan_tasks.md)

```markdown
# [Feature] Implementation Plan

> **For agentic workers:** Use executing-plans-aim to implement.

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
