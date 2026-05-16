from __future__ import annotations

from dataclasses import dataclass, field
import random

from .config import (
    ALIEN_COLS,
    ALIEN_HEIGHT,
    ALIEN_ROWS,
    ALIEN_START_X,
    ALIEN_START_Y,
    ALIEN_WIDTH,
    ALIEN_X_SPACING,
    ALIEN_Y_SPACING,
    BULLET_HEIGHT,
    BULLET_WIDTH,
    PLAYER_FIRE_COOLDOWN,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)


@dataclass
class RectEntity:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def intersects(self, other: "RectEntity") -> bool:
        return not (
            self.right < other.left
            or self.left > other.right
            or self.bottom < other.top
            or self.top > other.bottom
        )


@dataclass
class Bullet(RectEntity):
    velocity_y: float
    owner: str


@dataclass
class Alien(RectEntity):
    row: int
    col: int
    alive: bool = True


@dataclass
class Player(RectEntity):
    lives: int = 3
    cooldown: int = 0


@dataclass
class SpaceInvadersGame:
    width: int = WORLD_WIDTH
    height: int = WORLD_HEIGHT
    seed: int | None = None
    player: Player = field(init=False)
    aliens: list[Alien] = field(default_factory=list)
    player_bullets: list[Bullet] = field(default_factory=list)
    alien_bullets: list[Bullet] = field(default_factory=list)
    alien_direction: int = 1
    alien_speed: float = 1.0
    alien_drop: float = 22.0
    alien_fire_chance: float = 0.006
    score: int = 0
    level: int = 1
    frame: int = 0
    game_over: bool = False
    paused: bool = False
    victory: bool = False

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.reset()

    def reset(self) -> None:
        self.player = Player(
            x=self.width / 2 - PLAYER_WIDTH / 2,
            y=self.height - 56,
            width=PLAYER_WIDTH,
            height=PLAYER_HEIGHT,
            lives=3,
            cooldown=0,
        )
        self.aliens = []
        self.player_bullets = []
        self.alien_bullets = []
        self.alien_direction = 1
        self.alien_speed = 1.0
        self.alien_fire_chance = 0.006
        self.score = 0
        self.level = 1
        self.frame = 0
        self.game_over = False
        self.paused = False
        self.victory = False
        self.spawn_wave()

    def spawn_wave(self) -> None:
        self.aliens = []
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLS):
                self.aliens.append(
                    Alien(
                        x=ALIEN_START_X + col * ALIEN_X_SPACING,
                        y=ALIEN_START_Y + row * ALIEN_Y_SPACING,
                        width=ALIEN_WIDTH,
                        height=ALIEN_HEIGHT,
                        row=row,
                        col=col,
                        alive=True,
                    )
                )
        self.player_bullets.clear()
        self.alien_bullets.clear()

    def live_aliens(self) -> list[Alien]:
        return [alien for alien in self.aliens if alien.alive]

    def move_player(self, direction: int) -> None:
        if self.game_over or self.paused:
            return
        self.player.x += PLAYER_SPEED * direction
        self.player.x = max(8, min(self.width - self.player.width - 8, self.player.x))

    def player_shoot(self) -> bool:
        if self.game_over or self.paused:
            return False
        if self.player.cooldown > 0:
            return False
        self.player.cooldown = PLAYER_FIRE_COOLDOWN
        self.player_bullets.append(
            Bullet(
                x=self.player.center_x - BULLET_WIDTH / 2,
                y=self.player.y - BULLET_HEIGHT,
                width=BULLET_WIDTH,
                height=BULLET_HEIGHT,
                velocity_y=-9.0,
                owner="player",
            )
        )
        return True

    def alien_shoot(self) -> bool:
        live = self.live_aliens()
        if not live:
            return False

        if self.rng.random() > self.alien_fire_chance:
            return False

        bottom_aliens_by_col: dict[int, Alien] = {}
        for alien in live:
            previous = bottom_aliens_by_col.get(alien.col)
            if previous is None or alien.y > previous.y:
                bottom_aliens_by_col[alien.col] = alien

        shooter = self.rng.choice(list(bottom_aliens_by_col.values()))
        self.alien_bullets.append(
            Bullet(
                x=shooter.center_x - BULLET_WIDTH / 2,
                y=shooter.bottom,
                width=BULLET_WIDTH,
                height=BULLET_HEIGHT,
                velocity_y=5.2 + self.level * 0.25,
                owner="alien",
            )
        )
        return True

    def update(self) -> None:
        if self.game_over or self.paused:
            return

        self.frame += 1
        if self.player.cooldown > 0:
            self.player.cooldown -= 1

        self.update_player_bullets()
        self.update_aliens()
        self.update_alien_bullets()
        self.handle_collisions()
        self.alien_shoot()
        self.check_wave_state()

    def update_player_bullets(self) -> None:
        for bullet in self.player_bullets:
            bullet.y += bullet.velocity_y
        self.player_bullets = [bullet for bullet in self.player_bullets if bullet.bottom > 0]

    def update_alien_bullets(self) -> None:
        for bullet in self.alien_bullets:
            bullet.y += bullet.velocity_y
        self.alien_bullets = [bullet for bullet in self.alien_bullets if bullet.y < self.height]

    def update_aliens(self) -> None:
        live = self.live_aliens()
        if not live:
            return

        left = min(alien.left for alien in live)
        right = max(alien.right for alien in live)
        speed = self.alien_speed + (self.level - 1) * 0.18 + (ALIEN_ROWS * ALIEN_COLS - len(live)) * 0.018

        should_drop = False
        if right + speed * self.alien_direction > self.width - 24:
            should_drop = True
        if left + speed * self.alien_direction < 24:
            should_drop = True

        if should_drop:
            self.alien_direction *= -1
            for alien in live:
                alien.y += self.alien_drop
        else:
            for alien in live:
                alien.x += speed * self.alien_direction

        if any(alien.bottom >= self.player.y for alien in live):
            self.game_over = True

    def handle_collisions(self) -> None:
        for bullet in list(self.player_bullets):
            for alien in self.live_aliens():
                if bullet.intersects(alien):
                    alien.alive = False
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    self.score += 10 + alien.row * 5
                    break

        for bullet in list(self.alien_bullets):
            if bullet.intersects(self.player):
                if bullet in self.alien_bullets:
                    self.alien_bullets.remove(bullet)
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.game_over = True
                break

    def check_wave_state(self) -> None:
        if self.game_over:
            return

        if not self.live_aliens():
            self.level += 1
            self.score += 150
            self.alien_speed += 0.25
            self.alien_fire_chance = min(0.035, self.alien_fire_chance + 0.0025)
            self.spawn_wave()

    def state_summary(self) -> dict[str, object]:
        return {
            "score": self.score,
            "level": self.level,
            "lives": self.player.lives,
            "live_aliens": len(self.live_aliens()),
            "player_bullets": len(self.player_bullets),
            "alien_bullets": len(self.alien_bullets),
            "frame": self.frame,
            "game_over": self.game_over,
            "paused": self.paused,
        }
