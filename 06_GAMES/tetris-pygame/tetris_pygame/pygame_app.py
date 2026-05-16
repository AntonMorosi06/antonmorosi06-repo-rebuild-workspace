from __future__ import annotations

from pathlib import Path

from .core import TetrisGame
from .highscore import load_highscore, update_highscore
from .tetrominoes import TETROMINOES


CELL = 30
BOARD_LEFT = 32
BOARD_TOP = 32
PANEL_LEFT = BOARD_LEFT + CELL * 10 + 32
WIDTH = 640
HEIGHT = 720

BACKGROUND = (8, 13, 22)
PANEL = (17, 24, 39)
GRID = (31, 41, 55)
TEXT = (237, 243, 255)
MUTED = (154, 168, 189)
GHOST = (86, 96, 112)


class TetrisPygameApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("Tetris Pygame - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 19)
        self.big = pygame.font.SysFont("Arial", 34, bold=True)

        self.game = TetrisGame(seed=None)
        self.highscore_path = Path(__file__).resolve().parents[1] / "data" / "highscore.json"
        self.highscore = load_highscore(self.highscore_path)
        self.running = True
        self.drop_timer = 0.0

    def drop_interval(self) -> float:
        return max(0.08, 0.64 - (self.game.level - 1) * 0.045)

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_p:
            self.game.paused = not self.game.paused
        elif key == pygame.K_r:
            self.game.reset()
        elif key == pygame.K_LEFT:
            self.game.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.game.move(1, 0)
        elif key == pygame.K_DOWN:
            self.game.soft_drop()
        elif key in (pygame.K_UP, pygame.K_x):
            self.game.rotate(clockwise=True)
        elif key == pygame.K_z:
            self.game.rotate(clockwise=False)
        elif key == pygame.K_SPACE:
            self.game.hard_drop()
        elif key == pygame.K_c:
            self.game.hold()

    def update(self, dt: float) -> None:
        if self.game.game_over:
            self.highscore = update_highscore(self.highscore_path, self.game.score)
            return

        if self.game.paused:
            return

        self.drop_timer += dt
        if self.drop_timer >= self.drop_interval():
            self.drop_timer = 0.0
            self.game.tick()

    def draw_cell(self, x: int, y: int, color: tuple[int, int, int], inset: int = 2) -> None:
        pygame = self.pygame
        rect = pygame.Rect(
            BOARD_LEFT + x * CELL + inset,
            BOARD_TOP + y * CELL + inset,
            CELL - inset * 2,
            CELL - inset * 2,
        )
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, width=1, border_radius=5)

    def draw_board(self) -> None:
        pygame = self.pygame
        board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, CELL * self.game.width, CELL * self.game.height)
        pygame.draw.rect(self.screen, PANEL, board_rect, border_radius=12)

        for y in range(self.game.height):
            for x in range(self.game.width):
                rect = pygame.Rect(BOARD_LEFT + x * CELL, BOARD_TOP + y * CELL, CELL, CELL)
                pygame.draw.rect(self.screen, GRID, rect, width=1)

        if self.game.active is not None:
            ghost_y = self.game.ghost_piece_y()
            for x, y in self.game.active.cells(y=ghost_y):
                if y >= 0:
                    self.draw_cell(x, y, GHOST, inset=7)

        for (x, y), name in self.game.visible_cells().items():
            color = TETROMINOES[name].color
            self.draw_cell(x, y, color)

    def draw_small_piece(self, name: str | None, x: int, y: int) -> None:
        if not name:
            return

        pygame = self.pygame
        definition = TETROMINOES[name]
        for dx, dy in definition.rotations[0]:
            rect = pygame.Rect(x + (dx + 2) * 18, y + (dy + 2) * 18, 15, 15)
            pygame.draw.rect(self.screen, definition.color, rect, border_radius=4)

    def text(self, value: str, x: int, y: int, color=TEXT, big: bool = False) -> None:
        font = self.big if big else self.font
        rendered = font.render(value, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_panel(self) -> None:
        pygame = self.pygame
        panel_rect = pygame.Rect(PANEL_LEFT, BOARD_TOP, WIDTH - PANEL_LEFT - 30, CELL * self.game.height)
        pygame.draw.rect(self.screen, PANEL, panel_rect, border_radius=16)

        x = PANEL_LEFT + 18
        y = BOARD_TOP + 18

        self.text("TETRIS", x, y, big=True)
        y += 56

        items = [
            ("Score", self.game.score),
            ("High score", self.highscore),
            ("Lines", self.game.lines),
            ("Level", self.game.level),
            ("Locked", self.game.pieces_locked),
        ]

        for label, value in items:
            self.text(label, x, y, MUTED)
            self.text(str(value), x, y + 22, TEXT)
            y += 58

        self.text("Next", x, y, MUTED)
        y += 18
        self.draw_small_piece(self.game.next_queue[0] if self.game.next_queue else None, x, y)
        y += 90

        self.text("Hold", x, y, MUTED)
        y += 18
        self.draw_small_piece(self.game.hold_piece, x, y)
        y += 100

        controls = [
            "←/→ move",
            "↓ soft drop",
            "↑/X rotate",
            "Z rotate back",
            "Space hard drop",
            "C hold",
            "P pause",
            "R reset",
            "Q/Esc quit",
        ]

        for line in controls:
            self.text(line, x, y, MUTED)
            y += 23

    def draw_overlay(self) -> None:
        if not self.game.game_over and not self.game.paused:
            return

        pygame = self.pygame
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        self.screen.blit(overlay, (0, 0))

        if self.game.game_over:
            message = "GAME OVER"
            sub = "Press R to reset"
        else:
            message = "PAUSED"
            sub = "Press P to resume"

        rendered = self.big.render(message, True, TEXT)
        self.screen.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, HEIGHT // 2 - 42))
        rendered_sub = self.font.render(sub, True, MUTED)
        self.screen.blit(rendered_sub, (WIDTH // 2 - rendered_sub.get_width() // 2, HEIGHT // 2 + 8))

    def draw(self) -> None:
        self.screen.fill(BACKGROUND)
        self.draw_board()
        self.draw_panel()
        self.draw_overlay()
        self.pygame.display.flip()

    def run(self) -> None:
        pygame = self.pygame

        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.update(dt)
            self.draw()

        pygame.quit()


def run_app() -> None:
    TetrisPygameApp().run()
