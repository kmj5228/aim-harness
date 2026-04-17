# Base Harness Migration

## Goal

`base-harness`를 `aim-harness` 복제본에서 여러 제품이 재사용 가능한 공통 하네스로 점진적으로 전환한다.

## Current State

- `base-harness`는 더 이상 단순 복제본 상태는 아니다.
- 메타 문서, 코어 스킬, 협업 스킬, 주요 support prompt의 1차 공통화가 완료됐다.
- 남은 잔재의 중심은 `product-specific/`로 분리한 product pack 번들, 일부 product-specific support 파일, 그리고 기록 문서다.

## Documentation Rule

마이그레이션 중 수행한 모든 작업은 이 문서에 순차 기록한다.

- 기준선 조사
- 용어 인벤토리
- 분류 판단
- 문서/스킬 수정
- rename 보류 또는 제거 보류 판단
- 검증 결과

## Strategy

### Baseline Files

현재 1차 마이그레이션 기준 파일:

- `AGENTS.md`
- `README.md`
- Claude runtime files (`CLAUDE.md`, `settings.json`, `hooks/session-start.sh`)
- `skills/*`

### Product-Specific Term Inventory

1차 스캔 대상:

- `README.md`
- Claude runtime files
- `skills/*/SKILL.md`

반복적으로 확인된 제품 종속 키워드:

- 제품/조직명: `aim-harness`, `AIM`
- 이슈/협업 도구: `IMS`, `Jira`, `GitLab`, `Confluence`, `NotebookLM`
- 실행 방식: `dx`, `dev_exec.sh`
- 브랜치 정책: `rb_73`
- 테스트/품질 기준: `GoogleTest`, `gcov`, diff coverage 80%
- 운영 절차: `manual-guide`, patch verification

### Initial Classification

#### Common Core Candidates

- `brainstorming-base`
- `writing-plans-base`
- `executing-plans-base`
- `test-driven-development-base`
- `systematic-debugging-base`
- `verification-before-completion-base`
- `writing-skills-base`

#### Collaboration Layer Candidates

- `subagent-driven-development-base`
- `dispatching-parallel-agents-base`
- `using-feature-branches-base`
- `requesting-code-review-base`
- `receiving-code-review-base`
- `code-reviewer-base`
- `finishing-a-development-branch-base`

#### Product-Specific Product Pack Candidates

- `issue-analysis-base`
- `completing-patch-base`
- `writing-documents-base`

#### Meta

- `using-base-harness`

메타 스킬은 `using-aim-harness`에서 `using-base-harness`로 rename했다. hook과 문서 참조도 함께 전환했다.

### File-Level Findings

#### `README.md`

- 거의 전면이 `aim-harness` 소개문이었다.
- 공통화용 소개, 현재 상태, 스킬 분류, 추출 전략으로 재작성했다.

#### Claude runtime files

- `CLAUDE.md`는 라우팅 표 일부는 재사용 가능했지만 설명이 AIM 운영 절차에 강하게 묶여 있었다.
- `hooks/session-start.sh`는 주석과 메시지가 모두 `aim-harness` 기준이었다.
- `settings.json`은 구조 자체보다 hook 경로 정책이 핵심 검토 대상이었다.

### Ordered Execution

1. 메타 문서 공통화
2. hook 메시지 공통화
3. 코어 스킬 6~7개 공통화
4. 협업 스킬 공통화
5. AIM 전용 스킬을 product pack 후보로 분리
6. 마지막에 naming 정리

### Verification Commands

1차 잔존 용어 확인:

```bash
rg -n "aim-harness|AIM|IMS|dx|rb_73|GitLab|Jira|Confluence|NotebookLM|GoogleTest|gcov|manual-guide" base-harness
```

문서 변경 상태 확인:

```bash
git -C base-harness status --short
```

### Out Of Scope For This Round

- `*-aim` 디렉토리 일괄 rename
- 스킬 디렉토리 대량 이동
- 제품 전용 product-pack 디렉토리 구조 신설
- 각 스킬 내부의 상세 절차 전면 개편

## Decision Log

### 2026-04-17

- `using-aim-harness`는 SessionStart hook이 의존하므로 즉시 rename하지 않음
- `issue-analysis-base`, `completing-patch-base`, `writing-documents-base`는 현재 기준으로 제품 전용 product pack 후보로 분류
- `brainstorming-base`, `writing-plans-base`, `executing-plans-base`, `test-driven-development-base`, `systematic-debugging-base`, `verification-before-completion-base`를 다음 공통화 우선 대상으로 유지
- `MIGRATION_PLAN.md`와 `MIGRATION_LOG.md`는 역할이 겹치므로 `MIGRATION.md` 하나로 통합

## Execution Log

### 2026-04-17 1. Base 정책 문서 추가

- `AGENTS.md` 신규 작성
- 목적: `aim-harness` 복제본이 아니라 공통 하네스로 점진 추출하는 저장소라는 점을 고정
- 포함 내용: 제품 종속 요소 정의, 공통화 원칙, rename 규칙, 우선순위, 완료 기준

### 2026-04-17 2. 기준선 및 인벤토리 수집

- 기준 파일 목록 확인: `AGENTS.md`, `README.md`, Claude runtime files, `skills/*`
- 메타 문서와 hook에서 제품 종속 키워드 수집
- 스킬 전체에서 `AIM`, `IMS`, `dx`, `rb_73`, `GitLab`, `Jira`, `NotebookLM`, `manual-guide` 잔존 여부 확인

