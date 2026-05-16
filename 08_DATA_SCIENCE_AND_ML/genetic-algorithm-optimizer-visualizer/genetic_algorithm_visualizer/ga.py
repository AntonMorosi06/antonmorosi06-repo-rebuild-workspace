from __future__ import annotations

from dataclasses import dataclass, field
import random

from .genome import Individual, clamp_genome
from .landscapes import Landscape, get_landscape
from .metrics import best_individual, diversity, mean_fitness


@dataclass
class GAConfig:
    population_size: int = 110
    mutation_rate: float = 0.16
    mutation_sigma: float = 0.42
    crossover_rate: float = 0.82
    tournament_size: int = 4
    elite_count: int = 3


@dataclass
class GAHistoryEntry:
    generation: int
    best_fitness: float
    mean_fitness: float
    diversity: float
    best_x: float
    best_y: float


@dataclass
class GeneticAlgorithm:
    landscape_name: str = "sphere"
    config: GAConfig = field(default_factory=GAConfig)
    seed: int | None = 42
    population: list[Individual] = field(default_factory=list)
    generation: int = 0
    history: list[GAHistoryEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.landscape = get_landscape(self.landscape_name)
        self.reset()

    def reset(self) -> None:
        self.population = [self.random_individual() for _ in range(self.config.population_size)]
        self.generation = 0
        self.history = []
        self.evaluate_population()
        self.record_history()

    def set_landscape(self, name: str) -> None:
        self.landscape_name = name
        self.landscape = get_landscape(name)
        self.reset()

    def random_individual(self) -> Individual:
        low, high = self.landscape.bounds
        return Individual(
            genome=[
                self.rng.uniform(low, high),
                self.rng.uniform(low, high),
            ]
        )

    def evaluate_population(self) -> None:
        for individual in self.population:
            individual.fitness = self.landscape.fitness(individual.genome)

    def tournament_select(self) -> Individual:
        candidates = self.rng.sample(self.population, k=min(self.config.tournament_size, len(self.population)))
        return best_individual(candidates).copy()

    def crossover(self, parent_a: Individual, parent_b: Individual) -> tuple[Individual, Individual]:
        if self.rng.random() > self.config.crossover_rate:
            return parent_a.copy(), parent_b.copy()

        alpha = self.rng.uniform(-0.25, 1.25)
        child_a_genome = [
            alpha * a + (1.0 - alpha) * b
            for a, b in zip(parent_a.genome, parent_b.genome)
        ]
        child_b_genome = [
            alpha * b + (1.0 - alpha) * a
            for a, b in zip(parent_a.genome, parent_b.genome)
        ]

        return Individual(child_a_genome), Individual(child_b_genome)

    def mutate(self, individual: Individual) -> Individual:
        genome = individual.genome[:]

        for index in range(len(genome)):
            if self.rng.random() < self.config.mutation_rate:
                genome[index] += self.rng.gauss(0.0, self.config.mutation_sigma)

        genome = clamp_genome(genome, self.landscape.bounds)
        return Individual(genome=genome)

    def step(self) -> None:
        self.evaluate_population()

        sorted_population = sorted(
            self.population,
            key=lambda individual: individual.fitness if individual.fitness is not None else float("-inf"),
            reverse=True,
        )

        new_population = [individual.copy() for individual in sorted_population[: self.config.elite_count]]

        while len(new_population) < self.config.population_size:
            parent_a = self.tournament_select()
            parent_b = self.tournament_select()
            child_a, child_b = self.crossover(parent_a, parent_b)

            new_population.append(self.mutate(child_a))
            if len(new_population) < self.config.population_size:
                new_population.append(self.mutate(child_b))

        for individual in new_population:
            individual.age += 1

        self.population = new_population
        self.generation += 1
        self.evaluate_population()
        self.record_history()

    def record_history(self) -> None:
        best = best_individual(self.population)
        self.history.append(
            GAHistoryEntry(
                generation=self.generation,
                best_fitness=best.fitness or 0.0,
                mean_fitness=mean_fitness(self.population),
                diversity=diversity(self.population),
                best_x=best.x,
                best_y=best.y,
            )
        )

        if len(self.history) > 240:
            self.history.pop(0)

    def best(self) -> Individual:
        return best_individual(self.population)

    def summary(self) -> dict[str, object]:
        best = self.best()
        return {
            "landscape": self.landscape_name,
            "generation": self.generation,
            "population_size": len(self.population),
            "best_fitness": best.fitness or 0.0,
            "best_x": best.x,
            "best_y": best.y,
            "mean_fitness": mean_fitness(self.population),
            "diversity": diversity(self.population),
            "mutation_rate": self.config.mutation_rate,
            "crossover_rate": self.config.crossover_rate,
            "elite_count": self.config.elite_count,
        }
