"""B3 · 컬렉션 채점."""

from basics.b03_collections import add_food, add_hobby, has_key, profile_lines, unique_sorted


class TestAddFood:
    def test_returns_first_and_last(self):
        assert add_food(["치킨", "피자"], "떡볶이") == ("치킨", "떡볶이")

    def test_does_not_touch_the_original(self):
        foods = ["치킨", "피자"]
        add_food(foods, "떡볶이")
        assert foods == ["치킨", "피자"]      # append 를 그대로 쓰면 여기서 걸린다


def test_profile_lines_keeps_insertion_order():
    profile = {"이름": "김파이", "나이": 25, "취미": "등산"}
    assert profile_lines(profile) == ["이름: 김파이", "나이: 25", "취미: 등산"]


def test_unique_sorted():
    assert unique_sorted([3, 1, 3, 2, 1]) == [1, 2, 3]
    assert unique_sorted([]) == []


class TestAddHobby:
    def test_adds(self):
        assert add_hobby({"이름": "김파이"}, "등산") == {"이름": "김파이", "취미": "등산"}

    def test_original_is_untouched(self):
        profile = {"이름": "김파이"}
        add_hobby(profile, "등산")
        assert profile == {"이름": "김파이"}


def test_has_key():
    assert has_key({"이름": "김파이"}, "이름") is True
    assert has_key({"이름": "김파이"}, "나이") is False
