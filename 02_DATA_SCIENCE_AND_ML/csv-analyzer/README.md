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