확인 결과:

- `README.md`는 거의 전면이 `aim-harness` 소개문
- Claude runtime files는 공통 라우팅 표 일부만 재사용 가능했고, 메시지와 주석은 `aim-harness` 기준이 강했다
- 코어 후보 스킬에도 제품 종속 명령과 도구 결합이 광범위하게 남아 있음

### 2026-04-17 3. 마이그레이션 체크리스트 문서화

- 초기에 `MIGRATION_PLAN.md` 신규 작성
- 이후 `MIGRATION.md`로 통합

### 2026-04-17 4. 메타 문서 1차 공통화

- `README.md`를 `base-harness` 목적 중심 문서로 재작성
- Claude runtime guide를 공통 워크플로우와 제품 전용 확장으로 분리해 1차 일반화
- Claude hook 메시지를 `base-harness` 과도기 상태 설명으로 수정

### 2026-04-17 5. 1차 재검증

- `README.md`, Claude runtime files, 마이그레이션 문서를 대상으로 잔존 용어 재검색 수행

재검증 결과:

- `README.md`의 잔존 표현은 현재 상태 설명, 분류표, 과도기 스킬명 설명에 한정됨
- Claude runtime files의 잔존 표현은 당시 메타 스킬명 `using-aim-harness` 참조에 한정됨
- 마이그레이션 문서의 잔존 표현은 인벤토리와 작업 기록 목적의 의도된 보존

판단:

- 메타 문서 1차 공통화는 완료
- 다음 라운드부터는 문서 자체보다 코어 스킬 내부의 제품 종속 명령과 도구 결합 제거가 우선

### 2026-04-17 6. 마이그레이션 문서 통합

- `MIGRATION_PLAN.md`와 `MIGRATION_LOG.md`를 `MIGRATION.md`로 통합
- 전략과 실행 이력을 한 문서에서 함께 유지하도록 구조 변경
- `README.md`의 마이그레이션 문서 참조를 `MIGRATION.md`로 변경

### 2026-04-17 7. `brainstorming-base` 1차 공통화

- `brainstorming-base/SKILL.md`에서 `AIM`, `IMS`, `Jira`, `NotebookLM` 등 제품 종속 표현 식별
- description을 AIM 전용 설계 스킬에서 공통 설계 진입 조건으로 변경
- 체크리스트의 `analysis_report.md`, 외부 시스템 조사, affected modules를 공통 개념으로 일반화
- 설계 문서 템플릿을 `Affected Modules`, 헤더 변경, errcode 중심에서 범용 component/interface/error-handling 구조로 변경
- integration 섹션은 `issue-analysis-base`를 제품 전용 선행 분석 스킬로만 남기고 나머지는 일반화

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide" base-harness/skills/brainstorming-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 파일명 `brainstorming-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음
- `../agent/prompt/<topic>/design_spec.md` 경로는 공통화 관점에서 후속 검토가 필요함

### 2026-04-17 8. `writing-plans-base` 1차 공통화

- `writing-plans-base/SKILL.md`에서 `AIM`, `dx`, 특정 헤더 규칙, errcode/msgcode, C/OpenFrame 전제 식별
- description과 overview를 AIM 전용 구현 계획 스킬에서 공통 태스크 분해 스킬로 변경
- 파일 구조 섹션을 특정 헤더 규칙이 아니라 "현재 디렉토리 관례 우선" 원칙으로 일반화
- task granularity를 `gtest`, `dx make` 고정에서 "targeted verification + broader verification" 구조로 변경
- plan header와 template을 `Affected Modules` 중심에서 범용 component/interface 중심으로 변경
- plan code sketch 원칙은 유지하되 교정 대상과 정확성 요구를 범용 개념으로 재서술

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|OpenFrame|C developer|errcode|msgcode|lib/svr/tool/util" base-harness/skills/writing-plans-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 예시 코드와 명령이 `TypeScript + pnpm`에 치우쳐 있어 완전한 스택 중립 예시는 아님
- `../agent/prompt/<topic>/plan_tasks.md` 경로는 공통화 관점에서 후속 검토가 필요함

### 2026-04-17 9. `executing-plans-base` 1차 공통화

- `executing-plans-base/SKILL.md`에서 `rb_73`, `dx`, `gtest`, coverage 스크립트, AIM 전용 branch/build 규칙 식별
- Step 0을 특정 브랜치 검사에서 범용 working context 확인 단계로 변경
- task execution 단계에서 `gtest`, `dx make` 고정을 제거하고 targeted verification + broader verification 구조로 일반화
- task 완료 후 coverage 강제를 제거하고 `verification-before-completion-base`로 최종 검증을 위임
- commit/branch 규칙을 특정 저장소 정책이 아니라 repository-specific workflow 준수 원칙으로 변경

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|clang-format|gtest|Text file busy" base-harness/skills/executing-plans-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- `../agent/prompt/<topic>/plan_tasks.md` 경로는 여전히 공통화 관점에서 후속 검토가 필요함
- 일부 설명은 여전히 branch-based workflow를 기본 사례로 두고 있어 non-git 환경까지 완전히 일반화되진 않음

### 2026-04-17 10. `test-driven-development-base` 1차 공통화

