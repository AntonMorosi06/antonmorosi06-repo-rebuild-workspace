from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vec2":
        if abs(scalar) < 1e-12:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / scalar, self.y / scalar)

    def copy(self) -> "Vec2":
        return Vec2(self.x, self.y)

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def normalized(self) -> "Vec2":
        value = self.length()
        if value < 1e-12:
            return Vec2(0.0, 0.0)
        return self / value

    def perpendicular(self) -> "Vec2":
        return Vec2(-self.y, self.x)

    def clamp_length(self, maximum: float) -> "Vec2":
        current = self.length()
        if current <= maximum or current < 1e-12:
            return self
        return self.normalized() * maximum

    def tuple_int(self) -> tuple[int, int]:
        return (int(self.x), int(self.y))


def distance(a: Vec2, b: Vec2) -> float:
    return (a - b).length()


def from_angle(angle: float, magnitude: float = 1.0) -> Vec2:
    return Vec2(math.cos(angle) * magnitude, math.sin(angle) * magnitude)
