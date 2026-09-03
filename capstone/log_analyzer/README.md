# CAPSTONE A · 로그 분석 CLI

> 원문: `docs/30_core_21.md`

대용량 접근 로그를 **스트리밍으로** 처리해 통계를 내는 명령줄 도구입니다.
코어 트랙에서 따로따로 배운 것들을 한 프로그램에 합치는 게 목적입니다.

## 요구사항

| # | 요구 | 관련 파트 |
| --- | --- | --- |
| 1 | 제너레이터 파이프라인으로 **메모리 사용량이 파일 크기와 무관** | 08 |
| 2 | `argparse` 로 기간·상태코드·출력형식 옵션 | 16 |
| 3 | 결과 모델은 `frozen dataclass`, 상태 코드는 `IntEnum` | 12 |
| 4 | 파싱 실패 줄은 커스텀 예외로 **수집**해 마지막에 요약 | 13 |
| 5 | 여러 파일은 `ProcessPoolExecutor` 로 병렬 처리 | 17 |
| 6 | `mypy --strict` 통과 + pytest 단위 테스트 | 15, 18 |

## 설계 — 네 단계를 이어 붙이기

```python
read_lines(paths)                     # 파일 → (줄번호, 줄)
    → parse(numbered_lines)           # 줄 → Entry | ParseError
    → filter_entries(entries, ...)    # 조건에 맞는 것만
    → aggregate(entries)              # → Report
```

각 단계를 **순수 함수 + 제너레이터**로 유지하면, 테스트에서 리스트를 넣고
리스트를 받는 형태로 각각 따로 검증할 수 있습니다. `main` 은 연결만 합니다.

## 로그 형식 (Common Log Format)

```text
127.0.0.1 - - [24/Jul/2026:10:00:00 +0900] "GET /index.html HTTP/1.1" 200 512
```

## 채점

`analyzer.py` 의 `NotImplementedError` 를 지워 나가세요.

```bash
./study capstone            # 이 캡스톤만 채점
```

1~4번과 6번은 테스트가 붙어 있습니다.
**5번(병렬 처리)과 CLI 옵션은 테스트가 없습니다** — 직접 만들고, 직접 확인하세요.
`sample.log` 로 실제로 돌려 보는 것까지가 이 과제입니다.

```bash
.venv/bin/python capstone/log_analyzer/analyzer.py capstone/log_analyzer/sample.log --status 200
```

## 다 했다면

- `CAPSTONE B` 미니 ORM — 디스크립터와 `__init_subclass__` 로 객체 모델을 끝까지 (`docs/30_core_21.md`)
- `CAPSTONE C` 비동기 크롤러 — `asyncio` + `TaskGroup` + `except*`

두 캡스톤은 정답이 하나로 정해지지 않아 테스트를 붙이지 않았습니다.
대신 원문의 체크리스트를 하나씩 지워 나가고, **자기 테스트를 직접 쓰는 것**이 과제의 일부입니다.
