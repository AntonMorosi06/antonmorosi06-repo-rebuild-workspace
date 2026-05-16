from __future__ import annotations

from dataclasses import dataclass
from collections import deque

from .point import ClusteredPoint, Point2D


NOISE = -1


@dataclass
class DBSCANResult:
    points: list[ClusteredPoint]
    epsilon: float
    min_samples: int
    cluster_count: int
    noise_count: int
    core_count: int
    border_count: int

    def labels(self) -> list[int | None]:
        return [point.label for point in self.points]


def region_query(points: list[ClusteredPoint], index: int, epsilon: float) -> list[int]:
    center = points[index].point
    neighbors: list[int] = []

    for other_index, candidate in enumerate(points):
        if center.distance_to(candidate.point) <= epsilon:
            neighbors.append(other_index)

    return neighbors


def reset_points(points: list[ClusteredPoint]) -> None:
    for point in points:
        point.reset_clustering()


def dbscan(raw_points: list[Point2D], epsilon: float, min_samples: int) -> DBSCANResult:
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if min_samples < 1:
        raise ValueError("min_samples must be at least 1")

    points = [ClusteredPoint(point=point) for point in raw_points]
    cluster_id = 0

    for index, point in enumerate(points):
        if point.visited:
            continue

        point.visited = True
        neighbors = region_query(points, index, epsilon)
        point.neighbor_count = len(neighbors)

        if len(neighbors) < min_samples:
            point.label = NOISE
            point.is_noise = True
            continue

        expand_cluster(points, index, neighbors, cluster_id, epsilon, min_samples)
        cluster_id += 1

    finalize_border_and_noise(points)

    core_count = sum(1 for point in points if point.is_core)
    border_count = sum(1 for point in points if point.is_border)
    noise_count = sum(1 for point in points if point.label == NOISE)

    return DBSCANResult(
        points=points,
        epsilon=epsilon,
        min_samples=min_samples,
        cluster_count=cluster_id,
        noise_count=noise_count,
        core_count=core_count,
        border_count=border_count,
    )


def expand_cluster(
    points: list[ClusteredPoint],
    start_index: int,
    neighbors: list[int],
    cluster_id: int,
    epsilon: float,
    min_samples: int,
) -> None:
    points[start_index].label = cluster_id
    points[start_index].is_core = True
    points[start_index].is_noise = False

    queue = deque(neighbors)
    queued = set(neighbors)

    while queue:
        neighbor_index = queue.popleft()
        neighbor = points[neighbor_index]

        if not neighbor.visited:
            neighbor.visited = True
            new_neighbors = region_query(points, neighbor_index, epsilon)
            neighbor.neighbor_count = len(new_neighbors)

            if len(new_neighbors) >= min_samples:
                neighbor.is_core = True
                for candidate_index in new_neighbors:
                    if candidate_index not in queued:
                        queue.append(candidate_index)
                        queued.add(candidate_index)

        if neighbor.label is None or neighbor.label == NOISE:
            neighbor.label = cluster_id
            neighbor.is_noise = False


def finalize_border_and_noise(points: list[ClusteredPoint]) -> None:
    for point in points:
        if point.label == NOISE:
            point.is_noise = True
            point.is_border = False
            point.is_core = False
        elif point.label is not None and not point.is_core:
            point.is_border = True
            point.is_noise = False
