from __future__ import annotations

from typing import Optional

import numpy as np


def make_clustered_points(
    width: int,
    height: int,
    side_panel_width: int,
    seed: Optional[int] = None,
    clusters: int = 4,
    points_per_cluster: int = 55,
    noise_points: int = 35,
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    usable_width = width - side_panel_width - 80
    x_min = 60
    x_max = max(x_min + 20, usable_width)
    y_min = 70
    y_max = height - 70

    centers = []
    for _ in range(clusters):
        centers.append([
            rng.uniform(x_min + 80, x_max - 80),
            rng.uniform(y_min + 60, y_max - 60),
        ])

    points = []
    for center in centers:
        center = np.asarray(center, dtype=float)
        covariance = rng.uniform(260, 780)
        cloud = rng.normal(loc=center, scale=np.sqrt(covariance), size=(points_per_cluster, 2))
        points.append(cloud)

    noise = np.column_stack([
        rng.uniform(x_min, x_max, size=noise_points),
        rng.uniform(y_min, y_max, size=noise_points),
    ])
    points.append(noise)

    result = np.vstack(points)
    result[:, 0] = np.clip(result[:, 0], x_min, x_max)
    result[:, 1] = np.clip(result[:, 1], y_min, y_max)
    return result.astype(float)


def make_noise_points(
    count: int,
    width: int,
    height: int,
    side_panel_width: int,
    seed: Optional[int] = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    usable_width = width - side_panel_width - 80

    x = rng.uniform(60, usable_width, size=count)
    y = rng.uniform(70, height - 70, size=count)
    return np.column_stack([x, y]).astype(float)
