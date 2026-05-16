from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import time

import numpy as np
import pygame

from .dbscan_core import NOISE, DBSCANResult, dbscan
from .datasets import make_clustered_points, make_noise_points


WIDTH = 1220
HEIGHT = 780
SIDE_PANEL_WIDTH = 340
FPS = 60

BACKGROUND = (13, 18, 28)
GRID = (31, 40, 56)
PANEL = (18, 25, 38)
TEXT = (232, 238, 248)
MUTED = (150, 164, 184)
ACCENT = (90, 168, 255)
NOISE_COLOR = (130, 138, 150)
CORE_RING = (255, 255, 255)

CLUSTER_COLORS = [
    (255, 107, 107),
    (78, 205, 196),
    (255, 209, 102),
    (167, 139, 250),
    (99, 179, 237),
    (72, 187, 120),
    (246, 135, 179),
    (251, 146, 60),
    (56, 189, 248),
    (190, 242, 100),
]


@dataclass
class AppState:
    points: np.ndarray
    eps: float = 46.0
    min_samples: int = 5
    result: DBSCANResult | None = None
    dirty: bool = True
    show_help: bool = True
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
    state.result = dbscan(state.points, state.eps, state.min_samples)
    state.dirty = False


def add_point(state: AppState, position: Tuple[int, int]) -> None:
    x, y = position
    if x >= WIDTH - SIDE_PANEL_WIDTH:
        return
    new_point = np.array([[float(x), float(y)]])
    if len(state.points) == 0:
        state.points = new_point
    else:
        state.points = np.vstack([state.points, new_point])
    state.dirty = True


def save_screenshot(surface: pygame.Surface, state: AppState) -> None:
    screenshots = Path(__file__).resolve().parents[1] / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    path = screenshots / f"dbscan_visualizer_{stamp}.png"
    pygame.image.save(surface, str(path))
    state.last_screenshot_path = str(path)
    state.screenshot_message_until = time.time() + 2.2


def draw_points(surface: pygame.Surface, state: AppState) -> None:
    if state.result is None:
        return

    labels = state.result.labels
    core_mask = state.result.core_mask

    for index, point in enumerate(state.points):
        x, y = int(point[0]), int(point[1])
        label = int(labels[index])

        if label == NOISE:
            color = NOISE_COLOR
            radius = 4
        else:
            color = CLUSTER_COLORS[label % len(CLUSTER_COLORS)]
            radius = 5

        pygame.draw.circle(surface, color, (x, y), radius)

        if core_mask[index]:
            pygame.draw.circle(surface, CORE_RING, (x, y), radius + 3, 1)


def draw_panel(surface: pygame.Surface, state: AppState, font: pygame.font.Font, small: pygame.font.Font) -> None:
    panel_x = WIDTH - SIDE_PANEL_WIDTH
    pygame.draw.rect(surface, PANEL, (panel_x, 0, SIDE_PANEL_WIDTH, HEIGHT))

    x = panel_x + 22
    y = 24

    draw_text(surface, font, "DBSCAN Visualizer", x, y, TEXT)
    y += 34
    draw_text(surface, small, "Reconstructed clean skeleton", x, y, MUTED)
    y += 34

    if state.result is not None:
        lines = [
            f"Points: {len(state.points)}",
            f"Clusters: {state.result.cluster_count}",
            f"Noise points: {state.result.noise_count}",
            f"Core points: {state.result.core_count}",
            f"eps: {state.eps:.1f}",
            f"min_samples: {state.min_samples}",
            f"Dirty state: {'yes' if state.dirty else 'no'}",
        ]
    else:
        lines = [
            f"Points: {len(state.points)}",
            "Clusters: not computed",
            "Noise points: not computed",
            "Core points: not computed",
            f"eps: {state.eps:.1f}",
            f"min_samples: {state.min_samples}",
            "Dirty state: yes",
        ]

    for line in lines:
        draw_text(surface, small, line, x, y, TEXT)
        y += 24

    y += 14
    draw_text(surface, small, "Controls", x, y, ACCENT)
    y += 28

    controls = [
        "Left click: add point",
        "R: regenerate dataset",
        "C: clear points",
        "N: add random noise",
        "+ / -: change eps",
        "[ / ]: min_samples",
        "Space: recompute",
        "S: save screenshot",
        "H: toggle help",
        "Esc: quit",
    ]

    for line in controls:
        draw_text(surface, small, line, x, y, MUTED)
        y += 22

    y += 16
    draw_text(surface, small, "Model note", x, y, ACCENT)
    y += 26

    note = [
        "DBSCAN groups dense regions.",
        "Sparse points become noise.",
        "No cluster count is predefined.",
        "Useful for anomaly reasoning",
        "and spatial telemetry demos.",
    ]

    for line in note:
        draw_text(surface, small, line, x, y, MUTED)
        y += 22

    if time.time() < state.screenshot_message_until:
        y = HEIGHT - 70
        draw_text(surface, small, "Screenshot saved:", x, y, ACCENT)
        y += 22
        draw_text(surface, small, Path(state.last_screenshot_path).name, x, y, TEXT)