- `test-driven-development-base/SKILL.md`에서 `GoogleTest`, `gcov`, `dx`, C 전용 예시, AIM 전용 testing patterns를 식별
- 부분 수정 대신 파일 전체를 공통 TDD 스킬로 재작성
- 핵심 RED-GREEN-REFACTOR 루프와 검증 체크리스트는 유지하고, 특정 프레임워크/빌드 명령/커버리지 규칙은 제거
- bug fix, task execution, refactoring에 모두 적용 가능한 범용 TDD 원칙으로 재구성
- `testing-anti-patterns.md` 참조는 유지하되 제품 전용 문맥은 제거

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|gtest|measure_diff_cov|clang-format|C/GoogleTest|AIM_OK|AIM_ERR|Text file busy|/root/ofsrc/aim|valgrind" base-harness/skills/test-driven-development-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 예시가 현재 `TypeScript` 중심이라 다중 언어 예시까지는 제공하지 않음
- 파일명 `test-driven-development-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 11. `systematic-debugging-base` 1차 공통화

- `systematic-debugging-base/SKILL.md`에서 AIM 경로, `dx`, `gdb`, `valgrind`, errcode 중심 예시를 식별
- 부분 수정 대신 파일 전체를 공통 root-cause 디버깅 스킬로 재작성
- 핵심 4단계 구조는 유지하고, 특정 빌드/디버깅 명령 대신 증거 수집, 재현, 데이터 흐름 추적, 가설 검증 원칙으로 일반화
- supporting docs (`root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`) 참조는 유지
- Phase 4는 `test-driven-development-base`, `verification-before-completion-base`와의 연동 중심으로 정리

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|gtest|clang-format|/root/ofsrc/aim|gdb|valgrind|errcode|AIM_|fd 'filename'|Text file busy" base-harness/skills/systematic-debugging-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 실제 도구 예시(`gdb`, profiler 등)를 일반 개념으로만 남겨서 도구 선택 가이드는 다소 추상적임
- 파일명 `systematic-debugging-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 12. `verification-before-completion-base` 1차 공통화

- `verification-before-completion-base/SKILL.md`에서 `dx make gtest`, coverage 80%, 특정 스크립트 의존, AIM 전용 검증 순서를 식별
- 부분 수정 대신 파일 전체를 공통 검증 게이트 스킬로 재작성
- 핵심 "evidence before claims" 원칙은 유지하고, 저장소별 실제 검증 명령을 사용하라는 방향으로 일반화
- coverage는 저장소가 실제로 요구할 때만 측정하는 선택적 policy gate로 재배치
- reporting rule을 추가해 검증 결과를 어떻게 보고해야 하는지 명시

검증:

- 1차 검색: `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|gtest|measure_diff_cov|clang-format|/root/ofsrc/aim|Text file busy|80%|coverage" base-harness/skills/verification-before-completion-base/SKILL.md`
- 관찰: `CLAIMS` 문자열 내부의 `AIM`이 false positive로 잡힘
- 2차 검색: `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame" base-harness/skills/verification-before-completion-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- generic `coverage` 언급은 남겨두었지만, 저장소별 정책으로만 해석되도록 유지함
- 파일명 `verification-before-completion-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 13. 코어/메타 재검색

- 메타 문서 + 코어 스킬 6개(`brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`)를 대상으로 단어 기준 재검색 수행

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame" base-harness/README.md base-harness/CLAUDE.md base-harness/hooks/session-start.sh base-harness/skills/brainstorming-base/SKILL.md base-harness/skills/writing-plans-base/SKILL.md base-harness/skills/executing-plans-base/SKILL.md base-harness/skills/test-driven-development-base/SKILL.md base-harness/skills/systematic-debugging-base/SKILL.md base-harness/skills/verification-before-completion-base/SKILL.md`

결과:

- 코어 스킬 6개에서는 매칭 없음
- 잔존 표현은 대부분 `README.md`의 현재 상태 설명과 제품 종속 요소 인벤토리 섹션에만 남음
- Claude runtime files는 `using-aim-harness`라는 과도기 메타 스킬명을 직접 참조하므로 후속 rename 전까지 잔존이 예상됨

판단:

- 코어 개발 루프 공통화 1차 완료
- 다음 라운드는 협업 레이어 스킬 공통화와 과도기 메타 스킬 rename 전략 정리로 넘어감

### 2026-04-17 14. `using-feature-branches-base` 1차 공통화

