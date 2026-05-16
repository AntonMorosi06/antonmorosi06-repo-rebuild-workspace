from __future__ import annotations

import math
import random

from .point import Point2D


def generate_blobs(seed: int = 42, points_per_blob: int = 80) -> list[Point2D]:
    rng = random.Random(seed)
    centers = [(-2.2, -1.3), (1.9, -1.1), (0.2, 1.9), (2.6, 2.2)]
    points: list[Point2D] = []

    for cx, cy in centers:
        for _ in range(points_per_blob):
            points.append(Point2D(
                x=rng.gauss(cx, 0.38),
                y=rng.gauss(cy, 0.38),
            ))

    for _ in range(26):
        points.append(Point2D(
            x=rng.uniform(-4.0, 4.0),
            y=rng.uniform(-3.3, 3.3),
        ))

    return points


def generate_moons(seed: int = 42, count: int = 260) -> list[Point2D]:
    rng = random.Random(seed)
    points: list[Point2D] = []

    for index in range(count):
        angle = rng.uniform(0.0, math.pi)
        noise_x = rng.gauss(0.0, 0.07)
        noise_y = rng.gauss(0.0, 0.07)

        if index % 2 == 0:
            x = math.cos(angle) * 2.0 + noise_x
            y = math.sin(angle) * 1.25 + noise_y
        else:
            x = 1.0 - math.cos(angle) * 2.0 + noise_x
            y = -math.sin(angle) * 1.25 + 0.72 + noise_y

        points.append(Point2D(x=x, y=y))

    return points


def generate_rings(seed: int = 42, count: int = 300) -> list[Point2D]:
    rng = random.Random(seed)
    points: list[Point2D] = []

    for index in range(count):
        if index % 2 == 0:
            radius = rng.gauss(1.25, 0.06)
        else:
            radius = rng.gauss(2.55, 0.08)

        angle = rng.uniform(0.0, math.tau)
        points.append(Point2D(
            x=math.cos(angle) * radius + rng.gauss(0.0, 0.025),
            y=math.sin(angle) * radius + rng.gauss(0.0, 0.025),
        ))

    return points


def generate_noise(seed: int = 42, count: int = 320) -> list[Point2D]:
    rng = random.Random(seed)
    return [
        Point2D(
            x=rng.uniform(-4.0, 4.0),
            y=rng.uniform(-3.2, 3.2),
        )
        for _ in range(count)
    ]


def generate_mixed(seed: int = 42) -> list[Point2D]:
    rng = random.Random(seed)
    points: list[Point2D] = []

    points.extend(generate_blobs(seed=seed + 1, points_per_blob=42))
    points.extend(generate_rings(seed=seed + 2, count=130))

    for _ in range(42):
        angle = rng.uniform(0.0, math.tau)
        radius = rng.uniform(0.1, 1.2)
        points.append(Point2D(
            x=-2.8 + math.cos(angle) * radius * 0.6,
            y=2.2 + math.sin(angle) * radius * 0.9,
        ))

    return points


DATASET_BUILDERS = {
    "blobs": generate_blobs,
    "moons": generate_moons,
    "rings": generate_rings,
    "noise": generate_noise,
    "mixed": generate_mixed,
}


def generate_dataset(name: str, seed: int = 42) -> list[Point2D]:
    if name not in DATASET_BUILDERS:
        raise ValueError(f"unknown dataset: {name}")
    return DATASET_BUILDERS[name](seed=seed)


def dataset_names() -> list[str]:
    return sorted(DATASET_BUILDERS.keys())
