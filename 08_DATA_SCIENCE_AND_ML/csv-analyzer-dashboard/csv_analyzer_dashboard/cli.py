from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from .analyzer import analyze_csv
from .report import compact_summary, write_json_report, write_markdown_report


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV Analyzer Dashboard CLI.")
    parser.add_argument("--input", required=True, help="Input CSV file.")
    parser.add_argument("--json", help="Optional JSON report output path.")
    parser.add_argument("--markdown", help="Optional Markdown report output path.")
    parser.add_argument("--print-summary", action="store_true", help="Print compact analysis summary.")
    parser.add_argument("--web-sample", action="store_true", help="Also copy JSON output to web/data/sample_report.json.")
    args = parser.parse_args()

    analysis = analyze_csv(args.input)

    if args.print_summary:
        print(compact_summary(analysis))

    if args.json:
        write_json_report(analysis, args.json)
        print(f"[OK] JSON report written: {args.json}")

        if args.web_sample:
            web_path = Path(__file__).resolve().parents[1] / "web" / "data" / "sample_report.json"
            web_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(args.json, web_path)
            print(f"[OK] Web sample report updated: {web_path}")

    if args.markdown:
        write_markdown_report(analysis, args.markdown)
        print(f"[OK] Markdown report written: {args.markdown}")


if __name__ == "__main__":
    main()
