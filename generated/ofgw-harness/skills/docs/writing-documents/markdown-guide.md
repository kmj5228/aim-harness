# OFGW Markdown Writing Guide

## Core Rules

### Start With the Conclusion

- Write the conclusion first, then evidence, then detail
- Avoid background-first paragraphs

### Prefer Diagrams For Flows

- Use `mermaid` before long text for architecture, flow, and module relationships
- Do not use ASCII art

### Artifact Contract

- Store topic-scoped documents under `agent/<topic>/`
- Treat filenames below as canonical runtime artifacts

| logical artifact | canonical filename |
|------------------|--------------------|
| `analysis_report` | `analysis_report.md` |
| `design_spec` | `design_spec.md` |
| `implementation_plan` | `plan_tasks.md` |

### OFGW Scope Reminder

- Call out whether the document concerns `ofgwSrc`, `webterminal`, `ofgwAdmin`, config/resources, or scripts
- Do not claim untouched modules as verified
- If manual follow-up is needed, keep the draft in `generated/manual/`
