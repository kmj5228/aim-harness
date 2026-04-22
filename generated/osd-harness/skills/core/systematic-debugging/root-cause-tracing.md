# Root Cause Tracing

## Overview

Bugs often appear deep in the stack or at the wrong operational layer. The visible symptom may be in a coverage script, generated artifact, or packaging flow even when the original trigger is elsewhere.

**Core principle:** Trace backward through the call chain and workflow boundary until you find the original trigger, then fix at the source.

## Typical OSD Example

### 1. Observe the Symptom

```text
Coverage report looks incomplete, but only part of the OSD product surface was actually exercised
```

### 2. Find Immediate Cause

**What directly produced the report?**

```text
test/run_coverage.sh
```

### 3. Ask What Fed It

```text
coverage conclusion
  -> depended on changed file scope
  -> depended on which tests were actually run
  -> depended on whether the change was runtime code or operational packaging
```

### 4. Keep Tracing

- Was the change in `src/lib`, `src/server`, `src/tool`, or `src/util`?
- Was the claim accidentally widened to include `dist/` packaging flow?
- Did the report confuse runtime verification with release automation?

### 5. Find the Original Trigger

Usually the real bug is an over-broad conclusion:

- runtime code in one module changed
- but the report claimed "OSD verified" as if the whole product and distribution flow were covered

## Practical Rule

- bind conclusions to the exact command that ran
- bind conclusions to the exact surface that changed
- separate runtime code, code-table changes, and `dist/` operations

## Fix Pattern

- narrow the conclusion to the proven scope
- make the touched module explicit
- add a guard so the same overstatement does not recur
