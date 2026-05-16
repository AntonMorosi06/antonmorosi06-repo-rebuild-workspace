from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Point2D:
    x: float
    y: float

    def distance_to(self, other: "Point2D") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass
class ClusteredPoint:
    point: Point2D
    label: int | None = None
    visited: bool = False
    is_core: bool = False
    is_border: bool = False
    is_noise: bool = False
    neighbor_count: int = 0

    def reset_clustering(self) -> None:
        self.label = None
        self.visited = False
        self.is_core = False
        self.is_border = False
        self.is_noise = False
        self.neighbor_count = 0
