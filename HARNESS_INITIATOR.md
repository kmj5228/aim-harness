# Harness Initiator

## Purpose

이 문서는 `harness-initiator` 작업 브랜치에서 합의된 현재 방향을 고정한다.
아직 구조 개편이나 스킬 구현은 시작하지 않았고, 우선 결정사항과 짧은 작업 세션 단위를 정리한다.

## Confirmed Decisions

### Naming

- 변환 원본 묶음은 `source-packs/` 대신 `templates/`라는 이름을 사용한다.
- 이 naming은 "재사용 가능한 생성 입력"이라는 의도를 우선한다.

### Generated Output

- 생성된 제품 하네스는 `generated/<product>-harness/` 아래에 둔다.
- 첫 대상 제품은 `ofgw`다.

예시:

```text
generated/
└── ofgw-harness/
```

### Initiator Flow

`harness-initiator`는 한 번에 아래 흐름을 담당한다.

1. `templates/`와 대상 코드베이스를 읽는다.
2. `adapters/<product>/` 초안을 생성한다.
3. 사용자 확인이 필요한 빈칸과 가정을 보고한다.
4. 사용자가 adapter를 확정한 뒤 `generated/<product>-harness/`를 생성한다.

즉, 현재 기준의 기본 흐름은:

```text
templates/aim + target repo
-> harness-initiator
-> adapters/ofgw/product-profile.yaml (draft)
-> adapters/ofgw/mappings.yaml (draft)
-> user confirmation
-> harness-initiator
-> generated/ofgw-harness/
```

### Deliverable Priority

- 1차 핵심 결과물은 `generated/ofgw-harness/` 자체가 아니라 `harness-initiator` 스킬이다.
- `generated/<product>-harness/`는 initiator를 검증하는 첫 실행 대상이자 후속 산출물로 본다.
- 즉 현재 라운드의 우선순위는:
  1. initiator 계약 정리
  2. initiator 스킬 초안 작성
  3. 최소 adapter draft 규칙 정의
  4. 그 다음 실제 제품 하네스 생성 시도

### Adapter Files

- adapter 포맷은 처음부터 세분화하지 않는다.
- 일단 아래 두 파일로 시작한다.
  - `product-profile.yaml`
  - `mappings.yaml`
- 추가 파일은 실제 생성 과정에서 반복적으로 필요한 항목이 확인될 때만 도입한다.

### Scope Control

- 지금 단계에서는 실제 디렉토리 이동이나 구조 개편을 하지 않는다.
- `product-specific/`를 즉시 없애지 않는다.
- `templates/`, `adapters/`, `generated/` 구조는 현재 설계 방향으로만 기록한다.
- `bindings/`나 세부 스키마는 최소 범위로 시작하고, 실제 사용 후 확장한다.

## Working Interpretation

- 현재 `product-specific/` 아래의 AIM 결합 자산은 폐기 대상이 아니라 변환 입력 후보로 본다.
- 다만 지금 바로 물리 이동하지 않고, 먼저 initiator의 입력/출력 계약을 문서로 고정한다.
- 최종 제품 하네스에서는 `product-specific/` 같은 과도기 디렉토리보다 `skills/` 중심 구조를 목표로 한다.
- 그러나 그 목표 구조도 이번 라운드에서는 문서화까지만 하고 실제 적용은 보류한다.

## Micro-Session Plan

각 세션은 약 2~3분 단위로 끊어 진행한다.

### Session 1. Decision Freeze

- 현재 합의사항을 문서에 고정한다.
- naming, 출력 위치, 최초 대상 제품, adapter 흐름을 다시 뒤집지 않도록 기준선을 만든다.

### Session 2. Input Inventory

- 현재 `product-specific/` 아래에서 initiator 입력 후보를 빠르게 목록화한다.
- 어떤 스킬/지원 파일이 변환 대상인지 범위만 정한다.

Result:

| Asset | Current classification | Notes |
|------|------------------------|-------|
| `product-specific/skills/issue-analysis-base/SKILL.md` | First-pass template candidate | verdict 기반 분석 workflow는 재사용 가능. IMS/Jira/NotebookLM/Chrome/dx/path는 binding 후보 |
| `product-specific/skills/writing-documents-base/SKILL.md` | First-pass template candidate | audience -> tone -> structure -> approval skeleton은 재사용 가능. platform guide와 AIM marker 규칙은 분리 필요 |
| `product-specific/skills/writing-documents-base/markdown-guide.md` | Template support reference | 내부 markdown 구조 가이드는 비교적 범용적이라 지원 문서로 유지 가능 |
| `product-specific/skills/completing-patch-base/SKILL.md` | Decompose-before-template | IMS patch verification, HTML editor, manual marker 상태머신이 강하게 결합돼 있어 즉시 템플릿화 비권장 |
| `product-specific/skills/writing-documents-base/manual-guide.md` | Ops-locked reference | AIM manual repo, branch, Antora/AsciiDoc 운영 절차에 강하게 결합 |
| `product-specific/skills/writing-documents-base/{jira,gitlab,ims,confluence,mail}-guide.md` | Product/platform reference set | 개별 platform reference로 보관 가능하지만 초기 initiator의 코어 템플릿 범위에서는 제외 |
| `product-specific/code-reviewer-base/info-collector-prompt.md` | Ops-locked prompt asset | topic naming, IMS/Jira/GitLab/project ID 등 AIM 전제 강함 |
| `product-specific/code-reviewer-base/coverage-analyst-prompt.md` | Ops-locked prompt asset | `rb_73`, `dx`, `gcov`, 80% policy 등 저장소 정책 결합이 강함 |
| `product-specific/code-reviewer-base/scripts/measure_diff_cov.sh` | Legacy support script | 초기 initiator 입력보다는 AIM 예시/레거시 스크립트로 보는 편이 안전 |

Current boundary:

- 초기 `templates/` 후보는 `issue-analysis`, `writing-documents`, `markdown-guide`까지로 제한한다.
- `completing-patch`, `manual-guide`, coverage 관련 자산은 1차 생성 범위에서 제외한다.
- 즉, 첫 `ofgw` 시범 생성은 "분석/문서 허브" 중심으로 시작하고, QA 문서/수동 운영 절차는 뒤로 미룬다.

### Session 3. Core Neutrality Audit

- `skills/*-base`가 실제로 언어/프레임워크/기술 스택과 무관하게 재사용 가능한지 점검한다.
- 핵심 체크는 stack-specific example, artifact path contract, runtime coupling이다.

Result:

