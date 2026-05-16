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
