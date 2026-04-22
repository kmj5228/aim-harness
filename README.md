# base-harness

## 소개

`base-harness`는 여러 제품 하네스를 생성하고 발전시키기 위한 공통 생성기 저장소다.
기본 런타임은 Codex이며, 공통 스킬은 `skills/`, 생성 입력은 `templates/`, 제품별 적응 정보는 `adapters/`, 생성 결과는 `generated/`에 둔다.

핵심 원칙:

- 공통 runtime skill set은 `skills/`에 둔다.
- 생성 입력 source pack은 `templates/`에 둔다.
- 제품별 binding draft는 `adapters/`에 둔다.
- 생성된 제품 하네스는 `generated/` 아래에 둔다.
- Codex hook source-of-truth는 `hooks/`에 둔다.
- Claude 자산은 선택형 runtime pack으로 `claude/`에 둔다.

## 현재 상태

현재 기준으로는 아래가 정리돼 있다.

- 코어 개발 루프와 주요 협업 스킬의 1차 공통화 완료
- AIM 유래 공통 스킬을 root `skills/` 아래 standalone 이름으로 정리
- AIM 결합 자산을 `templates/aim/` source pack으로 이동
- `harness-initiator`로 `adapters/`와 `generated/` 흐름을 검증 중
- Codex용 `SessionStart` 훅 source를 `hooks/`로 정리

즉, `base-harness`는 더 이상 단순 복제본이 아니라:

- `skills/` = 기본 base runtime skill set
- `templates/` = generation source packs
- `adapters/` = product adaptation drafts
- `generated/` = generated product harness drafts
- `hooks/` = Codex hook source-of-truth
- `claude/` = 선택형 Claude runtime pack

구조로 해석하는 것이 맞다.

## 기본 규칙

기본 런타임 규칙은 [AGENTS.md](/home/woosuk_jung/harness/of-harness/AGENTS.md:1)에 있다.

요약:

- 관련 스킬이 있으면 행동 전에 먼저 사용한다.
- 기본 스킬 라우팅은 `skills/`만 대상으로 본다.
- `templates/`는 generation source로만 사용한다.
- 검증 없이 완료를 주장하지 않는다.

## 기본 스킬 세트

### 코어 루프

- `brainstorming`
- `writing-plans`
- `executing-plans`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`

### 협업 루프

- `subagent-driven-development`
- `dispatching-parallel-agents`
- `using-feature-branches`
- `requesting-code-review`
- `receiving-code-review`
- `code-reviewer`
- `finishing-a-development-branch`

### 메타 및 저작

- `using-base-harness`
- `harness-initiator`
- `harness-support-assets`
- `harness-refinement`
- `writing-skills`

## Source Packs

기본 스킬 라우팅에서 분리된 generation input 자산:

- `templates/aim/skills/issue-analysis`
- `templates/aim/skills/completing-patch`
- `templates/aim/skills/writing-documents`
- `templates/aim/skills/writing-skills`
- `templates/aim/AGENTS.template.md`
- `templates/aim/review/code-reviewer/*`

이 영역은 기본 런타임에 자동 포함되지 않는다.
`harness-initiator`가 읽는 generation source pack으로 본다.

## Generated Harness Target

`generated/<product>-harness/`의 장기 목표는 standalone product harness다.

의도하는 구조는 아래와 같다.

```text
generated/<product>-harness/
├── AGENTS.md
├── README.md
├── hooks/
├── skills/
│   ├── core/
│   ├── collab/
│   ├── authoring/
│   ├── docs/
│   ├── review/
│   └── product/
└── generated/
    └── manual/
```

현재 `generated/ofgw-harness/`는 이 최종 구조를 검증하기 위한 rebuilt validation draft다.
즉 usable first draft 수준까지는 올라왔지만, 여전히 initiator 계약을 다듬기 위한 검증 산출물로 본다.

## Runtime Layout

```text
base-harness/
├── AGENTS.md
├── README.md
├── MIGRATION.md
├── HARNESS_INITIATOR.md
├── hooks/
│   ├── README.md
│   ├── config.toml
│   ├── hooks.json
│   └── session-start.sh
├── skills/
│   ├── using-base-harness/
│   ├── harness-initiator/
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── subagent-driven-development/
│   ├── dispatching-parallel-agents/
│   ├── test-driven-development/
│   ├── systematic-debugging/
│   ├── verification-before-completion/
│   ├── using-feature-branches/
│   ├── finishing-a-development-branch/
│   ├── requesting-code-review/
│   ├── receiving-code-review/
│   ├── code-reviewer/
│   └── writing-skills/
├── templates/
│   ├── README.md
│   └── aim/
│       ├── README.md
│       ├── skills/
│       └── review/
├── adapters/
│   └── <product>/
├── generated/
│   └── <product>-harness/
└── claude/
    ├── README.md
    ├── CLAUDE.md
    ├── settings.json
    └── hooks/
        └── session-start.sh
```

## Runtime Policy

### Codex

- 기본 진입점은 루트 [AGENTS.md](/home/woosuk_jung/harness/of-harness/AGENTS.md:1)다.
- [hooks](/home/woosuk_jung/harness/of-harness/hooks) 는 Codex hook source-of-truth다.
- 저장소를 `git pull`하는 것만으로는 로컬 Codex 런타임에 자동 활성화되지 않는다.
- 실제 사용하려면 `hooks/config.toml`, `hooks/hooks.json`을 `~/.codex/` 또는 프로젝트 `.codex/` 레이아웃에 맞게 배치하거나 병합해야 한다.

### Claude

- Claude 자산은 [claude](/home/woosuk_jung/harness/of-harness/claude) 아래에 모아 둔다.
- Claude 사용자는 이 디렉토리를 선택형 runtime pack으로 사용한다.
- 자세한 배치와 설치 전제는 [claude/README.md](/home/woosuk_jung/harness/of-harness/claude/README.md:1)를 본다.

## 문서 역할

- [AGENTS.md](/home/woosuk_jung/harness/of-harness/AGENTS.md:1): Codex 기본 런타임 규칙
- [README.md](/home/woosuk_jung/harness/of-harness/README.md:1): 구조와 사용법
- [MIGRATION.md](/home/woosuk_jung/harness/of-harness/MIGRATION.md:1): 마이그레이션 기록
- [HARNESS_INITIATOR.md](/home/woosuk_jung/harness/of-harness/HARNESS_INITIATOR.md:1): initiator 방향, 검증 기준, flow I/O, 현재 결정사항
- [templates](/home/woosuk_jung/harness/of-harness/templates): source template packs

## 참고

현재까지의 추출 과정과 판단 로그는 [MIGRATION.md](/home/woosuk_jung/harness/of-harness/MIGRATION.md:1)에 유지한다.
`harness-initiator` 브랜치에서 합의한 생성기 방향, 검증 기준, refinement 경계, flow I/O는 [HARNESS_INITIATOR.md](/home/woosuk_jung/harness/of-harness/HARNESS_INITIATOR.md:1)에 유지한다.
실제 스킬 초안은 [skills/harness-initiator/SKILL.md](/home/woosuk_jung/harness/of-harness/skills/harness-initiator/SKILL.md:1)에 있다.
