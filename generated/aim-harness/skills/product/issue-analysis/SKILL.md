---
name: issue-analysis
description: Use when an IMS issue or Jira ticket needs analysis to determine if it's a bug, expected behavior, configuration error, or unsupported feature before deciding next action
---

# Issue Analysis

## Overview

Systematically analyze an IMS issue to determine root cause and classify the verdict before taking action.

**Core principle:** Analyze first, act second. The verdict determines the action — never skip to fixing without understanding.

<HARD-GATE>
Do NOT start coding, brainstorming, or planning until the analysis is complete and the verdict is determined. Even if the fix seems obvious from the issue title.
</HARD-GATE>

## When to Use

- IMS issue assigned or reported
- Jira ticket needs investigation
- Customer-reported problem needs triage
- Need to determine if something is a bug or expected behavior

## Checklist

Complete in order:

1. **Gather context** — IMS issue, Jira ticket, related MRs
2. **Understand the symptom** — exact error, reproduction steps, environment
3. **Analyze code** — trace the execution path, find the root cause
4. **Reference spec** — check XSP specification via NotebookLM (사용자가 명시적으로 불필요하다고 하지 않는 한 필수)
5. **Determine verdict** — classify into one of 4 categories
6. **Take verdict-specific action** — see Verdict Actions below
7. **Write analysis report** — save to `agent/<topic>/analysis_report.md`

## Information Gathering

### IMS Issue

Open in Chrome browser automation:
```
URL 패턴: https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>
예: ims350846 → https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=350846
```

사용자가 "ims{번호}" 또는 "ims {번호}"로 요청하면 위 URL로 접근.

Extract: symptom description, customer environment, error messages, reproduction steps.

### Jira Ticket

**Jira는 REST API로 접근한다. Chrome 브라우저 자동화를 사용하지 않는다.** (IMS만 Chrome 사용)

```bash
# Mac curl (not dx) — Jira REST API
# 인증 정보: agent/info/access.md 참조
curl -s -u "<EMAIL>:<API_TOKEN>" \
  "https://tmaxsoft.atlassian.net/rest/api/2/issue/<JIRA_KEY>" | jq '.fields.summary, .fields.description'
```

### XSP Specification

XSP 스펙을 **항상** 참조한다. 모호하지 않더라도 확인한다. 사용자가 처음에 "스펙 확인 불필요"라고 명시한 경우에만 생략 가능.

- Notebook ID: `xsp-specification`
- **반드시 "XSP 스펙을 참조합니다"라고 사용자에게 알린 후 참조**
- `mcp__notebooklm__ask_question` 도구 사용
- **실패 시 재인증 후 재시도**: NotebookLM은 인증 만료로 자주 실패함. 실패하면 `mcp__notebooklm__re_auth` 또는 `notebooklm.auth-repair` prompt로 재인증 후 다시 시도. 실패를 이유로 스펙 참조를 건너뛰지 않는다.

### Code Trace

```bash
dx bash -c "rg 'function_or_error_pattern' /root/ofsrc/aim/src/"
```

Trace the execution path from symptom to root cause.

## Verdict Classification

| Verdict | Criteria | Action |
|---------|----------|--------|
| **Bug** | Code doesn't match spec or intended behavior | → brainstorming (pass analysis_report.md) |
| **Expected behavior** | Code matches spec, customer misunderstands | → Draft IMS response explaining correct behavior |
| **Configuration error** | Customer's environment misconfigured | → Draft customer guide with correct settings |
| **Unsupported feature** | Requested behavior not in spec | → Draft Jira feature request |

## Verdict Actions

### Bug → Development Pipeline

```
analysis_report.md exists
  └─→ brainstorming (skip re-collection, use analysis_report.md)
        └─→ writing-plans → executing-plans → ...
```

**Key:** brainstorming checks for `analysis_report.md`. If present, it skips the information gathering phase and uses the analysis directly.

### Expected Behavior → IMS Response

Draft a clear response explaining:
- What the correct behavior is
- Where in the spec this is defined
- Steps the customer should follow

Present draft to user for review before posting.

### Configuration Error → Customer Guide

Draft a guide with:
- What's misconfigured
- Correct configuration values
- Verification steps

### Unsupported Feature → Jira Feature Request

Draft with:
- Feature description
- Use case from customer
- Spec reference showing current scope


## Cross-Reference

- IMS 응답/가이드 초안 작성 시: **writing-documents**의 ims-guide.md 참조
- Jira feature request 초안 작성 시: **writing-documents**의 jira-guide.md 참조
- analysis_report.md 구조: **writing-documents**의 markdown-guide.md "분석 보고서" 참조

## Output

Save to `agent/<topic>/analysis_report.md`:

```markdown
# Issue Analysis: <topic>

## Issue Info
- IMS: <number>
- Jira: <key>
- Reporter: <customer/team>

## Symptom
<exact error, environment, reproduction>

## Root Cause Analysis
<code trace, logic analysis>

## Spec Reference
<XSP spec findings, if applicable>

## Verdict: <Bug | Expected Behavior | Configuration Error | Unsupported Feature>

## Rationale
<why this verdict>

## Recommended Action
<specific next step>
```

## Red Flags

- Starting to code before analysis is complete
- Assuming "bug" without tracing the code
- Skipping spec reference ("모호하지 않으니 불필요" — 합리화. 사용자가 생략하라고 하지 않았으면 필수)
- Writing an IMS response without understanding the root cause
- Jumping to brainstorming without analysis_report.md

## Common Mistakes

### Assuming the customer is wrong

- **Problem:** Dismissing as "expected behavior" without code trace
- **Fix:** Always trace the execution path regardless of initial assumption

### Fixing without understanding

- **Problem:** Patching the symptom instead of the root cause
- **Fix:** Complete the full analysis before any fix attempt

### Skipping spec check

- **Problem:** "Bug" verdict when behavior actually matches spec
- **Fix:** XSP 스펙을 항상 참조. "모호하지 않으니 불필요" 는 합리화

## Integration

**Called by:** 직접 호출 (체인 진입점)

**Feeds into (verdict별):**
- **brainstorming** — Bug/기능 필요 시 (analysis_report.md 전달, 재수집 skip)
- **writing-documents** — IMS 답변/Jira feature request 초안 작성 시
