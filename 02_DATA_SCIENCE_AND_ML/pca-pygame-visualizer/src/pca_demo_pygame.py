from __future__ import annotations

import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pygame


WIDTH = 1400
HEIGHT = 820
FPS = 60

BACKGROUND = (12, 14, 22)
PANEL_BG = (22, 25, 38)
TEXT = (230, 235, 245)
MUTED = (150, 160, 180)
GRID = (55, 65, 85)
AXIS_X = (230, 90, 90)
AXIS_Y = (90, 220, 140)
AXIS_Z = (100, 160, 240)
POINT = (110, 190, 255)
POINT_DEPTH_NEAR = (255, 210, 120)
POINT_DEPTH_FAR = (80, 130, 255)
PCA_1 = (255, 120, 120)
PCA_2 = (120, 255, 170)
PCA_3 = (140, 180, 255)
WHITE = (255, 255, 255)

OUTPUT_DIR = Path("output")


@dataclass
class Camera:
    yaw: float = 0.65
    pitch: float = -0.45
    zoom: float = 120.0
    distance: float = 5.5


@dataclass
class PCAResult:
    mean: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    explained_variance_ratio: np.ndarray


def generate_correlated_points(n: int = 180, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)

    latent_a = rng.normal(0, 1.5, n)
    latent_b = rng.normal(0, 0.75, n)
    noise = rng.normal(0, 0.28, n)

    x = latent_a
    y = 0.65 * latent_a + latent_b
    z = 0.55 * latent_a - 0.35 * latent_b + noise

    points = np.column_stack([x, y, z])
    points -= points.mean(axis=0)

    return points


def compute_pca(points: np.ndarray) -> PCAResult:
    mean = points.mean(axis=0)
    centered = points - mean
    covariance = np.cov(centered.T)

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]

    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    total = eigenvalues.sum()
    if total <= 0:
        explained = np.zeros_like(eigenvalues)
    else:
        explained = eigenvalues / total

    return PCAResult(
        mean=mean,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        explained_variance_ratio=explained,
    )


def rotation_matrix(yaw: float, pitch: float) -> np.ndarray:
    cy = math.cos(yaw)
    sy = math.sin(yaw)
    cp = math.cos(pitch)
    sp = math.sin(pitch)

    rot_yaw = np.array([
        [cy, 0, sy],
        [0, 1, 0],
        [-sy, 0, cy],
    ])

    rot_pitch = np.array([
        [1, 0, 0],
        [0, cp, -sp],
        [0, sp, cp],
    ])

    return rot_pitch @ rot_yaw


def project(point: np.ndarray, camera: Camera, center_x: int, center_y: int) -> tuple[int, int, float]:
    rotated = rotation_matrix(camera.yaw, camera.pitch) @ point
    z = rotated[2] + camera.distance

    if z <= 0.1:
        z = 0.1

    factor = camera.zoom / z
    x2d = center_x + rotated[0] * factor
    y2d = center_y - rotated[1] * factor

    return int(x2d), int(y2d), z


def mix_color(a, b, t: float):
    t = max(0.0, min(1.0, t))
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def point_color(point: np.ndarray, depth: float, mode: int):
    if mode == 1:
        return POINT

    if mode == 2:
        t = max(0.0, min(1.0, (depth - 2.0) / 8.0))
        return mix_color(POINT_DEPTH_NEAR, POINT_DEPTH_FAR, t)

    if point[0] >= 0 and point[1] >= 0:
        return (255, 170, 110)
    if point[0] < 0 and point[1] >= 0:
        return (120, 230, 160)
    if point[0] < 0 and point[1] < 0:
        return (130, 170, 255)
    return (240, 120, 220)


def draw_text(surface, font, text, x, y, color=TEXT):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_axes(surface, camera: Camera, center_x: int, center_y: int):
    origin = np.array([0.0, 0.0, 0.0])
    axes = [
        (np.array([2.5, 0.0, 0.0]), AXIS_X, "X"),
        (np.array([0.0, 2.5, 0.0]), AXIS_Y, "Y"),
        (np.array([0.0, 0.0, 2.5]), AXIS_Z, "Z"),
    ]

    ox, oy, _ = project(origin, camera, center_x, center_y)

    for endpoint, color, label in axes:
        ex, ey, _ = project(endpoint, camera, center_x, center_y)
        pygame.draw.line(surface, color, (ox, oy), (ex, ey), 2)
        pygame.draw.circle(surface, color, (ex, ey), 5)
        draw_text(surface, pygame.font.SysFont("Menlo", 14), label, ex + 6, ey + 6, color)


def draw_grid(surface, camera: Camera, center_x: int, center_y: int):
    for i in range(-4, 5):
        a = np.array([i, -4, 0.0])
        b = np.array([i, 4, 0.0])
        ax, ay, _ = project(a, camera, center_x, center_y)
        bx, by, _ = project(b, camera, center_x, center_y)
        pygame.draw.line(surface, GRID, (ax, ay), (bx, by), 1)

        c = np.array([-4, i, 0.0])
        d = np.array([4, i, 0.0])
        cx, cy, _ = project(c, camera, center_x, center_y)
        dx, dy, _ = project(d, camera, center_x, center_y)
        pygame.draw.line(surface, GRID, (cx, cy), (dx, dy), 1)


def draw_points(surface, points: np.ndarray, camera: Camera, center_x: int, center_y: int, color_mode: int):
    projected = []
    for point in points:
        x, y, depth = project(point, camera, center_x, center_y)
        projected.append((depth, x, y, point))

    projected.sort(reverse=True)

    for depth, x, y, point in projected:
        radius = int(max(3, min(8, 8 - depth * 0.55)))
        color = point_color(point, depth, color_mode)
        pygame.draw.circle(surface, color, (x, y), radius)


