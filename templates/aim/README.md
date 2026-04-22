# AIM Template Pack

`templates/aim/`는 AIM에서 추출한 generation source pack이다.

현재 해석:

- 이 디렉토리는 AIM 런타임 자체가 아니라, 다른 제품 하네스를 생성하기 위한 source pack이다.
- 다만 최소 curated 템플릿만 두는 것이 아니라, AIM 원본의 entry contract와 skill-adjacent support asset도 함께 보존하는 source-fidelity pack으로 본다.
- initiator는 여기서:
  - active workflow skeleton
  - startup/runtime contract
  - support asset
  - inline binding candidate
  를 읽고 generated harness를 만든다.

## Layer Model

현재 `of-harness`는 같은 이름의 skill이 여러 레이어에 존재할 수 있다.

- root `skills/<skill>/SKILL.md`
  - shared runtime skill
  - AIM 의존성을 제거한 일반화 버전
  - initiator의 기본 carry-over source
- `templates/aim/skills/<skill>/SKILL.md`
  - AIM source skill
  - 원본 AIM의 workflow, wording, support asset 맥락을 보존하는 source-fidelity 자산
- `generated/<product>-harness/skills/.../SKILL.md`
  - product runtime v1
  - shared runtime carry-over와 template-derived productization 결과가 합쳐진 generated skill

즉 `templates/aim/skills/`의 `SKILL.md`는 root `skills/`와 중복 실수로 두는 것이 아니다.
source skill이 있어야 initiator가 support asset과 workflow semantics를 함께 해석할 수 있다.

포함 범위:

- `AGENTS.template.md`
- `skills/`
  - core/collab/product/docs source skills
  - skill-adjacent support asset
- `review/code-reviewer/`
  - review workflow source skill
  - prompt/script support asset

주의:

- `templates/aim/`는 원본 `aim-harness`의 무차별 mirror가 아니다.
- source pack으로 의미가 있는 skill, startup contract, support asset만 유지한다.
- build output, cache, 개인 환경 산출물은 넣지 않는다.

## Current Structure Decision

현재는 `templates/aim/`를 더 세분화하지 않는다.

즉, 당장은 아래 구조를 유지한다.

```text
templates/aim/
├── AGENTS.template.md
├── skills/
└── review/
```

판단 근거:

- 실제 binding 정보가 아직 `bindings/*.yaml`처럼 독립 자산으로 정리돼 있지 않고, `issue-analysis`, `writing-documents`, `manual-guide`, review prompt, entry contract 본문 안에 섞여 있다.
- 별도 `examples/`로 옮길 만한 실물 예시 자산도 아직 충분히 모여 있지 않다. 현재 다수의 "예시"는 본문 속 inline example이거나 외부 runtime path 참조다.
- 지금 물리 분리를 먼저 하면 initiator 입력은 늘어나지만, 생성 규칙은 오히려 더 모호해질 수 있다.

현재 해석:

- `AGENTS.template.md`는 원본 AIM의 startup/runtime contract source다.
- `skills/`는 workflow template와 support asset을 함께 담는다.
- `review/`는 review-specific skill과 prompt/script 자산을 담는다.
- binding과 example은 우선 inline 상태로 유지하고, initiator가 adapter draft를 만들면서 추출 대상으로 식별한다.

향후 분리 조건:

- 같은 종류의 binding field가 둘 이상의 template pack에서 반복적으로 등장할 때
- inline example을 독립 reference asset으로 재사용할 수 있을 만큼 축적됐을 때
- initiator가 `bindings/`와 `examples/`를 직접 읽어 generation 품질을 높일 수 있을 때

그 전까지는 `templates/aim/`를 억지로 `skills/`, `bindings/`, `examples/`로 나누지 않는다.

## Inline Binding Inventory

현재 AIM pack에서 initiator가 읽는 binding 후보는 별도 파일이 아니라 본문 안에 있다.

### `AGENTS.template.md`

- startup skill routing rule
- workflow chain
- skill gap reporting obligation
- runtime entry semantics
  - draft target: generated `AGENTS.md` and hook/session-start generation

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

## Support Asset Policy

현재 AIM pack은 support asset을 적극적으로 포함한다.

예:

- `skills/brainstorming/spec-document-reviewer-prompt.md`
- `skills/writing-plans/plan-document-reviewer-prompt.md`
- `skills/subagent-driven-development/*.md`
- `skills/systematic-debugging/*.md`, `find-polluter.sh`
- `skills/test-driven-development/testing-anti-patterns.md`
- `skills/writing-skills/*`
- `review/code-reviewer/*.md`, `measure_diff_cov.sh`

원칙:

- source pack에서는 원본 skill 옆에 support asset을 둔다.
- generated runtime에서는 initiator와 `harness-support-assets`가 이 자산을 기본적으로 generated skill 옆으로 함께 싣는다.
- 예외 판단은 실제 generation/validation pass에서 구체 문제가 드러난 뒤에만 도입한다.
- generated runtime에 함께 실을 때는 원본 AIM처럼 generated skill 디렉토리 안 `SKILL.md`와 같은 위치 계층에 둔다.
  - 예: `skills/review/code-reviewer/measure_diff_cov.sh`
  - 예: `skills/brainstorming/spec-document-reviewer-prompt.md`
- support asset을 source pack에서 제거한 뒤 generated에서 다시 추정하지 않는다.

현재 확인된 사실:

- 원본 `aim-harness/skills/*`의 skill-adjacent support asset은 현재 `templates/aim`에 모두 들어와 있다.
- generated v1에서 빠지는 자산은 source 누락보다 productization 범위 문제로 본다.
  - active generated skill로 이미 흡수된 경우
  - ops-locked이라 template에 남기는 경우
  - 아직 첫 productization pass에서 선택되지 않은 경우

분류 원칙:

- URL, repo path, notebook target, browser/API/MCP/workspace mode는 binding 후보다.
- artifact filename, workspace placeholder, marker contract는 generated runtime convention 후보다.
- 스타일 가이드, 서술 예시, 긴 prompt body는 support reference 또는 excluded asset 후보다.