- `using-feature-branches-base/SKILL.md`에서 `rb_73`, branch naming, commit/push, token URL, Jira/IMS 기반 규칙 식별
- 부분 수정 대신 파일 전체를 공통 branch/workspace isolation 스킬로 재작성
- 핵심 원칙을 "shared baseline branch에 직접 commit 금지"로 일반화
- branch naming, push flow, staging, review handoff를 저장소별 정책을 따르는 방향으로 정리
- direct push URL, 토큰, 사내 브랜치명, 한국어 commit 규칙 같은 제품 전용 내용 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|OFV7|oauth2|openframe" base-harness/skills/using-feature-branches-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- branch-based workflow를 전제로 서술돼 있어 branchless trunk-based 환경까지 완전히 포괄하진 않음
- 파일명 `using-feature-branches-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 15. `subagent-driven-development-base` 1차 공통화

- `subagent-driven-development-base/SKILL.md`에서 `dx`, AIM 규칙, 2단계 리뷰의 저장소 전용 전제, 구현자 재스폰 규칙의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 subagent execution 패턴으로 재작성
- 핵심 원칙을 "fresh implementer per task + review before acceptance"로 일반화
- implementer status 처리, review 순서, re-dispatch 규칙, context curation 역할을 저장소 중립적 개념으로 정리
- 검증 명령은 제거하고 fresh verification 재실행 원칙만 남김

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|gtest|clang-format" base-harness/skills/subagent-driven-development-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- `../agent/prompt/<topic>/plan_tasks.md` 경로는 여전히 공통화 관점에서 후속 검토가 필요함
- 구현자/리뷰자 역할 분리는 유지했지만, 실제 프롬프트 파일명(`implementer`, `spec-reviewer`, `code-quality-reviewer`) rename 전략은 아직 남아 있음

### 2026-04-17 16. `dispatching-parallel-agents-base` 1차 공통화

- `dispatching-parallel-agents-base/SKILL.md`에서 `dx`, AIM rules, module 예시, 병렬 검증 명령의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 병렬 분배 스킬로 재작성
- 핵심 원칙을 "독립 문제를 겹치지 않는 write scope로 나눠 병렬 처리"로 일반화
- task framing, ownership, overlap 방지, integration review를 저장소 중립적 개념으로 정리
- 병렬 완료 후 integrated verification 필요성을 유지하되 특정 명령은 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|gtest|clang-format" base-harness/skills/dispatching-parallel-agents-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 여전히 "agent"와 "parallel dispatch" 중심 표현이라 subagent 없는 환경에는 직접 적용성이 낮을 수 있음
- 파일명 `dispatching-parallel-agents-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 17. `requesting-code-review-base` 1차 공통화

- `requesting-code-review-base/SKILL.md`에서 AIM/MR/Phase/branch diff 전제의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 셀프 리뷰 요청 스킬로 재작성
- 핵심 원칙을 "외부 리뷰 전 자기 패치를 구조적으로 다시 검토"로 일반화
- review scope 정의, review path 호출, findings triage, fix 후 재검증 루프를 저장소 중립적 개념으로 정리
- `code-reviewer-base`는 선택 가능한 structured review workflow로만 남기고 특정 phase 설명은 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|MR|Phase|OFV7" base-harness/skills/requesting-code-review-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 실제 self-review 실행 메커니즘은 아직 `code-reviewer-base` 의존이 커서 후속 공통화 필요
- 파일명 `requesting-code-review-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 18. `receiving-code-review-base` 1차 공통화

- `receiving-code-review-base/SKILL.md`에서 AIM/GitLab/`dx`/MR discussion 전제의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 리뷰 피드백 처리 스킬로 재작성
- 핵심 원칙을 "피드백을 기술적으로 검증한 뒤 수정"으로 일반화
- triage, pushback, 채널별 응답 원칙, 수정 후 재검증 루프를 저장소 중립적 개념으로 정리
- GitLab API, curl, phase 개념, 사내 리뷰 흐름 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|MR|Phase|OFV7|curl|discussion" base-harness/skills/receiving-code-review-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- structured review 결과를 생산하는 메커니즘은 여전히 `code-reviewer-base` 의존이 커서 후속 공통화 필요
- 파일명 `receiving-code-review-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 19. `finishing-a-development-branch-base` 1차 공통화

- `finishing-a-development-branch-base/SKILL.md`에서 MR/manual/marker/coverage/push/token/patch 후속 규칙의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 branch/review completion 스킬로 재작성
- 핵심 원칙을 "검증 -> 정리 -> 브랜치 동기화 -> 리뷰/완료 옵션 제시"로 일반화
- manual-guide, marker, patch verification, GitLab API, 사내 템플릿, coverage 수치 같은 제품 전용 흐름 제거
- 제품별 release/documentation 후속은 product-specific completion steps로만 남김

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|MR|marker|pending-merge|OFV7|oauth2|curl|coverage|squash" base-harness/skills/finishing-a-development-branch-base/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- review artifact를 PR/MR 중심으로 서술해 branchless direct-submit 환경까지 완전히 일반화되진 않음
- 파일명 `finishing-a-development-branch-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 20. `code-reviewer-base` 1차 공통화

- `code-reviewer-base/SKILL.md`에서 AIM/GitLab/coverage/Phase 오케스트레이션, API 등록, 후속 검증 루프의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 리뷰 오케스트레이션 스킬로 재작성
- 핵심 원칙을 "정보 수집 -> 분석 -> 종합 -> 후속 검증" 구조로 일반화
- context collector / code reviewer / test reviewer / synthesizer 역할 분리를 저장소 중립적 개념으로 정리
- GitLab API, Phase A~I, IMS/Jira, coverage script, 사내 경로, Chrome/MCP 흐름 제거

검증:

- 1차 검색: `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|Phase|coverage|curl|MR|LGTM|clang-format|Chrome|OFV7|IMS#" base-harness/skills/code-reviewer-base/SKILL.md`
- 관찰: `coverage` 일반 용어가 "missing coverage areas" 문맥으로 매칭됨
- 판단: 제품 종속 잔재가 아니라 일반 리뷰 개념이므로 허용

잔여 리스크:

- 실제 structured review 실행 메커니즘과 동봉된 prompt 파일들은 아직 과거 naming을 유지하므로 후속 rename 전략 필요
- 파일명 `code-reviewer-base` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 21. 메타 스킬 rename 및 참조 정리

- `using-aim-harness`를 `using-base-harness`로 교체
- 새 메타 스킬 파일 `skills/using-base-harness/SKILL.md` 추가
- `README.md`와 Claude runtime files 참조를 새 이름으로 갱신
- SessionStart hook이 새 메타 스킬을 직접 주입하도록 변경

검증:

