from __future__ import annotations

from pathlib import Path
import math

from .config import (
    ALIEN_ALT_COLOR,
    ALIEN_COLOR,
    BACKGROUND,
    BULLET_COLOR,
    ENEMY_BULLET_COLOR,
    MUTED,
    PANEL,
    PLAYER_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TEXT,
    WORLD_HEIGHT,
)
from .core import Alien, Bullet, SpaceInvadersGame
from .highscore import load_highscore, update_highscore


class SpaceInvadersPygameApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("Space Invaders Pygame - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 19)
        self.big = pygame.font.SysFont("Arial", 36, bold=True)
        self.game = SpaceInvadersGame(seed=None)
        self.highscore_path = Path(__file__).resolve().parents[1] / "data" / "highscore.json"
        self.highscore = load_highscore(self.highscore_path)
        self.running = True
        self.left_pressed = False
        self.right_pressed = False

    def handle_keydown(self, key: int) -> None:
        pygame = self.pygame
        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.left_pressed = True
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.right_pressed = True
        elif key == pygame.K_SPACE:
            self.game.player_shoot()
        elif key == pygame.K_p:
            self.game.paused = not self.game.paused
        elif key == pygame.K_r:
            self.game.reset()

    def handle_keyup(self, key: int) -> None:
        pygame = self.pygame
        if key in (pygame.K_LEFT, pygame.K_a):
            self.left_pressed = False
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.right_pressed = False

    def update(self) -> None:
        if self.left_pressed:
            self.game.move_player(-1)
        if self.right_pressed:
            self.game.move_player(1)

        self.game.update()

        if self.game.game_over:
            self.highscore = update_highscore(self.highscore_path, self.game.score)

    def draw_player(self) -> None:
        pygame = self.pygame
        player = self.game.player
        x = int(player.x)
        y = int(player.y)
        w = int(player.width)
        h = int(player.height)

        points = [
            (x + w // 2, y),
            (x + w, y + h),
            (x + int(w * 0.68), y + int(h * 0.78)),
            (x + int(w * 0.32), y + int(h * 0.78)),
            (x, y + h),
        ]
        pygame.draw.polygon(self.screen, PLAYER_COLOR, points)
        pygame.draw.polygon(self.screen, TEXT, points, width=1)

    def draw_alien(self, alien: Alien) -> None:
        pygame = self.pygame
        color = ALIEN_COLOR if alien.row % 2 == 0 else ALIEN_ALT_COLOR
        x = int(alien.x)
        y = int(alien.y)
        w = int(alien.width)
        h = int(alien.height)

        pygame.draw.rect(self.screen, color, (x, y + 4, w, h - 4), border_radius=7)
        pygame.draw.circle(self.screen, BACKGROUND, (x + int(w * 0.32), y + int(h * 0.45)), 3)
        pygame.draw.circle(self.screen, BACKGROUND, (x + int(w * 0.68), y + int(h * 0.45)), 3)
        pygame.draw.line(self.screen, TEXT, (x + 4, y + h), (x + 12, y + h + 6), 2)
        pygame.draw.line(self.screen, TEXT, (x + w - 4, y + h), (x + w - 12, y + h + 6), 2)

    def draw_bullet(self, bullet: Bullet) -> None:
        pygame = self.pygame
        color = BULLET_COLOR if bullet.owner == "player" else ENEMY_BULLET_COLOR
        pygame.draw.rect(
            self.screen,
            color,
            (int(bullet.x), int(bullet.y), int(bullet.width), int(bullet.height)),
            border_radius=3,
        )

    def draw_background(self) -> None:
        pygame = self.pygame
        self.screen.fill(BACKGROUND)

        for index in range(70):
            x = (index * 97 + self.game.frame * 1.3) % SCREEN_WIDTH
            y = (index * 53) % WORLD_HEIGHT
            brightness = 80 + int(math.sin(index + self.game.frame * 0.02) * 40)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 1)

    def draw_panel(self) -> None:
        pygame = self.pygame
        pygame.draw.rect(self.screen, PANEL, (0, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - WORLD_HEIGHT))

        items = [
            f"Score {self.game.score}",
            f"High {self.highscore}",
            f"Lives {self.game.player.lives}",
            f"Level {self.game.level}",
            f"Aliens {len(self.game.live_aliens())}",
        ]

        x = 18
        for item in items:
            rendered = self.font.render(item, True, TEXT)
            self.screen.blit(rendered, (x, WORLD_HEIGHT + 18))
            x += rendered.get_width() + 28

        controls = "←/→ or A/D move | Space fire | P pause | R reset | Q/Esc quit"
        rendered = self.font.render(controls, True, MUTED)
        self.screen.blit(rendered, (18, WORLD_HEIGHT + 54))

    def draw_overlay(self) -> None:
        if not self.game.game_over and not self.game.paused:
            return

        pygame = self.pygame
        overlay = pygame.Surface((SCREEN_WIDTH, WORLD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        message = "GAME OVER" if self.game.game_over else "PAUSED"
        sub = "Press R to reset" if self.game.game_over else "Press P to resume"

        rendered = self.big.render(message, True, TEXT)
        self.screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, WORLD_HEIGHT // 2 - 42))
        rendered_sub = self.font.render(sub, True, MUTED)
        self.screen.blit(rendered_sub, (SCREEN_WIDTH // 2 - rendered_sub.get_width() // 2, WORLD_HEIGHT // 2 + 8))

    def draw(self) -> None:
        self.draw_background()

        for alien in self.game.live_aliens():
            self.draw_alien(alien)

        for bullet in self.game.player_bullets:
            self.draw_bullet(bullet)

        for bullet in self.game.alien_bullets:
            self.draw_bullet(bullet)

        self.draw_player()
        self.draw_panel()
        self.draw_overlay()

        self.pygame.display.flip()

    def run(self) -> None:
        pygame = self.pygame

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event.key)

            self.update()
            self.draw()

        pygame.quit()


def run_app() -> None:
    SpaceInvadersPygameApp().run()
