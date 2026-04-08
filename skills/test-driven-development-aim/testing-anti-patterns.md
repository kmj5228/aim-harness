# Testing Anti-Patterns (C/GoogleTest)

**Load this reference when:** writing or changing tests, adding stubs/wrappers, or tempted to add test-only methods to production code.

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
```cpp
// BAD: Testing that the stub returns what we told it to
TEST(AimConfig, LoadsConfig) {
    // stub always returns "test_value"
    const char *val = aim_config_get("key");
    EXPECT_STREQ(val, "test_value");  // proves nothing!
}
```

**Why this is wrong:**
- You're verifying the stub works, not that the config module works
- Test passes because stub returns fixed value
- Tells you nothing about real behavior

**The fix:**
```cpp
// GOOD: Test with real config file or test the parsing logic
TEST(AimConfig, ParsesKeyValuePair) {
    aim_config_t cfg;
    int rc = aim_config_parse_line(&cfg, "retry_count=3");
    EXPECT_EQ(rc, AIM_OK);
    EXPECT_EQ(aim_config_get_int(&cfg, "retry_count"), 3);
}
```

## Anti-Pattern 2: Test-Only Functions in Production

**The violation:**
```c
// BAD: _aim_reset_internal_state() only used in tests
void _aim_reset_internal_state(void) {
    memset(&g_state, 0, sizeof(g_state));
}
```

**Why this is wrong:**
- Production code polluted with test-only functions
- Dangerous if accidentally called in production
- Confuses module lifecycle

**The fix:**
```cpp
// GOOD: Test fixture handles setup/teardown
class AimStateTest : public ::testing::Test {
protected:
    void SetUp() override {
        aim_init();  // use real init
    }
    void TearDown() override {
        aim_fini();  // use real cleanup
    }
};
```

If no real init/fini exists, the test setup should use only public API.

## Anti-Pattern 3: Over-Stubbing Dependencies

**The violation:**
```cpp
// BAD: Stubbing too much, breaking the logic under test
// Stub replaces aim_mqn_lookup which the function being tested depends on
int aim_mqn_lookup(const char *name) { return 0; }  // link-time stub

TEST(AimSend, SendsMessage) {
    // aim_send internally calls aim_mqn_lookup
    // but stub always returns 0, hiding real lookup behavior
    int rc = aim_send("queue_name", data, len);
    EXPECT_EQ(rc, AIM_OK);  // false confidence
}
```

**The fix:**
Stub only the lowest-level external dependency (e.g., actual socket/IPC call), not intermediate functions the code under test depends on.

## Anti-Pattern 4: Incomplete Test Data

**The violation:**
```cpp
// BAD: Partial struct - only fields you think you need
aim_msg_header_t hdr = {0};
hdr.msg_type = AIM_MSG_REQUEST;
// Missing: hdr.msg_len, hdr.src_id, hdr.timestamp
// Code crashes when accessing unset fields
```

**The fix:**
```cpp
// GOOD: Complete struct matching real data
aim_msg_header_t hdr = {
    .msg_type = AIM_MSG_REQUEST,
    .msg_len = 128,
    .src_id = "TEST_SRC",
    .timestamp = time(NULL)
};
```

## Anti-Pattern 5: Static Function Not Promoted

**The violation:**
```c
// BAD: Can't test because static
static int _parse_header(const char *buf, aim_header_t *hdr) { ... }
```

**The fix:**
```c
// GOOD: Promote for testing (see AGENTS.md static function rules)
// In {source}.h:
int _parse_header(const char *buf, aim_header_t *hdr);

// In {source}.c: remove static, include {source}.h
```

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on stub return value | Test real logic or don't stub it |
| Test-only functions in production | Use test fixtures or public API |
| Stub without understanding | Understand dependency chain first, stub minimally |
| Incomplete test data | Initialize all struct fields matching real data |
| Static can't be tested | Promote to header per AGENTS.md convention |

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
