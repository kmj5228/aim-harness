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

- `brainstorming`
- `writing-plans`
- `executing-plans`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `writing-skills`

#### Collaboration Layer Candidates

- `subagent-driven-development`
- `dispatching-parallel-agents`
- `using-feature-branches`
- `requesting-code-review`
- `receiving-code-review`
- `code-reviewer`
- `finishing-a-development-branch`

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
- `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`를 다음 공통화 우선 대상으로 유지
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

### 2026-04-17 7. `brainstorming` 1차 공통화

- `brainstorming/SKILL.md`에서 `AIM`, `IMS`, `Jira`, `NotebookLM` 등 제품 종속 표현 식별
- description을 AIM 전용 설계 스킬에서 공통 설계 진입 조건으로 변경
- 체크리스트의 `analysis_report.md`, 외부 시스템 조사, affected modules를 공통 개념으로 일반화
- 설계 문서 템플릿을 `Affected Modules`, 헤더 변경, errcode 중심에서 범용 component/interface/error-handling 구조로 변경
- integration 섹션은 `issue-analysis-base`를 제품 전용 선행 분석 스킬로만 남기고 나머지는 일반화

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide" base-harness/skills/brainstorming/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 파일명 `brainstorming` 자체는 과도기 이름이라 아직 제품 중립적이지 않음
- `../agent/prompt/<topic>/design_spec.md` 경로는 공통화 관점에서 후속 검토가 필요함

### 2026-04-17 8. `writing-plans` 1차 공통화

- `writing-plans/SKILL.md`에서 `AIM`, `dx`, 특정 헤더 규칙, errcode/msgcode, C/OpenFrame 전제 식별
- description과 overview를 AIM 전용 구현 계획 스킬에서 공통 태스크 분해 스킬로 변경
- 파일 구조 섹션을 특정 헤더 규칙이 아니라 "현재 디렉토리 관례 우선" 원칙으로 일반화
- task granularity를 `gtest`, `dx make` 고정에서 "targeted verification + broader verification" 구조로 변경
- plan header와 template을 `Affected Modules` 중심에서 범용 component/interface 중심으로 변경
- plan code sketch 원칙은 유지하되 교정 대상과 정확성 요구를 범용 개념으로 재서술

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|OpenFrame|C developer|errcode|msgcode|lib/svr/tool/util" base-harness/skills/writing-plans/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 예시 코드와 명령이 `TypeScript + pnpm`에 치우쳐 있어 완전한 스택 중립 예시는 아님
- `../agent/prompt/<topic>/plan_tasks.md` 경로는 공통화 관점에서 후속 검토가 필요함

### 2026-04-17 9. `executing-plans` 1차 공통화

- `executing-plans/SKILL.md`에서 `rb_73`, `dx`, `gtest`, coverage 스크립트, AIM 전용 branch/build 규칙 식별
- Step 0을 특정 브랜치 검사에서 범용 working context 확인 단계로 변경
- task execution 단계에서 `gtest`, `dx make` 고정을 제거하고 targeted verification + broader verification 구조로 일반화
- task 완료 후 coverage 강제를 제거하고 `verification-before-completion`로 최종 검증을 위임
- commit/branch 규칙을 특정 저장소 정책이 아니라 repository-specific workflow 준수 원칙으로 변경

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|clang-format|gtest|Text file busy" base-harness/skills/executing-plans/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- `../agent/prompt/<topic>/plan_tasks.md` 경로는 여전히 공통화 관점에서 후속 검토가 필요함
- 일부 설명은 여전히 branch-based workflow를 기본 사례로 두고 있어 non-git 환경까지 완전히 일반화되진 않음

### 2026-04-17 10. `test-driven-development` 1차 공통화

- `test-driven-development/SKILL.md`에서 `GoogleTest`, `gcov`, `dx`, C 전용 예시, AIM 전용 testing patterns를 식별
- 부분 수정 대신 파일 전체를 공통 TDD 스킬로 재작성
- 핵심 RED-GREEN-REFACTOR 루프와 검증 체크리스트는 유지하고, 특정 프레임워크/빌드 명령/커버리지 규칙은 제거
- bug fix, task execution, refactoring에 모두 적용 가능한 범용 TDD 원칙으로 재구성
- `testing-anti-patterns.md` 참조는 유지하되 제품 전용 문맥은 제거

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|gtest|measure_diff_cov|clang-format|C/GoogleTest|AIM_OK|AIM_ERR|Text file busy|/root/ofsrc/aim|valgrind" base-harness/skills/test-driven-development/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 예시가 현재 `TypeScript` 중심이라 다중 언어 예시까지는 제공하지 않음
- 파일명 `test-driven-development` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 11. `systematic-debugging` 1차 공통화

- `systematic-debugging/SKILL.md`에서 AIM 경로, `dx`, `gdb`, `valgrind`, errcode 중심 예시를 식별
- 부분 수정 대신 파일 전체를 공통 root-cause 디버깅 스킬로 재작성
- 핵심 4단계 구조는 유지하고, 특정 빌드/디버깅 명령 대신 증거 수집, 재현, 데이터 흐름 추적, 가설 검증 원칙으로 일반화
- supporting docs (`root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`) 참조는 유지
- Phase 4는 `test-driven-development`, `verification-before-completion`와의 연동 중심으로 정리

검증:

- `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|gtest|clang-format|/root/ofsrc/aim|gdb|valgrind|errcode|AIM_|fd 'filename'|Text file busy" base-harness/skills/systematic-debugging/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 실제 도구 예시(`gdb`, profiler 등)를 일반 개념으로만 남겨서 도구 선택 가이드는 다소 추상적임
- 파일명 `systematic-debugging` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 12. `verification-before-completion` 1차 공통화

- `verification-before-completion/SKILL.md`에서 `dx make gtest`, coverage 80%, 특정 스크립트 의존, AIM 전용 검증 순서를 식별
- 부분 수정 대신 파일 전체를 공통 검증 게이트 스킬로 재작성
- 핵심 "evidence before claims" 원칙은 유지하고, 저장소별 실제 검증 명령을 사용하라는 방향으로 일반화
- coverage는 저장소가 실제로 요구할 때만 측정하는 선택적 policy gate로 재배치
- reporting rule을 추가해 검증 결과를 어떻게 보고해야 하는지 명시

검증:

- 1차 검색: `rg -n "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|gtest|measure_diff_cov|clang-format|/root/ofsrc/aim|Text file busy|80%|coverage" base-harness/skills/verification-before-completion/SKILL.md`
- 관찰: `CLAIMS` 문자열 내부의 `AIM`이 false positive로 잡힘
- 2차 검색: `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame" base-harness/skills/verification-before-completion/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- generic `coverage` 언급은 남겨두었지만, 저장소별 정책으로만 해석되도록 유지함
- 파일명 `verification-before-completion` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 13. 코어/메타 재검색

- 메타 문서 + 코어 스킬 6개(`brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`)를 대상으로 단어 기준 재검색 수행

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame" base-harness/README.md base-harness/CLAUDE.md base-harness/hooks/session-start.sh base-harness/skills/brainstorming/SKILL.md base-harness/skills/writing-plans/SKILL.md base-harness/skills/executing-plans/SKILL.md base-harness/skills/test-driven-development/SKILL.md base-harness/skills/systematic-debugging/SKILL.md base-harness/skills/verification-before-completion/SKILL.md`

결과:

- 코어 스킬 6개에서는 매칭 없음
- 잔존 표현은 대부분 `README.md`의 현재 상태 설명과 제품 종속 요소 인벤토리 섹션에만 남음
- Claude runtime files는 `using-aim-harness`라는 과도기 메타 스킬명을 직접 참조하므로 후속 rename 전까지 잔존이 예상됨

판단:

- 코어 개발 루프 공통화 1차 완료
- 다음 라운드는 협업 레이어 스킬 공통화와 과도기 메타 스킬 rename 전략 정리로 넘어감

### 2026-04-17 14. `using-feature-branches` 1차 공통화

- `using-feature-branches/SKILL.md`에서 `rb_73`, branch naming, commit/push, token URL, Jira/IMS 기반 규칙 식별
- 부분 수정 대신 파일 전체를 공통 branch/workspace isolation 스킬로 재작성
- 핵심 원칙을 "shared baseline branch에 직접 commit 금지"로 일반화
- branch naming, push flow, staging, review handoff를 저장소별 정책을 따르는 방향으로 정리
- direct push URL, 토큰, 사내 브랜치명, 한국어 commit 규칙 같은 제품 전용 내용 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|OFV7|oauth2|openframe" base-harness/skills/using-feature-branches/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- branch-based workflow를 전제로 서술돼 있어 branchless trunk-based 환경까지 완전히 포괄하진 않음
- 파일명 `using-feature-branches` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 15. `subagent-driven-development` 1차 공통화

- `subagent-driven-development/SKILL.md`에서 `dx`, AIM 규칙, 2단계 리뷰의 저장소 전용 전제, 구현자 재스폰 규칙의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 subagent execution 패턴으로 재작성
- 핵심 원칙을 "fresh implementer per task + review before acceptance"로 일반화
- implementer status 처리, review 순서, re-dispatch 규칙, context curation 역할을 저장소 중립적 개념으로 정리
- 검증 명령은 제거하고 fresh verification 재실행 원칙만 남김

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|gtest|clang-format" base-harness/skills/subagent-driven-development/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- `../agent/prompt/<topic>/plan_tasks.md` 경로는 여전히 공통화 관점에서 후속 검토가 필요함
- 구현자/리뷰자 역할 분리는 유지했지만, 실제 프롬프트 파일명(`implementer`, `spec-reviewer`, `code-quality-reviewer`) rename 전략은 아직 남아 있음

### 2026-04-17 16. `dispatching-parallel-agents` 1차 공통화

- `dispatching-parallel-agents/SKILL.md`에서 `dx`, AIM rules, module 예시, 병렬 검증 명령의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 병렬 분배 스킬로 재작성
- 핵심 원칙을 "독립 문제를 겹치지 않는 write scope로 나눠 병렬 처리"로 일반화
- task framing, ownership, overlap 방지, integration review를 저장소 중립적 개념으로 정리
- 병렬 완료 후 integrated verification 필요성을 유지하되 특정 명령은 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|gtest|clang-format" base-harness/skills/dispatching-parallel-agents/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 여전히 "agent"와 "parallel dispatch" 중심 표현이라 subagent 없는 환경에는 직접 적용성이 낮을 수 있음
- 파일명 `dispatching-parallel-agents` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 17. `requesting-code-review` 1차 공통화

