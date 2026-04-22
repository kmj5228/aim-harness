# Templates

`templates/`는 `base-harness`의 generation source pack 영역이다.

원칙:

- 이 디렉토리는 기본 런타임 `skills/`에 자동 포함되지 않는다.
- 각 pack은 특정 제품이나 운영 환경에서 추출한 source template 묶음을 담는다.
- `harness-initiator`는 여기서 template를 읽고 `adapters/<product>/`와 결합해 `generated/<product>-harness/`를 만든다.

현재 live pack:

- `templates/aim/`

장기 방향:

- `templates/ofgw/`
- `templates/osc/`

같은 추가 pack이 생길 수 있다.
