from __future__ import annotations

import random

from .linalg import Matrix, distance


def nearest_center(point: list[float], centers: Matrix) -> int:
    best_index = 0
    best_distance = float("inf")

    for index, center in enumerate(centers):
        d = distance(point, center)
        if d < best_distance:
            best_distance = d
            best_index = index

    return best_index


def mean_of_points(points: Matrix, dimension: int) -> list[float]:
    if not points:
        return [0.0 for _ in range(dimension)]

    return [
        sum(point[index] for point in points) / len(points)
        for index in range(dimension)
    ]


def kmeans(data: Matrix, k: int, seed: int = 42, max_iterations: int = 80) -> tuple[list[int], Matrix]:
    if not data:
        raise ValueError("data cannot be empty")
    if k < 1:
        raise ValueError("k must be at least 1")
    if k > len(data):
        raise ValueError("k cannot exceed number of data points")

    rng = random.Random(seed)
    dimension = len(data[0])
    initial_indices = rng.sample(range(len(data)), k)
    centers = [data[index][:] for index in initial_indices]
    labels = [0 for _ in data]

    for _ in range(max_iterations):
        changed = False

        for index, point in enumerate(data):
            label = nearest_center(point, centers)
            if label != labels[index]:
                changed = True
                labels[index] = label

        buckets = [[] for _ in range(k)]
        for label, point in zip(labels, data):
            buckets[label].append(point)

        for index in range(k):
            if buckets[index]:
                centers[index] = mean_of_points(buckets[index], dimension)
            else:
                centers[index] = data[rng.randrange(len(data))][:]

        if not changed:
            break

    return labels, centers