- `requesting-code-review/SKILL.md`에서 AIM/MR/Phase/branch diff 전제의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 셀프 리뷰 요청 스킬로 재작성
- 핵심 원칙을 "외부 리뷰 전 자기 패치를 구조적으로 다시 검토"로 일반화
- review scope 정의, review path 호출, findings triage, fix 후 재검증 루프를 저장소 중립적 개념으로 정리
- `code-reviewer`는 선택 가능한 structured review workflow로만 남기고 특정 phase 설명은 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|MR|Phase|OFV7" base-harness/skills/requesting-code-review/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- 실제 self-review 실행 메커니즘은 아직 `code-reviewer` 의존이 커서 후속 공통화 필요
- 파일명 `requesting-code-review` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 18. `receiving-code-review` 1차 공통화

- `receiving-code-review/SKILL.md`에서 AIM/GitLab/`dx`/MR discussion 전제의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 리뷰 피드백 처리 스킬로 재작성
- 핵심 원칙을 "피드백을 기술적으로 검증한 뒤 수정"으로 일반화
- triage, pushback, 채널별 응답 원칙, 수정 후 재검증 루프를 저장소 중립적 개념으로 정리
- GitLab API, curl, phase 개념, 사내 리뷰 흐름 제거

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|MR|Phase|OFV7|curl|discussion" base-harness/skills/receiving-code-review/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- structured review 결과를 생산하는 메커니즘은 여전히 `code-reviewer` 의존이 커서 후속 공통화 필요
- 파일명 `receiving-code-review` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 19. `finishing-a-development-branch` 1차 공통화

- `finishing-a-development-branch/SKILL.md`에서 MR/manual/marker/coverage/push/token/patch 후속 규칙의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 branch/review completion 스킬로 재작성
- 핵심 원칙을 "검증 -> 정리 -> 브랜치 동기화 -> 리뷰/완료 옵션 제시"로 일반화
- manual-guide, marker, patch verification, GitLab API, 사내 템플릿, coverage 수치 같은 제품 전용 흐름 제거
- 제품별 release/documentation 후속은 product-specific completion steps로만 남김

검증:

- `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|MR|marker|pending-merge|OFV7|oauth2|curl|coverage|squash" base-harness/skills/finishing-a-development-branch/SKILL.md`
- 결과: 매칭 없음

잔여 리스크:

- review artifact를 PR/MR 중심으로 서술해 branchless direct-submit 환경까지 완전히 일반화되진 않음
- 파일명 `finishing-a-development-branch` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

### 2026-04-17 20. `code-reviewer` 1차 공통화

- `code-reviewer/SKILL.md`에서 AIM/GitLab/coverage/Phase 오케스트레이션, API 등록, 후속 검증 루프의 제품 종속 표현을 식별
- 부분 수정 대신 파일 전체를 공통 리뷰 오케스트레이션 스킬로 재작성
- 핵심 원칙을 "정보 수집 -> 분석 -> 종합 -> 후속 검증" 구조로 일반화
- context collector / code reviewer / test reviewer / synthesizer 역할 분리를 저장소 중립적 개념으로 정리
- GitLab API, Phase A~I, IMS/Jira, coverage script, 사내 경로, Chrome/MCP 흐름 제거

검증:

- 1차 검색: `rg -n -w "AIM|IMS|Jira|NotebookLM|dx|rb_73|GitLab|Confluence|GoogleTest|gcov|manual-guide|measure_diff_cov|OpenFrame|Phase|coverage|curl|MR|LGTM|clang-format|Chrome|OFV7|IMS#" base-harness/skills/code-reviewer/SKILL.md`
- 관찰: `coverage` 일반 용어가 "missing coverage areas" 문맥으로 매칭됨
- 판단: 제품 종속 잔재가 아니라 일반 리뷰 개념이므로 허용

잔여 리스크:

- 실제 structured review 실행 메커니즘과 동봉된 prompt 파일들은 아직 과거 naming을 유지하므로 후속 rename 전략 필요
- 파일명 `code-reviewer` 자체는 과도기 이름이라 아직 제품 중립적이지 않음

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
  - `writing-skills` 내부의 AIM 전용 규칙

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

- `brainstorming/spec-document-reviewer-prompt.md`
- `writing-plans/plan-document-reviewer-prompt.md`
- `subagent-driven-development/*.md`
- `code-reviewer/*.md`
- `test-driven-development/testing-anti-patterns.md`
- `writing-skills/*`

관찰:

- 코어/협업 `SKILL.md` 본문은 대부분 공통화됐지만, 동봉 prompt/support 파일은 아직 AIM 프로젝트 전제를 그대로 담고 있음
- 특히 `writing-skills`은 description, naming 규칙, tool examples, branch/review guidance 전반이 AIM harness 기준이라 별도 라운드가 필요함
- 따라서 현재 잔존의 중심은 더 이상 메인 스킬 본문이 아니라 support prompt와 skill-authoring guidance다

### 2026-04-17 25. 설계/계획 reviewer prompt 1차 공통화

- `brainstorming/spec-document-reviewer-prompt.md`
- `writing-plans/plan-document-reviewer-prompt.md`

판단:

- 두 파일은 제품 전용 product pack으로 남길 이유가 약함
- 현재 `brainstorming`, `writing-plans` 본문과 직접 연결되는 보조 reviewer prompt이므로 같은 라운드에서 공통화하는 편이 자연스러움

수정:

- reviewer 역할 설명에서 `AIM C project` 전제 제거
- `AIM conventions`, `dx`, `gtest`, 헤더 규칙 같은 저장소 전용 점검 항목을 `repository conventions`, `verification loop` 같은 일반 표현으로 교체
- interface/documentation 점검 항목은 API, schema, config, UX 변화처럼 범용 표현으로 확장

검증:

- `rg -n -w "AIM|dx|gtest|errcode|msgcode" base-harness/skills/brainstorming/spec-document-reviewer-prompt.md base-harness/skills/writing-plans/plan-document-reviewer-prompt.md`
- 결과 없음

### 2026-04-17 26. subagent 지원 프롬프트 1차 공통화

- `subagent-driven-development/implementer-prompt.md`
- `subagent-driven-development/spec-reviewer-prompt.md`
- `subagent-driven-development/code-quality-reviewer-prompt.md`

판단:

- 세 파일 모두 특정 제품 예시라기보다 `subagent-driven-development`의 핵심 실행 패턴을 구성하는 보조 prompt다
- 따라서 product-specific pack으로 분리하기보다 generic subagent prompt로 먼저 공통화하는 편이 맞음

수정:

- `AIM C project`, `dx`, `gtest`, `rb_73`, 헤더 규칙, 사내 formatting/commit 규칙을 제거
- 구현자 prompt는 repository rule, targeted verification, task-level verification 중심의 일반 지시로 교체
- spec reviewer는 제품 전용 규칙 검사 대신 task-relevant repository convention과 요구사항 충족 여부를 보도록 변경
- code quality reviewer는 C/AIM 전용 품질 기준을 repository-compatible quality checklist로 재작성

검증:

- `rg -n -w "AIM|dx|gtest|rb_73|clang-format|errcode|msgcode" base-harness/skills/subagent-driven-development/*.md`
- 결과 없음

### 2026-04-17 27. review 오케스트레이션 프롬프트 분류 및 1차 공통화

대상:

- `code-reviewer/code-reviewer-prompt.md`
- `code-reviewer/test-reviewer-prompt.md`
- `code-reviewer/review-synthesizer-prompt.md`
- `code-reviewer/info-collector-prompt.md`
- `code-reviewer/coverage-analyst-prompt.md`

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

- 1차 검색: `rg -n -w "AIM|GitLab|Jira|gcov|Phase|MR|gtest|coverage" base-harness/skills/code-reviewer/code-reviewer-prompt.md base-harness/skills/code-reviewer/test-reviewer-prompt.md base-harness/skills/code-reviewer/review-synthesizer-prompt.md`
- 관찰: `coverage` 일반 용어가 테스트 범위 설명으로 1건 잡힘. 제품 종속 잔재는 아님
- 2차 검색: `rg -n -w "AIM|GitLab|Jira|gcov|Phase|MR|gtest" base-harness/skills/code-reviewer/code-reviewer-prompt.md base-harness/skills/code-reviewer/test-reviewer-prompt.md base-harness/skills/code-reviewer/review-synthesizer-prompt.md`
- 결과 없음

### 2026-04-17 28. `writing-skills` 공통 skill-authoring guide로 전환

판단:

- `writing-skills`는 제품 전용 product pack보다 코어 방법론 문서에 가깝다
- 남아 있던 AIM 전용 요소는 skill authoring 원리 자체가 아니라 naming, tooling, branch, testing stack, external system 예시에 집중돼 있었음
- 따라서 legacy로 격리하기보다 본문을 공통 skill-authoring guide로 재작성하는 편이 저장소 목적에 부합함

수정:

- description에서 `AIM harness` 전제 제거
- `AIM-Specific Rules` 섹션 제거
- `dx`, `rb_73`, `GitLab`, `Jira`, `IMS`, `NotebookLM`, `GoogleTest`, `gcov`, `clang-format`, `aim-harness` 배포 규칙 제거
- directory/name 규칙을 저장소 로컬 convention 우선 원칙으로 일반화
- skill authoring 구조를 TDD, discovery, token discipline, rationalization control 중심의 범용 guide로 재작성

검증:

- `rg -n -w "AIM|aim-harness|dx|rb_73|GitLab|Jira|IMS|NotebookLM|GoogleTest|gcov|gtest|clang-format|C/GoogleTest" base-harness/skills/writing-skills/SKILL.md`
- 결과 없음

### 2026-04-17 29. support 문서 경량화 및 전체 잔존 표현 재분류

수정:

- `test-driven-development/testing-anti-patterns.md`를 범용 테스트 anti-pattern reference로 재작성
- 제목의 `C/GoogleTest` 전제 제거
- AIM 전용 예시(`AimConfig`, `AIM_OK`, C struct/gtest 초기화 관용구 등)를 범용 테스트 예시로 교체

전체 스캔 관찰:

- `MIGRATION.md`, `AGENTS.md`, `README.md`의 다수 매칭은 과거 상태 설명과 분류 규칙 문맥이다
- 남은 제품 종속 표현의 중심은 여전히 `issue-analysis-base`, `completing-patch-base`, `writing-documents-base`와 `code-reviewer/info-collector-prompt.md`, `code-reviewer/coverage-analyst-prompt.md` 같은 product-pack 후보 파일이다

재분류:

