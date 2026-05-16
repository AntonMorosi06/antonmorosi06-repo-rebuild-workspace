from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class Individual:
    genome: list[float]
    fitness: float | None = None
    age: int = 0

    def copy(self) -> "Individual":
        return Individual(genome=self.genome[:], fitness=self.fitness, age=self.age)

    @property
    def x(self) -> float:
        return self.genome[0]

    @property
    def y(self) -> float:
        return self.genome[1]

    def distance_to(self, other: "Individual") -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.genome, other.genome)))


def clamp_genome(genome: list[float], bounds: tuple[float, float]) -> list[float]:
    low, high = bounds
    return [max(low, min(high, value)) for value in genome]