| Skill | Classification | Why |
|------|----------------|-----|
| `brainstorming-base` | Core but needs neutralization | `../agent/prompt/<topic>/analysis_report.md`, `design_spec.md` 경로/파일명 계약이 하드코딩 |
| `writing-plans-base` | Core but needs neutralization | `../agent/prompt/<topic>/plan_tasks.md` 경로 고정 + `TypeScript`/`pnpm` 예시 |
| `executing-plans-base` | Core but needs neutralization | `plan_tasks.md` 위치를 고정된 artifact path로 가정 |
| `subagent-driven-development-base` | Core but needs neutralization | `plan_tasks.md` 위치 가정 |
| `test-driven-development-base` | Core but needs neutralization | `ts` 코드 예시가 기본 사례로 들어가 있어 스택 편향 발생 |
| `verification-before-completion-base` | True core | 검증 카테고리 중심으로 서술되어 스택 결합이 낮음 |
| `systematic-debugging-base` | True core | 증거 수집/가설 검증 중심이라 기술 스택 종속성이 낮음 |
| `dispatching-parallel-agents-base` | Mostly core | 예시 경로가 있지만 개념적 workflow는 중립적. 후순위 정리 가능 |
| `code-reviewer-base` | True core | review role과 workflow 중심으로 기술돼 있어 스택 중립적 |
| `requesting-code-review-base` | True core | 저장소/언어 전제보다 review 행위 자체에 집중 |
| `receiving-code-review-base` | True core | feedback triage와 수정 루프가 중심 |
| `using-feature-branches-base` | Workflow-core | 언어/프레임워크와 무관. branch/workspace workflow가 있는 저장소에선 그대로 사용 가능 |
| `finishing-a-development-branch-base` | Workflow-core | review handoff 성격의 workflow. 스택 종속성은 낮음 |
| `using-base-harness` | Intentionally runtime-specific | base-harness 현재 구조와 라우팅을 설명하는 메타 스킬이므로 strict core audit 대상에서 분리 |
| `writing-skills-base` | Intentionally authoring-specific | runtime core보다 skill authoring guide 역할 |

Implications:

- `harness-initiator`보다 먼저 `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `test-driven-development`를 중립화해야 한다.
- `../agent/prompt/<topic>/...` 계약은 core skill의 기본 전제로 두지 말고, runtime 또는 generated harness가 제공하는 artifact convention으로 내려야 한다.
- `TypeScript` + `pnpm` 예시는 pseudocode 또는 stack-neutral 예시로 바꾸는 편이 맞다.

### Session 4. Artifact Contract

- core skill이 직접 filesystem 경로를 아는 구조를 끊는다.
- core는 logical artifact id만 알고, 실제 path는 runtime 또는 generated harness가 제공한다.

Contract:

| Logical artifact | Canonical filename | Purpose |
|------------------|--------------------|---------|
| `analysis_report` | `analysis_report.md` | 선행 분석/triage 결과 |
| `design_spec` | `design_spec.md` | 구현 전 설계 문서 |
| `implementation_plan` | `plan_tasks.md` | 실행 계획 |

Rules:

- core skill은 `../agent/prompt/<topic>/...` 같은 물리 경로를 직접 적지 않는다.
- core skill은 "current runtime artifact workspace" 또는 "artifact directory for the current topic" 같은 논리 표현을 사용한다.
- cross-skill handoff는 path가 아니라 artifact identity로 연결한다.
  - 예: "기존 `analysis_report`가 있으면 재사용"
  - 예: "`design_spec`를 기준으로 `implementation_plan`을 작성"
- runtime 또는 generated harness는 위 logical artifact를 실제 path로 매핑한다.

Transitional mapping for current runtime:

| Logical artifact | Current physical path |
|------------------|-----------------------|
| `analysis_report` | `../agent/prompt/<topic>/analysis_report.md` |
| `design_spec` | `../agent/prompt/<topic>/design_spec.md` |
| `implementation_plan` | `../agent/prompt/<topic>/plan_tasks.md` |

Current decision:

- 이번 라운드에서는 canonical filename은 유지한다.
- 먼저 physical root hardcoding만 제거한다.
- prefix 체계나 추가 artifact 종류는 실제 중립화 edit를 진행하면서 필요할 때만 확장한다.

### Session 5. Initiator Phases

- `harness-initiator` 내부 phase를 짧게 정리한다.
- 최소 기준은 `analyze -> draft adapter -> confirm gaps -> generate harness`다.

Phase contract:

| Phase | Purpose | Main inputs | Main outputs | Stop condition |
|------|---------|-------------|--------------|----------------|
| `analyze` | 대상 repo와 선택된 template 후보에서 재사용 가능한 부분과 binding 후보를 식별 | `templates/<source-pack>` 개념, target repo, selected scope | analysis summary, inferred repo facts, red flags, template applicability notes | 필수 입력이 없거나 대상 repo 특성이 너무 불명확하면 중단 |
| `draft-adapter` | codebase로 추론 가능한 값과 치환 규칙을 adapter 초안으로 구조화 | analyze 결과, target repo facts | `adapters/<product>/product-profile.yaml` draft, `adapters/<product>/mappings.yaml` draft, inferred vs unresolved field list | unresolved field가 많아도 초안은 만들되, 추측으로 확정하지 않음 |
| `confirm-gaps` | 사람 확인이 필요한 값, 정책, 운영 절차를 명시적으로 확인 | adapter draft, unresolved field list, red flags | confirmation report, user decisions, accepted assumptions | 사용자 확인 전에는 generate 단계로 진행하지 않음 |
| `generate-harness` | 확정된 adapter를 적용해 첫 product harness 초안을 생성 | confirmed adapter, selected templates, generated skeleton rules | `generated/<product>-harness/` 초안, generation summary, excluded items list | adapter가 미확정이거나 template boundary가 모호하면 중단 |

Execution rules:

1. `analyze`는 product-specific 전체를 한 번에 변환하려 하지 않는다.
   - 현재 기준의 입력 범위는 `issue-analysis`, `writing-documents`, `markdown-guide` 중심이다.
2. `draft-adapter`는 codebase-derived 값과 human-confirmed 값의 경계를 유지한다.
   - 모르면 `TODO` 또는 explicit gap으로 남긴다.
3. `confirm-gaps`는 질문을 줄이기 위해 unresolved item을 묶어서 보여준다.
   - issue tracker
   - review channel
   - docs channel
   - manual/release workflow 필요 여부
4. `generate-harness`는 생성 결과와 제외 결과를 함께 보고한다.
   - 생성된 skill
   - 제외된 skill/reference
   - 아직 분해되지 않은 ops-locked asset

Minimal per-phase artifacts:

| Phase | Artifact or report |
|------|---------------------|
| `analyze` | analysis summary in working notes or generation summary draft |
| `draft-adapter` | `product-profile.yaml` draft, `mappings.yaml` draft |
| `confirm-gaps` | confirmation checklist or unresolved-items report |
| `generate-harness` | `generated/<product>-harness/` + generation summary |

Non-goals for first run:

- source pack backfill
- automatic restructuring of every product-specific skill
- manual-guide / patch-completion generation
- direct in-place rewrite of live source assets

### Session 6. Initiator Skill Draft

- `harness-initiator` 자체의 `SKILL.md` 초안을 만든다.
- focus는 trigger, workflow, phase gate, expected outputs다.
- 이 단계에서는 실제 생성 결과보다 "어떻게 작동해야 하는가"를 먼저 고정한다.

### Session 7. Adapter Draft Contract

- `product-profile.yaml`, `mappings.yaml`에 어떤 필드가 반드시 들어가야 하는지 최소 셋을 잡는다.
- 코드베이스로 채울 값과 사람 확인이 필요한 값을 구분한다.

Contract goal:

- `product-profile.yaml`은 대상 저장소의 실행 사실, safety note, runtime hint를 담는다.
- `mappings.yaml`은 source template를 대상 제품에서 실제로 어떻게 접근하고 실행할지에 대한 binding을 담는다.
- 초안 단계에서는 inferred 값과 unresolved 값을 섞지 않는다.
- 같은 조직/팀 계열에서는 workflow label보다 access/integration binding이 우선 확인 대상일 수 있다.

### `product-profile.yaml`

Minimum shape:

```yaml
product:
  name: <product-name>

