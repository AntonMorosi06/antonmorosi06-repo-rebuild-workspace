from __future__ import annotations

from datetime import datetime


MISSING_MARKERS = {"", "na", "n/a", "null", "none", "nan", "-", "--"}


def is_missing(value: str) -> bool:
    return value is None or str(value).strip().lower() in MISSING_MARKERS


def non_missing(values: list[str]) -> list[str]:
    return [value for value in values if not is_missing(value)]


def parse_int(value: str) -> int | None:
    try:
        cleaned = str(value).strip().replace(",", "")
        if cleaned == "":
            return None
        if "." in cleaned:
            return None
        return int(cleaned)
    except ValueError:
        return None


def parse_float(value: str) -> float | None:
    try:
        cleaned = str(value).strip().replace(",", "")
        if cleaned == "":
            return None
        return float(cleaned)
    except ValueError:
        return None


def parse_bool(value: str) -> bool | None:
    cleaned = str(value).strip().lower()
    truthy = {"true", "t", "yes", "y", "1"}
    falsey = {"false", "f", "no", "n", "0"}

    if cleaned in truthy:
        return True
    if cleaned in falsey:
        return False
    return None


def parse_date_like(value: str) -> datetime | None:
    cleaned = str(value).strip()
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue

    return None


def infer_type(values: list[str]) -> str:
    present = non_missing(values)
    if not present:
        return "empty"

    int_count = sum(1 for value in present if parse_int(value) is not None)
    float_count = sum(1 for value in present if parse_float(value) is not None)
    bool_count = sum(1 for value in present if parse_bool(value) is not None)
    date_count = sum(1 for value in present if parse_date_like(value) is not None)

    total = len(present)
    threshold = 0.92

    if bool_count / total >= threshold:
        return "boolean"

    if int_count / total >= threshold:
        return "integer"

    if float_count / total >= threshold:
        return "float"

    if date_count / total >= threshold:
        return "date"

    return "categorical"


def coerce_numeric(values: list[str]) -> list[float]:
    numbers: list[float] = []
    for value in values:
        if is_missing(value):
            continue
        parsed = parse_float(value)
        if parsed is not None:
            numbers.append(parsed)
    return numbers
