from __future__ import annotations

from pathlib import Path
import time

import pygame

from .obstacle import default_obstacle, random_obstacle
from .population import Population


WIDTH = 1220
HEIGHT = 780
SIDE_PANEL_WIDTH = 340
CANVAS_WIDTH = WIDTH - SIDE_PANEL_WIDTH
FPS = 60

BACKGROUND = (13, 18, 28)
GRID = (31, 40, 56)
PANEL = (18, 25, 38)
TEXT = (232, 238, 248)
MUTED = (150, 164, 184)
ACCENT = (90, 168, 255)
TARGET = (120, 255, 170)
TARGET_RING = (220, 255, 235)

POPULATION_SIZE = 170
LIFESPAN = 320
MAX_FORCE = 0.34
INITIAL_MUTATION_RATE = 0.012
TARGET_RADIUS = 18


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Genetic Rockets Simulation - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 13)

        self.target = pygame.Vector2(CANVAS_WIDTH // 2, 90)
        self.start_position = (CANVAS_WIDTH // 2, HEIGHT - 70)
        self.bounds = pygame.Rect(0, 0, CANVAS_WIDTH, HEIGHT)
        self.obstacles = [default_obstacle(CANVAS_WIDTH, HEIGHT)]

        self.population = Population(
            size=POPULATION_SIZE,
            lifespan=LIFESPAN,
            max_force=MAX_FORCE,
            start_position=self.start_position,
            mutation_rate=INITIAL_MUTATION_RATE,
        )

        self.step = 0
        self.paused = False
        self.show_help = True
        self.running = True
        self.screenshot_message_until = 0.0
        self.last_screenshot_path = ""

    def reset_population(self) -> None:
        self.population.reset()
        self.step = 0

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"genetic_rockets_{stamp}.png"
        pygame.image.save(self.screen, str(path))
        self.last_screenshot_path = str(path)
        self.screenshot_message_until = time.time() + 2.2

    def handle_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.running = False

        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused

        elif event.key == pygame.K_r:
            self.reset_population()

        elif event.key == pygame.K_h:
            self.show_help = not self.show_help

        elif event.key == pygame.K_s:
            self.save_screenshot()

        elif event.key == pygame.K_o:
            self.obstacles = [random_obstacle(CANVAS_WIDTH, HEIGHT)]
            self.reset_population()

        elif event.key == pygame.K_c:
            self.obstacles = [default_obstacle(CANVAS_WIDTH, HEIGHT)]
            self.reset_population()

        elif event.key == pygame.K_UP:
            self.population.mutation_rate = min(0.20, self.population.mutation_rate + 0.002)

        elif event.key == pygame.K_DOWN:
            self.population.mutation_rate = max(0.0, self.population.mutation_rate - 0.002)

    def update(self) -> None:
        if self.paused:
            return

        self.population.update(
            step=self.step,
            target=self.target,
            target_radius=TARGET_RADIUS,
            obstacles=self.obstacles,
            bounds=self.bounds,
        )
        self.step += 1

        if self.step >= self.population.lifespan:
            self.population.evaluate(self.target)
            self.population.evolve()
            self.step = 0

    def draw_text(self, text: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen_font = font or self.small
        rendered = chosen_font.render(text, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_grid(self) -> None:
        for x in range(0, CANVAS_WIDTH, 40):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(self.screen, GRID, (0, y), (CANVAS_WIDTH, y), 1)

    def draw_target(self) -> None:
        pygame.draw.circle(self.screen, TARGET, (int(self.target.x), int(self.target.y)), TARGET_RADIUS)
        pygame.draw.circle(self.screen, TARGET_RING, (int(self.target.x), int(self.target.y)), TARGET_RADIUS + 8, 2)
        self.draw_text("TARGET", int(self.target.x) - 28, int(self.target.y) - 42, TARGET, self.tiny)

    def draw_start_pad(self) -> None:
        x, y = int(self.start_position[0]), int(self.start_position[1])
        pygame.draw.circle(self.screen, (90, 168, 255), (x, y), 12)
        pygame.draw.circle(self.screen, (210, 230, 255), (x, y), 18, 2)
        self.draw_text("LAUNCH", x - 30, y + 22, MUTED, self.tiny)

    def draw_panel(self) -> None:
        panel_x = CANVAS_WIDTH
        pygame.draw.rect(self.screen, PANEL, (panel_x, 0, SIDE_PANEL_WIDTH, HEIGHT))

        x = panel_x + 22
        y = 24

        self.draw_text("Genetic Rockets", x, y, TEXT, self.font)
        y += 34
        self.draw_text("Reconstructed GA simulation", x, y, MUTED, self.small)
        y += 34

        stats = self.population.last_stats
        progress = self.step / max(1, self.population.lifespan)

        lines = [
            f"Generation: {self.population.generation}",
            f"Step: {self.step} / {self.population.lifespan}",
            f"Progress: {progress * 100:.1f}%",
            f"Population: {self.population.size}",
            f"Mutation rate: {self.population.mutation_rate:.3f}",
            f"Best fitness: {stats.best_fitness:.2f}",
            f"Avg fitness: {stats.average_fitness:.2f}",
            f"Completed last gen: {stats.completed_count}",
            f"Crashed last gen: {stats.crashed_count}",
            f"Best distance: {stats.best_distance:.1f}",
            f"Paused: {'yes' if self.paused else 'no'}",
        ]

        for line in lines:
            self.draw_text(line, x, y, TEXT, self.small)
            y += 24

        y += 12
        self.draw_text("Controls", x, y, ACCENT, self.small)
        y += 26

        controls = [
            "Space: pause/resume",
            "R: reset population",
            "O: random obstacle",
            "C: default obstacle",
            "Up/Down: mutation rate",
            "S: save screenshot",
            "H: toggle help",
            "Esc: quit",
        ]

        for line in controls:
            self.draw_text(line, x, y, MUTED, self.small)
            y += 22

        y += 14
        self.draw_text("Model note", x, y, ACCENT, self.small)
        y += 26

        note = [
            "Each rocket has DNA made",
            "of force vectors. Better",
            "trajectories are selected,",
            "crossed and mutated across",
            "generations.",
        ]

        for line in note:
            self.draw_text(line, x, y, MUTED, self.small)
            y += 22

        if time.time() < self.screenshot_message_until:
            y = HEIGHT - 70
            self.draw_text("Screenshot saved:", x, y, ACCENT, self.small)
            y += 22
            self.draw_text(Path(self.last_screenshot_path).name, x, y, TEXT, self.small)

    def draw_help_overlay(self) -> None:
        if not self.show_help:
            return

        overlay = pygame.Surface((CANVAS_WIDTH - 50, 100), pygame.SRCALPHA)
        overlay.fill((10, 16, 26, 215))
        self.screen.blit(overlay, (25, 22))

        lines = [
            "Genetic algorithm: DNA vectors drive each rocket for one lifespan.",
            "At the end of a generation, fitness rewards closeness, completion and speed.",
            "Selection, crossover and mutation produce the next generation.",
            "Use Space to pause, R to reset, O to randomize the obstacle and S for screenshots.",
        ]

        y = 35
        for line in lines:
            self.draw_text(line, 42, y, TEXT, self.small)
            y += 23

    def draw(self) -> None:
        self.screen.fill(BACKGROUND)
        self.draw_grid()

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.draw_target()
        self.draw_start_pad()
        self.population.draw(self.screen)
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
