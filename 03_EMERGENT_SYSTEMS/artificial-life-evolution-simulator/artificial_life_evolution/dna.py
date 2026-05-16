from __future__ import annotations

from dataclasses import dataclass
import colorsys
import random


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


@dataclass(frozen=True)
class DNA:
    speed: float
    vision: float
    aggression: float
    sociability: float
    fertility: float
    metabolism: float
    nocturnality: float
    longevity: float
    hue: float

    @classmethod
    def random_prey(cls) -> "DNA":
        return cls(
            speed=random.uniform(1.45, 2.70),
            vision=random.uniform(65.0, 145.0),
            aggression=random.uniform(0.00, 0.25),
            sociability=random.uniform(0.25, 0.95),
            fertility=random.uniform(0.45, 0.95),
            metabolism=random.uniform(0.55, 1.15),
            nocturnality=random.uniform(0.05, 0.55),
            longevity=random.uniform(900.0, 1650.0),
            hue=random.uniform(0.45, 0.66),
        )

    @classmethod
    def random_predator(cls) -> "DNA":
        return cls(
            speed=random.uniform(1.80, 3.10),
            vision=random.uniform(100.0, 190.0),
            aggression=random.uniform(0.65, 1.00),
            sociability=random.uniform(0.05, 0.45),
            fertility=random.uniform(0.15, 0.55),
            metabolism=random.uniform(0.90, 1.55),
            nocturnality=random.uniform(0.25, 0.90),
            longevity=random.uniform(1150.0, 2050.0),
            hue=random.uniform(0.95, 1.00),
        )

    def crossover(self, other: "DNA") -> "DNA":
        return DNA(
            speed=random.choice([self.speed, other.speed]),
            vision=random.choice([self.vision, other.vision]),
            aggression=random.choice([self.aggression, other.aggression]),
            sociability=random.choice([self.sociability, other.sociability]),
            fertility=random.choice([self.fertility, other.fertility]),
            metabolism=random.choice([self.metabolism, other.metabolism]),
            nocturnality=random.choice([self.nocturnality, other.nocturnality]),
            longevity=random.choice([self.longevity, other.longevity]),
            hue=random.choice([self.hue, other.hue]),
        )

    def mutate(self, rate: float = 0.08, strength: float = 0.12) -> "DNA":
        if rate < 0.0 or rate > 1.0:
            raise ValueError("mutation rate must be between 0 and 1")
        if strength < 0.0:
            raise ValueError("mutation strength cannot be negative")

        def maybe(value: float, minimum: float, maximum: float) -> float:
            if random.random() < rate:
                value += random.gauss(0.0, strength * (maximum - minimum))
            return clamp(value, minimum, maximum)

        return DNA(
            speed=maybe(self.speed, 0.80, 3.80),
            vision=maybe(self.vision, 35.0, 230.0),
            aggression=maybe(self.aggression, 0.0, 1.0),
            sociability=maybe(self.sociability, 0.0, 1.0),
            fertility=maybe(self.fertility, 0.0, 1.0),
            metabolism=maybe(self.metabolism, 0.35, 2.10),
            nocturnality=maybe(self.nocturnality, 0.0, 1.0),
            longevity=maybe(self.longevity, 500.0, 2600.0),
            hue=maybe(self.hue, 0.0, 1.0),
        )

    def color(self, predator: bool = False) -> tuple[int, int, int]:
        hue = self.hue % 1.0
        saturation = 0.72 if not predator else 0.82
        value = 0.96 if not predator else 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return (int(r * 255), int(g * 255), int(b * 255))

    def summary(self) -> dict[str, float]:
        return {
            "speed": self.speed,
            "vision": self.vision,
            "aggression": self.aggression,
            "sociability": self.sociability,
            "fertility": self.fertility,
            "metabolism": self.metabolism,
            "nocturnality": self.nocturnality,
            "longevity": self.longevity,
            "hue": self.hue,
        }
