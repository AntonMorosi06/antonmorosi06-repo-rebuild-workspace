from __future__ import annotations

from collections import Counter
import math


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    n = len(ordered)
    middle = n // 2

    if n % 2 == 1:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / 2.0


def sample_stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    avg = mean(values)
    variance = sum((value - avg) ** 2 for value in values) / (len(values) - 1)
    return math.sqrt(variance)


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]

    position = q * (len(ordered) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))

    if lower == upper:
        return ordered[lower]

    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def numeric_summary(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {
            "count": 0,
            "min": 0.0,
            "max": 0.0,
            "mean": 0.0,
            "median": 0.0,
            "stdev": 0.0,
            "q1": 0.0,
            "q3": 0.0,
        }

    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "median": median(values),
        "stdev": sample_stdev(values),
        "q1": quantile(values, 0.25),
        "q3": quantile(values, 0.75),
    }


def top_values(values: list[str], limit: int = 8) -> list[dict[str, int | str]]:
    counter = Counter(values)
    return [
        {"value": value, "count": count}
        for value, count in counter.most_common(limit)
    ]


def pearson_correlation(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("correlation inputs must have equal length")
    if len(a) < 2:
        return 0.0

    mean_a = mean(a)
    mean_b = mean(b)

    numerator = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
    denom_a = math.sqrt(sum((x - mean_a) ** 2 for x in a))
    denom_b = math.sqrt(sum((y - mean_b) ** 2 for y in b))

    denominator = denom_a * denom_b
    if denominator < 1e-12:
        return 0.0

    return numerator / denominator
