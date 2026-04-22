# osd-harness

This directory is the current standalone-target draft for `osd`.

It was produced from:

- source pack: `templates/aim/`
- adapter inputs: `adapters/osd/product-profile.yaml`, `adapters/osd/mappings.yaml`

Current goal:

- validate that `harness-initiator` can move beyond a docs/product-only skeleton
- materialize reusable `core`, `collab`, `review`, and docs layers inside the generated harness
- keep template/source-only carry-over out of the standalone harness
- allow selected support prompts and guides to live next to generated skills when they make the product harness v1 materially more usable

## Layout

```text
generated/osd-harness/
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
- bundled support assets:
  - selected core reviewer prompts
  - selected subagent dispatch prompts
  - selected review prompts
  - selected writing guides

## Status

- standalone target: materially usable first draft
- current tree: generated from the current initiator contract
- generated bindings: reviewed and traceable to adapter inputs plus initiator default carry-over
- coverage review workflow: generated
- local manual draft workflow: generated
- external manual publish workflow: not generated yet
- full completion/patch workflow: not generated yet
