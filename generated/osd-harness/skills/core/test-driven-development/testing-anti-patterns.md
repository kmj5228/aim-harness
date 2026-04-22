# Testing Anti-Patterns (OSD / C / GoogleTest)

**Load this reference when:** writing or changing tests, adding stubs or wrappers, or when a shortcut would make `make -C test` green without proving real behavior.

## Overview

Tests must verify real behavior, not stub behavior. Stubs isolate external dependencies, not the thing being tested.

**Core principle:** Test what the code does, not what the test doubles do.

## The Iron Laws

```text
1. NEVER test stub behavior
2. NEVER add test-only functions to production code
3. NEVER stub without understanding the dependency chain
```

## Anti-Pattern 1: Testing Stub Behavior

**The violation:**

```cpp
TEST(OsdConfig, LoadsValue) {
    const char *value = osd_config_get("key");
    EXPECT_STREQ(value, "test_value");
}
```

**Why this is wrong:**

- it proves the stub returns what you hard-coded
- it does not prove `osd_config_get()` works against real input

**The fix:**

```cpp
TEST(OsdConfig, ParsesKeyValuePair) {
    osd_config_t cfg{};
    ASSERT_EQ(osd_config_parse_line(&cfg, "retry_count=3"), OSD_OK);
    EXPECT_EQ(osd_config_get_int(&cfg, "retry_count"), 3);
}
```

## Anti-Pattern 2: Test-Only Functions In Production

**The violation:**

```c
void _osd_reset_internal_state(void) {
    memset(&g_state, 0, sizeof(g_state));
}
```

**Why this is wrong:**

- production code now exposes a test-only lifecycle hook
- the test becomes coupled to internals instead of public behavior

**The fix:**

- prefer real init/fini API
- if no lifecycle API exists, use public setup paths in the test fixture

## Anti-Pattern 3: Over-Stubbing Dependencies

**The violation:**

```cpp
int osd_lookup_target(const char *name) { return 0; }

TEST(OsdSend, SendsMessage) {
    int rc = osd_send("queue_name", data, len);
    EXPECT_EQ(rc, OSD_OK);
}
```

**Why this is wrong:**

- if `osd_send()` depends on `osd_lookup_target()`, the stub may hide the real failure mode

**The fix:**

- stub the lowest-level external dependency
- keep the intermediate lookup or routing logic real when that is what the test is supposed to verify

## Anti-Pattern 4: Incomplete Test Data

**The violation:**

```cpp
osd_msg_header_t hdr = {0};
hdr.msg_type = OSD_MSG_REQUEST;
```

**The fix:**

```cpp
osd_msg_header_t hdr{};
hdr.msg_type = OSD_MSG_REQUEST;
hdr.msg_len = 128;
strcpy(hdr.src_id, "TEST_SRC");
```

Populate fields the real code path expects.

## Anti-Pattern 5: C Struct `= {0}` In C++ GoogleTest

**The violation:**

```cpp
TEST(OsdAssign, CachedHit) {
    osd_assign_t cached = {0};
    cached.state = OSD_ASSIGN_CACHED;
}
```

**The fix:**

```cpp
osd_assign_t cached{};
/* or */
memset(&cached, 0, sizeof(cached));
```

## Anti-Pattern 6: Static Function Not Promoted For Testable Logic

**The violation:**

```c
static int _parse_header(const char *buf, osd_header_t *hdr) { ... }
```

**The fix:**

- promote test-worthy parsing logic into a header-visible helper when repository conventions allow it
- do not keep meaningful parse/validation logic permanently hidden if it blocks direct behavioral testing

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on stub return value | Test real logic or remove the stub |
| Test-only functions in production | Use public lifecycle/setup paths |
| Stub without understanding | Trace the dependency chain first |
| Incomplete test data | Populate the fields real code reads |
| C struct `= {0}` in C++ | Use `{}` or `memset` |
| Static logic blocks tests | Promote only genuinely test-worthy helpers |

## OSD Verification Reminder

After changing tests or test support code:

- run the narrowest relevant test target first
- then run `make -C test`
- if coverage behavior matters, use `test/run_coverage.sh`

Do not claim a testing fix is sound if it only proves the stub path.
