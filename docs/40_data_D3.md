# D3 · polars — 표현식과 지연 실행

`expression API · LazyFrame`

polars는 Rust로 구현된 데이터프레임 라이브러리입니다. pandas와 결정적으로 다른 점은 두 가지: **표현식(expression) 기반 API**와 **쿼리 최적화가 붙는 지연 실행**입니다. 08파트의 제너레이터 파이프라인 사고방식이 그대로 이어집니다.

*기본*

```python
import polars as pl

df = pl.read_csv("orders.csv", try_parse_dates=True)

df.select(
    pl.col("sku"),
    (pl.col("qty") * pl.col("unit_price")).alias("amount"),
)

df.filter(
    (pl.col("amount") > 10_000) & (pl.col("status") == "paid")
).group_by("customer_id").agg(
    pl.col("amount").sum().alias("total"),
    pl.len().alias("cnt"),
    pl.col("amount").mean().alias("avg"),
).sort("total", descending=True)
```

인덱스가 없고, 모든 연산이 **컬럼 표현식의 조합**입니다. 그래서 pandas의 `SettingWithCopyWarning` 같은 애매함이 구조적으로 존재하지 않습니다.

*지연 실행*

```python
result = (
    pl.scan_parquet("events/*.parquet")      # 아직 아무것도 읽지 않는다
      .filter(pl.col("ts") >= since)
      .group_by("user_id")
      .agg(pl.col("amount").sum())
      .sort("amount", descending=True)
      .head(100)
      .collect()                              # 여기서 실행
)

# 실행 계획 확인 — 조건이 파일 읽기 단계로 내려가는지(predicate pushdown) 볼 수 있다
print(plan.explain())
```

|   | pandas | polars |
| --- | --- | --- |
| 실행 | 즉시 | 즉시(DataFrame) / 지연(LazyFrame) |
| 인덱스 | 있음 | 없음 |
| 병렬 | 기본 단일 스레드 | 기본 멀티스레드(GIL 밖) |
| 메모리 | 큼 | 작음(Arrow 기반) |
| 생태계 | 매우 넓음 | 성장 중 |

**💡 언제 무엇을**

기존 코드·라이브러리 연동이 많거나 데이터가 수백 MB 이하면 pandas로 충분합니다. 파일이 수 GB이거나 배치 파이프라인의 실행 시간이 문제라면 polars의 `scan_*` + `collect()` 조합이 체감 차이가 큽니다. 둘은 `df.to_pandas()`, `pl.from_pandas()`로 오갑니다.

### 🏋 DRILL D3 — polars

1. D2에서 만든 pandas 집계를 polars로 옮기고 실행 시간을 비교하세요.
2. `scan_parquet`으로 지연 파이프라인을 구성하고 `explain()`에서 predicate pushdown을 확인하세요.
3. `pl.when().then().otherwise()`로 구간별 등급 컬럼을 만드세요.
4. 윈도우 함수(`pl.col("x").sum().over("group")`)로 그룹 내 비중을 계산하세요.