def draw_pca_vectors(surface, pca: PCAResult, camera: Camera, center_x: int, center_y: int):
    colors = [PCA_1, PCA_2, PCA_3]
    labels = ["PC1", "PC2", "PC3"]

    origin = pca.mean
    ox, oy, _ = project(origin, camera, center_x, center_y)

    for i in range(3):
        vector = pca.eigenvectors[:, i]
        scale = math.sqrt(max(pca.eigenvalues[i], 0.0)) * 2.0

        endpoint_a = origin + vector * scale
        endpoint_b = origin - vector * scale

        ax, ay, _ = project(endpoint_a, camera, center_x, center_y)
        bx, by, _ = project(endpoint_b, camera, center_x, center_y)

        color = colors[i]

        pygame.draw.line(surface, color, (bx, by), (ax, ay), 4)
        pygame.draw.circle(surface, color, (ax, ay), 7)
        pygame.draw.circle(surface, color, (bx, by), 5)

        draw_text(surface, pygame.font.SysFont("Menlo", 14), labels[i], ax + 8, ay + 8, color)

    pygame.draw.circle(surface, WHITE, (ox, oy), 5)


def draw_panel(surface, font, small_font, pca: PCAResult, show_vectors: bool, color_mode: int, point_count: int):
    panel_x = WIDTH - 360
    pygame.draw.rect(surface, PANEL_BG, (panel_x, 0, 360, HEIGHT))

    x = panel_x + 24
    y = 28

    draw_text(surface, font, "PCA Visualizer", x, y)
    y += 36

    draw_text(surface, small_font, "Principal Component Analysis", x, y, MUTED)
    y += 34

    draw_text(surface, small_font, f"Points: {point_count}", x, y)
    y += 24

    draw_text(surface, small_font, f"PCA vectors: {'ON' if show_vectors else 'OFF'}", x, y)
    y += 24

    mode_name = {1: "fixed", 2: "depth", 3: "quadrant"}.get(color_mode, "unknown")
    draw_text(surface, small_font, f"Color mode: {mode_name}", x, y)
    y += 38

    draw_text(surface, small_font, "Explained variance:", x, y, TEXT)
    y += 26

    colors = [PCA_1, PCA_2, PCA_3]

    for i, ratio in enumerate(pca.explained_variance_ratio):
        percent = ratio * 100.0
        draw_text(surface, small_font, f"PC{i + 1}: {percent:5.2f}%", x, y, colors[i])
        y += 24

        bar_w = int(250 * ratio)
        pygame.draw.rect(surface, (45, 50, 70), (x, y, 250, 10))
        pygame.draw.rect(surface, colors[i], (x, y, bar_w, 10))
        y += 22

    y += 16
    draw_text(surface, small_font, "Controls:", x, y, TEXT)
    y += 26

    controls = [
        "Mouse drag: rotate",
        "Mouse wheel: zoom",
        "SPACE: PCA vectors",
        "R: regenerate data",
        "C: reset camera",
        "S: screenshot",
        "1/2/3: color mode",
        "ESC: exit"
    ]

    for line in controls:
        draw_text(surface, small_font, line, x, y, MUTED)
        y += 22


def save_screenshot(surface):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"pca_visualizer_{timestamp}.png"
    pygame.image.save(surface, path)
    print(f"[OK] Screenshot saved: {path}")


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PCA Pygame Visualizer")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Menlo", 24)
    small_font = pygame.font.SysFont("Menlo", 16)

    camera = Camera()
    points = generate_correlated_points()
    pca = compute_pca(points)

    show_vectors = True
    color_mode = 2

    dragging = False
    last_mouse = None

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    show_vectors = not show_vectors

                elif event.key == pygame.K_r:
                    points = generate_correlated_points(seed=int(time.time()) % 100000)
                    pca = compute_pca(points)

                elif event.key == pygame.K_c:
                    camera = Camera()

                elif event.key == pygame.K_s:
                    save_screenshot(screen)

                elif event.key == pygame.K_1:
                    color_mode = 1

                elif event.key == pygame.K_2:
                    color_mode = 2

                elif event.key == pygame.K_3:
                    color_mode = 3

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and event.pos[0] < WIDTH - 360:
                    dragging = True
                    last_mouse = event.pos

                elif event.button == 4:
                    camera.zoom *= 1.08

                elif event.button == 5:
                    camera.zoom /= 1.08

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    last_mouse = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                if last_mouse is not None:
                    dx = event.pos[0] - last_mouse[0]
                    dy = event.pos[1] - last_mouse[1]
                    camera.yaw += dx * 0.008
                    camera.pitch += dy * 0.008
                    camera.pitch = max(-1.45, min(1.45, camera.pitch))
                last_mouse = event.pos

        screen.fill(BACKGROUND)

        center_x = (WIDTH - 360) // 2
        center_y = HEIGHT // 2

        draw_grid(screen, camera, center_x, center_y)
        draw_axes(screen, camera, center_x, center_y)
        draw_points(screen, points, camera, center_x, center_y, color_mode)

        if show_vectors:
            draw_pca_vectors(screen, pca, camera, center_x, center_y)

        draw_panel(screen, font, small_font, pca, show_vectors, color_mode, len(points))

        fps_text = f"{clock.get_fps():5.1f} FPS"
        draw_text(screen, small_font, fps_text, 18, 18, MUTED)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
