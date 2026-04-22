---
name: harness-installer
description: Use when a generated product harness already exists and needs to be installed into a real project repository by transforming the generated layout into project-local .agents/skills and .codex files without overwriting the repo's own AGENTS.md
---

# Harness Installer

## Overview

Install a generated product harness into a real project repository.

**Core principle:** generated harnesses are install artifacts, not final on-repo layout.
This skill transforms:

- layered generated `skills/<layer>/<skill>/`
- generated startup contract
- generated hook draft

into project-local Codex layout:

- `<repo>/.agents/skills/<skill>/`
- `<repo>/.codex/<product>-harness/AGENTS.md`
- `<repo>/.codex/config.toml`
- `<repo>/.codex/hooks/*`

Do not overwrite the repo's own root `AGENTS.md` during install.

## When to Use

- `generated/<product>-harness/` already exists
- the next goal is to use that harness inside a real target repository
- you need to transform generated layout into project-local Codex layout
- you need an auditable install step before building a more automated installer

Do not use for:

- template selection
- adapter drafting
- generated harness creation
- product skill refinement inside `generated/`

Use:

- `harness-initiator` for generation
- `harness-support-assets` for template-side support asset productization
- `harness-refinement` for post-generation runtime improvement

## Current Install Contract

### Skill Install

- source:
  - `generated/<product>-harness/skills/<layer>/<skill>/`
- target:
  - `<repo>/.agents/skills/<skill>/`

Interpretation:

- generated layer names do not survive installation
- installed project-local skills use flat skill directories under `.agents/skills/`

### Startup Contract Install

- source:
  - `generated/<product>-harness/AGENTS.md`
- target:
  - preferred when `<repo>/AGENTS.md` does not exist:
    - `<repo>/AGENTS.md`
  - fallback when `<repo>/AGENTS.md` already exists:
    - `<repo>/.codex/<product>-harness/AGENTS.md`

Interpretation:

- if `<repo>/AGENTS.md` does not exist, generated runtime `AGENTS.md` may be installed there directly
- if `<repo>/AGENTS.md` already exists, do not overwrite it
- in that case, treat generated runtime `AGENTS.md` as harness-local startup contract under `.codex`
- always report which startup contract path was chosen

### Hook Install

- source:
  - `generated/<product>-harness/hooks/config.toml`
  - `generated/<product>-harness/hooks/hooks.json`
  - `generated/<product>-harness/hooks/session-start.sh`
- target:
  - `<repo>/.codex/config.toml`
  - `<repo>/.codex/hooks/hooks.json`
  - `<repo>/.codex/hooks/session-start.sh`

Install rewrite rules:

- hook command must point to `<repo>/.codex/hooks/session-start.sh`
- session-start script must read whichever startup contract path was actually installed

### Runtime Workspace Install

- source:
  - `generated/<product>-harness/agent/`
  - `generated/<product>-harness/generated/manual/`
- target:
  - `<repo>/agent/`
  - `<repo>/generated/manual/`

Interpretation:

- keep runtime workspace paths stable when possible
- install should not rename these paths unless the generated contract itself changes

## Workflow

1. Read the generated harness layout and the target repo state.
2. Check for conflicting existing paths:
   - `.agents/skills/<skill>/`
   - `.codex/<product>-harness/`
   - `.codex/hooks/`
   - `agent/`
   - `generated/manual/`
3. Decide whether this is:
   - first install
   - reinstall/upgrade
4. For first install:
   - create missing target directories
   - flatten generated skills into `.agents/skills/`
   - if root `AGENTS.md` is absent, install generated `AGENTS.md` there directly
   - if root `AGENTS.md` already exists, keep it and install generated `AGENTS.md` under `.codex/<product>-harness/`
   - install hook draft under `.codex/hooks/`
   - rewrite hook paths to project-local layout
   - rewrite startup contract path inside installed hook script to match the chosen contract location
   - materialize `agent/` and `generated/manual/`
5. Validate the installed result:
   - expected skill count
   - `bash -n` on installed `session-start.sh`
   - installed hook command path correctness
   - startup contract path correctness
6. Record:
   - what was copied directly
   - what required path rewrite
   - what was intentionally not installed

## Safety Rules

- do not overwrite the repo root `AGENTS.md`
- if the repo root `AGENTS.md` already exists, report that collision explicitly
- do not assume project-local `.codex/` already exists
- do not assume `.agents/skills/` is empty
- for first implementation, prefer explicit refusal over destructive merge
- if an install target already exists and merge policy is unclear, stop and report the collision

## Outputs

- installed project-local skills under `.agents/skills/`
- installed startup contract under root `AGENTS.md` or `.codex/<product>-harness/AGENTS.md`
- installed hook draft under `.codex/hooks/`
- installed runtime workspace placeholders under `agent/` and `generated/manual/`
- short install report with:
  - copied
  - rewritten
  - skipped
  - collisions

## Current Validation Target

The first install proof target is:

- generated source:
  - `generated/ofgw-harness/`
- real target repo:
  - `/home/woosuk_jung/harness/ofgw/`

This skill should follow the install contract recorded in `HARNESS_INITIATOR.md`.
