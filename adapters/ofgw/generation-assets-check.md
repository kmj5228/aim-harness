# Generation Assets Check: ofgw

## Purpose

Verify that `adapters/ofgw/mappings.yaml` `generation_assets` entries match the current generated `ofgw-harness` tree.

Applied procedure:

1. enumerate every `generation_assets` entry
2. verify `source`, `action`, `target` shape
3. compare declared result with the observed generated tree
4. separate template-derived matches from initiator default carry-over

## Check Result

Status: pass with expected initiator carry-over

## Entry-by-Entry Check

| Source | Action | Expected target | Observed state | Result |
|------|--------|-----------------|----------------|--------|
| `templates/aim/skills/issue-analysis/SKILL.md` | `generate` | `skills/product/issue-analysis/SKILL.md` | target exists | pass |
| `templates/aim/skills/writing-documents/SKILL.md` | `generate` | `skills/docs/writing-documents/SKILL.md` | target exists | pass |
| `templates/aim/skills/writing-documents/markdown-guide.md` | `absorb` | `skills/docs/writing-documents/SKILL.md` | markdown rules are folded into docs skill | pass |
| `templates/aim/skills/writing-documents/manual-guide.md` | `absorb_partial` | `skills/docs/manual-workflow/SKILL.md` | local manual workflow exists, external publish remains excluded | pass |
| `templates/aim/skills/completing-patch/SKILL.md` | `defer` | none | no generated `completing-patch` skill | pass |
| `templates/aim/review/code-reviewer/info-collector-prompt.md` | `absorb_partial` | `skills/review/review-context-collector/SKILL.md` | target exists | pass |
| `templates/aim/review/code-reviewer/coverage-analyst-prompt.md` | `absorb_partial` | `skills/review/coverage-review/SKILL.md` | target exists | pass |
| `templates/aim/review/code-reviewer/measure_diff_cov.sh` | `stay_in_templates` | none | no generated copy exists | pass |
| `templates/aim/skills/writing-documents/jira-guide.md` | `stay_in_templates` | none | no generated copy exists | pass |
| `templates/aim/skills/writing-documents/gitlab-guide.md` | `stay_in_templates` | none | no generated copy exists | pass |
| `templates/aim/skills/writing-documents/ims-guide.md` | `stay_in_templates` | none | no generated copy exists | pass |
| `templates/aim/skills/writing-documents/confluence-guide.md` | `stay_in_templates` | none | no generated copy exists | pass |
| `templates/aim/skills/writing-documents/mail-guide.md` | `stay_in_templates` | none | no generated copy exists | pass |

## Expected Initiator Carry-Over

The current generated tree still includes generated skills that are not listed in `generation_assets`:

- `skills/core/*`
- `skills/collab/*`
- `skills/review/code-reviewer/SKILL.md`

Interpretation:

- these are valid generated assets for the current `ofgw` draft
- but they come from `harness-initiator`의 기본 base-runtime carry-over 정책 rather than from template source-asset mapping
- this carry-over is expected as long as the default carry-over policy stays in the initiator skill

## Conclusion

- `generation_assets` now explains the template-derived portion of the current `ofgw` generation pass
- base-runtime carry-over는 별도 adapter schema가 아니라 initiator skill의 기본 정책으로 해석하는 편이 현재 구조에 더 맞다
