from pathlib import Path
from datetime import datetime
import subprocess
import textwrap

ROOT = Path.home() / "Desktop" / "ANTONMOROSI06_REPO_REBUILD_WORKSPACE"
TARGET = ROOT / "02_DATA_SCIENCE_AND_ML" / "csv-analyzer"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print("[OK] wrote", path.relative_to(ROOT))

def touch(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

def run(cmd, cwd=None):
    print("[CMD]", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)

for folder in [
    "csv_analyzer",
    "data",
    "reports/generated",
    "docs",
    "demos/screenshots",
    "tests",
    "issues",
    "labels",
    "output"
]:
    path = TARGET / folder
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")

write(
    TARGET / "README.md",
    """
# CSV Analyzer

CSV Analyzer is a cleaned and reconstructed Python data-analysis utility inspired by the original `AntonMorosi2234/CSV_ANALYZER` repository.

This version is not cloned automatically from the old repository. It is rebuilt as a clean, portfolio-ready skeleton based on the repository analysis: command-line CSV analysis, smart separator detection, Pandas summaries, missing-value reports, correlation output, Matplotlib histograms and a small Tkinter GUI.

## Current status

Status: reconstructed functional skeleton.

This repository contains:

- a reusable package in `csv_analyzer/`;
- a command-line interface;
- a Tkinter GUI;
- a sample synthetic dataset in `data/vendite.csv`;
- generated reports folder;
- documentation;
- issue backlog;
- labels.

## What this project does

CSV Analyzer can:

- load CSV files;
- detect common separators;
- display row and column counts;
- list column names;
- show data types;
- show head rows;
- calculate numeric descriptive statistics;
- calculate missing-value counts;
- calculate numeric correlation matrix when possible;
- save a Markdown report;
- generate numeric histograms;
- provide a simple desktop GUI.

## What this project is not

This is not a full business-intelligence platform. It does not replace advanced notebook analysis, ETL systems or production dashboards. It is a compact educational and portfolio tool for exploring CSV files quickly.

## Install

From this folder:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Run CLI

Analyze the demo dataset:

    python -m csv_analyzer --file data/vendite.csv --report --plots

Show help:

    python -m csv_analyzer --help

## Run GUI

    python -m csv_analyzer.gui

## Output

Generated reports and plots go to:

    reports/generated/

Generated outputs are ignored by Git except folder placeholders.

## Portfolio positioning

This project demonstrates Python, Pandas, Matplotlib, CLI design, basic GUI design and clean project packaging. It is useful as a small data-analysis proof-of-work and can later connect conceptually to MicroBot telemetry analytics.
"""
)

write(
    TARGET / "requirements.txt",
    """
pandas
numpy
matplotlib
"""
)

write(
    TARGET / ".gitignore",
    """
.DS_Store
__pycache__/
*.pyc
.venv/
venv/
env/
.pytest_cache/
reports/generated/*
!reports/generated/.gitkeep
output/*
!output/.gitkeep
*.log
"""
)

write(
    TARGET / "csv_analyzer" / "__init__.py",
    """
__version__ = "0.1.0"

from .core import read_csv_smart, analyze_dataframe
"""
)

write(
    TARGET / "csv_analyzer" / "__main__.py",
    """
from .cli import main

if __name__ == "__main__":
    main()
"""
)

write(
    TARGET / "csv_analyzer" / "core.py",
    """
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


COMMON_SEPARATORS = [",", ";", "\\t", "|"]


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

    return "\\n".join(lines)
"""
)

write(
    TARGET / "csv_analyzer" / "reporting.py",
    """
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

    report_path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
    return report_path
"""
)

write(
    TARGET / "csv_analyzer" / "plotting.py",
    """
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def save_histograms(df, output_dir: str | Path) -> list[Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    numeric_df = df.select_dtypes(include="number")
    saved = []

    for column in numeric_df.columns:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(numeric_df[column].dropna(), bins=20)
        ax.set_title(f"Histogram: {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        fig.tight_layout()

        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in column)
        path = output_path / f"histogram_{safe_name}.png"
        fig.savefig(path)
        plt.close(fig)
        saved.append(path)

    return saved
"""
)

write(
    TARGET / "csv_analyzer" / "cli.py",
    """
from __future__ import annotations

import argparse
from pathlib import Path

from .core import read_csv_smart, analyze_dataframe, format_analysis_for_terminal
from .reporting import save_markdown_report
from .plotting import save_histograms


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-analyzer",
        description="Analyze CSV files from the command line.",
    )

    parser.add_argument(
        "--file",
        default="data/vendite.csv",
        help="Path to the CSV file. Defaults to data/vendite.csv.",
    )

    parser.add_argument(
        "--sep",
        default=None,
        help="Optional CSV separator. If omitted, common separators are tested.",
    )

    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Preferred file encoding. Fallback encodings are attempted automatically.",
    )

    parser.add_argument(
        "--head",
        type=int,
        default=5,
        help="Number of rows to show in the preview.",
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Save a Markdown report.",
    )

    parser.add_argument(
        "--plots",
        action="store_true",
        help="Save histograms for numeric columns.",
    )

    parser.add_argument(
        "--output",
        default="reports/generated",
        help="Output folder for generated reports and plots.",
    )

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = read_csv_smart(args.file, sep=args.sep, encoding=args.encoding)
    analysis = analyze_dataframe(result.dataframe, head_rows=args.head)

    print(format_analysis_for_terminal(result, analysis))

    output_dir = Path(args.output)

    if args.report:
        report_path = save_markdown_report(result, analysis, output_dir)
        print(f"[OK] Report saved: {report_path}")

    if args.plots:
        plot_paths = save_histograms(result.dataframe, output_dir)
        if plot_paths:
            for path in plot_paths:
                print(f"[OK] Plot saved: {path}")
        else:
            print("[INFO] No numeric columns available for plotting.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""
)

write(
    TARGET / "csv_analyzer" / "gui.py",
    """
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .core import read_csv_smart, analyze_dataframe, format_analysis_for_terminal
from .reporting import save_markdown_report
from .plotting import save_histograms


class CsvAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CSV Analyzer")
        self.geometry("1000x700")
        self.minsize(900, 600)

        self.current_result = None
        self.current_analysis = None

        self._build_ui()

    def _build_ui(self):
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Open CSV", command=self.open_csv).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Save Report", command=self.save_report).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Save Histograms", command=self.save_plots).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(toolbar, text="Clear", command=self.clear).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(toolbar, textvariable=self.status_var).pack(side=tk.RIGHT)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.summary_text = tk.Text(notebook, wrap=tk.NONE)
        self.summary_text.configure(font=("Menlo", 12))

        xscroll = ttk.Scrollbar(notebook, orient=tk.HORIZONTAL, command=self.summary_text.xview)
        yscroll = ttk.Scrollbar(notebook, orient=tk.VERTICAL, command=self.summary_text.yview)
        self.summary_text.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        frame = ttk.Frame(notebook)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.summary_text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        notebook.add(frame, text="Summary")

    def open_csv(self):
        path = filedialog.askopenfilename(
            title="Open CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            result = read_csv_smart(path)
            analysis = analyze_dataframe(result.dataframe)
            self.current_result = result
            self.current_analysis = analysis

            text = format_analysis_for_terminal(result, analysis)
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, text)

            self.status_var.set(f"Loaded: {Path(path).name}")
        except Exception as exc:
            messagebox.showerror("CSV Analyzer Error", str(exc))
            self.status_var.set("Error")

    def save_report(self):
        if not self.current_result or not self.current_analysis:
            messagebox.showinfo("CSV Analyzer", "Open a CSV file first.")
            return

        output_dir = Path("reports/generated")
        path = save_markdown_report(self.current_result, self.current_analysis, output_dir)
        messagebox.showinfo("CSV Analyzer", f"Report saved:\\n{path}")
        self.status_var.set("Report saved")

    def save_plots(self):
        if not self.current_result:
            messagebox.showinfo("CSV Analyzer", "Open a CSV file first.")
            return

        output_dir = Path("reports/generated")
        paths = save_histograms(self.current_result.dataframe, output_dir)

        if paths:
            messagebox.showinfo("CSV Analyzer", f"Saved {len(paths)} histogram(s).")
        else:
            messagebox.showinfo("CSV Analyzer", "No numeric columns available.")

        self.status_var.set("Plots saved")

    def clear(self):
        self.current_result = None
        self.current_analysis = None
        self.summary_text.delete("1.0", tk.END)
        self.status_var.set("Ready")


def main():
    app = CsvAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
"""
)

write(
    TARGET / "data" / "vendite.csv",
    """
id_cliente,nome,eta,sesso,prodotto,quantita,prezzo_unitario,data_acquisto
1,Marco,28,M,Telefono,1,699.00,2026-01-10
2,Giulia,34,F,Computer,1,1299.00,2026-01-12
3,Luca,22,M,Tablet,2,399.00,2026-01-13
4,Sara,41,F,Smartwatch,1,249.00,2026-01-15
5,Andrea,31,M,Auricolari,3,89.00,2026-01-16
6,Francesca,27,F,Telefono,1,799.00,2026-01-18
7,Matteo,45,M,Computer,2,1199.00,2026-01-20
8,Elena,38,F,Tablet,1,449.00,2026-01-21
9,Paolo,29,M,Smartwatch,2,229.00,2026-01-22
10,Chiara,33,F,Auricolari,1,99.00,2026-01-23
"""
)

write(
    TARGET / "docs" / "usage.md",
    """
# Usage

## CLI

From the project folder:

    python -m csv_analyzer --file data/vendite.csv

Generate report and plots:

    python -m csv_analyzer --file data/vendite.csv --report --plots

Use a custom separator:

    python -m csv_analyzer --file data/my_file.csv --sep ";"

## GUI

Run:

    python -m csv_analyzer.gui

Then choose a CSV file from the file dialog.

## Output

Reports and plots are written to:

    reports/generated/
"""
)

write(
    TARGET / "docs" / "known_limitations.md",
    """
# Known Limitations

- This is a compact educational CSV analyzer, not a full BI platform.
- Very large CSV files may be slow or memory-heavy because Pandas loads the file into memory.
- Separator detection is based on common separators, not a full dialect inference system.
- The GUI is intentionally simple.
- Plots are basic histograms for numeric columns.
- No database connection is implemented.
- No automatic data cleaning is performed beyond reading and summary generation.
"""
)

write(
    TARGET / "docs" / "portfolio_summary.md",
    """
# Portfolio Summary

CSV Analyzer demonstrates a small but complete Python data-analysis utility.

It shows:

- project packaging;
- command-line design;
- Pandas data loading;
- separator detection;
- missing-value analysis;
- numeric statistics;
- correlation matrix generation;
- Matplotlib output;
- Tkinter GUI basics;
- report generation.

This project can be presented as a compact data-analysis proof-of-work and as a foundation for future MicroBot telemetry analytics.
"""
)

write(
    TARGET / "issues" / "ISSUES_BACKLOG.md",
    """
# Issues Backlog for csv-analyzer

## Issue 01: Validate CLI execution

Goal:
Confirm the command-line analyzer works on the demo dataset.

Tasks:
- [ ] Create virtual environment.
- [ ] Install requirements.
- [ ] Run CLI on data/vendite.csv.
- [ ] Save terminal output.

Acceptance criteria:
- CLI prints row count, column count, missing values and numeric summary.

## Issue 02: Validate report generation

Goal:
Confirm Markdown report generation.

Tasks:
- [ ] Run with --report.
- [ ] Confirm reports/generated/csv_analysis_report.md exists.
- [ ] Inspect generated report.

Acceptance criteria:
- Report is readable and contains major sections.

## Issue 03: Validate histogram generation

Goal:
Confirm numeric histograms are generated.

Tasks:
- [ ] Run with --plots.
- [ ] Confirm PNG files exist.
- [ ] Inspect at least one plot.

Acceptance criteria:
- Histogram PNG files are generated for numeric columns.

## Issue 04: Validate GUI

Goal:
Confirm Tkinter GUI opens and analyzes a CSV.

Tasks:
- [ ] Run python -m csv_analyzer.gui.
- [ ] Open data/vendite.csv.
- [ ] Save screenshot.

Acceptance criteria:
- GUI displays analysis summary.

## Issue 05: Add tests

Goal:
Add tests for smart CSV reading and analysis output.

Tasks:
- [ ] Add pytest.
- [ ] Test comma-separated file.
- [ ] Test semicolon-separated file.
- [ ] Test missing values.

Acceptance criteria:
- Tests pass locally.

## Issue 06: Add MicroBot telemetry example

Goal:
Prepare future connection to MicroBot telemetry analytics.

Tasks:
- [ ] Add synthetic MicroBot telemetry CSV.
- [ ] Analyze voltage, current, temperature and state.
- [ ] Add docs/microbot_telemetry_relevance.md.

Acceptance criteria:
- The project demonstrates indirect MicroBot relevance.
"""
)

write(
    TARGET / "labels" / "labels.yml",
    """
- name: python
  color: "3572A5"
  description: "Python code"
- name: data-analysis
  color: "0e8a16"
  description: "CSV, Pandas and analysis features"
- name: gui
  color: "1d76db"
  description: "Tkinter GUI"
- name: cli
  color: "5319e7"
  description: "Command-line interface"
- name: plotting
  color: "fbca04"
  description: "Matplotlib plots"
- name: documentation
  color: "0366d6"
  description: "README and docs"
- name: testing
  color: "fbca04"
  description: "Tests and validation"
- name: microbot-alignment
  color: "0052cc"
  description: "Relation to MicroBot telemetry analytics"
- name: portfolio-ready
  color: "0e8a16"
  description: "Required before public presentation"
"""
)

write(
    TARGET / "CHANGELOG.md",
    f"""
# Changelog

## Reconstructed skeleton batch - {now}

- Rebuilt CSV Analyzer as a clean functional skeleton.
- Added Python package structure.
- Added smart CSV loading.
- Added CLI.
- Added Tkinter GUI.
- Added Markdown report generation.
- Added histogram plotting.
- Added sample synthetic sales dataset.
- Added usage docs.
- Added known limitations.
- Added portfolio summary.
- Added issues and labels.
"""
)

population_log = ROOT / "05_POPULATION_LOG.md"
old_log = population_log.read_text(encoding="utf-8") if population_log.exists() else "# Population Log\n\n"

write(
    population_log,
    old_log + f"""

## {now}

Rebuilt csv-analyzer as a reconstructed functional skeleton.

Decision:
Do not clone AntonMorosi2234 repositories automatically.

Created:

- csv_analyzer package
- CLI
- GUI
- sample data
- report generation
- plotting
- docs
- issues
- labels
"""
)

run(["git", "add", "-A"], cwd=ROOT)

commit = run(["git", "commit", "-m", "Rebuild CSV Analyzer as functional skeleton"], cwd=ROOT)

if commit.returncode == 0:
    print("[OK] Commit created.")
else:
    print("[WARN] Commit not created. Maybe no changes.")
    print(commit.stdout)
    print(commit.stderr)

push = run(["git", "push", "origin", "main"], cwd=ROOT)

if push.returncode == 0:
    print("[OK] Pushed to origin main.")
else:
    print("[WARN] Push failed.")
    print(push.stdout)
    print(push.stderr)

print("[OK] CSV Analyzer skeleton rebuild complete.")
