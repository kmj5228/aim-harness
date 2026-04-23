# of-harness

## 개요

`of-harness`는 여러 제품용 harness를 생성하고 검증하기 위한 공통 생성기 저장소다.

현재 기준의 핵심은 아래 3개 스킬이다.

- `harness-initiator`
- `harness-support-assets`
- `harness-refinement`

이 저장소의 목표는 특정 제품 하네스를 직접 완성하는 것이 아니라, 위 3개 스킬과 최소 schema로 제품별 harness를 **재현 가능하게 생성**하는 것이다.

## 현재 해석

현재 구조는 이렇게 본다.

- `skills/`
  - shared normalized runtime skills
- `templates/`
  - source-fidelity generation packs
- `adapters/`
  - product-specific truth and generation mapping
- `generated/`
  - generated product harness runtime v1
- `hooks/`
  - Codex hook source-of-truth

즉 이 저장소는 `aim-harness`의 복제본이 아니라, `aim`을 source pack으로 삼아 product harness를 생성하는 **generator repo**다.

## 검증 상태

현재까지 확인된 것:

- `ofgw-harness`
  - 현재 3스킬 계약으로 재생성 가능
- `osd-harness`
  - 같은 3스킬 계약으로 cross-product 재현 가능함을 별도 실증에서 확인
- `aim-harness`
  - source-heavy final validation 대상에서 parity를 확인
- `writing-skills`
  - shared authoring family로 승격 완료
- `using-{product}-harness`
  - root shared skill이 아니라 generated runtime-local meta skill로 생성하는 방향이 검증됨
- `runtime_entry`
  - generated `AGENTS.md`, `hooks/*`, startup contract를 묶는 정식 generation contract로 정리됨

현재 generated harness는 “최종 완성품”보다 **standalone runtime v1.x**로 보는 게 맞다.

또한 generated harness는 필요하면 실제 프로젝트의 Codex layout으로 한 번 더 설치 변환된다.

## 디렉토리 역할

```text
of-harness/
├── README.md
├── AGENTS.md
├── HARNESS_INITIATOR.md
├── MIGRATION.md
├── hooks/
├── skills/
├── templates/
├── adapters/
├── generated/
└── claude/
```

세부 의미:

- `skills/`
  - 생성기와 generated harness가 공통으로 재사용하는 shared runtime skill
- `templates/aim/`
  - AIM 원본에서 가져온 source-fidelity pack
  - generated `AGENTS.md`의 source는 여기의 `AGENTS.template.md`
- `adapters/<product>/`
  - product truth, bindings, generation decisions
- `generated/<product>-harness/`
  - 실제 생성된 product runtime

중요:

- `adapters/`는 제품 truth를 담는 canonical 위치이지만, 새 제품 생성에서 자동으로 신뢰되는 defaults 저장소는 아니다.
- `generated/`는 live runtime draft이자 validation target이지만, 새 생성의 입력 source는 아니다.
- 새 제품 생성에서는 기존 adapter/generated 결과가 있어도 사용자 확인이 우선이고, 재생성 검증일 때만 기존 adapter truth를 그대로 재사용할 수 있다.
- live adapter에는 최소한 현재 확인 상태를 나타내는 `adapter_status` 메타가 들어갈 수 있다.

## 문서 역할

- `README.md`
  - 사람용 개요 문서
- `AGENTS.md`
  - 이 생성기 저장소를 다루는 AI 에이전트용 작업 계약
  - generated harness의 `AGENTS.md` source가 아니다
- `HARNESS_INITIATOR.md`
  - 현재 생성기 계약, 검증 기준, 실험 결과, 주요 결정사항
- `MIGRATION.md`
  - 연속 작업 기록과 변경 로그

중요:

- generated harness의 `AGENTS.md`는 root `AGENTS.md`에서 직접 오지 않는다.
- generated runtime contract의 source는 `templates/<pack>/AGENTS.template.md`와 adapter truth다.
- root `AGENTS.md`는 **이 저장소 자체를 유지보수할 때**만 의미가 있다.

## 현재 live 산출물

현재 live generated harness는:

- `generated/ofgw-harness/`

현재 live adapter는:

- `adapters/ofgw/`

`aim`, `osd`는 현재 live 배포 대상이 아니라, generator 검증 과정에서 사용한 historical validation target으로 본다.

백업/임시 rebuild 산출물은 기본적으로 유지하지 않는다. 필요하면 검증 후 제거한다.

## 설치 해석

generated harness는 install 이전 산출물이다. 실제 프로젝트 사용 시에는 보통 아래 layout으로 변환된다.

- skills:
  - `<repo>/.agents/skills/<skill>/`
- startup contract:
  - `<repo>/AGENTS.md`
  - 또는 `<repo>/.codex/<product>-harness/AGENTS.md`
- project-local config and hooks:
  - `<repo>/.codex/config.toml`
  - `<repo>/.codex/hooks/*`
- runtime workspace:
  - `<repo>/agent/`
  - `<repo>/generated/manual/`

즉 생성과 설치는 분리된 단계다.

## 다음 관심사

현재 생성기에서 가장 큰 남은 격차는 원본 `aim-harness`의 advanced tail workflow다.

예:

- `completing-patch`
- external manual publish
- marker/manual follow-up 같은 post-merge 운영 체인

이 영역은 base generator 기본 기능보다 optional extension에 가깝다.

## 참고

생성기 계약과 최근 검증 결과는 아래 문서를 본다.

- [HARNESS_INITIATOR.md](/home/woosuk_jung/harness/of-harness/HARNESS_INITIATOR.md)
- [MIGRATION.md](/home/woosuk_jung/harness/of-harness/MIGRATION.md)
