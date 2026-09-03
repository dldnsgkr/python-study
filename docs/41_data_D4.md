# D4 · 데이터 파이프라인

`포맷 · 청크 · 검증 · 재현성`

## 포맷 선택

| 포맷 | 쓸 때 | 주의 |
| --- | --- | --- |
| CSV | 사람이 읽어야 할 때, 교환용 | 타입 정보 없음, 느림, 인코딩 문제 |
| Parquet | 분석용 저장의 기본값 | 열 지향·압축·타입 보존, 부분 읽기 가능 |
| JSON Lines | 스키마가 유동적인 로그 | 한 줄 = 한 레코드라 스트리밍에 적합 |
| SQLite/DuckDB | 중간 결과를 질의하고 싶을 때 | DuckDB는 parquet에 직접 SQL을 던질 수 있음 |

*메모리보다 큰 데이터 처리*

```python
# pandas: 청크 단위
totals = Counter()
for chunk in pd.read_csv("huge.csv", chunksize=200_000):
    totals.update(chunk.groupby("sku")["qty"].sum().to_dict())

# polars: 지연 + 스트리밍
(pl.scan_csv("huge.csv")
   .group_by("sku").agg(pl.col("qty").sum())
   .collect(streaming=True))

# 순수 파이썬: 제너레이터 (08파트)
for batch in batches(read_records("huge.jsonl"), 10_000):
    load(batch)
```

## 재현성과 검증

- **난수 시드 고정** — `np.random.default_rng(42)`를 인자로 주입해 테스트 가능하게.
- **입력 스키마 검증** — pydantic(B1) 또는 pandera로 컬럼·타입·범위를 계약화.
- **중간 산출물 저장** — 단계별 parquet으로 남기면 실패 지점부터 재실행 가능.
- **멱등성** — 같은 입력을 두 번 돌려도 결과가 같도록. 로드는 upsert로.

*파이프라인 골격*

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Step:
    name: str
    fn: Callable[[pl.LazyFrame], pl.LazyFrame]

STEPS = [
    Step("clean", drop_invalid),
    Step("enrich", join_customer),
    Step("aggregate", monthly_totals),
]

def run(src: Path, dst: Path) -> None:
    lf = pl.scan_parquet(src)
    for step in STEPS:
        logger.info("step start", extra={"extra_fields": {"step": step.name}})
        lf = step.fn(lf)
    lf.collect(streaming=True).write_parquet(dst)
```

**💡 시각화는 마지막에**

탐색은 `df.plot`/matplotlib으로 충분하고, 공유용 대시보드가 필요하면 streamlit이 가장 빠릅니다. 다만 **차트를 만들기 전에 숫자를 검증**하세요 — 그림은 틀린 집계도 그럴듯하게 보여 줍니다.

### 🏋 DRILL D4 — 파이프라인

1. 같은 데이터를 CSV/Parquet으로 저장해 파일 크기와 읽기 시간을 비교하세요.
2. 메모리보다 큰 CSV를 청크와 스트리밍 두 방식으로 집계하고 최대 메모리를 `tracemalloc`으로 비교하세요.
3. 입력 스키마 검증 단계를 추가해 잘못된 행을 별도 파일로 격리하고 요약 리포트를 남기세요.
4. 파이프라인을 두 번 실행해도 결과가 동일한지(멱등성) 확인하는 테스트를 pytest로 작성하세요.
