# aim-harness

This directory is the current standalone-target draft for `aim`.

It was produced from:

- source pack: `templates/aim/`
- adapter inputs: `adapters/aim/product-profile.yaml`, `adapters/aim/mappings.yaml`

Current goal:

- validate that `harness-initiator` can materialize a usable AIM-bound standalone harness
- materialize reusable `core`, `collab`, `review`, and docs layers inside the generated harness
- keep template/source-only carry-over out of the standalone harness

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

- base-runtime carry-over:
  - `skills/core/*`
  - `skills/collab/*`
  - `skills/review/code-reviewer/`
  - `skills/review/review-context-collector/`
  - `skills/review/coverage-review/`
- product-bound generated layer:
  - `skills/product/issue-analysis/`
  - `skills/docs/writing-documents/`
  - `skills/docs/manual-workflow/`
- runtime materialization:
  - `agent/`
  - `generated/manual/`
  - `hooks/`

## Status

- standalone target: materially usable first draft
- current tree: generated from the current initiator contract
- generated bindings: reviewed and traceable to adapter inputs plus initiator default carry-over
- review workflow is merge-request aware
- coverage review workflow is generated around `make gtest`
- local manual draft workflow is generated
- external manual publish workflow is not generated yet
- full completion/patch workflow is not generated yet
