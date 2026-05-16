# Issue 003 - Performance neighbor search

## Goal

Improve performance for larger datasets.

## Current implementation

The region query checks every point against every other point.

## Future improvements

Add grid spatial hash.

Add KD-tree optional backend.

Add benchmark script.

Add performance notes.

## Acceptance criteria

The direct implementation should remain available because it is easier to understand educationally.
