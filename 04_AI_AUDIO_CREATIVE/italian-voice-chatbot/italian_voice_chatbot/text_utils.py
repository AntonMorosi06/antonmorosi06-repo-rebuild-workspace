from __future__ import annotations

import re
import unicodedata


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_text(text: str) -> str:
    text = strip_accents(text.lower().strip())
    text = re.sub(r"[^a-z0-9àèéìòùç\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_any(text: str, keywords: list[str]) -> bool:
    normalized = normalize_text(text)
    return any(normalize_text(keyword) in normalized for keyword in keywords)


def is_exit_command(text: str) -> bool:
    normalized = normalize_text(text)
    return normalized in {"exit", "quit", "esci", "chiudi", "basta", "ciao"}
