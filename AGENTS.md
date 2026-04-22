# of-harness Agent Contract

이 문서는 `of-harness` **생성기 저장소 자체**를 다룰 때 사용하는 AI 에이전트용 작업 계약이다.

중요:

- 이 문서는 generated harness의 `AGENTS.md` source가 아니다.
- generated runtime contract source는 `templates/<pack>/AGENTS.template.md`와 adapter truth다.
- root `AGENTS.md`는 `of-harness` repo를 유지보수할 때만 적용한다.

## Repository Interpretation

이 저장소는 product runtime이 아니라 generator repo다.

- `skills/`
  - shared normalized runtime skills
- `templates/`
  - source-fidelity generation packs
- `adapters/`
  - product-specific truth and generation mapping
- `generated/`
  - generated product runtime v1
- `hooks/`
  - generator-side Codex hook source-of-truth

`generated/<product>-harness/AGENTS.md`와 이 파일을 혼동하지 않는다.

## Main Working Rule

이 저장소에서 작업할 때는 항상 아래를 먼저 구분한다.

1. shared generator rule인가
2. template source pack 자산인가
3. adapter truth인가
4. generated runtime 결과물인가

이 구분이 흐려지면, 우선 분류부터 다시 맞춘다.

## Three-Skill Priority

현재 generator의 중심은 아래 3개다.

1. `harness-initiator`
2. `harness-support-assets`
3. `harness-refinement`

새 요구가 생기면 먼저:

- 이게 `initiator` 책임인지
- `support-assets` 책임인지
- `refinement` 책임인지

를 나눈 뒤에 수정한다.

## Responsibility Boundary

### `harness-initiator`

- adapter draft
- runtime skeleton generation
- shared family carry-over
- `runtime_entry`
- generated `AGENTS.md`/`hooks/*` 생성 계약

### `harness-support-assets`

- template-side adjacent support asset의 first-pass `bundle + port`
- obvious path / command / terminology / stack-aware porting
- source-only helper -> repo-native helper rewrite 후보 처리

### `harness-refinement`

- first-pass 이후에도 남는 residual mismatch 정리
- bundled support asset이 실제 target runtime에 충분히 맞는지 2차 점검

## Root vs Template vs Generated

같은 이름의 skill이 여러 레이어에 있어도 중복 실수로 보지 않는다.

- root `skills/`
  - shared normalized runtime
- `templates/<pack>/skills/`
  - source-fidelity pack
- `generated/<product>-harness/skills/`
  - generated product runtime

특히 `templates/<pack>/skills/<skill>/SKILL.md`는 adjacent support asset 해석의 anchor일 수 있으니 함부로 제거하지 않는다.

## Working Policy

- 사람용 개요는 `README.md`를 우선한다.
- 생성기 계약과 검증 기준은 `HARNESS_INITIATOR.md`를 우선한다.
- 연속 로그와 변경 기록은 `MIGRATION.md`를 우선한다.
- root 문서 간 내용이 겹치면:
  - `README.md`는 사람용 요약
  - `AGENTS.md`는 AI 작업 계약
  - 상세 결정사항은 `HARNESS_INITIATOR.md`
  - 연속 기록은 `MIGRATION.md`
  로 정리한다.

## Generated Runtime Caution

`generated/` 아래 자산은 validation target이기도 하지만, 동시에 live runtime draft다.

- 불필요한 backup/rebuild 산출물은 검증 후 제거한다.
- 다른 세션에서 만든 unrelated generated drift는 함부로 섞지 않는다.
- generated harness 수정이 필요한 경우:
  - generator 계약에서 재현 가능한지
  - 아니면 아직 manual proof인지
  를 먼저 구분한다.
- `generated/`를 다음 generation pass의 truth source처럼 사용하지 않는다.

## Fresh vs Rebuild Rule

이 저장소를 다룰 때는 항상 아래를 먼저 판단한다.

- fresh generation
  - 기존 `adapters/<product>/`와 `generated/<product>-harness/`가 있어도 자동 신뢰하지 않는다.
  - 기존 adapter 값은 suggestion일 수 있지만, confirmed truth로 간주하지 않는다.
  - 필요한 확인값은 다시 사용자에게 닫는다.
- rebuild validation
  - 이미 accepted 된 adapter truth를 재사용해 parity를 확인한다.
  - 이 경우 기존 adapter는 canonical input으로 재사용 가능하다.
  - 기존 generated harness는 comparison target일 뿐 generation input은 아니다.

Live adapter를 수정할 때는 최소 상태 메타를 유지한다.

- `adapter_status.confirmation_level`
- `adapter_status.reuse_policy`

이 메타는 fresh generation에서 자동 신뢰를 막고, rebuild validation에서만 canonical reuse가 가능하다는 현재 계약을 드러내기 위한 것이다.

## Skill-First Rule

이 저장소를 수정할 때도 relevant skill이 있으면 먼저 읽는다.

특히 우선 확인 대상:

- `harness-initiator`
- `harness-support-assets`
- `harness-refinement`
- `writing-skills`
- `using-base-harness`

## Current Interpretation

현재 기준으로는:

- generated harness는 standalone runtime v1.x
- original `aim-harness` 대비 운영 완성도는 아직 약간 부족
- 하지만 `ofgw`, `osd`에서 cross-product 재현성은 확보됨

따라서 이 저장소의 우선순위는 product harness 완성보다 **generator contract 개선과 재현성 검증**이다.
