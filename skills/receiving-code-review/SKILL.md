---
name: receiving-code-review
description: Use when receiving code review feedback from self-review, automated review, or human reviewers before implementing the suggested changes
---

# Receiving Code Review

## Overview

Code review feedback should be evaluated technically, not performed socially.

**Core principle:** Verify feedback before implementing it. Technical correctness comes before agreement theater.

## The Response Pattern

```text
WHEN receiving review feedback:

1. READ: consume the full feedback
2. UNDERSTAND: restate the requirement or concern
3. VERIFY: compare it with code and intended behavior
4. EVALUATE: is the feedback technically correct?
5. RESPOND: acknowledge, question, or push back with evidence
6. IMPLEMENT: fix one meaningful item at a time
```

## Forbidden Responses

Do not:
- Agree performatively before checking
- Promise a fix before understanding the issue
- Treat reviewer comments as automatically correct

Instead:
- Restate the technical concern
- Ask clarifying questions when needed
- Push back with evidence when needed
- Prefer action over empty acknowledgment

## Implementation Order

For multi-item feedback:

1. Clarify unclear items first
2. Triage by severity
   - Critical or correctness issues first
   - Small mechanical fixes next
   - Behavior or logic changes one at a time
3. Re-verify after each meaningful fix

**Required:** Use test-driven-development for logic fixes or bug-related changes.

## When To Push Back

Push back when:
- The suggestion breaks intended behavior
- The reviewer missed important context
- The suggestion conflicts with explicit design decisions
- The suggestion adds unnecessary scope
- The suggestion is technically incorrect

## How To Push Back

- Use technical reasoning
- Reference evidence
- Show the relevant code path, test behavior, or requirement
- Stay concise and factual

## Acknowledging Correct Feedback

Good:

```text
Fixed. Updated validation flow and re-ran tests.
```

```text
Confirmed. The fallback path was wrong; corrected and re-verified.
```

Bad:

```text
You're absolutely right!
```

```text
Great catch, amazing feedback!
```

## Review Channel Guidance

If feedback comes through a specific platform:
- Reply in the repository's normal review channel
- Keep the reply attached to the original review context when possible
- Prefer concise technical updates over status noise

The exact reply mechanism is repository-specific and should follow local review workflow.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State the technical issue or act on it |
| Blind implementation | Verify against code and intent first |
| Large batch fixes without feedback loop | Fix in small verified increments |
| Avoiding pushback when reviewer is wrong | Respond with evidence |
| Treating review as social approval | Treat review as technical quality control |

## Bottom Line

Review feedback is input to evaluate, not an order to obey blindly.

Verify. Question. Fix. Re-verify.

## Integration

**Called by:**
- **requesting-code-review** — after self-review findings
- **code-reviewer** — after structured review output
- Any human or automated review channel

**Uses:**
- **test-driven-development** — when applying logic fixes
- **verification-before-completion** — after review-driven changes
