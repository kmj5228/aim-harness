# aim-harness

This directory is the regenerated standalone-target draft for `aim`.

It was produced from:

- source pack: `templates/aim/`
- adapter inputs:
  - `adapters/aim/product-profile.yaml`
  - `adapters/aim/mappings.yaml`

Current goal:

- test how closely the current initiator/refinement system can reconstruct the original `aim-harness`
- preserve AIM workflow meaning while using the current layered generated layout
- keep the original `/home/woosuk_jung/harness/aim-harness` untouched

## Layout

```text
generated/aim-harness/
├── AGENTS.md
├── README.md
├── GENERATION_SUMMARY.md
├── agent/README.md
├── hooks/
├── skills/
│   ├── core/
│   ├── collab/
│   ├── docs/
│   ├── review/
│   └── product/
└── generated/manual/README.md
```

## Included Now

- regenerated base/runtime loop:
  - `skills/core/*`
  - `skills/collab/*`
- regenerated review layer:
  - `skills/review/code-reviewer/`
  - `skills/review/review-context-collector/`
  - `skills/review/coverage-review/`
- regenerated docs/product layer:
  - `skills/product/issue-analysis/`
  - `skills/docs/writing-documents/`
  - `skills/docs/manual-workflow/`
- runtime materialization:
  - `agent/`
  - `generated/manual/`
  - `hooks/`

## Status

- semantic reconstruction: meaningful
- generated runtime: usable comparison draft
- strongest preserved areas:
  - issue triage
  - design/plan/execute loop
  - AIM-style review semantics
  - document authoring hub
- still missing as first-class generated runtime:
  - `completing-patch`
  - full external MANUAL repo publication
  - original `using-aim-harness` startup model