repo:
  build_systems:
    - <build-system>
  primary_languages:
    - <language>
  modules:
    - <module-or-subproject>
  test_frameworks:
    - <framework>
  coverage_tool: <tool-or-null>
  commands:
    build: <command-or-null>
    test: <command-or-null>
    coverage: <command-or-null>

workflow:
  defaults:
    issue_tracker: <system-or-null>
    review_channel: <channel-or-null>
    docs_channel: <channel-or-null>
    manual_workflow_required: <bool-or-null>

confirm:
  - workflow.defaults.issue_tracker
  - workflow.defaults.review_channel
  - workflow.defaults.docs_channel
  - workflow.defaults.manual_workflow_required
```

Field rule:

- `repo.*`는 codebase-derived facts 위주다.
- `workflow.defaults.*`는 fallback 또는 조직 기본값 레이어다.
- auto-commit task, destructive packaging step 같은 값은 `notes`로 남긴다.
- `confirm`에는 아직 확정되지 않은 필드만 남긴다.

### `mappings.yaml`

Minimum shape:

```yaml
source_pack: <source-pack-name>
target_product: <product-name>

terminology:
  issue_item: <target-term-or-null>
  review_artifact: <target-term-or-null>
  docs_artifact: <target-term-or-null>

command_bindings:
  project_build_command: <command-or-null>
  project_test_command: <command-or-null>
  project_coverage_command: <command-or-null>

access_bindings:
  issue_sources:
    jira:
      enabled: <bool-or-null>
      default_mode: <mcp-or-browser-or-api-or-null>
      fallback_modes:
        - <mode>
      location: <url-path-or-null>
    ims:
      enabled: <bool-or-null>
      default_mode: <browser-or-null>
      fallback_modes:
        - <mode>
      location: <url-path-or-null>
  spec_sources:
    notebooklm:
      enabled: <bool-or-null>
      default_mode: <mcp-or-browser-or-manual-or-null>
      fallback_modes:
        - <mode>
      location: <notebook-id-or-url-or-null>
  review_targets:
    pull_request:
      enabled: <bool-or-null>
      default_mode: <browser-or-git-or-mcp-or-null>
      fallback_modes:
        - <mode>
      location: <url-pattern-or-null>
    merge_request:
      enabled: <bool-or-null>
      default_mode: <browser-or-mcp-or-null>
      fallback_modes:
        - <mode>
      location: <url-pattern-or-null>
  docs_targets:
    repo_markdown:
      enabled: <bool-or-null>
      default_mode: <workspace_file-or-null>
      fallback_modes:
        - <mode>
      location: <repo-path-or-null>
    confluence:
      enabled: <bool-or-null>
      default_mode: <browser-or-api-or-null>
      fallback_modes:
        - <mode>
      location: <url-or-null>
  manual_targets:
    manual_repo:
      enabled: <bool-or-null>
      default_mode: <workspace_file-or-browser-or-null>
      fallback_modes:
        - <mode>
      location: <repo-path-or-url-or-null>

confirm:
  - terminology.issue_item
  - terminology.review_artifact
  - terminology.docs_artifact
  - access_bindings.issue_sources.jira.enabled
  - access_bindings.issue_sources.jira.default_mode
  - access_bindings.issue_sources.jira.location
  - access_bindings.issue_sources.ims.enabled
  - access_bindings.issue_sources.ims.location
  - access_bindings.spec_sources.notebooklm.enabled
  - access_bindings.spec_sources.notebooklm.default_mode
  - access_bindings.spec_sources.notebooklm.location
  - access_bindings.review_targets.pull_request.enabled
  - access_bindings.review_targets.pull_request.default_mode
  - access_bindings.review_targets.pull_request.location
  - access_bindings.docs_targets.repo_markdown.enabled
  - access_bindings.docs_targets.repo_markdown.location
  - access_bindings.manual_targets.manual_repo.enabled
  - access_bindings.manual_targets.manual_repo.default_mode
  - access_bindings.manual_targets.manual_repo.location
```

Field rule:

- `command_bindings.*`는 가능하면 codebase에서 채운다.
- `terminology.*`는 표현 레이어라서 중요하지만 1순위 confirm 대상은 아니다.
- `access_bindings.*`는 provider registry처럼 정의한다.
- 같은 시스템 이름을 쓰더라도 `enabled`, `default_mode`, `fallback`, `location`이 다르면 별도 binding으로 본다.
- 사용자 요청이 `jira`, `ims`, `manual`, `spec` 중 무엇을 가리키는지에 따라 해당 provider를 선택한다.

### Inferred vs Human-Confirmed

| Category | Default owner | Examples |
|---------|----------------|----------|
| build systems | inferred | `gradle`, `pnpm` |
| languages | inferred | `java`, `kotlin`, `javascript` |
| test frameworks | inferred | `junit5`, `mockito` |
| coverage tool | inferred | `jacoco` |
| build/test/coverage command | inferred first, then user correction if needed | `./gradlew :ofgwSrc:test` |
| workflow defaults | human-confirmed fallback | `jira`, `pull_request`, `repo_markdown` |
| terminology | human-confirmed when wording matters | `issue`, `MR`, `analysis note` |
| provider registry | human-confirmed | `jira`, `ims`, `notebooklm`, `pull_request`, `repo_markdown`, `manual_repo` |
| provider mode/location | human-confirmed | `mcp`, `browser`, `workspace_file`, URL, repo path |

### OFGW Draft Example

The current `ofgw` repository suggests this first-pass draft:

```yaml
product:
  name: ofgw

