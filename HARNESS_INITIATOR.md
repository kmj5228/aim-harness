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
- 장기 목표 산출물은 standalone product harness다.
- 현재의 최소 생성본은 이 장기 목표를 검증하기 위한 중간 패스다.

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

### Responsibility Boundary

- `harness-initiator`의 책임:
  - template scope selection
  - binding extraction rule 정의
  - adapter draft 생성
  - unresolved gap confirmation
  - 첫 generated harness 생성
  - generated harness의 구조/분류 검증
  - source asset을 `active skill`, `defer`, `stay in templates`로 분류
- `harness-initiator`의 책임 밖:
  - generated harness 내부 skill body를 계속 고도화하는 일
  - 제품 운영에 맞춘 review/manual/coverage semantics의 장기 개선
  - standalone harness를 실제로 사용하면서 생기는 wording/ergonomics 조정

현재 `generated/ofgw-harness/`에서 진행한 review/manual/coverage skill 구체화는 initiator 검증을 위한 exploratory pass로는 의미가 있었지만, 앞으로는 generated harness refinement work로 보는 편이 맞다.

### Default Carry-Over Policy

- base runtime skill 번들링은 현재 adapter가 아니라 `harness-initiator` skill의 기본 generator policy로 둔다.
- 즉 `skills/core/*`, `skills/collab/*`, base `code-reviewer`는 product별 `generation_assets`가 아니라 initiator 기본 규칙으로 포함될 수 있다.
- `generation_assets`는 template-derived 자산 처리 계획만 설명한다.

### Validation Pack

- initiator 검증 기준과 flow I/O 요약은 이 문서 안에 직접 유지한다.
- root에는 별도 validation/io 문서를 늘리지 않는다.
- current validation은 아래 질문에 답할 수 있어야 한다.
  - standalone first draft를 재현 가능하게 만들었는가
  - initiator와 refinement 경계가 흐려지지 않았는가
  - generated harness가 source/template leakage 없이 self-contained한가
  - shared skill 문제를 product-local schema 증가 없이 식별할 수 있는가

### Adapter Files

- adapter 포맷은 처음부터 세분화하지 않는다.
- 일단 아래 두 파일로 시작한다.
  - `product-profile.yaml`
  - `mappings.yaml`
- 추가 파일은 실제 생성 과정에서 반복적으로 필요한 항목이 확인될 때만 도입한다.
- source asset 처리 계획(`generation_assets`)은 `mappings.yaml`에 둔다.
- `generation_assets` action은 현재 아래 다섯 개로 제한한다.
  - `generate`
  - `absorb`
  - `absorb_partial`
  - `defer`
  - `stay_in_templates`

### Scope Control

- `templates/`, `adapters/`, `generated/` 구조를 실제 physical layout으로 사용한다.
- `bindings/`나 세부 스키마는 최소 범위로 시작하고, 실제 사용 후 확장한다.

## Validation And Flow Summary

### Complete Assembly

`완전 구성`은 아래 조건을 만족하는 usable first draft를 뜻한다.

1. `templates/<pack>/`와 `adapters/<product>/`만으로 standalone product harness 기본 tree를 생성할 수 있다.
2. generated tree가 runtime 관점에서 self-contained하다.
3. generated tree 안에 `templates/`, `adapters/`, comparison 자료 같은 생성기 내부 자산이 남지 않는다.
4. 필수 runtime layer가 존재한다.
5. 각 layer가 최소한의 usable skill body와 binding을 가진다.
6. `review-generated-harness`를 통과한다.

필수 runtime layer:

- root docs:
  - `AGENTS.md`
  - `README.md`
  - `GENERATION_SUMMARY.md`
- runtime:
  - `hooks/`
  - `agent/`
  - `generated/manual/`
- skills:
  - `skills/core/`
  - `skills/collab/`
  - `skills/docs/`
  - `skills/review/`
  - `skills/product/`

주의:

- `완전 구성`은 최종 polished harness를 뜻하지 않는다.
- wording, ergonomics, 운영 세부조정은 refinement에 남을 수 있다.
- `REVIEW_GENERATED_HARNESS.md`는 validation artifact이지 runtime asset이 아니다.
- generated harness root md는 runtime-facing 문서만 유지한다:
  - `README.md`
  - `AGENTS.md`
  - `GENERATION_SUMMARY.md`
- validation/evaluation 문서는 `adapters/<product>/` 아래에 둔다.

### Initiator vs Refinement

| 구분 | initiator | refinement |
|------|-----------|------------|
| template 선택/범위 | 담당 | 비대상 |
| binding 추출/adapter draft | 담당 | 비대상 |
| confirm gaps | 담당 | 비대상 |
| standalone tree 생성 | 담당 | 비대상 |
| source asset 분류 | 담당 | 비대상 |
| generated harness 구조 검증 | 담당 | 비대상 |
| generated skill body 고도화 | 최소 viable draft까지만 | 담당 |
| wording/ergonomics 개선 | 최소 범위만 | 담당 |
| product-local semantics 강화 | 비대상 | 담당 |

추가 규칙:

- generated `skills/review/` 안에 `review-context-collector`, `coverage-review`가 포함되면 `code-reviewer`도 이를 bound helper로 인식해야 한다.
- 이런 review-layer coherence는 product-local refinement보다 shared carry-over 품질 문제에 가깝다.

### Flow I/O

#### Harness Initiator

질문:

- 무엇을 생성해야 하는가
- 어떤 template 자산을 흡수/보류/유지해야 하는가
- 어떤 binding이 제품 truth인가

대표 입력:

- `templates/<pack>/`
- target repo
- `adapters/<product>/product-profile.yaml`
- `adapters/<product>/mappings.yaml`
- unresolved confirmation 결과

대표 출력:

- `generated/<product>-harness/`
- `GENERATION_SUMMARY.md`
- `adapters/<product>/REVIEW_GENERATED_HARNESS.md`
- 첫 adapter draft 직후의 `Fill Now` 목록
- generation-phase fix/defer 판단

#### Product Harness Refinement

질문:

- 이미 생성된 harness를 어떻게 더 usable하게 만들 것인가
- 이 개선이 product-local correction인가, shared pattern 후보인가
- 개선 대비 adapter/schema 비용이 과한가

대표 입력:

- `generated/<product>-harness/`
- adapter의 `refinement_goal`, `refinement_targets`
- target repo evidence
- generated review findings

대표 출력:

- refined generated runtime assets
- `adapters/<product>/REFINEMENT_EVALUATION.md` 같은 refinement 평가 문서
- product-local vs shared-candidate 판단

### Validation Checklist

Inputs:

- selected template pack exists
- target repo is inspectable
- `product-profile.yaml` draft exists
- `mappings.yaml` draft exists
- required unresolved values are no longer `unknown`

Outputs:

- analysis summary exists
- adapter drafts exist
- confirmation packet exists
- `Fill Now` list exists after the first adapter draft
- generated harness tree exists
- generated harness review report exists

Pass conditions:

- selected template scope was respected
- excluded scope was reported explicitly
- bindings were materialized into runtime paths
- generated tree matches the current target layout
- generated carry-over skills use standalone naming
- generated review layer is internally coherent when companion review skills exist
- generated tree contains no template-internal carry-over directory

## Working Interpretation

- 현재 AIM 결합 자산은 `templates/aim/` source pack으로 본다.
- `harness-initiator`는 `templates/<pack>/`를 입력으로 읽고 `generated/<product>-harness/`를 생성한다.
- 최종 제품 하네스에서는 `product-specific/` 같은 과도기 디렉토리 없이 `skills/` 중심 구조를 목표로 한다.
- 따라서 현재 `generated/ofgw-harness/`는 final shape 자체가 아니라, final shape로 가는 생성 규칙 검증본으로 해석한다.

