from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


Cell = Tuple[int, int]


@dataclass(frozen=True)
class TetrominoDefinition:
    name: str
    color: tuple[int, int, int]
    rotations: tuple[tuple[Cell, ...], ...]


TETROMINOES: Dict[str, TetrominoDefinition] = {
    "I": TetrominoDefinition(
        name="I",
        color=(103, 215, 255),
        rotations=(
            ((-2, 0), (-1, 0), (0, 0), (1, 0)),
            ((0, -1), (0, 0), (0, 1), (0, 2)),
            ((-2, 1), (-1, 1), (0, 1), (1, 1)),
            ((-1, -1), (-1, 0), (-1, 1), (-1, 2)),
        ),
    ),
    "O": TetrominoDefinition(
        name="O",
        color=(255, 209, 102),
        rotations=(
            ((0, 0), (1, 0), (0, 1), (1, 1)),
            ((0, 0), (1, 0), (0, 1), (1, 1)),
            ((0, 0), (1, 0), (0, 1), (1, 1)),
            ((0, 0), (1, 0), (0, 1), (1, 1)),
        ),
    ),
    "T": TetrominoDefinition(
        name="T",
        color=(183, 148, 255),
        rotations=(
            ((-1, 0), (0, 0), (1, 0), (0, 1)),
            ((0, -1), (0, 0), (0, 1), (1, 0)),
            ((-1, 0), (0, 0), (1, 0), (0, -1)),
            ((0, -1), (0, 0), (0, 1), (-1, 0)),
        ),
    ),
    "S": TetrominoDefinition(
        name="S",
        color=(124, 255, 178),
        rotations=(
            ((0, 0), (1, 0), (-1, 1), (0, 1)),
            ((0, -1), (0, 0), (1, 0), (1, 1)),
            ((0, 0), (1, 0), (-1, 1), (0, 1)),
            ((0, -1), (0, 0), (1, 0), (1, 1)),
        ),
    ),
    "Z": TetrominoDefinition(
        name="Z",
        color=(255, 77, 95),
        rotations=(
            ((-1, 0), (0, 0), (0, 1), (1, 1)),
            ((1, -1), (0, 0), (1, 0), (0, 1)),
            ((-1, 0), (0, 0), (0, 1), (1, 1)),
            ((1, -1), (0, 0), (1, 0), (0, 1)),
        ),
    ),
    "J": TetrominoDefinition(
        name="J",
        color=(90, 168, 255),
        rotations=(
            ((-1, 0), (0, 0), (1, 0), (-1, 1)),
            ((0, -1), (0, 0), (0, 1), (1, 1)),
            ((-1, 0), (0, 0), (1, 0), (1, -1)),
            ((0, -1), (0, 0), (0, 1), (-1, -1)),
        ),
    ),
    "L": TetrominoDefinition(
        name="L",
        color=(255, 184, 107),
        rotations=(
            ((-1, 0), (0, 0), (1, 0), (1, 1)),
            ((0, -1), (0, 0), (0, 1), (1, -1)),
            ((-1, 0), (0, 0), (1, 0), (-1, -1)),
            ((0, -1), (0, 0), (0, 1), (-1, 1)),
        ),
    ),
}


BAG_ORDER = tuple(TETROMINOES.keys())


def get_definition(name: str) -> TetrominoDefinition:
    if name not in TETROMINOES:
        raise ValueError(f"unknown tetromino: {name}")
    return TETROMINOES[name]
