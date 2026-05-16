# CSV Analyzer Dashboard

This repository is a clean reconstructed skeleton of the old CSV Analyzer project. It is not a clone of the original repository. It is a rebuilt, documented and improved version prepared inside the AntonMorosi06 repository rebuild workspace.

The project implements a dependency-light CSV analysis toolkit using Python standard library modules. It can load CSV files, infer column types, detect missing values, compute numeric statistics, summarize categorical columns, calculate simple Pearson correlations, generate JSON reports and generate Markdown reports.

The repository also includes a small static web dashboard that can display an exported analysis JSON file. The analysis engine and the visual dashboard are separated so that the core can be tested from the command line without requiring a browser.

## Current status

Status: reconstructed skeleton  
Original clone: intentionally not used  
Project type: data analysis / CSV profiling  
Core engine: pure Python and testable without external data science libraries  
Dashboard: static HTML/CSS/JS  
External dependency: pytest only for tests  
Portfolio readiness: prepared baseline  
GitHub Pages readiness: prepared baseline for static dashboard  

## Features

The analyzer supports CSV loading, dialect sniffing, type inference, missing-value counting, numeric descriptive statistics, categorical top values, boolean detection, date-like detection, unique counts, column profiles, dataset summary, Pearson correlations and report export.

The CLI can analyze a CSV file and write both JSON and Markdown reports.

The web dashboard can load a prepared JSON report and display dataset metrics, column profiles and correlations in a browser.

## Repository layout

README.md  
CHANGELOG.md  
requirements.txt  
.gitignore  
main.py  
csv_analyzer_dashboard/loader.py  
csv_analyzer_dashboard/inference.py  
csv_analyzer_dashboard/statistics.py  
csv_analyzer_dashboard/analyzer.py  
csv_analyzer_dashboard/report.py  
csv_analyzer_dashboard/cli.py  
web/index.html  
web/style.css  
web/src/app.js  
web/data/sample_report.json  
data/sample_sales.csv  
docs/analyzer_model.md  
docs/type_inference_notes.md  
docs/controls_and_usage.md  
docs/report_format.md  
docs/github_pages_checklist.md  
docs/portfolio_summary.md  
docs/known_limitations.md  
issues/001_csv_import_edge_cases.md  
issues/002_dashboard_upload_mode.md  
issues/003_large_file_streaming.md  
labels/repo_labels.md  
tests/test_analyzer_core.py  

## Quick start

Run the sample analysis:

python3 main.py --input data/sample_sales.csv --print-summary --json reports/sample_report.json --markdown reports/sample_report.md

Run tests:

PYTHONPATH=. python3 -m pytest tests

Open the static dashboard:

cd web
python3 -m http.server 8080

Then open:

http://127.0.0.1:8080

## CLI examples

Analyze a CSV and print a summary:

python3 main.py --input data/sample_sales.csv --print-summary

Export JSON:

python3 main.py --input data/sample_sales.csv --json reports/analysis.json

Export Markdown:

python3 main.py --input data/sample_sales.csv --markdown reports/analysis.md

Export both:

python3 main.py --input data/sample_sales.csv --json reports/analysis.json --markdown reports/analysis.md

## Educational purpose

This project is useful because CSV analysis is one of the most common practical data tasks. Before building machine learning models or dashboards, the analyst must understand columns, missing values, numeric ranges, categories and possible relationships between variables.

The reconstructed version keeps the code readable and inspectable. It does not hide the logic behind pandas or external profiling packages.

## Portfolio value

The strongest portfolio angle is the full small-tool workflow: CSV input, profiling engine, JSON output, Markdown output, tests, documentation and static dashboard. It shows practical data engineering and data analysis habits without overcomplicating the repository.

## Responsible reconstruction note

This is a reconstructed educational baseline. It should be presented as a clean repo rebuild, not as a recovered historical source tree.
