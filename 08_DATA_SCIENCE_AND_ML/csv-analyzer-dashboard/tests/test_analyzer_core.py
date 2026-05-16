from csv_analyzer_dashboard.analyzer import analyze_rows
from csv_analyzer_dashboard.inference import infer_type, parse_bool, parse_float, parse_int
from csv_analyzer_dashboard.statistics import numeric_summary, pearson_correlation
from csv_analyzer_dashboard.report import render_markdown_report


def test_type_inference_numeric_boolean_date_and_categorical():
    assert infer_type(["1", "2", "3", ""]) == "integer"
    assert infer_type(["1.2", "2.5", "3.7"]) == "float"
    assert infer_type(["true", "false", "yes", "no"]) == "boolean"
    assert infer_type(["2026-01-01", "2026-01-02"]) == "date"
    assert infer_type(["north", "south", "east"]) == "categorical"


def test_parse_helpers():
    assert parse_int("12") == 12
    assert parse_int("12.5") is None
    assert parse_float("12.5") == 12.5
    assert parse_bool("yes") is True
    assert parse_bool("no") is False


def test_numeric_summary():
    summary = numeric_summary([1, 2, 3, 4, 5])

    assert summary["count"] == 5
    assert summary["min"] == 1
    assert summary["max"] == 5
    assert summary["mean"] == 3
    assert summary["median"] == 3


def test_pearson_correlation_positive():
    value = pearson_correlation([1, 2, 3, 4], [2, 4, 6, 8])

    assert abs(value - 1.0) < 1e-9


def test_analyze_rows_profiles_columns():
    rows = [
        {"region": "North", "units": "10", "revenue": "100.0", "returned": "false"},
        {"region": "South", "units": "20", "revenue": "210.0", "returned": "false"},
        {"region": "North", "units": "", "revenue": "", "returned": "true"},
    ]

    analysis = analyze_rows(rows, source="test")

    assert analysis.row_count == 3
    assert analysis.column_count == 4

    profiles = {column.name: column for column in analysis.columns}
    assert profiles["region"].inferred_type == "categorical"
    assert profiles["units"].inferred_type == "integer"
    assert profiles["revenue"].inferred_type == "float"
    assert profiles["returned"].inferred_type == "boolean"
    assert profiles["units"].missing_count == 1


def test_markdown_report_contains_sections():
    rows = [
        {"a": "1", "b": "2"},
        {"a": "2", "b": "4"},
        {"a": "3", "b": "6"},
    ]
    analysis = analyze_rows(rows, source="test")
    markdown = render_markdown_report(analysis)

    assert "# CSV Analysis Report" in markdown
    assert "## Column profiles" in markdown
    assert "## Correlations" in markdown
