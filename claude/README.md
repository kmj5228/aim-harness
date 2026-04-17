# Claude Runtime Pack

이 디렉토리는 `base-harness`의 선택형 Claude runtime pack이다.

원칙:

- 루트 `AGENTS.md`가 기본 Codex 런타임 규칙이다.
- `claude/`는 Claude 사용자를 위한 보조 자산만 담는다.
- 이 디렉토리 안의 파일은 소스 저장 위치일 뿐이고, 실제 사용 시에는 Claude 런타임 레이아웃에 맞게 배치해야 한다.

포함 파일:

- `claude/CLAUDE.md`
- `claude/settings.json`
- `claude/hooks/session-start.sh`

설치 전제:

- `settings.json`과 `hooks/session-start.sh`는 `.claude/` 레이아웃을 기준으로 작성돼 있다.
- 따라서 필요하면 이 디렉토리의 파일을 `.claude/` 구조에 맞게 복사하거나 패킹해서 사용한다.