- `rg -n "using-aim-harness|using-base-harness|aim-harness skills|aim-harness" base-harness/README.md base-harness/CLAUDE.md base-harness/hooks/session-start.sh base-harness/skills/using-base-harness/SKILL.md base-harness/MIGRATION.md`

결과:

- 실행 경로에서의 `using-aim-harness` 참조는 제거됨
- `README.md`와 `MIGRATION.md`에는 여전히 과거 상태 설명과 마이그레이션 기록 목적으로 `aim-harness` 표현이 남음

잔여 리스크:

- `MIGRATION.md`는 과거 상태를 기록하므로 `aim-harness` 표현이 의도적으로 남아 있음

### 2026-04-17 22. 전체 잔존 표현 재분류

- 전체 저장소를 다시 스캔하여 남은 AIM 계열 표현을 분류함

분류 결과:

- **의도된 기록/설명용 잔존**
  - `README.md`: 현재 상태 설명, 제품 종속 인벤토리, product-specific 후보 설명
  - `MIGRATION.md`: 과거 작업 기록과 인벤토리
  - `AGENTS.md`: 공통화 기준과 판단 규칙

- **의도된 product-specific product-pack 잔존**
  - `issue-analysis-base`
  - `completing-patch-base`
  - `writing-documents-base`

- **후속 rename/정리 필요**
  - `*-aim` 접미사를 유지한 스킬명 전반
  - 동봉 prompt/support 파일의 과거 naming
  - `writing-skills-base` 내부의 AIM 전용 규칙

판단:

- 코어/협업 스킬 본문 정리는 1차 완료
- 남은 잔재의 중심은 "이름", "product-specific product pack", "supporting prompt" 세 범주다

### 2026-04-17 23. product-specific product-pack 후보 처리 전략 확정

대상:

- `issue-analysis-base`
- `completing-patch-base`
- `writing-documents-base`

전략:

1. 당장은 공통 코어로 편입하지 않는다.
2. `base-harness` 안에서는 `product-specific product-pack candidate`로 명시 유지한다.
3. 후속 라운드에서 아래 중 하나를 선택한다.
   - 명시적 product-pack 디렉토리로 분리
   - 공통 개념만 뽑아 새 코어 스킬 작성
   - legacy product pack으로 남기고 문서에서만 참조

이유:

- 현재 내용이 외부 도구와 조직 프로세스에 과하게 결합돼 있어 억지 일반화 시 문서 품질이 급격히 낮아짐
- `base-harness` 단계에서는 "무리한 일반화보다 경계 명확화"가 더 중요함

### 2026-04-17 24. 남은 운영 경로 표현과 지원 파일 범위 재분류

- 메타 문서와 지원 파일을 다시 스캔해 "실행 경로에 남은 stale 표현"과 "후속 공통화 대상"을 분리함

실행 경로 정리:

- `CLAUDE.md` 라우팅 문구의 `MR`, `Phase A~I` 표현을 일반 표현으로 교체
- 현재 실행 경로에서 남은 AIM 계열 표현은 주로 과거 상태 설명과 마이그레이션 기록에 한정됨

후속 공통화 대상:

- `brainstorming-base/spec-document-reviewer-prompt.md`
- `writing-plans-base/plan-document-reviewer-prompt.md`
- `subagent-driven-development-base/*.md`
- `code-reviewer-base/*.md`
- `test-driven-development-base/testing-anti-patterns.md`
- `writing-skills-base/*`

관찰:

- 코어/협업 `SKILL.md` 본문은 대부분 공통화됐지만, 동봉 prompt/support 파일은 아직 AIM 프로젝트 전제를 그대로 담고 있음
- 특히 `writing-skills-base`은 description, naming 규칙, tool examples, branch/review guidance 전반이 AIM harness 기준이라 별도 라운드가 필요함
- 따라서 현재 잔존의 중심은 더 이상 메인 스킬 본문이 아니라 support prompt와 skill-authoring guidance다

### 2026-04-17 25. 설계/계획 reviewer prompt 1차 공통화

- `brainstorming-base/spec-document-reviewer-prompt.md`
- `writing-plans-base/plan-document-reviewer-prompt.md`

판단:

- 두 파일은 제품 전용 product pack으로 남길 이유가 약함
- 현재 `brainstorming-base`, `writing-plans-base` 본문과 직접 연결되는 보조 reviewer prompt이므로 같은 라운드에서 공통화하는 편이 자연스러움

수정:

- reviewer 역할 설명에서 `AIM C project` 전제 제거
- `AIM conventions`, `dx`, `gtest`, 헤더 규칙 같은 저장소 전용 점검 항목을 `repository conventions`, `verification loop` 같은 일반 표현으로 교체
- interface/documentation 점검 항목은 API, schema, config, UX 변화처럼 범용 표현으로 확장

검증:

- `rg -n -w "AIM|dx|gtest|errcode|msgcode" base-harness/skills/brainstorming-base/spec-document-reviewer-prompt.md base-harness/skills/writing-plans-base/plan-document-reviewer-prompt.md`
- 결과 없음

### 2026-04-17 26. subagent 지원 프롬프트 1차 공통화

- `subagent-driven-development-base/implementer-prompt.md`
- `subagent-driven-development-base/spec-reviewer-prompt.md`
- `subagent-driven-development-base/code-quality-reviewer-prompt.md`

판단:

