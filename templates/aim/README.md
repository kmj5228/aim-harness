# AIM Template Pack

`templates/aim/`는 AIM에서 추출한 generation source pack이다.

포함 범위:

- `skills/issue-analysis/`
- `skills/completing-patch/`
- `skills/writing-documents/`
- `review/code-reviewer/`

해석 원칙:

- 이 디렉토리는 AIM 런타임 자체가 아니라, 다른 제품 하네스를 생성하기 위한 원본 pack이다.
- 재사용 가능한 workflow와 strongly-coupled binding을 함께 보존하되, 생성 시점에는 adapter로 분리한다.
- 첫 `harness-initiator` 검증 대상인 `ofgw`도 이 pack을 source로 사용한다.

주의:

- 모든 자산이 즉시 템플릿화 가능한 것은 아니다.
- `manual-guide`, `completing-patch`, coverage 관련 자산은 여전히 분해 후 재사용 대상으로 본다.

## Current Structure Decision

현재는 `templates/aim/`를 더 세분화하지 않는다.

즉, 당장은 아래 구조를 유지한다.

```text
templates/aim/
├── skills/
└── review/
```

판단 근거:

- 실제 binding 정보가 아직 `bindings/*.yaml`처럼 독립 자산으로 정리돼 있지 않고, `issue-analysis`, `writing-documents`, `manual-guide`, review prompt 본문 안에 섞여 있다.
- 별도 `examples/`로 옮길 만한 실물 예시 자산도 아직 충분히 모여 있지 않다. 현재 다수의 "예시"는 본문 속 inline example이거나 외부 runtime path 참조다.
- 지금 물리 분리를 먼저 하면 initiator 입력은 늘어나지만, 생성 규칙은 오히려 더 모호해질 수 있다.

현재 해석:

- `skills/`는 workflow template와 support guide를 함께 담는다.
- `review/`는 review-specific prompt/script 자산을 담는다.
- binding과 example은 우선 inline 상태로 유지하고, initiator가 adapter draft를 만들면서 추출 대상으로 식별한다.

향후 분리 조건:

- 같은 종류의 binding field가 둘 이상의 template pack에서 반복적으로 등장할 때
- inline example을 독립 reference asset으로 재사용할 수 있을 만큼 축적됐을 때
- initiator가 `bindings/`와 `examples/`를 직접 읽어 generation 품질을 높일 수 있을 때

그 전까지는 `templates/aim/`를 억지로 `skills/`, `bindings/`, `examples/`로 나누지 않는다.

## Inline Binding Inventory

현재 AIM pack에서 initiator가 읽는 binding 후보는 별도 파일이 아니라 본문 안에 있다.

### `skills/issue-analysis/`

- IMS issue URL pattern
  - draft target: `access_bindings.issue_sources.ims.*`
- Jira access rule and API pattern
  - draft target: `access_bindings.issue_sources.jira.*`
- NotebookLM / spec lookup requirement
  - draft target: `access_bindings.spec_sources.notebooklm.*`
- analysis report artifact naming
  - draft target: generated runtime artifact convention

### `skills/writing-documents/`

- platform guide set (`jira`, `confluence`, `ims`, `gitlab`, `mail`, `markdown`)
  - draft target: docs/review/manual support reference selection
- markdown document workspace convention
  - draft target: `access_bindings.docs_targets.repo_markdown.*`
- manual workflow and manual repository semantics
  - draft target:
    - `workflow.defaults.manual_workflow_required`
    - `access_bindings.manual_targets.manual_repo.*`
- MR description marker semantics
  - draft target: generated completion/manual workflow notes

### `review/code-reviewer/`

- MR/API/project policy hints in info-collector prompt
  - draft target: `access_bindings.review_targets.*` candidate
- coverage command, base branch, measurement script semantics
  - draft target: review support reference or excluded ops-locked asset

분류 원칙:

- URL, repo path, notebook target, browser/API/MCP/workspace mode는 binding 후보다.
- artifact filename, workspace placeholder, marker contract는 generated runtime convention 후보다.
- 스타일 가이드, 서술 예시, 긴 prompt body는 support reference 또는 excluded asset 후보다.
