from __future__ import annotations

from pathlib import Path
import time

from .ga import GeneticAlgorithm
from .landscapes import landscape_names
from .palette import BACKGROUND, BEST, DANGER, GRID, HIGH, LOW, MID, MUTED, PANEL, TEXT, TRAIL


WIDTH = 1280
HEIGHT = 820
PANEL_WIDTH = 370
PLOT_WIDTH = WIDTH - PANEL_WIDTH


class GeneticAlgorithmVisualizerApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("Genetic Algorithm Optimizer Visualizer - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 13)

        self.ga = GeneticAlgorithm(landscape_name="sphere", seed=42)
        self.running = True
        self.paused = False
        self.show_trails = True
        self.show_debug = True
        self.trails: list[list[tuple[float, float]]] = []
        self.cached_field = None
        self.cached_landscape_name = None

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"genetic_algorithm_{self.ga.landscape_name}_{stamp}.png"
        self.pygame.image.save(self.screen, str(path))
        print("[OK] Screenshot saved:", path)

    def reset(self) -> None:
        self.ga.reset()
        self.trails.clear()
        self.cached_field = None
        self.cached_landscape_name = None

    def set_landscape_by_index(self, index: int) -> None:
        names = ["sphere", "rastrigin", "himmelblau", "ridge", "multi_peak"]
        if 0 <= index < len(names):
            self.ga.set_landscape(names[index])
            self.trails.clear()
            self.cached_field = None
            self.cached_landscape_name = None

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_n:
            self.ga.step()
            self.update_trails()
        elif key == pygame.K_r:
            self.reset()
        elif key == pygame.K_1:
            self.set_landscape_by_index(0)
        elif key == pygame.K_2:
            self.set_landscape_by_index(1)
        elif key == pygame.K_3:
            self.set_landscape_by_index(2)
        elif key == pygame.K_4:
            self.set_landscape_by_index(3)
        elif key == pygame.K_5:
            self.set_landscape_by_index(4)
        elif key == pygame.K_UP:
            self.ga.config.mutation_rate = min(0.95, self.ga.config.mutation_rate + 0.02)
        elif key == pygame.K_DOWN:
            self.ga.config.mutation_rate = max(0.0, self.ga.config.mutation_rate - 0.02)
        elif key == pygame.K_RIGHT:
            self.ga.config.crossover_rate = min(1.0, self.ga.config.crossover_rate + 0.03)
        elif key == pygame.K_LEFT:
            self.ga.config.crossover_rate = max(0.0, self.ga.config.crossover_rate - 0.03)
        elif key == pygame.K_e:
            self.ga.config.elite_count = 0 if self.ga.config.elite_count >= 5 else self.ga.config.elite_count + 1
        elif key == pygame.K_t:
            self.show_trails = not self.show_trails
        elif key == pygame.K_d:
            self.show_debug = not self.show_debug
        elif key == pygame.K_s:
            self.save_screenshot()

    def update_trails(self) -> None:
        points = [(individual.x, individual.y) for individual in self.ga.population]
        self.trails.append(points)
        if len(self.trails) > 60:
            self.trails.pop(0)

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        low, high = self.ga.landscape.bounds
        nx = (x - low) / max(1e-9, high - low)
        ny = (y - low) / max(1e-9, high - low)
        margin = 58
        sx = margin + nx * (PLOT_WIDTH - margin * 2)
        sy = margin + (1.0 - ny) * (HEIGHT - margin * 2)
        return int(sx), int(sy)

    def screen_to_world(self, sx: int, sy: int) -> tuple[float, float]:
        low, high = self.ga.landscape.bounds
        margin = 58
        nx = (sx - margin) / max(1e-9, PLOT_WIDTH - margin * 2)
        ny = 1.0 - ((sy - margin) / max(1e-9, HEIGHT - margin * 2))
        return low + nx * (high - low), low + ny * (high - low)

    def fitness_color(self, value: float, min_value: float, max_value: float) -> tuple[int, int, int]:
        t = 0.0 if max_value <= min_value else (value - min_value) / (max_value - min_value)
        if t < 0.5:
            k = t / 0.5
            return (
                int(LOW[0] + (MID[0] - LOW[0]) * k),
                int(LOW[1] + (MID[1] - LOW[1]) * k),
                int(LOW[2] + (MID[2] - LOW[2]) * k),
            )
        k = (t - 0.5) / 0.5
        return (
            int(MID[0] + (HIGH[0] - MID[0]) * k),
            int(MID[1] + (HIGH[1] - MID[1]) * k),
            int(MID[2] + (HIGH[2] - MID[2]) * k),
        )

    def build_field_cache(self):
        pygame = self.pygame
        surface = pygame.Surface((PLOT_WIDTH, HEIGHT))
        step = 10
        values = []

        for y in range(0, HEIGHT, step):
            for x in range(0, PLOT_WIDTH, step):
                wx, wy = self.screen_to_world(x + step // 2, y + step // 2)
                values.append(self.ga.landscape.fitness([wx, wy]))

        min_value = min(values)
        max_value = max(values)
        index = 0

        for y in range(0, HEIGHT, step):
            for x in range(0, PLOT_WIDTH, step):
                color = self.fitness_color(values[index], min_value, max_value)
                pygame.draw.rect(surface, color, (x, y, step + 1, step + 1))
                index += 1

        self.cached_field = surface
        self.cached_landscape_name = self.ga.landscape_name

    def draw_background(self) -> None:
        pygame = self.pygame

        if self.cached_field is None or self.cached_landscape_name != self.ga.landscape_name:
            self.build_field_cache()

        self.screen.blit(self.cached_field, (0, 0))
        overlay = pygame.Surface((PLOT_WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 13, 22, 92))
        self.screen.blit(overlay, (0, 0))

        for x in range(0, PLOT_WIDTH, 48):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 48):
            pygame.draw.line(self.screen, GRID, (0, y), (PLOT_WIDTH, y), 1)

        pygame.draw.rect(self.screen, PANEL, (PLOT_WIDTH, 0, PANEL_WIDTH, HEIGHT))

    def draw_trails(self) -> None:
        if not self.show_trails:
            return

        pygame = self.pygame
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for age, generation_points in enumerate(self.trails):
            alpha = int(16 + 88 * (age + 1) / max(1, len(self.trails)))
            for x, y in generation_points:
                sx, sy = self.world_to_screen(x, y)
                pygame.draw.circle(surface, (*TRAIL, alpha), (sx, sy), 2)

        self.screen.blit(surface, (0, 0))

    def draw_population(self) -> None:
        pygame = self.pygame
        best = self.ga.best()

        for individual in self.ga.population:
            sx, sy = self.world_to_screen(individual.x, individual.y)
            pygame.draw.circle(self.screen, (237, 243, 255), (sx, sy), 4)
            pygame.draw.circle(self.screen, MID, (sx, sy), 3)

        bx, by = self.world_to_screen(best.x, best.y)
        pygame.draw.circle(self.screen, BEST, (bx, by), 10)
        pygame.draw.circle(self.screen, (255, 255, 255), (bx, by), 12, width=2)

        ox, oy = self.ga.landscape.optimum_hint
        osx, osy = self.world_to_screen(ox, oy)
        pygame.draw.circle(self.screen, DANGER, (osx, osy), 8, width=2)

    def draw_history_chart(self, x: int, y: int, width: int, height: int) -> None:
        pygame = self.pygame
        history = self.ga.history[-90:]
        if len(history) < 2:
            return

        values = [entry.best_fitness for entry in history]
        min_v = min(values)
        max_v = max(values)

        pygame.draw.rect(self.screen, (8, 13, 22), (x, y, width, height), border_radius=8)
        pygame.draw.rect(self.screen, GRID, (x, y, width, height), width=1, border_radius=8)

        points = []
        for index, value in enumerate(values):
            nx = index / max(1, len(values) - 1)
            ny = 0.5 if max_v <= min_v else (value - min_v) / (max_v - min_v)
            points.append((int(x + nx * width), int(y + height - ny * height)))

        if len(points) >= 2:
            pygame.draw.lines(self.screen, BEST, False, points, 2)

    def text(self, value: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen = font or self.small
        rendered = chosen.render(value, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_panel(self) -> None:
        summary = self.ga.summary()
        x = PLOT_WIDTH + 22
        y = 24

        self.text("Genetic Algorithm", x, y, TEXT, self.font)
        y += 34
        self.text("Real-valued optimizer", x, y, MUTED)
        y += 36

        lines = [
            f"Landscape: {summary['landscape']}",
            f"Generation: {summary['generation']}",
            f"Population: {summary['population_size']}",
            f"Best fitness: {summary['best_fitness']:.5f}",
            f"Best x: {summary['best_x']:.3f}",
            f"Best y: {summary['best_y']:.3f}",
            f"Mean fitness: {summary['mean_fitness']:.5f}",
            f"Diversity: {summary['diversity']:.4f}",
            f"Mutation: {summary['mutation_rate']:.2f}",
            f"Crossover: {summary['crossover_rate']:.2f}",
            f"Elite count: {summary['elite_count']}",
            f"State: {'paused' if self.paused else 'running'}",
        ]

        for line in lines:
            self.text(line, x, y, TEXT)
            y += 23

        y += 12
        self.text("Best fitness history", x, y, HIGH)
        y += 25
        self.draw_history_chart(x, y, PANEL_WIDTH - 44, 90)
        y += 112

        self.text("Controls", x, y, HIGH)
        y += 25

        controls = [
            "Space pause/resume",
            "N step one generation",
            "R reset population",
            "1 sphere",
            "2 rastrigin",
            "3 himmelblau",
            "4 ridge",
            "5 multi-peak",
            "Up/Down mutation",
            "Left/Right crossover",
            "E elitism level",
            "T trails",
            "S screenshot",
            "Q/Esc quit",
        ]

        for line in controls:
            self.text(line, x, y, MUTED, self.tiny)
            y += 17

    def draw_debug_footer(self) -> None:
        if not self.show_debug:
            return

        message = (
            f"GA pipeline: evaluate -> tournament selection -> blend crossover -> Gaussian mutation -> elitism | "
            f"{self.ga.landscape.description}"
        )
        self.text(message, 18, HEIGHT - 28, TEXT, self.tiny)

    def draw(self) -> None:
        self.draw_background()
        self.draw_trails()
        self.draw_population()
        self.draw_panel()
        self.draw_debug_footer()
        self.pygame.display.flip()

    def run(self) -> None:
        pygame = self.pygame

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            if not self.paused:
                self.ga.step()
                self.update_trails()

            self.draw()
            self.clock.tick(30)

        pygame.quit()


def run_app() -> None:
    GeneticAlgorithmVisualizerApp().run()
