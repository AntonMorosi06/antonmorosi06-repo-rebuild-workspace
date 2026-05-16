from __future__ import annotations

from dataclasses import dataclass, field

from .genome import Genome
from .vector import Vec2


@dataclass
class Food:
    position: Vec2
    energy: float = 30.0
    radius: float = 3.0


@dataclass
class Agent:
    position: Vec2
    velocity: Vec2
    genome: Genome
    energy: float = 90.0
    age: int = 0
    generation: int = 0
    lineage_id: int = 0
    alive: bool = True
    eaten: int = 0
    children: int = 0
    trail: list[Vec2] = field(default_factory=list)

    def remember(self, trail_length: int) -> None:
        self.trail.append(self.position.copy())
        if len(self.trail) > trail_length:
            self.trail.pop(0)

    @property
    def radius(self) -> float:
        return self.genome.size

    @property
    def max_age(self) -> int:
        return int(900 + self.genome.fertility * 420 + self.genome.size * 18)

    def fitness_proxy(self) -> float:
        return self.energy + self.eaten * 10.0 + self.children * 35.0 + self.age * 0.02
