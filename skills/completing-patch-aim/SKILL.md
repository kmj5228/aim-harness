---
name: completing-patch-aim
description: Use when MR is merged and you need to write the IMS patch verification document (패치 검증서) for QA review
---

# Completing Patch

## Overview

After MR merge, write the patch verification document in IMS for QA review.

**Core principle:** QA가 읽는 문서다. 동작 관점으로 작성하고, 코드 레벨 설명은 금지한다.

<HARD-GATE>
상수명, 함수명, 코드 레벨 설명을 사용하지 않는다. 모든 내용을 동작/기능 관점에서 기술한다.
</HARD-GATE>

## When to Use

- GitLab MR이 merge된 후
- IMS 이슈에 패치 검증서를 작성해야 할 때

## Checklist

1. **정보 수집** — MR 변경 사항, 커밋 내역, 테스트 결과 확인
2. **초안 작성** — 5개 섹션을 텍스트 파일로 작성
3. **사용자 검토** — 초안 확인 후 승인
4. **HTML 변환** — X-Free Editor 호환 HTML로 변환
5. **IMS 등록** — 브라우저 자동화로 IMS 에디터에 반영

## 5개 섹션

### Rnd 섹션 (첫 번째 iframe)

#### 1. Reason for change (required)
왜 변경했는지. 기능/버그 수정 배경.

- 한 줄 요약 + bullet list로 주요 동기
- IMS 이슈 내용 기반

#### 2. Change content (optional)
무엇을 변경했는지. 기능 단위로 나열.

- 번호 매기기 (1. xxx, 2. xxx)
- 각 기능 하위에 bullet list로 세부 사항
- **동작 관점:** "메시지 자동 재전송 기능 추가" (O) / "`aim_rcv_insert()` 함수 추가" (X)

### Verification 섹션 (두 번째 iframe)

#### 3. Defining Change History (required)
어떤 모듈이 어떻게 변경됐는지 표로 정리.

- 테이블: 모듈 | 변경 유형(신규/수정) | 설명
- 이어서 **기능 변화점** — 번호 매기기, 각 기능의 동작 변화를 기술

#### 4. Verification Items (required)
QA가 검증해야 할 항목.

- 카테고리별로 나누어 bullet list
- 활성화/비활성화 조건 분리
- Known Bug은 별도 강조 블록으로 표기
- **구체적 동작 시나리오:** "X 설정 시 Y 동작 확인" 형식

#### 5. Impact Analysis / Regression Items
기존 기능에 미치는 영향.

- 변경이 기존 동작에 영향 없음을 항목별로 기술
- 성능 영향이 있으면 최적화 방안과 함께 기술


## Cross-Reference

공통 문서 작성 규칙(독자별 추상화, 톤, 두괄식)은 **writing-documents-aim** SKILL.md를 참조한다. 아래는 패치 검증서 고유 규칙만 기술한다.

## 작성 규칙

### 동작 관점 작성 (QA 문서)

| 금지 | 허용 |
|------|------|
| `aim_rcv_insert()` 함수 추가 | recovery 메시지 DB 저장 기능 추가 |
| `AIM_ERR_INVALID_PARAM` 반환 | 잘못된 입력 시 에러 반환 |
| `dcms_recovery_mark_retry()` 호출 | 전송 실패 시 재시도 상태로 전이 |
| `static` 함수를 헤더로 승격 | (검증서에 불필요한 내용) |
| `g_recovery_cache` 전역 변수 | 설정 캐시로 반복 로드 제거 |

### Best Practice 참조

작성 전 반드시 아래 파일을 Read하여 톤/구조/상세도를 참고:
- **Rnd 섹션:** `../agent/prompt/msgrcv_sum#2.html`
- **Verification 섹션:** `../agent/prompt/msgrcv_verification#5.html`

## HTML 변환 규칙 (X-Free Editor v5)

### 필수 헤더
```html
<html><head><style title="__xfree_default">
    html { cursor: text; }
    p { margin-top: 0pt; margin-bottom: 0pt; line-height: 1.2; white-space: pre-wrap;}
    ol, li, ul { margin-top: 3pt; margin-bottom: 3pt; }
    td { }
    blockquote { margin-top: 0pt; margin-bottom: 0pt }
    body { word-break: break-all; font-size: 10pt;}
</style></head><body style="font-family: 굴림; font-size: 9pt;">
```

### 안전한 태그
- `<b>`, `<i>`, `<span style="...">`, `<br>`, `<p>`, `<ul>`, `<li>`
- `<table border="1" cellpadding="4" cellspacing="0" style="border-collapse: collapse; font-size: 9pt;">`
- `<tr style="background-color: #f0f0f0;">` (헤더 행)
- `<td>`, `<td><b>헤더</b></td>` (th 대체)

### 사용 금지
- `<h1>` ~ `<h6>` → `<b><span style="font-size: 10pt;">제목</span></b>` 사용
- `<th>` → `<td><b>헤더</b></td>` 사용
- CSS class → inline style로 대체
- CSS pseudo-selector (`nth-child`, `hover`) → 제거

### Known Bug 강조
```html
<div style="background-color: #fff3cd; border-left: 3px solid #ffc107; padding: 6px 10px; margin: 6px 0; font-size: 9pt;">
<b>[Known Bug] 제목</b><br>설명
</div>
```

## 산출물

텍스트 초안: `../agent/prompt/<topic>/patch_verification.txt`
HTML (Rnd): `../agent/prompt/<topic>/patch_rnd.html`
HTML (Verification): `../agent/prompt/<topic>/patch_verification.html`

## IMS 등록 워크플로우

### 1. 패치 검증서 페이지 열기

IMS 메인 페이지에서 JS 실행 (Chrome 자동화):
```javascript
popupPatchVerification('<IMS_NUMBER>')
```
직접 URL 접근 불가 — 반드시 JS 함수로 열어야 함.

### 2. iframe 식별

- Rnd 섹션: 첫 번째 iframe (`xfeDesignFrame_{randomNum1}`)
- Verification 섹션: 두 번째 iframe (`xfeDesignFrame_{randomNum2}`)
- iframe ID는 페이지 로드마다 변경됨

### 3. HTML 주입

```javascript
// Rnd 섹션 — iframe DOM 직접 수정
var rndFrame = document.querySelectorAll('iframe[id^="xfeDesignFrame_"]')[0];
rndFrame.contentDocument.body.innerHTML = '<Rnd HTML 내용>';

// Verification 섹션 — 에디터 인스턴스 사용
xfeArry[0].xfeContentsHandler.setHtmlValue('<Verification HTML 내용>');
```

### 4. 저장

```javascript
// confirm 팝업 자동 승인 후 저장
var origConfirm = window.confirm;
window.confirm = function() { return true; };
doRndSave();
window.confirm = origConfirm;
```

저장 후 페이지 새로고침 → iframe ID 변경됨.

## Red Flags

- 상수명/함수명/코드 레벨 설명 사용
- best practice 파일 읽지 않고 작성
- HTML에 `<h2>`, `<th>`, CSS class 사용
- 사용자 검토 없이 IMS 등록
- `savePatch()` 호출 (이것은 Patch Registration용 — `doRndSave()` 사용)

## Integration

**Called by:**
- **finishing-a-development-branch-aim** 이후 (MR merge 후)

**Requires:**
- IMS 로그인 상태 (비밀번호 입력은 사용자가 직접)
- Chrome 브라우저 자동화 도구 (`mcp__claude-in-chrome__*`)
