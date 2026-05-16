from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


COMMON_SEPARATORS = [",", ";", "\t", "|"]


@dataclass
class CsvReadResult:
    dataframe: pd.DataFrame
    path: Path
    separator: str
    encoding: str


def read_csv_smart(
    path: str | Path,
    sep: Optional[str] = None,
    encoding: str = "utf-8",
) -> CsvReadResult:
    csv_path = Path(path).expanduser().resolve()

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if not csv_path.is_file():
        raise ValueError(f"Path is not a file: {csv_path}")

    encodings_to_try = [encoding]
    if encoding.lower() != "utf-8":
        encodings_to_try.append("utf-8")
    for fallback in ["utf-8-sig", "latin-1"]:
        if fallback not in encodings_to_try:
            encodings_to_try.append(fallback)

    separators_to_try = [sep] if sep else COMMON_SEPARATORS

    last_error = None

    for enc in encodings_to_try:
        for separator in separators_to_try:
            try:
                df = pd.read_csv(csv_path, sep=separator, encoding=enc)
                if df.shape[1] > 1 or separator == separators_to_try[-1]:
                    return CsvReadResult(
                        dataframe=df,
                        path=csv_path,
                        separator=separator,
                        encoding=enc,
                    )
            except Exception as exc:
                last_error = exc

    raise RuntimeError(f"Unable to read CSV file: {csv_path}. Last error: {last_error}")


def analyze_dataframe(df: pd.DataFrame, head_rows: int = 5) -> dict:
    numeric_df = df.select_dtypes(include="number")

    analysis = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "head": df.head(head_rows),
        "missing_values": df.isna().sum().sort_values(ascending=False),
        "numeric_columns": list(numeric_df.columns),
        "numeric_summary": numeric_df.describe().T if not numeric_df.empty else pd.DataFrame(),
        "correlation": numeric_df.corr() if numeric_df.shape[1] >= 2 else pd.DataFrame(),
    }

    return analysis


def format_analysis_for_terminal(result: CsvReadResult, analysis: dict) -> str:
    lines = []

    lines.append("CSV ANALYZER REPORT")
    lines.append("=" * 60)
    lines.append(f"File: {result.path}")
    lines.append(f"Detected separator: {repr(result.separator)}")
    lines.append(f"Encoding: {result.encoding}")
    lines.append(f"Rows: {analysis['rows']}")
    lines.append(f"Columns: {analysis['columns']}")
    lines.append("")

    lines.append("Columns:")
    for col in analysis["column_names"]:
        lines.append(f"- {col} ({analysis['dtypes'][col]})")
    lines.append("")

    lines.append("Missing values:")
    missing = analysis["missing_values"]
    if missing.empty:
        lines.append("No columns found.")
    else:
        for col, value in missing.items():
            lines.append(f"- {col}: {int(value)}")
    lines.append("")

    lines.append("Numeric summary:")
    numeric_summary = analysis["numeric_summary"]
    if numeric_summary.empty:
        lines.append("No numeric columns available.")
    else:
        lines.append(numeric_summary.to_string())
    lines.append("")

    lines.append("Correlation matrix:")
    correlation = analysis["correlation"]
    if correlation.empty:
        lines.append("Not enough numeric columns for correlation.")
    else:
        lines.append(correlation.to_string())
    lines.append("")

    lines.append("Head:")
    lines.append(analysis["head"].to_string(index=False))
    lines.append("")

    return "\n".join(lines)
