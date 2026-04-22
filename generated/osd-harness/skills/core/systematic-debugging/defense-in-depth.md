# Defense-in-Depth Validation

## Overview

When a bug comes from bad input or bad state, one guard often looks sufficient. In practice, different code paths, tests, tools, and environment assumptions bypass single-point validation.

**Core principle:** Validate at every meaningful layer the data passes through. Make the failure structurally harder to repeat.

## Why This Matters In OSD

OSD has multiple surfaces:

- `src/lib`
- `src/server`
- `src/tool`
- `src/util`
- test and coverage helpers

Invalid state can enter from one surface and fail in another. A check only at the first entry point is often not enough.

## The Four Layers

### Layer 1: Entry Validation

Reject obviously bad input where it first enters.

```c
int osd_open_config(const char *path)
{
    if (path == NULL || *path == '\0') {
        return OSD_ERR_INVALID_ARG;
    }
    return osd_open_config_impl(path);
}
```

### Layer 2: Business Validation

Validate assumptions again where the operation becomes meaningful.

```c
int osd_build_runtime(const osd_config_t *cfg)
{
    if (cfg == NULL || cfg->server_port <= 0) {
        return OSD_ERR_INVALID_STATE;
    }
    ...
}
```

### Layer 3: Environment Guards

Protect dangerous operations in test or tool-specific contexts.

```c
int osd_write_runtime_file(const char *path)
{
    if (running_under_test() && !path_is_under_tmp(path)) {
        return OSD_ERR_UNSAFE_PATH;
    }
    ...
}
```

### Layer 4: Debug Instrumentation

Capture enough context that the next failure is explainable.

```c
osd_log_debug("runtime write rejected", "path=%s mode=%s", path, current_mode());
```

## Applying The Pattern

When you find a bug:

1. trace where the bad value first appears
2. list every checkpoint it passes through
3. add a guard at each meaningful layer
4. test at least two layers so the fix is not a single fragile gate

## OSD-Specific Guidance

- `src/lib` validation should not assume `src/server` callers are always correct
- `src/tool` helpers should not trust external file or process state blindly
- test helpers and coverage scripts should fail fast on missing prerequisites
- use `make`, `make -C test`, and `test/run_coverage.sh` as the default verification context when documenting fixes

## Key Insight

Single-point validation says "we patched the last failure."

Defense-in-depth says "we made the same class of failure harder to reproduce across lib/server/tool/test paths."
