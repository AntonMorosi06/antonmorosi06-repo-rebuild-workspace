from __future__ import annotations

from pathlib import Path
import time

from .datasets import dataset_names, generate_dataset
from .dbscan import dbscan
from .metrics import normalized_bounds, result_summary
from .palette import ACCENT, BACKGROUND, BORDER_OUTLINE, CORE_OUTLINE, MUTED, PANEL, TEXT, color_for_label


WIDTH = 1240
HEIGHT = 820
PANEL_WIDTH = 330
PLOT_WIDTH = WIDTH - PANEL_WIDTH
PLOT_HEIGHT = HEIGHT


class DBSCANVisualizerApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("DBSCAN Pygame Visualizer - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 13)

        self.dataset_name = "blobs"
        self.seed = 42
        self.epsilon = 0.42
        self.min_samples = 5
        self.show_core = True
        self.show_neighborhood = True
        self.show_debug = True
        self.selected_index = 0
        self.running = True

        self.raw_points = generate_dataset(self.dataset_name, seed=self.seed)
        self.result = dbscan(self.raw_points, self.epsilon, self.min_samples)
        self.bounds = normalized_bounds(self.raw_points)

    def recluster(self) -> None:
        self.result = dbscan(self.raw_points, self.epsilon, self.min_samples)
        self.selected_index = min(self.selected_index, max(0, len(self.result.points) - 1))

    def load_dataset(self, name: str) -> None:
        self.dataset_name = name
        self.raw_points = generate_dataset(name, seed=self.seed)
        self.bounds = normalized_bounds(self.raw_points)

        defaults = {
            "blobs": (0.42, 5),
            "moons": (0.28, 5),
            "rings": (0.22, 5),
            "noise": (0.26, 6),
            "mixed": (0.30, 5),
        }
        self.epsilon, self.min_samples = defaults.get(name, (self.epsilon, self.min_samples))
        self.recluster()

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"dbscan_visualizer_{self.dataset_name}_{stamp}.png"
        self.pygame.image.save(self.screen, str(path))
        print("[OK] Screenshot saved:", path)

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_r:
            self.recluster()
        elif key == pygame.K_b:
            self.load_dataset("blobs")
        elif key == pygame.K_m:
            self.load_dataset("moons")
        elif key == pygame.K_o:
            self.load_dataset("rings")
        elif key == pygame.K_n:
            self.load_dataset("noise")
        elif key == pygame.K_x:
            self.load_dataset("mixed")
        elif key == pygame.K_UP:
            self.epsilon = min(3.0, self.epsilon + 0.02)
            self.recluster()
        elif key == pygame.K_DOWN:
            self.epsilon = max(0.04, self.epsilon - 0.02)
            self.recluster()
        elif key == pygame.K_RIGHT:
            self.min_samples = min(25, self.min_samples + 1)
            self.recluster()
        elif key == pygame.K_LEFT:
            self.min_samples = max(1, self.min_samples - 1)
            self.recluster()
        elif key == pygame.K_c:
            self.show_core = not self.show_core
        elif key == pygame.K_h:
            self.show_neighborhood = not self.show_neighborhood
        elif key == pygame.K_d:
            self.show_debug = not self.show_debug
        elif key == pygame.K_s:
            self.save_screenshot()
        elif key == pygame.K_TAB:
            self.selected_index = (self.selected_index + 1) % max(1, len(self.result.points))

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        min_x, max_x, min_y, max_y = self.bounds
        nx = (x - min_x) / max(1e-9, max_x - min_x)
        ny = (y - min_y) / max(1e-9, max_y - min_y)

        margin = 56
        sx = margin + nx * (PLOT_WIDTH - margin * 2)
        sy = margin + (1.0 - ny) * (PLOT_HEIGHT - margin * 2)
        return int(sx), int(sy)

    def epsilon_to_pixels(self) -> float:
        min_x, max_x, min_y, max_y = self.bounds
        x_scale = (PLOT_WIDTH - 112) / max(1e-9, max_x - min_x)
        y_scale = (PLOT_HEIGHT - 112) / max(1e-9, max_y - min_y)
        return self.epsilon * min(x_scale, y_scale)

    def draw_plot_background(self) -> None:
        pygame = self.pygame
        self.screen.fill(BACKGROUND)

        for x in range(0, PLOT_WIDTH, 48):
            pygame.draw.line(self.screen, (18, 26, 42), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 48):
            pygame.draw.line(self.screen, (18, 26, 42), (0, y), (PLOT_WIDTH, y), 1)

        pygame.draw.rect(self.screen, PANEL, (PLOT_WIDTH, 0, PANEL_WIDTH, HEIGHT))

    def draw_neighborhood(self) -> None:
        if not self.show_neighborhood or not self.result.points:
            return

        pygame = self.pygame
        selected = self.result.points[self.selected_index]
        sx, sy = self.world_to_screen(selected.point.x, selected.point.y)
        radius = int(self.epsilon_to_pixels())

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (90, 168, 255, 38), (sx, sy), radius)
        pygame.draw.circle(surface, (90, 168, 255, 140), (sx, sy), radius, width=2)
        self.screen.blit(surface, (0, 0))

    def draw_points(self) -> None:
        pygame = self.pygame

        for index, clustered in enumerate(self.result.points):
            sx, sy = self.world_to_screen(clustered.point.x, clustered.point.y)
            color = color_for_label(clustered.label)
            radius = 5

            if clustered.is_core:
                radius = 6
            elif clustered.is_noise:
                radius = 4

            pygame.draw.circle(self.screen, color, (sx, sy), radius)

            if self.show_core and clustered.is_core:
                pygame.draw.circle(self.screen, CORE_OUTLINE, (sx, sy), radius + 3, width=1)
            elif self.show_core and clustered.is_border:
                pygame.draw.circle(self.screen, BORDER_OUTLINE, (sx, sy), radius + 2, width=1)

            if index == self.selected_index:
                pygame.draw.circle(self.screen, (255, 255, 255), (sx, sy), radius + 8, width=2)

    def text(self, value: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen = font or self.small
        rendered = chosen.render(value, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_panel(self) -> None:
        summary = result_summary(self.result)
        x = PLOT_WIDTH + 22
        y = 24

        self.text("DBSCAN", x, y, TEXT, self.font)
        y += 34
        self.text("Density-based clustering", x, y, MUTED, self.small)
        y += 36

        lines = [
            f"Dataset: {self.dataset_name}",
            f"Points: {len(self.result.points)}",
            f"Epsilon: {self.epsilon:.2f}",
            f"Min samples: {self.min_samples}",
            f"Clusters: {summary['cluster_count']}",
            f"Noise: {summary['noise_count']}",
            f"Core: {summary['core_count']}",
            f"Border: {summary['border_count']}",
            f"Selected: {self.selected_index}",
        ]

        for line in lines:
            self.text(line, x, y, TEXT)
            y += 24

        y += 12
        self.text("Cluster sizes", x, y, ACCENT)
        y += 26

        cluster_sizes = summary["cluster_sizes"]
        if cluster_sizes:
            for cluster_id, size in list(cluster_sizes.items())[:9]:
                self.text(f"Cluster {cluster_id}: {size}", x, y, MUTED)
                y += 21
        else:
            self.text("No clusters", x, y, MUTED)
            y += 21

        y += 18
        self.text("Controls", x, y, ACCENT)
        y += 26

        controls = [
            "B blobs | M moons",
            "O rings | N noise | X mixed",
            "Up/Down epsilon",
            "Left/Right min_samples",
            "Tab select point",
            "C core overlay",
            "H neighborhood",
            "D debug",
            "S screenshot",
            "Q/Esc quit",
        ]

        for line in controls:
            self.text(line, x, y, MUTED, self.tiny)
            y += 19

    def draw_debug_footer(self) -> None:
        if not self.show_debug:
            return

        selected = self.result.points[self.selected_index] if self.result.points else None
        if not selected:
            return

        label = selected.label
        role = "core" if selected.is_core else "border" if selected.is_border else "noise" if selected.is_noise else "unclassified"
        message = (
            f"Selected point: x={selected.point.x:.3f}, y={selected.point.y:.3f}, "
            f"label={label}, role={role}, neighbors={selected.neighbor_count}"
        )

        self.text(message, 18, HEIGHT - 28, TEXT, self.tiny)

    def draw(self) -> None:
        self.draw_plot_background()
        self.draw_neighborhood()
        self.draw_points()
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

            self.draw()
            self.clock.tick(60)

        pygame.quit()


def run_app() -> None:
    DBSCANVisualizerApp().run()