- 기록용 잔존:
  - `MIGRATION.md`
  - `AGENTS.md`
  - `README.md`
- product-specific product-pack 잔존:
  - `issue-analysis-base/*`
  - `completing-patch-base/*`
  - `writing-documents-base/*`
  - `code-reviewer/info-collector-prompt.md`
  - `code-reviewer/coverage-analyst-prompt.md`
  - `code-reviewer/scripts/measure_diff_cov.sh`
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
- `code-reviewer/info-collector-prompt.md`
- `code-reviewer/coverage-analyst-prompt.md`
- `code-reviewer/scripts/measure_diff_cov.sh`

관찰:

- 메타 문서와 라우팅 문서가 여전히 현재 `skills/` 경로를 직접 참조한다
- `issue-analysis-base`, `completing-patch-base`, `writing-documents-base`는 서로를 직접 참조한다
- `code-reviewer` 내부 product-specific support 파일도 현재 skill 디렉토리와 결합돼 있다

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

- `brainstorming-aim` -> `brainstorming`
- `writing-plans-aim` -> `writing-plans`
- `executing-plans-aim` -> `executing-plans`
- `test-driven-development-aim` -> `test-driven-development`
- `systematic-debugging-aim` -> `systematic-debugging`
- `verification-before-completion-aim` -> `verification-before-completion`
- `writing-skills-aim` -> `writing-skills`
- `subagent-driven-development-aim` -> `subagent-driven-development`
- `dispatching-parallel-agents-aim` -> `dispatching-parallel-agents`
- `using-feature-branches-aim` -> `using-feature-branches`
- `requesting-code-review-aim` -> `requesting-code-review`
- `receiving-code-review-aim` -> `receiving-code-review`
- `code-reviewer-aim` -> `code-reviewer`
- `finishing-a-development-branch-aim` -> `finishing-a-development-branch`
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
- `skills/code-reviewer/info-collector-prompt.md` -> `product-specific/code-reviewer/info-collector-prompt.md`
- `skills/code-reviewer/coverage-analyst-prompt.md` -> `product-specific/code-reviewer/coverage-analyst-prompt.md`
- `skills/code-reviewer/scripts/measure_diff_cov.sh` -> `product-specific/code-reviewer/scripts/measure_diff_cov.sh`

수정:

- `README.md`를 `skills/` = base runtime, `product-specific/` = product pack bundle 구조로 갱신
- `CLAUDE.md`에서 제품 전용 bundle을 기본 skill routing에서 제거
- `using-base-harness/SKILL.md`에서 product-specific 항목을 기본 skill table에서 제거하고 `product-specific/skills/` 안내로 교체
- `brainstorming/SKILL.md`의 `issue-analysis-base` 참조를 product-pack bundle 참조로 완화
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

### 2026-04-17 38. Codex hook source 추가

수정:

- `hooks/config.toml`, `hooks/hooks.json`, `hooks/session-start.sh`를 추가
- `hooks/`를 Codex hook source-of-truth로 문서화
- `README.md`, `AGENTS.md`에 실제 Codex 사용 시 `.codex/` 또는 `~/.codex/` 배치가 필요하다는 점을 명시

판단:

- 저장소를 `git pull`하는 것만으로는 사용자 로컬 Codex 런타임에 hook이 자동 적용되지 않는다
- 하지만 repository source 차원에서는 Codex hook 자산을 함께 버전 관리하는 편이 낫다
- 따라서 `hooks/`는 소스 위치로 두고, 실제 활성화는 사용자 설치 단계에서 수행하는 구조가 적절하다

### 2026-04-20 39. `harness-initiator` 작업 기준선 기록

수정:

- 작업 브랜치 `harness-initiator`를 생성
- 현재 합의된 initiator 방향을 `HARNESS_INITIATOR.md`에 기록
- `README.md`에 initiator 결정 문서 링크를 추가

현재 합의:

- 변환 입력 묶음은 `source-packs/` 대신 `templates/`라는 이름으로 가정
- 생성 결과는 `generated/<product>-harness/` 아래에 둠
- 최초 대상 제품은 `ofgw`
- initiator는 `adapter draft 생성 -> 사용자 확인 -> product harness 생성` 흐름을 담당
- adapter 포맷은 우선 `product-profile.yaml`, `mappings.yaml` 두 파일만 사용
- 이번 라운드에서는 실제 구조 개편, 파일 이동, 스킬 구현을 하지 않음

판단:

- 아직 구조를 바꾸기보다 결정사항과 짧은 실행 단위를 먼저 고정하는 편이 안전하다
- 특히 `product-specific/` 자산의 물리 이동은 initiator 입력/출력 계약이 더 선명해진 뒤 진행하는 편이 낫다

### 2026-04-20 40. Session 2 입력 인벤토리 기록

수정:

- `product-specific/` 자산을 initiator 입력 후보 관점에서 1차 분류
- 결과를 `HARNESS_INITIATOR.md`에 기록

분류 결과:

- **1차 template 후보**
  - `issue-analysis-base`
  - `writing-documents-base`
  - `writing-documents-base/markdown-guide.md`
- **분해 후 검토 대상**
  - `completing-patch-base`
  - `writing-documents-base/manual-guide.md`
- **초기 범위 제외**
  - `writing-documents-base` 하위의 platform guide 다수
  - `product-specific/code-reviewer/*`
  - `measure_diff_cov.sh`

판단:

- 첫 initiator 시범 범위는 전체 product workflow가 아니라, 템플릿화 가능한 분석/문서 허브 중심으로 좁히는 편이 낫다
- QA 문서, 수동 운영 절차, 저장소 정책 결합 스크립트는 adapter 이전에 먼저 분해 기준이 필요하다

### 2026-04-20 41. Core Neutrality Audit 추가

수정:

- `skills/*-base`에 대해 stack-specific example, artifact path contract, runtime coupling을 1차 점검
- 결과를 `HARNESS_INITIATOR.md`에 기록하고 세션 순서를 조정

주요 관찰:

- `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`는 `../agent/prompt/<topic>/...` 경로 계약을 공통 전제로 둔다
- `writing-plans`, `test-driven-development`는 `TypeScript`/`pnpm` 예시 편향이 남아 있다
- `verification-before-completion`, `systematic-debugging`, `code-reviewer`는 상대적으로 기술 스택 중립성이 높다
- `using-base-harness`와 `writing-skills`는 strict core라기보다 runtime/meta 성격이므로 별도 취급이 적절하다

판단:

- initiator가 core skill의 스택 편향까지 보정하는 구조는 좋지 않다
- path contract와 example neutralization은 base layer에서 먼저 정리하고, initiator는 product adaptation에 집중시키는 편이 맞다

### 2026-04-20 42. Artifact Contract 초안 추가

수정:

- `HARNESS_INITIATOR.md`에 core-neutral artifact contract를 추가
- micro-session 순서를 갱신하여 initiator phase 설계 전에 artifact contract를 고정

계약 초안:

- core skill은 physical path 대신 logical artifact id를 사용
- 1차 대상 artifact:
  - `analysis_report`
  - `design_spec`
  - `implementation_plan`
- 현재 `../agent/prompt/<topic>/...`는 transitional runtime mapping으로만 유지

판단:

- 지금 문제의 본질은 파일명보다 physical root hardcoding이다
- 따라서 이번 라운드의 최소 목표는 canonical filename을 유지한 채, core skill이 root path를 직접 아는 구조를 끊는 것이다

### 2026-04-20 43. 1차 core skill neutralization 적용

수정:

