# OSD Analysis Summary

## Repository Facts

Target repo:

- `/home/woosuk_jung/harness/osd`

Observed evidence:

- `/home/woosuk_jung/harness/osd/Makefile`
- `/home/woosuk_jung/harness/osd/test/Makefile`
- `/home/woosuk_jung/harness/osd/make/rules.gtest`
- `/home/woosuk_jung/harness/osd/test/run_coverage.sh`
- `/home/woosuk_jung/harness/osd/dist/patch_osd.sh`
- `/home/woosuk_jung/harness/osd/dist/dist_osd.sh`
- git remote: `http://192.168.51.106/openframe/openframe7/osd.git`

Observed repo shape:

- root build orchestrator is `Makefile`
- top-level source groups:
  - `errcode`
  - `msgcode`
  - `include`
  - `sysmsg`
  - `src`
  - `install`
  - `test`
  - `dist`
  - `make`
- `src` splits into:
  - `lib`
  - `server`
  - `tool`
  - `util`
- `test` mirrors multiple product surfaces:
  - `test/lib/*`
  - `test/server/*`
  - `test/tool/*`
  - `test/util/*`

## Stack Snapshot

- primary build system: `make`
- primary languages:
  - `c`
  - `c++`
  - `shell`
- test framework signals:
  - `gtest`
  - `gmock`
- coverage tool signals:
  - `gcov`
  - `lcov`
  - `genhtml`

## Command Signals

Build signal:

- root `Makefile` delegates to `$(SOURCE_BASE)/osd/make/rules`
- concrete build depends on product environment variables such as `SOURCE_BASE` and runtime installation paths

Coverage signal:

- `test/run_coverage.sh` is a repo-native coverage entry point
- it builds coverage-aware test binaries with `--coverage`
- it collects coverage with:
  - `gcov`
  - `lcov`
  - `genhtml`
- it also depends on environment/runtime values:
  - `OPENFRAME_ROOT`
  - staged runtime libs under `/tmp/oframe_cov`

Patch/release signal:

- `dist/patch_osd.sh` is an operational patch packaging script
- it requires:
  - IMS number
  - module name
  - patch date
  - files to package
- it can also trigger backup copy via `scp` when `~/.patchrc` enables it

Distribution signal:

- `dist/dist_osd.sh` builds a module list and binary tarball
- it depends on:
  - `SOURCE_BASE`
  - `OPENFRAME_HOME`
  - `offile`

## Initiator Interpretation

What looks reusable for generation:

- `issue-analysis`
- `writing-documents`
- `review-context-collector`
- `coverage-review`

What is clearly product-bound and should stay careful:

- `coverage-review`
  - usable because the repo has a native coverage script
  - but strongly environment-dependent
- `manual-workflow`
  - possible only as local draft workflow until manual target is confirmed
- `completing-patch`
  - highly coupled to `patch_osd.sh`, environment variables, and operational backup behavior

## Adapter Draft Direction

Likely first draft direction:

- issue/review/docs bindings may follow the same org-level defaults as `ofgw`
- repo markdown workspace can still default to `agent/`
- PR review target likely maps to the git remote host path
- manual target should remain unconfirmed until product policy is explicitly closed

## Open Questions

- Is Jira/IMS access the same as `ofgw`, or does `osd` use a different issue path in practice?
- Should manual follow-up stay enabled by default for `osd`?
- Is `generated/manual/` still the desired local manual workspace?
- Should `coverage-review` be generated immediately, or deferred until the environment requirements are confirmed?
- Is `patch_osd.sh` enough to justify earlier `completing-patch` productization, or should it stay deferred for now?
