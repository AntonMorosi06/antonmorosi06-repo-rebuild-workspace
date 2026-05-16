from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorldConfig:
    width: int = 1100
    height: int = 720
    initial_agents: int = 90
    initial_food: int = 220
    food_spawn_rate: float = 0.35
    food_energy: float = 32.0
    max_agents: int = 420
    max_food: int = 650
    trail_length: int = 32
    reproduction_energy_fraction: float = 0.48


PRESETS = {
    "balanced": WorldConfig(
        initial_agents=90,
        initial_food=220,
        food_spawn_rate=0.35,
        food_energy=32.0,
        max_agents=420,
        max_food=650,
    ),
    "scarce": WorldConfig(
        initial_agents=110,
        initial_food=120,
        food_spawn_rate=0.18,
        food_energy=28.0,
        max_agents=360,
        max_food=420,
    ),
    "abundant": WorldConfig(
        initial_agents=70,
        initial_food=360,
        food_spawn_rate=0.62,
        food_energy=36.0,
        max_agents=560,
        max_food=850,
    ),
    "high_mutation": WorldConfig(
        initial_agents=100,
        initial_food=230,
        food_spawn_rate=0.38,
        food_energy=32.0,
        max_agents=460,
        max_food=700,
    ),
    "drift": WorldConfig(
        initial_agents=80,
        initial_food=260,
        food_spawn_rate=0.44,
        food_energy=30.0,
        max_agents=430,
        max_food=700,
    ),
}
