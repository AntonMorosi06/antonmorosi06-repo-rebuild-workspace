# Issue 001 - Spatial hash performance

## Goal

Keep nearby-neighbor queries efficient as the creature population grows.

## Current implementation

The world uses a simple spatial hash with fixed-size cells. Each alive creature is inserted into the hash by position. During update, a creature queries nearby cells using its vision radius.

## Acceptance criteria

The spatial hash should be rebuilt once per world update.

Creatures should query only nearby cells, not the entire population.

The implementation should remain readable and easy to document.

Future work can add profiling and adjustable cell size.
