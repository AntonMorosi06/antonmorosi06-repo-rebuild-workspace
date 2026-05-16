from __future__ import annotations

from .genome import Individual


def best_individual(population: list[Individual]) -> Individual:
    if not population:
        raise ValueError("population cannot be empty")
    return max(population, key=lambda individual: individual.fitness if individual.fitness is not None else float("-inf"))


def mean_fitness(population: list[Individual]) -> float:
    if not population:
        return 0.0
    values = [individual.fitness or 0.0 for individual in population]
    return sum(values) / len(values)


def diversity(population: list[Individual]) -> float:
    if len(population) < 2:
        return 0.0

    total = 0.0
    count = 0

    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            total += population[i].distance_to(population[j])
            count += 1

    return total / max(1, count)


def population_summary(population: list[Individual]) -> dict[str, float]:
    best = best_individual(population)
    return {
        "best_fitness": best.fitness or 0.0,
        "best_x": best.x,
        "best_y": best.y,
        "mean_fitness": mean_fitness(population),
        "diversity": diversity(population),
    }
