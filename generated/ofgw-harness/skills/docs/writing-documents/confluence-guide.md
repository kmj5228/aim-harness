# OFGW Confluence Writing Guide

## Current Status

- Confluence is not the active default docs target in the current `ofgw` adapter
- repo markdown under `agent/` remains the primary generated docs destination
- this guide is still bundled as a dormant support asset so the harness preserves the full writing-reference set

## Audience

- primary audience: developers and technical collaborators
- code snippets, pseudo-code, SQL, and structured tables are acceptable
- use this guide when the user explicitly wants a Confluence-style document or a later refinement pass enables a Confluence target

## Recommended Structure

```text
# Title

Author: @name
History:
- YYYY-MM-DD: update summary

---

## 1. Overview
## 2. Architecture / Flow
## 3. Module Details
## 4. Test
## 5. Related Issues / Documents
```

## OFGW Rules

- keep conclusions first
- prefer diagrams or structured sections before long prose
- state the real changed surface:
  - `ofgwSrc`
  - `webterminal`
  - `ofgwAdmin`
  - config/resources
  - scripts
- if only backend changed, do not imply admin/frontend scope
- use verified backend evidence when citing implementation or verification:
  - `:ofgwSrc:classes`
  - `:ofgwSrc:test`
  - `:ofgwSrc:jacocoTestReport`

## Practical Use In The Current Runtime

- default generated docs still belong under `agent/`
- if the user asks for a Confluence-ready structure, this guide can shape the draft even when the final output remains markdown
- if a later pass enables an actual Confluence target, this guide is already available next to the docs skill
