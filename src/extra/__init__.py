"""확장 드릴 — 원본 워크북의 DRILL 중 채점 키트(KIT)에 빠져 있던 문제들.

원본 KIT은 코어 20개 파트 중 20개 함수만 테스트합니다. 나머지 드릴은
"직접 해 보세요"로만 남아 있어 맞았는지 확인할 방법이 없었습니다.
여기서 기계적으로 판정 가능한 것들을 골라 테스트를 붙였습니다.

  strings.py      03 문자열 — 표 정렬, CSV, 한글 폭
  mappings.py     05 매핑 — LRU 캐시, 깊은 병합
  control.py      06 제어흐름 — match 라우터, walrus 청크 읽기
  iteration.py    08 이터레이션 — 무한 제너레이터, JSONL 파이프라인
  decorators.py   09 데코레이터 — 마스킹 감사 로그, 레이트리밋, 동기/비동기 겸용
  modeling.py     12 데이터 모델링 — frozen dataclass, TypedDict 어댑터
  errors.py       13 예외 — ExceptionGroup, 제너레이터 정리 시점
  typed.py        15 타입 — @overload
  stdlib_extra.py 16 표준 라이브러리 — pathlib/Counter, 정규식, JSON 왕복
  concurrency.py  17 동시성 — Semaphore 제한, 비동기 재시도
  perf.py         19 성능 — 집합 연산, heapq, 스트리밍
"""
