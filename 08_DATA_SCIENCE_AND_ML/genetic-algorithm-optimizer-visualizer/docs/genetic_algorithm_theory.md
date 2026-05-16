# Genetic algorithm theory

A genetic algorithm is a population-based optimization method inspired by evolution.

Each candidate solution is represented as a genome. In this project the genome is a two-dimensional real-valued vector.

The algorithm evaluates every individual with a fitness function. Higher fitness means a better solution.

Selection chooses individuals that are more likely to reproduce. This baseline uses tournament selection.

Crossover combines two parent genomes to create children. This baseline uses blend crossover.

Mutation randomly perturbs genes to preserve exploration and avoid premature convergence.

Elitism copies the best individuals directly into the next generation so that the best known solutions are not lost.

Across generations, the population tends to move toward high-fitness regions of the landscape.
