---
name: receiving-code-review-aim
description: Use when receiving code review feedback from code-reviewer-aim or human reviewers, before implementing suggestions - requires technical verification, not performative agreement
---

# Receiving Code Review

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for AIM codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, TDD for each fix
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Implementation Order

For multi-item feedback:

1. **Clarify** anything unclear FIRST
2. **Then implement in order:**
   - Critical/security issues → immediate
   - Simple fixes (typos, formatting) → quick batch
   - Logic changes → one at a time with TDD
3. **Test each fix:** `dx make gtest`
4. **Verify no regressions:** `dx make`

**REQUIRED:** Use test-driven-development-aim for each logic fix.

## GitLab MR Discussion Replies

When feedback comes from GitLab MR:

```bash
# Reply to specific discussion (Mac curl, not dx)
curl -s --request POST \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"body": "<response>"}' \
  "http://192.168.51.106/api/v4/projects/211/merge_requests/<MR_IID>/discussions/<DISCUSSION_ID>/notes"
```

Reply in the discussion thread, not as top-level MR comment.

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for AIM/C
- Legacy/compatibility reasons exist
- Conflicts with user's architectural decisions

**How to push back:**
- Technical reasoning, not defensiveness
- Reference working tests/code
- Show evidence from AIM codebase

## Acknowledging Correct Feedback

```
GOOD: "Fixed. [Brief description]"
GOOD: "Good catch - [issue]. Fixed in [file:line]."
GOOD: [Just fix it and show the diff]

BAD: "You're absolutely right!"
BAD: "Thanks for catching that!"
```

Actions speak. Just fix it.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |

## The Bottom Line

**Review feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement with TDD.

## Integration

**Called by:**
- **requesting-code-review-aim** — 셀프 리뷰 후 피드백 처리
- **code-reviewer-aim Phase H** — 타인 리뷰 반영 검증 시
- GitLab MR 피드백 직접 수신

**Uses:**
- **test-driven-development-aim** — 로직 수정 시 TDD
