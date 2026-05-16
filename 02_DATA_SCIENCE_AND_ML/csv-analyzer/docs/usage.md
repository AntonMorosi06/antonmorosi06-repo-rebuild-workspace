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
