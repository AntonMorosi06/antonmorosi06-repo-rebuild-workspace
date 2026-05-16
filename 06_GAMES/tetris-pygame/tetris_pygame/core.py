from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Optional

from .tetrominoes import BAG_ORDER, TETROMINOES, TetrominoDefinition, get_definition


BOARD_WIDTH = 10
BOARD_HEIGHT = 20


@dataclass
class ActivePiece:
    name: str
    x: int
    y: int
    rotation: int = 0

    @property
    def definition(self) -> TetrominoDefinition:
        return get_definition(self.name)

    def cells(self, rotation: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> list[tuple[int, int]]:
        chosen_rotation = self.rotation if rotation is None else rotation % 4
        chosen_x = self.x if x is None else x
        chosen_y = self.y if y is None else y

        return [
            (chosen_x + dx, chosen_y + dy)
            for dx, dy in self.definition.rotations[chosen_rotation]
        ]


@dataclass
class TetrisGame:
    width: int = BOARD_WIDTH
    height: int = BOARD_HEIGHT
    seed: int | None = None
    board: list[list[str | None]] = field(default_factory=list)
    active: ActivePiece | None = None
    next_queue: list[str] = field(default_factory=list)
    hold_piece: str | None = None
    hold_used: bool = False
    score: int = 0
    lines: int = 0
    level: int = 1
    pieces_locked: int = 0
    game_over: bool = False
    paused: bool = False

    def __post_init__(self) -> None:
        if self.width < 6 or self.height < 10:
            raise ValueError("board is too small for Tetris")
        self.rng = random.Random(self.seed)
        self.reset()

    def reset(self) -> None:
        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.next_queue = []
        self.hold_piece = None
        self.hold_used = False
        self.score = 0
        self.lines = 0
        self.level = 1
        self.pieces_locked = 0
        self.game_over = False
        self.paused = False
        self._refill_bag()
        self.spawn_piece()

    def _refill_bag(self) -> None:
        bag = list(BAG_ORDER)
        self.rng.shuffle(bag)
        self.next_queue.extend(bag)

    def pop_next_piece(self) -> str:
        if len(self.next_queue) < 7:
            self._refill_bag()
        return self.next_queue.pop(0)

    def spawn_piece(self, name: str | None = None) -> None:
        piece_name = name or self.pop_next_piece()
        self.active = ActivePiece(name=piece_name, x=self.width // 2, y=0, rotation=0)
        self.hold_used = False

        if self.collides(self.active):
            self.game_over = True

    def collides(self, piece: ActivePiece, rotation: int | None = None, x: int | None = None, y: int | None = None) -> bool:
        for cell_x, cell_y in piece.cells(rotation=rotation, x=x, y=y):
            if cell_x < 0 or cell_x >= self.width:
                return True
            if cell_y >= self.height:
                return True
            if cell_y >= 0 and self.board[cell_y][cell_x] is not None:
                return True
        return False

    def move(self, dx: int, dy: int) -> bool:
        if self.game_over or self.paused or self.active is None:
            return False

        new_x = self.active.x + dx
        new_y = self.active.y + dy

        if not self.collides(self.active, x=new_x, y=new_y):
            self.active.x = new_x
            self.active.y = new_y
            return True

        return False

    def soft_drop(self) -> bool:
        moved = self.move(0, 1)
        if moved:
            self.score += 1
        return moved

    def hard_drop(self) -> int:
        if self.game_over or self.paused or self.active is None:
            return 0

        distance = 0
        while self.move(0, 1):
            distance += 1

        self.score += distance * 2
        self.lock_piece()
        return distance

    def rotate(self, clockwise: bool = True) -> bool:
        if self.game_over or self.paused or self.active is None:
            return False

        old_rotation = self.active.rotation
        new_rotation = (old_rotation + (1 if clockwise else -1)) % 4

        kicks = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]

        for kick_x, kick_y in kicks:
            test_x = self.active.x + kick_x
            test_y = self.active.y + kick_y
            if not self.collides(self.active, rotation=new_rotation, x=test_x, y=test_y):
                self.active.rotation = new_rotation
                self.active.x = test_x
                self.active.y = test_y
                return True

        return False

    def hold(self) -> bool:
        if self.game_over or self.paused or self.active is None or self.hold_used:
            return False

        current = self.active.name

        if self.hold_piece is None:
            self.hold_piece = current
            self.spawn_piece()
        else:
            self.active = ActivePiece(name=self.hold_piece, x=self.width // 2, y=0, rotation=0)
            self.hold_piece = current
            if self.collides(self.active):
                self.game_over = True

        self.hold_used = True
        return True

    def tick(self) -> None:
        if self.game_over or self.paused:
            return

        if not self.move(0, 1):
            self.lock_piece()

    def lock_piece(self) -> None:
        if self.active is None:
            return

        for cell_x, cell_y in self.active.cells():
            if cell_y < 0:
                self.game_over = True
                return
            if 0 <= cell_y < self.height and 0 <= cell_x < self.width:
                self.board[cell_y][cell_x] = self.active.name

        self.pieces_locked += 1
        cleared = self.clear_lines()
        self.apply_score(cleared)
        self.spawn_piece()

    def clear_lines(self) -> int:
        remaining = [row for row in self.board if any(cell is None for cell in row)]
        cleared = self.height - len(remaining)

        for _ in range(cleared):
            remaining.insert(0, [None for _ in range(self.width)])

        self.board = remaining
        self.lines += cleared
        self.level = 1 + self.lines // 10
        return cleared

    def apply_score(self, cleared: int) -> None:
        if cleared <= 0:
            return

        line_scores = {
            1: 100,
            2: 300,
            3: 500,
            4: 800,
        }
        self.score += line_scores.get(cleared, 0) * self.level

    def ghost_piece_y(self) -> int:
        if self.active is None:
            return 0

        ghost_y = self.active.y
        while not self.collides(self.active, y=ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def visible_cells(self) -> dict[tuple[int, int], str]:
        cells = {}

        for y, row in enumerate(self.board):
            for x, value in enumerate(row):
                if value is not None:
                    cells[(x, y)] = value

        if self.active is not None:
            for x, y in self.active.cells():
                if y >= 0:
                    cells[(x, y)] = self.active.name

        return cells

    def state_summary(self) -> dict[str, object]:
        return {
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "pieces_locked": self.pieces_locked,
            "active": self.active.name if self.active else None,
            "hold": self.hold_piece,
            "next": self.next_queue[:3],
            "game_over": self.game_over,
            "paused": self.paused,
        }
