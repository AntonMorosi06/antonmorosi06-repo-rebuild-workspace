from __future__ import annotations

from pathlib import Path

from .core import CsvReadResult


def save_markdown_report(result: CsvReadResult, analysis: dict, output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report_path = output_path / "csv_analysis_report.md"

    lines = []
    lines.append("# CSV Analysis Report")
    lines.append("")
    lines.append(f"File: `{result.path}`")
    lines.append("")
    lines.append(f"Detected separator: `{repr(result.separator)}`")
    lines.append("")
    lines.append(f"Encoding: `{result.encoding}`")
    lines.append("")
    lines.append(f"Rows: {analysis['rows']}")
    lines.append("")
    lines.append(f"Columns: {analysis['columns']}")
    lines.append("")
    lines.append("## Columns")
    lines.append("")

    for col in analysis["column_names"]:
        lines.append(f"- `{col}`: `{analysis['dtypes'][col]}`")

    lines.append("")
    lines.append("## Missing values")
    lines.append("")

    for col, value in analysis["missing_values"].items():
        lines.append(f"- `{col}`: {int(value)}")

    lines.append("")
    lines.append("## Numeric summary")
    lines.append("")

    numeric_summary = analysis["numeric_summary"]
    if numeric_summary.empty:
        lines.append("No numeric columns available.")
    else:
        lines.append(numeric_summary.to_markdown())

    lines.append("")
    lines.append("## Correlation matrix")
    lines.append("")

    correlation = analysis["correlation"]
    if correlation.empty:
        lines.append("Not enough numeric columns for correlation.")
    else:
        lines.append(correlation.to_markdown())

    lines.append("")
    lines.append("## Head")
    lines.append("")
    lines.append(analysis["head"].to_markdown(index=False))

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path
