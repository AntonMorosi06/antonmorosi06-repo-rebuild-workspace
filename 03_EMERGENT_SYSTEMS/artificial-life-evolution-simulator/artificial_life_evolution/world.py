from __future__ import annotations

from dataclasses import dataclass
import random

import pygame

from .config import (
    INITIAL_FOOD,
    INITIAL_PREDATORS,
    INITIAL_PREY,
    MAX_FOOD,
    MAX_PREDATORS,
    MAX_PREY,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)
from .creature import Creature
from .dna import DNA
from .food import Food
from .spatial_hash import SpatialHash


SEASONS = ["spring", "summer", "autumn", "winter"]


@dataclass
class WorldStats:
    prey_count: int
    predator_count: int
    food_count: int
    avg_prey_speed: float
    avg_prey_vision: float
    avg_predator_speed: float
    avg_generation: float
    births: int
    deaths: int
    season: str
    day_phase: float
    event_name: str


class World:
    def __init__(self) -> None:
        self.creatures: list[Creature] = []
        self.foods: list[Food] = []
        self.creature_hash = SpatialHash(cell_size=82)
        self.tick = 0
        self.births = 0
        self.deaths = 0
        self.event_name = "stable ecosystem"
        self.event_timer = 0
        self.reset()

    def reset(self) -> None:
        self.creatures.clear()
        self.foods.clear()
        self.tick = 0
        self.births = 0
        self.deaths = 0
        self.event_name = "stable ecosystem"
        self.event_timer = 0

        for _ in range(INITIAL_FOOD):
            self.add_food_random()

        for _ in range(INITIAL_PREY):
            self.add_creature_random(predator=False)

        for _ in range(INITIAL_PREDATORS):
            self.add_creature_random(predator=True)

    @property
    def day_phase(self) -> float:
        return (self.tick % 1800) / 1800.0

    @property
    def season(self) -> str:
        return SEASONS[(self.tick // 3600) % len(SEASONS)]

    def add_food_random(self) -> None:
        if len(self.foods) >= MAX_FOOD:
            return
        x = random.uniform(20.0, WORLD_WIDTH - 20.0)
        y = random.uniform(20.0, WORLD_HEIGHT - 20.0)
        self.foods.append(Food.at(x, y))

    def add_food_at(self, x: float, y: float) -> None:
        if len(self.foods) < MAX_FOOD:
            self.foods.append(Food.at(x, y))

    def add_creature_random(self, predator: bool = False) -> None:
        x = random.uniform(25.0, WORLD_WIDTH - 25.0)
        y = random.uniform(25.0, WORLD_HEIGHT - 25.0)
        dna = DNA.random_predator() if predator else DNA.random_prey()
        energy = 190.0 if predator else 135.0
        self.creatures.append(Creature(position=pygame.Vector2(x, y), dna=dna, predator=predator, energy=energy))

    def add_creature_at(self, x: float, y: float, predator: bool = False) -> None:
        prey_count, predator_count = self.population_counts()
        if predator and predator_count >= MAX_PREDATORS:
            return
        if not predator and prey_count >= MAX_PREY:
            return
        dna = DNA.random_predator() if predator else DNA.random_prey()
        energy = 190.0 if predator else 135.0
        self.creatures.append(Creature(position=pygame.Vector2(x, y), dna=dna, predator=predator, energy=energy))

    def rebuild_hash(self) -> None:
        self.creature_hash.clear()
        for creature in self.creatures:
            if creature.alive:
                self.creature_hash.insert(creature, creature.position.x, creature.position.y)

    def population_counts(self) -> tuple[int, int]:
        prey_count = sum(1 for creature in self.creatures if creature.alive and not creature.predator)
        predator_count = sum(1 for creature in self.creatures if creature.alive and creature.predator)
        return prey_count, predator_count

    def season_food_probability(self) -> float:
        if self.season == "spring":
            return 0.80
        if self.season == "summer":
            return 0.55
        if self.season == "autumn":
            return 0.40
        if self.season == "winter":
            return 0.18
        return 0.40

    def trigger_random_event(self) -> None:
        event = random.choice(["food bloom", "cold snap", "predator pressure", "quiet recovery"])

        if event == "food bloom":
            for _ in range(85):
                self.add_food_random()
            self.event_name = "food bloom"

        elif event == "cold snap":
            for creature in self.creatures:
                creature.energy *= 0.82
            self.event_name = "cold snap"

        elif event == "predator pressure":
            for _ in range(4):
                self.add_creature_random(predator=True)
            self.event_name = "predator pressure"

        else:
            for _ in range(35):
                self.add_food_random()
            for creature in self.creatures:
                if not creature.predator:
                    creature.energy += 8.0
            self.event_name = "quiet recovery"

        self.event_timer = 420

    def update(self) -> None:
        self.tick += 1

        if self.event_timer > 0:
            self.event_timer -= 1
        else:
            self.event_name = "stable ecosystem"

        if random.random() < self.season_food_probability() and len(self.foods) < MAX_FOOD:
            self.add_food_random()

        if random.random() < 0.0009:
            self.trigger_random_event()

        self.rebuild_hash()

        newborns: list[Creature] = []
        alive_before = sum(1 for creature in self.creatures if creature.alive)

        for creature in list(self.creatures):
            if not creature.alive:
                continue

            nearby = self.creature_hash.nearby(creature.position.x, creature.position.y, creature.dna.vision)
            nearby_creatures = [item for item in nearby if isinstance(item, Creature)]

            child = creature.update(
                foods=self.foods,
                nearby_creatures=nearby_creatures,
                day_phase=self.day_phase,
                season=self.season,
            )

            if child is not None:
                prey_count, predator_count = self.population_counts()
                if child.predator and predator_count + sum(1 for c in newborns if c.predator) < MAX_PREDATORS:
                    newborns.append(child)
                elif not child.predator and prey_count + sum(1 for c in newborns if not c.predator) < MAX_PREY:
                    newborns.append(child)

        if newborns:
            self.creatures.extend(newborns)
            self.births += len(newborns)

        self.creatures = [creature for creature in self.creatures if creature.alive]
        alive_after = len(self.creatures)
        self.deaths += max(0, alive_before - alive_after)

        prey_count, predator_count = self.population_counts()
        if prey_count < 24:
            for _ in range(6):
                self.add_creature_random(predator=False)
        if predator_count < 3 and prey_count > 65:
            self.add_creature_random(predator=True)

    def stats(self) -> WorldStats:
        prey = [creature for creature in self.creatures if creature.alive and not creature.predator]
        predators = [creature for creature in self.creatures if creature.alive and creature.predator]
        all_alive = [creature for creature in self.creatures if creature.alive]

        def average(items: list[float]) -> float:
            return sum(items) / len(items) if items else 0.0

        return WorldStats(
            prey_count=len(prey),
            predator_count=len(predators),
            food_count=len(self.foods),
            avg_prey_speed=average([creature.dna.speed for creature in prey]),
            avg_prey_vision=average([creature.dna.vision for creature in prey]),
            avg_predator_speed=average([creature.dna.speed for creature in predators]),
            avg_generation=average([creature.generation for creature in all_alive]),
            births=self.births,
            deaths=self.deaths,
            season=self.season,
            day_phase=self.day_phase,
            event_name=self.event_name,
        )

    def draw(self, surface: pygame.Surface, show_trails: bool = True) -> None:
        for food in self.foods:
            food.draw(surface)

        for creature in self.creatures:
            creature.draw(surface, show_trails=show_trails)
