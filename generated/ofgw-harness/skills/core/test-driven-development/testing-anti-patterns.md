# Testing Anti-Patterns (JUnit 5 / Mockito / Kotlin-Java Services)

**Load this reference when:** writing or changing tests in `ofgwSrc`, adding mocks/stubs, or tempted to add test-only seams to production code.

## Overview

Tests must verify real behavior, not stub behavior. Stubs isolate external dependencies, not the thing being tested.

**Core principle:** Test what the code does, not what the stubs do.

**Following strict TDD prevents these anti-patterns.**

## The Iron Laws

```
1. NEVER test stub behavior
2. NEVER add test-only functions to production code
3. NEVER stub without understanding dependencies
```

## Anti-Pattern 1: Testing Stub Behavior

**The violation:**
```kotlin
// BAD: Asserting the exact value injected by the mock
@Test
fun loadsConfig() {
    whenever(configRepository.findValue("key")).thenReturn("test_value")

    val value = service.loadValue("key")

    assertThat(value).isEqualTo("test_value") // proves almost nothing
}
```

**Why this is wrong:**
- You're verifying the stub works, not that the config module works
- Test passes because stub returns fixed value
- Tells you nothing about real behavior

**The fix:**
```kotlin
// GOOD: Test parsing or state transformation with meaningful input
@Test
fun parsesRetryCount() {
    val parsed = configParser.parseLine("retry_count=3")

    assertThat(parsed["retry_count"]).isEqualTo("3")
}
```

## Anti-Pattern 2: Test-Only Functions in Production

**The violation:**
```kotlin
// BAD: production-only-for-tests seam
fun resetStateForTest() {
    internalCache.clear()
}
```

**Why this is wrong:**
- Production code polluted with test-only functions
- Dangerous if accidentally called in production
- Confuses module lifecycle

**The fix:**
```kotlin
// GOOD: Test fixture or explicit setup owns lifecycle
@BeforeEach
fun setUp() {
    service = GatewayService(realValidator, fakeClock)
}

@AfterEach
fun tearDown() {
    fakeClock.reset()
}
```

If no real init/fini exists, the test setup should use only public API.

## Anti-Pattern 3: Over-Stubbing Dependencies

**The violation:**
```kotlin
// BAD: Mocking through the whole call chain
@Test
fun sendsMessage() {
    whenever(queueRepository.findByName("queue_name")).thenReturn(queue)
    whenever(serializer.serialize(payload)).thenReturn(serialized)
    whenever(client.send(queue, serialized)).thenReturn(true)

    val result = service.send("queue_name", payload)

    assertThat(result).isTrue() // mostly confirms your mocks line up
}
```

**The fix:**
Mock only the external boundary you truly need to isolate. Do not replace internal collaborators so aggressively that the test stops exercising real branching, validation, or mapping logic.

## Anti-Pattern 4: Incomplete Test Data

**The violation:**
```kotlin
// BAD: Partial request object missing fields real code depends on
val request = GatewayRequest(
    msgType = REQUEST
    // missing tenantId, requestId, payloadSize
)
```

**The fix:**
```kotlin
// GOOD: Build the request shape the runtime actually expects
val request = GatewayRequest(
    msgType = REQUEST,
    payloadSize = 128,
    tenantId = "TEST_TENANT",
    requestId = "REQ-1"
)
```

## Anti-Pattern 5: Mockito로 implementation detail만 검증

**The violation:**
```kotlin
// BAD: Test only cares that internal helper calls happened
@Test
fun updatesGateway() {
    service.update(command)

    verify(validator).validate(command)
    verify(mapper).toEntity(command)
    verify(repository).save(any())
}
```

**Why this is wrong:**
- This verifies call choreography, not business behavior
- Refactoring internal collaboration can break the test without breaking the feature
- It encourages tests that mirror implementation instead of asserting outcomes

**The fix:**
Assert observable outputs, persisted state, emitted events, or thrown errors instead of verifying every internal helper call.

## Anti-Pattern 6: Private helper testing through reflection or forced visibility

**The violation:**
```kotlin
// BAD: forcing access just to test a private helper
val method = service::class.java.getDeclaredMethod("parseHeader", String::class.java)
method.isAccessible = true
val result = method.invoke(service, rawHeader)
```

**The fix:**
Extract the parsing logic into a collaborator or value object with a public contract, then test that contract directly.

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on stub return value | Test real logic or don't stub it |
| Test-only functions in production | Use test fixtures or public API |
| Stub without understanding | Understand dependency chain first, stub minimally |
| Incomplete test data | Initialize all struct fields matching real data |
| Verify only internal helper calls | Assert observable state, outputs, or errors |
| Reflection/private-helper testing | Extract a public collaborator or value object |

## Red Flags

- Assertion checks stub return values directly
- Functions only called in test files
- Link-time stubs replace functions the test depends on
- Test passes but same scenario fails in production
- Can't explain why a stub is needed
- Stubbing "just to be safe"

## The Bottom Line

**Stubs are tools to isolate external dependencies, not things to test.**

If TDD reveals you're testing stub behavior, you've gone wrong.
Fix: Test real behavior or question why you're stubbing at all.
