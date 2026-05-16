# Issue 001 - Shared core engine

## Goal

Keep all Snake variants powered by the same rules engine.

## Current implementation

The core module owns movement, food placement, collision, score and board representation.

## Acceptance criteria

New interfaces should not duplicate game rules.

Core tests should cover movement, direction, food growth and collision.

The README should explain the architecture clearly.
