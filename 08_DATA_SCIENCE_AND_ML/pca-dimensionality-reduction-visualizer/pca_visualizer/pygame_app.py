from __future__ import annotations

from pathlib import Path
import time

from .datasets import generate_dataset
from .metrics import bounds_2d, pca_summary, reconstruction_mse
from .palette import AXIS_1, AXIS_2, BACKGROUND, GRID, MUTED, PANEL, POINT, POINT_ALT, PROJECTION, RECONSTRUCTION, TEXT
from .pca import fit_pca


WIDTH = 1280
HEIGHT = 820
PANEL_WIDTH = 360
PLOT_WIDTH = WIDTH - PANEL_WIDTH


class PCAVisualizerApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("PCA Dimensionality Reduction Visualizer - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 13)

        self.dataset_name = "correlated"
        self.seed = 42
        self.n_components = 1
        self.show_centered = False
        self.show_projected = True
        self.show_vectors = True
        self.show_debug = True
        self.running = True

        self.raw_data = generate_dataset(self.dataset_name, seed=self.seed)
        self.result = fit_pca(self.raw_data, n_components=self.n_components)
        self.bounds = self.current_bounds()

    def current_points_for_plot(self):
        if self.show_projected:
            return self.projected_points_2d()
        if self.show_centered:
            return self.centered_points_2d()
        return self.raw_points_2d()

    def raw_points_2d(self):
        return [[row[0], row[1] if len(row) > 1 else 0.0] for row in self.raw_data]

    def centered_points_2d(self):
        return [[row[0], row[1] if len(row) > 1 else 0.0] for row in self.result.centered]

    def projected_points_2d(self):
        points = []
        for row in self.result.transformed:
            x = row[0] if len(row) >= 1 else 0.0
            y = row[1] if len(row) >= 2 else 0.0
            points.append([x, y])
        return points

    def current_bounds(self):
        return bounds_2d(self.current_points_for_plot())

    def recompute(self) -> None:
        dimension = len(self.raw_data[0])
        self.n_components = max(1, min(dimension, self.n_components))
        self.result = fit_pca(self.raw_data, n_components=self.n_components)
        self.bounds = self.current_bounds()

    def load_dataset(self, name: str) -> None:
        self.dataset_name = name
        self.raw_data = generate_dataset(name, seed=self.seed)
        dimension = len(self.raw_data[0])
        self.n_components = 1 if dimension == 2 else 2
        self.recompute()

    def regenerate(self) -> None:
        self.seed += 1
        self.raw_data = generate_dataset(self.dataset_name, seed=self.seed)
        self.recompute()

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"pca_visualizer_{self.dataset_name}_{stamp}.png"
        self.pygame.image.save(self.screen, str(path))
        print("[OK] Screenshot saved:", path)

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_r:
            self.regenerate()
        elif key == pygame.K_c:
            self.show_centered = not self.show_centered
            if self.show_centered:
                self.show_projected = False
            self.bounds = self.current_bounds()
        elif key == pygame.K_p:
            self.show_projected = not self.show_projected
            if self.show_projected:
                self.show_centered = False
            self.bounds = self.current_bounds()
        elif key == pygame.K_v:
            self.show_vectors = not self.show_vectors
        elif key == pygame.K_d:
            self.show_debug = not self.show_debug
        elif key == pygame.K_s:
            self.save_screenshot()
        elif key == pygame.K_UP:
            self.n_components += 1
            self.recompute()
        elif key == pygame.K_DOWN:
            self.n_components -= 1
            self.recompute()
        elif key == pygame.K_1:
            self.load_dataset("correlated")
        elif key == pygame.K_2:
            self.load_dataset("ellipse")
        elif key == pygame.K_3:
            self.load_dataset("clusters")
        elif key == pygame.K_4:
            self.load_dataset("ribbon3d")
        elif key == pygame.K_5:
            self.load_dataset("line")

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        min_x, max_x, min_y, max_y = self.bounds
        nx = (x - min_x) / max(1e-9, max_x - min_x)
        ny = (y - min_y) / max(1e-9, max_y - min_y)

        margin = 58
        sx = margin + nx * (PLOT_WIDTH - margin * 2)
        sy = margin + (1.0 - ny) * (HEIGHT - margin * 2)
        return int(sx), int(sy)

    def draw_background(self) -> None:
        pygame = self.pygame
        self.screen.fill(BACKGROUND)
        pygame.draw.rect(self.screen, PANEL, (PLOT_WIDTH, 0, PANEL_WIDTH, HEIGHT))

        for x in range(0, PLOT_WIDTH, 48):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 48):
            pygame.draw.line(self.screen, GRID, (0, y), (PLOT_WIDTH, y), 1)

        if not self.show_projected:
            zero = self.world_to_screen(0.0, 0.0)
            pygame.draw.line(self.screen, (42, 54, 74), (0, zero[1]), (PLOT_WIDTH, zero[1]), 1)
            pygame.draw.line(self.screen, (42, 54, 74), (zero[0], 0), (zero[0], HEIGHT), 1)

    def draw_points(self) -> None:
        pygame = self.pygame
        points = self.current_points_for_plot()

        color = PROJECTION if self.show_projected else POINT_ALT if self.show_centered else POINT

        for row in points:
            sx, sy = self.world_to_screen(row[0], row[1])
            pygame.draw.circle(self.screen, color, (sx, sy), 4)

        if self.show_projected and self.n_components == 1:
            for row in points:
                sx, sy = self.world_to_screen(row[0], 0.0)
                pygame.draw.circle(self.screen, PROJECTION, (sx, sy), 4)

    def draw_principal_vectors(self) -> None:
        if not self.show_vectors or self.show_projected:
            return

        pygame = self.pygame
        mean = [0.0, 0.0] if self.show_centered else [self.result.mean[0], self.result.mean[1] if len(self.result.mean) > 1 else 0.0]
        origin = self.world_to_screen(mean[0], mean[1])
        scale = 1.8

        colors = [AXIS_1, AXIS_2]

        for index, component in enumerate(self.result.components[:2]):
            value = self.result.eigenvalues[index] if index < len(self.result.eigenvalues) else 1.0
            length = max(0.8, abs(value) ** 0.5) * scale
            dx = component[0] * length
            dy = component[1] * length if len(component) > 1 else 0.0

            end_a = self.world_to_screen(mean[0] + dx, mean[1] + dy)
            end_b = self.world_to_screen(mean[0] - dx, mean[1] - dy)

            pygame.draw.line(self.screen, colors[index], end_b, end_a, 4)
            pygame.draw.circle(self.screen, colors[index], end_a, 7)

    def text(self, value: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen = font or self.small
        rendered = chosen.render(value, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_panel(self) -> None:
        summary = pca_summary(self.result)
        mse = reconstruction_mse(self.raw_data, self.result.reconstructed)

        x = PLOT_WIDTH + 22
        y = 24

        self.text("PCA Visualizer", x, y, TEXT, self.font)
        y += 34
        self.text("Principal Component Analysis", x, y, MUTED)
        y += 36

        mode = "projected" if self.show_projected else "centered" if self.show_centered else "original"
        dimension = len(self.raw_data[0])

        lines = [
            f"Dataset: {self.dataset_name}",
            f"Samples: {len(self.raw_data)}",
            f"Dimension: {dimension}",
            f"View: {mode}",
            f"Components: {self.n_components}",
            f"Retained variance: {summary['retained_variance_ratio']:.3f}",
            f"Reconstruction MSE: {mse:.5f}",
            f"Seed: {self.seed}",
        ]

        for line in lines:
            self.text(line, x, y, TEXT)
            y += 24

        y += 12
        self.text("Explained variance", x, y, AXIS_1)
        y += 26

        for index, ratio in enumerate(self.result.explained_variance_ratio[:5]):
            self.text(f"PC{index + 1}: {ratio:.4f}", x, y, MUTED)
            y += 21

        y += 18
        self.text("Eigenvalues", x, y, AXIS_2)
        y += 26

        for index, value in enumerate(self.result.eigenvalues[:5]):
            self.text(f"λ{index + 1}: {value:.4f}", x, y, MUTED)
            y += 21

        y += 18
        self.text("Controls", x, y, AXIS_1)
        y += 26

        controls = [
            "1 correlated cloud",
            "2 ellipse",
            "3 rotated clusters",
            "4 3D ribbon",
            "5 noisy line",
            "Up/Down components",
            "C centered view",
            "P projected view",
            "V principal vectors",
            "R regenerate",
            "S screenshot",
            "Q/Esc quit",
        ]

        for line in controls:
            self.text(line, x, y, MUTED, self.tiny)
            y += 18

    def draw_debug_footer(self) -> None:
        if not self.show_debug:
            return

        message = (
            f"Mean: {', '.join(f'{v:.3f}' for v in self.result.mean)} | "
            f"Components shown: {self.n_components} | "
            f"View: {'projected' if self.show_projected else 'centered' if self.show_centered else 'original'}"
        )
        self.text(message, 18, HEIGHT - 28, TEXT, self.tiny)

    def draw(self) -> None:
        self.draw_background()
        self.draw_points()
        self.draw_principal_vectors()
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
    PCAVisualizerApp().run()
