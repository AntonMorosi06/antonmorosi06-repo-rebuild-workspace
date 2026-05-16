from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

from .config import (
    ABSORPTION_RADIUS,
    ACCRETION_RADIUS,
    BLACK_HOLE_MASS,
    DEFAULT_PARTICLES,
    EVENT_HORIZON_RADIUS,
    MAX_PARTICLES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SOFTENING,
    SPAWN_MODES,
    TRAIL_LENGTH,
)
from .entities import BlackHole, Particle, Shockwave
from .vector import Vec2, distance, from_angle


@dataclass
class SimulationStats:
    particles: int
    absorbed_total: int
    shockwaves: int
    spawn_mode: str
    average_energy: float
    frame: int


@dataclass
class BlackHoleSimulation:
    width: int = SCREEN_WIDTH
    height: int = SCREEN_HEIGHT
    seed: int | None = None
    particles: list[Particle] = field(default_factory=list)
    shockwaves: list[Shockwave] = field(default_factory=list)
    spawn_mode: str = "edge"
    absorbed_total: int = 0
    frame: int = 0
    paused: bool = False

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.black_hole = BlackHole(
            position=Vec2(self.width / 2, self.height / 2),
            mass=BLACK_HOLE_MASS,
            event_horizon_radius=EVENT_HORIZON_RADIUS,
            absorption_radius=ABSORPTION_RADIUS,
            accretion_radius=ACCRETION_RADIUS,
        )
        self.reset()

    def reset(self) -> None:
        self.particles.clear()
        self.shockwaves.clear()
        self.absorbed_total = 0
        self.frame = 0
        for _ in range(DEFAULT_PARTICLES):
            self.spawn_particle(self.spawn_mode)

    def cycle_spawn_mode(self, mode: str) -> None:
        if mode not in SPAWN_MODES:
            raise ValueError(f"unknown spawn mode: {mode}")
        self.spawn_mode = mode

    def spawn_particle(self, mode: str | None = None) -> Particle:
        mode = mode or self.spawn_mode
        center = self.black_hole.position

        if mode == "disk":
            angle = self.rng.uniform(0.0, math.tau)
            radius = self.rng.uniform(self.black_hole.accretion_radius * 0.82, self.black_hole.accretion_radius * 1.75)
            position = center + from_angle(angle, radius)
            tangent = (position - center).perpendicular().normalized()
            speed = self.rng.uniform(2.0, 4.2)
            velocity = tangent * speed

        elif mode == "spiral":
            angle = self.rng.uniform(0.0, math.tau)
            radius = self.rng.uniform(self.black_hole.accretion_radius * 1.1, self.black_hole.accretion_radius * 2.4)
            position = center + from_angle(angle, radius)
            inward = (center - position).normalized()
            tangent = inward.perpendicular()
            velocity = tangent * self.rng.uniform(2.3, 4.8) + inward * self.rng.uniform(0.4, 1.2)

        elif mode == "rain":
            x = self.rng.uniform(0.0, self.width)
            y = self.rng.uniform(-120.0, 10.0)
            position = Vec2(x, y)
            target = center + Vec2(self.rng.uniform(-160.0, 160.0), self.rng.uniform(-80.0, 80.0))
            velocity = (target - position).normalized() * self.rng.uniform(1.2, 3.8)

        elif mode == "cluster":
            angle = self.rng.uniform(0.0, math.tau)
            cluster_center = center + from_angle(angle, self.rng.uniform(330.0, 520.0))
            position = cluster_center + Vec2(self.rng.gauss(0.0, 42.0), self.rng.gauss(0.0, 42.0))
            velocity = (center - position).normalized() * self.rng.uniform(0.4, 2.3)

        else:
            side = self.rng.choice(["left", "right", "top", "bottom"])
            if side == "left":
                position = Vec2(-20.0, self.rng.uniform(0.0, self.height))
            elif side == "right":
                position = Vec2(self.width + 20.0, self.rng.uniform(0.0, self.height))
            elif side == "top":
                position = Vec2(self.rng.uniform(0.0, self.width), -20.0)
            else:
                position = Vec2(self.rng.uniform(0.0, self.width), self.height + 20.0)

            target = center + Vec2(self.rng.uniform(-220.0, 220.0), self.rng.uniform(-160.0, 160.0))
            velocity = (target - position).normalized() * self.rng.uniform(1.0, 3.6)

        particle = Particle(
            position=position,
            velocity=velocity,
            mass=self.rng.uniform(0.6, 1.8),
            radius=self.rng.uniform(1.4, 3.2),
            energy=self.rng.uniform(0.1, 0.65),
        )
        self.particles.append(particle)
        return particle

    def update(self, dt: float = 1.0 / 60.0) -> None:
        if self.paused:
            return

        self.frame += 1

        alive_particles: list[Particle] = []

        for particle in self.particles:
            self.update_particle(particle, dt)

            if particle.absorbed:
                self.absorbed_total += 1
                self.shockwaves.append(Shockwave(position=particle.position.copy()))
            elif self.is_far_outside(particle):
                pass
            else:
                alive_particles.append(particle)

        self.particles = alive_particles

        for shockwave in self.shockwaves:
            shockwave.update(dt)
        self.shockwaves = [shockwave for shockwave in self.shockwaves if shockwave.alive]

        while len(self.particles) < DEFAULT_PARTICLES and len(self.particles) < MAX_PARTICLES:
            self.spawn_particle(self.spawn_mode)

    def update_particle(self, particle: Particle, dt: float) -> None:
        center = self.black_hole.position
        offset = center - particle.position
        radius_sq = max(offset.length_squared(), SOFTENING)
        radius = math.sqrt(radius_sq)
        direction = offset / radius

        gravitational_strength = self.black_hole.mass / radius_sq
        acceleration = direction * gravitational_strength

        swirl = direction.perpendicular() * (self.black_hole.mass / max(radius_sq * radius * 0.42, 1.0))
        particle.velocity = particle.velocity + (acceleration + swirl) * (dt * 60.0)
        particle.velocity = particle.velocity.clamp_length(13.0)

        particle.position = particle.position + particle.velocity * (dt * 60.0)
        particle.age += dt
        particle.energy = min(1.0, particle.energy + max(0.0, 1.0 - radius / self.black_hole.accretion_radius) * 0.018)
        particle.remember(TRAIL_LENGTH)

        if radius <= self.black_hole.absorption_radius:
            particle.absorbed = True

    def is_far_outside(self, particle: Particle) -> bool:
        margin = 260.0
        return (
            particle.position.x < -margin
            or particle.position.x > self.width + margin
            or particle.position.y < -margin
            or particle.position.y > self.height + margin
        )

    def burst(self, count: int = 90) -> None:
        center = self.black_hole.position
        for _ in range(count):
            angle = self.rng.uniform(0.0, math.tau)
            radius = self.rng.uniform(self.black_hole.event_horizon_radius * 1.2, self.black_hole.accretion_radius * 0.75)
            position = center + from_angle(angle, radius)
            velocity = from_angle(angle, self.rng.uniform(2.0, 6.5))
            self.particles.append(
                Particle(
                    position=position,
                    velocity=velocity,
                    mass=self.rng.uniform(0.4, 1.1),
                    radius=self.rng.uniform(1.1, 2.4),
                    energy=1.0,
                )
            )

    def stats(self) -> SimulationStats:
        if self.particles:
            average_energy = sum(particle.energy for particle in self.particles) / len(self.particles)
        else:
            average_energy = 0.0

        return SimulationStats(
            particles=len(self.particles),
            absorbed_total=self.absorbed_total,
            shockwaves=len(self.shockwaves),
            spawn_mode=self.spawn_mode,
            average_energy=average_energy,
            frame=self.frame,
        )