repo:
  build_systems:
    - gradle
    - pnpm
  primary_languages:
    - java
    - kotlin
    - javascript
  modules:
    - ofgwSrc
    - webterminal
    - ofgwAdmin
  test_frameworks:
    - junit5
    - mockito
  coverage_tool: jacoco
  commands:
    build: ./gradlew build
    test: ./gradlew :ofgwSrc:test
    coverage: ./gradlew :ofgwSrc:jacocoTestReport

workflow:
  issue_tracker: null
  review_channel: null
  docs_channel: null
  manual_workflow_required: null

confirm:
  - workflow.issue_tracker
  - workflow.review_channel
  - workflow.docs_channel
  - workflow.manual_workflow_required
```

Why this is enough for now:

- initiator의 첫 실행은 완벽한 schema보다 "추론 가능한 값과 확인이 필요한 값을 명확히 분리"하는 것이 더 중요하다.
- 실제 생성을 해보면서 반복적으로 필요한 필드가 드러나면 그때 schema를 확장한다.

### Session 8. Template Boundary

- 현재 자산에서 본문, 용어 치환점, 예시, 운영 절차를 어떻게 나눌지 기준만 만든다.
- 실제 이동은 하지 않는다.

Boundary rule:

- template 본문은 product workflow skeleton만 남긴다.
- product/tool/channel-specific 값은 binding 또는 reference로 내린다.
- 사람 승인, verdict branching, document structure 같은 반복 가능한 규칙은 template 본문에 남긴다.
- mixed-stack target repo(`ofgw` 같은 예외 사례)는 adapter 초안의 입력일 뿐, template body를 특정 스택에 맞게 다시 쓰는 근거가 되지 않는다.

### `issue-analysis` boundary

Keep in template body:

- analyze first, act second 원칙
- context gathering -> symptom 이해 -> code trace -> spec/reference 확인 -> verdict 결정
- verdict categories 자체
  - bug
  - expected behavior
  - configuration error
  - unsupported feature
- `analysis_report` artifact 구조
- verdict별 downstream handoff 개념

Move to bindings or product config:

- IMS / Jira 같은 issue system 이름
- NotebookLM / 특정 spec source
- Chrome automation 사용 여부
- Jira REST API / auth 방식
- repo root path, `dx` 명령, concrete code trace command
- IMS response / Jira feature request 같은 구체 채널 이름

Move to reference/example:

- URL 패턴
- example API call
- example report text with product-specific labels

### `writing-documents` boundary

Keep in template body:

- audience -> tone -> structure -> review 순서
- 두괄식, 다이어그램 우선, approval gate
- "작성"과 "저장/발송" 분리 규칙
- 독자별 추상화 수준 표
- 사용자 승인 전 발송 금지

Move to bindings or product config:

- Jira / Confluence / IMS / GitLab / Mail 같은 채널 이름
- greeting convention이 조직별 강제 규칙인지 여부
- 어떤 docs channel이 실제 기본 채널인지
- manual workflow 자동 호출 여부
- MR marker / HTML comment 상태 공유 규칙

Move to reference/example:

- `jira-guide.md`
- `gitlab-guide.md`
- `ims-guide.md`
- `confluence-guide.md`
- `mail-guide.md`
- `manual-guide.md`

### `markdown-guide` boundary

Keep in template body or shared reference:

- `analysis_report`, `design_spec`, `implementation_plan` artifact 구조
- 두괄식, 다이어그램, 목차 기준
- 문서 타입별 기본 섹션 틀

Treat as transitional reference, not core template body:

- canonical filename 설명
- prefix 관습
- product-specific field labels (`IMS`, `Jira`, `XSP`)가 들어간 example text

Current decision:

- 첫 initiator는 `issue-analysis`, `writing-documents`를 main template 후보로 본다.
- `markdown-guide`는 shared support reference에 더 가깝게 다룬다.
- `ofgw`에서 보이는 Java/Kotlin/JS 사실은 adapter draft에만 반영하고, template body는 C 계열 제품에도 그대로 적용될 수준으로 유지한다.

### Session 9. Confirmation Loop

- adapter 초안을 사용자에게 어떤 형식으로 보여주고 무엇을 확인받을지 정한다.
- 비어 있는 값, 가정, red flag 보고 형식을 함께 정한다.

Loop goal:

- unresolved field를 흩어진 질문으로 던지지 않고, 작은 묶음으로 확인한다.
- 사용자가 확정한 값, 보류한 값, 아직 모르는 값을 분리 기록한다.
- 이 단계가 끝나면 `generate-harness`가 바로 읽을 수 있는 confirmed adapter 상태가 되어야 한다.

### Confirmation Packet

`confirm-gaps`는 아래 4개 블록으로 보고한다.

1. **Inferred Facts**
   - 코드베이스에서 추론한 값
   - 사용자가 바꾸지 않으면 그대로 adapter에 반영
2. **Needs Confirmation**
   - 운영 정책/채널/용어처럼 사람 확인이 필요한 값
3. **Red Flags**
   - template 적용 범위가 애매하거나 ops-locked asset이 남아 있는 경우
4. **Proposed Next Step**
   - 확인 후 바로 생성 가능한지, 아니면 추가 분해가 필요한지

### Confirmation Report Format

```markdown
# Adapter Confirmation: <product>

## Inferred Facts
- build_systems: gradle, pnpm
- primary_languages: java, kotlin, javascript
- test_frameworks: junit5, mockito
- coverage_tool: jacoco

## Needs Confirmation
- workflow.issue_tracker: ?
- workflow.review_channel: ?
- workflow.docs_channel: ?
- workflow.manual_workflow_required: ?
- terminology.issue_item: ?
- terminology.review_artifact: ?
- terminology.docs_artifact: ?

## Red Flags
- `completing-patch` is still excluded from first-run generation
- `manual-guide` remains ops-locked