- 세 파일 모두 특정 제품 예시라기보다 `subagent-driven-development-base`의 핵심 실행 패턴을 구성하는 보조 prompt다
- 따라서 product-specific pack으로 분리하기보다 generic subagent prompt로 먼저 공통화하는 편이 맞음

수정:

- `AIM C project`, `dx`, `gtest`, `rb_73`, 헤더 규칙, 사내 formatting/commit 규칙을 제거
- 구현자 prompt는 repository rule, targeted verification, task-level verification 중심의 일반 지시로 교체
- spec reviewer는 제품 전용 규칙 검사 대신 task-relevant repository convention과 요구사항 충족 여부를 보도록 변경
- code quality reviewer는 C/AIM 전용 품질 기준을 repository-compatible quality checklist로 재작성

검증:

- `rg -n -w "AIM|dx|gtest|rb_73|clang-format|errcode|msgcode" base-harness/skills/subagent-driven-development-base/*.md`
- 결과 없음

### 2026-04-17 27. review 오케스트레이션 프롬프트 분류 및 1차 공통화

대상:

- `code-reviewer-base/code-reviewer-prompt.md`
- `code-reviewer-base/test-reviewer-prompt.md`
- `code-reviewer-base/review-synthesizer-prompt.md`
- `code-reviewer-base/info-collector-prompt.md`
- `code-reviewer-base/coverage-analyst-prompt.md`

분류 판단:

- `code-reviewer-prompt`, `test-reviewer-prompt`, `review-synthesizer-prompt`는 제품 전용 product pack보다 일반 리뷰 오케스트레이션 역할에 가깝다
- `info-collector-prompt`, `coverage-analyst-prompt`는 외부 시스템, API, 프로젝트 정책, 측정 스크립트 결합이 강해서 이번 라운드에서는 `product-specific product-pack` 후보로 유지한다

수정:

- 일반 리뷰 3종 prompt의 AIM/GitLab/Jira/gcov/Phase 전제를 제거
- code reviewer는 correctness, maintainability, safety, architecture fit 중심의 일반 코드 리뷰 prompt로 재작성
- test reviewer는 scenario relevance, missing cases, realism, test organization 중심의 일반 테스트 리뷰 prompt로 재작성
- synthesizer는 repository-specific delivery를 수용하는 일반 review summary prompt로 재작성

보류:

- `info-collector-prompt.md`: IMS/Jira/GitLab/API/branch 규칙 의존
- `coverage-analyst-prompt.md`: gcov, diff coverage 정책, 측정 스크립트 의존

검증:

- 1차 검색: `rg -n -w "AIM|GitLab|Jira|gcov|Phase|MR|gtest|coverage" base-harness/skills/code-reviewer-base/code-reviewer-prompt.md base-harness/skills/code-reviewer-base/test-reviewer-prompt.md base-harness/skills/code-reviewer-base/review-synthesizer-prompt.md`
- 관찰: `coverage` 일반 용어가 테스트 범위 설명으로 1건 잡힘. 제품 종속 잔재는 아님
- 2차 검색: `rg -n -w "AIM|GitLab|Jira|gcov|Phase|MR|gtest" base-harness/skills/code-reviewer-base/code-reviewer-prompt.md base-harness/skills/code-reviewer-base/test-reviewer-prompt.md base-harness/skills/code-reviewer-base/review-synthesizer-prompt.md`
- 결과 없음

### 2026-04-17 28. `writing-skills-base` 공통 skill-authoring guide로 전환

판단:

- `writing-skills-base`는 제품 전용 product pack보다 코어 방법론 문서에 가깝다
- 남아 있던 AIM 전용 요소는 skill authoring 원리 자체가 아니라 naming, tooling, branch, testing stack, external system 예시에 집중돼 있었음
- 따라서 legacy로 격리하기보다 본문을 공통 skill-authoring guide로 재작성하는 편이 저장소 목적에 부합함

수정:

- description에서 `AIM harness` 전제 제거
- `AIM-Specific Rules` 섹션 제거
- `dx`, `rb_73`, `GitLab`, `Jira`, `IMS`, `NotebookLM`, `GoogleTest`, `gcov`, `clang-format`, `aim-harness` 배포 규칙 제거
- directory/name 규칙을 저장소 로컬 convention 우선 원칙으로 일반화
- skill authoring 구조를 TDD, discovery, token discipline, rationalization control 중심의 범용 guide로 재작성

검증:

- `rg -n -w "AIM|aim-harness|dx|rb_73|GitLab|Jira|IMS|NotebookLM|GoogleTest|gcov|gtest|clang-format|C/GoogleTest" base-harness/skills/writing-skills-base/SKILL.md`
- 결과 없음

### 2026-04-17 29. support 문서 경량화 및 전체 잔존 표현 재분류

수정:

- `test-driven-development-base/testing-anti-patterns.md`를 범용 테스트 anti-pattern reference로 재작성
- 제목의 `C/GoogleTest` 전제 제거
- AIM 전용 예시(`AimConfig`, `AIM_OK`, C struct/gtest 초기화 관용구 등)를 범용 테스트 예시로 교체

전체 스캔 관찰:

- `MIGRATION.md`, `AGENTS.md`, `README.md`의 다수 매칭은 과거 상태 설명과 분류 규칙 문맥이다
- 남은 제품 종속 표현의 중심은 여전히 `issue-analysis-base`, `completing-patch-base`, `writing-documents-base`와 `code-reviewer-base/info-collector-prompt.md`, `code-reviewer-base/coverage-analyst-prompt.md` 같은 product-pack 후보 파일이다

