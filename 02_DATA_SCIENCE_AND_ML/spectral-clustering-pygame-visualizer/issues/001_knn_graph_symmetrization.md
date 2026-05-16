# Issue 001 - KNN graph symmetrization

## Goal

Ensure that the k-nearest-neighbor affinity graph is suitable for spectral clustering.

## Current implementation

The visualizer builds a directed KNN-style affinity matrix and then symmetrizes it with the maximum between the matrix and its transpose.

## Reason

A directed KNN graph can create asymmetric relationships. Spectral clustering with a standard normalized Laplacian expects an undirected affinity structure.

## Acceptance criteria

The affinity matrix should be square.

The diagonal should remain zero.

The matrix should be symmetric.

The graph should remain readable in the visualizer.

The graph edge count should appear in the dashboard.