## Generated Target Model

### Long-Term Product Harness

장기적으로 `generated/<product>-harness/`는 아래와 같은 standalone layout을 목표로 한다.

```text
generated/<product>-harness/
├── AGENTS.md
├── README.md
├── hooks/
├── skills/
│   ├── core/
│   ├── collab/
│   ├── docs/
│   ├── review/
│   └── product/
└── generated/
    └── manual/
```

핵심 원칙:

- `skills/core/`에는 base runtime에서 재사용 가능한 코어 루프를 배치한다.
- `skills/collab/`에는 branch, review, handoff 같은 협업 스킬을 배치한다.
- `skills/docs/`, `skills/review/`, `skills/product/`에는 pack + adapter로부터 생성된 product-bound layer를 배치한다.
- runtime에 필요한 support guidance는 해당 skill이나 root doc로 흡수한다.
- `templates/`, `adapters/` 같은 생성기 내부 디렉토리는 final generated harness 안에 남지 않는다.
- `REVIEW_GENERATED_HARNESS.md`는 generated tree 안에 둘 수 있지만 runtime asset이 아니라 validation artifact로 본다.
- generated carry-over skill은 standalone runtime 이름을 유지하고 legacy `*-base` naming을 다시 드러내지 않는다.
- generated harness 이후의 고도화는 `harness-initiator`보다 별도 `product-harness-refinement` skill로 분리하는 편이 적절하다.
- `ofgw-harness`를 기반으로 후속 개선을 하더라도, 그 목적이 `product-harness-refinement`와 refinement schema 검증인지 제품 완성도 상승인지 먼저 고정해야 한다.

### Current Validation Pass

현재 `ofgw`에 대해 만들어진 최소 생성본은 위 장기 목표를 바로 다 채우지 않는다.

- 목적은 template selection, exclusion reporting, binding materialization, safety semantics preservation을 먼저 검증하는 것이다.
- 따라서 first pass는 `docs`, `product`, workspace placeholder 중심으로 시작한다.
- 다음 generate pass부터는 `skills/core/`, `skills/collab/`, `skills/review/`를 포함하는 standalone target으로 수렴시킨다.

## Micro-Session Plan

각 세션은 약 2~3분 단위로 끊어 진행한다.

### Session 1. Decision Freeze

- 현재 합의사항을 문서에 고정한다.
- naming, 출력 위치, 최초 대상 제품, adapter 흐름을 다시 뒤집지 않도록 기준선을 만든다.

### Session 2. Input Inventory

- 현재 `templates/aim/` 아래에서 initiator 입력 후보를 빠르게 목록화한다.
- 어떤 스킬/지원 파일이 변환 대상인지 범위만 정한다.

Result:

| Asset | Current classification | Notes |
|------|------------------------|-------|
| `templates/aim/skills/issue-analysis/SKILL.md` | First-pass template candidate | verdict 기반 분석 workflow는 재사용 가능. IMS/Jira/NotebookLM/Chrome/dx/path는 binding 후보 |
| `templates/aim/skills/writing-documents/SKILL.md` | First-pass template candidate | audience -> tone -> structure -> approval skeleton은 재사용 가능. platform guide와 AIM marker 규칙은 분리 필요 |
| `templates/aim/skills/writing-documents/markdown-guide.md` | Template support reference | 내부 markdown 구조 가이드는 비교적 범용적이라 지원 문서로 유지 가능 |
| `templates/aim/skills/completing-patch/SKILL.md` | Decompose-before-template | IMS patch verification, HTML editor, manual marker 상태머신이 강하게 결합돼 있어 즉시 템플릿화 비권장 |
| `templates/aim/skills/writing-documents/manual-guide.md` | Ops-locked reference | AIM manual repo, branch, Antora/AsciiDoc 운영 절차에 강하게 결합 |
| `templates/aim/skills/writing-documents/{jira,gitlab,ims,confluence,mail}-guide.md` | Product/platform reference set | 개별 platform reference로 보관 가능하지만 초기 initiator의 코어 템플릿 범위에서는 제외 |
| `templates/aim/review/code-reviewer/info-collector-prompt.md` | Ops-locked prompt asset | topic naming, IMS/Jira/GitLab/project ID 등 AIM 전제 강함 |
| `templates/aim/review/code-reviewer/coverage-analyst-prompt.md` | Ops-locked prompt asset | `rb_73`, `dx`, `gcov`, 80% policy 등 저장소 정책 결합이 강함 |
| `templates/aim/review/code-reviewer/measure_diff_cov.sh` | Legacy support script | 초기 initiator 입력보다는 AIM 예시/레거시 스크립트로 보는 편이 안전 |

Current boundary:

- 초기 `templates/` 후보는 `issue-analysis`, `writing-documents`, `markdown-guide`까지로 제한한다.
- `completing-patch`, `manual-guide`, coverage 관련 자산은 1차 생성 범위에서 제외한다.
- 즉, 첫 `ofgw` 시범 생성은 "분석/문서 허브" 중심으로 시작하고, QA 문서/수동 운영 절차는 뒤로 미룬다.
- 다만 이후 pass에서는 `manual-guide`의 전체 body가 아니라 need gate와 draft-first safety semantics만 흡수한 local `manual-workflow`를 별도 generated skill로 만들 수 있다.

### Session 3. Core Neutrality Audit

- root `skills/`의 reusable common skill이 실제로 언어/프레임워크/기술 스택과 무관하게 재사용 가능한지 점검한다.
- 핵심 체크는 stack-specific example, artifact path contract, runtime coupling이다.

Result:

| Skill | Classification | Why |
|------|----------------|-----|
| `brainstorming` | Core but needs neutralization | `../agent/prompt/<topic>/analysis_report.md`, `design_spec.md` 경로/파일명 계약이 하드코딩 |
| `writing-plans` | Core but needs neutralization | `../agent/prompt/<topic>/plan_tasks.md` 경로 고정 + `TypeScript`/`pnpm` 예시 |
| `executing-plans` | Core but needs neutralization | `plan_tasks.md` 위치를 고정된 artifact path로 가정 |
| `subagent-driven-development` | Core but needs neutralization | `plan_tasks.md` 위치 가정 |
| `test-driven-development` | Core but needs neutralization | `ts` 코드 예시가 기본 사례로 들어가 있어 스택 편향 발생 |
| `verification-before-completion` | True core | 검증 카테고리 중심으로 서술되어 스택 결합이 낮음 |
| `systematic-debugging` | True core | 증거 수집/가설 검증 중심이라 기술 스택 종속성이 낮음 |
| `dispatching-parallel-agents` | Mostly core | 예시 경로가 있지만 개념적 workflow는 중립적. 후순위 정리 가능 |
| `code-reviewer` | True core | review role과 workflow 중심으로 기술돼 있어 스택 중립적 |
| `requesting-code-review` | True core | 저장소/언어 전제보다 review 행위 자체에 집중 |
| `receiving-code-review` | True core | feedback triage와 수정 루프가 중심 |
| `using-feature-branches` | Workflow-core | 언어/프레임워크와 무관. branch/workspace workflow가 있는 저장소에선 그대로 사용 가능 |
| `finishing-a-development-branch` | Workflow-core | review handoff 성격의 workflow. 스택 종속성은 낮음 |
| `using-base-harness` | Intentionally runtime-specific | base-harness 현재 구조와 라우팅을 설명하는 메타 스킬이므로 strict core audit 대상에서 분리 |
| `writing-skills` | Intentionally authoring-specific | runtime core보다 skill authoring guide 역할 |

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
- 최소 기준은 `analyze -> draft adapter -> confirm gaps -> generate harness -> review-generated-harness`다.

