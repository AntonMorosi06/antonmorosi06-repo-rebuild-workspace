from __future__ import annotations

from .entities import Agent


def average(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def population_metrics(agents: list[Agent], food_count: int, tick: int, preset: str) -> dict[str, float | int | str]:
    alive = [agent for agent in agents if agent.alive]

    if not alive:
        return {
            "tick": tick,
            "preset": preset,
            "population": 0,
            "food": food_count,
            "average_energy": 0.0,
            "average_speed": 0.0,
            "average_perception": 0.0,
            "average_metabolism": 0.0,
            "average_mutation": 0.0,
            "average_generation": 0.0,
            "total_children": 0,
            "oldest_age": 0,
            "best_fitness_proxy": 0.0,
        }

    return {
        "tick": tick,
        "preset": preset,
        "population": len(alive),
        "food": food_count,
        "average_energy": average([agent.energy for agent in alive]),
        "average_speed": average([agent.genome.speed for agent in alive]),
        "average_perception": average([agent.genome.perception for agent in alive]),
        "average_metabolism": average([agent.genome.metabolism for agent in alive]),
        "average_mutation": average([agent.genome.mutation_intensity for agent in alive]),
        "average_generation": average([agent.generation for agent in alive]),
        "total_children": sum(agent.children for agent in alive),
        "oldest_age": max(agent.age for agent in alive),
        "best_fitness_proxy": max(agent.fitness_proxy() for agent in alive),
    }
