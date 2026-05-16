# Analyzer model

The analyzer is organized as a small pipeline.

The loader reads a CSV file using the standard library csv module.

The inference module determines whether each column is empty, boolean, integer, float, date-like or categorical.

The analyzer builds a profile for every column.

The statistics module computes numeric summaries, top categorical values and Pearson correlations.

The report module exports JSON and Markdown.

The web dashboard reads an exported JSON file and renders it in a browser.