Phase contract:

| Phase | Purpose | Main inputs | Main outputs | Stop condition |
|------|---------|-------------|--------------|----------------|
| `analyze` | 대상 repo와 선택된 template 후보에서 재사용 가능한 부분과 binding 후보를 식별 | `templates/<source-pack>` 개념, target repo, selected scope | analysis summary, inferred repo facts, red flags, template applicability notes | 필수 입력이 없거나 대상 repo 특성이 너무 불명확하면 중단 |
| `draft-adapter` | codebase-derived 사실과 template-inherited binding 후보를 adapter 초안으로 구조화 | analyze 결과, target repo facts, inherited template patterns | `adapters/<product>/product-profile.yaml` draft, `adapters/<product>/mappings.yaml` draft, inferred vs unresolved field list | unresolved field가 많아도 초안은 만들되, 추측으로 확정하지 않음 |
| `confirm-gaps` | 사람 확인이 필요한 값, 정책, 운영 절차를 명시적으로 확인 | adapter draft, unresolved field list, red flags | confirmation report, user decisions, accepted assumptions | 사용자 확인 전에는 generate 단계로 진행하지 않음 |
| `generate-harness` | 확정된 adapter를 적용해 첫 product harness 초안을 생성 | confirmed adapter, selected templates, generated skeleton rules | `generated/<product>-harness/` 초안, generation summary, excluded items list | adapter가 미확정이거나 template boundary가 모호하면 중단 |
| `review-generated-harness` | 생성 결과를 standalone harness 관점에서 검토하고 구조/분류 오류를 잡음 | generated harness draft, generation summary, target layout rules | generated-harness review notes, required fixes, confirmed deferred scope | 생성 결과에 source path 누수나 active/reference 분류 오류가 남아 있으면 완료로 보지 않음 |

Execution rules:

1. `analyze`는 선택된 template pack 전체를 한 번에 변환하려 하지 않는다.
   - 현재 기준의 입력 범위는 `issue-analysis`, `writing-documents`, `markdown-guide` 중심이다.
2. `draft-adapter`는 codebase-derived 값과 human-confirmed 값의 경계를 유지한다.
   - 모르면 `TODO` 또는 explicit gap으로 남긴다.
   - 다만 `access_bindings.*`는 codebase만으로 채우는 것이 아니라, template에서 상속된 access pattern을 suggested default로 가져올 수 있다.
   - org-level 공통 패턴이 이미 검증된 경우, 초안 단계에서는:
     - Jira = `mcp` default
     - manual workspace = `generated/manual/`
     를 default bias로 둘 수 있다.
3. `confirm-gaps`는 질문을 줄이기 위해 unresolved item을 묶어서 보여준다.
   - issue tracker
   - review channel
   - docs channel
   - manual/release workflow 필요 여부
   - 그리고 첫 adapter draft 직후에는 항상 `Fill Now` 목록으로 구체적인 field path, 현재 draft, 답 형식을 같이 제시한다.
4. `generate-harness`는 생성 결과와 제외 결과를 함께 보고한다.
   - 생성된 skill
   - 제외된 skill/reference
   - 아직 분해되지 않은 ops-locked asset
   - 이미 확정된 binding이 가리키는 concrete workspace path (`agent/`, `generated/manual/` 등)
5. `review-generated-harness`는 생성 결과를 후속 사용 관점에서 한 번 더 검토한다.
   - target layout conformity
   - active skill vs reference-only classification
   - source-pack path leakage
   - naming normalization
   - hook/runtime consistency
   - review-layer coherence when companion review skills exist
   - excluded scope reporting
   - maturity gain vs initiator-only baseline when available
   - interface cost of any attached refinement schema
   - portability of observed refinement results

Minimal per-phase artifacts:

| Phase | Artifact or report |
|------|---------------------|
| `analyze` | analysis summary in working notes or generation summary draft |
| `draft-adapter` | `product-profile.yaml` draft, `mappings.yaml` draft |
| `confirm-gaps` | confirmation checklist or unresolved-items report |
| `generate-harness` | `generated/<product>-harness/` + generation summary |
| `review-generated-harness` | `adapters/<product>/REVIEW_GENERATED_HARNESS.md` + fix/defer decisions |

Non-goals for first run:

- source pack backfill
- automatic restructuring of every template-pack asset
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
  issue_item:
    canonical: <target-term-or-null>
    aliases:
      - <alternate-term>
  review_artifact:
    canonical: <target-term-or-null>
    aliases:
      - <alternate-term>
  docs_artifact:
    canonical: <target-term-or-null>
    aliases:
      - <alternate-term>

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
  - terminology.issue_item.canonical
  - terminology.review_artifact.canonical
  - terminology.docs_artifact.canonical
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
- `terminology.*.canonical`은 generated harness의 기본 표현을 정한다.
- `terminology.*.aliases`는 추가 표현과 입력 해석을 위해 유지하되, 초기 생성의 hard gate로 보지 않는다.
- `workflow.defaults.*`가 confirmed provider binding에서 직접 유도될 수 있으면, 별도 confirm gate로 남기지 않고 derived default로 본다.
- generated skill은 source skill의 behavior-critical safety semantics를 보존해야 한다.
- `access_bindings.*`는 provider registry처럼 정의한다.
- `access_bindings.*`의 초안은 보통 세 입력을 섞어 만든다:
  - target repo/codebase에서 읽은 사실
  - selected template 안에 들어 있는 inherited access pattern
  - 사용자 또는 조직 기본값 확인
- 같은 시스템 이름을 쓰더라도 `enabled`, `default_mode`, `fallback`, `location`이 다르면 별도 binding으로 본다.
- 사용자 요청이 `jira`, `ims`, `manual`, `spec` 중 무엇을 가리키는지에 따라 해당 provider를 선택한다.

Inline extraction rule:

- `templates/<pack>/bindings/`가 아직 없어도 initiator는 selected template 본문에서 binding 후보를 뽑아야 한다.
- 우선 추출 대상:
  - URL pattern
  - repo path
  - notebook target
  - access mode 제약 (`mcp`, `browser`, `api`, `workspace_file`)
  - workflow marker / completion semantics
- 구분 규칙:
  - provider routing에 영향을 주면 `access_bindings.*`
  - generated workspace path와 artifact materialization에 영향을 주면 runtime convention
  - 표현 예시나 긴 본문은 support reference 또는 excluded asset

### Inferred vs Human-Confirmed

| Category | Default owner | Examples |
|---------|----------------|----------|
| build systems | inferred | `gradle`, `pnpm` |
| languages | inferred | `java`, `kotlin`, `javascript` |
| test frameworks | inferred | `junit5`, `mockito` |
| coverage tool | inferred | `jacoco` |
| build/test/coverage command | inferred first, then user correction if needed | `./gradlew :ofgwSrc:test` |
| workflow defaults | human-confirmed fallback | `jira`, `pull_request`, `repo_markdown` |
| terminology | human-confirmed when wording matters | `issue` + aliases, `pull request` + aliases |
| provider registry | template-inherited candidate + human confirmation | `jira`, `ims`, `notebooklm`, `pull_request`, `repo_markdown`, `manual_repo` |
| provider mode/location | template-inherited candidate + repo signal + human confirmation | `mcp`, `browser`, `workspace_file`, URL, repo path |

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

