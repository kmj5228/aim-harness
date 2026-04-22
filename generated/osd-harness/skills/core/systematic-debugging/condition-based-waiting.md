# Condition-Based Waiting

## Overview

Flaky tests often guess at timing with arbitrary delays. That creates race conditions where `make -C test` sometimes passes locally and fails under load or in CI.

**Core principle:** Wait for the actual condition you care about, not a guess about how long it takes.

## When to Use

Use when:

- a test sleeps for a fixed interval before checking output
- a server or tool process must reach a known ready state before assertions
- file or socket side effects appear asynchronously
- `make -C test` failures look timing-sensitive or non-deterministic

Do not use when:

- testing real timeout, debounce, or interval behavior
- the timing itself is the product behavior under test

## Core Pattern

```c
/* BEFORE: guessed delay */
usleep(200000);
rc = osd_check_output(...);
ASSERT_EQ(rc, 0);

/* AFTER: condition-based waiting */
ASSERT_EQ(wait_until_output_ready(2000), 0);
rc = osd_check_output(...);
ASSERT_EQ(rc, 0);
```

## Quick Patterns

| Scenario | Pattern |
|----------|---------|
| Wait for file | poll `access(path, F_OK)` until it succeeds |
| Wait for process state | poll status API or pid file until ready |
| Wait for log line | poll log reader until target string appears |
| Wait for queue/message count | poll count function until threshold met |
| Wait for command output | poll helper command until expected token appears |

## Implementation Sketch

```c
static int wait_until(int (*condition)(void), int timeout_ms, int poll_ms)
{
    int elapsed = 0;

    while (elapsed < timeout_ms) {
        if (condition()) {
            return 0;
        }

        usleep(poll_ms * 1000);
        elapsed += poll_ms;
    }

    return -1;
}
```

Typical OSD usage:

- call `wait_until()` around file creation, process readiness, or observable output
- keep polling interval modest
- fail with a message that says which condition never became true

## Common Mistakes

**Wrong:** `sleep(1)` with no explanation  
**Fix:** poll a concrete readiness condition

**Wrong:** no timeout at all  
**Fix:** fail clearly after a bounded wait

**Wrong:** caching a stale result outside the loop  
**Fix:** re-check the real condition each poll

## When Arbitrary Delay Is Actually Correct

Only after:

1. the triggering condition is already confirmed
2. the timing is part of the behavior under test
3. the reason is documented in the test

If those are not true, prefer condition-based waiting.
