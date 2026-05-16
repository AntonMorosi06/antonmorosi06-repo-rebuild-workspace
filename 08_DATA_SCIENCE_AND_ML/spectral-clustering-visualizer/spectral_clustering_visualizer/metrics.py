from __future__ import annotations

from collections import Counter

from .linalg import Matrix


def bounds_2d(data: Matrix, x_index: int = 0, y_index: int = 1) -> tuple[float, float, float, float]:
    if not data:
        return (-1.0, 1.0, -1.0, 1.0)

    xs = [row[x_index] for row in data]
    ys = [row[y_index] if len(row) > y_index else 0.0 for row in data]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    pad_x = max(0.5, (max_x - min_x) * 0.14)
    pad_y = max(0.5, (max_y - min_y) * 0.14)

    return (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)


def cluster_size_map(labels: list[int]) -> dict[int, int]:
    return dict(sorted(Counter(labels).items()))


def result_summary(result) -> dict[str, object]:
    return {
        "k": result.k,
        "sigma": result.sigma,
        "k_neighbors": result.k_neighbors,
        "cluster_count": result.cluster_count,
        "cluster_sizes": cluster_size_map(result.labels),
        "first_eigenvalues": result.eigenvalues[: min(8, len(result.eigenvalues))],
    }