### Inline Binding Extraction Map

현재 `templates/aim/`에서는 아래처럼 본문 안의 규칙을 추출 대상으로 본다.

| Source asset | Inline candidate | Draft target |
|------|-------------------|-------------|
| `skills/issue-analysis/SKILL.md` | IMS URL pattern | `access_bindings.issue_sources.ims.location` |
| `skills/issue-analysis/SKILL.md` | Jira API/MCP semantics | `access_bindings.issue_sources.jira.*` |
| `skills/issue-analysis/SKILL.md` | NotebookLM / spec lookup requirement | `access_bindings.spec_sources.notebooklm.*` |
| `skills/writing-documents/SKILL.md` + `markdown-guide.md` | markdown workspace convention | `access_bindings.docs_targets.repo_markdown.*` |
| `skills/writing-documents/manual-guide.md` | manual repo path / mode / workflow semantics | `workflow.defaults.manual_workflow_required`, `access_bindings.manual_targets.manual_repo.*` |
| `skills/writing-documents/gitlab-guide.md` | MR target/API pattern | `access_bindings.review_targets.*` candidate |
| `review/code-reviewer/info-collector-prompt.md` | review system and project access assumptions | review-target candidate or excluded review reference |
| `review/code-reviewer/coverage-analyst-prompt.md` | coverage measurement semantics | review reference or excluded ops-locked asset |

Current rule:

- 별도 `bindings/` 디렉토리가 없어도 위 inline candidate를 읽어 adapter 초안을 만든다.
- 반복 패턴이 여러 pack에서 안정적으로 재등장하기 전에는 별도 `bindings/*.yaml`로 승격하지 않는다.

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
- terminology.issue_item.canonical: ?
- terminology.review_artifact.canonical: ?
- terminology.docs_artifact.canonical: ?

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
| terminology | `terminology.issue_item.canonical`, `terminology.review_artifact.canonical`, `terminology.docs_artifact.canonical` |

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
└── agent/
```

Role of each item:

- `AGENTS.md`
  - generated harness의 현재 scope와 사용 규칙을 짧게 설명한다
- `README.md`
  - 이 초안이 first validation draft라는 점과 포함/제외 범위를 요약한다
- `GENERATION_SUMMARY.md`
  - 무엇을 생성했고 무엇을 의도적으로 제외했는지 기록한다
- `agent/`
  - generated harness의 markdown workspace binding을 실제 디렉토리로 materialize 한다
- `skills/docs/writing-documents/`
  - selected template scope에서 생성된 문서 workflow 스킬 초안
- `skills/product/issue-analysis/`
  - selected template scope에서 생성된 분석 workflow 스킬 초안
- `agent/`
  - generated harness의 markdown workspace binding을 실제 디렉토리로 materialize 한다

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

Long-term direction after this pass:

- 다음 skeleton부터는 `skills/core/`, `skills/collab/`, `skills/review/`를 누락 상태가 아니라 생성 목표 상태로 취급한다.
- first pass에서 빠진 자산은 "불필요"가 아니라 "다음 generate pass로 미룬 범위"로 해석한다.
- 즉 Session 11의 minimal skeleton은 final target definition이 아니라 validation scaffold다.
- generated standalone harness는 long-term 기준으로 `references/`를 갖지 않는 편이 더 적절하다.
- support guidance는 해당 skill이나 root doc로 흡수하고, source-derived comparison material은 `templates/`에 남긴다.

Second-pass inclusion criteria:

- `skills/core/`: base runtime skill이 stack-neutral이고 artifact contract를 따른 경우 포함
- `skills/collab/`: branch/review/handoff workflow가 제품 고유 시스템 없이 동작하면 포함
- `skills/review/`: base review workflow + product-bound bindings 조합으로 표현 가능하면 포함
- source review info-collector는 provider binding과 local artifact shape가 확정되면 `skills/review/review-context-collector/`로 승격 가능
- source coverage workflow는 repository-native coverage path가 확인되면 `skills/review/coverage-review/`로 승격 가능
- source manual-guide는 external publish 절차를 제외한 local draft workflow로만 제한적으로 `skills/docs/manual-workflow/`에 승격 가능
- excluded review prompt/script: adapter가 외부 시스템 결합을 안전하게 설명할 수 있을 때까지 `templates/`에 남겨 둔다

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
- `product-specific/code-reviewer/info-collector-prompt.md`
- `product-specific/code-reviewer/coverage-analyst-prompt.md`

Decision:

- initiator 1차 입력 범위는 product workflow 전체가 아니라, 먼저 템플릿화 가능한 자산으로 제한한다.
- `issue-analysis`와 `writing-documents`는 템플릿 후보로 유지한다.
- `completing-patch`와 manual/coverage 자산은 운영 절차 결합이 강하므로 분해 전까지 제외한다.

### 2026-04-20 Session 3. Core Neutrality Audit

Reviewed:

- `skills/brainstorming/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/test-driven-development/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/dispatching-parallel-agents/SKILL.md`
- `skills/code-reviewer/SKILL.md`
- `skills/using-base-harness/SKILL.md`

Findings:

- 현재 가장 큰 중립성 문제는 `../agent/prompt/<topic>/...` 형태의 산출물 경로 계약이다.
- 그 다음은 `writing-plans`, `test-driven-development`의 `TypeScript`/`pnpm` 예시 편향이다.
- 반면 review/debug/verification 계열은 기술 스택이 바뀌어도 거의 그대로 재사용 가능하다.

Decision:

- initiator phase 설계 전에 core skill neutralization을 선행 항목으로 둔다.
- artifact path 계약과 stack-specific example은 base layer에서 정리한다.

### 2026-04-20 Session 4. Artifact Contract

Reviewed:

- `skills/brainstorming/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `product-specific/skills/writing-documents-base/markdown-guide.md`

Decision:

- core skill은 logical artifact id만 참조하고, 실제 physical path는 runtime이 제공한다.
- 우선 `analysis_report`, `design_spec`, `implementation_plan` 세 artifact만 contract에 포함한다.
- 현재 runtime의 `../agent/prompt/<topic>/...` 경로는 transitional mapping으로만 문서화하고, core skill 본문 규칙으로는 유지하지 않는다.

### 2026-04-20 Session 5. Core Skill Neutralization

Edited:

- `skills/brainstorming/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/test-driven-development/SKILL.md`

Changes:

- `brainstorming`의 `analysis_report` / `design_spec` 참조를 logical artifact 표현으로 변경
- `writing-plans`의 `implementation_plan` 저장/전달 표현을 artifact contract 기준으로 변경
- `executing-plans`, `subagent-driven-development`의 plan loading 규칙을 physical path 대신 artifact 참조로 변경
- `writing-plans`, `test-driven-development`의 `TypeScript`/`pnpm` 예시를 stack-neutral pseudocode로 교체

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
- `skills/dispatching-parallel-agents/SKILL.md`
- `skills/systematic-debugging/SKILL.md`

Changes:

- `using-base-harness`에 현재 `product-specific` 구조가 transitional layout임을 명시
- `using-base-harness`에 `templates/`, `adapters/`, `generated/` 방향과 logical artifact convention을 추가
- `markdown-guide`의 산출물 규칙을 fixed physical path에서 artifact contract 중심 표현으로 변경
- `dispatching-parallel-agents`, `systematic-debugging`는 현재 기준으로 추가 중립화 없이 유지 가능하다고 확인

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
- 첫 adapter draft 이후에는 위 보고와 함께 `Fill Now` 목록도 항상 제공한다.
- `Fill Now`는 각 unresolved 값에 대해:
  - field path
  - current draft
  - meaning
  - answer shape
  - recommended value if plausible
  를 짧게 보여준다.
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

