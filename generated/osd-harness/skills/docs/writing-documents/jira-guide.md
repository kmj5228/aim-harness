# OSD Jira Writing Guide

## Default Access

- Jira MCP first
- API fallback only when needed
- auth fallback path: `agent/info/access.md`

## Writing Rules

- 기존 `Problem`, `Goal`은 특별한 이유가 없으면 유지
- 실제 OSD 변경 영역을 명시:
  - `src/lib`, `src/server`, `src/tool`, `src/util`
  - code tables
  - `dist/` operational flow
- runtime 검증은 `make`, `make -C test`, `test/run_coverage.sh` 기준으로 적는다
- packaging script 실행을 일반적인 runtime 검증처럼 쓰지 않는다