## Proposed Next Step
- Confirm the unresolved workflow and terminology values
- Then generate the first `ofgw-harness` draft from the selected templates
```

### Grouping Rule

질문은 field 단위가 아니라 아래 묶음 단위로 보여준다.

| Group | Typical fields |
|------|----------------|
| workflow core | `workflow.issue_tracker`, `workflow.review_channel`, `workflow.docs_channel` |
| release/manual policy | `workflow.manual_workflow_required`, `workflow_bindings.completion_workflow` |
| terminology | `terminology.issue_item`, `terminology.review_artifact`, `terminology.docs_artifact` |

### Resolution States

각 unresolved 항목은 아래 중 하나로만 처리한다.

- `confirmed`
- `deferred`
- `unknown`

Rule:

- `confirmed`: adapter에 값 반영
- `deferred`: 생성은 진행 가능하지만 후속 검토 대상으로 generation summary에 남김
- `unknown`: generate-harness 진행 금지

### Post-Confirmation Update Rule

확인 루프가 끝나면 initiator는:

1. `confirm` 목록에서 `confirmed` 항목 제거
2. `deferred` 항목은 generation summary의 follow-up 목록으로 이동
3. `unknown` 항목이 남아 있으면 generate 단계로 가지 않음

### OFGW Example Grouping

For the first `ofgw` run, the expected grouped questions are:

- workflow core
  - 이슈 시스템은 무엇인가
  - 리뷰 채널은 무엇인가
  - 기본 문서 채널은 무엇인가
- release/manual policy
  - 매뉴얼 또는 release verification workflow가 필수인가
- terminology
  - issue item을 무엇이라 부르는가
  - review artifact를 무엇이라 부르는가
  - docs artifact를 무엇이라 부르는가

### Session 10. First Validation Target

- `generated/ofgw-harness/`는 세부 설계 대상이 아니라 initiator 검증 대상으로 다룬다.
- 즉 "무엇을 얼마나 생성해 보면 initiator가 유효하다고 판단할 수 있는가"를 정한다.

Validation target for the first `ofgw` run:

- 목표는 완성된 `ofgw-harness`를 만드는 것이 아니라, `harness-initiator`가 계약된 흐름을 끝까지 유지하는지 검증하는 것이다.
- 따라서 첫 pass는 full product-pack generation이 아니라 `selected templates -> adapter draft -> confirmation packet -> minimal generated draft`가 성립하는지에 집중한다.

Pass criteria:

1. `analyze` 결과가 아래를 분리 보고한다.
   - selected templates
   - inferred repo facts
   - excluded or ops-locked assets
   - mixed-stack red flags
2. `draft-adapter`가 아래 두 파일의 초안을 만든다.
   - `product-profile.yaml`
   - `mappings.yaml`
3. `confirm-gaps`가 아래 4블록 보고를 만든다.
   - `Inferred Facts`
   - `Needs Confirmation`
   - `Red Flags`
   - `Proposed Next Step`
4. 사용자 확인 뒤 `generate-harness`가 최소 generated draft를 만든다.
   - root-level harness draft metadata
   - selected template 범위에 해당하는 generated skill draft
   - excluded items summary

Selected template scope for the first validation pass:

- `issue-analysis`
- `writing-documents`
- `markdown-guide` reference carry-over only

Non-goals:

- `completing-patch`까지 생성하는 것
- manual/release workflow를 product-specific detail까지 확정하는 것
- `ofgw` mixed-stack fact를 기준으로 template body를 재작성하는 것
- production-ready `generated/ofgw-harness/` 구조를 한 번에 완성하는 것

Failure signals:

- unresolved `unknown` 값이 남아 있는데도 generation을 진행함
- excluded asset을 summary 없이 조용히 누락함
- generated draft가 selected template scope 밖의 asset까지 암묵적으로 포함함
- `ofgw` repo facts를 template body 규칙으로 승격시켜 버림

Current interpretation:

- 첫 validation pass 통과는 `harness-initiator`가 1차 적용 가능 수준이라는 뜻이다.
- 이 단계에서는 generated harness의 완성도보다, initiator가 생성 범위와 제외 범위를 얼마나 명확히 관리하는지가 더 중요하다.

### Session 11. Generated Harness Skeleton

- `generated/ofgw-harness/`에 어떤 루트 파일과 어떤 `skills/` 하위 구조가 필요한지 최소 골격만 정의한다.
- 이 세션은 initiator 검증에 꼭 필요한 범위까지만 다룬다.

Minimal skeleton for the first validation pass:

```text
generated/ofgw-harness/
├── AGENTS.md
├── README.md
├── GENERATION_SUMMARY.md
├── skills/
│   ├── docs/
│   │   └── writing-documents/
│   └── product/
│       └── issue-analysis/
└── references/
    └── markdown-guide.md
```

Role of each item:

- `AGENTS.md`
  - generated harness의 현재 scope와 사용 규칙을 짧게 설명한다
- `README.md`
  - 이 초안이 first validation draft라는 점과 포함/제외 범위를 요약한다
- `GENERATION_SUMMARY.md`
  - 무엇을 생성했고 무엇을 의도적으로 제외했는지 기록한다
- `skills/docs/writing-documents/`
  - selected template scope에서 생성된 문서 workflow 스킬 초안
- `skills/product/issue-analysis/`
  - selected template scope에서 생성된 분석 workflow 스킬 초안
- `references/markdown-guide.md`
  - main template body가 아니라 shared support reference로 carry-over 한다

Explicitly out of scope for this skeleton:

- `hooks/`
- `profiles/`
- `skills/core/`
- `skills/collab/`
- `skills/review/`
- `completing-patch` 또는 manual/release workflow 디렉토리

Reason:

- 위 자산들은 장기적으로 필요할 수 있지만, 첫 validation pass에서는 initiator의 template selection / exclusion reporting / minimal generation 능력을 확인하는 데 필수는 아니다.
- 따라서 첫 skeleton은 "생성기 검증에 필요한 최소 산출물"만 포함한다.

### Session 12. First Build Readiness

- 위 결정이 모이면 첫 `ofgw` 시범 생성에 필요한 최소 조건이 갖춰졌는지 점검한다.
- 부족한 항목만 다음 라운드 액션으로 남긴다.

Readiness result:

- `analyze`: ready
- `draft-adapter`: ready
- `confirm-gaps`: ready
- `generate-harness`: not ready until the first confirmation packet is actually resolved

Ready now:

- initiator skill draft exists
- first-pass template scope is fixed
- template boundary is fixed
- adapter minimum schema is fixed
- confirmation packet shape is fixed
- first validation target is fixed
- minimal generated skeleton is fixed

Still required before the first actual `ofgw` run:

1. collect one concrete `ofgw` analysis snapshot
   - selected templates
   - inferred repo facts
   - explicit excluded assets
2. write the first adapter draft content
   - `product-profile.yaml`
   - `mappings.yaml`
3. assemble the first confirmation packet
   - grouped unresolved workflow values
   - grouped terminology values
   - red flags
4. wait for user confirmation on unresolved values
5. only then attempt `generate-harness`

Current go/no-go judgment:

- go for `analyze`
- go for `draft-adapter`
- go for `confirm-gaps`
- no-go for `generate-harness` before confirmed adapter state exists

Reason:

- 현재 부족한 것은 구조 정의가 아니라 첫 실제 adapter draft와 confirmation state다.
- 즉 다음 라운드의 핵심은 설계를 더 늘리는 것이 아니라, 지금까지 고정한 계약으로 첫 `ofgw` draft를 실제로 만들어 보는 것이다.

### Session 13. First Adapter Draft Packet

- 첫 실제 `ofgw` adapter draft를 문서 메모가 아니라 concrete file set으로 만든다.
- 이 세션의 출력은 `analyze`, `draft-adapter`, `confirm-gaps`를 한 번에 보여주는 첫 packet이다.

Expected draft artifacts:

- `adapters/ofgw/analysis-summary.md`
- `adapters/ofgw/product-profile.yaml`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`

