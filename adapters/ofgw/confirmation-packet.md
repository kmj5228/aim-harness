# Adapter Confirmation: ofgw

## Inferred Facts

- build_systems: `gradle`, `pnpm`
- primary_languages: `java`, `kotlin`, `javascript`
- modules: `ofgwSrc`, `webterminal`, `ofgwAdmin`
- runtime_hints: `jeus`, `servlet`, `websocket`, `jpa`, `querydsl`
- test_frameworks: `junit5`, `mockito`, `assertj`, `hamcrest`
- coverage_tool: `jacoco`
- project_build_command: `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:classes --no-daemon`
- project_test_command: `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:test --no-daemon`
- coverage_command: `JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 ./gradlew :ofgwSrc:jacocoTestReport --no-daemon`

## Needs Confirmation

## Suggested Defaults

- `access_bindings.issue_sources.jira.enabled`: `true`
  - evidence: root repo guide contains a Jira query guardrail and example key format `OFV7-1234`
- `access_bindings.issue_sources.jira.default_mode`: `mcp`
  - evidence: this is the current preferred org default
- `access_bindings.issue_sources.jira.location`: `atlassian-rovo`
  - evidence: current preferred setup uses Codex MCP server alias `atlassian-rovo`
- `access_bindings.issue_sources.ims.enabled`: `true`
  - evidence: base `issue-analysis` skill explicitly supports both IMS issue and Jira ticket flows
- `access_bindings.issue_sources.ims.location`: `https://ims.tmaxsoft.com/tody/ims/issue/issueView.do?issueId=<IMS_NUMBER>`
  - evidence: base `issue-analysis` skill already defines this Chrome automation URL pattern
- `access_bindings.review_targets.pull_request.enabled`: `true`
  - evidence: `ofgwAdmin/AGENTS.md` explicitly documents PR expectations
- `access_bindings.review_targets.pull_request.default_mode`: `browser`
  - evidence: repo docs imply PR workflow but not MCP automation
- `access_bindings.review_targets.pull_request.location`: `http://192.168.51.106/openframe/openframe7/ofgw`
  - evidence: user confirmed the product Git repository URL
- `access_bindings.docs_targets.repo_markdown.enabled`: `true`
  - evidence: repository contains AGENTS/README style docs and no strong Confluence/wiki signal
- `access_bindings.docs_targets.repo_markdown.default_mode`: `workspace_file`
  - evidence: current repository documentation is markdown-based and workspace-local
- `access_bindings.docs_targets.repo_markdown.location`: `agent/`
  - evidence: user wants a product-root `agent/` directory while preserving existing skill subfolder structure
- `access_bindings.manual_targets.manual_repo.enabled`: keep unresolved
  - evidence: no reliable repository signal for product-level manual repo workflow

### Jira Setup Required

When `jira.default_mode` is `mcp`, initiator should tell the user to ensure the MCP provider is configured:

```bash
codex mcp add atlassian-rovo --url https://mcp.atlassian.com/v1/mcp
codex mcp login atlassian-rovo
codex mcp list
codex mcp get atlassian-rovo
```

If MCP is unavailable or the user prefers REST API access, initiator should also surface the fallback requirement:

```bash
curl -s -u "<EMAIL>:<API_TOKEN>" \
  "https://tmaxsoft.atlassian.net/rest/api/2/issue/<JIRA_KEY>" | jq '.fields.summary, .fields.description'
```

Auth source:
- `../agent/info/access.md`

### NotebookLM Setup Required

The default NotebookLM provider should use the open-source MCP CLI:

- `https://github.com/jacob-bd/notebooklm-mcp-cli`

Initiator should treat this as the default MCP provider and ask the user only for:

- the target NotebookLM URL or notebook identifier

Current target notebook:

- `https://notebooklm.google.com/notebook/158fe966-8a78-4a7e-a6c9-40747330edc5`

### Access Bindings
- no unresolved access binding remains for NotebookLM

### Release / Manual Policy

- `workflow.defaults.manual_workflow_required`: unknown
- `access_bindings.manual_targets.manual_repo.enabled`: unknown
- `access_bindings.manual_targets.manual_repo.default_mode`: unknown
- `access_bindings.manual_targets.manual_repo.location`: unknown

### Terminology

- `terminology.issue_item`: unknown
- `terminology.review_artifact`: unknown
- `terminology.docs_artifact`: unknown

## Red Flags

- `ofgw` is a mixed-stack validation target and must not cause template bodies to become JVM-specific.
- Root packaging tasks can update version files and create git commits, so release packaging commands should not become default validation commands.
- `completing-patch`, `manual-guide`, and coverage-specific prompt/script assets remain excluded from the first generated scope.
- Jira MCP requires explicit bootstrap and login; without that setup, initiator must fall back to REST API guidance instead of assuming MCP is ready.
- IMS is enabled by default, but access still assumes Chrome/browser automation according to the inherited URL pattern.
- NotebookLM provider is assumed to exist via the community MCP CLI; the current `ofgw` draft already fixes one notebook target URL, but future products will still need their own notebook target.
- Generated markdown storage is assumed to live under the product root `agent/` directory.

## Proposed Next Step

- Confirm the unresolved manual repo usage and terminology values.
- Keep the first generated scope limited to:
  - `issue-analysis`
  - `writing-documents`
  - `markdown-guide` as support reference
- After confirmation, generate only the minimal first-pass skeleton for `generated/ofgw-harness/`.