def draw_help_overlay(surface: pygame.Surface, state: AppState, small: pygame.font.Font) -> None:
    if not state.show_help:
        return

    overlay = pygame.Surface((WIDTH - SIDE_PANEL_WIDTH - 50, 86), pygame.SRCALPHA)
    overlay.fill((10, 16, 26, 210))
    surface.blit(overlay, (25, 22))

    lines = [
        "DBSCAN: eps controls neighborhood radius, min_samples controls density threshold.",
        "Core points have enough neighbors, border points attach to clusters, isolated points become noise.",
        "Use +, -, [, ] to tune parameters. Use S to export a screenshot for documentation.",
    ]

    y = 36
    for line in lines:
        draw_text(surface, small, line, 42, y, TEXT)
        y += 24


def draw_eps_preview(surface: pygame.Surface, state: AppState) -> None:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x >= WIDTH - SIDE_PANEL_WIDTH:
        return

    preview = pygame.Surface((WIDTH - SIDE_PANEL_WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(preview, (90, 168, 255, 36), (mouse_x, mouse_y), int(state.eps), 1)
    surface.blit(preview, (0, 0))


def handle_key(event: pygame.event.Event, state: AppState) -> bool:
    if event.key == pygame.K_ESCAPE:
        return False

    if event.key == pygame.K_r:
        state.points = make_clustered_points(WIDTH, HEIGHT, SIDE_PANEL_WIDTH, seed=None)
        state.dirty = True

    elif event.key == pygame.K_c:
        state.points = np.zeros((0, 2), dtype=float)
        state.dirty = True

    elif event.key == pygame.K_n:
        noise = make_noise_points(25, WIDTH, HEIGHT, SIDE_PANEL_WIDTH, seed=None)
        if len(state.points) == 0:
            state.points = noise
        else:
            state.points = np.vstack([state.points, noise])
        state.dirty = True

    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
        state.eps = min(180.0, state.eps + 4.0)
        state.dirty = True

    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
        state.eps = max(4.0, state.eps - 4.0)
        state.dirty = True

    elif event.key == pygame.K_LEFTBRACKET:
        state.min_samples = max(1, state.min_samples - 1)
        state.dirty = True

    elif event.key == pygame.K_RIGHTBRACKET:
        state.min_samples = min(30, state.min_samples + 1)
        state.dirty = True

    elif event.key == pygame.K_SPACE:
        state.dirty = True

    elif event.key == pygame.K_h:
        state.show_help = not state.show_help

    return True


def run_app() -> None:
    pygame.init()
    pygame.display.set_caption("DBSCAN Pygame Visualizer - Reconstructed Skeleton")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24, bold=True)
    small = pygame.font.SysFont("Arial", 16)

    state = AppState(
        points=make_clustered_points(WIDTH, HEIGHT, SIDE_PANEL_WIDTH, seed=42),
        eps=46.0,
        min_samples=5,
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
        draw_eps_preview(screen, state)
        draw_points(screen, state)
        draw_help_overlay(screen, state, small)
        draw_panel(screen, state, font, small)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
