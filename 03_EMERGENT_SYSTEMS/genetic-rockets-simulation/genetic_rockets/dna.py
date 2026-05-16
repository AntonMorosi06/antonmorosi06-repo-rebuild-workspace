from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import math
import random


Vector = Tuple[float, float]


@dataclass
class DNA:
    genes: List[Vector]
    max_force: float

    @property
    def lifespan(self) -> int:
        return len(self.genes)

    @staticmethod
    def random_gene(max_force: float) -> Vector:
        angle = random.uniform(0.0, math.tau)
        magnitude = random.uniform(0.15 * max_force, max_force)
        return (math.cos(angle) * magnitude, math.sin(angle) * magnitude)

    @classmethod
    def random(cls, lifespan: int, max_force: float) -> "DNA":
        if lifespan < 1:
            raise ValueError("lifespan must be at least 1")
        if max_force <= 0:
            raise ValueError("max_force must be positive")
        genes = [cls.random_gene(max_force) for _ in range(lifespan)]
        return cls(genes=genes, max_force=max_force)

    def copy(self) -> "DNA":
        return DNA(genes=list(self.genes), max_force=self.max_force)

    def crossover(self, other: "DNA") -> "DNA":
        if self.lifespan != other.lifespan:
            raise ValueError("DNA crossover requires equal lifespan")
        if self.lifespan == 1:
            return DNA(genes=[random.choice([self.genes[0], other.genes[0]])], max_force=self.max_force)

        midpoint = random.randint(1, self.lifespan - 1)
        child_genes = self.genes[:midpoint] + other.genes[midpoint:]
        return DNA(genes=child_genes, max_force=self.max_force)

    def mutate(self, mutation_rate: float) -> "DNA":
        if mutation_rate < 0:
            raise ValueError("mutation_rate cannot be negative")
        if mutation_rate > 1:
            raise ValueError("mutation_rate cannot be greater than 1")

        mutated = []
        for gene in self.genes:
            if random.random() < mutation_rate:
                mutated.append(self.random_gene(self.max_force))
            else:
                mutated.append(gene)

        return DNA(genes=mutated, max_force=self.max_force)
