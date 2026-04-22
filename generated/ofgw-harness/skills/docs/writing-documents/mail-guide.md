# OFGW Mail Writing Guide

## Purpose

Use this guide when the user needs email-style communication rather than repo markdown, PR text, or IMS action text.

## Subject Pattern

```text
[OFGW/<issue-id>/<topic>] one-line summary
```

Use a subject that lets the recipient predict the body without opening the mail.

## Body Structure

```text
안녕하십니까.
{소속} {이름}입니다.

{목적 한 문장}

1. 배경 또는 원인
2. 변경 사항 또는 대응 내용
3. 검증 결과 또는 요청 사항

감사합니다.

{이름} 드림
```

## OFGW Rules

- use formal Korean consistently
- keep sections short and numbered
- avoid decorative separators
- choose abstraction level by recipient:
  - internal engineering audience: module-level wording is acceptable
  - external or broad audience: behavior-level wording only
- call out the real touched surface:
  - `ofgwSrc`
  - `webterminal`
  - `ofgwAdmin`
  - config/resources
  - scripts

## Evidence Guidance

- prefer compile/test/coverage evidence from the confirmed backend path:
  - `:ofgwSrc:classes`
  - `:ofgwSrc:test`
  - `:ofgwSrc:jacocoTestReport`
- do not imply release packaging or admin/frontend validation unless it actually happened

## Approval Rule

- drafting mail content and sending mail are separate actions
- always stop after the draft and wait for explicit user approval before any send action
