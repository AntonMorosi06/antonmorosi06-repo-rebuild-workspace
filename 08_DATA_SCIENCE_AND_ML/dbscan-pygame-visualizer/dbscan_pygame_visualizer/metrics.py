from __future__ import annotations

from collections import Counter

from .dbscan import DBSCANResult, NOISE


def cluster_size_map(result: DBSCANResult) -> dict[int, int]:
    counter = Counter(point.label for point in result.points if point.label is not None and point.label != NOISE)
    return dict(sorted(counter.items()))


def result_summary(result: DBSCANResult) -> dict[str, object]:
    return {
        "epsilon": result.epsilon,
        "min_samples": result.min_samples,
        "cluster_count": result.cluster_count,
        "noise_count": result.noise_count,
        "core_count": result.core_count,
        "border_count": result.border_count,
        "cluster_sizes": cluster_size_map(result),
    }


def normalized_bounds(points) -> tuple[float, float, float, float]:
    if not points:
        return (-1.0, 1.0, -1.0, 1.0)

    xs = [point.x for point in points]
    ys = [point.y for point in points]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    pad_x = max(0.5, (max_x - min_x) * 0.12)
    pad_y = max(0.5, (max_y - min_y) * 0.12)

    return (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)
