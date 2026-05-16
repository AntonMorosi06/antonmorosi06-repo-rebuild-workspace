from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import random

import pygame

from .dna import DNA
from .obstacle import RectObstacle
from .rocket import Rocket


@dataclass
class GenerationStats:
    generation: int
    best_fitness: float
    average_fitness: float
    completed_count: int
    crashed_count: int
    best_distance: float


class Population:
    def __init__(
        self,
        size: int,
        lifespan: int,
        max_force: float,
        start_position: Tuple[float, float],
        mutation_rate: float,
    ) -> None:
        if size < 2:
            raise ValueError("population size must be at least 2")
        if lifespan < 1:
            raise ValueError("lifespan must be at least 1")

        self.size = size
        self.lifespan = lifespan
        self.max_force = max_force
        self.start_position = start_position
        self.mutation_rate = mutation_rate
        self.generation = 1
        self.rockets: List[Rocket] = [
            Rocket(DNA.random(lifespan=lifespan, max_force=max_force), start_position)
            for _ in range(size)
        ]
        self.best_dna = self.rockets[0].dna.copy()
        self.last_stats = GenerationStats(
            generation=1,
            best_fitness=0.0,
            average_fitness=0.0,
            completed_count=0,
            crashed_count=0,
            best_distance=float("inf"),
        )

    def update(
        self,
        step: int,
        target: pygame.Vector2,
        target_radius: float,
        obstacles: List[RectObstacle],
        bounds: pygame.Rect,
    ) -> None:
        for rocket in self.rockets:
            rocket.update(
                step=step,
                target=target,
                target_radius=target_radius,
                obstacles=obstacles,
                bounds=bounds,
            )

    def evaluate(self, target: pygame.Vector2) -> GenerationStats:
        fitness_values = []
        for rocket in self.rockets:
            fitness_values.append(rocket.calculate_fitness(target, self.lifespan))

        best = max(self.rockets, key=lambda rocket: rocket.fitness)
        self.best_dna = best.dna.copy()

        completed_count = sum(1 for rocket in self.rockets if rocket.completed)
        crashed_count = sum(1 for rocket in self.rockets if rocket.crashed)
        best_distance = min(rocket.closest_distance for rocket in self.rockets)

        stats = GenerationStats(
            generation=self.generation,
            best_fitness=max(fitness_values),
            average_fitness=sum(fitness_values) / len(fitness_values),
            completed_count=completed_count,
            crashed_count=crashed_count,
            best_distance=best_distance,
        )
        self.last_stats = stats
        return stats

    def tournament_parent(self, tournament_size: int = 5) -> Rocket:
        candidates = random.sample(self.rockets, k=min(tournament_size, len(self.rockets)))
        return max(candidates, key=lambda rocket: rocket.fitness)

    def evolve(self) -> None:
        new_rockets: List[Rocket] = []

        elite = Rocket(self.best_dna.copy(), self.start_position, color=(120, 255, 170))
        new_rockets.append(elite)

        while len(new_rockets) < self.size:
            parent_a = self.tournament_parent()
            parent_b = self.tournament_parent()
            child_dna = parent_a.dna.crossover(parent_b.dna).mutate(self.mutation_rate)
            new_rockets.append(Rocket(child_dna, self.start_position))

        self.rockets = new_rockets
        self.generation += 1

    def reset(self) -> None:
        self.generation = 1
        self.rockets = [
            Rocket(DNA.random(lifespan=self.lifespan, max_force=self.max_force), self.start_position)
            for _ in range(self.size)
        ]
        self.best_dna = self.rockets[0].dna.copy()
        self.last_stats = GenerationStats(
            generation=1,
            best_fitness=0.0,
            average_fitness=0.0,
            completed_count=0,
            crashed_count=0,
            best_distance=float("inf"),
        )

    def draw(self, surface: pygame.Surface) -> None:
        for rocket in self.rockets:
            rocket.draw(surface)
