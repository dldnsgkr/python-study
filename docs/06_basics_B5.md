# B5 · 함수 — 나만의 명령 만들기

`def · 매개변수 · 반환값`

`print()`나 `len()`처럼, 우리도 **직접 명령을 만들** 수 있습니다. 그게 함수입니다. 자주 쓰는 코드 묶음에 이름을 붙여두고, 필요할 때마다 그 이름으로 부릅니다.

*함수 만들고 쓰기*

```python
# 만들기 (정의)
def greet(name):
    return f"안녕하세요, {name}님!"

# 쓰기 (호출)
message = greet("김파이")
print(message)               # 안녕하세요, 김파이님!

print(greet("이자바"))        # 안녕하세요, 이자바님!
```

구조를 뜯어봅니다.

- `def`는 "정의한다(define)"의 줄임. "지금부터 함수를 만들게"라는 신호.
- `greet`는 함수 이름. 변수처럼 의미 있게 짓습니다.
- 괄호 안 `name`은 **매개변수** — 받을 입력에 붙인 이름표.
- `return`은 **결과를 돌려주는** 명령. 이 값이 함수를 부른 자리로 돌아갑니다.

*입력이 여럿, 또는 없을 수도*

```python
# 입력 두 개
def add(a, b):
    return a + b

add(3, 5)                    # 8

# 입력 없이도 가능
def say_hello():
    return "안녕!"

say_hello()                  # "안녕!"

# 기본값 주기 (안 넣으면 이 값 사용)
def greet(name, greeting="안녕하세요"):
    return f"{greeting}, {name}님!"

greet("김파이")                    # "안녕하세요, 김파이님!"
greet("김파이", "반갑습니다")        # "반갑습니다, 김파이님!"
```

**⚠️ return과 print는 다르다**

초보자가 자주 헷갈립니다. `print`는 화면에 **보여주기만** 하고, `return`은 값을 **돌려줘서 계속 쓸 수 있게** 합니다. `return`한 값은 변수에 담거나 다른 계산에 넣을 수 있지만, `print`만 한 값은 화면에 찍고 사라집니다. 계산 결과를 이어서 쓰려면 반드시 `return`이 필요합니다.

*왜 함수가 좋은가 — 반복을 없앤다*

```python
# 함수 없이: 같은 계산을 여기저기 반복
price1 = 10000 * 1.1
price2 = 25000 * 1.1
price3 = 8000 * 1.1

# 함수로: 규칙을 한 곳에 정의
def with_tax(price):
    return price * 1.1

price1 = with_tax(10000)
price2 = with_tax(25000)
price3 = with_tax(8000)
# 세율이 바뀌어도 함수 한 곳만 고치면 된다!
```

### 🏋 실습 B5 — 함수

1. 두 수를 받아 곱을 돌려주는 `multiply(a, b)`를 만드세요.
2. 이름을 받아 "환영합니다, OOO님"을 **돌려주는**(print 아님!) 함수를 만들고, 그 결과를 변수에 담아 출력하세요.
3. 섭씨를 화씨로 바꾸는 함수를 만드세요. (화씨 = 섭씨 × 9/5 + 32)
4. 리스트를 받아 그 안 숫자들의 평균을 돌려주는 함수를 만드세요. (힌트: `sum()`과 `len()`)

---

**🟢 3·4번 답**

```python
# 3) 섭씨 → 화씨
def to_fahrenheit(celsius):
    return celsius * 9/5 + 32

to_fahrenheit(100)       # 212.0

# 4) 평균
def average(numbers):
    return sum(numbers) / len(numbers)

average([90, 80, 100])   # 90.0
```

`sum()`은 리스트 숫자를 다 더하고, `len()`은 개수를 셉니다. 둘을 나누면 평균이죠.

---
