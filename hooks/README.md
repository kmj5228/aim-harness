# Codex Hook Source

이 디렉토리는 `base-harness`의 Codex hook source-of-truth다.

포함 파일:

- `hooks/config.toml`
- `hooks/hooks.json`
- `hooks/session-start.sh`

역할:

- `config.toml`: Codex hook feature flag 예시
- `hooks.json`: Codex 이벤트 훅 정의
- `session-start.sh`: `using-base-harness` 메타 스킬을 세션 시작 시 추가 컨텍스트로 주입

중요:

- 이 디렉토리는 소스 저장 위치다.
- Codex가 이 경로를 자동으로 읽는 것은 아니다.
- 실제 사용하려면 사용자의 `~/.codex/config.toml` 또는 프로젝트 `.codex/config.toml`, `.codex/hooks.json`에 맞게 배치하거나 병합해야 한다.
