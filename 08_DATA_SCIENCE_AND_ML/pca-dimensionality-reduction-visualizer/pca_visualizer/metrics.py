from __future__ import annotations

from .linalg import Matrix


def bounds_2d(data: Matrix, x_index: int = 0, y_index: int = 1) -> tuple[float, float, float, float]:
    if not data:
        return (-1.0, 1.0, -1.0, 1.0)

    xs = [row[x_index] for row in data]
    ys = [row[y_index] for row in data]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    pad_x = max(0.5, (max_x - min_x) * 0.14)
    pad_y = max(0.5, (max_y - min_y) * 0.14)

    return (min_x - pad_x, max_x + pad_x, min_y - pad_y, max_y + pad_y)


def reconstruction_mse(original: Matrix, reconstructed: Matrix) -> float:
    if not original or not reconstructed:
        return 0.0

    total = 0.0
    count = 0

    for row_a, row_b in zip(original, reconstructed):
        for a, b in zip(row_a, row_b):
            total += (a - b) ** 2
            count += 1

    return total / max(1, count)


def pca_summary(result) -> dict[str, object]:
    return {
        "n_components": result.n_components,
        "eigenvalues": result.eigenvalues,
        "explained_variance_ratio": result.explained_variance_ratio,
        "retained_variance_ratio": result.retained_variance_ratio,
        "reconstruction_mse": reconstruction_mse(
            [[centered_value + mean_value for centered_value, mean_value in zip(row, result.mean)] for row in result.centered],
            result.reconstructed,
        ),
    }
