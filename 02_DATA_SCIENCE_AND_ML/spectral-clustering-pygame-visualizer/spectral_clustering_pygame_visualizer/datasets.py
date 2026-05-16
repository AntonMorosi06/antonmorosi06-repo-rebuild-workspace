from __future__ import annotations

from typing import Optional

import numpy as np


def make_moons_like_dataset(
    width: int,
    height: int,
    side_panel_width: int,
    seed: Optional[int] = None,
    points_per_arc: int = 95,
    noise_points: int = 28,
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    canvas_width = width - side_panel_width
    center_x = canvas_width * 0.48
    center_y = height * 0.50

    theta_a = rng.uniform(0.0, np.pi, size=points_per_arc)
    arc_a = np.column_stack([
        center_x + 220.0 * np.cos(theta_a),
        center_y - 70.0 + 145.0 * np.sin(theta_a),
    ])

    theta_b = rng.uniform(0.0, np.pi, size=points_per_arc)
    arc_b = np.column_stack([
        center_x + 220.0 * np.cos(theta_b) + 95.0,
        center_y + 105.0 - 145.0 * np.sin(theta_b),
    ])

    arc_a += rng.normal(0.0, 14.0, size=arc_a.shape)
    arc_b += rng.normal(0.0, 14.0, size=arc_b.shape)

    noise = np.column_stack([
        rng.uniform(60.0, canvas_width - 70.0, size=noise_points),
        rng.uniform(65.0, height - 70.0, size=noise_points),
    ])

    points = np.vstack([arc_a, arc_b, noise])
    points[:, 0] = np.clip(points[:, 0], 45.0, canvas_width - 45.0)
    points[:, 1] = np.clip(points[:, 1], 45.0, height - 45.0)
    return points.astype(float)


def make_random_noise(
    count: int,
    width: int,
    height: int,
    side_panel_width: int,
    seed: Optional[int] = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    canvas_width = width - side_panel_width
    return np.column_stack([
        rng.uniform(55.0, canvas_width - 55.0, size=count),
        rng.uniform(55.0, height - 55.0, size=count),
    ]).astype(float)
