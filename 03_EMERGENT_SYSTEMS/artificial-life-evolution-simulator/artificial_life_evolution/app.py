from __future__ import annotations

from pathlib import Path
import math
import time

import pygame

from .config import (
    ACCENT,
    BACKGROUND,
    FOOD_COLOR,
    FPS,
    GRID,
    HEIGHT,
    MUTED,
    PANEL,
    PREDATOR_COLOR,
    PREY_COLOR,
    SIDE_PANEL_WIDTH,
    TEXT,
    WIDTH,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)
from .world import World


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Artificial Life Evolution Simulator - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 12)
        self.world = World()
        self.running = True
        self.paused = False
        self.show_help = True
        self.show_minimap = True
        self.show_trails = True
        self.screenshot_message_until = 0.0
        self.last_screenshot_path = ""

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"artificial_life_evolution_{stamp}.png"
        pygame.image.save(self.screen, str(path))
        self.last_screenshot_path = str(path)
        self.screenshot_message_until = time.time() + 2.2

    def mouse_world_position(self) -> tuple[int, int] | None:
        x, y = pygame.mouse.get_pos()
        if x >= WORLD_WIDTH:
            return None
        return x, y

    def handle_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.running = False

        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused

        elif event.key == pygame.K_r:
            self.world.reset()

        elif event.key == pygame.K_h:
            self.show_help = not self.show_help

        elif event.key == pygame.K_m:
            self.show_minimap = not self.show_minimap

        elif event.key == pygame.K_t:
            self.show_trails = not self.show_trails

        elif event.key == pygame.K_s:
            self.save_screenshot()

        elif event.key == pygame.K_e:
            self.world.trigger_random_event()

        elif event.key == pygame.K_f:
            position = self.mouse_world_position()
            if position:
                for _ in range(9):
                    self.world.add_food_at(position[0], position[1])

        elif event.key == pygame.K_p:
            position = self.mouse_world_position()
            if position:
                self.world.add_creature_at(position[0], position[1], predator=False)

        elif event.key == pygame.K_x:
            position = self.mouse_world_position()
            if position:
                self.world.add_creature_at(position[0], position[1], predator=True)

    def update(self) -> None:
        if not self.paused:
            self.world.update()

    def draw_text(self, text: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen_font = font or self.small
        rendered = chosen_font.render(text, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_grid(self) -> None:
        for x in range(0, WORLD_WIDTH, 40):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, WORLD_HEIGHT), 1)
        for y in range(0, WORLD_HEIGHT, 40):
            pygame.draw.line(self.screen, GRID, (0, y), (WORLD_WIDTH, y), 1)

    def draw_day_night_overlay(self) -> None:
        phase = self.world.day_phase
        darkness = 0.5 - 0.5 * math.sin(phase * math.tau)
        alpha = int(18 + darkness * 85)
        overlay = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 8, 24, alpha))
        self.screen.blit(overlay, (0, 0))

    def draw_panel(self) -> None:
        panel_x = WORLD_WIDTH
        pygame.draw.rect(self.screen, PANEL, (panel_x, 0, SIDE_PANEL_WIDTH, HEIGHT))

        stats = self.world.stats()
        x = panel_x + 22
        y = 24

        self.draw_text("Artificial Life", x, y, TEXT, self.font)
        y += 34
        self.draw_text("Evolution ecosystem simulator", x, y, MUTED, self.small)
        y += 34

        lines = [
            f"Tick: {self.world.tick}",
            f"Season: {stats.season}",
            f"Day phase: {stats.day_phase:.2f}",
            f"Event: {stats.event_name}",
            f"Prey: {stats.prey_count}",
            f"Predators: {stats.predator_count}",
            f"Food: {stats.food_count}",
            f"Births: {stats.births}",
            f"Deaths: {stats.deaths}",
            f"Avg generation: {stats.avg_generation:.2f}",
            f"Avg prey speed: {stats.avg_prey_speed:.2f}",
            f"Avg prey vision: {stats.avg_prey_vision:.1f}",
            f"Avg predator speed: {stats.avg_predator_speed:.2f}",
            f"Paused: {'yes' if self.paused else 'no'}",
        ]

        for line in lines:
            self.draw_text(line, x, y, TEXT, self.small)
            y += 23

        y += 12
        self.draw_text("Controls", x, y, ACCENT, self.small)
        y += 26

        controls = [
            "Space: pause/resume",
            "R: reset ecosystem",
            "F: add food at mouse",
            "P: add prey at mouse",
            "X: add predator at mouse",
            "E: random event",
            "M: toggle minimap",
            "T: toggle trails",
            "S: save screenshot",
            "H: toggle help",
            "Esc: quit",
        ]

        for line in controls:
            self.draw_text(line, x, y, MUTED, self.small)
            y += 20

        if time.time() < self.screenshot_message_until:
            y = HEIGHT - 70
            self.draw_text("Screenshot saved:", x, y, ACCENT, self.small)
            y += 22
            self.draw_text(Path(self.last_screenshot_path).name, x, y, TEXT, self.small)

    def draw_help_overlay(self) -> None:
        if not self.show_help:
            return

        overlay = pygame.Surface((WORLD_WIDTH - 50, 106), pygame.SRCALPHA)
        overlay.fill((10, 16, 26, 218))
        self.screen.blit(overlay, (25, 22))

        lines = [
            "Artificial life: creatures search, flee, hunt, eat, reproduce, mutate and die.",
            "DNA controls speed, vision, aggression, sociability, fertility, metabolism, nocturnality and longevity.",
            "The world includes food, predators, prey, day/night, seasons and random environmental events.",
            "Use F/P/X at the mouse position to inject food, prey or predators into the ecosystem.",
        ]

        y = 35
        for line in lines:
            self.draw_text(line, 42, y, TEXT, self.small)
            y += 23

    def draw_minimap(self) -> None:
        if not self.show_minimap:
            return

        map_w = 150
        map_h = 118
        x0 = WORLD_WIDTH - map_w - 18
        y0 = HEIGHT - map_h - 18

        pygame.draw.rect(self.screen, (10, 16, 26), (x0, y0, map_w, map_h), border_radius=8)
        pygame.draw.rect(self.screen, (80, 98, 130), (x0, y0, map_w, map_h), width=1, border_radius=8)

        sx = map_w / WORLD_WIDTH
        sy = map_h / WORLD_HEIGHT

        for food in self.world.foods[::4]:
            x = int(x0 + food.position.x * sx)
            y = int(y0 + food.position.y * sy)
            pygame.draw.circle(self.screen, FOOD_COLOR, (x, y), 1)

        for creature in self.world.creatures:
            x = int(x0 + creature.position.x * sx)
            y = int(y0 + creature.position.y * sy)
            color = PREDATOR_COLOR if creature.predator else PREY_COLOR
            pygame.draw.circle(self.screen, color, (x, y), 2)

        self.draw_text("minimap", x0 + 8, y0 + 7, MUTED, self.tiny)

    def draw_legend(self) -> None:
        x = 24
        y = HEIGHT - 32
        items = [
            ("prey", PREY_COLOR),
            ("predator", PREDATOR_COLOR),
            ("food", FOOD_COLOR),
        ]

        for label, color in items:
            pygame.draw.circle(self.screen, color, (x, y), 6)
            self.draw_text(label, x + 12, y - 7, MUTED, self.tiny)
            x += 90

    def draw(self) -> None:
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        self.world.draw(self.screen, show_trails=self.show_trails)
        self.draw_day_night_overlay()
        self.draw_minimap()
        self.draw_legend()
        self.draw_help_overlay()
        self.draw_panel()
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


def run_app() -> None:
    App().run()
