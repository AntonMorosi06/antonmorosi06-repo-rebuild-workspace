from __future__ import annotations

from pathlib import Path
import time

from .datasets import generate_dataset
from .metrics import bounds_2d, result_summary
from .palette import ACCENT, BACKGROUND, EDGE, GRID, MUTED, PANEL, TEXT, color_for_label
from .spectral import spectral_clustering


WIDTH = 1280
HEIGHT = 820
PANEL_WIDTH = 370
PLOT_WIDTH = WIDTH - PANEL_WIDTH


class SpectralClusteringVisualizerApp:
    def __init__(self) -> None:
        try:
            import pygame
        except Exception as exc:
            raise RuntimeError("pygame is not installed. Install it with: pip install -r requirements.txt") from exc

        self.pygame = pygame
        pygame.init()
        pygame.display.set_caption("Spectral Clustering Visualizer - Reconstructed Skeleton")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small = pygame.font.SysFont("Arial", 16)
        self.tiny = pygame.font.SysFont("Arial", 13)

        self.dataset_name = "moons"
        self.seed = 42
        self.k = 2
        self.sigma = 0.34
        self.k_neighbors = 12
        self.show_edges = True
        self.show_embedding = False
        self.show_debug = True
        self.running = True

        self.data = generate_dataset(self.dataset_name, seed=self.seed)
        self.result = spectral_clustering(self.data, k=self.k, sigma=self.sigma, k_neighbors=self.k_neighbors, seed=self.seed)
        self.bounds = self.current_bounds()

    def current_points_for_plot(self):
        if self.show_embedding:
            return [[row[0], row[1] if len(row) > 1 else 0.0] for row in self.result.embedding]
        return self.data

    def current_bounds(self):
        return bounds_2d(self.current_points_for_plot())

    def recluster(self) -> None:
        self.k = max(1, min(self.k, len(self.data)))
        self.sigma = max(0.05, self.sigma)
        self.result = spectral_clustering(
            self.data,
            k=self.k,
            sigma=self.sigma,
            k_neighbors=self.k_neighbors,
            seed=self.seed,
        )
        self.bounds = self.current_bounds()

    def load_dataset(self, name: str) -> None:
        self.dataset_name = name
        self.data = generate_dataset(name, seed=self.seed)

        defaults = {
            "moons": (2, 0.34, 12),
            "rings": (2, 0.26, 12),
            "blobs": (3, 0.48, 12),
            "bridge": (2, 0.32, 10),
            "islands": (4, 0.34, 10),
            "spiral": (2, 0.30, 12),
        }

        self.k, self.sigma, self.k_neighbors = defaults.get(name, (self.k, self.sigma, self.k_neighbors))
        self.recluster()

    def regenerate(self) -> None:
        self.seed += 1
        self.data = generate_dataset(self.dataset_name, seed=self.seed)
        self.recluster()

    def save_screenshot(self) -> None:
        screenshots = Path(__file__).resolve().parents[1] / "screenshots"
        screenshots.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = screenshots / f"spectral_clustering_{self.dataset_name}_{stamp}.png"
        self.pygame.image.save(self.screen, str(path))
        print("[OK] Screenshot saved:", path)

    def handle_key(self, key: int) -> None:
        pygame = self.pygame

        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif key == pygame.K_r:
            self.regenerate()
        elif key == pygame.K_1:
            self.load_dataset("moons")
        elif key == pygame.K_2:
            self.load_dataset("rings")
        elif key == pygame.K_3:
            self.load_dataset("blobs")
        elif key == pygame.K_4:
            self.load_dataset("bridge")
        elif key == pygame.K_5:
            self.load_dataset("islands")
        elif key == pygame.K_6:
            self.load_dataset("spiral")
        elif key == pygame.K_UP:
            self.k = min(8, self.k + 1)
            self.recluster()
        elif key == pygame.K_DOWN:
            self.k = max(1, self.k - 1)
            self.recluster()
        elif key == pygame.K_RIGHT:
            self.sigma = min(2.0, self.sigma + 0.03)
            self.recluster()
        elif key == pygame.K_LEFT:
            self.sigma = max(0.06, self.sigma - 0.03)
            self.recluster()
        elif key == pygame.K_e:
            self.show_edges = not self.show_edges
        elif key == pygame.K_p:
            self.show_embedding = not self.show_embedding
            self.bounds = self.current_bounds()
        elif key == pygame.K_d:
            self.show_debug = not self.show_debug
        elif key == pygame.K_s:
            self.save_screenshot()

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

    def draw_edges(self) -> None:
        if not self.show_edges or self.show_embedding:
            return

        pygame = self.pygame
        points = self.current_points_for_plot()
        edges = self.result.display_edges(threshold=0.62, max_edges=420)

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for i, j, value in edges:
            a = self.world_to_screen(points[i][0], points[i][1])
            b = self.world_to_screen(points[j][0], points[j][1])
            alpha = int(25 + value * 78)
            pygame.draw.line(surface, (*EDGE, alpha), a, b, 1)

        self.screen.blit(surface, (0, 0))

    def draw_points(self) -> None:
        pygame = self.pygame
        points = self.current_points_for_plot()

        for row, label in zip(points, self.result.labels):
            x = row[0]
            y = row[1] if len(row) > 1 else 0.0
            sx, sy = self.world_to_screen(x, y)
            color = color_for_label(label)

            pygame.draw.circle(self.screen, color, (sx, sy), 6)
            pygame.draw.circle(self.screen, (255, 255, 255), (sx, sy), 7, width=1)

    def text(self, value: str, x: int, y: int, color=TEXT, font=None) -> None:
        chosen = font or self.small
        rendered = chosen.render(value, True, color)
        self.screen.blit(rendered, (x, y))

    def draw_panel(self) -> None:
        summary = result_summary(self.result)
        x = PLOT_WIDTH + 22
        y = 24

        self.text("Spectral Clustering", x, y, TEXT, self.font)
        y += 34
        self.text("Graph Laplacian + eigenvectors", x, y, MUTED)
        y += 36

        view = "embedding" if self.show_embedding else "original data"

        lines = [
            f"Dataset: {self.dataset_name}",
            f"Samples: {len(self.data)}",
            f"View: {view}",
            f"Clusters k: {self.k}",
            f"Sigma: {self.sigma:.2f}",
            f"kNN: {self.k_neighbors}",
            f"Cluster count: {summary['cluster_count']}",
            f"Edges: {'on' if self.show_edges else 'off'}",
            f"Seed: {self.seed}",
        ]

        for line in lines:
            self.text(line, x, y, TEXT)
            y += 24

        y += 12
        self.text("Cluster sizes", x, y, ACCENT)
        y += 26

        for cluster_id, size in summary["cluster_sizes"].items():
            self.text(f"Cluster {cluster_id}: {size}", x, y, MUTED)
            y += 21

        y += 18
        self.text("Smallest eigenvalues", x, y, ACCENT)
        y += 26

        for index, value in enumerate(summary["first_eigenvalues"][:7]):
            self.text(f"λ{index}: {value:.5f}", x, y, MUTED)
            y += 20

        y += 18
        self.text("Controls", x, y, ACCENT)
        y += 26

        controls = [
            "1 moons",
            "2 rings",
            "3 blobs",
            "4 bridge",
            "5 islands",
            "6 spiral",
            "Up/Down k",
            "Left/Right sigma",
            "E graph edges",
            "P embedding view",
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
            f"Spectral pipeline: affinity graph -> normalized Laplacian -> smallest eigenvectors -> row-normalized embedding -> k-means | "
            f"dataset={self.dataset_name}, k={self.k}, sigma={self.sigma:.2f}"
        )
        self.text(message, 18, HEIGHT - 28, TEXT, self.tiny)

    def draw(self) -> None:
        self.draw_background()
        self.draw_edges()
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
    SpectralClusteringVisualizerApp().run()
