# Controls and usage

Run the CLI with:

python3 main.py --input data/sample_sales.csv --print-summary

Export JSON:

python3 main.py --input data/sample_sales.csv --json reports/analysis.json

Export Markdown:

python3 main.py --input data/sample_sales.csv --markdown reports/analysis.md

Update the dashboard sample report:

python3 main.py --input data/sample_sales.csv --json reports/sample_report.json --web-sample

Run the dashboard:

cd web
python3 -m http.server 8080
