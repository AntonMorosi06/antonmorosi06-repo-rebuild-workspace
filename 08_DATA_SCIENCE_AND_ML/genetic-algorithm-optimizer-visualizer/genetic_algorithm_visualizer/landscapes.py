from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable


FitnessFunction = Callable[[list[float]], float]


@dataclass(frozen=True)
class Landscape:
    name: str
    description: str
    bounds: tuple[float, float]
    optimum_hint: tuple[float, float]
    fitness: FitnessFunction


def sphere_fitness(genome: list[float]) -> float:
    x, y = genome
    return -(x * x + y * y)


def rastrigin_fitness(genome: list[float]) -> float:
    x, y = genome
    value = 20.0 + (x * x - 10.0 * math.cos(2.0 * math.pi * x)) + (y * y - 10.0 * math.cos(2.0 * math.pi * y))
    return -value


def himmelblau_fitness(genome: list[float]) -> float:
    x, y = genome
    value = (x * x + y - 11.0) ** 2 + (x + y * y - 7.0) ** 2
    return -value


def ridge_fitness(genome: list[float]) -> float:
    x, y = genome
    ridge = -((y - math.sin(1.8 * x)) ** 2) * 3.5
    center_bonus = -0.08 * (x * x + y * y)
    return ridge + center_bonus


def multi_peak_fitness(genome: list[float]) -> float:
    x, y = genome
    peaks = [
        (2.2, 1.7, 2.8, 0.62),
        (-2.1, -1.4, 2.2, 0.72),
        (0.1, 2.6, 1.8, 0.58),
        (1.4, -2.4, 1.4, 0.50),
    ]

    value = 0.0
    for cx, cy, height, width in peaks:
        dist_sq = (x - cx) ** 2 + (y - cy) ** 2
        value += height * math.exp(-dist_sq / (2.0 * width * width))

    value -= 0.04 * (x * x + y * y)
    return value


LANDSCAPES = {
    "sphere": Landscape(
        name="sphere",
        description="Simple convex bowl with one global optimum at the center.",
        bounds=(-5.0, 5.0),
        optimum_hint=(0.0, 0.0),
        fitness=sphere_fitness,
    ),
    "rastrigin": Landscape(
        name="rastrigin",
        description="Multi-modal benchmark with many local optima.",
        bounds=(-5.12, 5.12),
        optimum_hint=(0.0, 0.0),
        fitness=rastrigin_fitness,
    ),
    "himmelblau": Landscape(
        name="himmelblau",
        description="Classic function with multiple equivalent minima converted into fitness peaks.",
        bounds=(-6.0, 6.0),
        optimum_hint=(3.0, 2.0),
        fitness=himmelblau_fitness,
    ),
    "ridge": Landscape(
        name="ridge",
        description="Sinusoidal ridge that rewards following a curved valley.",
        bounds=(-5.0, 5.0),
        optimum_hint=(0.0, 0.0),
        fitness=ridge_fitness,
    ),
    "multi_peak": Landscape(
        name="multi_peak",
        description="Several Gaussian-like peaks with local optima.",
        bounds=(-5.0, 5.0),
        optimum_hint=(2.2, 1.7),
        fitness=multi_peak_fitness,
    ),
}


def landscape_names() -> list[str]:
    return sorted(LANDSCAPES.keys())


def get_landscape(name: str) -> Landscape:
    if name not in LANDSCAPES:
        raise ValueError(f"unknown landscape: {name}")
    return LANDSCAPES[name]
