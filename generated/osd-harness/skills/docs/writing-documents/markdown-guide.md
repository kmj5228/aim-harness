# OSD Markdown Writing Guide

## Core Rules

- 결론 먼저, 근거와 상세는 뒤에 쓴다
- 흐름/구조 설명은 가능하면 `mermaid`를 먼저 쓴다
- topic 문서는 `agent/<topic>/`에 둔다

## OSD Scope Reminder

- 문서가 어떤 영역을 다루는지 명시한다:
  - `src/lib`
  - `src/server`
  - `src/tool`
  - `src/util`
  - `errcode`, `msgcode`, `sysmsg`
  - `dist/`
- 검증되지 않은 영역까지 바뀌었다고 쓰지 않는다
- manual follow-up이 필요하면 `generated/manual/`에 draft를 둔다