### Session 14. Confirmation Candidate Narrowing

- unresolved 값을 바로 확정하지 않고, repository evidence 기반의 추천 후보만 좁힌다.
- 이 세션의 출력은 사용자 확인을 쉽게 만드는 suggested defaults이며, adapter 확정 자체는 아니다.

### Session 15. Access Binding Contract Reframe

- adapter 확인 우선순위를 workflow label보다 access/integration binding으로 다시 잡는다.
- 이 세션의 목표는 "무슨 시스템을 쓰는가"보다 "그 시스템에 어떻게 접근하는가"를 먼저 모델링하는 것이다.

### Session 16. OFGW Draft Rewrite For Access Bindings

- `ofgw` adapter draft를 새 계약에 맞게 다시 쓴다.
- 이 세션의 목표는 기존 workflow-centered draft를 access-binding-centered draft로 바꾸는 것이다.

### Session 17. Mode Naming Cleanup

- access binding의 `repo` mode를 `workspace_file`로 바꾼다.
- 이 세션의 목표는 Git repository와 workspace file access를 명확히 구분하는 것이다.

### Session 18. Provider Registry Reframe

- `access_bindings`를 flat access block이 아니라 provider registry로 다시 잡는다.
- 이 세션의 목표는 사용자 요청이 어떤 대상(`jira`, `ims`, `notebooklm`, `manual`)을 가리키든 그에 맞는 provider 정의를 선택할 수 있게 만드는 것이다.

### Session 19. Jira/IMS Provider Defaults Refinement

- `jira` provider의 default mode와 setup requirement를 더 구체화한다.
- `ims` provider는 기존 `issue-analysis` 스킬의 URL pattern과 browser flow를 기본값으로 유지한다.

### Session 20. NotebookLM/PR/Workspace Defaults Freeze

- `NotebookLM`, `pull_request`, `repo_markdown` provider의 기본 location과 mode를 사용자 입력으로 고정한다.
- 이 세션의 목표는 generate 전에 꼭 필요한 provider location 값을 줄이는 것이다.

## Deferred For Now

- 실제 `templates/` 디렉토리 생성
- `product-specific/` 물리 이동
- `adapters/ofgw/` 파일 생성
- `generated/ofgw-harness/` 생성
- 세부 `bindings/` 스키마 확장

## Session Log

### 2026-04-20 Session 2. Input Inventory

Reviewed:

- `product-specific/skills/issue-analysis-base/SKILL.md`
- `product-specific/skills/completing-patch-base/SKILL.md`
- `product-specific/skills/writing-documents-base/SKILL.md`
- `product-specific/skills/writing-documents-base/manual-guide.md`
- `product-specific/skills/writing-documents-base/markdown-guide.md`
- `product-specific/code-reviewer-base/info-collector-prompt.md`
- `product-specific/code-reviewer-base/coverage-analyst-prompt.md`

Decision:

- initiator 1차 입력 범위는 product workflow 전체가 아니라, 먼저 템플릿화 가능한 자산으로 제한한다.
- `issue-analysis`와 `writing-documents`는 템플릿 후보로 유지한다.
- `completing-patch`와 manual/coverage 자산은 운영 절차 결합이 강하므로 분해 전까지 제외한다.

### 2026-04-20 Session 3. Core Neutrality Audit

Reviewed:

- `skills/brainstorming-base/SKILL.md`
- `skills/writing-plans-base/SKILL.md`
- `skills/executing-plans-base/SKILL.md`
- `skills/subagent-driven-development-base/SKILL.md`
- `skills/test-driven-development-base/SKILL.md`
- `skills/verification-before-completion-base/SKILL.md`
- `skills/systematic-debugging-base/SKILL.md`
- `skills/dispatching-parallel-agents-base/SKILL.md`
- `skills/code-reviewer-base/SKILL.md`
- `skills/using-base-harness/SKILL.md`

Findings:

- 현재 가장 큰 중립성 문제는 `../agent/prompt/<topic>/...` 형태의 산출물 경로 계약이다.
- 그 다음은 `writing-plans-base`, `test-driven-development-base`의 `TypeScript`/`pnpm` 예시 편향이다.
- 반면 review/debug/verification 계열은 기술 스택이 바뀌어도 거의 그대로 재사용 가능하다.

Decision:

- initiator phase 설계 전에 core skill neutralization을 선행 항목으로 둔다.
- artifact path 계약과 stack-specific example은 base layer에서 정리한다.

### 2026-04-20 Session 4. Artifact Contract

Reviewed:

- `skills/brainstorming-base/SKILL.md`
- `skills/writing-plans-base/SKILL.md`
- `skills/executing-plans-base/SKILL.md`
- `skills/subagent-driven-development-base/SKILL.md`
- `product-specific/skills/writing-documents-base/markdown-guide.md`

Decision:

- core skill은 logical artifact id만 참조하고, 실제 physical path는 runtime이 제공한다.
- 우선 `analysis_report`, `design_spec`, `implementation_plan` 세 artifact만 contract에 포함한다.
- 현재 runtime의 `../agent/prompt/<topic>/...` 경로는 transitional mapping으로만 문서화하고, core skill 본문 규칙으로는 유지하지 않는다.

### 2026-04-20 Session 5. Core Skill Neutralization

Edited:

- `skills/brainstorming-base/SKILL.md`
- `skills/writing-plans-base/SKILL.md`
- `skills/executing-plans-base/SKILL.md`
- `skills/subagent-driven-development-base/SKILL.md`
- `skills/test-driven-development-base/SKILL.md`

Changes:

