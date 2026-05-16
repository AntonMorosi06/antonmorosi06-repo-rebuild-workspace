# Genetic algorithm notes

A genetic algorithm is an optimization method inspired by biological evolution. It starts from a population of candidate solutions, evaluates them with a fitness function, selects better candidates, combines them through crossover and introduces variation through mutation.

In this simulation, each rocket is a candidate solution. The rocket does not decide dynamically where to go. Instead, it follows a DNA sequence. Each DNA gene is a small two-dimensional force vector. During a generation, the rocket applies one force vector per frame.

At the end of the generation, the simulation evaluates all rockets. Rockets that get closer to the target receive a better score. Rockets that reach the target receive a large completion bonus. Rockets that reach the target earlier receive an additional speed bonus. Rockets that crash into an obstacle or leave the screen receive a penalty.

The next generation is produced using tournament selection. A few rockets are sampled from the previous generation and the one with the best fitness becomes a parent. Two parents produce a child through crossover. Mutation randomly replaces some genes with new vectors, allowing the population to explore trajectories that were not present before.

The important lesson is that no single rocket understands the full problem. The visible behavior emerges from repeated evaluation and reproduction across generations.
