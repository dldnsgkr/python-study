"""B13 · 함수 더 깊이 채점."""

import pytest

from basics.b13_functions_deep import (
    append_safe,
    apply_twice,
    build_tag,
    bump,
    factorial,
    make_accumulator,
    make_multiplier,
    make_url,
    min_max,
    reset_counter,
    sum_nested,
    total,
)


class TestMakeUrl:
    def test_defaults(self):
        assert make_url("a.com") == "http://a.com:80"

    def test_keyword_arguments(self):
        assert make_url("a.com", port=443, secure=True) == "https://a.com:443"
        with pytest.raises(TypeError):
            make_url("a.com", 443)        # * 뒤는 이름으로만 넘길 수 있다

    def test_port_only(self):
        assert make_url("a.com", port=8080) == "http://a.com:8080"


class TestTotal:
    def test_sums_any_number_of_arguments(self):
        assert total(1, 2, 3) == 6
        assert total(5) == 5

    def test_no_arguments(self):
        assert total() == 0


class TestBuildTag:
    def test_no_attributes(self):
        assert build_tag("a") == "<a>"

    def test_keeps_the_given_order(self):
        assert build_tag("a", href="x", id="y") == '<a href="x" id="y">'

    def test_single_attribute(self):
        assert build_tag("img", src="p.png") == '<img src="p.png">'


class TestMinMax:
    def test_returns_both(self):
        assert min_max([3, 1, 2]) == (1, 3)

    def test_unpacking_works(self):
        low, high = min_max([5, 9, 1])
        assert (low, high) == (1, 9)

    def test_single_element(self):
        assert min_max([7]) == (7, 7)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            min_max([])


class TestApplyTwice:
    def test_with_lambda(self):
        assert apply_twice(lambda x: x + 1, 1) == 3

    def test_with_a_named_function(self):
        assert apply_twice(str.upper, "a") == "A"

    def test_with_a_list_operation(self):
        assert apply_twice(lambda xs: xs + [0], []) == [0, 0]


class TestMakeMultiplier:
    def test_remembers_n(self):
        double = make_multiplier(2)
        assert double(5) == 10

    def test_each_one_is_independent(self):
        double, triple = make_multiplier(2), make_multiplier(3)
        assert (double(5), triple(5)) == (10, 15)

    def test_returns_a_function(self):
        assert callable(make_multiplier(2))


class TestMakeAccumulator:
    def test_accumulates(self):
        acc = make_accumulator()
        assert acc(10) == 10
        assert acc(5) == 15
        assert acc(0) == 15

    def test_accumulators_are_independent(self):
        a, b = make_accumulator(), make_accumulator()
        a(100)
        assert b(1) == 1


class TestBump:
    def test_increments_the_global(self):
        reset_counter()
        assert bump() == 1
        assert bump() == 2

    def test_reset_works(self):
        reset_counter()
        bump()
        reset_counter()
        assert bump() == 1


class TestFactorial:
    @pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (5, 120), (10, 3_628_800)])
    def test_factorial(self, n, expected):
        assert factorial(n) == expected

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)


class TestSumNested:
    def test_nested(self):
        assert sum_nested([1, [2, [3, 4]], 5]) == 15

    def test_flat(self):
        assert sum_nested([1, 2]) == 3

    def test_empty(self):
        assert sum_nested([]) == 0
        assert sum_nested([[], [[]]]) == 0

    def test_deeply_nested(self):
        assert sum_nested([[[[[1]]]]]) == 1


class TestAppendSafe:
    def test_creates_a_new_list_each_call(self):
        assert append_safe(1) == [1]
        assert append_safe(2) == [2]      # [1, 2] 가 나오면 가변 기본값 함정에 빠진 것

    def test_uses_the_given_list(self):
        assert append_safe(3, [0]) == [0, 3]

    def test_many_calls_stay_independent(self):
        results = [append_safe(i) for i in range(3)]
        assert results == [[0], [1], [2]]
