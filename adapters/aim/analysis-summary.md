# AIM Analysis Summary

## Selected Templates

- `issue-analysis`
- `writing-documents`
- `review/code-reviewer/*`
- `markdown-guide` as bundled support reference
- `manual-guide` as a high-value source reference, but not fully promotable under the current first-pass generator contract

## Inferred Repository Facts

- build system wrapper: `dx` over `make`, `git`, and shell commands
- primary languages:
  - `c`
  - `c++`
  - `shell`
  - `markdown`
- release branch policy:
  - never commit directly to `rb_73`
- test framework:
  - `GoogleTest`
- coverage policy:
  - diff-added code coverage `>= 80%`
- issue and review systems:
  - IMS
  - Jira
  - GitLab MR
- external spec source:
  - NotebookLM `xsp-specification`

## Inferred Commands

- build:
  - `dx make`
- test:
  - `dx tmdown -y && dx make gtest`
- coverage:
  - `dx bash -c "cd /root/ofsrc/aim && bash skills/review/code-reviewer/scripts/measure_diff_cov.sh"`

## Runtime And Hook Facts

- original runtime entrypoint is `CLAUDE.md`, not `AGENTS.md`
- original auto-injection path is:
  - `settings.json`
  - `hooks/session-start.sh`
  - `skills/using-aim-harness/SKILL.md`
- original artifact workspace is externalized around `../agent/prompt/<topic>/`
- current generated model instead prefers:
  - `AGENTS.md`
  - `hooks/`
  - `agent/<topic>/`
  - `generated/manual/`

## Excluded Or Difficult Assets Under Current Contract

- `completing-patch`
- full external manual publish procedure to `/Users/mjkang/company/MANUAL/openFrame_aim`
- Claude-specific `using-aim-harness` meta-skill auto-injection model
- complete normalization of Claude-era orchestration vocabulary inside copied review/subagent skills

## Red Flags

- This workspace contains `aim-harness`, not the live AIM product repo itself, so repo commands and project paths are inferred from harness documents.
- Original AIM runtime semantics are split across `CLAUDE.md`, hook files, and many skill bodies, while the current generated model expects a cleaner `AGENTS.md`-first entrypoint.
- Full semantic reconstruction of manual/completion flow requires first-class schema for:
  - external manual repo target
  - manual marker lifecycle
  - post-merge patch-verification workflow

## Evidence

- `/home/woosuk_jung/harness/aim-harness/README.md`
- `/home/woosuk_jung/harness/aim-harness/CLAUDE.md`
- `/home/woosuk_jung/harness/aim-harness/settings.json`
- `/home/woosuk_jung/harness/aim-harness/hooks/session-start.sh`
- `/home/woosuk_jung/harness/aim-harness/skills/issue-analysis-aim/SKILL.md`
- `/home/woosuk_jung/harness/aim-harness/skills/writing-documents-aim/SKILL.md`
- `/home/woosuk_jung/harness/aim-harness/skills/code-reviewer-aim/SKILL.md`
- `/home/woosuk_jung/harness/aim-harness/skills/completing-patch-aim/SKILL.md`
