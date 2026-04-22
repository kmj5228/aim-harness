# Testing Anti-Patterns

**Load this reference when:** writing or changing tests, adding stubs or wrappers, or feeling pressure to change production code just to make tests easier.

## Overview

Tests must verify real behavior, not fake behavior created by the test itself.

**Core principle:** Test what the system does, not what the test double does.

## The Iron Laws

```text
1. NEVER test stub behavior
2. NEVER add test-only functions to production code
3. NEVER stub without understanding the dependency boundary
```

## Anti-Pattern 1: Testing Stub Behavior

**The violation:**

```ts
// BAD: testing the stubbed value rather than the production logic
it("loads configuration", () => {
  fakeConfigStore.get.mockReturnValue("test-value");
  expect(loadConfig("key")).toBe("test-value");
});
```

**Why this is wrong:**

- The test proves the stub returned the configured value
- It does not prove the real parsing, lookup, or fallback logic works
- It creates false confidence

**The fix:**

```ts
// GOOD: test the real parsing logic or a realistic integration boundary
it("parses retry_count from configuration text", () => {
  const cfg = parseConfigLine("retry_count=3");
  expect(cfg.retryCount).toBe(3);
});
```

## Anti-Pattern 2: Test-Only Functions in Production

**The violation:**

```js
// BAD: added only so tests can reset hidden state
export function _resetInternalStateForTests() {
  internalState = createEmptyState();
}
```

**Why this is wrong:**

- Production code is bent around the test
- Internal lifecycle becomes less clear
- The test stops exercising real setup and teardown behavior

**The fix:**

- Use public setup/cleanup APIs if they exist
- Use fixtures, factories, or repository-supported test hooks
- If the code is impossible to reset cleanly, revisit the design boundary instead of adding test-only escape hatches

## Anti-Pattern 3: Over-Stubbing Dependencies

**The violation:**

```ts
// BAD: replacing the logic that the behavior under test actually depends on
vi.spyOn(queueLookup, "find").mockReturnValue({ id: "q1" });

it("sends the message", async () => {
  await sendMessage("orders", payload);
  expect(sendTransport).toHaveBeenCalled();
});
```

**Why this is wrong:**

- The lookup path itself may be the risky behavior
- The test may still pass while the real code fails

**The fix:**

- Stub only the lowest external boundary you need to isolate
- Keep the internal decision path real whenever possible

## Anti-Pattern 4: Incomplete Test Data

**The violation:**

```ts
// BAD: partial object missing fields real code depends on
const request = {
  type: "create"
};
```

**Why this is wrong:**

- Real code often depends on fields the test forgot
- Crashes and invalid branches appear only outside the test

**The fix:**

- Build test data that matches realistic shapes
- Prefer complete fixtures with intentional overrides

```ts
const request = buildRequest({
  type: "create",
  actorId: "user-1",
  timestamp: 1710000000,
  payload: { name: "sample" }
});
```

## Anti-Pattern 5: Language-Specific Initialization Shortcuts

**The violation:**

```cpp
// BAD: shortcut initialization that does not match the active language rules
WidgetState state = {0};
```

**Why this is wrong:**

- Some initialization idioms are valid in one language or type shape but unsafe or invalid in another
- Tests become brittle or fail for the wrong reason

**The fix:**

- Use the initialization style that is correct for the active language and type
- Prefer repository-standard fixture builders or explicit constructors when available

## Anti-Pattern 6: Hiding Untestable Design Behind `static` or Private Scope

**The violation:**

```c
static int parse_header(const char *buf, header_t *hdr) { ... }
```

**Why this is risky:**

- Sometimes the helper is simple and should stay private
- Sometimes the helper contains core behavior that now has no realistic test path

**The fix:**

- First ask whether the behavior should be testable through the public interface
- If not, consider extracting a small testable unit through repository-approved patterns
- Do not weaken encapsulation casually; change the boundary only when the design justifies it

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on stub return value | Test real logic or a realistic boundary |
| Test-only functions in production | Use fixtures, public lifecycle, or redesign the boundary |
| Stub without understanding | Map the dependency chain first, then stub minimally |
| Incomplete test data | Use realistic fixtures and complete inputs |
| Wrong-language initialization shortcut | Use valid initialization for the actual language and type |
| Untestable hidden helper | Reassess the boundary instead of exposing internals by reflex |

## Red Flags

- The assertion proves only what the stub was configured to return
- A function exists only because tests needed it
- The test replaces multiple layers of the real behavior
- The same scenario fails outside the test but passes inside it
- You cannot explain why a stub is needed at that exact boundary

## Bottom Line

Test doubles should isolate external dependencies, not replace the behavior you claim to be verifying.

If the test mainly proves the fake behaves as instructed, the test is not protecting you.
