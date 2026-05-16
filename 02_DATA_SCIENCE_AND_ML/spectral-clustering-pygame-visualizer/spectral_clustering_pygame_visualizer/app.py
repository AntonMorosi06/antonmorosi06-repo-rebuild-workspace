from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
import time

import numpy as np
import pygame

from .datasets import make_moons_like_dataset, make_random_noise
from .spectral_core import SpectralResult, spectral_cluster


WIDTH = 1240
HEIGHT = 780
SIDE_PANEL_WIDTH = 360
FPS = 60

BACKGROUND = (13, 18, 28)
GRID = (31, 40, 56)
PANEL = (18, 25, 38)
TEXT = (232, 238, 248)
MUTED = (150, 164, 184)
ACCENT = (90, 168, 255)
EDGE_COLOR = (90, 168, 255, 36)
POINT_OUTLINE = (245, 248, 255)

CLUSTER_COLORS = [
    (255, 107, 107),
    (78, 205, 196),
    (255, 209, 102),
    (167, 139, 250),
    (99, 179, 237),
    (72, 187, 120),
    (246, 135, 179),
    (251, 146, 60),
]


@dataclass
class AppState:
    points: np.ndarray
    cluster_count: int = 2
    neighbor_count: int = 9
    sigma: float = 88.0
    result: SpectralResult | None = None
    dirty: bool = True
    show_help: bool = True
    show_graph: bool = True
    screenshot_message_until: float = 0.0
    last_screenshot_path: str = ""


def draw_text(surface: pygame.Surface, font: pygame.font.Font, text: str, x: int, y: int, color=TEXT) -> None:
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))


