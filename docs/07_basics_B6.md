# B6 · 클래스 — 나만의 데이터 종류 만들기

`class · 객체 · 메서드`

B2에서 int·str 같은 **타입**을 배웠습니다. 클래스는 **내가 직접 새로운 타입을 만드는** 방법입니다. "학생", "자동차", "은행계좌"처럼 현실의 무언가를 코드로 표현할 때 씁니다.

*클래스 정의와 사용*

```python
class Dog:
    def __init__(self, name, age):     # 초기 설정 (붕어빵 틀에 속 넣기)
        self.name = name               # 이 강아지의 이름
        self.age = age                 # 이 강아지의 나이

    def bark(self):                    # 이 강아지가 할 수 있는 행동
        return f"{self.name}: 멍멍!"

# 객체 만들기 (틀로 붕어빵 찍기)
my_dog = Dog("바둑이", 3)
your_dog = Dog("초코", 5)

# 데이터 꺼내기
my_dog.name              # "바둑이"
your_dog.age             # 5

# 행동 시키기 (메서드 호출)
my_dog.bark()            # "바둑이: 멍멍!"
```

낯선 단어들을 하나씩 풀어봅니다.

- `class Dog:` — "Dog라는 새 타입을 만든다". 클래스 이름은 보통 **대문자로 시작**합니다.
- `__init__` — 객체가 **처음 만들어질 때 자동 실행**되는 특별한 함수. 초기 데이터를 채웁니다. (앞뒤 밑줄 두 개가 "특별함"의 표시입니다.)
- `self` — **"이 객체 자신"**을 가리킵니다. `self.name`은 "이 강아지의 이름". 여러 붕어빵을 구별하는 장치입니다.
- **메서드** — 클래스 안에 정의된 함수. 그 객체가 할 수 있는 **행동**입니다.

**💡 self가 어렵게 느껴지면**

`self`는 처음엔 누구나 헷갈립니다. 이렇게 생각하세요. `my_dog.bark()`를 부르면 파이썬이 속으로 "어떤 강아지? my_dog이구나" 하고 그 객체를 `self`로 넣어줍니다. 그래서 메서드 안 `self.name`이 "바둑이"가 됩니다. 정의할 땐 `self`를 항상 첫 번째로 적고, 부를 땐 신경 쓰지 않아도 됩니다.

사실 우리는 클래스를 계속 써 왔습니다. `"안녕".upper()`의 `upper`, `[1,2].append(3)`의 `append`가 전부 str·list 클래스의 메서드입니다. 파이썬에서는 **모든 것이 객체**이고, 그 객체의 타입이 클래스입니다.

### 🏋 실습 B6 — 클래스

1. `Person` 클래스를 만들어 이름·나이를 담고, 자기소개를 돌려주는 메서드를 추가하세요.
2. `BankAccount` 클래스를 만들어 잔액을 담고, 입금·출금 메서드를 만드세요.
3. 같은 클래스로 객체 두 개를 만들어, 서로 데이터가 독립적인지 확인하세요.

---

**🟢 2번 답**

```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "잔액 부족"
        self.balance = self.balance - amount
        return self.balance

account = BankAccount(1000)
account.deposit(500)         # 1500
account.withdraw(200)        # 1300
```

---
