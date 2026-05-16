from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Iterable


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def move(self, direction: "Direction") -> "Point":
        dx, dy = direction.vector
        return Point(self.x + dx, self.y + dy)


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vector(self) -> tuple[int, int]:
        return self.value

    def opposite(self, other: "Direction") -> bool:
        dx, dy = self.vector
        ox, oy = other.vector
        return dx + ox == 0 and dy + oy == 0


@dataclass
class SnakeGame:
    width: int = 24
    height: int = 18
    seed: int | None = None
    snake: list[Point] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    pending_direction: Direction = Direction.RIGHT
    food: Point = Point(0, 0)
    score: int = 0
    steps: int = 0
    game_over: bool = False
    win: bool = False

    def __post_init__(self) -> None:
        if self.width < 6 or self.height < 6:
            raise ValueError("width and height must be at least 6")
        self.rng = random.Random(self.seed)
        self.reset()

    def reset(self) -> None:
        center = Point(self.width // 2, self.height // 2)
        self.snake = [
            center,
            Point(center.x - 1, center.y),
            Point(center.x - 2, center.y),
        ]
        self.direction = Direction.RIGHT
        self.pending_direction = Direction.RIGHT
        self.score = 0
        self.steps = 0
        self.game_over = False
        self.win = False
        self.food = self.place_food()

    def place_food(self) -> Point:
        occupied = set(self.snake)
        free = [
            Point(x, y)
            for y in range(self.height)
            for x in range(self.width)
            if Point(x, y) not in occupied
        ]

        if not free:
            self.win = True
            self.game_over = True
            return self.snake[0]

        return self.rng.choice(free)

    def turn(self, direction: Direction) -> None:
        if not direction.opposite(self.direction):
            self.pending_direction = direction

    def step(self) -> None:
        if self.game_over:
            return

        self.direction = self.pending_direction
        new_head = self.snake[0].move(self.direction)
        self.steps += 1

        if self.collides_with_wall(new_head):
            self.game_over = True
            return

        growing = new_head == self.food
        body_to_check = self.snake if growing else self.snake[:-1]

        if new_head in body_to_check:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if growing:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()

    def collides_with_wall(self, point: Point) -> bool:
        return point.x < 0 or point.x >= self.width or point.y < 0 or point.y >= self.height

    def board_rows(self) -> list[str]:
        snake_set = set(self.snake)
        rows = []

        for y in range(self.height):
            chars = []
            for x in range(self.width):
                point = Point(x, y)
                if point == self.snake[0]:
                    chars.append("@")
                elif point in snake_set:
                    chars.append("o")
                elif point == self.food:
                    chars.append("*")
                else:
                    chars.append(".")
            rows.append("".join(chars))

        return rows

    def board_text(self) -> str:
        return "\n".join(self.board_rows())

    def state_summary(self) -> dict[str, object]:
        return {
            "width": self.width,
            "height": self.height,
            "score": self.score,
            "steps": self.steps,
            "length": len(self.snake),
            "direction": self.direction.name,
            "food": {"x": self.food.x, "y": self.food.y},
            "game_over": self.game_over,
            "win": self.win,
        }


def direction_from_key(key: str) -> Direction | None:
    normalized = key.lower().strip()

    mapping = {
        "w": Direction.UP,
        "up": Direction.UP,
        "arrowup": Direction.UP,
        "s": Direction.DOWN,
        "down": Direction.DOWN,
        "arrowdown": Direction.DOWN,
        "a": Direction.LEFT,
        "left": Direction.LEFT,
        "arrowleft": Direction.LEFT,
        "d": Direction.RIGHT,
        "right": Direction.RIGHT,
        "arrowright": Direction.RIGHT,
    }

    return mapping.get(normalized)
