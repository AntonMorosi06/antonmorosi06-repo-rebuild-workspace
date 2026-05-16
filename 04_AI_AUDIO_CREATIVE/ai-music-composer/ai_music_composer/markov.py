from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Sequence


@dataclass
class WeightedTransition:
    options: list[int]
    weights: list[float]

    def choose(self, rng: random.Random) -> int:
        return rng.choices(self.options, weights=self.weights, k=1)[0]


class MarkovMelodyModel:
    def __init__(self, scale_degrees: Sequence[int]) -> None:
        if not scale_degrees:
            raise ValueError("scale_degrees cannot be empty")

        self.scale_degrees = list(scale_degrees)
        self.transitions = self._build_default_transitions()

    def _build_default_transitions(self) -> dict[int, WeightedTransition]:
        transitions: dict[int, WeightedTransition] = {}

        for degree in self.scale_degrees:
            options = []
            weights = []

            for candidate in self.scale_degrees:
                distance = abs(candidate - degree)
                if distance == 0:
                    weight = 0.85
                elif distance == 1:
                    weight = 1.40
                elif distance == 2:
                    weight = 1.05
                elif distance == 3:
                    weight = 0.55
                else:
                    weight = 0.22

                if candidate in (0, 2, 4):
                    weight *= 1.12

                options.append(candidate)
                weights.append(weight)

            transitions[degree] = WeightedTransition(options=options, weights=weights)

        return transitions

    def generate(self, length: int, rng: random.Random, start_degree: int = 0) -> list[int]:
        if length < 1:
            raise ValueError("length must be at least 1")

        current = start_degree
        result = [current]

        for _ in range(length - 1):
            transition = self.transitions.get(current)
            if transition is None:
                current = rng.choice(self.scale_degrees)
            else:
                current = transition.choose(rng)
            result.append(current)

        return result


def rhythm_pattern(style: str, rng: random.Random, steps: int) -> list[float]:
    if steps < 1:
        raise ValueError("steps must be at least 1")

    if style == "ambient":
        choices = [0.5, 1.0, 1.5, 2.0]
        weights = [0.20, 0.35, 0.25, 0.20]
    elif style == "arcade":
        choices = [0.25, 0.5, 0.75, 1.0]
        weights = [0.34, 0.36, 0.14, 0.16]
    elif style == "dark":
        choices = [0.5, 1.0, 1.0, 1.5]
        weights = [0.25, 0.35, 0.25, 0.15]
    else:
        choices = [0.5, 0.75, 1.0, 1.5]
        weights = [0.25, 0.25, 0.35, 0.15]

    return [rng.choices(choices, weights=weights, k=1)[0] for _ in range(steps)]


def velocity_pattern(style: str, rng: random.Random, steps: int) -> list[int]:
    if style == "ambient":
        return [rng.randint(48, 72) for _ in range(steps)]
    if style == "arcade":
        return [rng.randint(78, 112) for _ in range(steps)]
    if style == "dark":
        return [rng.randint(58, 92) for _ in range(steps)]
    return [rng.randint(64, 102) for _ in range(steps)]