- `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `test-driven-development`를 수정
- artifact 참조를 physical path 대신 logical artifact 중심으로 재서술
- stack-specific 예시(`TypeScript`, `pnpm`)를 stack-neutral pseudocode로 교체

검증:

- `rg -n '\\.\\./agent/prompt|pnpm|TypeScript|buildResult|validateQueueName' <대상 스킬들>`
- 관찰: direct path hardcoding과 이전 TS 예시 표현은 제거됨

판단:

- core layer는 이제 artifact identity를 알고, physical path는 runtime mapping이 제공하는 구조로 이동하기 시작했다
- 아직 canonical filename 설명은 일부 남겨두었지만, 이는 transitional mapping 문맥으로만 유지된다

### 2026-04-20 44. 메타 스킬 및 markdown guide 정렬

수정:

- `using-base-harness`에 transitional product-bound layout과 장기 방향(`templates/`, `adapters/`, `generated/`)을 병기
- `using-base-harness`에 logical artifact convention을 추가
- `product-specific/skills/writing-documents-base/markdown-guide.md`를 artifact contract 기준으로 재서술

추가 점검:

- `dispatching-parallel-agents`
- `systematic-debugging`

판단:

- 위 두 스킬은 현재 기준으로 path hardcoding이나 stack-specific example이 거의 없어 추가 수정 없이 유지 가능하다
- 남은 artifact/path 결합은 주로 product-specific 문서군과 후속 템플릿 분해 작업에서 다루면 된다

### 2026-04-20 45. Initiator phase contract 고정

수정:

- `HARNESS_INITIATOR.md`의 Session 5에 initiator phase contract를 추가
- `analyze -> draft-adapter -> confirm-gaps -> generate-harness` 각 단계의 입력/출력/중단 조건을 명시

핵심 규칙:

- `analyze`는 선택된 template 후보와 target repo만 다룬다
- `draft-adapter`는 inferred 값과 unresolved 값을 분리한다
- `confirm-gaps`는 필수 사용자 확인 게이트다
- `generate-harness`는 confirmed adapter만 입력으로 받는다

판단:

- adapter 초안 생성과 사용자 확인을 분리해야 추정값을 사실처럼 굳히는 오류를 막을 수 있다
- 생성 단계는 마지막에 두어야 제외 대상과 생성 대상의 경계를 함께 보고할 수 있다

### 2026-04-20 46. 결과물 우선순위 재정렬

수정:

- `HARNESS_INITIATOR.md`에 deliverable priority를 추가
- micro-session 순서를 `generated/ofgw-harness/` 설계 우선이 아니라 `harness-initiator` 스킬 우선으로 재정렬

새 우선순위:

- 1차 핵심 결과물: `harness-initiator` 스킬
- 후속 검증 대상: `generated/<product>-harness/`

판단:

- 지금 단계에서는 생성 결과 자체보다 생성기 계약과 스킬 본문을 먼저 고정하는 편이 낫다
- `generated/ofgw-harness/`는 initiator 품질을 확인하는 첫 validation target으로 다루는 것이 더 자연스럽다

### 2026-04-20 47. `harness-initiator` 스킬 초안 추가

수정:

- `skills/harness-initiator/SKILL.md` 신규 작성
- `using-base-harness`, `AGENTS.md`, `README.md`에 initiator 스킬 참조 추가

스킬 초안 범위:

- trigger 정의
- first-run scope
- `analyze -> draft-adapter -> confirm-gaps -> generate-harness` workflow
- output contract
- common mistakes

판단:

- initiator는 이제 메모 문서의 아이디어가 아니라 실제로 호출 가능한 skill 초안이 됐다
- 다음 라운드에서는 이 skill이 요구하는 adapter schema를 더 구체화하는 편이 자연스럽다

### 2026-04-20 48. Adapter draft contract 정의

수정:

- `HARNESS_INITIATOR.md` Session 7에 `product-profile.yaml`, `mappings.yaml` 최소 schema를 추가
- `skills/harness-initiator/SKILL.md`에 adapter draft contract 요약을 추가

핵심 규칙:

- `product-profile.yaml`은 repo facts와 workflow confirmation fields를 분리한다
- `mappings.yaml`은 terminology / command / workflow 대응을 담는다
- unresolved 값은 `confirm` 목록으로 남겨 추정값이 확정값처럼 굳지 않게 한다

`ofgw` 기준 현재 추론 가능 사실:

- build systems: `gradle`, `pnpm`
- languages: `java`, `kotlin`, `javascript`
- modules: `ofgwSrc`, `webterminal`, `ofgwAdmin`
- test/coverage stack: `junit5`, `mockito`, `jacoco`

판단:

- 첫 adapter schema는 작게 시작하는 편이 맞다
- 반복적인 generation 시도에서 공통 필드가 더 드러날 때만 schema를 확장한다

### 2026-04-20 49. Template boundary 정의

수정:

- `HARNESS_INITIATOR.md` Session 8에 `issue-analysis`, `writing-documents`, `markdown-guide`의 boundary 기준을 추가
- `skills/harness-initiator/SKILL.md`에 mixed-stack target을 template body에 과적합시키지 말라는 규칙을 추가

핵심 경계:

- template body:
  - reusable workflow skeleton
  - approval / verdict / document-structure rules
- binding 또는 product config:
  - issue system, review channel, docs channel
  - concrete commands, repo paths, auth, automation choice
- reference/example:
  - URL patterns
  - API call examples
  - product-specific sub-guides

추가 판단:

- `ofgw`는 adapter draft 사실을 얻는 데 유용하지만, OF 계열 대부분이 C 기반이라는 점을 고려하면 template body를 mixed-stack 기준으로 다시 쓰면 안 된다
- 따라서 `markdown-guide`는 shared support reference로 두고, main template 후보는 `issue-analysis`, `writing-documents` 중심으로 유지한다

### 2026-04-20 50. Confirmation loop 정의

수정:

- `HARNESS_INITIATOR.md` Session 9에 confirmation packet / grouped question / resolution state 규칙을 추가
- `skills/harness-initiator/SKILL.md`의 confirm-gaps 단계에 동일한 운용 규칙을 추가

핵심 규칙:

- 보고는 `Inferred Facts / Needs Confirmation / Red Flags / Proposed Next Step` 4블록으로 구성
- 질문은 workflow core / release-manual policy / terminology 묶음으로 제시
- unresolved 상태는 `confirmed`, `deferred`, `unknown`으로만 관리

판단:

- initiator는 질문을 잘게 쪼개기보다 확인 패킷 형태로 묶어서 보여주는 편이 낫다
- `unknown` 상태를 남긴 채 생성으로 넘어가면 adapter 초안의 미확정 값이 다시 숨겨지므로, 이 상태는 생성 금지 게이트로 유지한다

### 2026-04-20 51. First validation target 정의

수정:

- `HARNESS_INITIATOR.md` Session 10에 첫 `ofgw` validation target의 pass criteria / non-goals / failure signals를 추가
- `skills/harness-initiator/SKILL.md`에 first validation target 섹션을 추가

핵심 기준:

- 첫 검증의 목표는 완성된 `ofgw-harness`가 아니라 `harness-initiator`가 계약된 흐름을 유지하는지 확인하는 것이다
- pass 조건은 `analyze -> draft-adapter -> confirm-gaps -> minimal generate-harness`가 끝까지 성립하는지에 둔다
- 첫 generated scope는 `issue-analysis`, `writing-documents`, `markdown-guide` support reference로 제한한다

실패 신호:

- `unknown` 값이 남아 있는데 generation을 진행함
- 제외된 asset을 summary 없이 누락함
- `ofgw` mixed-stack 사실을 template body 규칙으로 승격시킴
- 첫 검증 범위를 넘어 `completing-patch` 같은 자산까지 암묵적으로 포함함

판단:

- 현재 라운드의 핵심 deliverable은 여전히 생성물보다 생성기다
- 따라서 validation도 generated harness의 완성도보다, initiator가 범위와 제외 대상을 얼마나 명확히 통제하는지에 맞추는 편이 더 적절하다

### 2026-04-20 52. Generated harness skeleton 최소화

수정:

- `HARNESS_INITIATOR.md` Session 11에 first validation pass용 minimal generated skeleton을 추가
- `skills/harness-initiator/SKILL.md`의 generate 단계에 minimal skeleton 규칙을 추가

최소 skeleton:

- `generated/ofgw-harness/AGENTS.md`
- `generated/ofgw-harness/README.md`
- `generated/ofgw-harness/GENERATION_SUMMARY.md`
- `generated/ofgw-harness/skills/product/issue-analysis/`
- `generated/ofgw-harness/skills/docs/writing-documents/`
- `generated/ofgw-harness/references/markdown-guide.md`

명시적 제외 범위:

- `hooks/`
- `profiles/`
- `skills/core/`
- `skills/collab/`
- `skills/review/`
- `completing-patch`, manual/release workflow 디렉토리

판단:

- 첫 validation pass는 full harness rollout이 아니라 template selection과 exclusion reporting이 올바른지 검증하는 단계다
- 따라서 공통 자산 전체를 복제하기보다, selected template scope와 support reference만 담는 작은 skeleton이 더 적절하다

### 2026-04-20 53. First build readiness 점검

수정:

- `HARNESS_INITIATOR.md` Session 12에 first build readiness 결과를 추가
- `skills/harness-initiator/SKILL.md`에 readiness 상태를 짧게 명시

판정:

- `analyze`: ready
- `draft-adapter`: ready
- `confirm-gaps`: ready
- `generate-harness`: confirmed adapter 전까지 not ready

다음 실제 필요 작업:

- 하나의 concrete `ofgw` analysis snapshot 수집
- 첫 `product-profile.yaml` / `mappings.yaml` draft 작성
- 첫 confirmation packet 구성
- unresolved 값 사용자 확인 후 generation 시도

판단:

- 이제 부족한 것은 설계 문서가 아니라 첫 실제 draft 실행이다
- 따라서 다음 라운드는 설계 확장보다 `ofgw` adapter draft를 실제로 구성해 보는 쪽이 더 적절하다

### 2026-04-20 54. First `ofgw` adapter draft packet 작성

수정:

- `adapters/ofgw/analysis-summary.md` 추가
- `adapters/ofgw/product-profile.yaml` 추가
- `adapters/ofgw/mappings.yaml` 추가
- `adapters/ofgw/confirmation-packet.md` 추가
- `HARNESS_INITIATOR.md`에 Session 13과 session log를 추가

초안에 반영한 inferred facts:

- build systems: `gradle`, `pnpm`
- languages: `java`, `kotlin`, `javascript`
- modules: `ofgwSrc`, `webterminal`, `ofgwAdmin`
- runtime hints: `jeus`, `servlet`, `websocket`, `jpa`, `querydsl`
- test stack: `junit5`, `mockito`, `assertj`, `hamcrest`
- coverage: `jacoco`

초안에서 계속 미확정으로 남긴 값:

- `workflow.issue_tracker`
- `workflow.review_channel`
- `workflow.docs_channel`
- `workflow.manual_workflow_required`
- terminology fields
- workflow binding fields

판단:

- 이제 initiator 흐름은 추상 설계가 아니라 실제 draft artifact까지 내려왔다
- `ofgw`용 YAML은 사용자가 맨땅에서 쓰는 파일이 아니라, initiator가 codebase-derived 사실을 채우고 사람 확인이 필요한 값만 남기는 초안이라는 점을 concrete file로 확인했다

### 2026-04-20 55. Confirmation candidate narrowing

수정:

- `adapters/ofgw/confirmation-packet.md`에 suggested defaults를 추가

추천 후보:

- `workflow.issue_tracker`: `jira`
- `workflow.review_channel`: `pull_request`
- `workflow.docs_channel`: `repo_markdown` (low confidence)
- `workflow.manual_workflow_required`: 계속 미확정

근거:

- root `ofgw/AGENTS.md`에 Jira query guardrail과 `OFV7-1234` 예시가 있다
- `ofgwAdmin/AGENTS.md`에 PR expectation이 명시돼 있다
- markdown 문서는 보이지만 Confluence/wiki 강신호는 찾지 못했다

판단:

- 이 단계의 목적은 사용자 확인값을 대신 확정하는 것이 아니라, confirmation 질문을 더 좁히는 것이다
- 따라서 suggested default는 confirmation packet에만 두고, adapter YAML 자체는 아직 미확정 상태로 유지한다

### 2026-04-20 56. Adapter contract를 access binding 중심으로 재정의

수정:

- `HARNESS_INITIATOR.md` Session 7의 active contract를 workflow/terminology 중심에서 access/integration binding 중심으로 수정
- `skills/harness-initiator/SKILL.md`의 optional input, confirm-gaps grouping, adapter draft contract 문구를 동일 기준으로 수정

핵심 변화:

- `product-profile.yaml`은 repo facts + workflow defaults + safety note 레이어로 본다
- `mappings.yaml`은 terminology보다 `access_bindings`를 더 중요한 adaptation 레이어로 본다
- confirm 우선순위는 `issue/review/docs/notebook/manual access` 쪽으로 이동한다

판단:

- 같은 조직/팀 계열에서는 issue tracker 이름 자체보다, Jira/NotebookLM/manual repo에 어떻게 접근하는지가 실제 product adaptation에 더 중요할 수 있다
- 따라서 initiator의 핵심 질문도 "무슨 시스템인가"보다 "어떤 mode와 location으로 붙는가"를 먼저 다루는 쪽이 더 맞다

### 2026-04-20 57. `ofgw` draft를 access binding 기준으로 재작성

수정:

- `adapters/ofgw/product-profile.yaml` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `adapters/ofgw/confirmation-packet.md` 수정

핵심 변화:

- `workflow.issue_tracker` 등 직접 필드를 `workflow.defaults.*`로 내렸다
- `workflow_bindings`를 제거하고 `access_bindings.issue_access/review_access/docs_access/notebook_access/manual_access`로 교체했다
- confirmation packet도 `workflow core`보다 `access bindings`를 먼저 묻도록 바꿨다

판단:

- 이제 `ofgw` 초안은 initiator의 새 active contract와 같은 모델을 사용한다
- 현재 남은 질문은 시스템 종류 자체보다 `mode`, `location`, `manual/notebook` 관련 binding 쪽에 집중된다

### 2026-04-21 58. `repo` mode naming 정리

수정:

- `HARNESS_INITIATOR.md`, `skills/harness-initiator/SKILL.md`의 mode 예시를 `workspace_file`로 변경
- `adapters/ofgw/mappings.yaml`, `adapters/ofgw/confirmation-packet.md`의 `docs_access.mode`를 `workspace_file`로 변경

판단:

- `repo`는 mode 이름으로 두면 Git 저장소 자체와 file access 방식을 혼동시키기 쉽다
- `workspace_file`은 현재 작업 중인 워크스페이스 파일을 직접 읽고 쓴다는 뜻이 더 분명하다

### 2026-04-21 59. Provider registry 구조로 재정의

수정:

- `HARNESS_INITIATOR.md`의 `access_bindings` 예시를 provider registry 형태로 변경
- `skills/harness-initiator/SKILL.md`의 adapter contract 문구를 provider-style binding 기준으로 수정
- `adapters/ofgw/mappings.yaml`, `adapters/ofgw/confirmation-packet.md`를 provider registry 기준으로 재작성

핵심 변화:

- `issue_sources`, `spec_sources`, `review_targets`, `docs_targets`, `manual_targets`를 도입
- `jira`, `ims`, `notebooklm`, `pull_request`, `repo_markdown`, `manual_repo`를 provider entry로 취급
- 확인 항목을 flat access field 대신 provider별 `enabled/default_mode/location` 중심으로 재배치

판단:

- initiator는 특정 시스템 이름을 고정하는 도구보다, 요청 대상별 provider를 선택하는 라우터에 가까워야 한다
- 따라서 실제 generate gate도 provider label보다 provider location과 사용 여부 쪽 확인이 더 중요하다

### 2026-04-21 60. Jira/IMS provider 기본값 구체화

수정:

- `adapters/ofgw/mappings.yaml`에서 `jira` provider를 `mcp` 기본 + `api` fallback으로 구체화
- `adapters/ofgw/mappings.yaml`에서 `ims.enabled`를 `true`로 바꾸고 URL pattern을 채움
- `adapters/ofgw/confirmation-packet.md`에 Jira MCP setup requirement와 REST API fallback 안내를 추가
- `HARNESS_INITIATOR.md`에 Session 19를 추가

핵심 변화:

- `jira.location` 기본값을 `atlassian-rovo`로 둠
- Jira MCP 사용 시 `codex mcp add/login/list/get` 절차를 사용자에게 알려줘야 한다고 명시
- MCP 실패 시 REST API fallback 정보를 같이 보여주도록 정리
- IMS는 기존 `issue-analysis-base`의 browser URL pattern을 기본 provider location으로 채움

판단:

- initiator는 provider label만 채우는 것이 아니라, 실제로 그 provider를 사용하기 위해 필요한 bootstrap 정보를 함께 말해줘야 한다
- `ims`는 이미 기존 스킬에 검증된 접근 패턴이 있으므로 default enabled로 두는 쪽이 더 일관적이다

### 2026-04-21 61. NotebookLM/PR/workspace 기본값 반영

수정:

- `adapters/ofgw/mappings.yaml`에서 `notebooklm` provider를 `enabled: true`, `default_mode: mcp`로 고정
- `adapters/ofgw/mappings.yaml`에 community NotebookLM MCP source repo를 기록
- `adapters/ofgw/mappings.yaml`에서 `pull_request.location`을 제품 저장소 URL로 설정
- `adapters/ofgw/mappings.yaml`에서 `repo_markdown.location`을 `agent/`로 설정
- `adapters/ofgw/confirmation-packet.md`를 같은 기준으로 갱신
- `HARNESS_INITIATOR.md`에 Session 20을 추가

핵심 변화:

- NotebookLM에서는 notebook URL만 project-specific confirm 항목으로 남김
- PR location은 `http://192.168.51.106/openframe/openframe7/ofgw`
- markdown 산출물 기본 위치는 제품 루트의 `agent/`

