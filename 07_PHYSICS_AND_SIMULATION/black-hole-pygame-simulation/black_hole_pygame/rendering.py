from __future__ import annotations

import math

from .config import (
    ACCENT,
    BACKGROUND,
    DISK_COLD,
    DISK_HOT,
    EVENT_HORIZON,
    JET_COLOR,
    MUTED,
    SHOCKWAVE,
    TEXT,
)
from .simulation import BlackHoleSimulation


def lerp(a: int, b: int, t: float) -> int:
    t = max(0.0, min(1.0, t))
    return int(a + (b - a) * t)


def particle_color(energy: float) -> tuple[int, int, int]:
    return (
        lerp(DISK_COLD[0], DISK_HOT[0], energy),
        lerp(DISK_COLD[1], DISK_HOT[1], energy),
        lerp(DISK_COLD[2], DISK_HOT[2], energy),
    )


class Renderer:
    def __init__(self, pygame_module, screen, font, small_font) -> None:
        self.pygame = pygame_module
        self.screen = screen
        self.font = font
        self.small_font = small_font

    def draw(self, simulation: BlackHoleSimulation, show_trails: bool, show_jets: bool, debug: bool) -> None:
        self.screen.fill(BACKGROUND)
        self.draw_starfield(simulation.frame)
        self.draw_accretion_glow(simulation)
        if show_trails:
            self.draw_trails(simulation)
        self.draw_particles(simulation)
        self.draw_shockwaves(simulation)
        if show_jets:
            self.draw_jets(simulation)
        self.draw_black_hole(simulation)
        self.draw_overlay(simulation, debug)

    def draw_starfield(self, frame: int) -> None:
        pygame = self.pygame
        width, height = self.screen.get_size()
        for index in range(115):
            x = (index * 117 + frame * 0.18) % width
            y = (index * 61) % height
            shade = 75 + int(math.sin(index * 0.7 + frame * 0.01) * 32)
            pygame.draw.circle(self.screen, (shade, shade, shade), (int(x), int(y)), 1)

    def draw_accretion_glow(self, simulation: BlackHoleSimulation) -> None:
        pygame = self.pygame
        center = simulation.black_hole.position
        radius = int(simulation.black_hole.accretion_radius)

        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        for step in range(10, 0, -1):
            alpha = int(7 * step)
            current_radius = int(radius * step / 10)
            color = (90, 168, 255, alpha)
            pygame.draw.circle(surface, color, center.tuple_int(), current_radius, width=2)

        self.screen.blit(surface, (0, 0))

    def draw_trails(self, simulation: BlackHoleSimulation) -> None:
        pygame = self.pygame
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        for particle in simulation.particles:
            if len(particle.trail) < 2:
                continue

            color = particle_color(particle.energy)
            for index in range(1, len(particle.trail)):
                factor = index / len(particle.trail)
                alpha = int(120 * factor)
                trail_color = (color[0], color[1], color[2], alpha)
                pygame.draw.line(
                    surface,
                    trail_color,
                    particle.trail[index - 1].tuple_int(),
                    particle.trail[index].tuple_int(),
                    1,
                )

        self.screen.blit(surface, (0, 0))

    def draw_particles(self, simulation: BlackHoleSimulation) -> None:
        pygame = self.pygame
        for particle in simulation.particles:
            color = particle_color(particle.energy)
            pygame.draw.circle(
                self.screen,
                color,
                particle.position.tuple_int(),
                max(1, int(particle.radius + particle.energy * 2.2)),
            )

    def draw_shockwaves(self, simulation: BlackHoleSimulation) -> None:
        pygame = self.pygame
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        for shockwave in simulation.shockwaves:
            alpha = int(180 * shockwave.alpha)
            color = (SHOCKWAVE[0], SHOCKWAVE[1], SHOCKWAVE[2], alpha)
            pygame.draw.circle(surface, color, shockwave.position.tuple_int(), int(shockwave.radius), width=2)

        self.screen.blit(surface, (0, 0))

    def draw_jets(self, simulation: BlackHoleSimulation) -> None:
        pygame = self.pygame
        center = simulation.black_hole.position
        width, height = self.screen.get_size()
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        pulse = 0.5 + 0.5 * math.sin(simulation.frame * 0.06)
        alpha = int(70 + pulse * 65)

        for direction in [-1, 1]:
            points = [
                (center.x - 18, center.y),
                (center.x + 18, center.y),
                (center.x + direction * 56, center.y + direction * 0),
            ]
            jet_end_y = 0 if direction < 0 else height
            pygame.draw.polygon(
                surface,
                (JET_COLOR[0], JET_COLOR[1], JET_COLOR[2], alpha),
                [
                    (center.x - 14, center.y),
                    (center.x + 14, center.y),
                    (center.x + 42, jet_end_y),
                    (center.x - 42, jet_end_y),
                ],
            )

        self.screen.blit(surface, (0, 0))

    def draw_black_hole(self, simulation: BlackHoleSimulation) -> None:
        pygame = self.pygame
        center = simulation.black_hole.position
        radius = int(simulation.black_hole.event_horizon_radius)

        pygame.draw.circle(self.screen, (18, 24, 39), center.tuple_int(), radius + 12)
        pygame.draw.circle(self.screen, EVENT_HORIZON, center.tuple_int(), radius)
        pygame.draw.circle(self.screen, ACCENT, center.tuple_int(), radius + 3, width=2)

    def draw_overlay(self, simulation: BlackHoleSimulation, debug: bool) -> None:
        stats = simulation.stats()
        lines = [
            "Black Hole Pygame Simulation",
            f"Particles: {stats.particles}",
            f"Absorbed: {stats.absorbed_total}",
            f"Shockwaves: {stats.shockwaves}",
            f"Mode: {stats.spawn_mode}",
            f"Average energy: {stats.average_energy:.3f}",
        ]

        if debug:
            lines.extend(
                [
                    f"Frame: {stats.frame}",
                    f"Paused: {simulation.paused}",
                    "Controls: 1-5 modes | Space pause | R reset | T trails | J jets | S screenshot",
                ]
            )

        x = 18
        y = 18

        for index, line in enumerate(lines):
            font = self.font if index == 0 else self.small_font
            color = TEXT if index == 0 else MUTED
            rendered = font.render(line, True, color)
            self.screen.blit(rendered, (x, y))
            y += 26 if index == 0 else 21
