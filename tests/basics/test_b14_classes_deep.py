"""B14 · 클래스 더 깊이 채점."""

import pytest

from basics.b14_classes_deep import Animal, Cat, Dog, Point, Rectangle, describe


@pytest.fixture(autouse=True)
def _reset_count():
    """테스트마다 클래스 변수를 0으로 되돌린다.

    reset_count 를 아직 안 만들었어도 픽스처가 터지지 않게 해 둔다 —
    그러면 '실패' 대신 '에러' 가 쏟아져서 어디를 봐야 할지 모르게 되니까.
    """
    reset = getattr(Animal, "reset_count", None)
    if callable(reset):
        reset()
    yield
    if callable(reset):
        reset()


class TestInheritance:
    def test_overridden_speak(self):
        assert issubclass(Dog, Animal) and issubclass(Cat, Animal)
        assert Dog("바둑이").speak() == "바둑이: 멍멍"
        assert Cat("나비").speak() == "나비: 야옹"

    def test_base_speak(self):
        assert Animal("무명").speak() == "무명: ..."

    def test_super_runs_the_parent_init(self):
        dog = Dog("바둑이")
        assert dog.name == "바둑이"        # 부모가 저장한 필드

    def test_dog_has_its_own_field(self):
        assert Dog("바둑이", breed="진돗개").breed == "진돗개"
        assert Dog("바둑이").breed == "믹스"
        with pytest.raises(TypeError):
            Dog("바둑이", "진돗개")        # breed 는 키워드 전용

    def test_isinstance_sees_the_parent(self):
        assert isinstance(Dog("x"), Animal) is True
        assert isinstance(Animal("x"), Dog) is False


class TestClassVariable:
    def test_counts_every_animal(self):
        Dog("a")
        Cat("b")
        Animal("c")
        assert Animal.count == 3          # 클래스 변수는 상속한 것까지 공유한다

    def test_reset_count_is_a_classmethod(self):
        assert isinstance(Animal.__dict__["reset_count"], classmethod)

    def test_starts_at_zero_after_reset(self):
        Dog("a")
        Animal.reset_count()
        assert Animal.count == 0

    def test_instances_share_it(self):
        a = Dog("a")
        Dog("b")
        assert a.count == 2               # 인스턴스로 읽어도 같은 값


class TestPoint:
    def test_str_is_for_people(self):
        assert str(Point(1, 2)) == "(1, 2)"

    def test_repr_is_for_developers(self):
        assert repr(Point(1, 2)) == "Point(1, 2)"

    def test_equality_compares_values(self):
        assert Point(1, 2) == Point(1, 2)
        assert Point(1, 2) != Point(3, 4)

    def test_not_equal_to_other_types(self):
        assert Point(1, 2) != "Point(1, 2)"

    def test_from_string_is_an_alternative_constructor(self):
        assert Point.from_string("1,2") == Point(1, 2)

    def test_from_string_is_a_classmethod(self):
        assert isinstance(Point.__dict__["from_string"], classmethod)

    def test_distance_is_a_staticmethod(self):
        assert Point.distance(Point(0, 0), Point(3, 4)) == 5.0
        assert isinstance(Point.__dict__["distance"], staticmethod)


class TestRectangle:
    def test_area(self):
        assert Rectangle(3, 4).area == 12

    def test_area_is_a_property_not_a_method(self):
        assert isinstance(type(Rectangle(1, 1)).__dict__["area"], property)

    def test_area_follows_width_changes(self):
        r = Rectangle(3, 4)
        r.width = 5
        assert r.area == 20              # __init__ 에서 계산해 두면 여기서 걸린다

    def test_area_is_read_only(self):
        with pytest.raises(AttributeError):
            Rectangle(3, 4).area = 100

    @pytest.mark.parametrize("bad", [0, -1])
    def test_setter_validates(self, bad):
        with pytest.raises(ValueError):
            Rectangle(3, 4).width = bad

    def test_constructor_also_validates(self):
        with pytest.raises(ValueError):
            Rectangle(-1, 4)             # __init__ 이 setter 를 거쳐야 한다

    def test_error_message_shows_the_value(self):
        with pytest.raises(ValueError, match="-1"):
            Rectangle(3, 4).width = -1


class TestDescribe:
    def test_narrow_types_win(self):
        assert describe(Dog("바둑이")) == "개 바둑이"
        assert describe(Cat("나비")) == "고양이 나비"

    def test_base_type_falls_through(self):
        assert describe(Animal("무명")) == "동물 무명"

    def test_order_matters(self):
        # Animal 을 먼저 검사하면 Dog 도 "동물" 이 되어 버린다
        assert describe(Dog("x")).startswith("개")
