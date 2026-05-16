from __future__ import annotations

from dataclasses import dataclass

import pygame

from .config import FOOD_COLOR


@dataclass
class Food:
    position: pygame.Vector2
    energy: float = 38.0
    radius: float = 3.5

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, FOOD_COLOR, (int(self.position.x), int(self.position.y)), int(self.radius))
        pygame.draw.circle(surface, (220, 255, 230), (int(self.position.x), int(self.position.y)), int(self.radius + 2), 1)

    @classmethod
    def at(cls, x: float, y: float) -> "Food":
        return cls(position=pygame.Vector2(x, y))
