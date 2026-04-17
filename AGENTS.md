# Base Harness Agent Guide

## Purpose

`base-harness`는 현재 `aim-harness`를 출발점으로 삼아, 여러 제품에서 재사용할 수 있는 공통 하네스로 정리하는 저장소다.

이 저장소에서의 작업 목표는 세 가지다.

1. AIM 전용 규칙과 용어를 식별한다.
2. 다른 제품에도 그대로 적용 가능한 공통 워크플로우만 남긴다.
3. 제품별 차이는 별도 adapter/example 레이어로 분리할 수 있게 만든다.

## Current State

- 현재 `base-harness`는 `aim-harness`의 복제본에 가깝다.
- 파일명, 스킬명, 설명, hook 메시지에 `aim` 용어와 AIM 전용 프로세스가 아직 많이 남아 있다.
- 따라서 현 시점의 `base-harness` 내용은 최종 정책이 아니라, 공통화 대상 원본으로 취급한다.

## What Counts As Product-Specific

아래 요소는 기본적으로 공통 코어가 아니라 제품 종속으로 본다.

- 특정 조직/제품명: `AIM`, `IMS`, 사내 시스템명
- 특정 브랜치 정책: `rb_73` 같은 팀 전용 Git 규칙
- 특정 실행 래퍼: `dx`, `dev_exec.sh`
- 특정 협업 도구 강결합: Jira, GitLab, Confluence, NotebookLM
- 특정 테스트 스택 강제: GoogleTest, gcov 80% 같은 고정 조합
- 특정 문서/배포 절차: patch verification, manual guide 같은 AIM 운영 절차

이런 요소는 삭제보다 먼저 아래 셋 중 하나로 재분류한다.

- 공통 개념으로 일반화
- 제품 adapter/example로 격리
- 당장 재사용 가치가 없으면 제거 후보로 표시

## Core Principles

- 공통 하네스는 특정 제품명을 몰라도 이해되고 적용 가능해야 한다.
- 워크플로우는 유지하되, 도구와 조직 정책은 파라미터화한다.
- 한 번에 크게 갈아엎지 말고, 문서와 스킬을 작은 단위로 분리한다.
- 이름을 바꾸면 참조도 함께 바꾼다. 반쪽 rename은 금지한다.
- 설명보다 구조를 먼저 공통화한다. 즉, 용어 교체만 하고 내부 절차가 그대로 AIM 종속이면 완료가 아니다.

## Migration Rules

### 1. Preserve the Harness Shape

다음 4개 축은 유지한다.

- `skills/`: 작업 방식 자체를 정의하는 재사용 가능한 지침
- `AGENTS.md`, `CLAUDE.md`: 저장소 단위 규칙과 라우팅
- `hooks/`: 세션 시작 시 주입할 최소 컨텍스트
- `settings.json`: hook 연결 지점

### 2. Separate Core From Example

공통화할 때는 가능한 한 아래 구조를 목표로 한다.

- core: 제품과 무관한 절차
- adapter: 특정 제품/팀 도구에 맞춘 치환 규칙
- example: AIM 같은 기존 구현 예시

아직 구조 개편 전이라도, 문서 안에서는 이 구분을 명시적으로 드러낸다.

### 3. Rename Carefully

- `*-aim` 접미사는 당장은 과도기 이름으로 본다.
- 실제 rename은 관련 문서, hook, settings, cross-reference를 한 번에 맞출 수 있을 때만 한다.
- 이름만 일반화하고 내용이 AIM 전용이면 rename하지 않는다.

### 4. Prefer Parameterization Over Hardcoding

예:

- `dx make test` → `<project_test_command>`
- `GitLab MR` → `code review / merge workflow`
- `IMS issue` → `issue tracker item`

단, 너무 추상적이어서 실행 불가능해지면 안 된다. 추상화할 때는 최소 1개의 concrete example을 남긴다.

## Skill Editing Rules

- 스킬을 수정할 때는 먼저 그 스킬이 공통 코어인지, AIM 전용인지 분류한다.
- 공통 코어 스킬은 trigger, workflow, verification을 제품 중립적으로 다시 쓴다.
- AIM 전용 스킬은 억지로 일반화하지 말고, 왜 전용인지 문서에 남긴다.
- 스킬 간 중복 설명은 줄이고, 공통 규칙은 `AGENTS.md` 또는 `CLAUDE.md`로 올린다.
- 새 스킬을 추가한다면 이름부터 제품 중립적으로 설계한다.

## Recommended Extraction Order

우선순위는 아래 순서를 기본으로 한다.

1. 메타 문서: `AGENTS.md`, `README.md`, `CLAUDE.md`
2. 공통 개발 루프: brainstorming, plans, execution, TDD, debugging, verification
3. 협업 루프: branch, review, completion
4. AIM 전용 절차: issue analysis, patch completion, manual/document workflow
5. hook 및 settings의 AIM 잔재 제거

## Definition Of Done

어떤 문서나 스킬이 `base-harness`에 맞게 정리됐다고 보려면 최소 아래를 만족해야 한다.

- 특정 제품명 없이도 언제 쓰는지 이해된다.
- 특정 사내 도구 없이도 절차가 성립한다.
- 필요 시 치환할 변수나 adapter 포인트가 보인다.
- 관련 cross-reference가 끊어지지 않는다.
- AIM 예시는 있어도, 규칙 본문은 AIM에 종속되지 않는다.

## Change Safety

- 대량 rename, 대량 이동, 스킬 일괄 삭제는 한 번에 하지 않는다.
- 공통화 과정에서 정보가 빠지면, 삭제 대신 `example`, `legacy`, `product-specific` 성격으로 먼저 표시한다.
- hook, settings, 문서 경로는 쉽게 깨지므로 파일 이동 전후에 참조를 반드시 다시 확인한다.

## Decision Heuristic

판단이 애매하면 아래 순서로 결정한다.

1. 이 규칙이 다른 제품에서도 그대로 유효한가?
2. 아니라면 제품 adapter로 분리할 수 있는가?
3. 그것도 아니라면 AIM example/legacy로 남겨야 하는가?
4. 셋 다 아니면 제거 후보다.

## Immediate Working Assumption

별도 지시가 없으면, 현재 작업은 `aim-harness`를 한 번에 새로 쓰는 것이 아니라 `base-harness`를 점진적으로 경량화하는 방향으로 진행한다.