재분류:

- 기록용 잔존:
  - `MIGRATION.md`
  - `AGENTS.md`
  - `README.md`
- product-specific product-pack 잔존:
  - `issue-analysis-base/*`
  - `completing-patch-base/*`
  - `writing-documents-base/*`
  - `code-reviewer-base/info-collector-prompt.md`
  - `code-reviewer-base/coverage-analyst-prompt.md`
  - `code-reviewer-base/scripts/measure_diff_cov.sh`
- rename-only 또는 transitional 잔존:
  - `*-aim` 디렉토리명 전반

검증:

- `rg -n -w "AIM|aim-harness|dx|rb_73|GitLab|Jira|IMS|NotebookLM|GoogleTest|gcov|gtest|clang-format|manual-guide|measure_diff_cov|MR|Phase|using-aim-harness" base-harness`
- 관찰: 매칭의 대부분은 기록 문서와 product-specific product-pack 후보에 집중됨

### 2026-04-17 30. product-specific product-pack 후보의 물리 이동 보류

검토 대상:

- `issue-analysis-base`
- `completing-patch-base`
- `writing-documents-base`
- `code-reviewer-base/info-collector-prompt.md`
- `code-reviewer-base/coverage-analyst-prompt.md`
- `code-reviewer-base/scripts/measure_diff_cov.sh`

관찰:

- 메타 문서와 라우팅 문서가 여전히 현재 `skills/` 경로를 직접 참조한다
- `issue-analysis-base`, `completing-patch-base`, `writing-documents-base`는 서로를 직접 참조한다
- `code-reviewer-base` 내부 product-specific support 파일도 현재 skill 디렉토리와 결합돼 있다

결정:

- 이번 라운드에서는 위 후보들을 별도 `product-pack` 영역으로 **물리 이동하지 않는다**
- 대신 이들을 `in-place staged product packs`로 간주한다
- 실제 이동은 아래 두 선행 조건 이후에 수행한다:
  1. `product-pack` 최종 디렉토리 구조 확정

이유:

- 지금 이동하면 경로 변경과 rename 변경이 두 번 겹쳐 문서/참조 churn이 커진다
- 현재 단계의 핵심 문제는 위치보다 경계 정의이며, 경계는 이미 문서상으로 충분히 고정됐다

### 2026-04-17 31. `*-aim` -> `*-base` rename 적용

적용 범위:

- 코어 스킬 디렉토리
- 협업 스킬 디렉토리
- product-specific product-pack 스킬 디렉토리
- 관련 `SKILL.md` frontmatter `name`
- 스킬 간 상호참조
- 메타 문서와 hook의 라우팅 이름

수정:

- `brainstorming-aim` -> `brainstorming-base`
- `writing-plans-aim` -> `writing-plans-base`
- `executing-plans-aim` -> `executing-plans-base`
- `test-driven-development-aim` -> `test-driven-development-base`
- `systematic-debugging-aim` -> `systematic-debugging-base`
- `verification-before-completion-aim` -> `verification-before-completion-base`
- `writing-skills-aim` -> `writing-skills-base`
- `subagent-driven-development-aim` -> `subagent-driven-development-base`
- `dispatching-parallel-agents-aim` -> `dispatching-parallel-agents-base`
- `using-feature-branches-aim` -> `using-feature-branches-base`
- `requesting-code-review-aim` -> `requesting-code-review-base`
- `receiving-code-review-aim` -> `receiving-code-review-base`
- `code-reviewer-aim` -> `code-reviewer-base`
- `finishing-a-development-branch-aim` -> `finishing-a-development-branch-base`
- `issue-analysis-aim` -> `issue-analysis-base`
- `completing-patch-aim` -> `completing-patch-base`
- `writing-documents-aim` -> `writing-documents-base`

추가 정리:

- 빈 `skills/using-aim-harness/` 디렉토리 제거
- `using-base-harness`는 유지

검증:

- `find base-harness/skills -maxdepth 1 -mindepth 1 -type d | sort`
- 관찰: `skills/` 아래 스킬 디렉토리는 `*-base` 또는 `using-base-harness` 기준으로 정리됨
- `rg -n "[A-Za-z0-9-]+-aim|using-aim-harness" base-harness`
- 관찰: 남은 매칭은 주로 `MIGRATION.md`의 과거 기록과 일부 product-specific pack 본문의 역사 설명에 한정됨

### 2026-04-17 32. product-specific product-pack 번들을 `product-specific/`로 분리

이동 대상:

- `skills/issue-analysis-base` -> `product-specific/skills/issue-analysis-base`
- `skills/completing-patch-base` -> `product-specific/skills/completing-patch-base`
- `skills/writing-documents-base` -> `product-specific/skills/writing-documents-base`
- `skills/code-reviewer-base/info-collector-prompt.md` -> `product-specific/code-reviewer-base/info-collector-prompt.md`
- `skills/code-reviewer-base/coverage-analyst-prompt.md` -> `product-specific/code-reviewer-base/coverage-analyst-prompt.md`
- `skills/code-reviewer-base/scripts/measure_diff_cov.sh` -> `product-specific/code-reviewer-base/scripts/measure_diff_cov.sh`

수정:

- `README.md`를 `skills/` = base runtime, `product-specific/` = product pack bundle 구조로 갱신
- `CLAUDE.md`에서 제품 전용 bundle을 기본 skill routing에서 제거
- `using-base-harness/SKILL.md`에서 product-specific 항목을 기본 skill table에서 제거하고 `product-specific/skills/` 안내로 교체
- `brainstorming-base/SKILL.md`의 `issue-analysis-base` 참조를 product-pack bundle 참조로 완화
- `product-specific/README.md` 신규 작성