판단:

- provider의 종류와 mode가 안정적으로 정해진 경우에는 location만 남겨 confirm 대상을 줄이는 편이 좋다
- `agent/`를 제품 루트 workspace 디렉토리로 두면 기존 skill들의 하위 문서 구조도 유지하기 쉽다

### 2026-04-21 62. NotebookLM target 확정 및 provider semantics 정리

수정:

- `adapters/ofgw/mappings.yaml`의 `notebooklm.location`을 현재 `ofgw` notebook URL로 채움
- `adapters/ofgw/mappings.yaml`의 confirm 목록에서 NotebookLM location을 제거
- `adapters/ofgw/confirmation-packet.md`에서 NotebookLM unresolved 항목을 제거하고 current target URL을 명시
- `HARNESS_INITIATOR.md`에 provider group semantics 정리 세션을 추가

핵심 변화:

- `review_targets`, `docs_targets`, `issue_sources` 같은 그룹은 "정확히 하나만 true"가 아니라 "동시에 사용 가능한 provider set"으로 본다
- `manual_targets`는 기존 `manual-guide`/patch completion 연동처럼 manual/release workflow에 접근하는 방법을 담는 자리로 정리
- `manual_workflow_required`는 해당 workflow를 제품 기본 completion path에 포함할지 결정하는 상위 정책 플래그로 분리

판단:

- initiator는 요청 유형에 따라 provider를 라우팅해야 하므로, group 내부 provider는 상호배타적일 필요가 없다
- 다만 ambiguous한 생성 결과를 피하려면 각 group에서 우선 provider와 fallback 순서는 계속 명시해야 한다

### 2026-04-21 63. AIM-style manual flow 유지 + generated workspace로 위치 전환

수정:

- `adapters/ofgw/product-profile.yaml` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `adapters/ofgw/confirmation-packet.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- `workflow.defaults.manual_workflow_required`를 `true`로 확정
- `access_bindings.manual_targets.manual_repo.enabled`를 `true`로 확정
- `access_bindings.manual_targets.manual_repo.default_mode`를 `workspace_file`로 확정
- `access_bindings.manual_targets.manual_repo.location`을 `generated/manual/`로 확정
- manual flow는 AIM의 상태 기반 completion semantics를 유지하되, legacy AIM MANUAL repo 대신 generated harness 내부 workspace를 writable target으로 사용한다고 문서화

판단:

- `manual_workflow_required`와 `manual_repo.enabled`는 같은 방향으로 묶는 편이 계약상 더 안전하다
- `workspace_file`은 단순히 제품 repo 어딘가를 뜻하는 것이 아니라, 실제로 생성물이 쓸 수 있는 명시적 파일 경로를 뜻해야 한다
- `generated/manual/`는 AIM의 외부 manual repo 개념을 generated harness 내부로 옮긴 단순화된 첫 구현 위치로 보기 적절하다

### 2026-04-21 64. terminology를 canonical + aliases 구조로 확정

수정:

- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `adapters/ofgw/confirmation-packet.md` 수정

핵심 변화:

- terminology schema를 단일 문자열 대신 `canonical` + `aliases` 구조로 고정
- `issue_item` canonical을 `issue`로, alias를 `ticket`, `jira`, `ims`로 확정
- `review_artifact` canonical을 `PR`로, alias를 `pull request`, `review request`로 확정
- `docs_artifact` canonical을 `markdown document`로, alias를 `doc`, `note`, `report`로 확정
- `mappings.yaml`의 terminology confirm 항목을 제거하고 confirmation packet을 confirmed 상태로 갱신

판단:

- generated harness의 기본 문체와 예시는 `canonical`을 기준으로 맞추는 것이 좋다
- runtime 해석과 사용자 입력 다양성은 `aliases`가 흡수하도록 두는 편이 더 유연하다
- provider 이름과 사람이 읽는 용어를 같은 필드에 섞지 않는 현재 방향이 유지돼야 한다

### 2026-04-21 65. First `generate-harness` pass 실행 및 derived-default 규칙 정리

수정:

- `generated/ofgw-harness/AGENTS.md` 추가
- `generated/ofgw-harness/README.md` 추가
- `generated/ofgw-harness/GENERATION_SUMMARY.md` 추가
- `generated/ofgw-harness/skills/product/issue-analysis/SKILL.md` 추가
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md` 추가
- `generated/ofgw-harness/references/markdown-guide.md` 추가
- `generated/ofgw-harness/generated/manual/README.md` 추가
- `adapters/ofgw/product-profile.yaml` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `adapters/ofgw/confirmation-packet.md` 수정
- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- 첫 `generate-harness` pass로 `generated/ofgw-harness/` 최소 스켈레톤을 실제 생성
- generated draft에서 concrete workspace convention을 명시적으로 materialize
  - `agent/<topic>/`
  - `agent/`
  - `generated/manual/`
- `manual`은 required completion policy로 유지하되, 첫 pass에서는 workspace binding만 생성하고 full `manual-guide` body는 계속 제외
- `workflow.defaults.issue_tracker`, `review_channel`, `docs_channel`은 confirmed provider binding에서 직접 유도되는 derived default로 정리
- `product-profile.yaml`의 workflow confirm 목록을 제거하고 `mappings.yaml`의 confirm을 빈 목록으로 정리

판단:

- generated harness의 첫 실증에서는 "무엇이 제외됐는지 숨기지 않는 것"과 "확정된 binding을 실제 경로로 내리는 것"이 중요하다
- provider binding으로 충분히 결정되는 workflow label까지 별도 generate gate로 유지하면 adapter 인터페이스가 불필요하게 이중화된다
- 따라서 generated pass 이후에는 derived default와 hard gate field를 구분해 주는 편이 initiator 계약을 더 매끄럽게 만든다

### 2026-04-21 66. First generated draft review 반영

수정:

