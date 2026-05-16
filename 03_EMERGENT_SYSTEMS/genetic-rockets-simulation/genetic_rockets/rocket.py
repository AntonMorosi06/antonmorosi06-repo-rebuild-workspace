from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import math

import pygame

from .dna import DNA
from .obstacle import RectObstacle


Color = Tuple[int, int, int]


@dataclass
class Rocket:
    dna: DNA
    start_position: Tuple[float, float]
    color: Color = (120, 200, 255)

    def __post_init__(self) -> None:
        self.position = pygame.Vector2(self.start_position)
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.completed = False
        self.crashed = False
        self.closest_distance = float("inf")
        self.finish_step = None
        self.fitness = 0.0

    def reset_runtime_state(self) -> None:
        self.position = pygame.Vector2(self.start_position)
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.completed = False
        self.crashed = False
        self.closest_distance = float("inf")
        self.finish_step = None
        self.fitness = 0.0

    def apply_force(self, force: pygame.Vector2) -> None:
        if not self.completed and not self.crashed:
            self.acceleration += force

    def update(
        self,
        step: int,
        target: pygame.Vector2,
        target_radius: float,
        obstacles: List[RectObstacle],
        bounds: pygame.Rect,
    ) -> None:
        if self.completed or self.crashed:
            return

        distance = self.position.distance_to(target)
        self.closest_distance = min(self.closest_distance, distance)

        if distance <= target_radius:
            self.completed = True
            self.finish_step = step
            self.position = pygame.Vector2(target)
            return

        if not bounds.collidepoint(int(self.position.x), int(self.position.y)):
            self.crashed = True
            return

        for obstacle in obstacles:
            if obstacle.contains_point(self.position):
                self.crashed = True
                return

        if step < self.dna.lifespan:
            gene = self.dna.genes[step]
            self.apply_force(pygame.Vector2(gene[0], gene[1]))

        self.velocity += self.acceleration
        if self.velocity.length() > 5.2:
            self.velocity.scale_to_length(5.2)
        self.position += self.velocity
        self.acceleration *= 0.0

    def calculate_fitness(self, target: pygame.Vector2, lifespan: int) -> float:
        distance_score = 1.0 / ((self.closest_distance + 1.0) ** 2)
        fitness = distance_score * 100000.0

        if self.completed:
            step = self.finish_step if self.finish_step is not None else lifespan
            speed_bonus = max(1.0, (lifespan - step) / max(1.0, lifespan) * 4.0)
            fitness *= 8.0 + speed_bonus

        if self.crashed:
            fitness *= 0.25

        self.fitness = max(0.000001, fitness)
        return self.fitness

    def draw(self, surface: pygame.Surface) -> None:
        angle = 0.0
        if self.velocity.length_squared() > 0.001:
            angle = math.atan2(self.velocity.y, self.velocity.x)

        nose = pygame.Vector2(12, 0).rotate_rad(angle)
        left = pygame.Vector2(-8, -5).rotate_rad(angle)
        right = pygame.Vector2(-8, 5).rotate_rad(angle)

        points = [
            self.position + nose,
            self.position + left,
            self.position + right,
        ]

        if self.completed:
            color = (120, 255, 170)
        elif self.crashed:
            color = (120, 120, 135)
        else:
            color = self.color

        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (245, 248, 255), points, width=1)
