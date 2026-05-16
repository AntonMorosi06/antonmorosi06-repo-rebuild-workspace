from __future__ import annotations

import math

from .linalg import Matrix, distance


def gaussian_affinity(data: Matrix, sigma: float) -> Matrix:
    if sigma <= 0:
        raise ValueError("sigma must be positive")

    n = len(data)
    scale = 2.0 * sigma * sigma
    affinity = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        affinity[i][i] = 0.0
        for j in range(i + 1, n):
            d = distance(data[i], data[j])
            value = math.exp(-(d * d) / scale)
            affinity[i][j] = value
            affinity[j][i] = value

    return affinity


def sparsify_knn(affinity: Matrix, k_neighbors: int | None) -> Matrix:
    if k_neighbors is None or k_neighbors <= 0:
        return [row[:] for row in affinity]

    n = len(affinity)
    sparse = [[0.0 for _ in range(n)] for _ in range(n)]

    for i, row in enumerate(affinity):
        ranked = sorted(
            [(value, j) for j, value in enumerate(row) if j != i],
            reverse=True,
        )
        for value, j in ranked[:k_neighbors]:
            sparse[i][j] = value

    for i in range(n):
        for j in range(i + 1, n):
            value = max(sparse[i][j], sparse[j][i])
            sparse[i][j] = value
            sparse[j][i] = value

    return sparse


def degree_vector(affinity: Matrix) -> list[float]:
    return [sum(row) for row in affinity]


def normalized_laplacian(affinity: Matrix) -> Matrix:
    n = len(affinity)
    degree = degree_vector(affinity)
    laplacian = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        laplacian[i][i] = 1.0

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if degree[i] <= 1e-12 or degree[j] <= 1e-12:
                value = 0.0
            else:
                value = -affinity[i][j] / math.sqrt(degree[i] * degree[j])
            laplacian[i][j] = value

    return laplacian


def graph_edges_for_display(data: Matrix, affinity: Matrix, threshold: float = 0.55, max_edges: int = 520) -> list[tuple[int, int, float]]:
    edges: list[tuple[int, int, float]] = []
    n = len(data)

    for i in range(n):
        for j in range(i + 1, n):
            value = affinity[i][j]
            if value >= threshold:
                edges.append((i, j, value))

    edges.sort(key=lambda item: item[2], reverse=True)
    return edges[:max_edges]
