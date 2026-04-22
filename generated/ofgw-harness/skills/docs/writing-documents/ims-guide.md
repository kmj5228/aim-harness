# OFGW IMS Writing Guide

## Default Access

- Use the browser-based IMS issue page pattern from the adapter
- Keep IMS numbers explicit when the user asks for IMS-facing output
- Treat IMS writing as a formal external-facing or QA-facing channel

## Recommended Structure

```text
안녕하십니까.
{소속} {이름}입니다.

{결론 또는 목적 한 문단}

1. 원인 또는 배경
2. 현상 또는 영향 범위
3. 조치 계획 또는 요청 사항

감사합니다.
```

## OFGW Rules

- use formal Korean endings consistently
  - `~합니다`
  - `~드립니다`
  - `~부탁드립니다`
- separate:
  - actual changed module
  - inspected-only module
  - user-visible symptom
- for QA or customer-facing IMS text:
  - do not use file names, function names, or code constants
  - describe behavior and configuration impact instead
- if the issue only changed `ofgwSrc`, do not imply `webterminal` or `ofgwAdmin` changed

## Safe Content Pattern

- conclusion first
- symptom next
- module or scope explanation after that
- schedule or next action last

## IMS Save Boundary

- drafting IMS text and saving IMS content are different actions
- draft first, then wait for explicit user approval before any browser-side save or submit action
- do not collapse `write` and `save` into one turn