### 2026-04-21 Session 22. AIM-style manual flow 유지 + generated workspace로 위치 전환

Edited:

- `adapters/ofgw/product-profile.yaml`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `HARNESS_INITIATOR.md`

Changes:

- `workflow.defaults.manual_workflow_required`를 `true`로 확정
- `access_bindings.manual_targets.manual_repo.enabled`를 `true`로 확정
- `access_bindings.manual_targets.manual_repo.default_mode`를 `workspace_file`로 확정
- `access_bindings.manual_targets.manual_repo.location`을 `generated/manual/`로 확정
- manual flow는 AIM의 상태 기반 completion path semantics를 유지하되, legacy AIM MANUAL repo 대신 generated harness 내부 workspace를 writable target으로 사용한다고 문서화

Decision:

- `manual_workflow_required`와 `manual_repo.enabled`는 같은 방향으로 움직여야 한다
- `workspace_file`은 제품 repo 내부 문서 일반 경로(`agent/`)와 구분되는 별도 manual workspace를 가리켜야 한다
- `generated/manual/`는 AIM의 외부 manual repo 개념을 generated harness 안으로 단순화한 위치로 본다

### 2026-04-21 Session 23. terminology를 canonical + aliases로 확정

Edited:

- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- terminology schema를 단일 문자열 대신 `canonical` + `aliases` 구조로 고정
- `issue_item`을 `issue` 기준으로 확정하고 alias를 `ticket`, `jira`, `ims`로 설정
- `review_artifact`를 `PR` 기준으로 확정하고 alias를 `pull request`, `review request`로 설정
- `docs_artifact`를 `markdown document` 기준으로 확정하고 alias를 `doc`, `note`, `report`로 설정
- `mappings.yaml`의 terminology confirm 항목을 제거하고 confirmation packet을 confirmed 상태로 갱신

Decision:

- generated harness는 `canonical`을 기본 표현으로 사용한다
- runtime 해석과 사용자 입력 다양성은 `aliases`로 흡수한다
- provider label과 terminology label은 계속 분리한다

### 2026-04-21 Session 24. First `generate-harness` pass 실행 및 인터페이스 정리

Edited:

- `generated/ofgw-harness/AGENTS.md`
- `generated/ofgw-harness/README.md`
- `generated/ofgw-harness/GENERATION_SUMMARY.md`
- `generated/ofgw-harness/skills/product/issue-analysis/SKILL.md`
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md`
- `generated/ofgw-harness/references/markdown-guide.md`
- `generated/ofgw-harness/generated/manual/README.md`
- `adapters/ofgw/product-profile.yaml`
- `adapters/ofgw/mappings.yaml`
- `adapters/ofgw/confirmation-packet.md`
- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- `generated/ofgw-harness/` 최소 스켈레톤을 실제로 생성
- generated draft에 concrete workspace convention을 materialize
  - `agent/<topic>/`
  - `agent/`
  - `generated/manual/`
- manual flow는 required policy로 유지하되, 첫 pass에서는 writable workspace binding만 생성
- `workflow.defaults.issue_tracker`, `review_channel`, `docs_channel`은 confirmed provider binding에서 직접 유도되는 derived default로 정리
- `product-profile.yaml`의 workflow confirm 목록을 제거하고 `mappings.yaml`의 confirm을 빈 목록으로 정리

Decision:

- 첫 generated draft는 "full workflow 복원"보다 "binding이 실제 파일 구조로 내려오는지"를 검증하는 데 의미가 있다
- generated harness는 binding이 이미 확정된 경로를 실제 디렉토리와 파일로 materialize해야 인터페이스가 매끄럽다
- provider binding으로 충분히 결정되는 workflow label은 별도 generate gate로 남기지 않는 편이 더 일관적이다

### 2026-04-21 Session 25. First generated draft review 반영

Edited:

- `generated/ofgw-harness/agent/README.md`
- `generated/ofgw-harness/README.md`
- `generated/ofgw-harness/AGENTS.md`
- `generated/ofgw-harness/GENERATION_SUMMARY.md`
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md`
- `generated/ofgw-harness/skills/product/issue-analysis/SKILL.md`
- `skills/harness-initiator/SKILL.md`
- `HARNESS_INITIATOR.md`

Changes:

- `agent/` workspace placeholder를 실제로 추가해 generated path policy와 생성물을 일치시킴
- generated `writing-documents` skill에 source workflow의 hard gate와 write/save 분리 규칙을 다시 주입
- generated `issue-analysis` skill에 NotebookLM target URL과 provider source를 반영
- initiator contract에 "behavior-critical safety semantics 보존" 규칙을 추가

Decision:

- generated harness가 source template를 축약하더라도 안전 규칙을 약화시키면 안 된다
- 경로 정책을 문서로만 설명하지 말고 실제 placeholder로 내려주는 편이 first-pass review에 유리하다
- review 결과는 generated artifact 수정에 그치지 않고 initiator contract 개선으로 다시 환류돼야 한다

### 2026-04-21 Session 26. `templates/aim/` 물리 전환 확정

Edited:

- `templates/README.md`
- `templates/aim/README.md`
- `README.md`
- `AGENTS.md`
- `skills/using-base-harness/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/harness-initiator/SKILL.md`
- `claude/CLAUDE.md`
- `adapters/ofgw/mappings.yaml`

Changes:

- `product-specific/`에 있던 AIM source 자산을 실제로 `templates/aim/`로 이동
- 루트 문서와 메타 스킬에서 `templates/`를 intended layout이 아니라 live physical layout으로 고정
- `adapters/ofgw/mappings.yaml`의 `source_pack` 식별자를 `aim-template`로 정리
- `templates/README.md`, `templates/aim/README.md`를 추가해 source pack 레이어를 문서화

Decision:

- 이제 `product-specific/`는 active source location이 아니다
- 과거 `product-specific/` 경로는 `MIGRATION.md`와 세션 기록 안에서만 historical reference로 남긴다
- 이후 initiator 입력은 `templates/<pack>/`를 기준으로 설계하고 확장한다

### 2026-04-21 Session 27. generated target을 standalone harness 기준으로 재정렬

Edited:

- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`
- `README.md`

Changes:

- generated output에 대해 "현재 validation pass"와 "장기 standalone target"을 분리해 문서화
- 장기 target을 `skills/core`, `skills/collab`, `skills/docs`, `skills/review`, `skills/product` 구조로 고정
- 기존 first-pass minimal skeleton은 final shape가 아니라 validation scaffold라는 점을 명시

Decision:

- 앞으로 generated harness 품질 평가는 "minimal draft가 만들어졌는가"가 아니라 "standalone target으로 수렴하는 generate contract가 명확한가"를 같이 본다
- `skills/core/`, `skills/collab/`, `skills/review/`는 더 이상 optional final scope가 아니라 다음 pass의 명시적 생성 목표다

### 2026-04-21 Session 28. `templates/aim/` 세부 분리 보류

Edited:

- `templates/aim/README.md`
- `HARNESS_INITIATOR.md`
- `MIGRATION.md`

Changes:

- `templates/aim/`를 당장 `skills/`, `bindings/`, `examples/`로 물리 분리하지 않기로 결정
- 현재 pack 안의 binding/example은 독립 자산보다 inline 규칙에 가깝다는 점을 문서화
- 향후 분리 조건을 "반복되는 binding schema", "독립 example asset 축적", "initiator의 직접 소비 가치" 기준으로 고정

Decision:

- 지금 시점의 최적 구조는 얕은 `skills/` + `review/` 유지다
- 먼저 해야 할 일은 디렉토리 분리보다 inline binding을 adapter schema로 안정적으로 추출하는 규칙 정리다
- `bindings/`와 `examples/`는 두 번째 template pack 이상이 생기거나, 생성기에서 직접 읽을 실익이 생길 때 도입한다

### 2026-04-21 Session 29. binding 추출 소스를 codebase-only로 보지 않도록 계약 보정

Edited:

- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`
- `MIGRATION.md`