def draw_grid(surface: pygame.Surface) -> None:
    canvas_width = WIDTH - SIDE_PANEL_WIDTH
    for x in range(0, canvas_width, 40):
        pygame.draw.line(surface, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(surface, GRID, (0, y), (canvas_width, y), 1)


def recalculate(state: AppState) -> None:
    state.result = spectral_cluster(
        state.points,
        cluster_count=state.cluster_count,
        neighbor_count=state.neighbor_count,
        sigma=state.sigma,
    )
    state.dirty = False


def add_point(state: AppState, position: Tuple[int, int]) -> None:
    x, y = position
    if x >= WIDTH - SIDE_PANEL_WIDTH:
        return
    point = np.array([[float(x), float(y)]])
    if len(state.points) == 0:
        state.points = point
    else:
        state.points = np.vstack([state.points, point])
    state.dirty = True


def save_screenshot(surface: pygame.Surface, state: AppState) -> None:
    screenshots = Path(__file__).resolve().parents[1] / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    path = screenshots / f"spectral_clustering_visualizer_{stamp}.png"
    pygame.image.save(surface, str(path))
    state.last_screenshot_path = str(path)
    state.screenshot_message_until = time.time() + 2.2


def draw_graph_edges(surface: pygame.Surface, state: AppState) -> None:
    if not state.show_graph or state.result is None:
        return

    points = state.points
    affinity = state.result.affinity

    if len(points) == 0 or affinity.size == 0:
        return

    edge_surface = pygame.Surface((WIDTH - SIDE_PANEL_WIDTH, HEIGHT), pygame.SRCALPHA)
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            weight = affinity[i, j]
            if weight <= 0:
                continue

            alpha = int(max(18, min(95, 24 + weight * 95)))
            color = (90, 168, 255, alpha)
            pygame.draw.line(
                edge_surface,
                color,
                (int(points[i, 0]), int(points[i, 1])),
                (int(points[j, 0]), int(points[j, 1])),
                1,
            )

    surface.blit(edge_surface, (0, 0))


def draw_points(surface: pygame.Surface, state: AppState) -> None:
    if state.result is None:
        return

    labels = state.result.labels

    for index, point in enumerate(state.points):
        x, y = int(point[0]), int(point[1])
        label = int(labels[index]) if index < len(labels) else 0
        color = CLUSTER_COLORS[label % len(CLUSTER_COLORS)]
        pygame.draw.circle(surface, color, (x, y), 6)
        pygame.draw.circle(surface, POINT_OUTLINE, (x, y), 8, 1)


def draw_sigma_preview(surface: pygame.Surface, state: AppState) -> None:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x >= WIDTH - SIDE_PANEL_WIDTH:
        return

    preview = pygame.Surface((WIDTH - SIDE_PANEL_WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(preview, (90, 168, 255, 24), (mouse_x, mouse_y), int(state.sigma), 1)
    surface.blit(preview, (0, 0))


def draw_panel(surface: pygame.Surface, state: AppState, font: pygame.font.Font, small: pygame.font.Font) -> None:
    panel_x = WIDTH - SIDE_PANEL_WIDTH
    pygame.draw.rect(surface, PANEL, (panel_x, 0, SIDE_PANEL_WIDTH, HEIGHT))

    x = panel_x + 22
    y = 24

    draw_text(surface, font, "Spectral Clustering", x, y, TEXT)
    y += 34
    draw_text(surface, small, "Graph affinity visualizer", x, y, MUTED)
    y += 34

    if state.result is not None:
        lines = [
            f"Points: {len(state.points)}",
            f"Clusters: {state.result.cluster_count}",
            f"KNN neighbors: {state.neighbor_count}",
            f"Graph edges: {state.result.edge_count}",
            f"Sigma: {state.sigma:.1f}",
            f"Dirty state: {'yes' if state.dirty else 'no'}",
            f"Graph shown: {'yes' if state.show_graph else 'no'}",
        ]
    else:
        lines = [
            f"Points: {len(state.points)}",
            f"Clusters: {state.cluster_count}",
            f"KNN neighbors: {state.neighbor_count}",
            "Graph edges: not computed",
            f"Sigma: {state.sigma:.1f}",
            "Dirty state: yes",
            f"Graph shown: {'yes' if state.show_graph else 'no'}",
        ]

    for line in lines:
        draw_text(surface, small, line, x, y, TEXT)
        y += 24

    y += 10
    draw_text(surface, small, "Smallest eigenvalues", x, y, ACCENT)
    y += 26

    if state.result is not None and len(state.result.eigenvalues) > 0:
        values = [f"{value:.4f}" for value in state.result.eigenvalues[:6]]
        for value in values:
            draw_text(surface, small, value, x, y, MUTED)
            y += 20
    else:
        draw_text(surface, small, "not computed", x, y, MUTED)
        y += 20

    y += 14
    draw_text(surface, small, "Controls", x, y, ACCENT)
    y += 26

    controls = [
        "Left click: add point",
        "R: regenerate dataset",
        "C: clear points",
        "N: add random noise",
        "J / K: cluster count",
        "[ / ]: KNN neighbors",
        "- / +: affinity sigma",
        "G: toggle graph edges",
        "S: save screenshot",
        "H: toggle help",
        "Esc: quit",
    ]

    for line in controls:
        draw_text(surface, small, line, x, y, MUTED)
        y += 21

    y += 14
    draw_text(surface, small, "Model note", x, y, ACCENT)
    y += 25

    note = [
        "Spectral clustering builds",
        "a graph, studies the",
        "Laplacian eigenvectors",
        "and clusters the embedded",
        "representation.",
    ]

    for line in note:
        draw_text(surface, small, line, x, y, MUTED)
        y += 21

    if time.time() < state.screenshot_message_until:
        y = HEIGHT - 70
        draw_text(surface, small, "Screenshot saved:", x, y, ACCENT)
        y += 22
        draw_text(surface, small, Path(state.last_screenshot_path).name, x, y, TEXT)


def draw_help_overlay(surface: pygame.Surface, state: AppState, small: pygame.font.Font) -> None:
    if not state.show_help:
        return

    overlay = pygame.Surface((WIDTH - SIDE_PANEL_WIDTH - 50, 100), pygame.SRCALPHA)
    overlay.fill((10, 16, 26, 215))
    surface.blit(overlay, (25, 22))

    lines = [
        "Spectral clustering converts points into a graph, then uses Laplacian eigenvectors to reveal partitions.",
        "KNN neighbors controls graph connectivity. Sigma controls how strongly distance affects affinity weights.",
        "S is reserved only for screenshots, avoiding the old screenshot/zoom key conflict.",
        "Use G to hide or show graph edges when the canvas becomes dense.",
    ]

    y = 35
    for line in lines:
        draw_text(surface, small, line, 42, y, TEXT)
        y += 23


def handle_key(event: pygame.event.Event, state: AppState) -> bool:
    if event.key == pygame.K_ESCAPE:
        return False

    if event.key == pygame.K_r:
        state.points = make_moons_like_dataset(WIDTH, HEIGHT, SIDE_PANEL_WIDTH, seed=None)
        state.dirty = True

    elif event.key == pygame.K_c:
        state.points = np.zeros((0, 2), dtype=float)
        state.dirty = True

    elif event.key == pygame.K_n:
        noise = make_random_noise(22, WIDTH, HEIGHT, SIDE_PANEL_WIDTH, seed=None)
        if len(state.points) == 0:
            state.points = noise
        else:
            state.points = np.vstack([state.points, noise])
        state.dirty = True

    elif event.key == pygame.K_j:
        state.cluster_count = max(1, state.cluster_count - 1)
        state.dirty = True

    elif event.key == pygame.K_k:
        state.cluster_count = min(8, state.cluster_count + 1)
        state.dirty = True

    elif event.key == pygame.K_LEFTBRACKET:
        state.neighbor_count = max(1, state.neighbor_count - 1)
        state.dirty = True

    elif event.key == pygame.K_RIGHTBRACKET:
        state.neighbor_count = min(40, state.neighbor_count + 1)
        state.dirty = True

    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
        state.sigma = max(8.0, state.sigma - 6.0)
        state.dirty = True

    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
        state.sigma = min(220.0, state.sigma + 6.0)
        state.dirty = True

    elif event.key == pygame.K_g:
        state.show_graph = not state.show_graph

    elif event.key == pygame.K_h:
        state.show_help = not state.show_help

    elif event.key == pygame.K_SPACE:
        state.dirty = True

    return True


def run_app() -> None:
    pygame.init()
    pygame.display.set_caption("Spectral Clustering Pygame Visualizer - Reconstructed Skeleton")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24, bold=True)
    small = pygame.font.SysFont("Arial", 16)

    state = AppState(
        points=make_moons_like_dataset(WIDTH, HEIGHT, SIDE_PANEL_WIDTH, seed=42),
        cluster_count=2,
        neighbor_count=9,
        sigma=88.0,
        dirty=True,
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                add_point(state, event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_screenshot(screen, state)
                else:
                    running = handle_key(event, state)

        if state.dirty:
            recalculate(state)

        screen.fill(BACKGROUND)
        draw_grid(screen)
        draw_sigma_preview(screen, state)
        draw_graph_edges(screen, state)
        draw_points(screen, state)
        draw_help_overlay(screen, state, small)
        draw_panel(screen, state, font, small)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
