# OFGW Analysis Summary

## Selected Templates

- `issue-analysis`
- `writing-documents`
- `markdown-guide` as support reference only

## Inferred Repository Facts

- Build systems: `gradle`, `pnpm`
- Primary languages: `java`, `kotlin`, `javascript`
- Main modules:
  - `ofgwSrc`
  - `webterminal`
  - `ofgwAdmin`
- Runtime hints:
  - `jeus`
  - `servlet`
  - `websocket`
  - `jpa`
  - `querydsl`
- Test frameworks:
  - `junit5`
  - `mockito`
  - `assertj`
  - `hamcrest`
- Coverage tool: `jacoco`

## Inferred Commands

- Safe compile-oriented build:
  - `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:classes --no-daemon`
- Test:
  - `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:test --no-daemon`
- Coverage:
  - `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:jacocoTestReport --no-daemon`

## Excluded Or Ops-Locked Assets

- `completing-patch`
- `manual-guide`
- coverage-specific prompt/script assets
- full `generated/ofgw-harness/` rollout beyond the minimal first-pass skeleton

## Red Flags

- `ofgw` is a mixed-stack validation target and should not rewrite template bodies around JVM or frontend specifics.
- Root packaging tasks can mutate version files and create git commits:
  - `:ofgwSrc:jar`
  - `:webterminal:war`
- `ofgwAdmin` is built with `pnpm` and separate packaging steps, but it is outside the first generated template scope.
- Repository guidelines mention Jira and PR expectations, but they do not confirm the generated harness workflow fields by themselves.

## Evidence

- Root repo guide: `/home/woosuk_jung/harness/ofgw/AGENTS.md`
- Root build orchestration: `/home/woosuk_jung/harness/ofgw/build.gradle`
- Core module build/test/coverage: `/home/woosuk_jung/harness/ofgw/ofgwSrc/build.gradle`
- Admin frontend guide: `/home/woosuk_jung/harness/ofgw/ofgwAdmin/AGENTS.md`
