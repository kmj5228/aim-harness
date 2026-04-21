# IMS 작성 가이드

## IMS 액션 (Action) 작성

### 구조

```
안녕하십니까.
{소속} {이름}입니다.

{목적/배경 한 문단}

{본문 — 번호 매기기 또는 bullet}

감사합니다.
```

### 독자별 유형

| 유형 | 독자 | 톤 | 내용 수준 |
|------|------|-----|----------|
| 분석 결과 공유 | QA + 개발자 | 격식체 | 동작 관점 + 모듈 수준 |
| 일정 공유 | PM + QA | 격식체 | 기능/일정만 |
| 기술 의견 전달 | 개발자 | 격식체 | 모듈/기능 수준 허용 |
| 고객 답변 (Expected behavior) | QA → 고객 | 격식체 | 동작 관점만, 코드 용어 금지 |
| 고객 가이드 (Configuration error) | QA → 고객 | 격식체 | 설정값 + 절차만 |

### 규칙

- **격식체 필수**: "~합니다", "~드립니다", "~부탁드립니다"
- **인사**: **"안녕하십니까"** (통일)
- **소속**: "{팀명} {이름}입니다"
- **마무리**: "감사합니다"
- **코드 레벨 금지** (QA/고객 대상): 파일명, 함수명, 상수명 사용하지 않음
- **첨부**: 첨부 파일이 있으면 본문에 파일명과 설명 기술

### 예시 패턴 (일정 공유)

```
안녕하십니까.
MMS OB개발팀 강민재입니다.

본건 Action No.XXXXXXX의 개발 요건으로 XX일 개발 완료 예상합니다.
패치 등록은 우선순위에 따라 등록 예정입니다.

감사합니다.
```

### 예시 패턴 (분석 결과 — 두괄식)

```
안녕하십니까.
MMS OB개발팀 강민재입니다.

본건 분석 결과, {결론/원인 한 문장}으로 확인되었습니다.

1. 원인
   - {모듈 수준 원인 기술}

2. 현상
   - {동작 관점 증상 기술}

3. 조치 계획
   - {개발 범위 + 일정}

감사합니다.
```

## IMS 액션 등록 (Chrome 자동화)

### 에디터 HTML 규칙

액션 에디터도 X-Free Editor를 사용한다. **`<p>` 태그가 줄바꿈으로 렌더링되지 않는다.**

- **줄바꿈**: `<br>` 사용
- **문단 구분**: `<div>내용</div>` + `<br>` 또는 `<br><br>`
- `<p>` 태그 사용 금지 — 에디터에서 줄바꿈 없이 이어 붙여짐

```html
<!-- Bad: 줄바꿈 안 됨 -->
<p>안녕하십니까.</p>
<p>MMS OB개발팀 강민재입니다.</p>

<!-- Good: 정상 줄바꿈 -->
안녕하십니까.<br>
MMS OB개발팀 강민재입니다.<br>
<br>
본건 분석 결과를 공유드립니다.<br>
```

### 등록 워크플로우

```
1. IMS 이슈 페이지 접근
2. "Action Registration" 링크 클릭 → 액션 등록 폼 열림
3. (필요 시) 핸들러 드롭다운에서 대상 선택
4. 에디터에 HTML 입력 (<br>로 줄바꿈)
5. ★ 사용자에게 입력 내용 확인 요청 ★
6. 사용자 승인 후 → fileUpload() + confirm 우회로 저장
```

### 핸들러 변경

- 액션 등록 시 **핸들러를 동시에 변경** 가능
- 액션 등록 폼의 "Handler" 드롭다운에서 선택
- 사용자가 핸들러를 지정하면 드롭다운에서 해당 인원 선택 후 액션 등록

### 저장 (confirm 우회)

저장 함수는 `fileUpload()` — 패치 검증서의 `doRndSave()`와 **다름**.

```javascript
var origConfirm = window.confirm;
window.confirm = function() { return true; };
fileUpload();
window.confirm = origConfirm;
```

### 저장 트리거 규칙 (HARD-GATE보다 강력)

**동사 분리:**
- "작성해", "써줘", "입력해" → 에디터에 입력만. **fileUpload() 호출 금지.**
- "저장해", "save", "submit" → fileUpload() 호출 허용.

**턴 분리:** fileUpload()는 **내용 입력과 같은 턴에서 호출 금지.** 반드시 사용자 메시지를 거친 후에만 호출.

```
Turn 1: 에디터에 HTML 입력 → "입력 완료. 확인해 주십시오." (여기서 멈춤)
Turn 2: 사용자: "저장해" / "save" / "submit"
Turn 3: fileUpload() + confirm 우회
```

**"작성해줘"를 듣고 저장까지 수행하면 규칙 위반이다.** "작성" ≠ "저장".

---

## IMS 패치 검증서

패치 검증서 작성은 **completing-patch** 스킬을 참조한다.

핵심 규칙 요약:
- **QA 관점**: 상수명/함수명/코드 레벨 설명 금지
- **5개 섹션**: Reason for change, Change content, Defining Change History, Verification Items, Impact Analysis
- **HTML**: X-Free Editor v5 호환 (h1~h6 금지, th 금지, CSS class 금지, inline style만)
- **Best practice**: `agent/msgrcv_sum#2.html`, `agent/msgrcv_verification#5.html`
- **등록**: `popupPatchVerification()` → iframe DOM 수정 → `doRndSave()` + confirm 우회

상세는 completing-patch SKILL.md 전체를 참조할 것.

## IMS 접근

- URL 패턴: `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId={번호}`
- Chrome 브라우저 자동화로 접근
- 로그인 필수 (비밀번호는 사용자가 직접 입력)
