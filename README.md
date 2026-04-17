# base-harness

## 소개

`base-harness`는 현재 `aim-harness`를 출발점으로 삼아, 여러 제품에서 재사용 가능한 공통 하네스를 만드는 작업 저장소다.

이 저장소의 목표는 단순 복제가 아니라 분리다.

- 공통 워크플로우는 코어로 남긴다.
- 제품 전용 규칙은 별도 product pack 성격으로 격리한다.
- 지금 당장 일반화하기 어려운 내용은 `legacy` 후보로 표시하고 보존한다.

하네스의 기본 구성은 그대로 유지한다.

```text
Harness = Skills + Agents/Prompts + Repository Rules + Hooks
```

## 현재 상태

현재 `base-harness`는 구조상 이미 별도 저장소이고, 코어 개발 루프와 주요 협업 스킬의 1차 공통화는 완료됐다.

- 메타 스킬과 hook 참조는 `using-base-harness` 기준으로 정리됐다.
- 코어/협업 스킬과 주요 support prompt 본문은 대부분 공통화됐다.
- 남은 잔재의 중심은 `product-specific/`로 분리한 product pack 번들, 일부 product-specific support 파일, 그리고 마이그레이션 기록 문서다.

따라서 이 저장소는 지금 “완성된 공통 하네스”가 아니라, **공통화 작업 중인 베이스 레이어**로 보는 것이 맞다.

짧게 말하면:

- 공통 실행 루프는 이미 `base-harness` 쪽으로 기울었다.
- 남은 문제는 주로 `product-specific/` 번들의 장기 구조와 후속 product-pack 구조 정리다.

## 무엇을 공통화하는가

기본 원칙은 [AGENTS.md](/home/smj/harness/base-harness/AGENTS.md:1)에 정리돼 있다.

1차적으로 제거 또는 분리 대상인 요소:

- 특정 제품명과 조직 용어: `AIM`, `aim-harness`
- 특정 브랜치 정책: `rb_73`
- 특정 실행 래퍼: `dx`
- 특정 협업 도구 결합: `IMS`, `Jira`, `GitLab`, `Confluence`, `NotebookLM`
- 특정 테스트 스택 강제: `GoogleTest`, `gcov`, diff coverage 80%
- 특정 운영 문서 절차: patch verification, `manual-guide`

이 요소들은 즉시 삭제하지 않고 아래 셋 중 하나로 다룬다.

- 공통 개념으로 일반화
- product pack 후보로 격리
- 현재 라운드에서 보존하되 제품 전용으로 명시

## 스킬 분류

현재 스킬 이름은 1차 rename이 끝나 `*-base` 기준으로 정리됐다. 다만 일부 스킬은 내용상 여전히 product-specific product pack 성격을 가진다.

### 공통 코어 후보

| 스킬 | 비고 |
|------|------|
| `brainstorming-base` | 설계 절차는 공통화 가능, 외부 도구 의존 제거 필요 |
| `writing-plans-base` | 태스크 분해/TDD 체크포인트는 공통화 가능 |
| `executing-plans-base` | 실행 gate는 공통화 가능, 명령은 파라미터화 필요 |
| `test-driven-development-base` | 핵심 루프는 공통화 가능, 테스트 스택 고정 제거 필요 |
| `systematic-debugging-base` | 디버깅 절차는 공통화 가능 |
| `verification-before-completion-base` | 완료 전 검증 규칙은 공통화 가능 |
| `writing-skills-base` | 스킬 작성 방법론의 1차 공통화 완료 |

### 협업 레이어 후보

| 스킬 | 비고 |
|------|------|
| `subagent-driven-development-base` | 서브에이전트 패턴은 공통화 가능 |
| `dispatching-parallel-agents-base` | 병렬 분배 규칙은 공통화 가능 |
| `using-feature-branches-base` | 브랜치 전략은 일반화 가능, 현재 규칙은 제품 종속 |
| `requesting-code-review-base` | 셀프 리뷰 루프는 공통화 가능 |
| `receiving-code-review-base` | 피드백 처리 루프는 공통화 가능 |
| `code-reviewer-base` | 리뷰 구조는 재사용 가능하나 외부 연동 의존 큼 |
| `finishing-a-development-branch-base` | 완료/정리 절차는 일반화 가능, MR/manual 세부는 분리 필요 |

### Product Packs

