"""B12 · 파일과 모듈 — 프로그램 밖의 세상

지금까지는 전부 프로그램 안에서만 놀았습니다. 이제 파일을 읽고 씁니다.

이번 파트에서 쓰는 도구:
    with open(경로, "r", encoding="utf-8") as f:   읽기
    with open(경로, "w", encoding="utf-8") as f:   쓰기 (기존 내용을 지운다!)
    with open(경로, "a", encoding="utf-8") as f:   덧붙이기
    f.read()        전체를 문자열 하나로
    f.readlines()   줄 리스트로
    for line in f:  한 줄씩 (파일이 커도 안전)
    f.write(문자열)  print 와 달리 줄바꿈이 자동으로 안 붙는다

⚠️ encoding="utf-8" 을 항상 적으세요.
   안 적으면 운영체제 기본값을 쓰는데, 윈도우에서는 cp949 라서 한글이 깨집니다.
   "내 맥에선 되는데요" 의 대표적 원인입니다.

⚠️ with 를 쓰세요.
   with 블록을 벗어나면 파일이 자동으로 닫힙니다. 직접 open/close 하면
   중간에 예외가 났을 때 파일이 열린 채 남습니다.
"""

from __future__ import annotations


def write_lines(path: str, lines: list[str]) -> None:
    """각 줄을 파일에 쓴다. 줄마다 줄바꿈을 붙인다. 기존 내용은 덮어쓴다.

    write_lines(p, ["첫 줄", "둘째 줄"])  ->  파일 내용은 "첫 줄\\n둘째 줄\\n"

    f.write() 는 print 와 달리 줄바꿈을 자동으로 붙이지 않습니다. 직접 "\\n" 을 넣으세요.
    """
    raise NotImplementedError


def read_lines(path: str) -> list[str]:
    """파일을 줄 리스트로 읽는다. 각 줄 끝의 줄바꿈은 제거.

    read_lines(p) == ["첫 줄", "둘째 줄"]

    파일이 없으면 FileNotFoundError 가 그대로 올라갑니다(여기서 잡지 마세요).
    """
    raise NotImplementedError


def append_line(path: str, line: str) -> None:
    """파일 끝에 한 줄을 덧붙인다. 파일이 없으면 새로 만든다.

    모드 "a" 를 씁니다. "w" 로 열면 **기존 내용이 전부 사라집니다** —
    로그 파일을 통째로 날려 먹는 실수의 원인입니다.
    """
    raise NotImplementedError


def count_lines(path: str) -> int:
    """줄 수를 센다.

    ⚠️ f.read() 로 전부 올리지 말고 `for line in f:` 로 한 줄씩 세세요.
       10GB 로그 파일에도 같은 코드가 그대로 돕니다.
    """
    raise NotImplementedError


def word_frequencies(path: str) -> dict[str, int]:
    """파일에 나온 단어의 빈도. 공백으로 나누고 소문자로 통일.

    B9의 count_words 와 B12의 파일 읽기를 합치는 문제입니다.
    작은 함수를 조합해 큰 일을 하는 것 — 이게 프로그래밍의 전부입니다.
    """
    raise NotImplementedError


def main() -> str:
    """이 파일을 직접 실행했을 때 할 일.

    "b12 실행됨" 을 돌려주기만 하면 됩니다.

    아래 `if __name__ == "__main__":` 가 이 파일의 마지막 주제입니다.
        - 파일을 `python b12_files.py` 로 **직접 실행**하면 __name__ 은 "__main__"
        - 다른 파일에서 `import` 하면 __name__ 은 "b12_files"
    그래서 저 줄은 "직접 실행할 때만 돌려라"라는 뜻입니다.

    이게 없으면 import 하는 순간 프로그램이 실행돼 버립니다.
    테스트가 정확히 그걸 확인합니다 — import 해도 아무 일이 없어야 합니다.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print(main())
