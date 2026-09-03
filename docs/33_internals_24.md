# 24 · 인터닝 · 스페셜라이제이션 · GIL 내부

`PEP 659 · PEP 703 · C 확장`

## 인터닝

*interning*

```python
import sys

a = "hello_world"
b = "hello_world"
a is b                 # True  — 식별자처럼 생긴 리터럴은 자동 인터닝

c = "hello world!"     # 공백·특수문자가 있으면 자동 인터닝 대상이 아니다
d = "hello world!"
c is d                 # 컴파일 단위가 같으면 True, 런타임 생성이면 False

key = sys.intern(user_input)    # 같은 문자열이 대량 반복될 때 메모리·비교 속도 이득
```

인터닝된 문자열끼리는 **포인터 비교 한 번**으로 같음을 판단합니다. dict 키 조회가 빠른 이유 중 하나입니다. 단 이것에 의존한 `is` 비교는 절대 금지입니다(03파트).

## 적응형 특화 인터프리터 (3.11+, PEP 659)

CPython은 이제 **실행하면서 자기 바이트코드를 다시 씁니다**. 같은 명령이 반복 실행되며 매번 같은 타입을 만나면, 범용 명령을 특화 명령으로 교체합니다.

*dis(adaptive=True)*

```python
import dis

def add(a, b): return a + b

for _ in range(100):
    add(1, 2)                    # 정수만 계속 들어오면…

dis.dis(add, adaptive=True)
# BINARY_OP → BINARY_OP_ADD_INT 로 특화됨 (인라인 캐시 포함)
```

- **quickening**: 몇 번 실행된 뒤 특화 시도
- **inline cache**: 속성 조회 결과, 타입 정보를 명령 옆에 저장
- **deoptimization**: 가정이 깨지면(다른 타입이 오면) 범용 명령으로 되돌림

실무적 함의: **같은 함수에 여러 타입을 섞어 넣지 마세요.** 타입이 일관되면 인터프리터가 알아서 빨라집니다. 3.12는 컴프리헨션 인라이닝(PEP 709)으로 프레임 생성 비용까지 없앴습니다.

## GIL은 어떻게 넘어가는가

*GIL*

```python
import sys

sys.getswitchinterval()          # 0.005 — 기본 5ms
sys.setswitchinterval(0.001)
```

GIL은 "N개 바이트코드마다"가 아니라 **시간 간격(기본 5ms)**으로 다른 스레드에 넘어갑니다. 또 I/O 호출과 `time.sleep`, numpy의 무거운 C 연산은 진입 시 GIL을 **자발적으로 반납**합니다. 그래서 numpy 연산은 스레드로도 병렬화가 됩니다.

**💡 3.13 free-threaded build (PEP 703)**

`python3.13t` 빌드는 GIL 없이 동작합니다. 진짜 멀티코어 병렬이 되지만, ① 단일 스레드 성능이 다소 떨어지고 ② C 확장이 free-threading을 지원해야 하며 ③ 그동안 GIL이 공짜로 주던 **자료구조 원자성이 사라집니다**. 아직 실험 단계이지만, 앞으로 파이썬 동시성 코드의 전제가 바뀔 지점이라 흐름은 따라가 둘 가치가 있습니다.

## 더 빠르게 해야 할 때의 선택지

| 방법 | 적합한 경우 | 비용 |
| --- | --- | --- |
| numpy / polars 벡터화 | 배열·표 형태 수치 연산 | 낮음 — 대부분 여기서 해결 |
| `ProcessPoolExecutor` | 독립적인 CPU 작업 다수 | 직렬화·프로세스 비용 |
| Cython / mypyc | 핫스팟 함수 몇 개 | 빌드 파이프라인 추가 |
| Rust 확장(PyO3) / C 확장 | 라이브러리 수준 최적화 | 높음 — 별도 언어 |
| PyPy | 순수 파이썬 장시간 실행 | C 확장 호환성 제약 |

### 🏋 DRILL 24 — 내부 최적화

1. 단일 타입만 받는 함수와 int/str/float를 번갈아 받는 함수를 각각 100만 번 호출해 시간 차이를 재고, `dis(adaptive=True)`로 특화 여부를 확인하세요.
2. `sys.intern`을 적용한 경우와 아닌 경우 100만 개 반복 문자열의 메모리를 비교하세요.
3. `sys.setswitchinterval`을 크게/작게 바꾸며 스레드 두 개의 처리량과 지연을 관찰하세요.
4. 순수 파이썬 핫스팟 함수 하나를 골라 numpy 벡터화로 바꾸고 개선 배수를 기록하세요.
