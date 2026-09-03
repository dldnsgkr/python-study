# D2 · pandas

`DataFrame · groupby · merge · 함정`

*입출력과 기본 탐색*

```python
import pandas as pd

df = pd.read_csv("orders.csv", parse_dates=["created_at"], dtype={"sku": "string"})
df = pd.read_parquet("orders.parquet")        # 대용량은 parquet 권장

df.head(); df.info(); df.describe(); df.dtypes
df.shape; df.columns; df.isna().sum()
```

*선택과 필터*

```python
df["amount"]                 # Series
df[["sku", "amount"]]        # DataFrame

df.loc[df["amount"] > 10000, ["sku", "amount"]]     # 라벨 기준
df.iloc[0:5, 0:3]                                    # 위치 기준

df.query("amount > 10000 and status == 'paid'")      # 가독성 좋은 필터

# 조건 조합은 반드시 괄호 + & | ~ (and/or 사용 불가)
df[(df["amount"] > 10000) & (df["status"] == "paid")]
```

*집계*

```python
(df.groupby("customer_id")
   .agg(total=("amount", "sum"),
        cnt=("order_id", "count"),
        avg=("amount", "mean"))
   .sort_values("total", ascending=False)
   .head(10))

df.pivot_table(index="date", columns="channel", values="amount", aggfunc="sum", fill_value=0)

# 시계열 리샘플링
df.set_index("created_at").resample("1D")["amount"].sum()
```

*결합*

```python
pd.merge(orders, customers, on="customer_id", how="left", validate="many_to_one")
pd.concat([df1, df2], ignore_index=True)
```

`validate=`를 습관적으로 붙이세요. 조인 키가 예상과 달리 중복이면 행이 폭증하는데, 이걸 나중에 발견하면 이미 잘못된 리포트가 나간 뒤입니다.

**⚠️ Gotcha · SettingWithCopyWarning**

```python
# 위험 — 뷰일 수도 복사본일 수도 있어서 반영 여부가 불확실
df[df["amount"] > 0]["status"] = "ok"

# 안전 — 한 번의 .loc 로 지정
df.loc[df["amount"] > 0, "status"] = "ok"

# 원본과 분리하고 싶다면 명시적으로
sub = df[df["amount"] > 0].copy()
```

연쇄 인덱싱(`df[...][...]`)은 pandas에서 가장 흔한 버그 원인입니다. 규칙 하나로 정리하세요: **값을 쓸 때는 항상 단일 `.loc`**.

**💡 성능**

`df.apply(func, axis=1)`은 사실상 파이썬 루프입니다. 벡터화 연산 → `np.where`/`np.select` → `map`(사전 조회) 순으로 먼저 시도하고, apply는 최후 수단으로 두세요. 문자열 컬럼은 `dtype="string"`이나 `category`로 바꾸면 메모리와 속도가 크게 좋아집니다.

### 🏋 DRILL D2 — pandas

1. 주문 CSV를 읽어 월별·채널별 매출 피벗 테이블을 만들고 전월 대비 증감률 컬럼을 추가하세요.
2. 고객별 첫 구매일과 재구매까지 걸린 일수를 구하세요(`groupby` + `shift`).
3. 연쇄 인덱싱으로 값을 대입해 경고를 재현하고 `.loc`으로 고치세요.
4. 같은 집계를 `apply`와 벡터화로 각각 구현해 시간을 비교하세요(10만 행 이상).

---

**🟢 2번 힌트**

```python
df = df.sort_values(["customer_id", "created_at"])
df["prev"] = df.groupby("customer_id")["created_at"].shift(1)
df["gap_days"] = (df["created_at"] - df["prev"]).dt.days

first = df.groupby("customer_id")["created_at"].min().rename("first_order")
```

---
