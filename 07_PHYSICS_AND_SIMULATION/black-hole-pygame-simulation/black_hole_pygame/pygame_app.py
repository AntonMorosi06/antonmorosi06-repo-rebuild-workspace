from __future__ import annotations

from pathlib import Path
import time

from .config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, SPAWN_MODES
from .rendering import Renderer
from .simulation import BlackHoleSimulation


class BlackHolePygameApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("Black Hole Pygame Simulation - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.renderer = Renderer(pygame, self.screen, self.font, self.small_font)
        self.simulation = BlackHoleSimulation(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, seed=None)
        self.running = True
        self.show_trails = True
        self.show_jets = True
        self.debug = True
        self.fullscreen = False

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"black_hole_simulation_{stamp}.png"
        self.pygame.image.save(self.screen, str(path))
        print("[OK] Screenshot saved:", path)

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        flags = self.pygame.FULLSCREEN if self.fullscreen else self.pygame.RESIZABLE
        self.screen = self.pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        self.renderer = Renderer(self.pygame, self.screen, self.font, self.small_font)

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_SPACE:
            self.simulation.paused = not self.simulation.paused
        elif key == pygame.K_r:
            self.simulation.reset()
        elif key == pygame.K_t:
            self.show_trails = not self.show_trails
        elif key == pygame.K_j:
            self.show_jets = not self.show_jets
        elif key == pygame.K_d:
            self.debug = not self.debug
        elif key == pygame.K_s:
            self.save_screenshot()
        elif key == pygame.K_f:
            self.toggle_fullscreen()
        elif key == pygame.K_b:
            self.simulation.burst()
        elif key in (pygame.K_1, pygame.K_KP1):
            self.simulation.cycle_spawn_mode("edge")
        elif key in (pygame.K_2, pygame.K_KP2):
            self.simulation.cycle_spawn_mode("disk")
        elif key in (pygame.K_3, pygame.K_KP3):
            self.simulation.cycle_spawn_mode("spiral")
        elif key in (pygame.K_4, pygame.K_KP4):
            self.simulation.cycle_spawn_mode("rain")
        elif key in (pygame.K_5, pygame.K_KP5):
            self.simulation.cycle_spawn_mode("cluster")

    def run(self) -> None:
        pygame = self.pygame

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.simulation.update(dt)
            self.renderer.draw(self.simulation, self.show_trails, self.show_jets, self.debug)
            pygame.display.flip()

        pygame.quit()


def run_app() -> None:
    BlackHolePygameApp().run()
