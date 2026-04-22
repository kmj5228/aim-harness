# Codex Hooks

이 디렉토리는 generated `ofgw-harness`의 hook 초안이다.

포함 파일:

- `hooks/config.toml`
- `hooks/hooks.json`
- `hooks/session-start.sh`

역할:

- `config.toml`: Codex hook feature flag 예시
- `hooks.json`: generated harness 기준 SessionStart 훅 정의
- `session-start.sh`: generated `AGENTS.md`를 세션 시작 컨텍스트로 주입

중요:

- 이 디렉토리는 generated harness 내부의 hook 초안이다.
- 사용자의 Codex 런타임에 자동 반영되지는 않는다.
- 실제 사용하려면 사용자의 `~/.codex/config.toml` 또는 프로젝트 `.codex/` 레이아웃에 맞게 배치하거나 병합해야 한다.
