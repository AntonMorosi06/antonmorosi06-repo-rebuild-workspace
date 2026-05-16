from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, List, Tuple
import math


class SpatialHash:
    def __init__(self, cell_size: int = 70) -> None:
        self.cell_size = max(8, int(cell_size))
        self.cells: DefaultDict[Tuple[int, int], list[object]] = defaultdict(list)

    def clear(self) -> None:
        self.cells.clear()

    def key(self, x: float, y: float) -> Tuple[int, int]:
        return (int(math.floor(x / self.cell_size)), int(math.floor(y / self.cell_size)))

    def insert(self, item: object, x: float, y: float) -> None:
        self.cells[self.key(x, y)].append(item)

    def nearby(self, x: float, y: float, radius: float) -> List[object]:
        cell_radius = int(math.ceil(radius / self.cell_size))
        cx, cy = self.key(x, y)
        result: list[object] = []

        for gx in range(cx - cell_radius, cx + cell_radius + 1):
            for gy in range(cy - cell_radius, cy + cell_radius + 1):
                result.extend(self.cells.get((gx, gy), []))

        return result
