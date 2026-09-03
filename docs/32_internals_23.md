# 23 · 바이트코드 · 프레임 · 평가 루프

`code object · cell · exception table`

## 코드 객체

*code object*

```python
def outer(a, b=2):
    c = a + b
    def inner():
        return c            # 자유 변수
    return inner

co = outer.__code__
co.co_varnames      # ('a', 'b', 'inner')   지역 변수 이름
co.co_cellvars      # ('c',)                내부 함수에 넘겨줄 변수
co.co_consts        # (None, <code inner>)  중첩 함수도 상수로 들어 있다
co.co_names         # 전역/속성 이름
co.co_argcount, co.co_kwonlyargcount, co.co_flags
```

함수는 **코드 객체 + 기본값 + 클로저 + 전역 네임스페이스 참조**를 묶은 얇은 껍데기입니다. 그래서 `func.__defaults__`를 바꾸거나 같은 코드 객체로 다른 함수를 만드는 일이 가능합니다.

*클로저의 정체 = cell*

```python
f = outer(1)
f.__closure__            # (<cell at 0x…: int object at 0x…>,)
f.__closure__[0].cell_contents    # 3
```

07파트의 "늦은 바인딩"은 여기서 설명됩니다. 클로저는 값이 아니라 **cell 객체**를 붙잡고 있고, cell 안의 내용은 나중에 바뀔 수 있습니다.

## 지역 변수는 배열, 전역 변수는 dict

*dis 비교*

```python
import dis

GLOBAL = 1
def use_global(): return GLOBAL
def use_local():
    local = 1
    return local

dis.dis(use_global)    # LOAD_GLOBAL  ← 이름으로 dict 조회 (모듈 → 빌트인)
dis.dis(use_local)     # LOAD_FAST    ← 배열 인덱스 접근
```

루프 안에서 전역 함수나 메서드를 반복 호출할 때 `local_len = len`처럼 지역 이름에 캐시하면 빨라지는 이유가 이것입니다. (요즘은 스페셜라이제이션으로 격차가 줄었지만 여전히 유효합니다.)

## 프레임

*frame*

```python
import inspect, sys

def who_called_me():
    frame = inspect.currentframe().f_back
    return frame.f_code.co_name, frame.f_lineno, frame.f_locals

sys.setrecursionlimit(3000)     # 프레임 스택 한계 — 꼬리 재귀 최적화는 없다
```

예외의 트레이스백은 프레임 체인을 따라간 결과이고, 디버거·프로파일러·`logging`의 `%(funcName)s`도 전부 프레임을 읽습니다. 제너레이터와 코루틴은 **프레임을 힙에 보관했다가 재개**하는 물건입니다 — 그래서 지역 변수와 실행 위치가 그대로 살아남습니다.

*3.11의 zero-cost exceptions*

```python
co.co_exceptiontable       # 예외 처리 범위가 별도 테이블로 분리됨

# 이전: try 블록에 진입할 때마다 SETUP_FINALLY 명령 실행 (예외가 없어도 비용)
# 3.11+: 정상 경로에는 명령이 없고, 예외가 실제로 나면 테이블을 조회
```

결론: **예외가 발생하지 않는 `try`는 이제 사실상 공짜**입니다. EAFP 스타일을 더 자신 있게 쓸 수 있게 된 변화입니다.

**🖥 REPL 퀴즈 — 23-1 · 상수 폴딩**

```python
>>> def f(): return 60 * 60 * 24
>>> f.__code__.co_consts
>>> def g(): return "ab" * 3
>>> g.__code__.co_consts
```

---

**🟢 출력 보기**

```text
(None, 86400)
(None, 'ababab')
```

컴파일러가 상수식을 미리 계산해 둡니다(peephole 최적화). 그래서 가독성을 위해 `60 * 60 * 24`라고 써도 런타임 비용이 0입니다. 단, 결과가 너무 커지는 경우(`2**1000` 같은)는 폴딩하지 않습니다.

---

### 🏋 DRILL 23 — 바이트코드

1. 같은 로직을 for 루프 / 컴프리헨션 / `map`으로 작성하고 `dis` 출력을 나란히 비교하세요.
2. 클로저 변수를 담은 cell을 직접 꺼내 값을 확인하고, 늦은 바인딩 문제를 cell 관점에서 다시 설명하세요.
3. 재귀 함수의 최대 깊이를 실험으로 찾고, 같은 로직을 명시적 스택으로 바꿔 한계를 없애세요.
4. `try/except`가 있는 함수와 없는 함수의 바이트코드를 비교해 3.11 이후 정상 경로 비용이 없어졌음을 확인하세요.
