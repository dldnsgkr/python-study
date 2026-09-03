"""B8 모범답안."""

from __future__ import annotations


def initials(full_name: str) -> str:
    return "".join(word[0].upper() for word in full_name.split())


def slugify(title: str) -> str:
    return title.strip().lower().replace(" ", "-")


def join_with_comma(items: list[str]) -> str:
    return ", ".join(items)


def mask_email(email: str) -> str:
    local, _, domain = email.partition("@")
    return f"{local[0]}{'*' * (len(local) - 1)}@{domain}"


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + "..."


def title_case(text: str) -> str:
    return " ".join(word[0].upper() + word[1:] for word in text.split())


def is_palindrome(text: str) -> bool:
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def count_char(text: str, char: str) -> int:
    return text.lower().count(char.lower())
