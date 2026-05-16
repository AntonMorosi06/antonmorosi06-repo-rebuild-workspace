from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .vector import Vec2


@dataclass
class Particle:
    position: Vec2
    velocity: Vec2
    mass: float = 1.0
    radius: float = 2.0
    energy: float = 0.0
    age: float = 0.0
    absorbed: bool = False
    trail: list[Vec2] = field(default_factory=list)

    def remember(self, trail_length: int) -> None:
        self.trail.append(self.position.copy())
        if len(self.trail) > trail_length:
            self.trail.pop(0)


@dataclass
class Shockwave:
    position: Vec2
    radius: float = 8.0
    speed: float = 3.8
    alpha: float = 1.0
    age: float = 0.0

    def update(self, dt: float) -> None:
        self.age += dt
        self.radius += self.speed * dt * 60.0
        self.alpha = max(0.0, self.alpha - dt * 1.35)

    @property
    def alive(self) -> bool:
        return self.alpha > 0.01


@dataclass
class BlackHole:
    position: Vec2
    mass: float
    event_horizon_radius: float
    absorption_radius: float
    accretion_radius: float