- `brainstorming-base`의 `analysis_report` / `design_spec` 참조를 logical artifact 표현으로 변경
- `writing-plans-base`의 `implementation_plan` 저장/전달 표현을 artifact contract 기준으로 변경
- `executing-plans-base`, `subagent-driven-development-base`의 plan loading 규칙을 physical path 대신 artifact 참조로 변경
- `writing-plans-base`, `test-driven-development-base`의 `TypeScript`/`pnpm` 예시를 stack-neutral pseudocode로 교체

Verification:

- `rg`로 대상 5개 스킬에서 `../agent/prompt` 직접 경로 참조가 제거됐는지 확인
- `rg`로 `pnpm`, `TypeScript`, `buildResult`, `validateQueueName` 같은 예시 편향이 제거됐는지 확인

Remaining notes:

- canonical filename(`design_spec.md`, `plan_tasks.md`)은 transitional mapping 설명으로만 남겨둔다
- 다른 base skill과 product-specific 문서에는 후속 정리가 남아 있다

### 2026-04-20 Session 6. Meta And Guide Alignment

Reviewed:

- `skills/using-base-harness/SKILL.md`
- `product-specific/skills/writing-documents-base/markdown-guide.md`
- `skills/dispatching-parallel-agents-base/SKILL.md`
- `skills/systematic-debugging-base/SKILL.md`

Changes:

- `using-base-harness`에 현재 `product-specific` 구조가 transitional layout임을 명시
- `using-base-harness`에 `templates/`, `adapters/`, `generated/` 방향과 logical artifact convention을 추가
- `markdown-guide`의 산출물 규칙을 fixed physical path에서 artifact contract 중심 표현으로 변경
- `dispatching-parallel-agents-base`, `systematic-debugging-base`는 현재 기준으로 추가 중립화 없이 유지 가능하다고 확인

Verification:

- `rg`로 `using-base-harness`와 `markdown-guide`의 남은 path hardcoding 위치를 재확인
- 관찰: 남은 direct path hardcoding은 product-specific 문서군 내부 범위로 축소됨

### 2026-04-20 Session 7. Initiator Phase Contract

Decision:

- `harness-initiator`의 1차 실행 계약은 `analyze -> draft-adapter -> confirm-gaps -> generate-harness`로 고정한다.
- 각 phase는 입력, 출력, stop condition을 갖는다.
- `confirm-gaps`는 필수 사용자 확인 게이트이며, 이를 통과하기 전에는 harness 생성으로 넘어가지 않는다.

Why this shape:

- `analyze` 없이 바로 adapter를 쓰면 템플릿 적용 범위와 codebase-derived 사실이 섞인다.
- `draft-adapter`와 `confirm-gaps`를 분리해야 추정값과 확정값을 구분할 수 있다.
- `generate-harness`는 confirmed adapter만 입력으로 받아야 한다.

### 2026-04-20 Session 8. Priority Reset

Decision:

- 현재 라운드의 1차 결과물은 `generated/ofgw-harness/`가 아니라 `harness-initiator` 스킬로 본다.
- `generated/<product>-harness/`는 initiator를 시험하는 validation target으로 후순위에 둔다.
- 따라서 세션 순서를 initiator 계약/스킬 초안/adapter 규칙 우선으로 재정렬한다.

Updated order:

1. Artifact contract
2. Initiator phase contract
3. Initiator skill draft
4. Adapter draft contract
5. Template boundary
6. Confirmation loop
7. Validation target definition
8. Generated harness skeleton
9. First build readiness

### 2026-04-20 Session 9. Initiator Skill Draft

Edited:

- `skills/harness-initiator/SKILL.md`

Changes:

- `harness-initiator` 스킬 초안을 실제 skill 파일로 추가
- trigger, first-run scope, phase workflow, output contract, common mistakes를 포함
- 현재 라운드의 우선순위에 맞게 "스킬 자체가 1차 결과물"이라는 점을 본문에 명시

Related routing updates:

- `skills/using-base-harness/SKILL.md`
- `AGENTS.md`
- `README.md`

Decision:

- 이제 initiator 논의는 개념 메모만이 아니라 실제 discoverable skill 초안으로 전환됐다
- 다음 단계는 이 스킬이 기대하는 adapter draft contract를 구체화하는 것이다

### 2026-04-20 Session 10. Adapter Draft Contract

Decision:

- adapter 초안은 `product-profile.yaml`과 `mappings.yaml` 두 파일로 시작한다.
- `product-profile.yaml`은 repo facts + workflow confirmation fields를 담는다.
- `mappings.yaml`은 source template의 terminology / command / workflow 대응을 담는다.

Current `ofgw`-derived facts captured:

- `gradle` + `pnpm`
- `java`, `kotlin`, `javascript`
- modules: `ofgwSrc`, `webterminal`, `ofgwAdmin`
- `junit5`, `mockito`, `jacoco`

Rule:

- build/test/coverage facts는 먼저 codebase에서 채운다.
- issue tracker, review channel, docs channel, manual workflow는 사용자 확인 전까지 `confirm` 목록에 남긴다.

### 2026-04-20 Session 12. Confirmation Loop

Decision:

- `confirm-gaps`는 `Inferred Facts / Needs Confirmation / Red Flags / Proposed Next Step` 4블록으로 보고한다.
- 질문은 field 단위가 아니라 workflow core / release-manual policy / terminology 묶음으로 보여준다.
- unresolved 항목의 상태는 `confirmed`, `deferred`, `unknown` 셋 중 하나로만 관리한다.

Gate rule:

- `confirmed`는 adapter에 반영
- `deferred`는 generation summary 후속 항목으로 이동
- `unknown`이 남아 있으면 generate 단계로 가지 않는다

### 2026-04-20 Session 11. Template Boundary

Decision:

- `issue-analysis`와 `writing-documents`는 main template 후보로 유지한다.
- `markdown-guide`는 main template body보다는 shared support reference로 다룬다.

Boundary summary:

- reusable workflow skeleton은 template body에 남긴다
- 채널/도구/인증/URL/명령/조직 정책은 binding 또는 reference로 내린다
- mixed-stack repo인 `ofgw`의 사실은 adapter draft에만 반영하고, template body는 C 기반 OF 모듈에도 적용 가능한 수준으로 유지한다

### 2026-04-20 Session 13. First Adapter Draft Packet

Edited:

