from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def sniff_dialect(path: Path, encoding: str = "utf-8") -> csv.Dialect:
    sample = path.read_text(encoding=encoding, errors="replace")[:4096]

    try:
        return csv.Sniffer().sniff(sample)
    except csv.Error:
        return csv.excel


def load_csv(path: str | Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    dialect = sniff_dialect(path, encoding=encoding)

    with path.open("r", encoding=encoding, errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        if reader.fieldnames is None:
            raise ValueError("CSV file has no header row")

        rows: list[dict[str, str]] = []
        for row in reader:
            normalized = {
                str(key).strip(): "" if value is None else str(value).strip()
                for key, value in row.items()
                if key is not None
            }
            rows.append(normalized)

    return rows


def columns_from_rows(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []

    seen: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.append(key)
    return seen


def column_values(rows: list[dict[str, str]], column: str) -> list[str]:
    return [row.get(column, "") for row in rows]
