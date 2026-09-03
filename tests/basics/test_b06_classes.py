"""B6 · 클래스 채점."""

import pytest

from basics.b06_classes import BankAccount, Person


class TestPerson:
    def test_stores_fields(self):
        p = Person("김파이", 25)
        assert p.name == "김파이"
        assert p.age == 25

    def test_introduce(self):
        assert Person("김파이", 25).introduce() == "저는 김파이이고 25살입니다"


class TestBankAccount:
    def test_deposit_and_withdraw_return_balance(self):
        account = BankAccount(1000)
        assert account.deposit(500) == 1500
        assert account.withdraw(200) == 1300
        assert account.balance == 1300

    def test_default_balance_is_zero(self):
        assert BankAccount().balance == 0

    def test_overdraw_raises(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.withdraw(1000)
        assert account.balance == 100        # 실패한 출금이 잔액을 건드리면 안 된다

    @pytest.mark.parametrize("amount", [0, -100])
    def test_non_positive_amount_raises(self, amount):
        account = BankAccount(1000)
        with pytest.raises(ValueError):
            account.deposit(amount)
        with pytest.raises(ValueError):
            account.withdraw(amount)

    def test_instances_are_independent(self):
        a, b = BankAccount(1000), BankAccount(1000)
        a.deposit(500)
        assert b.balance == 1000
