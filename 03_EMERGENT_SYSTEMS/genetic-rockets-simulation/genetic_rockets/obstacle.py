from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import random

import pygame


Color = Tuple[int, int, int]


@dataclass
class RectObstacle:
    rect: pygame.Rect
    color: Color = (255, 107, 107)

    def contains_point(self, point: pygame.Vector2) -> bool:
        return self.rect.collidepoint(int(point.x), int(point.y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (255, 235, 235), self.rect, width=2, border_radius=8)


def default_obstacle(width: int, height: int) -> RectObstacle:
    rect = pygame.Rect(width // 2 - 165, height // 2 + 25, 330, 26)
    return RectObstacle(rect=rect)


def random_obstacle(width: int, height: int) -> RectObstacle:
    obstacle_width = random.randint(190, 360)
    obstacle_height = random.randint(22, 42)
    x = random.randint(120, max(121, width - obstacle_width - 120))
    y = random.randint(height // 2 - 40, height // 2 + 145)
    return RectObstacle(rect=pygame.Rect(x, y, obstacle_width, obstacle_height))