- `generated/ofgw-harness/agent/README.md` 추가
- `generated/ofgw-harness/README.md` 수정
- `generated/ofgw-harness/AGENTS.md` 수정
- `generated/ofgw-harness/GENERATION_SUMMARY.md` 수정
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md` 수정
- `generated/ofgw-harness/skills/product/issue-analysis/SKILL.md` 수정
- `skills/harness-initiator/SKILL.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- `agent/` workspace placeholder를 실제로 추가해 generated path policy와 생성물을 일치시킴
- generated `writing-documents` skill에 source workflow의 hard gate와 write/save 분리 규칙을 복원
- generated `issue-analysis` skill에 NotebookLM target URL과 provider source를 반영
- initiator contract에 "behavior-critical safety semantics 보존" 규칙을 추가

판단:

- generated draft가 source보다 작아도 사용자 안전과 행동 경계를 정하는 규칙은 빠지면 안 된다
- 문서에만 있는 경로 정책은 실제 생성물이 따라오지 않으면 인터페이스 거칠음으로 드러난다
- 따라서 generated artifact review는 생성 품질 검사이자 initiator contract 개선 루프의 일부로 다뤄야 한다

### 2026-04-21 67. `templates/aim/` 물리 이동 실행 및 live layout 전환

수정:

- `templates/README.md` 추가
- `templates/aim/README.md` 추가
- `README.md` 수정
- `AGENTS.md` 수정
- `claude/CLAUDE.md` 수정
- `skills/using-base-harness/SKILL.md` 수정
- `skills/brainstorming/SKILL.md` 수정
- `skills/harness-initiator/SKILL.md` 수정
- `skills/writing-skills/testing-skills-with-subagents.md` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `product-specific/` 하위 AIM 자산 이동

핵심 변화:

- `product-specific/`에 있던 AIM source 자산을 실제로 `templates/aim/` 아래로 옮김
- `templates/`는 더 이상 미래 구조가 아니라 현재 live physical layout으로 전환됨
- `templates/README.md`와 `templates/aim/README.md`를 추가해 source pack 레이어를 문서화
- `ofgw` adapter의 `source_pack` 식별자를 `aim-template`으로 정리
- skill authoring reference의 예시 경로를 현재 실제 위치로 맞춤

판단:

- 이제 initiator의 입력 계약은 개념적으로도 물리적으로도 `templates/<pack>/` 기준으로 읽는 편이 맞다
- `product-specific/` 경로는 history 기록 안에서만 남기고, active 문서/스킬에서 더 이상 기준 경로로 쓰지 않는 것이 혼선을 줄인다
- 이 전환으로 이후 `templates/ofgw/`, `templates/osc/` 같은 추가 pack을 도입할 발판이 생겼다

### 2026-04-21 68. generated target을 standalone harness 방향으로 고정

수정:

- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정
- `README.md` 수정

핵심 변화:

- generated harness에 대해 `current validation pass`와 `long-term standalone target`을 분리해 기술
- 장기 target layout을 `skills/core`, `skills/collab`, `skills/docs`, `skills/review`, `skills/product` 구조로 명시
- first-pass minimal skeleton은 final target이 아니라 validation scaffold라고 재정의

판단:

- 지금까지의 `generated/ofgw-harness/`는 의도적으로 축소된 검증 산출물이라, 그대로 최종 구조로 오해되면 initiator 인터페이스가 잘못 굳는다
- 따라서 생성기의 다음 단계부터는 "무엇을 아직 생성하지 않았는가"를 long-term target에 비춰 평가해야 한다
- 이 기준을 먼저 고정해 두는 편이 이후 core/collab bundling과 review layer 도입 순서를 정리하기 쉽다

### 2026-04-21 69. `templates/aim/` 하위 분리 필요성 점검

수정:

