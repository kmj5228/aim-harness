# OFGW Jira Writing Guide

## Default Access

- Use Jira MCP first when available
- Fallback to API only when MCP is unavailable or insufficient
- Credentials and fallback examples come from `agent/info/access.md`

## Recommended Description Structure

```text
h1. Problem
h1. Goal
h1. Analysis
h1. Design
h1. Development
h1. Test
h1. Document
h1. Reference
```

## Writing Rules

- Keep existing `Problem` and `Goal` unless the user explicitly wants them changed
- Add analysis, design, development, and test detail based on actual OFGW module changes
- Mention the real touched surface: `ofgwSrc`, `webterminal`, `ofgwAdmin`, config/resources, or scripts
- Link runtime artifacts from `agent/<topic>/` when they exist
- Backend verification can cite `:ofgwSrc:classes`, `:ofgwSrc:test`, and `:ofgwSrc:jacocoTestReport`