| 번들 | 이유 |
|------|------|
| `product-specific/skills/issue-analysis-base` | IMS/Jira/NotebookLM 흐름 의존 |
| `product-specific/skills/completing-patch-base` | IMS patch verification 절차 의존 |
| `product-specific/skills/writing-documents-base` | 문서 작성 자체는 공통화 가능하지만 현재는 도구/플랫폼 결합이 강함 |
| `product-specific/code-reviewer-base/*` | 외부 시스템/API/coverage 정책 결합이 강한 지원 자산 |

이 번들은 기본 `skills/` 라우팅에서 분리해 `product-specific/`로 이동했다.

- `issue-analysis-base`: 제품/조직의 이슈 트리아지 예시
- `completing-patch-base`: 제품별 배포 후속/검증 문서 예시
- `writing-documents-base`: 다중 협업 도구 연동 예시
- `code-reviewer-base` product-specific assets: 정보 수집/커버리지 측정 자산

후속 단계에서는 이들을 명시적 product-pack 구조로 더 정리한다.

- 공통 개념만 추출해 새 코어 스킬로 재구성
- 제품 전용 pack으로 유지
- 장기적으로 `product-packs/<product>/` 구조로 승격

현재 유지 정책은 단순하다.

- 코어 가치가 분명한 문서는 공통화한다.
- 외부 시스템/API/조직 절차에 강하게 묶인 문서는 `product-specific/`로 분리해 둔다.
- 스킬명 rename은 1차 완료됐고, 남은 정리는 product-specific pack의 최종 구조 문제다.

배치 정책도 함께 고정한다.

- 현재는 `product-specific/`로 1차 분리까지 완료했다.
- 이 디렉토리는 장기적으로 첫 번째 product pack 영역으로 해석한다.

### 메타

| 스킬 | 비고 |
|------|------|
| `using-base-harness` | SessionStart hook으로 자동 주입되는 메타 스킬 |

## 추출 순서

작업은 크게 다섯 단계로 나눈다.

1. 메타 문서 공통화: `AGENTS.md`, `README.md`, `CLAUDE.md`
2. hook 메시지와 설정의 `aim-harness` 잔재 정리
3. 공통 코어 스킬 1차 정리
4. 협업 레이어 스킬 일반화
5. 제품 전용 스킬을 product pack 후보로 분리

상세 체크리스트와 진행 기록은 [MIGRATION.md](/home/smj/harness/base-harness/MIGRATION.md:1)에 유지한다.

## 현재 워크플로우 해석

`base-harness`는 아직 이름과 내부 절차가 뒤섞여 있으므로, 당분간 워크플로우를 아래처럼 해석한다.

```text
Design
  -> Plan
  -> Execute
  -> Test / Debug
  -> Verify
  -> Review / Collaboration
  -> Product-specific completion steps (optional)
```

즉, 설계-계획-실행-검증 루프는 공통 코어로 살리고, 이슈 트래킹/문서/배포 후속 절차는 제품별 확장으로 밀어낸다.

## 디렉토리 구조

```text
base-harness/
├── AGENTS.md
├── README.md
├── CLAUDE.md
├── MIGRATION.md
├── settings.json
├── hooks/
│   └── session-start.sh
└── skills/
    ├── using-base-harness/
    ├── brainstorming-base/
    ├── writing-plans-base/
    ├── executing-plans-base/
    ├── subagent-driven-development-base/
    ├── dispatching-parallel-agents-base/
    ├── test-driven-development-base/
    ├── systematic-debugging-base/
    ├── verification-before-completion-base/
    ├── using-feature-branches-base/
    ├── finishing-a-development-branch-base/
    ├── requesting-code-review-base/
    ├── receiving-code-review-base/
    ├── code-reviewer-base/
    └── writing-skills-base/
product-specific/
├── skills/
│   ├── issue-analysis-base/
│   ├── completing-patch-base/
│   └── writing-documents-base/
└── code-reviewer-base/
    ├── info-collector-prompt.md
    ├── coverage-analyst-prompt.md
    └── scripts/
```

## 설치 관점 참고

최종 목표는 프로젝트가 이 저장소의 결과물을 자신의 `.claude/` 또는 동등한 하네스 경로에 설치해서 사용할 수 있게 만드는 것이다.

현재 단계에서는 설치 문서보다 공통화 기준을 먼저 다룬다.

- `settings.json`은 hook 연결 지점을 보여주는 예시다.
- `hooks/session-start.sh`는 메타 스킬 자동 주입 예시다.
- `skills/`는 기본 base runtime skill set이다.
- `product-specific/`는 첫 번째 product pack 번들을 분리 보관하는 영역이다.

설치 방법은 코어/product-pack 구조가 더 안정되면 다시 정리한다.
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```
