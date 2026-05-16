from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

from .entities import Agent, Food
from .genome import Genome
from .metrics import population_metrics
from .vector import Vec2, clamp, wrap_position
from .world import PRESETS, WorldConfig


@dataclass
class LifeSimulation:
    preset_name: str = "balanced"
    seed: int | None = 42
    config: WorldConfig = field(init=False)
    agents: list[Agent] = field(default_factory=list)
    food: list[Food] = field(default_factory=list)
    tick: int = 0
    paused: bool = False
    lineage_counter: int = 0
    history: list[dict[str, float | int | str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.set_preset(self.preset_name)

    def set_preset(self, name: str) -> None:
        if name not in PRESETS:
            raise ValueError(f"unknown preset: {name}")
        self.preset_name = name
        self.config = PRESETS[name]
        self.reset()

    def reset(self) -> None:
        self.agents.clear()
        self.food.clear()
        self.tick = 0
        self.lineage_counter = 0
        self.history.clear()

        for _ in range(self.config.initial_food):
            self.spawn_food()

        for _ in range(self.config.initial_agents):
            self.spawn_agent()

        if self.preset_name == "high_mutation":
            for agent in self.agents:
                genome = agent.genome
                agent.genome = Genome(
                    speed=genome.speed,
                    perception=genome.perception,
                    metabolism=genome.metabolism,
                    size=genome.size,
                    fertility=genome.fertility,
                    mutation_intensity=clamp(genome.mutation_intensity * 1.9, 0.10, 0.35),
                )

        self.record_history()

    def random_position(self) -> Vec2:
        return Vec2(
            self.rng.uniform(0.0, self.config.width),
            self.rng.uniform(0.0, self.config.height),
        )

    def random_velocity(self, speed: float) -> Vec2:
        angle = self.rng.uniform(0.0, math.tau)
        return Vec2(math.cos(angle) * speed, math.sin(angle) * speed)

    def spawn_food(self, position: Vec2 | None = None) -> Food:
        item = Food(
            position=position or self.random_position(),
            energy=self.config.food_energy * self.rng.uniform(0.7, 1.25),
            radius=self.rng.uniform(2.3, 4.4),
        )
        self.food.append(item)
        return item

    def spawn_agent(self, position: Vec2 | None = None, genome: Genome | None = None, generation: int = 0, lineage_id: int | None = None) -> Agent:
        genome = genome or Genome.random(self.rng)
        lineage_id = self.lineage_counter if lineage_id is None else lineage_id
        if lineage_id == self.lineage_counter:
            self.lineage_counter += 1

        agent = Agent(
            position=position or self.random_position(),
            velocity=self.random_velocity(genome.speed),
            genome=genome,
            energy=self.rng.uniform(70.0, 120.0),
            generation=generation,
            lineage_id=lineage_id,
        )
        self.agents.append(agent)
        return agent

    def nearest_food(self, agent: Agent) -> Food | None:
        best: Food | None = None
        best_distance = float("inf")

        for item in self.food:
            distance = agent.position.distance_to(item.position)
            if distance < best_distance and distance <= agent.genome.perception:
                best = item
                best_distance = distance

        return best

    def update_agent(self, agent: Agent) -> list[Agent]:
        if not agent.alive:
            return []

        target = self.nearest_food(agent)

        if target is not None:
            desired = (target.position - agent.position).normalized() * agent.genome.speed
            steering = (desired - agent.velocity) * 0.18
            agent.velocity = (agent.velocity + steering).clamp_length(agent.genome.speed)
        else:
            wander_angle = self.rng.uniform(-0.45, 0.45)
            cos_a = math.cos(wander_angle)
            sin_a = math.sin(wander_angle)
            rotated = Vec2(
                agent.velocity.x * cos_a - agent.velocity.y * sin_a,
                agent.velocity.x * sin_a + agent.velocity.y * cos_a,
            )
            if rotated.length() < 0.1:
                rotated = self.random_velocity(agent.genome.speed)
            agent.velocity = rotated.clamp_length(agent.genome.speed)

        agent.position = wrap_position(agent.position + agent.velocity, self.config.width, self.config.height)
        agent.age += 1
        agent.energy -= agent.genome.energy_cost_per_step()
        agent.remember(self.config.trail_length)

        self.handle_food_collision(agent)

        children: list[Agent] = []
        if self.can_reproduce(agent):
            child = self.reproduce(agent)
            if child is not None:
                children.append(child)

        if agent.energy <= 0.0 or agent.age > agent.max_age:
            agent.alive = False

        return children

    def handle_food_collision(self, agent: Agent) -> None:
        eaten_index = None

        for index, item in enumerate(self.food):
            distance = agent.position.distance_to(item.position)
            if distance <= agent.radius + item.radius:
                eaten_index = index
                agent.energy += item.energy
                agent.eaten += 1
                break

        if eaten_index is not None:
            self.food.pop(eaten_index)

    def can_reproduce(self, agent: Agent) -> bool:
        if len(self.agents) >= self.config.max_agents:
            return False
        if agent.energy < agent.genome.reproduction_threshold():
            return False
        if agent.age < 45:
            return False
        probability = 0.010 + agent.genome.fertility * 0.020
        return self.rng.random() < probability

    def reproduce(self, parent: Agent) -> Agent | None:
        parent.energy *= self.config.reproduction_energy_fraction
        child_genome = parent.genome.mutated(self.rng)
        offset = self.random_velocity(12.0)
        position = wrap_position(parent.position + offset, self.config.width, self.config.height)
        child = self.spawn_agent(
            position=position,
            genome=child_genome,
            generation=parent.generation + 1,
            lineage_id=parent.lineage_id,
        )
        child.energy = parent.energy * 0.78
        parent.children += 1
        return child

    def spawn_food_by_rate(self) -> None:
        attempts = int(self.config.food_spawn_rate)
        fractional = self.config.food_spawn_rate - attempts

        for _ in range(attempts):
            if len(self.food) < self.config.max_food:
                self.spawn_food()

        if self.rng.random() < fractional and len(self.food) < self.config.max_food:
            self.spawn_food()

    def step(self) -> None:
        if self.paused:
            return

        self.tick += 1

        new_children: list[Agent] = []
        for agent in list(self.agents):
            new_children.extend(self.update_agent(agent))

        self.agents = [agent for agent in self.agents if agent.alive]
        self.spawn_food_by_rate()

        if len(self.agents) == 0:
            for _ in range(max(12, self.config.initial_agents // 4)):
                self.spawn_agent()

        if self.tick % 20 == 0:
            self.record_history()

    def record_history(self) -> None:
        self.history.append(self.metrics())
        if len(self.history) > 360:
            self.history.pop(0)

    def metrics(self) -> dict[str, float | int | str]:
        return population_metrics(self.agents, len(self.food), self.tick, self.preset_name)

    def add_food_burst(self, count: int = 80) -> None:
        for _ in range(count):
            if len(self.food) < self.config.max_food:
                self.spawn_food()

    def add_agent_burst(self, count: int = 20) -> None:
        for _ in range(count):
            if len(self.agents) < self.config.max_agents:
                self.spawn_agent()
