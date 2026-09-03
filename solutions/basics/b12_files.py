"""B12 모범답안."""

from __future__ import annotations


def write_lines(path: str, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def append_line(path: str, line: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def count_lines(path: str) -> int:
    total = 0
    with open(path, encoding="utf-8") as f:
        for _ in f:                    # 파일 전체를 메모리에 올리지 않는다
            total += 1
    return total


def word_frequencies(path: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            for word in line.lower().split():
                counts[word] = counts.get(word, 0) + 1
    return counts


def main() -> str:
    return "b12 실행됨"


if __name__ == "__main__":
    print(main())
