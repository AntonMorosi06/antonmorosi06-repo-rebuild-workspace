from space_invaders_pygame.core import Bullet, SpaceInvadersGame
from space_invaders_pygame.config import BULLET_HEIGHT, BULLET_WIDTH


def test_game_initializes_wave():
    game = SpaceInvadersGame(seed=1)

    assert len(game.live_aliens()) == 50
    assert game.player.lives == 3
    assert game.score == 0
    assert not game.game_over


def test_player_moves_within_bounds():
    game = SpaceInvadersGame(seed=1)
    start_x = game.player.x

    game.move_player(-1)

    assert game.player.x < start_x

    for _ in range(200):
        game.move_player(-1)

    assert game.player.x >= 8


def test_player_shoot_creates_bullet_and_cooldown():
    game = SpaceInvadersGame(seed=1)

    result = game.player_shoot()

    assert result
    assert len(game.player_bullets) == 1
    assert game.player.cooldown > 0


def test_player_bullet_can_destroy_alien():
    game = SpaceInvadersGame(seed=1)
    alien = game.live_aliens()[0]
    game.player_bullets.append(
        Bullet(
            x=alien.x,
            y=alien.y,
            width=BULLET_WIDTH,
            height=BULLET_HEIGHT,
            velocity_y=-9.0,
            owner="player",
        )
    )

    game.handle_collisions()

    assert not alien.alive
    assert game.score > 0


def test_alien_bullet_can_hit_player():
    game = SpaceInvadersGame(seed=1)
    player = game.player
    game.alien_bullets.append(
        Bullet(
            x=player.x,
            y=player.y,
            width=BULLET_WIDTH,
            height=BULLET_HEIGHT,
            velocity_y=5.0,
            owner="alien",
        )
    )

    lives_before = player.lives
    game.handle_collisions()

    assert player.lives == lives_before - 1


def test_wave_clear_advances_level():
    game = SpaceInvadersGame(seed=1)

    for alien in game.aliens:
        alien.alive = False

    old_level = game.level
    game.check_wave_state()

    assert game.level == old_level + 1
    assert len(game.live_aliens()) == 50


def test_state_summary_contains_expected_keys():
    game = SpaceInvadersGame(seed=1)
    summary = game.state_summary()

    assert "score" in summary
    assert "level" in summary
    assert "live_aliens" in summary
