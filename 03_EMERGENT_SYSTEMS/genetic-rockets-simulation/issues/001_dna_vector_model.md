# Issue 001 - DNA vector model

## Goal

Keep the DNA representation clear, robust and easy to explain.

## Current implementation

Each DNA object contains a list of two-dimensional force vectors. Each rocket applies one vector per simulation step.

## Acceptance criteria

DNA length should match the simulation lifespan.

Crossover should preserve DNA length.

Mutation should preserve DNA length.

Mutation should replace only a controlled percentage of genes according to mutation_rate.

The README and algorithm notes should explain the DNA model clearly.
