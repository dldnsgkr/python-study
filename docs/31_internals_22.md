# 22 · CPython 객체 레이아웃과 메모리

`PyObject · refcount · dict 구조 · GC`

여기서부터는 "왜 그렇게 동작하는가"의 층입니다. 몰라도 코드는 짜지만, 알면 성능 판단과 이상한 버그 해석이 달라집니다. 아래 내용은 **CPython 구현 세부사항**이며 언어 명세가 아닙니다.

## 모든 객체의 공통 헤더

*C 레벨 구조 (개념)*

```text
typedef struct _object {
    Py_ssize_t ob_refcnt;      // 참조 카운트
    PyTypeObject *ob_type;     // 타입 포인터
} PyObject;

// 가변 길이 객체(list, tuple, str…)는 하나 더
typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size;        // 원소 개수
} PyVarObject;
```

파이썬에서 `x = 1`이 느린 이유가 여기 있습니다. 정수 하나도 **refcount + type 포인터 + 값**을 갖는 힙 객체이고, `a + b`는 두 포인터를 역참조해 타입 슬롯을 찾아 함수를 호출합니다.

*실측*

```python
import sys

sys.getsizeof(0)            # 28  (헤더 24 + 값)
sys.getsizeof(2**64)        # 40  (자릿수만큼 커진다)
sys.getsizeof("")           # 49
sys.getsizeof("a")          # 50  ← ASCII는 1바이트/문자
sys.getsizeof("한")          # 76  ← 비ASCII는 표현이 바뀐다
sys.getsizeof([])           # 56
sys.getsizeof([1, 2, 3])    # 88  (리스트는 포인터 배열만, 원소 크기는 별도)
sys.getsizeof({})           # 64
sys.getsizeof(())           # 40
```

**⚠️ Gotcha**

`getsizeof`는 **얕은 크기**입니다. `[obj] * 1000`은 포인터 1000개 크기만 보고하고 원소 자체는 세지 않습니다. 실제 사용량은 `tracemalloc`이나 `pympler`로 재세요.

## list의 과할당

*growth*

```python
xs = []
prev = 0
for i in range(20):
    xs.append(i)
    size = sys.getsizeof(xs)
    if size != prev:
        print(len(xs), size)     # 1,88 / 5,120 / 9,184 / 17,256 …
        prev = size
```

`append`는 자리가 모자랄 때 **필요한 양보다 넉넉히**(대략 1.125배 + 상수) 재할당합니다. 그래서 append의 *평균* 비용이 O(1)입니다. 반대로 `insert(0, x)`와 `pop(0)`은 전체를 밀어야 해서 O(n) — 이때 `deque`를 씁니다.

## dict: compact dict

*구조 (개념)*

```text
# 3.6+ 딕셔너리는 두 부분으로 나뉜다
indices = [None, 1, None, 0, ...]        # 해시 → entries 인덱스 (희소, 작은 정수 배열)
entries = [(hash, key, value),           # 삽입 순서대로 빽빽하게 (조밀)
           (hash, key, value)]
```

삽입 순서가 보장되는 것은 **이 구조의 부수 효과**였고, 3.7부터 명세가 되었습니다. 메모리도 이전보다 20~25% 줄었습니다.

인스턴스 속성은 **key-sharing dict**를 씁니다. 같은 클래스의 인스턴스들이 키 배열을 공유하므로, 인스턴스가 많아도 키 문자열이 중복 저장되지 않습니다. 단 `__init__` 밖에서 임의로 속성을 추가하면 공유가 깨져 개별 dict로 분리됩니다.

**🖥 REPL 퀴즈 — 22-1 · __slots__의 실제 효과**

```python
>>> class A:
...     def __init__(self): self.x, self.y = 1, 2
>>> class B:
...     __slots__ = ("x", "y")
...     def __init__(self): self.x, self.y = 1, 2
>>> sys.getsizeof(A().__dict__)
>>> hasattr(B(), "__dict__")
```

---

**🟢 출력 보기**

```text
104   (인스턴스 객체 자체와 별도로 dict가 더 붙는다)
False
```

slots 인스턴스는 dict 없이 **고정 오프셋 배열**에 값을 담습니다. 100만 개 기준 수백 MB 차이가 나기도 합니다. 대신 속성 추가 불가, 다중 상속 제약, `weakref`를 쓰려면 `"__weakref__"`를 슬롯에 명시해야 합니다.

---

## 참조 카운팅과 GC

*gc*

```python
import gc, sys, weakref

sys.getrefcount(obj)         # 인자로 넘기는 순간 +1 되므로 항상 1 크게 나온다

gc.get_threshold()           # (700, 10, 10) — 0세대 700회 초과 할당마다 수거
gc.get_count()
gc.collect(generation=2)     # 전체 수거
gc.freeze()                  # fork 전에 호출하면 CoW 페이지 낭비를 줄인다 (gunicorn 등)

class Node:
    def __init__(self, parent=None):
        self.parent = weakref.ref(parent) if parent else None   # 순환 끊기
```

참조 카운트가 0이 되면 **즉시** 해제됩니다. 세대별 GC는 오직 **순환 참조**를 청소하기 위해 존재합니다. 그래서 순환을 안 만들면 GC를 꺼도(`gc.disable()`) 문제가 없고, 실제로 지연에 민감한 서비스에서 그렇게 하기도 합니다.

**💡 Tip · 컨테이너 배포에서 자주 쓰는 조합**

워커 fork 직전에 `gc.freeze()`를 호출하면 이미 로드된 객체들이 GC 대상에서 빠져, 자식 프로세스에서 refcount 변경으로 인한 **Copy-on-Write 페이지 복사**가 크게 줄어듭니다. 프리포크 서버(gunicorn, uWSGI) 메모리 절감의 표준 트릭입니다.

### 🏋 DRILL 22 — 메모리

1. list와 tuple, set과 frozenset의 크기를 원소 수를 늘려가며 측정해 그래프로 그리세요.
2. 같은 데이터를 dataclass / slots dataclass / NamedTuple / dict로 각각 10만 개 만들어 `tracemalloc` 피크를 비교하세요.
3. 부모↔자식 순환 참조를 만들고 `gc.disable()` 상태에서 메모리가 해제되지 않는 것을 확인한 뒤 `weakref`로 고치세요.
4. `gc.set_debug(gc.DEBUG_SAVEALL)`로 수거된 객체를 `gc.garbage`에서 확인해 어떤 타입이 순환을 만드는지 관찰하세요.