Changes:

- adapter draft가 codebase-derived facts만으로 만들어지는 것이 아니라, template-inherited access pattern도 함께 사용한다고 명시
- `access_bindings.*`의 초안 소스를 `target repo + selected template + human confirmation` 조합으로 재정의
- 별도 `templates/<pack>/bindings/` 디렉토리 없이도 현재 initiator가 binding 초안을 만들 수 있는 이유를 문서화

Decision:

- `repo.*`와 `command_bindings.*`는 주로 codebase에서 가져온다
- `access_bindings.*`는 template 본문에 들어 있는 URL pattern, tool mode, workflow semantics를 suggested default로 상속받을 수 있다
- 따라서 지금 단계의 핵심 작업은 `templates/aim` 분리보다 "inline binding extraction rule"을 더 명확히 적는 것이다

### 2026-04-21 Session 30. inline binding inventory 및 second-pass 포함 기준 추가

Edited:

- `templates/aim/README.md`
- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`
- `MIGRATION.md`

Changes:

- `templates/aim`에서 실제로 어떤 inline 규칙이 binding 후보인지 source별 목록화
- initiator 계약에 inline extraction rule을 추가해 `access_bindings`, runtime convention, support reference를 구분
- second-pass generate에서 `skills/core`, `skills/collab`, `skills/review`를 포함하는 기준을 문서화

Decision:

- 이제 다음 generate pass는 단순 확장이 아니라, 어떤 자산이 standalone target에 들어갈 자격이 있는지 기준을 가진 상태에서 진행할 수 있다
- `templates/aim`는 여전히 얕은 구조를 유지하지만, initiator가 읽어야 할 inline candidate는 충분히 명시된 상태가 된다

### 2026-04-21 Session 31. `generated/ofgw-harness/` second-pass 재생성

Edited:

- `generated/ofgw-harness/AGENTS.md`
- `generated/ofgw-harness/README.md`
- `generated/ofgw-harness/GENERATION_SUMMARY.md`
- `generated/ofgw-harness/hooks/*`
- `generated/ofgw-harness/skills/core/*`
- `generated/ofgw-harness/skills/collab/*`
- `generated/ofgw-harness/skills/review/code-reviewer/SKILL.md`
- `generated/ofgw-harness/references/review/README.md`
- `generated/ofgw-harness/references/review/aim/*`

Changes:

- `core`, `collab`, `review` 레이어를 generated harness 안에 실제로 materialize
- base runtime carry-over skill을 standalone naming으로 정리해 generated tree에 포함
- `hooks/`를 generated harness 안에 함께 복사하고 SessionStart context를 generated `AGENTS.md` 기준으로 변경
- AIM review prompt/script는 active skill이 아니라 `references/review/aim/`의 reference-only 자산으로 포함

Decision:

- second pass부터 `generated/ofgw-harness/`는 더 이상 docs/product-only 검증본이 아니라 standalone target에 수렴하는 generated draft로 본다
- review layer는 reusable workflow와 AIM-locked reference를 분리해 가져가는 편이 현재 계약에 가장 맞다
- 다음 판단 포인트는 `references/review/aim/*` 중 무엇을 실제 `skills/review/`로 승격할지다

### 2026-04-21 Session 32. `review-generated-harness` phase 추가 및 `references/` 역할 명확화

Edited:

- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- initiator phase contract를 `analyze -> draft-adapter -> confirm-gaps -> generate-harness -> review-generated-harness`로 확장
- post-generate review에서 확인해야 할 구조/분류 체크리스트를 공식화
- `references/`를 "언젠가 없어져야 하는 임시 보관소"가 아니라 active behavior 밖의 지원 자산 계층으로 재정의

Decision:

- `review-generated-harness`는 optional human taste check가 아니라 initiator의 공식 후속 phase다
- standalone harness가 구성된 뒤에도 `references/` 자체는 남을 수 있다
- 다만 active runtime behavior는 `skills/*`로 이동해야 하며, AIM-locked carry-over 자산은 productized되거나 폐기되기 전까지 transitional reference로 본다

### 2026-04-21 Session 33. `ofgw-harness` 첫 공식 generated review 실행

Edited:

- `generated/ofgw-harness/REVIEW_GENERATED_HARNESS.md`
- `generated/ofgw-harness/hooks/hooks.json`
- `generated/ofgw-harness/skills/core/brainstorming/SKILL.md`
- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- `review-generated-harness` phase의 선호 산출물을 `generated/<product>-harness/REVIEW_GENERATED_HARNESS.md`로 고정
- 현재 `generated/ofgw-harness/`를 phase 체크리스트로 검토해 first official review 문서를 생성
- review 중 발견된 `hooks/hooks.json` 오염과 `brainstorming`의 source-pack path leakage를 즉시 수정

Decision:

- `generated/ofgw-harness/`는 현재 standalone-target draft로서 구조적으로는 pass 상태다
- 다만 review/manual asset의 productization 범위는 다음 pass에서 계속 정리해야 한다

### 2026-04-21 Session 34. review context와 local manual workflow의 제한적 productization

Edited:

- `generated/ofgw-harness/skills/review/review-context-collector/SKILL.md`
- `generated/ofgw-harness/skills/docs/manual-workflow/SKILL.md`
- `generated/ofgw-harness/references/manual/README.md`
- `generated/ofgw-harness/skills/review/code-reviewer/SKILL.md`
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md`
- `generated/ofgw-harness/generated/manual/README.md`
- `generated/ofgw-harness/README.md`
- `generated/ofgw-harness/AGENTS.md`
- `generated/ofgw-harness/GENERATION_SUMMARY.md`
- `generated/ofgw-harness/references/review/README.md`
- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- AIM info-collector pattern을 `ofgw` binding에 맞는 active `review-context-collector` skill로 승격
- AIM manual-guide의 전체 body는 유지하지 않고, need gate와 draft-first semantics만 흡수한 local `manual-workflow` skill을 추가
- coverage automation은 여전히 reference-only로 유지하고, 그 이유를 generated docs에 명시

Decision:

- review/manual source asset은 "통째 복제"보다 "재사용 가능한 semantics만 productize"하는 쪽이 현재 initiator 방향에 맞다
- `references/`는 줄어들 수는 있어도 0이 되는 것이 목표는 아니며, coverage 같은 AIM-locked automation은 당분간 reference-only가 맞다

### 2026-04-21 Session 35. `references/` 제거 방향 확정 및 `coverage-review` 추가

Edited:

- `generated/ofgw-harness/skills/review/coverage-review/SKILL.md`
- `generated/ofgw-harness/skills/review/code-reviewer/SKILL.md`
- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md`
- `generated/ofgw-harness/README.md`
- `generated/ofgw-harness/AGENTS.md`
- `generated/ofgw-harness/GENERATION_SUMMARY.md`
- `generated/ofgw-harness/REVIEW_GENERATED_HARNESS.md`
- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- `ofgw`에 맞는 JaCoCo 기반 active `coverage-review` skill을 추가
- standalone harness에서 `references/`를 제거하고, 필요한 markdown guidance는 active docs skill로 흡수
- template/source-only carry-over는 generated harness가 아니라 `templates/`에 남기는 방향으로 계약을 보정

Decision:

- standalone harness는 runtime 번들처럼 보여야 하므로 `references/` 없는 구조가 더 맞다
- source-derived comparison material과 미승격 자산은 generated harness가 아니라 `templates/`에 남긴다
- coverage workflow는 이제 active skill로 productize됐고, 남은 보류 범위는 diff-aware gating과 외부 manual publish workflow다

### 2026-04-21 Session 36. initiator 책임 경계 재정의

Edited:

- `HARNESS_INITIATOR.md`
- `skills/harness-initiator/SKILL.md`

Changes:

- `harness-initiator`의 책임을 template selection, binding extraction, adapter drafting, generation, generated-structure review로 한정
- generated harness 안의 review/manual/coverage skill 고도화는 별도의 refinement work로 보는 경계를 명시
- 최근 `ofgw` skill 구체화 작업은 initiator 검증을 위한 exploratory pass였다고 재분류

Decision:

- 앞으로 initiator 검증은 "생성기가 어떤 shape와 분류를 만들어내는가"에 집중한다
- generated harness의 skill body 품질 개선은 initiator의 기본 책임으로 넣지 않는다

### 2026-04-21 Session 37. initiator 검증 기준 문서화

Edited:

- `INITIATOR_VALIDATION.md`
- `HARNESS_INITIATOR.md`
- `MIGRATION.md`

Changes:

- complete assembly 정의를 문서화
- initiator 단독 생성 범위와 refinement 범위를 표로 정리
- adapter에 추가로 필요한 정보 항목을 정리
- initiator 입력/출력 체크리스트를 operational checklist 형태로 정리
- `templates/aim` 자산 분류표, `ofgw` 순수 initiator walkthrough, readiness 평가, second validation target 제안을 하나의 validation 문서로 정리

Decision:

- 앞으로 initiator 검증은 `INITIATOR_VALIDATION.md`를 기준선으로 본다
- `ofgw` generated harness 안의 일부 review/manual/coverage skill은 exploratory refinement 결과로 분리해서 해석한다
- second validation target의 현재 우선 후보는 `osd`다

### 2026-04-21 Session 38. `ofgw-harness` clean rebuild 및 naming normalization 규칙 보강

Edited:

- `generated/ofgw-harness/*`
- `adapters/ofgw/generation-assets-check.md`
- `skills/brainstorming/SKILL.md`
- `skills/harness-initiator/SKILL.md`
- `INITIATOR_VALIDATION.md`
- `HARNESS_INITIATOR.md`

Changes:

- 현재 initiator 계약과 adapter 입력만 기준으로 `generated/ofgw-harness/`를 다시 구성
- base-runtime carry-over skill을 regenerated tree에 다시 materialize
- generated standalone tree에서 source `*-base` naming을 runtime naming으로 정규화
- generated runtime skill에서 template source path 누수를 제거
- `generation-assets-check`와 `REVIEW_GENERATED_HARNESS`를 rebuilt tree 기준으로 다시 맞춤

Decision:

- clean rebuild는 현재 initiator 계약으로 재현 가능하다고 본다
- standalone product harness에서는 carry-over skill의 frontmatter와 cross-skill reference도 runtime 이름으로 정규화해야 한다
- `REVIEW_GENERATED_HARNESS.md`는 계속 validation artifact로만 유지하고 runtime asset으로 취급하지 않는다

### 2026-04-21 Session 39. root `skills/` standalone naming 전환

Edited:

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
- `INITIATOR_VALIDATION.md`
- `generated/ofgw-harness/*`

Changes:

- root `skills/`의 reusable common skill 디렉토리 naming을 `*-base`에서 standalone name으로 전환
- source skill frontmatter와 cross-skill reference를 새 root layout에 맞게 정리
- initiator carry-over policy를 새 root `skills/` layout 기준으로 보정
- rebuilt `ofgw-harness` 문서도 legacy `*-base` naming 누수 금지 기준으로 갱신

Decision:

- root `skills/`는 더 이상 `*-base` postfix를 사용하지 않는다
- generated harness review는 앞으로 “legacy naming이 재도입됐는지”를 보는 식으로 단순화할 수 있다

### 2026-04-21 Session 40. refinement skill 분리

Edited:

- `skills/product-harness-refinement/SKILL.md`
- `skills/using-base-harness/SKILL.md`
- `README.md`
- `INITIATOR_VALIDATION.md`
- `HARNESS_INITIATOR.md`

Changes:

- generated harness 이후의 고도화 작업을 `product-harness-refinement` skill로 분리
- `harness-initiator`는 generation/classification/review-generated-harness 범위에 집중하도록 경계를 다시 명시
- base meta skill routing에도 refinement skill을 추가

Decision:

- refinement는 initiator 안의 후반 phase보다 별도 skill이 더 적절하다
- 이후 generated harness 개선은 우선 `product-harness-refinement`로 다루고, generator defect만 initiator로 되돌린다

### 2026-04-21 Session 41. 첫 refinement target 실증

Edited:

- `generated/ofgw-harness/skills/docs/writing-documents/SKILL.md`
- `adapters/ofgw/mappings.yaml`
- `skills/product-harness-refinement/SKILL.md`

Changes:

- 첫 refinement target을 `writing-documents`로 선택
- generated docs skill에 `ofgwSrc`, `webterminal`, `ofgwAdmin` 실제 모듈 경계와 safe evidence guidance를 추가
- refinement schema에 `status`, `result_note`를 실제 사용해 봄

Decision:

- refinement는 generated asset 하나씩 좁게 적용하는 방식이 적절하다
- 이번 라운드는 generated docs skill을 더 정확하게 만들면서도 initiator scope나 publish adapter를 다시 열지 않는 선에서 검증하는 것이 맞다

### 2026-04-21 Session 42. second refinement target과 schema 보강

Edited:

- `generated/ofgw-harness/skills/review/coverage-review/SKILL.md`
- `adapters/ofgw/mappings.yaml`
- `skills/product-harness-refinement/SKILL.md`
- `INITIATOR_VALIDATION.md`

Changes:

- 두 번째 refinement target으로 `coverage-review`를 적용
- generated coverage skill에 `ofgwSrc`-only coverage boundary와 `webterminal`/`ofgwAdmin` 비포함 rule을 추가
- refinement schema에 `priority`, `depends_on`를 추가해 실행 순서를 표현

Decision:

- refinement schema는 target 목록만으로 끝내기보다 최소한의 ordering 정보까지 담는 편이 더 실용적이다
- refinement는 여전히 generated runtime asset 단위로 좁게 진행하는 것이 적절하다
### Session 43 - Cross-Product Refinement Guardrail

- `product-harness-refinement`는 `ofgw` 검증에 쓰더라도 shared skill/schema 자체는 `osd`와 이후 제품에도 재사용 가능해야 한다는 guardrail을 명시했다.
- refinement schema에 `portability`를 추가해 각 refinement 결과가 `product_local`인지 `shared_candidate`인지 표시할 수 있게 했다.
- `ofgw`의 `writing-documents`, `coverage-review` refinement는 `product_local`로 유지하고, `manual-workflow` refinement는 local draft contract 패턴 검증용 `shared_candidate`로 분류했다.
- generated `manual-workflow`는 제품 사실을 더 많이 집어넣는 대신, topic-scoped local draft path와 explicit draft status 같은 reusable output contract를 강화하는 쪽으로 보정했다.

### Session 44 - Two-Skill Rebuild Evaluation

- 현재 refined `generated/ofgw-harness/`를 새 백업으로 보존한 뒤, initiator-only baseline을 복원하고 다시 refinement를 적용해 두 단계 프로세스를 실제로 재현했다.
- 평가 초점은 `ofgw-harness` 완성도가 아니라:
  - 두 개의 skill 분리가 실제로 도움이 되는지
  - refinement 이후 harness가 initiator-only baseline보다 성숙해지는지
  - adapter/schema가 과하게 복잡해지지 않는지
  였다.
- `product-harness-refinement` skill과 validation 문서에 baseline 대비 성숙도, interface cost, portability를 함께 평가하라는 기준을 추가했다.
- 결과적으로 두-skill 모델은 유지할 가치가 있고, 현재 refinement schema는 아직 읽을 수 있는 크기라고 판단했다.

### Session 45 - Shared Review Criteria and OSD Draft Adapter

- `review-generated-harness` 체크리스트에 maturity gain, interface cost, portability를 추가했다.
- `HARNESS_FLOW_IO.md`를 추가해 `harness-initiator`와 `product-harness-refinement`의 I/O 예시를 한 장으로 압축했다.
- second validation target인 `osd`에 대해 initiator 범위의 analyze + draft-adapter를 수행했다.
- 생성한 초안:
  - `adapters/osd/analysis-summary.md`
  - `adapters/osd/product-profile.yaml`
  - `adapters/osd/mappings.yaml`
  - `adapters/osd/confirmation-packet.md`
- `osd-harness` generation은 아직 하지 않았다.
  - Jira/NotebookLM/manual policy가 미확정이라 confirm-gaps 이후로 넘겼다.

### Session 46 - Fill Now Contract

- `harness-initiator`는 이제 첫 adapter draft 직후 항상 `Fill Now` 목록을 제시해야 한다.
- `Fill Now`는 각 unresolved 값에 대해:
  - field path
  - current draft
  - meaning
  - answer shape
  - recommended value if plausible
  를 포함한다.
- 목적은 사용자가 adapter를 닫기 위해 무엇을 답해야 하는지 한 번에 보이게 만드는 것이다.

### Session 47 - Jira/Auth Path and OSD Default Policy

- Jira MCP binding은 `ofgw`와 같은 org-level shape를 기본값으로 재사용해도 되는 것으로 정리했다.
- Jira API fallback의 `auth_source`는 `../agent/info/access.md`가 아니라 `agent/info/access.md`로 바로잡았다.
  - 현재 standalone/generated runtime 기준에서는 이 경로가 더 일관적이다.
- `osd` adapter draft는 다음 기본값으로 닫았다:
  - Jira enabled = `true`
  - manual required = `true`
  - manual enabled = `true`
  - manual location = `generated/manual/`
- 따라서 현재 `osd`의 남은 필수 confirmation은 NotebookLM 여부만 남는다.

### Session 48 - OSD NotebookLM Default Alignment

- `osd`의 NotebookLM binding도 first draft 단계에서는 `ofgw`와 같은 기본값으로 닫았다.
- 이유:
  - 지금 단계에서는 "어느 notebook인가"보다 binding shape 검증이 더 중요하다.
  - `harness-initiator`가 default integration shape를 빠르게 materialize하는지 보는 편이 더 유효하다.
- 이 변경 후 `osd`는 confirm-gaps가 모두 닫힌 상태로 보고 generation 단계로 진행할 수 있게 됐다.

### Session 49 - OSD First Draft Generation

- `adapters/osd/*`를 confirmed 상태로 보고 `generated/osd-harness/` first draft를 생성했다.
- 생성 범위:
  - root docs
  - hooks
  - `agent/`
  - `generated/manual/`
  - `skills/core/*`
  - `skills/collab/*`
  - `skills/review/*`
  - `skills/docs/*`
  - `skills/product/issue-analysis/`
- `osd` product-bound file들은 `Makefile`, `test/run_coverage.sh`, `dist/patch_osd.sh`, git remote evidence에 맞게 다시 썼다.
- `adapters/osd/generation-assets-check.md`도 추가해 template-derived generation이 현재 draft와 맞는지 검증했다.

### Session 50 - Draft Default Bias

- `harness-initiator` 초안 생성 시 user-config 최소화를 위해 다음 default bias를 문서화했다:
  - Jira = `mcp` default
  - manual workspace = `generated/manual/`
- 다만 이 값들은 universal hard rule이 아니라 draft default로 본다.
- repo/product evidence가 다르면 adapter에서 다시 열거나 덮어쓸 수 있게 유지한다.

### Session 51 - Root Harness Docs Consolidation

- root 문서 역할을 다시 정리했다.
- `HARNESS_FLOW_IO.md`, `INITIATOR_VALIDATION.md`는 `HARNESS_INITIATOR.md`의 하위 성격이 강해서 별도 root 문서로 유지하지 않기로 했다.
- 두 문서의 현재 기준선은 이 문서의 `Validation And Flow Summary` 섹션으로 병합했다.
- root 기준 문서는 아래 네 개만 남긴다:
  - `README.md`
  - `AGENTS.md`
  - `MIGRATION.md`
  - `HARNESS_INITIATOR.md`

### Session 52 - Generated Harness Root Docs Consolidation

- generated harness root md도 runtime-facing 문서만 남기기로 했다.
- generated root 기준 문서는 아래 세 개로 고정한다:
  - `README.md`
  - `AGENTS.md`
  - `GENERATION_SUMMARY.md`
- `REVIEW_GENERATED_HARNESS.md`, `REFINEMENT_EVALUATION.md`는 runtime bundle 일부가 아니라 validation/evaluation 산출물이므로 `adapters/<product>/` 아래로 이동했다.
- 따라서:
  - generated harness root는 standalone runtime draft처럼 보이게 유지한다.
  - validation trace는 adapter 산출물로 분리한다.

### Session 53 - `.codex` Ignore and `product-specific/` Removal

- root `.gitignore`에 `.codex`를 추가했다.
- `product-specific/`는 이미 active source location이 아니고 deprecated 잔재만 남은 상태라고 다시 확인했다.
- 남아 있던 `product-specific/README.md`를 제거하고, 디렉토리 자체도 정리 대상으로 본다.
- 해석:
  - active source는 `templates/`
  - active runtime skill set은 `skills/`
  - `product-specific/`는 더 이상 live layout 일부가 아니다

### Session 51 - OSD Review-Layer Evaluation and Shared `code-reviewer` Fix

- `generated/osd-harness/`를 전반 평가한 결과, 가장 큰 문제는 product-local binding 부족이 아니라 review layer 내부 연결 부족이었다.
- `review-context-collector`와 `coverage-review`가 generated 됐더라도, carried-over `code-reviewer`가 이들을 bound helper로 인식하지 못하면 review layer가 반쪽짜리로 남는다.
- 이 문제는 `osd` 전용 refinement보다 shared `skills/code-reviewer/`와 initiator review 기준 보정으로 푸는 것이 더 적절하다고 판단했다.
- 따라서:
  - shared `skills/code-reviewer/SKILL.md`를 보강했다
  - generated `ofgw-harness`, `osd-harness`의 `skills/review/code-reviewer/SKILL.md`도 같은 기준으로 맞췄다
  - `review-generated-harness` 체크리스트에 companion review skill coherence를 추가했다
- 판단:
  - `osd-harness`는 initiator 적용이 전반적으로 잘 됐고 usable first draft다
  - 지금 시점의 핵심 개선은 adapter/schema 확장이 아니라 shared carry-over skill 품질 개선이다
