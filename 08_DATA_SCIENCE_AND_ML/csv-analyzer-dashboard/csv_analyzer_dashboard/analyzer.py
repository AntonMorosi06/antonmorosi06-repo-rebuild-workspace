from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from .inference import coerce_numeric, infer_type, is_missing, non_missing, parse_float
from .loader import column_values, columns_from_rows, load_csv
from .statistics import numeric_summary, pearson_correlation, top_values


@dataclass
class ColumnProfile:
    name: str
    inferred_type: str
    total_count: int
    missing_count: int
    missing_ratio: float
    unique_count: int
    numeric_summary: dict[str, float | int] | None
    top_values: list[dict[str, int | str]]


@dataclass
class DatasetAnalysis:
    source: str
    row_count: int
    column_count: int
    columns: list[ColumnProfile]
    correlations: list[dict[str, float | str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "columns": [asdict(column) for column in self.columns],
            "correlations": self.correlations,
        }


def analyze_column(name: str, values: list[str]) -> ColumnProfile:
    total = len(values)
    missing = sum(1 for value in values if is_missing(value))
    present = non_missing(values)
    inferred = infer_type(values)
    unique_count = len(set(present))
    missing_ratio = 0.0 if total == 0 else missing / total

    numeric = None
    if inferred in {"integer", "float"}:
        numeric = numeric_summary(coerce_numeric(values))

    categorical_values = present if inferred not in {"integer", "float"} else [str(value) for value in present]
    top = top_values(categorical_values, limit=8)

    return ColumnProfile(
        name=name,
        inferred_type=inferred,
        total_count=total,
        missing_count=missing,
        missing_ratio=missing_ratio,
        unique_count=unique_count,
        numeric_summary=numeric,
        top_values=top,
    )


def aligned_numeric_pairs(rows: list[dict[str, str]], col_a: str, col_b: str) -> tuple[list[float], list[float]]:
    a_values: list[float] = []
    b_values: list[float] = []

    for row in rows:
        a = row.get(col_a, "")
        b = row.get(col_b, "")

        if is_missing(a) or is_missing(b):
            continue

        parsed_a = parse_float(a)
        parsed_b = parse_float(b)

        if parsed_a is None or parsed_b is None:
            continue

        a_values.append(parsed_a)
        b_values.append(parsed_b)

    return a_values, b_values


def compute_correlations(rows: list[dict[str, str]], profiles: list[ColumnProfile]) -> list[dict[str, float | str]]:
    numeric_columns = [
        profile.name
        for profile in profiles
        if profile.inferred_type in {"integer", "float"}
    ]

    correlations: list[dict[str, float | str]] = []

    for i, col_a in enumerate(numeric_columns):
        for col_b in numeric_columns[i + 1:]:
            values_a, values_b = aligned_numeric_pairs(rows, col_a, col_b)
            if len(values_a) < 3:
                continue

            correlations.append({
                "column_a": col_a,
                "column_b": col_b,
                "correlation": pearson_correlation(values_a, values_b),
                "pair_count": len(values_a),
            })

    correlations.sort(key=lambda item: abs(float(item["correlation"])), reverse=True)
    return correlations


def analyze_rows(rows: list[dict[str, str]], source: str = "in-memory") -> DatasetAnalysis:
    columns = columns_from_rows(rows)
    profiles = [
        analyze_column(column, column_values(rows, column))
        for column in columns
    ]
    correlations = compute_correlations(rows, profiles)

    return DatasetAnalysis(
        source=source,
        row_count=len(rows),
        column_count=len(columns),
        columns=profiles,
        correlations=correlations,
    )


def analyze_csv(path: str | Path, encoding: str = "utf-8") -> DatasetAnalysis:
    path = Path(path)
    rows = load_csv(path, encoding=encoding)
    return analyze_rows(rows, source=str(path))
