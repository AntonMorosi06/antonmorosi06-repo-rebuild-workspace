from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import math
import random

import pygame

from .config import WORLD_HEIGHT, WORLD_WIDTH
from .dna import DNA
from .food import Food


def safe_normalize(vector: pygame.Vector2) -> pygame.Vector2:
    if vector.length_squared() <= 0.00001:
        return pygame.Vector2(0.0, 0.0)
    return vector.normalize()


@dataclass
class Creature:
    position: pygame.Vector2
    dna: DNA
    predator: bool = False
    energy: float = 120.0
    age: float = 0.0
    generation: int = 1
    radius: float = 5.0
    velocity: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0.0, 0.0))
    alive: bool = True
    last_reproduction_age: float = 0.0
    trail: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.predator:
            self.energy = max(self.energy, 170.0)
            self.radius = 7.0
        else:
            self.radius = 5.0
        if self.velocity.length_squared() == 0:
            angle = random.uniform(0.0, math.tau)
            self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.dna.speed

    def distance_to(self, other_position: pygame.Vector2) -> float:
        return self.position.distance_to(other_position)

    def daylight_factor(self, day_phase: float) -> float:
        daylight = 0.5 + 0.5 * math.sin(day_phase * math.tau)
        if self.dna.nocturnality > 0.5:
            return 0.72 + (1.0 - daylight) * 0.42
        return 0.72 + daylight * 0.42

    def season_energy_factor(self, season: str) -> float:
        if season == "spring":
            return 0.92
        if season == "summer":
            return 1.00
        if season == "autumn":
            return 1.08
        if season == "winter":
            return 1.22
        return 1.0

    def update(
        self,
        foods: list[Food],
        nearby_creatures: list["Creature"],
        day_phase: float,
        season: str,
    ) -> Optional["Creature"]:
        if not self.alive:
            return None

        self.age += 1.0

        metabolic_cost = 0.022 * self.dna.metabolism * self.season_energy_factor(season)
        movement_cost = 0.010 * self.velocity.length() * self.dna.metabolism
        self.energy -= metabolic_cost + movement_cost

        if self.age > self.dna.longevity or self.energy <= 0.0:
            self.alive = False
            return None

        steering = pygame.Vector2(0.0, 0.0)
        vision = self.dna.vision * self.daylight_factor(day_phase)

        if self.predator:
            steering += self.seek_prey(nearby_creatures, vision) * (1.8 + self.dna.aggression)
            steering += self.avoid_other_predators(nearby_creatures, vision * 0.55) * 0.45
        else:
            steering += self.seek_food(foods, vision) * 1.55
            steering += self.avoid_predators(nearby_creatures, vision) * 2.35
            steering += self.social_alignment(nearby_creatures, vision * 0.65) * self.dna.sociability

        steering += self.border_avoidance() * 1.8
        steering += pygame.Vector2(random.uniform(-0.06, 0.06), random.uniform(-0.06, 0.06))

        if steering.length_squared() > 0.0001:
            steering = safe_normalize(steering) * 0.16

        self.velocity += steering
        max_speed = self.dna.speed * (1.08 if self.predator else 1.0)
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

        self.position += self.velocity
        self.position.x = max(2.0, min(WORLD_WIDTH - 2.0, self.position.x))
        self.position.y = max(2.0, min(WORLD_HEIGHT - 2.0, self.position.y))

        self.trail.append((int(self.position.x), int(self.position.y)))
        if len(self.trail) > 22:
            self.trail.pop(0)

        if not self.predator:
            self.eat_food(foods)
        else:
            self.hunt(nearby_creatures)

        return self.try_reproduce()

    def seek_food(self, foods: list[Food], vision: float) -> pygame.Vector2:
        nearest = None
        nearest_distance = float("inf")

        for food in foods:
            distance = self.distance_to(food.position)
            if distance < vision and distance < nearest_distance:
                nearest = food
                nearest_distance = distance

        if nearest is None:
            return pygame.Vector2(0.0, 0.0)

        return safe_normalize(nearest.position - self.position)

    def eat_food(self, foods: list[Food]) -> None:
        for food in list(foods):
            if self.distance_to(food.position) <= self.radius + food.radius + 2.0:
                self.energy += food.energy
                foods.remove(food)
                break

    def seek_prey(self, creatures: list["Creature"], vision: float) -> pygame.Vector2:
        nearest = None
        nearest_distance = float("inf")

        for creature in creatures:
            if creature is self or creature.predator or not creature.alive:
                continue
            distance = self.distance_to(creature.position)
            if distance < vision and distance < nearest_distance:
                nearest = creature
                nearest_distance = distance

        if nearest is None:
            return pygame.Vector2(0.0, 0.0)

        return safe_normalize(nearest.position - self.position)

    def hunt(self, creatures: list["Creature"]) -> None:
        for creature in creatures:
            if creature is self or creature.predator or not creature.alive:
                continue
            if self.distance_to(creature.position) <= self.radius + creature.radius + 2.0:
                creature.alive = False
                self.energy += 95.0
                break

    def avoid_predators(self, creatures: list["Creature"], vision: float) -> pygame.Vector2:
        away = pygame.Vector2(0.0, 0.0)

        for creature in creatures:
            if creature is self or not creature.predator or not creature.alive:
                continue
            distance = self.distance_to(creature.position)
            if 0.1 < distance < vision:
                away += safe_normalize(self.position - creature.position) * (vision / distance)

        return away

    def avoid_other_predators(self, creatures: list["Creature"], vision: float) -> pygame.Vector2:
        away = pygame.Vector2(0.0, 0.0)

        for creature in creatures:
            if creature is self or not creature.predator or not creature.alive:
                continue
            distance = self.distance_to(creature.position)
            if 0.1 < distance < vision:
                away += safe_normalize(self.position - creature.position) * (1.0 / distance)

        return away

    def social_alignment(self, creatures: list["Creature"], vision: float) -> pygame.Vector2:
        center = pygame.Vector2(0.0, 0.0)
        count = 0

        for creature in creatures:
            if creature is self or creature.predator or not creature.alive:
                continue
            distance = self.distance_to(creature.position)
            if 0.1 < distance < vision:
                center += creature.position
                count += 1

        if count == 0:
            return pygame.Vector2(0.0, 0.0)

        center /= count
        return safe_normalize(center - self.position)

    def border_avoidance(self) -> pygame.Vector2:
        margin = 55
        force = pygame.Vector2(0.0, 0.0)

        if self.position.x < margin:
            force.x += 1.0
        elif self.position.x > WORLD_WIDTH - margin:
            force.x -= 1.0

        if self.position.y < margin:
            force.y += 1.0
        elif self.position.y > WORLD_HEIGHT - margin:
            force.y -= 1.0

        return force

    def try_reproduce(self) -> Optional["Creature"]:
        min_energy = 210.0 if not self.predator else 260.0
        cooldown = 220.0 if not self.predator else 380.0
        probability = 0.0035 * self.dna.fertility
        if self.predator:
            probability *= 0.55

        if self.energy < min_energy:
            return None
        if self.age - self.last_reproduction_age < cooldown:
            return None
        if random.random() > probability:
            return None

        self.energy *= 0.58
        self.last_reproduction_age = self.age

        child_dna = self.dna.mutate(rate=0.10, strength=0.07)
        offset = pygame.Vector2(random.uniform(-12.0, 12.0), random.uniform(-12.0, 12.0))
        child_position = self.position + offset
        child_position.x = max(5.0, min(WORLD_WIDTH - 5.0, child_position.x))
        child_position.y = max(5.0, min(WORLD_HEIGHT - 5.0, child_position.y))

        return Creature(
            position=child_position,
            dna=child_dna,
            predator=self.predator,
            energy=self.energy * 0.45,
            generation=self.generation + 1,
        )

    def draw(self, surface: pygame.Surface, show_trails: bool = True) -> None:
        color = self.dna.color(predator=self.predator)

        if show_trails and len(self.trail) > 2:
            for index in range(1, len(self.trail)):
                factor = index / len(self.trail)
                trail_color = tuple(max(0, int(channel * factor)) for channel in color)
                pygame.draw.line(surface, trail_color, self.trail[index - 1], self.trail[index], 1)

        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), int(self.radius))
        outline = (255, 230, 230) if self.predator else (225, 245, 255)
        pygame.draw.circle(surface, outline, (int(self.position.x), int(self.position.y)), int(self.radius + 2), 1)

        if self.predator:
            direction = safe_normalize(self.velocity)
            nose = self.position + direction * (self.radius + 5)
            pygame.draw.line(surface, outline, self.position, nose, 2)