- `adapters/ofgw/analysis-summary.md`
- `adapters/ofgw/product-profile.yaml`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`

Captured:

- selected templates: `issue-analysis`, `writing-documents`, `markdown-guide`
- inferred repo facts: `gradle`, `pnpm`, `java`, `kotlin`, `javascript`, `ofgwSrc`, `webterminal`, `ofgwAdmin`, `junit5`, `mockito`, `jacoco`
- safety note: root packaging tasks can mutate version files and create git commits
- unresolved workflow and terminology values grouped for confirmation

Decision:

- 첫 실제 initiator run은 문서 설계 연장이 아니라 concrete adapter draft packet을 남겨야 한다
- `ofgw` mixed-stack 사실은 adapter draft에만 반영하고, issue tracker / review channel / docs channel / terminology는 여전히 사람 확인 전까지 미확정으로 유지한다

### 2026-04-20 Session 14. Confirmation Candidate Narrowing

Edited:

- `adapters/ofgw/confirmation-packet.md`

Captured:

- suggested default for `workflow.issue_tracker`: `jira`
- suggested default for `workflow.review_channel`: `pull_request`
- low-confidence suggestion for `workflow.docs_channel`: `repo_markdown`
- `workflow.manual_workflow_required` remains unresolved

Evidence:

- root `ofgw/AGENTS.md` contains a Jira query guardrail and example issue key `OFV7-1234`
- `ofgwAdmin/AGENTS.md` documents PR expectations
- repository docs exist in markdown, but no strong Confluence/wiki signal was found

Decision:

- repository evidence can narrow candidate values, but it is not strong enough to auto-confirm workflow bindings
- suggested defaults belong in the confirmation packet, while the adapter files remain unconfirmed until user review

### 2026-04-20 Session 16. OFGW draft를 access binding 기준으로 재작성

Edited:

- `adapters/ofgw/product-profile.yaml`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`

Changes:

- `product-profile.yaml`의 `workflow`를 `workflow.defaults` 구조로 변경
- `mappings.yaml`의 `workflow_bindings`를 `access_bindings` 구조로 교체
- `confirmation-packet.md`의 unresolved 질문을 workflow label보다 access binding 중심으로 재배치

Current interpretation:

- `jira`, `pull_request`, `repo_markdown`은 현재 단계에서 provisional default일 뿐이고, 실제 생성 게이트는 `mode`와 `location` 확인에 있다
- `notebook_access`와 `manual_access`는 repository evidence가 부족하므로 계속 unresolved로 유지한다

### 2026-04-21 Session 17. `repo` mode를 `workspace_file`로 정리

Edited:

- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `MIGRATION.md`

Changes:

- access mode 이름 `repo`를 `workspace_file`로 변경
- `repo_markdown` 같은 시스템 라벨은 유지
- Git repository 자체와 file access mode를 구분하도록 용어를 정리

Decision:

- `repo`는 mode 이름으로 두면 Git 저장소 자체와 혼동되기 쉽다
- 파일 직접 접근 방식은 `workspace_file`로 부르는 편이 schema 의미가 더 분명하다

### 2026-04-21 Session 18. Provider registry 기준으로 재정의

Edited:

- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `MIGRATION.md`

Changes:

- `access_bindings`를 `issue_sources`, `spec_sources`, `review_targets`, `docs_targets`, `manual_targets` 구조로 재정의
- `jira`, `ims`, `notebooklm`, `pull_request`, `repo_markdown`, `manual_repo`를 provider entry로 취급
- 확인 항목을 provider별 `enabled/default_mode/fallback/location` 기준으로 재배치

Decision:

- initiator는 특정 시스템 하나를 고정하는 도구보다, 요청 대상별 provider를 고르는 라우터에 가까워야 한다
- 따라서 product adaptation의 핵심은 "무슨 시스템을 쓴다"보다 "어떤 provider set을 열어두고 어떤 mode로 접근하느냐"에 있다

### 2026-04-21 Session 19. Jira/IMS provider 기본값 구체화

Edited:

- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `HARNESS_INITIATOR.md`
- `MIGRATION.md`

Changes:

- `jira` provider를 `mcp` 기본 + `api` fallback 구조로 구체화
- `jira.location` 기본값을 `atlassian-rovo`로 두고 MCP bootstrap 절차를 기록
- `ims.enabled` 기본값을 `true`로 바꾸고 URL pattern을 기존 `issue-analysis` 스킬 기준으로 채움
- confirmation packet에 Jira MCP setup requirement와 REST API fallback requirement를 명시

Decision:

- initiator는 단순히 `jira`라는 이름만 넣는 것이 아니라, MCP bootstrap이 필요하다는 점까지 사용자에게 알려야 한다
- `ims`는 현재 inherited workflow가 분명하므로 provider location을 기본값으로 채운 상태에서 가져가는 편이 맞다

### 2026-04-21 Session 20. NotebookLM/PR/workspace 기본값 고정

Edited:

- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `HARNESS_INITIATOR.md`
- `MIGRATION.md`

Changes:

- `notebooklm` provider를 `enabled: true`, `default_mode: mcp`로 고정
- NotebookLM default provider를 `https://github.com/jacob-bd/notebooklm-mcp-cli` 기반 community MCP로 기록
- `pull_request.location`을 `http://192.168.51.106/openframe/openframe7/ofgw`로 고정
- `repo_markdown.location`을 제품 루트의 `agent/`로 고정
- confirm 목록에서 NotebookLM enabled/default_mode, PR location, repo_markdown location을 제거

Decision:

- NotebookLM은 provider 종류보다 notebook URL만 project-specific 값으로 남기는 것이 맞다
- review target은 제품 Git repository URL을 location으로 두고, markdown 산출물은 제품 루트 `agent/` 아래로 모으는 편이 현재 스킬 구조와 가장 잘 맞는다

### 2026-04-21 Session 21. NotebookLM target 확정 및 provider semantics 정리

Edited:

- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `HARNESS_INITIATOR.md`
- `MIGRATION.md`

Changes:

- `access_bindings.spec_sources.notebooklm.location`을 현재 `ofgw` 대상 notebook URL로 확정
- confirm 목록에서 NotebookLM location 항목 제거
- confirmation packet에서 NotebookLM unresolved 항목을 제거하고 current target을 명시
- provider group의 `enabled`는 상호배타 선택이 아니라 "사용 가능한 provider 집합"이라는 해석을 문서 메모로 고정

Decision:

- `review_targets`, `docs_targets`, `issue_sources` 하위에는 여러 provider가 동시에 `enabled: true`일 수 있다
- generate 시점의 핵심은 "어떤 provider들이 열려 있나"와 "요청이 들어왔을 때 어떤 provider를 우선 선택하나"이지, 그룹마다 반드시 하나만 true인 것은 아니다
- `manual_targets`는 기존 `manual-guide` / patch completion 연동 같은 release/manual workflow를 provider로 분리해 담는 자리이고, `manual_workflow_required`는 그 workflow 자체를 기본 completion path에 포함할지 정하는 상위 플래그다
