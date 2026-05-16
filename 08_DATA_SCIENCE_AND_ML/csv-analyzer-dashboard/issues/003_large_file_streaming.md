# Issue 003 - Large file streaming

## Goal

Improve behavior for larger CSV files.

## Current implementation

The analyzer loads rows into memory.

## Future improvements

Add streaming summary mode.

Add sampled profiling mode.

Add progress output.

Add maximum-row option.

Add memory usage notes.

## Acceptance criteria

The basic full-load implementation should remain available for small and medium files.
