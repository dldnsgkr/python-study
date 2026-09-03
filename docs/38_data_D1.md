# D1 · NumPy — 루프를 배열 연산으로

`ndarray · dtype · broadcasting · view`

데이터 트랙의 전제는 하나입니다. **파이썬 루프를 배열 연산으로 바꾸면 10~100배 빨라진다.** 이유는 24파트에서 본 그대로 — 객체 헤더·타입 디스패치·인터프리터 루프를 전부 건너뛰고 연속된 메모리 위에서 C 루프가 돕니다.

*기본*

```python
import numpy as np

a = np.array([1, 2, 3], dtype=np.int64)
np.zeros((3, 4)); np.ones(5); np.arange(0, 10, 2); np.linspace(0, 1, 11)
rng = np.random.default_rng(42)          # 권장 난수 API
x = rng.normal(size=(1000, 3))

x.shape, x.dtype, x.ndim, x.nbytes
x.reshape(-1, 6); x.T; x.astype(np.float32)
```

*벡터화*

```python
# 느림 — 파이썬 루프
result = [v * 1.1 for v in values]

# 빠름 — 전체가 한 번의 C 연산
arr = np.asarray(values)
result = arr * 1.1

# 조건부 계산도 루프 없이
discounted = np.where(arr >= 10000, arr * 0.9, arr)

# 불리언 마스킹
big = arr[arr > arr.mean()]
arr[arr < 0] = 0
```

## 브로드캐스팅

*broadcasting*

```python
prices = np.array([[100], [200], [300]])      # (3, 1)
rates  = np.array([0.9, 1.0, 1.1])            # (3,) → (1, 3)
prices * rates                                 # (3, 3) 결과

# 규칙: 뒤 차원부터 비교해 크기가 같거나 한쪽이 1이면 늘려서 맞춘다
# 정규화 예
x_norm = (x - x.mean(axis=0)) / x.std(axis=0)
```

**⚠️ Gotcha · view vs copy**

슬라이싱은 **뷰**라서 원본과 메모리를 공유합니다(파이썬 리스트 슬라이싱과 반대!).

```python
a = np.arange(10)
b = a[2:5]
b[0] = 999
a          # array([0, 1, 999, 3, ...])  ← 원본이 바뀐다
c = a[2:5].copy()          # 독립 복사
a.base is None             # 뷰인지 확인
```

반면 **팬시 인덱싱**(`a[[0, 2, 4]]`)과 불리언 인덱싱은 항상 복사본을 만듭니다.

**🖥 REPL 퀴즈 — D1-1 · dtype의 함정**

```python
>>> a = np.array([1, 2, 3], dtype=np.int8)
>>> a * 100
>>> np.array([1, 2]) / np.array([0, 1])
```

---

**🟢 출력 보기**

```text
array([100, -56,  44], dtype=int8)
array([inf,  2.])   (+ RuntimeWarning)
```

NumPy 정수는 파이썬 int와 달리 **고정 폭이라 오버플로가 조용히 일어납니다**(02파트와 정반대). 0 나누기도 예외가 아니라 `inf`/`nan`과 경고로 처리됩니다. `np.seterr(all="raise")`로 예외로 승격시킬 수 있습니다.

---

### 🏋 DRILL D1 — NumPy

1. 100만 개 값에 대해 파이썬 루프·컴프리헨션·NumPy 벡터화의 시간을 비교하세요.
2. 이동평균(window=7)을 `np.convolve`와 누적합 방식으로 각각 구현하고 결과가 같은지 검증하세요.
3. 뷰와 복사의 차이를 `np.shares_memory`로 확인하는 실험을 만드세요.
4. 결측치(`np.nan`)가 섞인 배열에서 `mean`과 `nanmean`의 차이를 확인하고, 결측 처리 전략을 정리하세요.
