from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


NOISE = -1
UNVISITED = -99


@dataclass
class DBSCANResult:
    labels: np.ndarray
    core_mask: np.ndarray
    neighbors: List[List[int]]
    eps: float
    min_samples: int

    @property
    def cluster_count(self) -> int:
        valid = self.labels[self.labels >= 0]
        if valid.size == 0:
            return 0
        return int(valid.max()) + 1

    @property
    def noise_count(self) -> int:
        return int(np.sum(self.labels == NOISE))

    @property
    def core_count(self) -> int:
        return int(np.sum(self.core_mask))


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a NumPy array with shape (n, 2)")
    if len(points) == 0:
        return np.zeros((0, 0), dtype=float)
    delta = points[:, None, :] - points[None, :, :]
    return np.sqrt(np.sum(delta * delta, axis=2))


def region_query(distance_matrix: np.ndarray, point_index: int, eps: float) -> List[int]:
    if eps <= 0:
        raise ValueError("eps must be positive")
    return np.where(distance_matrix[point_index] <= eps)[0].astype(int).tolist()


def dbscan(points: np.ndarray, eps: float, min_samples: int) -> DBSCANResult:
    points = np.asarray(points, dtype=float)

    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must be a NumPy array with shape (n, 2)")
    if eps <= 0:
        raise ValueError("eps must be positive")
    if min_samples < 1:
        raise ValueError("min_samples must be at least 1")

    n = len(points)
    if n == 0:
        return DBSCANResult(
            labels=np.array([], dtype=int),
            core_mask=np.array([], dtype=bool),
            neighbors=[],
            eps=float(eps),
            min_samples=int(min_samples),
        )

    distance_matrix = pairwise_distances(points)
    neighbors = [region_query(distance_matrix, i, eps) for i in range(n)]
    core_mask = np.array([len(items) >= min_samples for items in neighbors], dtype=bool)

    labels = np.full(n, UNVISITED, dtype=int)
    cluster_id = 0

    for point_index in range(n):
        if labels[point_index] != UNVISITED:
            continue

        if not core_mask[point_index]:
            labels[point_index] = NOISE
            continue

        labels[point_index] = cluster_id
        queue = list(neighbors[point_index])
        queued = set(queue)

        while queue:
            neighbor_index = queue.pop(0)

            if labels[neighbor_index] == NOISE:
                labels[neighbor_index] = cluster_id

            if labels[neighbor_index] != UNVISITED:
                continue

            labels[neighbor_index] = cluster_id

            if core_mask[neighbor_index]:
                for candidate in neighbors[neighbor_index]:
                    if candidate not in queued:
                        queue.append(candidate)
                        queued.add(candidate)

        cluster_id += 1

    return DBSCANResult(
        labels=labels,
        core_mask=core_mask,
        neighbors=neighbors,
        eps=float(eps),
        min_samples=int(min_samples),
    )