- `templates/aim/README.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- `templates/aim/`를 지금 당장 `skills/`, `bindings/`, `examples/`로 나누지 않기로 결정
- 현재 AIM pack의 binding 정보는 대부분 `issue-analysis`, `writing-documents`, `manual-guide`, review prompt 안의 inline 규칙으로 존재한다고 정리
- example 역시 독립 asset보다 본문 예시나 runtime 외부 참조 비중이 높아 별도 `examples/` 디렉토리 실익이 낮다고 판단

판단:

- 지금 물리 분리를 먼저 하면 디렉토리만 늘고 initiator가 실제로 소비할 안정 스키마는 아직 생기지 않는다
- 따라서 현 단계에서는 얕은 `skills/` + `review/` 구조를 유지하고, inline binding을 adapter draft로 뽑아내는 규칙을 다듬는 편이 낫다
- `bindings/`와 `examples/` 분리는 두 번째 template pack 이상이 생기거나, 반복되는 추출 패턴이 확인된 뒤 도입하는 것이 자연스럽다

### 2026-04-21 70. binding 추출 소스 해석 보정

수정:

- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- initiator의 adapter draft가 codebase-derived facts만으로 만들어지는 것처럼 읽히던 문구를 보정
- `access_bindings.*`는 target codebase, selected template 안의 inherited pattern, 사용자 확인을 함께 써서 초안을 만든다고 명시
- 별도 `templates/<pack>/bindings/` 디렉토리 없이도 현재 `ofgw` draft가 성립한 이유를 문서에 남김

판단:

- 실제 `ofgw` adapter를 보면 build/test/coverage command와 repo facts는 codebase에서 왔지만, IMS URL pattern, NotebookLM/Manual semantics, provider mode 후보는 template 본문과 조직 기본값에서 왔다
- 따라서 "binding은 전부 코드베이스에서 온다"는 해석은 현재 계약과 실제 산출물 모두에 맞지 않는다
- 앞으로는 codebase-derived와 template-inherited를 분리해서 설명해야 initiator 인터페이스가 덜 헷갈린다

### 2026-04-21 71. inline binding inventory와 second-pass 포함 기준 추가

수정:

- `templates/aim/README.md` 수정
- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- `templates/aim`의 source별 inline binding 후보를 실제 draft target과 함께 목록화
- initiator 계약에 `access_bindings`, runtime convention, support reference를 가르는 extraction rule을 추가
- second-pass generate에서 `skills/core`, `skills/collab`, `skills/review`를 포함하는 기준을 문서화

판단:

- 이제 다음 generate pass는 "무엇을 더 넣을까"가 아니라 "어떤 자산이 standalone target에 들어갈 자격이 있나"라는 기준 위에서 진행할 수 있다
- 별도 `bindings/` 디렉토리가 없어도, source pack 안의 inline 규칙만으로 adapter draft를 만드는 경로가 충분히 설명된다
- core/collab/review bundling 기준을 먼저 고정해 두면 `generated/ofgw-harness/` 2차 재생성 범위를 훨씬 선명하게 잡을 수 있다

### 2026-04-21 72. `generated/ofgw-harness/` second-pass 재생성

수정:

- `generated/ofgw-harness/AGENTS.md` 수정
- `generated/ofgw-harness/README.md` 수정
- `generated/ofgw-harness/GENERATION_SUMMARY.md` 수정
- `generated/ofgw-harness/hooks/*` 추가/수정
- `generated/ofgw-harness/skills/core/*` 추가
- `generated/ofgw-harness/skills/collab/*` 추가
- `generated/ofgw-harness/skills/review/code-reviewer/SKILL.md` 추가
- `generated/ofgw-harness/references/review/README.md` 추가
- `generated/ofgw-harness/references/review/aim/*` 추가

핵심 변화:

- standalone target에 맞춰 `core`, `collab`, `review` 레이어를 generated harness 안에 실제로 포함
- base runtime carry-over skill을 generated naming으로 정리해 포함
- `hooks/`를 generated tree 안으로 가져오고 SessionStart hook이 generated `AGENTS.md`를 읽도록 변경
- AIM review prompt/script는 active `ofgw` skill이 아니라 reference-only 자산으로 분리해 포함

판단:

- 이제 `generated/ofgw-harness/`는 "docs/product binding 실험"을 넘어서 standalone target 수렴 여부를 실제로 점검할 수 있는 단계에 들어왔다
- 다만 review 자동화는 아직 AIM 결합이 강하므로, reference-only 계층을 두고 active skill 승격은 다음 판단으로 미루는 편이 안전하다
- 다음 검토는 `references/review/aim/*` 중 어떤 부분을 `ofgw` review workflow로 productize할 수 있는지에 집중하면 된다

### 2026-04-21 73. `review-generated-harness` phase 공식 추가 및 `references/` 장기 역할 보정

수정:

- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- initiator workflow를 `analyze -> draft-adapter -> confirm-gaps -> generate-harness -> review-generated-harness`로 확장
- generated harness 검토 시 확인할 항목을 target layout, active/reference 분류, source path leakage, naming normalization, hook/runtime consistency, excluded-scope reporting으로 고정
- `references/`를 무조건 제거 대상인 임시 디렉토리로 보지 않고, active behavior 밖의 support/example/comparison 자산 계층으로 재정의

판단:

- generated harness 리뷰는 사용자 사용 중에만 드러나는 ergonomics와 별개로, initiator가 반드시 제공해야 하는 post-generate 품질 게이트다
- standalone harness가 완성된 뒤에도 `references/` 자체는 남을 수 있다
- 다만 AIM-locked carry-over 자산은 productized되거나 폐기되기 전까지 과도기적 reference로 취급하는 편이 맞다

### 2026-04-21 74. `generated/ofgw-harness/` 첫 공식 review 실행

수정:

- `generated/ofgw-harness/REVIEW_GENERATED_HARNESS.md` 추가
- `generated/ofgw-harness/hooks/hooks.json` 수정
- `generated/ofgw-harness/skills/core/brainstorming/SKILL.md` 수정
- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- `review-generated-harness` phase의 대표 산출물을 `generated/<product>-harness/REVIEW_GENERATED_HARNESS.md`로 고정
- 현재 `generated/ofgw-harness/`에 대해 target layout, active/reference 분류, source path leakage, hook consistency, excluded-scope reporting을 기준으로 첫 공식 리뷰 실행
- 리뷰 과정에서 `hooks/hooks.json`의 accidental patch-text 오염과 `brainstorming`의 source-pack path leakage를 즉시 수정

판단:

- 현재 draft는 standalone-target harness로서 구조적으로는 유효하다
- 남은 핵심 쟁점은 구조 자체보다 review/manual 자산 중 무엇을 active skill로 승격할지에 가깝다

### 2026-04-21 75. review context 승격 및 local manual workflow 추가

수정:

- `generated/ofgw-harness/skills/review/review-context-collector/SKILL.md` 추가
- `generated/ofgw-harness/skills/docs/manual-workflow/SKILL.md` 추가
- `generated/ofgw-harness/references/manual/README.md` 추가
- `generated/ofgw-harness/skills/review/code-reviewer/SKILL.md` 수정
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md` 수정
- `generated/ofgw-harness/generated/manual/README.md` 수정
- `generated/ofgw-harness/README.md` 수정
- `generated/ofgw-harness/AGENTS.md` 수정
- `generated/ofgw-harness/GENERATION_SUMMARY.md` 수정
- `generated/ofgw-harness/references/review/README.md` 수정
- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- AIM `info-collector`의 재사용 가능한 부분을 `ofgw` binding에 맞는 active `review-context-collector` skill로 승격
- AIM `manual-guide` 전체 body는 복제하지 않고, need gate와 local draft safety semantics만 흡수한 `manual-workflow`를 generated docs layer에 추가
- coverage prompt/script는 저장소 정책과 실행 환경 결합이 강하므로 계속 reference-only로 유지

판단:

- 현재 initiator는 source asset을 통째로 복제하기보다, product-safe semantics만 추출해 active skill로 재구성하는 편이 더 맞다
- review context 수집은 이미 productized 가능한 단계에 도달했지만, coverage automation과 외부 manual publish workflow는 아직 그렇지 않다

### 2026-04-21 76. `references/` 제거 방향 확정 및 `coverage-review` 추가

수정:

- `generated/ofgw-harness/skills/review/coverage-review/SKILL.md` 추가
- `generated/ofgw-harness/skills/review/code-reviewer/SKILL.md` 수정
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md` 수정
- `generated/ofgw-harness/README.md` 수정
- `generated/ofgw-harness/AGENTS.md` 수정
- `generated/ofgw-harness/GENERATION_SUMMARY.md` 수정
- `generated/ofgw-harness/REVIEW_GENERATED_HARNESS.md` 수정
- `generated/ofgw-harness/references/*` 삭제
- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- `ofgw`에 맞는 JaCoCo 기반 active `coverage-review` skill을 추가
- generated standalone harness에서 `references/` 디렉토리를 제거
- `markdown-guide` 규칙은 `writing-documents`로 흡수하고, template/source-only carry-over는 `templates/`에 남기는 방향으로 계약을 보정

판단:

- standalone harness는 runtime bundle처럼 보여야 하므로 `references/` 없는 구조가 더 자연스럽다
- source pack 설명 자산이나 미승격 자산을 generated harness에 들고 있는 것보다 `templates/`에 남겨두는 편이 책임 분리가 선명하다
- coverage review는 이제 active skill이 됐고, 남은 보류 범위는 diff-aware coverage gating과 external manual publish workflow다

### 2026-04-21 77. initiator 책임 경계 재정의

수정:

- `HARNESS_INITIATOR.md` 수정
- `skills/harness-initiator/SKILL.md` 수정

핵심 변화:

- initiator의 핵심 책임을 template scope selection, binding extraction, adapter drafting, generation, generated-structure review로 한정
- generated harness 내부 skill body를 계속 고도화하는 작업은 refinement work로 분리
- 최근 `ofgw` review/manual/coverage skill 구체화는 initiator 검증을 위한 exploratory pass였다고 재분류

판단:

- initiator는 생성기이지 product skill authoring 엔진이 아니다
- 앞으로 검증 포인트는 "무엇을 생성하고 무엇을 남기며 어떤 구조로 정리하는가"에 두는 편이 더 정확하다

### 2026-04-21 78. initiator 검증 기준 문서화

수정:

- `INITIATOR_VALIDATION.md` 추가
- `HARNESS_INITIATOR.md` 수정
- `MIGRATION.md` 수정

핵심 변화:

- complete assembly 정의, initiator/refinement 범위 표, adapter 추가 정보 항목을 문서화
- initiator 입력/출력 체크리스트를 별도 validation 문서에 정리
- `templates/aim` 자산 분류표와 `ofgw` 순수 initiator walkthrough, readiness 평가, second validation target 제안을 함께 정리

판단:

- 이제 initiator 검증은 개별 세션 로그가 아니라 명시적 validation pack 기준으로 볼 수 있다
- `ofgw`는 initiator 계약 실증에는 충분히 가깝지만, machine-readable asset classification이 더 필요하다
- second validation target은 현재 로컬 후보 기준 `osd`가 가장 타당하다

### 2026-04-21 79. `generation_assets` 초안 추가

수정:

- `adapters/ofgw/mappings.yaml` 수정
- `INITIATOR_VALIDATION.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- `generation_assets`를 실제 `mappings.yaml` 필드로 추가
- `generate`, `absorb`, `absorb_partial`, `defer`, `stay_in_templates` action을 `ofgw` adapter 초안에 반영
- source asset 처리 계획은 `product-profile.yaml`보다 `mappings.yaml` 층위에 둔다는 결정을 문서화

판단:

- 이제 `ofgw` adapter는 binding뿐 아니라 source asset 처리 계획까지 일부 machine-readable하게 담는다
- 완전 자동 generation까지 가려면 아직 schema를 더 다듬어야 하지만, initiator 단독 생성 가능성은 한 단계 올라갔다

### 2026-04-21 80. `generation_assets` 스키마 초안 및 `ofgw` 일치 검증

수정:

- `INITIATOR_VALIDATION.md` 수정
- `skills/harness-initiator/SKILL.md` 수정
- `HARNESS_INITIATOR.md` 수정
- `adapters/ofgw/generation-assets-check.md` 추가

핵심 변화:

- `generation_assets`의 minimum shape와 action별 규칙을 문서화
- `ofgw`의 template-derived generated asset이 현재 `generation_assets`와 실제 tree에 맞는지 점검
- base-runtime carry-over는 별도 adapter schema가 아니라 initiator skill 기본 정책으로 해석하는 쪽이 더 낫다는 방향으로 보정

판단:

- `generation_assets`는 template-derived generation 범위를 설명하는 데는 유효하다
- base-runtime carry-over는 지금 단계에서는 별도 machine-readable schema보다 initiator skill 정책으로 유지하는 편이 더 단순하고 적절하다

### 2026-04-21 81. base runtime 기본 carry-over policy와 generation-assets-check 절차 명시

수정:

- `skills/harness-initiator/SKILL.md` 수정
- `INITIATOR_VALIDATION.md` 수정
- `adapters/ofgw/generation-assets-check.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- base runtime carry-over는 adapter schema가 아니라 initiator skill의 기본 generator policy라고 명시
- `generation-assets-check`를 post-generate 표준 검증 절차로 정리
- `ofgw` 검증 문서에 실제 적용 절차를 짧게 추가

판단:

- 이제 generated tree 검증은
  - template-derived 부분은 `generation_assets`
  - base-runtime 부분은 initiator default policy
  로 나눠 해석하면 된다

### 2026-04-21 82. `REVIEW_GENERATED_HARNESS.md`의 non-runtime 성격 명시

수정:

- `skills/harness-initiator/SKILL.md` 수정
- `INITIATOR_VALIDATION.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- `REVIEW_GENERATED_HARNESS.md`를 runtime layer가 아니라 post-generate validation artifact로 명시
- generated tree 안에 존재할 수는 있지만, later generation input이나 adapter truth로 취급하면 안 된다는 점을 문서화

판단:

- generated harness 안의 검증 문서와 runtime asset의 계층을 분리해 두는 것이 이후 재구성과 검증에 더 안전하다

### 2026-04-21 83. `ofgw-harness` 재구성 및 generated naming 정규화

수정:

- `generated/ofgw-harness/*` 재구성
- `adapters/ofgw/generation-assets-check.md` 수정
- `skills/brainstorming/SKILL.md` 수정
- `skills/harness-initiator/SKILL.md` 수정
- `INITIATOR_VALIDATION.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- 백업된 이전 draft와 현재 initiator 계약을 기준으로 `generated/ofgw-harness/`를 clean rebuild
- template-derived asset은 `generation_assets`, base-runtime carry-over는 initiator 기본 정책으로 다시 materialize
- rebuilt tree에서 source `*-base` naming을 standalone runtime naming으로 정규화
- `brainstorming` generated copy에 남아 있던 template source path 누수를 제거
- `REVIEW_GENERATED_HARNESS.md`와 `generation-assets-check.md`를 rebuilt tree 기준으로 갱신

판단:

- 현재 initiator 계약은 `ofgw-harness`를 usable first draft 수준으로 재현할 수 있다
- 다만 carry-over skill의 naming normalization은 generator policy에 더 명시적으로 남겨야 한다
- 이후 initiator 검증은 “재구성 가능성”과 “runtime naming hygiene”를 함께 봐야 한다

### 2026-04-21 84. root `skills/`의 `*-base` postfix 제거

수정:

- `skills/brainstorming/`
- `skills/code-reviewer/`
- `skills/dispatching-parallel-agents/`
- `skills/executing-plans/`
- `skills/finishing-a-development-branch/`
- `skills/receiving-code-review/`
- `skills/requesting-code-review/`
- `skills/subagent-driven-development/`
- `skills/systematic-debugging/`
- `skills/test-driven-development/`
- `skills/using-feature-branches/`
- `skills/verification-before-completion/`
- `skills/writing-plans/`
- `skills/writing-skills/`
- `README.md`
- `skills/using-base-harness/SKILL.md`
- `skills/harness-initiator/SKILL.md`
- `HARNESS_INITIATOR.md`
- `INITIATOR_VALIDATION.md`
- `generated/ofgw-harness/*`

핵심 변화:

- root `skills/` 아래 reusable common skill 디렉토리에서 `-base` postfix를 제거
- source skill frontmatter와 cross-skill reference도 같은 standalone naming으로 정리
- initiator 문서의 default carry-over 정책을 새 root layout 기준으로 보정
- regenerated `ofgw-harness` 검증 문서도 legacy naming이 다시 새어 나오지 않는다는 기준으로 갱신

판단:

- 이제 `skills/`는 source/runtime 공통 레이어로서도 더 자연스러운 naming을 갖는다
- generated harness naming normalization은 여전히 필요하지만, 앞으로는 “legacy `*-base` 누수 방지” 수준으로 더 단순해진다

### 2026-04-21 85. `product-harness-refinement` skill 분리

수정:

- `skills/product-harness-refinement/SKILL.md` 추가
- `skills/using-base-harness/SKILL.md` 수정
- `README.md` 수정
- `INITIATOR_VALIDATION.md` 수정
- `HARNESS_INITIATOR.md` 수정

핵심 변화:

- generated harness 이후의 고도화 작업을 `harness-initiator`에서 분리
- refinement를 "생성기 후속 단계"가 아니라 별도 skill 책임으로 명시
- `using-base-harness` 라우팅에 `product-harness-refinement`를 추가

판단:

- 생성기와 generated harness authoring을 분리하는 편이 경계가 선명하다
- 앞으로 initiator는 generation/classification/review에 집중하고, generated harness 고도화는 별도 skill에서 다루는 편이 확장에 유리하다

### 2026-04-21 86. refinement schema 초안 및 `ofgw` 목적 고정

수정:

- `skills/product-harness-refinement/SKILL.md` 수정
- `INITIATOR_VALIDATION.md` 수정
- `HARNESS_INITIATOR.md` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `adapters/ofgw/analysis-summary.md` 수정

핵심 변화:

- `product-harness-refinement`용 최소 schema로 `refinement_goal`, `refinement_targets` 초안 추가
- `ofgw` refinement의 목적을 "product-harness-refinement skill/schema 검증"으로 고정
- refinement target을 generated runtime asset 기준으로만 적고, initiator scope 재개방과 구분
- `analysis-summary.md`의 stale evidence path를 현재 워크스페이스 경로로 교정

판단:

- `ofgw` 소스코드는 실제로 refinement/adapter 근거로 계속 참조하고 있다
- 다만 그 참조는 generated harness 확장 자체보다 refinement skill과 schema의 유효성 검증에 쓰는 편이 현재 목적에 더 맞다

### 2026-04-21 87. `product-harness-refinement` 첫 적용: `writing-documents`

수정:

- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `skills/product-harness-refinement/SKILL.md` 수정

핵심 변화:

- 첫 refinement target을 `writing-documents`로 선택
- `ofgw` 실제 repo 경계(`ofgwSrc`, `webterminal`, `ofgwAdmin`)를 generated docs skill에 반영
- docs skill이 패키징/릴리스 증거를 과장하지 않도록 safe evidence guidance를 추가
- refinement schema의 `status`, `result_note` 형태를 실제 한 번 사용해 봄

판단:

- 이 라운드의 목적은 `ofgw-harness` 완성도가 아니라 refinement skill/schema 검증이므로, publish adapter 확장 없이 generated docs skill만 좁게 다듬는 접근이 맞다
- `product-harness-refinement`는 generated runtime asset 하나를 선택해 점진적으로 개선하는 방식으로 검증하는 편이 적절하다

### 2026-04-21 88. 두 번째 refinement target: `coverage-review`

수정:

- `generated/ofgw-harness/skills/review/coverage-review/SKILL.md` 수정
- `adapters/ofgw/mappings.yaml` 수정
- `skills/product-harness-refinement/SKILL.md` 수정
- `INITIATOR_VALIDATION.md` 수정

핵심 변화:

- `coverage-review`를 두 번째 refinement target으로 적용
- generated coverage skill에 `ofgwSrc`만 현재 coverage boundary라는 점과 `webterminal`/`ofgwAdmin` 비포함 범위를 명시
- packaging task나 broader build 결과를 coverage evidence처럼 과장하지 않도록 rule을 추가
- refinement schema에 `priority`, `depends_on`를 추가해 실행 순서와 선행관계를 표현

판단:

- refinement schema는 단순 target 목록만으로는 부족하고, 최소한 우선순위와 선행관계가 있으면 더 실용적이다
- `coverage-review` refinement는 `ofgw` 실 repo 근거를 잘 반영하면서도 diff-aware gating 같은 미확정 범위를 다시 열지 않는 선에서 검증됐다
## 89. Cross-Product Refinement Guardrail

- `product-harness-refinement`와 refinement schema가 `ofgw`에 과적합되지 않도록 cross-product guardrail을 명시했다.
- refinement schema에 `portability`를 추가했다:
  - `product_local`
  - `shared_candidate`
- `adapters/ofgw/mappings.yaml`의 refinement targets를 이 기준으로 다시 표시했다.
- `manual-workflow` refinement는 `ofgw` 모듈 지식을 더 넣는 대신, reusable local draft contract를 분명히 하는 방향으로 정리했다.

## 90. Two-Skill Rebuild Evaluation

- `generated/ofgw-harness/`의 refined 상태를 백업한 뒤, initiator-only baseline으로 되돌리고 다시 refinement를 적용했다.
- 목적은 생성기/고도화기 분리가 실제로 유효한지 확인하는 것이었다.
- `product-harness-refinement`와 `INITIATOR_VALIDATION.md`에 refinement pass 평가 기준을 추가했다:
  - baseline 대비 성숙도 상승
  - adapter/schema 복잡도 증가가 정당한지
  - 결과가 `product_local`인지 `shared_candidate`인지
- 평가 결과:
  - 두-skill 분리는 유지 가치가 있다
  - `manual-workflow` local draft contract 강화는 shared candidate에 가깝다
  - 현재 refinement schema는 아직 `mappings.yaml` 안에서 직접 읽을 수 있는 수준이다

## 91. Shared Review Criteria and OSD Draft Adapter

- `review-generated-harness` 기준에 아래 평가 축을 추가했다:
  - maturity gain
  - interface cost
  - portability
- `HARNESS_FLOW_IO.md`를 추가해 두 skill의 입력/출력 경계를 한 장으로 정리했다.
- second validation target인 `osd`에 대해 initiator 범위의 초안을 만들었다:
  - `analysis-summary.md`
  - `product-profile.yaml`
  - `mappings.yaml`
  - `confirmation-packet.md`
- `osd`는 아직 generate 단계로 넘기지 않았다.
  - Jira/NotebookLM/manual policy가 미확정이어서 confirm-gaps가 먼저 필요하다고 판단했다.

## 92. Fill Now Contract

- `harness-initiator`에 `Fill Now` 계약을 추가했다.
- 첫 adapter draft 이후에는 unresolved 값을 prose 안에 숨기지 않고, 사용자가 바로 답할 수 있는 짧은 목록으로 항상 제시한다.
- 각 항목은 다음 정보를 포함한다:
  - field path
  - current draft
  - meaning
  - answer shape
  - recommended value if plausible

## 93. Jira/Auth Path and OSD Default Policy

- Jira MCP binding은 `ofgw`와 같은 형식을 다른 제품 adapter 초안에도 기본 적용 가능하도록 정리했다.
- `auth_source`는 live runtime 기준으로 `agent/info/access.md`가 더 맞다고 판단해 `ofgw` mapping도 수정했다.
- `osd` 초안에서 아래 기본값을 확정했다:
  - Jira enabled = true
  - manual required = true
  - manual enabled = true
  - manual location = generated/manual/
- 이 변경 후 `osd`에서 남은 필수 confirmation은 NotebookLM 여부만 남는다.

## 94. OSD NotebookLM Default Alignment

- `osd`의 NotebookLM binding도 first draft 단계에서는 `ofgw`와 같은 기본값으로 닫았다.
- 목적은 실제 notebook selection보다 binding shape 재현성을 먼저 검증하는 데 있다.
- 이 변경으로 `osd`는 generation 가능한 상태가 됐다.

## 95. OSD First Draft Generation

- `generated/osd-harness/` first draft를 생성했다.
- base runtime carry-over는 `harness-initiator` 기본 정책을 따랐고, product-bound file은 `osd` repo facts에 맞게 다시 작성했다.
- `osd` generated tree 안의 `ofgw` 흔적은 hook/agent/readme/review 문서까지 포함해 정리했다.
- `adapters/osd/generation-assets-check.md`를 추가해 template-derived generation 정합성을 기록했다.

## 96. Draft Default Bias

- `harness-initiator`에 draft default bias를 추가했다.
- 목적은 user 설정을 최소화하면서도 adapter override 가능성을 유지하는 것이다.
- 현재 bias:
  - Jira = `mcp` default
  - manual workspace = `generated/manual/`
- 이 값들은 hardcoded final truth가 아니라 first draft convenience bias로 해석한다.

## 97. OSD Review-Layer Evaluation and Shared `code-reviewer` Fix

- `generated/osd-harness/`를 전반 평가한 결과, 주요 gap은 `osd` 전용 세부 정보 부족이 아니라 generated review layer 내부 연결 부족이었다.
- `review-context-collector`와 `coverage-review`가 생성돼도 carried-over `code-reviewer`가 이를 bound helper로 다루지 않으면 harness는 구조상 맞아도 실제 사용 흐름이 덜 성숙해진다.
- 이 문제는 `osd` adapter나 refinement schema를 더 키우는 것보다 shared `skills/code-reviewer/` 보강으로 푸는 편이 맞다고 판단했다.
- 따라서:
  - shared `skills/code-reviewer/SKILL.md`에 companion review helper 규칙을 추가했다
  - generated `ofgw-harness`, `osd-harness`의 `skills/review/code-reviewer/SKILL.md`도 동기화했다
  - initiator 검증 기준에 review-layer coherence 항목을 추가했다
- 결론:
  - `osd-harness`는 usable first draft로 본다
  - 추가 product-local refinement보다 shared carry-over skill 품질 개선이 먼저였다

## 98. Root Harness Docs Consolidation

- root md 파일이 너무 많아 역할이 겹치는 문제를 정리했다.
- `HARNESS_FLOW_IO.md`, `INITIATOR_VALIDATION.md`는 별도 root 문서 대신 `HARNESS_INITIATOR.md`로 병합했다.
- 병합 후 root 기준 문서는 아래 네 개만 남긴다:
  - `README.md`
  - `AGENTS.md`
  - `MIGRATION.md`
  - `HARNESS_INITIATOR.md`
- 현재 의미 있는 기준선은 `HARNESS_INITIATOR.md`의 `Validation And Flow Summary` 섹션으로 흡수했다.

## 99. Generated Harness Root Docs Consolidation

- generated harness root md도 너무 많아 runtime bundle과 validation artifact가 섞이는 문제가 있었다.
- generated root 기준 문서를 아래 세 개로 고정했다:
  - `README.md`
  - `AGENTS.md`
  - `GENERATION_SUMMARY.md`
- 아래 파일은 generated root에서 제거하고 `adapters/<product>/` 아래로 이동했다:
  - `REVIEW_GENERATED_HARNESS.md`
  - `REFINEMENT_EVALUATION.md`
- 이동 대상:
  - `adapters/ofgw/REVIEW_GENERATED_HARNESS.md`
  - `adapters/ofgw/REFINEMENT_EVALUATION.md`
  - `adapters/osd/REVIEW_GENERATED_HARNESS.md`
  - `adapters/osd/REFINEMENT_EVALUATION.md`
- 해석:
  - generated harness root는 runtime-facing draft만 보여준다.
  - validation/evaluation 문서는 generation/refinement 산출물로 adapter 쪽에 남긴다.