판단:

- 이제 `product-specific product-pack` 번들은 개념적으로만 분리된 것이 아니라 디렉토리 구조상으로도 분리됐다
- 기본 `skills/`는 base runtime skill set만 남기는 방향으로 정리됐다

검증:

- `find base-harness/product-specific -maxdepth 3 -type f | sort`
- `find base-harness/skills -maxdepth 2 -type f | sort`
- 관찰: product-specific bundle과 code-reviewer 예시 자산이 `product-specific/` 아래로 이동했고, `skills/`에는 공통 base skill set만 남음

## Migration Summary

현재 상태는 아래처럼 요약할 수 있다.

- `skills/`의 base runtime skill set은 1차 공통화가 끝났다.
- 제품 전용 절차와 보조 자산은 `product-specific/` 아래로 분리됐다.
- 남은 정리는 주로 기록 문서 압축과 product-pack 운영 방식 명확화다.

### 2026-04-17 33. `product-specific/`를 장기적 product-pack 개념으로 고정

결정:

- `product-specific/`는 임시 예시 보관소가 아니라 제품별 확장 번들을 담는 영역으로 본다.
- 현재 구조에서는 첫 번째 product pack 영역으로 해석한다.
- `skills/`는 base runtime skill set, `product-specific/`는 선택형 product pack 번들을 담는 영역으로 구분한다.

이유:

- 현재 분리된 자산은 단순 매핑 계층보다 두껍고, 실제 제품 운영 절차를 담고 있다.
- 동시에 단순 legacy archive로 보기엔 이후 다른 제품 pack을 설계할 때 참고 가치가 있다.
- 따라서 장기 개념은 `product-pack`이 가장 자연스럽다.

향후 방향:

- 현재는 `product-specific/` 이름을 유지한다.
- 장기적으로 필요하면 `product-packs/<product>/` 구조로 승격할 수 있다.

### 2026-04-17 34. 마이그레이션 요약부 압축 및 다음 액션 재정렬

수정:

- `Migration Summary`를 현재 구조 중심의 짧은 상태 요약으로 압축
- `product-specific/`의 장기 구조 승격은 보류 상태로 두고, 즉시 필요한 문서 정리 액션만 남김
- `Next Actions`에서 이미 보류된 구조 승격 항목을 제거

판단:

- 현재 문서에서 가장 중요한 메시지는 "base runtime은 정리됐고, product-specific 자산은 product pack으로 분리됐다"는 상태다
- 구조 승격 결정은 다음 라운드로 미루더라도 현재 운영 문맥은 충분히 고정됐다

### 2026-04-17 35. 라운드 종료 요약 작성

라운드 종료 기준 요약:

- `skills/`는 base runtime skill set으로 정리됐다.
- 코어 개발 루프, 주요 협업 루프, 다수의 support prompt가 공통화됐다.
- 제품 전용 절차와 강결합 자산은 `product-specific/` 아래 product pack으로 분리됐다.
- 문서 해석도 `base runtime`과 `product pack` 경계 기준으로 고정됐다.

남은 일:

- 필요하면 기록성 문구를 더 줄인다.
- 다음 라운드에서만 `product-specific/`의 구조 승격 여부를 다시 검토한다.

### 2026-04-17 36. Codex-first runtime 구조로 재정렬

수정:

- 기존 migration 성격의 루트 `AGENTS.md`를 제거하고, Codex 기본 런타임 규칙 문서로 재작성
- 루트 `CLAUDE.md`, `settings.json`, `hooks/session-start.sh`를 `claude/` 아래 선택형 runtime pack으로 이동
- `README.md`를 `Codex-first`, `Claude-optional` 구조로 재작성
- `claude/README.md`를 추가해 Claude pack의 설치 전제를 문서화

판단:

- 루트의 메인 규칙 문서는 Codex가 직접 따르는 `AGENTS.md`여야 한다
- Claude 자산을 루트에 두면 기본 런타임이 무엇인지 계속 혼선을 준다
- Codex용 `settings.json`과 hook은 아직 런타임 계약이 확정되지 않았으므로 이번 라운드에서는 도입하지 않는다

결과:

- 루트는 `AGENTS.md` + `skills/` 중심의 Codex 기본 런타임으로 정리됐다
- Claude 사용자는 `claude/` 디렉토리의 선택형 runtime pack을 사용할 수 있다

## Next Actions

1. 필요하면 기록성 문구를 더 압축한다.
2. 필요하면 Codex 전용 runtime asset이 실제로 필요한지 별도 판단한다.

### 2026-04-17 37. runtime 용어 정리 및 기록 압축

수정:

- `using-base-harness`의 repository rule 우선순위에서 루트 `CLAUDE.md` 전제를 제거
- `MIGRATION.md` 초기 기록에서 `CLAUDE.md`, `settings.json`, `hooks/session-start.sh` 반복 서술을 `Claude runtime files` 묶음으로 압축
- 이번 세션 범위 밖인 `product-specific/` 구조 승격 제안은 `Next Actions`에서 제거

판단:

- 현재 루트 기준의 source of truth는 `AGENTS.md`다
- Claude 관련 기록은 남기되, 현재 구조와 충돌하지 않게 historical grouping만 유지하는 편이 낫다
