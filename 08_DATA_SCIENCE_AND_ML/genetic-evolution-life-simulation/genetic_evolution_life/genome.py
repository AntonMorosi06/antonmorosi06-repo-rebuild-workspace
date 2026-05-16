from __future__ import annotations

from dataclasses import dataclass
import random

from .vector import clamp


@dataclass(frozen=True)
class Genome:
    speed: float
    perception: float
    metabolism: float
    size: float
    fertility: float
    mutation_intensity: float

    @staticmethod
    def random(rng: random.Random) -> "Genome":
        return Genome(
            speed=rng.uniform(1.2, 3.6),
            perception=rng.uniform(45.0, 145.0),
            metabolism=rng.uniform(0.010, 0.040),
            size=rng.uniform(3.0, 6.2),
            fertility=rng.uniform(0.45, 0.78),
            mutation_intensity=rng.uniform(0.05, 0.18),
        )

    def mutated(self, rng: random.Random) -> "Genome":
        intensity = self.mutation_intensity

        return Genome(
            speed=clamp(self.speed + rng.gauss(0.0, 0.32 * intensity * 5.0), 0.65, 5.2),
            perception=clamp(self.perception + rng.gauss(0.0, 18.0 * intensity * 3.0), 18.0, 220.0),
            metabolism=clamp(self.metabolism + rng.gauss(0.0, 0.006 * intensity * 4.0), 0.004, 0.080),
            size=clamp(self.size + rng.gauss(0.0, 0.55 * intensity * 3.0), 2.0, 9.5),
            fertility=clamp(self.fertility + rng.gauss(0.0, 0.055 * intensity * 4.0), 0.20, 0.95),
            mutation_intensity=clamp(self.mutation_intensity + rng.gauss(0.0, 0.025), 0.01, 0.35),
        )

    def energy_cost_per_step(self) -> float:
        speed_cost = self.speed * 0.010
        perception_cost = self.perception * 0.000035
        size_cost = self.size * 0.004
        return self.metabolism + speed_cost + perception_cost + size_cost

    def reproduction_threshold(self) -> float:
        return 70.0 + self.size * 5.0 + self.fertility * 38.0

    def as_dict(self) -> dict[str, float]:
        return {
            "speed": self.speed,
            "perception": self.perception,
            "metabolism": self.metabolism,
            "size": self.size,
            "fertility": self.fertility,
            "mutation_intensity": self.mutation_intensity,
        }
