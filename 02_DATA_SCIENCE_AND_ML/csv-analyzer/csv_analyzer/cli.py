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
