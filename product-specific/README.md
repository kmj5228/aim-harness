# Product-Specific

이 디렉토리는 `base-harness`의 기본 runtime skill set에 포함하지 않는 product-specific product pack 번들을 모아둔 영역이다.

원칙:

- `skills/`에는 공통 base workflow만 둔다.
- 외부 시스템, 조직 절차, 특정 제품 정책에 강하게 묶인 문서는 `product-specific/`로 분리한다.
- 현재는 첫 번째 product pack 영역으로 유지하고, 장기적으로는 `product-packs/<product>/` 구조로 승격할 수 있다.

현재 포함 범위:

- `product-specific/skills/issue-analysis-base`
- `product-specific/skills/completing-patch-base`
- `product-specific/skills/writing-documents-base`
- `product-specific/code-reviewer-base/`의 정보 수집/커버리지 자산
