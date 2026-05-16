from __future__ import annotations

import math
import random

from .linalg import Matrix


def generate_moons(seed: int = 42, count: int = 132) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for index in range(count):
        angle = rng.uniform(0.0, math.pi)
        noise_x = rng.gauss(0.0, 0.055)
        noise_y = rng.gauss(0.0, 0.055)

        if index % 2 == 0:
            x = math.cos(angle) * 2.0 + noise_x
            y = math.sin(angle) * 1.15 + noise_y
        else:
            x = 1.0 - math.cos(angle) * 2.0 + noise_x
            y = -math.sin(angle) * 1.15 + 0.62 + noise_y

        data.append([x, y])

    return data


def generate_rings(seed: int = 42, count: int = 132) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for index in range(count):
        radius = rng.gauss(1.15, 0.045) if index % 2 == 0 else rng.gauss(2.45, 0.060)
        angle = rng.uniform(0.0, math.tau)
        data.append([
            math.cos(angle) * radius + rng.gauss(0.0, 0.018),
            math.sin(angle) * radius + rng.gauss(0.0, 0.018),
        ])

    return data


def generate_blobs(seed: int = 42, count_per_blob: int = 44) -> Matrix:
    rng = random.Random(seed)
    centers = [(-2.0, -1.2), (1.8, -1.0), (0.1, 1.8)]
    data: Matrix = []

    for cx, cy in centers:
        for _ in range(count_per_blob):
            data.append([
                rng.gauss(cx, 0.35),
                rng.gauss(cy, 0.35),
            ])

    return data


def generate_bridge(seed: int = 42, count: int = 138) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for _ in range(count // 3):
        data.append([rng.gauss(-2.2, 0.32), rng.gauss(0.0, 0.34)])
        data.append([rng.gauss(2.2, 0.32), rng.gauss(0.0, 0.34)])

    for i in range(count - len(data)):
        t = -1.8 + 3.6 * (i / max(1, count - len(data) - 1))
        data.append([t + rng.gauss(0.0, 0.05), rng.gauss(0.0, 0.09)])

    return data


def generate_islands(seed: int = 42, count: int = 140) -> Matrix:
    rng = random.Random(seed)
    centers = [(-2.7, -1.5), (-1.4, 1.4), (0.6, -0.6), (2.4, 1.2)]
    data: Matrix = []

    while len(data) < count:
        cx, cy = rng.choice(centers)
        data.append([rng.gauss(cx, 0.22), rng.gauss(cy, 0.22)])

    return data


def generate_spiral_arcs(seed: int = 42, count: int = 132) -> Matrix:
    rng = random.Random(seed)
    data: Matrix = []

    for index in range(count):
        arm = index % 2
        t = rng.uniform(0.35, 3.1 * math.pi)
        radius = 0.18 * t
        angle = t + arm * math.pi
        data.append([
            math.cos(angle) * radius + rng.gauss(0.0, 0.045),
            math.sin(angle) * radius + rng.gauss(0.0, 0.045),
        ])

    return data


DATASET_BUILDERS = {
    "moons": generate_moons,
    "rings": generate_rings,
    "blobs": generate_blobs,
    "bridge": generate_bridge,
    "islands": generate_islands,
    "spiral": generate_spiral_arcs,
}


def dataset_names() -> list[str]:
    return sorted(DATASET_BUILDERS.keys())


def generate_dataset(name: str, seed: int = 42) -> Matrix:
    if name not in DATASET_BUILDERS:
        raise ValueError(f"unknown dataset: {name}")
    return DATASET_BUILDERS[name](seed=seed)
