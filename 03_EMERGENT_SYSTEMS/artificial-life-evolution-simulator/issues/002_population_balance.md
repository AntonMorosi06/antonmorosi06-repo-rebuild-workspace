# Issue 002 - Population balance

## Goal

Improve long-term ecosystem stability.

## Current behavior

The simulation includes food regeneration, prey reproduction, predator hunting, predator reproduction and fallback respawn rules when prey or predator populations become too low.

## Open questions

The prey population may still explode under food-rich conditions.

The predator population may collapse if prey becomes too sparse.

Winter and cold snap parameters may be too harsh or too weak depending on random events.

## Acceptance criteria

The ecosystem should usually remain active for several minutes without total collapse.

Population statistics should make imbalance visible.

Documentation should clearly state that this is an educational model, not a biological claim.
