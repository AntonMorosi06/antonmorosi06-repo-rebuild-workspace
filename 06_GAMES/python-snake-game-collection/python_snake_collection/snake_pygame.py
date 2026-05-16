from __future__ import annotations

from .core import Direction, SnakeGame


CELL = 26
FPS = 12

BACKGROUND = (8, 13, 22)
GRID = (17, 24, 39)
HEAD = (124, 255, 178)
BODY = (103, 215, 255)
FOOD = (255, 77, 95)
TEXT = (237, 243, 255)
MUTED = (154, 168, 189)


def run_pygame() -> None:
    try:
        import pygame
    except Exception as exc:
        raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements-pygame.txt") from exc

    game = SnakeGame(width=30, height=22, seed=None)

    pygame.init()
    pygame.display.set_caption("Python Snake Game Collection - Pygame")
    screen = pygame.display.set_mode((game.width * CELL, game.height * CELL + 72))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    big = pygame.font.SysFont("Arial", 32, bold=True)

    key_map = {
        pygame.K_UP: Direction.UP,
        pygame.K_w: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_s: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_a: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_d: Direction.RIGHT,
    }

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()
                    paused = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key in key_map:
                    game.turn(key_map[event.key])

        if not paused and not game.game_over:
            game.step()

        screen.fill(BACKGROUND)

        for y in range(game.height):
            for x in range(game.width):
                pygame.draw.rect(
                    screen,
                    GRID,
                    (x * CELL, y * CELL, CELL, CELL),
                    width=1,
                )

        food = game.food
        pygame.draw.ellipse(
            screen,
            FOOD,
            (food.x * CELL + 5, food.y * CELL + 5, CELL - 10, CELL - 10),
        )

        for index, point in enumerate(game.snake):
            color = HEAD if index == 0 else BODY
            pygame.draw.rect(
                screen,
                color,
                (point.x * CELL + 3, point.y * CELL + 3, CELL - 6, CELL - 6),
                border_radius=6,
            )

        panel_y = game.height * CELL
        pygame.draw.rect(screen, (12, 18, 30), (0, panel_y, game.width * CELL, 72))

        status = f"Score {game.score}   Steps {game.steps}   Length {len(game.snake)}"
        controls = "Arrows/WASD move | Space pause | R reset | Q/Esc quit"

        screen.blit(font.render(status, True, TEXT), (16, panel_y + 12))
        screen.blit(font.render(controls, True, MUTED), (16, panel_y + 40))

        if game.game_over:
            message = "YOU WIN" if game.win else "GAME OVER"
            overlay = pygame.Surface((game.width * CELL, game.height * CELL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            rendered = big.render(message, True, TEXT)
            screen.blit(
                rendered,
                (
                    game.width * CELL // 2 - rendered.get_width() // 2,
                    game.height * CELL // 2 - rendered.get_height() // 2,
                ),
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
