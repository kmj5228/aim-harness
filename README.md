# base-harness

## 소개

`base-harness`는 여러 제품에서 재사용 가능한 공통 하네스를 만드는 저장소다.
현재는 `aim-harness`에서 추출한 공통 루프를 `Codex-first` 기준으로 정리하고 있다.

핵심 원칙:

- 기본 런타임은 Codex다.
- 공통 작업 방식은 `skills/`에 둔다.
- 제품 전용 절차는 `product-specific/`로 분리한다.
- Claude 자산은 선택형 runtime pack으로 `claude/`에 둔다.

## 현재 상태

현재 기준으로는 아래가 정리돼 있다.

- 코어 개발 루프와 주요 협업 스킬의 1차 공통화 완료
- `*-aim` 스킬을 `*-base`로 정리
- 제품 전용 절차와 강결합 자산을 `product-specific/`로 분리
- 루트는 Codex 기본 진입점, Claude 자산은 별도 pack으로 분리

즉, `base-harness`는 더 이상 단순 복제본이 아니라:

- `skills/` = 기본 base runtime skill set
- `product-specific/` = 선택형 product pack
- `claude/` = 선택형 Claude runtime pack

구조로 해석하는 것이 맞다.

## 기본 규칙

기본 런타임 규칙은 [AGENTS.md](/home/smj/harness/base-harness/AGENTS.md:1)에 있다.

요약:

- 관련 스킬이 있으면 행동 전에 먼저 사용한다.
- 기본 스킬 라우팅은 `skills/`만 대상으로 본다.
- `product-specific/`는 명시적으로 필요할 때만 사용한다.
- 검증 없이 완료를 주장하지 않는다.

## 기본 스킬 세트

### 코어 루프

- `brainstorming-base`
- `writing-plans-base`
- `executing-plans-base`
- `test-driven-development-base`
- `systematic-debugging-base`
- `verification-before-completion-base`

### 협업 루프

- `subagent-driven-development-base`
- `dispatching-parallel-agents-base`
- `using-feature-branches-base`
- `requesting-code-review-base`
- `receiving-code-review-base`
- `code-reviewer-base`
- `finishing-a-development-branch-base`

### 메타 및 저작

- `using-base-harness`
- `writing-skills-base`

## Product Packs

기본 스킬 라우팅에서 분리된 제품 전용 자산:

- `product-specific/skills/issue-analysis-base`
- `product-specific/skills/completing-patch-base`
- `product-specific/skills/writing-documents-base`
- `product-specific/code-reviewer-base/*`

이 영역은 기본 런타임에 자동 포함되지 않는다.
장기적으로는 첫 번째 product pack 영역으로 본다.

## Runtime Layout

```text
base-harness/
├── AGENTS.md
├── README.md
├── MIGRATION.md
├── skills/
│   ├── using-base-harness/
│   ├── brainstorming-base/
│   ├── writing-plans-base/
│   ├── executing-plans-base/
│   ├── subagent-driven-development-base/
│   ├── dispatching-parallel-agents-base/
│   ├── test-driven-development-base/
│   ├── systematic-debugging-base/
│   ├── verification-before-completion-base/
│   ├── using-feature-branches-base/
│   ├── finishing-a-development-branch-base/
│   ├── requesting-code-review-base/
│   ├── receiving-code-review-base/
│   ├── code-reviewer-base/
│   └── writing-skills-base/
├── product-specific/
│   ├── README.md
│   ├── skills/
│   └── code-reviewer-base/
└── claude/
    ├── README.md
    ├── CLAUDE.md
    ├── settings.json
    └── hooks/
        └── session-start.sh
```

## Runtime Policy

### Codex

- 기본 진입점은 루트 [AGENTS.md](/home/smj/harness/base-harness/AGENTS.md:1)다.
- 루트에는 Codex 전용 `settings.json`이나 hook을 두지 않는다.
- Codex용 추가 runtime asset은 실제 필요가 확인될 때만 도입한다.

### Claude

- Claude 자산은 [claude](/home/smj/harness/base-harness/claude) 아래에 모아 둔다.
- Claude 사용자는 이 디렉토리를 선택형 runtime pack으로 사용한다.
- 자세한 배치와 설치 전제는 [claude/README.md](/home/smj/harness/base-harness/claude/README.md:1)를 본다.

## 문서 역할

- [AGENTS.md](/home/smj/harness/base-harness/AGENTS.md:1): Codex 기본 런타임 규칙
- [README.md](/home/smj/harness/base-harness/README.md:1): 구조와 사용법
- [MIGRATION.md](/home/smj/harness/base-harness/MIGRATION.md:1): 마이그레이션 기록

## 참고

현재까지의 추출 과정과 판단 로그는 [MIGRATION.md](/home/smj/harness/base-harness/MIGRATION.md:1)에 유지한다.
