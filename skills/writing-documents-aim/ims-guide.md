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
- **한 문장 내 줄바꿈 금지**: 한 문장은 한 줄로 작성한다. 폭 압축 목적의 강제 줄바꿈은 가독성/복사/검색을 떨어뜨린다. 줄바꿈은 문장 종결 또는 단락 구분에만 사용.
- **기술 용어 단계적 약어**: 본문에서 도구/저장소/식별자가 첫 등장하는 시점에 `<도구명>의 <기능 표현>(<코드 레벨 식별자>)` 형식으로 정식 표기한 뒤, 같은 답변 내 이후 등장 시 축약형만 사용한다. 독자가 식별자를 한 번 인지한 상태에서 본문 길이를 줄여 가독성을 높인다.
  - 예시: 첫 등장 `aimmsgmgr의 저장 DB(OFM_AIM_DCMS_RECOVERY)` → 이후 `DB`
  - 예시: 첫 등장 `메시지 복구 스케줄러(dcms_rcv_scheduler)` → 이후 `스케줄러`
  - 예시: 첫 등장 `aimdcms의 메시지 큐(OFM_AIM_QUEUE)` → 이후 `큐`

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
- **표**: `<table>` 사용 가능. 단 `<th>`·CSS class는 에디터 sanitize로 제거될 수 있어 **`<td>`+`<b>` 헤더 + `border` 속성/inline style만** 사용. `fileUpload()` 저장 후에도 보존됨 (검증: IMS#354989 — 3열 사양 대조표)

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

### 에디터 DOM 자동화 (programmatic 입력)

JS로 직접 폼·에디터를 조작할 때의 구조 (검증: IMS#354989):

- **폼 열기**: "Action Registration" 셀의 `onclick="setDisplayAction()"`을 호출하면 액션 등록 폼과 X-Free 디자인 프레임이 생성된다. (호출 전에는 `xcontents`가 `display:none`)
- **본문 입력 대상**: 편집 표면은 contenteditable iframe `xfeDesignFrame_<id>`(동일 출처, `<id>` 동적), 데이터 홀더는 숨김 textarea `xcontents`(`actionRegMenu` 내부). 디자인 프레임 `body.innerHTML`에 HTML을 set한다.
- **저장 동기화**: `fileUpload()`가 프레임 HTML을 `xcontents`로 sync 후 제출한다. 안전하게 입력 직후 `xcontents.value = frame.body.innerHTML`로 명시 동기화해도 된다.
- **핸들러 select**: `moduleManagers`. 옵션 value 형식 = 역할접두어+계정 (예: `Qyujeong_ko`=고유정[QA], `Rminjae_kang`=강민재[R&D], `A...`=Reporter). 변경 시 value set + `change` 이벤트 dispatch.
- **alert 비차단**: `fileUpload()`는 confirm("Would you like to save?")과 저장 후 alert을 띄울 수 있다. **alert은 확장 세션을 블록**하므로, confirm은 `true` 반환·alert은 캡처(무동작)로 오버라이드한 뒤 호출하고, 결과는 **다음 단계에서 페이지 리로드/액션 로그 조회로 검증**한다(저장 성공 시 이슈 페이지가 리로드되어 컨텍스트가 초기화됨).

```javascript
// 입력만 (저장은 사용자 "저장해" 후 별도 턴)
setDisplayAction();
var fr = document.querySelector('iframe[id^="xfeDesignFrame_"]');
var d = fr.contentDocument || fr.contentWindow.document;
d.body.innerHTML = html;                              // <br>/<table>(td+b) 포함
document.getElementById('xcontents').value = d.body.innerHTML;
// 핸들러 변경 시에만:
// var s = document.getElementById('moduleManagers');
// s.value = 'Qyujeong_ko'; s.dispatchEvent(new Event('change', {bubbles:true}));
```

### 등록 워크플로우

```
1. IMS 이슈 페이지 접근
2. setDisplayAction() 호출 ("Action Registration" 셀 onclick) → 폼 + xfeDesignFrame 생성
3. (변경 시에만) moduleManagers 드롭다운 value set + change 이벤트
4. xfeDesignFrame body.innerHTML + xcontents에 HTML 입력 (<br> 줄바꿈, 표는 td+b)
5. ★ 사용자에게 입력 내용 확인 요청 ★ (저장 전 멈춤)
6. 사용자 승인 후 → fileUpload() + confirm 우회 + alert 캡처로 저장 → 리로드/로그로 검증
```

### 핸들러 변경

- 액션 등록 시 **핸들러 변경 가능**. 변경할 때만 "Handler" 드롭다운에서 다른 인원 선택.
- **핸들러 변경 안 함 = 드롭다운을 건드리지 않음.** 미선택 상태로 두면 현재 핸들러로 자동 유지된다.
- **자동화 시 동일하게 적용**: 변경 안 하려면 `moduleManagers.value = ...` 호출 자체를 하지 않는다. 변경할 때만 다른 사람의 value로 set.
- 동일 핸들러를 명시 set하면 폼이 alert `"The selected handler is the same as the current handler. Please select another one."`로 저장을 거부한다. **이는 정상 동작이다** — "변경 의도 없음 = 미설정"이 원칙이므로 동일 핸들러를 다시 지정하는 케이스는 존재하지 않는다.
- 사고 사례=IMS#338191 매뉴얼 작성 액션(2026-05-31): 직전 액션이 이미 이명신으로 넘긴 상태에서 다시 이명신을 명시 set → 정상 거부. 변경 의도 없었으므로 set하지 말았어야 함.

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

패치 검증서 작성은 **completing-patch-aim** 스킬을 참조한다.

핵심 규칙 요약:
- **QA 관점**: 상수명/함수명/코드 레벨 설명 금지
- **5개 섹션**: Reason for change, Change content, Defining Change History, Verification Items, Impact Analysis
- **HTML**: X-Free Editor v5 호환 (h1~h6 금지, th 금지, CSS class 금지, inline style만)
- **Best practice**: `../agent/prompt/DONE/msgrcv/msgrcv_sum#2.html`, `../agent/prompt/DONE/msgrcv/msgrcv_verification#5.html`
- **등록**: `popupPatchVerification('<issueId>')` → iframe DOM 수정 → `doRndSave()` + confirm 우회

상세는 completing-patch-aim SKILL.md 전체를 참조할 것.

### 검증서 팝업 자동화 (Chrome MCP)

패치 검증서 팝업은 `popupPatchVerification('<issueId>')`이 `window.open`으로 여는데, **features 인자가 있으면 별도 창으로 떠 MCP 탭 그룹이 포착하지 못한다**(`tabs_context_mcp`에 안 잡힘). `window.open`을 후킹해 features를 제거하면 같은 창의 새 탭으로 열려 MCP가 제어할 수 있다 (검증: IMS#348560).

```javascript
// 메인 이슈 탭에서 실행 → 팝업이 MCP 탭으로 열림
if (!window.__origOpen) window.__origOpen = window.open;
window.open = function(u, n, f){ return window.__origOpen.call(window, u, n || 'patchverif'); };
popupPatchVerification('<issueId>');   // 이후 tabs_context_mcp로 새 탭 확인
```

**두 X-Free 에디터 구조** (Rnd / Verification):
- 편집 프레임: `xfeDesignFrame_<id>` (Rnd = "Reason for change" 포함, Verification = "Defining Change History" 포함). id suffix는 동적.
- 데이터 홀더 textarea: `rndDesc`(Rnd), `veriRndDesc1`(Verification). **body 안쪽 innerHTML만** 저장(head/style 없음).
- 주입 시 designFrame `body.innerHTML`과 데이터 홀더 **둘 다** set. 한글 등 큰 HTML은 base64로 넘겨 `TextDecoder('utf-8')`로 복원(직접 문자열은 이스케이프·차단 이슈).
- **긴 예제/카드 이미지**: body의 `word-break: break-all`이 상속되어 monospace 정렬이 꺾인다. `<pre style="font-family:monospace; white-space:pre; word-break:normal;">`로 감싸고, **저장 후 재조회로 `<pre>` 생존 확인**.
- 저장은 `doRndSave()`(패치 검증서) — 액션 등록의 `fileUpload()`와 다름. **동사 분리·턴 분리 규칙(위 액션 섹션)을 동일 적용**: "작성/입력"은 주입까지만, "저장"에서만 `doRndSave()` 호출.

## IMS 접근

- URL 패턴: `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId={번호}`
- Chrome 브라우저 자동화로 접근
- 로그인 필수 (비밀번호는 사용자가 직접 입력)
