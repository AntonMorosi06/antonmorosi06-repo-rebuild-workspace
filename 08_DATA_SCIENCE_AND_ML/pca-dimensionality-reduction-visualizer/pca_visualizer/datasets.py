from __future__ import annotations

import math
import random

from .linalg import Matrix


def generate_correlated_cloud(seed: int = 42, count: int = 260) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for _ in range(count):
        base = rng.gauss(0.0, 1.0)
        x = base * 2.2 + rng.gauss(0.0, 0.35)
        y = base * 1.15 + rng.gauss(0.0, 0.42)
        data.append([x, y])

    return data


def generate_ellipse(seed: int = 42, count: int = 280) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []
    angle = math.radians(34)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    for _ in range(count):
        u = rng.gauss(0.0, 2.4)
        v = rng.gauss(0.0, 0.35)
        x = u * cos_a - v * sin_a
        y = u * sin_a + v * cos_a
        data.append([x, y])

    return data


def generate_rotated_clusters(seed: int = 42, count_per_cluster: int = 82) -> Matrix:
    rng = random.Random(seed)
    centers = [(-2.2, -1.0), (1.8, 0.4), (0.2, 2.0)]
    data: Matrix = []

    for cx, cy in centers:
        for _ in range(count_per_cluster):
            u = rng.gauss(0.0, 0.72)
            v = rng.gauss(0.0, 0.24)
            x = cx + u * 0.86 - v * 0.50
            y = cy + u * 0.50 + v * 0.86
            data.append([x, y])

    return data


def generate_3d_ribbon(seed: int = 42, count: int = 320) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for _ in range(count):
        t = rng.uniform(-3.0, 3.0)
        x = t + rng.gauss(0.0, 0.12)
        y = math.sin(t * 1.4) + rng.gauss(0.0, 0.16)
        z = 0.55 * t + 0.35 * math.cos(t * 1.8) + rng.gauss(0.0, 0.14)
        data.append([x, y, z])

    return data


def generate_noisy_line(seed: int = 42, count: int = 260) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for _ in range(count):
        x = rng.uniform(-3.2, 3.2)
        y = 0.72 * x + rng.gauss(0.0, 0.55)
        data.append([x, y])

    return data


DATASET_BUILDERS = {
    "correlated": generate_correlated_cloud,
    "ellipse": generate_ellipse,
    "clusters": generate_rotated_clusters,
    "ribbon3d": generate_3d_ribbon,
    "line": generate_noisy_line,
}


def dataset_names() -> list[str]:
    return sorted(DATASET_BUILDERS.keys())


def generate_dataset(name: str, seed: int = 42) -> Matrix:
    if name not in DATASET_BUILDERS:
        raise ValueError(f"unknown dataset: {name}")
    return DATASET_BUILDERS[name](seed=seed)
