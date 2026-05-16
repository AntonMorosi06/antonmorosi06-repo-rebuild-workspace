# Issue 001 - Dirty-state recomputation and performance

## Goal

Keep the DBSCAN visualization responsive by recalculating clusters only when the point set or algorithm parameters change.

## Current implementation

The application uses an AppState.dirty flag. The flag becomes true when the user adds points, clears points, regenerates points, adds noise, changes eps, changes min_samples, or presses Space. The next frame recalculates DBSCAN and sets the flag back to false.

## Acceptance criteria

The visualizer should not recompute DBSCAN continuously when the user is only observing the screen.

Changing eps or min_samples should update the clustering result immediately.

Adding or clearing points should update the clustering result immediately.

The dashboard should show whether the current state is dirty or clean.
